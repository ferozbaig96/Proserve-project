import json
import boto3
import time
import hashlib
import os
import cfnresponse

rds_client = boto3.client('rds-data')

# def fetch_ssm_parameter(parameter, isEncrypted):
#     ssmClient = boto3.client('ssm')
#     response = ssmClient.get_parameter(
#             Name = parameter,
#             WithDecryption = isEncrypted)
#     return response['Parameter']['Value']

# Timing function executions
def timeit(f):
    def timed(*args, **kw):
        ts = time.time()
        result = f(*args, **kw)
        te = time.time()
        print(f"""
            Function: {f.__name__}
            *  args: {args}
            *  kw: {kw}
            *  execution time: {(te-ts)*1000:8.2f} ms
            """)
        return result
    return timed

@timeit
def execute_statement(sql, sql_parameters=[]):
    response = rds_client.execute_statement(
        secretArn=db_credentials_secrets_store_arn,
        database=database_name,
        resourceArn=db_cluster_arn,
        sql=sql,
        parameters=sql_parameters
    )
    return response

def create_table():
    sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
        id                  VARCHAR(256)     PRIMARY KEY,
        object_key          TEXT            NOT NULL,
        object_size_bytes   NUMERIC         NOT NULL,
        created_on          CHAR(24)        NOT NULL
        ) ;
        """
    response = execute_statement(sql)
    return response

def add_FTS_to_table():
    sql = f"""
        ALTER TABLE {table_name} ADD COLUMN tsv tsvector;
        
        CREATE INDEX tsv_idx ON {table_name} USING gin(tsv);
        
        CREATE FUNCTION documents_search_trigger() RETURNS trigger AS $$
        begin
          new.tsv :=
            setweight(to_tsvector(regexp_replace(new.object_key, '[^\w]+', ' ', 'gi')), 'A');
          return new;
        end
        $$ LANGUAGE plpgsql;
        
        CREATE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE
        ON {table_name} FOR EACH ROW EXECUTE PROCEDURE documents_search_trigger();
        """
        
    response = execute_statement(sql)
    return response

def lambda_handler(event, context):

    if event['RequestType'] != 'Create':
        return {
            'statusCode': 204,
        }
    
    global database_name, table_name, db_cluster_arn, db_credentials_secrets_store_arn
    # database_name = fetch_ssm_parameter('ProserveProject_database_name', True)
    # table_name = fetch_ssm_parameter('ProserveProject_table_name', True)
    # db_cluster_arn = fetch_ssm_parameter('ProserveProject_db_cluster_arn', True)
    # db_credentials_secrets_store_arn = fetch_ssm_parameter('ProserveProject_db_credentials_secrets_store_arn', True)
    database_name = os.environ['DB_NAME']
    table_name = os.environ['DB_TABLE_NAME']
    db_cluster_arn = os.environ['DB_CLUSTER_ARN']
    db_credentials_secrets_store_arn = os.environ['DB_CREDENTIALS_STORE_ARN']
    
    create_table()
    add_FTS_to_table()
    
    responseData = {}
    cfnresponse.send(event, context, SUCCESS, responseData)
    
    return {
        'statusCode': 204,
    }
