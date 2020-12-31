import json
import urllib3

def lambda_handler(event, context):
    
    try:
        global code
        code = event['queryStringParameters']['code']
    except Exception as e:
        return {
            'statusCode': 401,
            'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,GET'
            },
        }
    
    TOKEN_ENDPOINT = 'https://auth-userpool.swatcat.ml/oauth2/token'
    CLIENT_ID = 'r6idl4n64lotv1ijlvpv5sb0f'
    REDIRECT_URI = 'https://lk7kafdzwf.execute-api.us-east-1.amazonaws.com/dev/token'
    
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = f'grant_type=authorization_code&client_id={CLIENT_ID}&code={code}&redirect_uri={REDIRECT_URI}'
    
    http = urllib3.PoolManager()
    response = http.request('POST', TOKEN_ENDPOINT, headers=headers, body=payload)
    
    return {
    # TODO redirect
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,GET'
        },
        'body': response.data.decode('utf-8')
    }