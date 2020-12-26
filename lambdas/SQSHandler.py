import json
import boto3
import time
import hashlib

database_name = 'video_db'
table_name = 'videos'
db_cluster_arn = 'arn:aws:rds:us-east-1:784439035548:cluster:serve-db-cluster'
db_credentials_secrets_store_arn = 'arn:aws:secretsmanager:us-east-1:784439035548:secret:serve-project/database-o1hKSq'

rds_client = boto3.client('rds-data')

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
