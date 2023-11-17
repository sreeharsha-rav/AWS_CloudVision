import time
import boto3
import json

AWS_ACCESS_KEY_ID = 'your_access_key'
AWS_SECRET_ACCESS_KEY_ID = 'your_secret_key'
sqs_queue_URL = 'sqs_output_queue_url'
REGION = 'your_region'

json_dict = {}
# with open('data.json', 'r+') as json_file:
#     json_dict = json.load(json_file)
with open("data.json", "w+") as outfile: 
    json.dump({'test': 'test'}, outfile)

SQS_Client = None


SQS_Client = boto3.client(
    'sqs',
    region_name = REGION,
    aws_access_key_id = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY_ID
)

def queue_receive():
    response_recieved = SQS_Client.receive_message(
        QueueUrl = sqs_queue_URL,
        AttributeNames = [
            'SentTimestamp'
        ],
        MaxNumberOfMessages = 1,
        MessageAttributeNames =[
            'All'
        ],
        VisibilityTimeout = 0,
        WaitTimeSeconds = 0
    )

    if 'Messages' in response_recieved:

        SQS_Client.delete_message(
        QueueUrl = sqs_queue_URL,
        ReceiptHandle = response_recieved['Messages'][0]['ReceiptHandle']
        )

        solution_tuple = response_recieved['Messages'][0]['Body'].strip("()").split(",")
        json_dict[solution_tuple[0]] = solution_tuple[1]

        with open("data.json", "w+") as outfile: 
            json.dump(json_dict, outfile)

        #print('Img: {} sol: {}'.format(solution_tuple[0], solution_tuple[1])) ############remove later

def queue_count():
    response = SQS_Client.get_queue_attributes(
        QueueUrl = sqs_queue_URL,
        AttributeNames = [
            'All'
        ]
    )
    return int(response['Attributes']['ApproximateNumberOfMessages'])


while(True):
    if queue_count() >= 0:
        queue_receive()
    else:
        print("Recieve is empty")
        time.sleep(1)
    
