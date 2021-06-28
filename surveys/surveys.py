import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('surveys')

def list_surveys():
    surveys = table.scan()['Items']
    return {
        "statusCode": 200,
        "body": json.dumps(surveys),
    }

def get_survey(id):
    response = table.get_item(Key={"id": id })
    print(f'returned survey ---> {response}')
    if('Item' in response):
        return {
            "statusCode": 200,
            "body": json.dumps(response['Item']),
        }
    else:
        return {
            "statusCode": 404,
            "body": f"No item found with the given id: {id}",
        }



# def json_response(data, response_code=200):
#     return json.dumps(data), response_code, {'Content-Type': 'application/json'}

def create_survey(newSurvey):
    survey = table.put_item(Item=newSurvey)
    # response = table.put_item(
    #    Item={
    #         'year': year,
    #         'title': title,
    #         'info': {
    #             'plot': plot,
    #             'rating': rating
    #         }
    #     }
    # )
    return {
        "statusCode": 200,
        "body": "item created",
    }

def surveys_handler(event, context):
    print(f'event ---> {event}')
    if(event['httpMethod'] == 'GET'):
        pathParams = event['pathParameters']
        if(pathParams is not None and "id" in pathParams):
            return get_survey(pathParams['id'])
        else:
            return list_surveys()
    elif(event['httpMethod']== 'POST'):
        return create_survey(json.loads(event['body']))
