import json
import urllib.parse
import boto3

print('Loading function')

def lambda_handler(event, context):
    print("Triggered getTextFromS3PDF event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        textract = boto3.client('textract')
        textract.start_document_analysis(
        DocumentLocation={
            'S3Object': {
                'Bucket': bucket,
                'Name': key
            }
        },
        FeatureTypes=['TABLES'],
        JobTag=key + '_Job',
        NotificationChannel={
            'RoleArn': 'arn:aws:iam::623030461743:role/pdf_sns_role',
            'SNSTopicArn': 'arn:aws:sns:us-east-2:623030461743:pdf_statement'
        })
        
        return 'Triggered PDF Processing for ' + key
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
