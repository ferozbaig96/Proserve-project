import json
import boto3

def lambda_handler(event, context):
    
    for record in event['Records']:
    	

    	
    s3dataArray = 
    event["Records"][0]["body"]
    
    return {
        'statusCode': 200,
        'body': json.dumps(bodydata)
    }
