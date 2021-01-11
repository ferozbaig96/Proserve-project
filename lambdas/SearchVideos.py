import json
import boto3
import time

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

def search_data(query, limit):
    # sql = f"""
    #     SELECT * FROM (
    #       SELECT * FROM {table_name}, plainto_tsquery('{query}') AS q
    #       WHERE (tsv @@ q)
    #     ) AS t1 ORDER BY ts_rank_cd(t1.tsv, plainto_tsquery('{query}')) DESC LIMIT {limit};
    #     """
    sql = f"""
        SELECT object_key FROM {table_name}, plainto_tsquery('{query}') AS q
        WHERE (tsv @@ q)
        ORDER BY created_on DESC LIMIT {limit};
        """
    response = execute_statement(sql)
    return response

def lambda_handler(event, context):
    
    global rds_client, database_name, table_name, db_cluster_arn, db_credentials_secrets_store_arn
    rds_client = boto3.client('rds-data')
    database_name = fetch_ssm_parameter('ProserveProject_database_name', True)
    table_name = fetch_ssm_parameter('ProserveProject_table_name', True)
    db_cluster_arn = fetch_ssm_parameter('ProserveProject_db_cluster_arn', True)
    db_credentials_secrets_store_arn = fetch_ssm_parameter('ProserveProject_db_credentials_secrets_store_arn', True)
    
    query = event['queryStringParameters']['query'].strip()
    LIMIT = 20
    result = search_data(query, LIMIT)
    
    response = []
    bucketName = fetch_ssm_parameter('ProserveProject_S3BucketName', True)
    for record in result['records']:
        objectKey = record[0]['stringValue']
        response.append({
            'name':objectKey
            })
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,GET'
        },
        'body': json.dumps(response)
    }
