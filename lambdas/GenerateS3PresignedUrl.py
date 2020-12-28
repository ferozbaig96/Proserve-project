import json
import boto3
from botocore.exceptions import ClientError

def get_bucket_name():
    ssmClient = boto3.client('ssm')
    response = ssmClient.get_parameter(
            Name = 'ProserveProject_S3BucketName',
            WithDecryption = True)
    return response['Parameter']['Value']

def lambda_handler(event, context):
    
    s3Client = boto3.client('s3')
    
    try:
        bucketName = get_bucket_name()
    except ClientError as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps("An error occurred")
        }

    URL_EXPIRATION_SECONDS = 150
    
    objectKey = event['queryStringParameters']['filename'].strip()
    contentType = event['queryStringParameters']['contentType'].strip()
    
    response = s3Client.generate_presigned_url('put_object',
        Params = {
            'Bucket': bucketName,
            'Key': objectKey,
            'ACL': 'public-read',
            'ContentType': contentType
        },
        ExpiresIn = URL_EXPIRATION_SECONDS)
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,GET'
        },
        'body': json.dumps(response)
    }
