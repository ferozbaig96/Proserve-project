# Postgres Commands

-- show databases
\l

-- create table
CREATE TABLE IF NOT EXISTS videos (
    id                  VARCHAR(64)     PRIMARY KEY,
    object_key          TEXT        	NOT NULL,
    object_size_bytes   NUMERIC     	NOT NULL,
    created_on          CHAR(24)    	NOT NULL
);

-- show tables
\d

-- delete table
DROP TABLE videos;

-- insert data into table
-- NOTE: single quotes to be used for string literals
INSERT INTO videos (id, object_key, object_size_bytes, created_on)
    VALUES ('123', 'abc', 1024, '2020-12-25T17:36:49.945Z');

INSERT INTO videos (id, object_key, object_size_bytes, created_on)
    VALUES ('456', 'def', 2048, 'DEF');

-- upsert data (overwrite data)
INSERT INTO videos (id, object_key, object_size_bytes, created_on)
    VALUES ('456', 'xyz', 256, 'XYZ')
	ON CONFLICT (id)
	DO UPDATE SET object_size_bytes = EXCLUDED.object_size_bytes, created_on = EXCLUDED.created_on ;

-- select data from table
SELECT * FROM videos ;

-- delete data from table
DELETE FROM videos
WHERE id='456';

-- delete all entries from table
TRUNCATE videos;

--------------------
# Full Text Search

#> https://blog.lateral.io/2015/05/full-text-search-in-milliseconds-with-postgresql/
#> https://www.compose.com/articles/mastering-postgresql-tools-full-text-search-and-phrase-search/
#> https://www.enterprisedb.com/postgres-tutorials/indexing-documents-full-text-search-postgresql
#> https://hevodata.com/blog/postgresql-full-text-search-setup/

-- To create the column for the tsvector values:
ALTER TABLE videos ADD COLUMN tsv tsvector;

-- And then to create the index on this column:
CREATE INDEX tsv_idx ON videos USING gin(tsv);

-- In this example, I am assuming a table with the structure with a 'text' column and a 'meta' column that contains a JSON object with a 'title'. To populate the tsv column with tsvectors, run the following:
-- 
-- UPDATE table_name SET tsv = setweight(to_tsvector(coalesce(meta->>'title','')), 'A') || setweight(to_tsvector(coalesce(text,'')), 'D');
-- 
-- This query gets the title from the meta JSON column and gives it the heighest weight of A. Then it gets the text value and weights it D. Then it combines the two tsvectors and writes them to the tsv column we just created.
-- 
UPDATE videos SET tsv = setweight(to_tsvector(coalesce(object_key,'')), 'A');

-- At this point, if your data was static you could stop and start querying. But we want all future rows and updates to have up-to-date tsv columns so we need to create a trigger to do this. Firstly, you’ll need to create a function to take a column and update the tsv column:
-- P.S. This is similar to UPDATE query, but as a function
-- 
-- CREATE FUNCTION documents_search_trigger() RETURNS trigger AS $$
-- begin
--   new.tsv :=
--     setweight(to_tsvector(coalesce(new.meta->>'title','')), 'A') ||
--     setweight(to_tsvector(coalesce(new.text,'')), 'D');
--   return new;
-- end
-- $$ LANGUAGE plpgsql;
-- 
CREATE FUNCTION documents_search_trigger() RETURNS trigger AS $$
begin
  new.tsv :=
    setweight(to_tsvector(coalesce(new.object_key,'')), 'A');
  return new;
end
$$ LANGUAGE plpgsql;

-- Now you need to create a trigger to execute that function when any row is updated or inserted:
CREATE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE
ON videos FOR EACH ROW EXECUTE PROCEDURE documents_search_trigger();

-- Adding some data
INSERT INTO videos
VALUES
	('1', 'Big Brown Fox', 1024, '2020-12-25T17:36:49.945Z'),
	('2', 'Brownies baked right but fox ate them all', 2048, '2020-12-25T17:36:49.945Z'),
	('3', 'Right way to cut a baked cake while running', 512, '2020-12-25T17:36:49.945Z'),
	('4', 'Running into a gate', 256, '2020-12-25T17:36:49.945Z')
;

-- Now you can search the database. Replace both occurences of YOUR QUERY text with what you want to search and run the following query:
-- 
-- SELECT id, meta->>'title' as title, meta FROM (
--   SELECT id, meta, tsv
--   FROM data_rows, plainto_tsquery('YOUR QUERY') AS q
--   WHERE (tsv @@ q)
-- ) AS t1 ORDER BY ts_rank_cd(t1.tsv, plainto_tsquery('YOUR QUERY')) DESC LIMIT 5;
-- 

  SELECT *
  FROM videos, plainto_tsquery('YOUR QUERY') AS q
  WHERE (tsv @@ q);

  SELECT *
  FROM videos, plainto_tsquery('baked fox') AS q
  WHERE (tsv @@ q);

SELECT * FROM (
  SELECT *
  FROM videos, plainto_tsquery('baked fox') AS q
  WHERE (tsv @@ q)
) AS t1 ORDER BY ts_rank_cd(t1.tsv, plainto_tsquery('baked fox')) DESC LIMIT 20;

-- This query performs two queries; firstly it performs the search on the indexed tsv column. Then it ranks and sorts those results and returns 20.
-- 
-- 

TRUNCATE videos;

INSERT INTO videos
VALUES
	('1', 'A fat cat sat on a mat and ate a fat rat', 1, 'date'),
	('2', 'You are so fat', 2, 'date'),
	('3', 'My mat is so fat', 3, 'date'),
	('4', 'Amazing rat dance', 4, 'date'),
	('5', 'I sat on a mat', 5, 'date'),
	('6', 'Father called for a mat', 6, 'date'),
	('7', 'Plural form - cats on a single mat', 7, 'date')
;

  SELECT *
  FROM videos, plainto_tsquery('fat mat') AS q
  WHERE (tsv @@ q);

-- See the ranking in action here
SELECT * FROM (
  SELECT *
  FROM videos, plainto_tsquery('fat mat') AS q
  WHERE (tsv @@ q)
) AS t1 ORDER BY ts_rank_cd(t1.tsv, plainto_tsquery('fat mat')) DESC LIMIT 20;

-- Plural form
  SELECT *
  FROM videos, plainto_tsquery('cat') AS q
  WHERE (tsv @@ q);
