import json
import urllib3
import jwt

def lambda_handler(event, context):
    
    code = event['queryStringParameters']['code']
    
    # TODO change
    TOKEN_ENDPOINT = 'https://auth-userpool.swatcat.ml/oauth2/token'
    CLIENT_ID = 'r6idl4n64lotv1ijlvpv5sb0f'
    REDIRECT_URI = 'https://example.com/'
    
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = f'grant_type=authorization_code&client_id={CLIENT_ID}&code={code}&redirect_uri={REDIRECT_URI}'
    
    http = urllib3.PoolManager()
    response = http.request('POST', TOKEN_ENDPOINT, headers=headers, body=payload)
    
    decoded_response_json = json.loads(response.data.decode('utf-8'))
    
    # todo redirect back to login page
    if 'error' in decoded_response_json:
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,GET'
            },
            'body': json.dumps(decoded_response_json)
        }
    
    id_token = decoded_response_json['id_token']
    decoded_id_token = jwt.decode(id_token, options={"verify_signature": False})
    
    if 'cognito:groups' in decoded_id_token:
        if 'admin' in decoded_id_token['cognito:groups']:
            return {
                'statusCode': 302,
                'headers': {
                    'Location': 'http://localhost/web/admin.html',
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,GET'
                }
            }
    
    return {
        'statusCode': 302,
        'headers': {
            'Location': 'http://localhost/web',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,GET'
        }
    }