import boto3

class QueueController:
    def __init__(self):
        self.AWS_ACCESS_KEY_ID = 'your_access_key'
        self.AWS_SECRET_ACCESS_KEY_ID = 'your_secret_access_key'
        self.REGION = 'your_region'
        self.ami_id = 'custom_ami_id'

        self.sqs_AWS_ACCESS_KEY_ID = 'sqs_access_key'
        self.sqs_AWS_SECRET_ACCESS_KEY_ID = 'sqs_secret_access_key'
        self.sqs_queue_URL = 'sqs_input_queue_url'
        self.make_client_SQS()
        self.make_client()
        self.key1 = 'your_pem_key'
        self.user_data = """#!/bin/bash
cd home/ubuntu/app-tier
chmod 777 image_classification.py
su ubuntu
sudo -u ubuntu python3 image_classification.py
"""
    def make_client(self):
        self.ec2 = boto3.client(
            'ec2',
            region_name = self.REGION,
            aws_access_key_id = self.AWS_ACCESS_KEY_ID,
            aws_secret_access_key = self.AWS_SECRET_ACCESS_KEY_ID
        )

    def make_client_SQS(self):
        self.SQS_Send = boto3.resource(
            'sqs',
            region_name = self.REGION,
            aws_access_key_id = self.sqs_AWS_ACCESS_KEY_ID,
            aws_secret_access_key = self.sqs_AWS_SECRET_ACCESS_KEY_ID
        )

        self.SQS_Client = boto3.client(
            'sqs',
            region_name = self.REGION,
            aws_access_key_id = self.sqs_AWS_ACCESS_KEY_ID,
            aws_secret_access_key = self.sqs_AWS_SECRET_ACCESS_KEY_ID
        )

    def launch_instance(self):
        response = self.ec2.run_instances(
            ImageId = self.ami_id,
            MinCount = 1,
            MaxCount = 1,
            UserData = self.user_data,
            InstanceType = 't2.micro',
            KeyName = self.key1
        )

        instance_id = response['Instances'][0]['InstanceId']
        #print(f'Launched EC2 instance with ID: {instance_id}')
        return instance_id

    def terminate_instance(self, instance_id):
        self.ec2.terminate_instances(InstanceIds=[instance_id])

    def instances_status(self):
        self.reservations = self.ec2.describe_instances(
            Filters = [
                {
                    "Name": "instance-state-name",
                    "Values": ["running", "pending"],
                },
                {
                    "Name": "image-id",
                    "Values": [self.ami_id],
                }],
            ).get("Reservations")
    
    #print list of instances
    def list_instances(self):
        self.instances_status()        
        for x in range(len(self.reservations)):
            instance = self.reservations[x]['Instances'][0]
            #print("Instance {} {} {}".format( x, instance['InstanceId'], instance['State']['Name']))

    def queue_count(self):
        response = self.SQS_Client.get_queue_attributes(
            QueueUrl = self.sqs_queue_URL,
            AttributeNames = [
                'All'
            ]
        )
        messageCount = response['Attributes']['ApproximateNumberOfMessages']
        return messageCount