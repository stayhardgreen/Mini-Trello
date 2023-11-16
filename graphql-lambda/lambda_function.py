import json
from schema import empSchema

def lambda_handler(event, context):
    print("Event Parameters:%s" %event)
    result = {}
    try:
        response = empSchema.execute(event['queryStringParameters']['query'])
        print("Response from Graphene:%s" %response)
        if response.data:
            result = {'statusCode': 200, 'body': json.dumps(response.data)}
        else:
            result = {'statusCode': 500, 'body': json.dumps(response.errors[0].message)}
    except Exception as e:
        result = {'statusCode': 500, 'body': "An error occurred:%s" %e}   
    return result
