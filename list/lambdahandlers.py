from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import uuid
import os
from botocore.exceptions import ClientError

endpoint_override = os.environ['ENDPOINT_OVERRIDE']

if not endpoint_override:
	dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
else:
	dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url=endpoint_override)

table_name = "Items"

# dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="http://dynamodb:8000")

def respond(err, response=None):
	return {
		"statusCode": 400 if err else 200,
		"body": err if err else json.dumps(response),
		"headers": {
			'Content-Type': 'application/json',
		},
	}
			
def get_items(event,context): 
	table = client.Table(table_name)

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

def get_item(event,context):
	
	try:
		listName = event['pathParameters']['listName']
	except KeyError:
		return respond('listName not found in path parameter.')
		
	table = dynamodb.Table(table_name)

	try:
		response = table.get_item(
			Key={
				'ItemID': ItemID,
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
	
	
def add_item(event,context):
	try:
		requestBody = json.loads(event['body'])
		ItemName = requestBody['ItemName']
	except KeyError:
		return respond('Request is not properly formatted.')
		
	table = dynamodb.Table(table_name)
	
	messageData = {
		'ItemID': str(uuid.uuid4()),
		'ItemName': str(ItemName)
	}

	try:
		response = table.put_item(Item=messageData) 
	except ClientError as e:
		return str(e)
		print(e.response['Error']['Message'])
	else:
		return respond(None,messageData)

		
def delete_item(event,context):
	
	try:
		listName = event['pathParameters']['listName']
	except KeyError:
		return respond('Request is not properly formatted.')
		
	table = dynamodb.Table(table_name)
	
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

	
def create_items_table_old(event,context):
	return respond(None,'hello')
	
def create_items_table(event,context):
	try:
		table = dynamodb.create_table(
			TableName=table_name,
			KeySchema=[
				{
					'AttributeName': 'ItemID',
					'KeyType': 'HASH'
				},
				{
					'AttributeName': 'ItemName',
					'KeyType': 'RANGE'
				},
			],
			AttributeDefinitions=[
				{
					'AttributeName': 'ItemID',
					'AttributeType': 'S'
				},
				{
					'AttributeName': 'ItemName',
					'AttributeType': 'S'
				},

			],
			ProvisionedThroughput={
				'ReadCapacityUnits': 1,
				'WriteCapacityUnits': 1
			}
		)
		
		# Wait until the table exists.
		dynamodb.meta.client.get_waiter('table_exists').wait(TableName=table_name)
		
		return respond(None,'Table created successfully.')

	except dynamodb.meta.client.exceptions.ResourceInUseException:
		return respond(None,'Table already exists.')
	except:
		return respond(None,'Unable to create table.  Unknown error.')

	
def list_tables(event,context):
	listoftables = dynamodb.list_tables()
	return respond(None,listoftables)
	
	
def hello(event,context):
	return respond(None,'hello')
	
if __name__ == "__main__":
	print("yeah baby")
	create_items_table(None, None)

	
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