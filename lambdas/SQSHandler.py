import json
import boto3
import time
import hashlib

rds_client = boto3.client('rds-data')

def fetch_ssm_parameter(parameter, isEncrypted):
    ssmClient = boto3.client('ssm')
    response = ssmClient.get_parameter(
            Name = parameter,
            WithDecryption = isEncrypted)
    return response['Parameter']['Value']

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

def upsert_data(objectKeyHash, objectKey, objectSize, eventTime):
    sql = f"""
        INSERT INTO {table_name} (id, object_key, object_size_bytes, created_on)
        VALUES ('{objectKeyHash}', '{objectKey}', {objectSize}, '{eventTime}')
        ON CONFLICT (id)
        DO UPDATE SET object_size_bytes = EXCLUDED.object_size_bytes, created_on = EXCLUDED.created_on ;
        """
    response = execute_statement(sql)
    return response

def delete_data(objectKeyHash):
    sql = f"""
        DELETE FROM {table_name}
        WHERE id = '{objectKeyHash}' ;
        """
    response = execute_statement(sql)
    return response

def lambda_handler(event, context):
    
    global database_name, table_name, db_cluster_arn, db_credentials_secrets_store_arn
    database_name = fetch_ssm_parameter('ProserveProject_database_name', True)
    table_name = fetch_ssm_parameter('ProserveProject_table_name', True)
    db_cluster_arn = fetch_ssm_parameter('ProserveProject_db_cluster_arn', True)
    db_credentials_secrets_store_arn = fetch_ssm_parameter('ProserveProject_db_credentials_secrets_store_arn', True)

    for record in event['Records']:
        s3record = json.loads(record['body'])['Records'][0]
        
        eventName = s3record['eventName']
        print(eventName)
        
        if eventName.startswith('ObjectCreated'):
            eventTime = s3record['eventTime']
            objectKey = s3record['s3']['object']['key']
            objectSize = s3record['s3']['object']['size']
            objectKeyHash = hashlib.sha256(bytes(f'{objectKey}', encoding='utf-8')).hexdigest()
            
            result = create_table()
            print(result)
            if result['ResponseMetadata']['HTTPStatusCode'] == 200:
                print(upsert_data(objectKeyHash, objectKey, objectSize, eventTime))
        else:
            objectKey = s3record['s3']['object']['key']
            objectKeyHash = hashlib.sha256(bytes(f'{objectKey}', encoding='utf-8')).hexdigest()
            print(delete_data(objectKeyHash))
    
    return {
        'statusCode': 204,
    }
