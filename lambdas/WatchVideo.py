import json
import boto3
from botocore.exceptions import ClientError
from urllib.parse import urlsplit

def get_bucket_name():
    ssmClient = boto3.client('ssm')
    response = ssmClient.get_parameter(
            Name = 'ProserveProject_S3BucketName',
            WithDecryption = True)
    return response['Parameter']['Value']

def lambda_handler(event, context):
    
    sess = boto3.session.Session(region_name="us-east-1")
    s3Client = sess.client('s3', config= boto3.session.Config(signature_version='s3v4'))
    
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
    
    url = s3Client.generate_presigned_url('get_object',
        Params = {
            'Bucket': bucketName,
            'Key': objectKey,
            # 'ACL': 'public-read',
        },
        ExpiresIn = URL_EXPIRATION_SECONDS)
    
    bucket_url = '{uri.scheme}://{uri.netloc}'.format(uri=urlsplit(url))
    BASE_URL = 'https://project.baigmohd.myinstance.com'
    url = url.replace(bucket_url, BASE_URL)
    
    return {
        'statusCode': 302,
        'headers': {
            'Location': url,
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,GET'
        },
    }
