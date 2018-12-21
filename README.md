SAM Example
===========

This is an example shopping-list application that leverages AWS's SAM (Serverless Application Model) framework. 

SAM is a framework for building serverless applications on AWS.  Consists of 1) AWS SAM template spec and 2) AWS SAM CLI.  The templates are CloudFormation templates (with a Serverless Transform macro that transforms these into full CFN templates).

## Prerequisites

* Docker
* Python 3.6
* AWS CLI
* SAM CLI (installed via Pip)

## Create a Docker network
Create a Docker network since both the SAM local docker container and the DynamoDB local container must be in the same network.

````
docker network create lambda-local
````

## Start up local DynamoDB container
````
docker run -p 8000:8000 --network lambda-local --name dynamodb amazon/dynamodb-local
````

OR if you've already created the container….

'docker start dynamodb'

## Install Dependencies
Create a build directory inside "list" and install packages defined in requirements.txt.  The build directory contains the source code and the Python packages that are loaded by SAM Local.

`pip install -r .\requirements.txt -t build`

## Copy source files to build directory 
Copy source files to build directory in order to deploy them.

## Test API locally
Start up the serverless application using the start-api command.  This creates a local instance of API Gateway that you can use to test HTTP request/response functionality.  It mounts Lambda functions as HTTP paths for invocation via browser, CLI, etc.

````
sam local start-api --template samTemplate.yml --docker-network lambda-local --env-vars test/test_environment_windows.json
````

## Run unit tests
`python ./test/api_tests.py 2`


## Create deployment package
Packages the local artifacts (local paths) that your AWS CloudFormation template references. The command uploads local artifacts, such as source code for an AWS Lambda function or a Swagger file for an AWS API Gateway REST API, to an S3 bucket. The command returns a copy of your template, replacing references to local artifacts with the S3 location where the command uploaded the artifacts


````
sam package --template-file samTemplate.yml --output-template-file packaged.yaml --s3-bucket shoppinglist-sam-matthew.pothier
````

## Deploy application
(alias for aws cloudformation deploy)  Deploys the specified AWS CloudFormation template by creating and then executing a change set.

````
sam deploy --template-file packaged.yaml --stack-name shoppinglist-sam-app --capabilities CAPABILITY_IAM --region us-east-1
````

## View Cloudformation Template Outputs
`aws cloudformation describe-stacks --stack-name shoppinglist-sam-app`


## View Logs
`sam logs -n HelloLambdaFunction --stack-name shoppinglist-sam-app`



