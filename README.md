# Serverless Website

Two kinds of users:
- Admin
    - Can upload file (CREATE/UPDATE or UPSERT)
    - Can read file (READ)
    - Can delete file (DELETE)
    - Can search for file (SEARCH)
- User
    - Can search for file (SEARCH)
    - Can read file (READ)

# Architecture
- CloudFront (CDN)
- Cognito (Authentication)
- S3
    - `media` bucket (stores uploaded files)
    - `www` bucket (stores static web content - html, css, js)
- Regional API Gateway (API server)
- Lambda (backing API Gateway)
- Standard SQS (for Queueing, acting as trigger to S3 `media` Upload/Delete)
- Postgres Aurora Serverless (stores metadata of uploaded files)
- Secrets Manager (stores Aurora Serverless Database credentials secrets)

Refer ArchProserve.png for diagram

## Before running stack

- Ensure that an ACM certificate has been issued in `us-east-1` region for the domain
- Ensure that a VPC exist with atleast 2 private subnets


## While running stack

#### Ensure unique value for
- {MediaBucketPrefix}
- {WwwBucketPrefix}
- {WebsiteDomain}
- {CognitoDomainPrefix}

#### Ensure correct value for
- {VpcIdForDb}
- {PrivateSubnetsForDb}

#### Ensure exists and is having correct value for
- {ACMCertificateIdentifier}


## After creation of stack

- Ensure `auth.js` and `index.js` have correct mapping to {WebsiteDomain} and Cognito clientId
- Ensure {WebsiteDomain} points to created CloudFront Domain


# How to Run stack

## To create package

	sam package   \
	--template-file project-template.yaml   \
	--output-template-file package.yaml   \
	--s3-bucket <s3-bkt-name>

## To deploy package

	sam deploy  \
	--template-file package.yaml  \
	--stack-name pro \
	--capabilities CAPABILITY_AUTO_EXPAND CAPABILITY_IAM \
	--parameter-overrides \
	MediaBucketPrefix=test-media \
	WwwBucketPrefix=test-www \
	WebsiteDomain=project.baigmohd.myinstance.com \
	CognitoDomainPrefix=testing-anksdasnd \
	VpcIdForDb=vpc-8c995af6 \
	PrivateSubnetsForDb=subnet-8b0cbed7,subnet-6720602d \
	DbPassword=somepassword \
	DbClusterIdentifier=video-db-cluster \
	ACMCertificateIdentifier=85936bdd-1860-4704-ab77-63d26f3fdc3d \
	MinimumProtocolVersion=TLSv1 \
	SslSupportMethod=sni-only

or

	`sam deploy  \
	--template-file package.yaml  \
	--stack-name pro \
	--capabilities CAPABILITY_AUTO_EXPAND CAPABILITY_IAM \
	--guided`

