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

# def json_response(data, response_code=200):
#     return json.dumps(data), response_code, {'Content-Type': 'application/json'}

def create_survey(newSurvey):
    survey = table.put_item(newSurvey)
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
        "body": json.dumps(survey),
    }

def surveys_handler(event, context):
    if(event['httpMethod'] == 'GET'):
        list_surveys()
    elif(event['httpMethod']== 'POST'):
        create_survey(event['body'])
