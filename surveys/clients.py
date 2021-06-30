import json
import boto3

dynamodb = boto3.resource('dynamodb')
clients_table = dynamodb.Table('clients')
surveys_table = dynamodb.Table('surveys')

def list_clients():
    clients = clients_table.scan()['Items']
    return {
        "statusCode": 200,
        "body": json.dumps(clients),
    }

def get_one_client(client_id):
    response = clients_table.get_item(Key={"client_id": client_id, 'survey_id': '0' })
    if('Item' in response):
        return {
            "statusCode": 200,
            "body": json.dumps(response['Item']),
        }
    else:
        return {
            "statusCode": 404,
            "body": f"No client found with the given id: {client_id}",
        }

def get_one_client_survey(client_id, survey_id):
    response = clients_table.get_item(Key={'client_id': client_id, 'survey_id': survey_id })
    print(f'returned survey ---> {response}')
    if('Item' in response):
        return {
            "statusCode": 200,
            "body": json.dumps(response['Item']),
        }
    else:
        return {
            "statusCode": 404,
            "body": f"No item found with the given id: {survey_id}",
        }

# def json_response(data, response_code=200):
#     return json.dumps(data), response_code, {'Content-Type': 'application/json'}

def create_client(newClient):
    client = clients_table.put_item(Item=newClient)
    return {
        "statusCode": 200,
        "body": "Client created",
    }

def attach_survey_to_client(client_id, survey_id):
    response = clients_table.get_item(Key={'client_id': client_id, 'survey_id': '0' })
    if('Item' not in response):
        return {
            "statusCode": 404,
            "body": f"No client found with the given id: {client_id}",
        }
    response = surveys_table.get_item(Key={"id": survey_id })
    if('Item' not in response):
        return {
            "statusCode": 404,
            "body": f"No survey found with the given id: {client_id}",
        }
    survey = response['Item']

    response = clients_table.update_item(
        Key={
                'client_id': client_id,
                'survey_id': survey['id']
            },
        UpdateExpression="set survey = :survey",
        ExpressionAttributeValues={
                ':survey': survey
            },
        ReturnValues="UPDATED_NEW"
        )
    return {
        "statusCode": 200,
        "body": response,
    }

def clients_handler(event, context):
    print(f'event ---> {event}')
    pathParams = event['pathParameters']
    if(event['httpMethod'] == 'GET'):
        if(pathParams is None):
            return list_clients();
        if('client_id' not in pathParams):
            return {
                "statusCode": 400,
                "body": "Client is required field",
            }
        if('survey_id' in pathParams):
            return get_one_client_survey(pathParams['client_id'], pathParams['survey_id'])
        else:
            return get_one_client(pathParams['client_id'])

    elif(event['httpMethod']== 'POST'):
        return create_client(json.loads(event['body']))

    elif(event['httpMethod']== 'PUT'):
        return attach_survey_to_client(pathParams['client_id'], pathParams['survey_id'])
