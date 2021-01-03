import json
import urllib3

def lambda_handler(event, context):
    
    code = event['queryStringParameters']['code']
    
    # CloudFront
    BASE_URL = 'https://project.baigmohd.myinstance.com'
    TOKEN_ENDPOINT = BASE_URL + '/oauth2/token'
    # TOKEN_ENDPOINT = 'https://serve.auth.us-east-1.amazoncognito.com/oauth2/token'
    CLIENT_ID = 'r6idl4n64lotv1ijlvpv5sb0f'
    # CloudFront
    REDIRECT_URI = BASE_URL
    # REDIRECT_URI = 'https://lk7kafdzwf.execute-api.us-east-1.amazonaws.com/dev/token'
    # REDIRECT_URI = 'https://example.com/'
    
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = f'grant_type=authorization_code&client_id={CLIENT_ID}&code={code}&redirect_uri={REDIRECT_URI}'
    
    http = urllib3.PoolManager()
    response = http.request('POST', TOKEN_ENDPOINT, headers=headers, body=payload)
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,GET'
        },
        'body': response.data.decode('utf-8')
    }