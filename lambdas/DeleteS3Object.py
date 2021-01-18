import json
import boto3
from botocore.exceptions import ClientError
import os

region = os.environ['AWS_REGION']
sess = boto3.session.Session(region_name=region)

# def get_bucket_name():
#     ssmClient = sess.client('ssm')
#     response = ssmClient.get_parameter(
#             Name = 'ProserveProject_S3BucketName',
#             WithDecryption = True)
#     return response['Parameter']['Value']

def lambda_handler(event, context):
    
    s3Client = sess.client('s3')
    
    # try:
    #     bucketName = get_bucket_name()
    # except ClientError as e:
    #     print(e)
    #     return {
    #         'statusCode': 500,
    #         'body': json.dumps("An error occurred")
    #     }
    bucketName = os.environ['BUCKET_NAME']

    objectKey = json.loads(event['body'])["objectKey"].strip()
    
    response = s3Client.delete_object(
        Bucket = bucketName,
        Key = objectKey,
        VersionId = "null",
    )
    
    return {
        'statusCode': 204,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,DELETE'
        },
    }
