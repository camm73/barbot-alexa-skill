import json
import boto3

iotClient = boto3.client('iot-data', region_name='us-east-1')

def lambda_handler(event, context):

    cocktailType = event['request']['intent']['slots']['cocktail']['value']

    params = {
        "action": 'makeCocktail',
        "data" : cocktailType.lower()
    }

    response = iotClient.publish(
        topic='barbot-main',
        qos=1,
        payload=json.dumps(params)
    )

    return{
        'statusCode': 200,
        'body': response
    }