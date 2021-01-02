CloudFront Mappings:

domain			    -> s3
domain/login		-> cognito/login?{query_params}
domain/{path}		-> s3/{path}

api.domain 		    -> api_gw/{stage}
api.domain/{path} 	-> api_gw/{stage}/{path}
