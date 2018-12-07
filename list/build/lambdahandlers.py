
from __future__ import print_function # Python 2/3 compatibility
import boto3
import json

def respond(err, response=None):
	return {
		'statusCode': '400' if err else '200',
		'body': err if err else json.dumps(response),
		'headers': {
			'Content-Type': 'application/json',
		},
	}

def get_lists(event,context):
    # create dynamodb resource object
	client = boto3.resource('dynamodb')

    #  search for dynamoDB table 
	table = client.Table("Lists")

	try:
		response = table.scan()
	except ClientError as e:
		print(e.response['Error']['Message'])
	else:
		items = response['Items']
		return {
		"body": json.dumps(
			{"data": items,
			"success": 'true'}
		)
	}	


def get_list(event,context):
	
	try:
		listName = event['pathParameters']['listName']
	except KeyError:
		return respond('listName not found in path parameter.')
		
	client = boto3.resource('dynamodb')
	table = client.Table("Lists")

	try:
		response = table.get_item(
			Key={
				'Name': listName,
				}
		)
	except ClientError as e:
		print(e.response['Error']['Message'])
	else:
		item = response['Item']
		return {
		"body": json.dumps(
			{"data": item,
			"success": 'true'}
		)
	}	
	
	
def add_list(event,context):
	try:
		requestBody = json.loads(event['body'])
		listName = requestBody['listName']
		storeName = requestBody['storeName']
	except KeyError:
		return respond('Request is not properly formatted.')
		
	client = boto3.resource('dynamodb')
	table = client.Table("Lists")
	
	messageData = {
		'Name': str(listName),
		'Store': str(storeName)
	}

	try:
		response = table.put_item(Item=messageData) 
	except ClientError as e:
		print(e.response['Error']['Message'])
	else:
		return {
		"body": json.dumps(
			{"data": json.dumps(response),
			"success": 'true'}
		)
	}	


def delete_list(event,context):
	
	try:
		listName = event['pathParameters']['listName']
	except KeyError:
		return respond('Request is not properly formatted.')
		
	client = boto3.resource('dynamodb')
	table = client.Table("Lists")
	
	try:
		response = table.delete_item(
			Key={
				'Name': listName,
				}
		)
	except ClientError as e:
		if e.response['Error']['Code'] == "ConditionalCheckFailedException":
			print(e.response['Error']['Message'])
		else:
			raise
	else:
		return {
		"body": json.dumps(
			{"data": json.dumps(response),
			"success": 'true'}
		)
	}	
	
def hello(event,context):
	return {
        "statusCode": 200,
        "body": json.dumps(
            {"message": "hello world"}
        )
	}	

# def lambda_handler(event, context):
    # # TODO implement
    
    # # Because we're using a Cognito User Pools authorizer, all of the claims
    # # included in the authentication token are provided in the request context.
    # # This includes the username as well as other attributes.
    # # username = event.requestContext.authorizer.claims['cognito:username'];
    
    # return add_item(event)
	# # return {
        # # "statusCode": 200,
        # # "body": json.dumps(
            # # {"message": "hello world"}
        # # )
	# # }