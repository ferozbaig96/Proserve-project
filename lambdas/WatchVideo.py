import json
import boto3
from botocore.exceptions import ClientError
import os

# def get_bucket_name():
#     ssmClient = boto3.client('ssm')
#     response = ssmClient.get_parameter(
#             Name = 'ProserveProject_S3BucketName',
#             WithDecryption = True)
#     return response['Parameter']['Value']

def presign_s3(action, bucket, key, expiration):
    sess = boto3.session.Session(region_name="us-east-1")
    s3Client = sess.client('s3', config= boto3.session.Config(signature_version='s3v4'))
    
    params = {
        'Bucket': bucket,
        'Key': key
    }
    
    url = s3Client.generate_presigned_url(action, Params=params, ExpiresIn=expiration)
    return url

def presign_for_cloudfront(cname, bucket, key, expiration):
    s3_url = presign_s3('get_object', bucket, key, expiration)
    cfurl = s3_url.split("?")
    cfurl = "https://" + cname + "/" + key + "?" + cfurl[1] 
    return cfurl

def lambda_handler(event, context):
    
    # try:
    #     bucketName = get_bucket_name()
    # except ClientError as e:
    #     print(e)
    #     return {
    #         'statusCode': 500,
    #         'body': json.dumps("An error occurred")
    #     }
    bucketName = os.environ['BUCKET_NAME']
    
    URL_EXPIRATION_SECONDS = 150
    objectKey = event['queryStringParameters']['filename'].strip()
    CNAME = 'project.baigmohd.myinstance.com'
    
    url = presign_for_cloudfront(CNAME, bucketName, objectKey, URL_EXPIRATION_SECONDS)
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,GET'
        },
        'body': json.dumps(url)
    }
