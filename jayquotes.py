import yaml
import boto3
import json
import random


bucket = 'jayquotes'
file = 'QuoteDB.yaml'


s3_client = boto3.client('s3')
sns = boto3.client('sns')
content = s3_client.get_object(Bucket=bucket, Key=file)


def newline():
    print('\n')

def lambda_handler(event, context):
    try:
        #access s3 bucket and loading file into memory as binary file
        newline()        
        print(f"[*] Loading bucket/file: " + bucket + '/' + file)
        newline()
        data = content['Body'].read()

        #load binary file data into dictionary type with yaml loader
        dataload = yaml.load(data, Loader=yaml.FullLoader)

        #generate random number to use as seed for random quote generation
        #range_start = 1
        #range_end = len(dataload.keys())
        range_start = 1
        range_end = 168
        num = str(random.randint(1,range_end))
        choice = dataload[num]

        #print chosen quote key's quote and author
        quote = choice[0]['Quote']
        author = '\n' + '-' + choice[1]['Author']
        print(quote)
        print(author)
        newline()

        response = sns.publish(
        TargetArn = 'arn:aws:sns:us-east-1:093353733761:JayQuote_Notify',
        Message = quote + author
        )

    except Exception as e:
        print("[!] Something went wrong. Check logs.")
        print("[-] Exiting...")
        newline()
        print(e)
        newline()

    return {
    	'statusCode': 200,
        'body': json.dumps('[+]fuction executed successfully.')
    }    

