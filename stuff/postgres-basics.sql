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
