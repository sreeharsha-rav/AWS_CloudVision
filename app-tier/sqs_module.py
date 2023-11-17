# Import all the modules and Libraries
import boto3

# AWS SQS interaction class
class AWS_SQSClient:
    # Initialize SQS Client
    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name):
        self.sqs_client = boto3.client(
            'sqs',
            region_name = region_name,
            aws_access_key_id = aws_access_key_id,
            aws_secret_access_key = aws_secret_access_key
            )

    # Send message through SQS Queue
    def send_message(self, queue_url, message_body):
        try:
            response = self.sqs_client.send_message(
                QueueUrl = queue_url, 
                MessageBody = message_body
                )
            print(f"Message sent to queue '{queue_url}' with MessageId: {response['MessageId']}")
        except Exception as e:
            print(f"Error sending message to queue '{queue_url}': {str(e)}")

    # Receive message from SQS Queue
    def receive_message(self, queue_url, max_messages=1):
        try:
            response = self.sqs_client.receive_message(
                QueueUrl=queue_url, 
                MaxNumberOfMessages=max_messages,
                #VisibilityTimeout = 3,  # wait for 3 seconds after receive_message
                WaitTimeSeconds=3,  # Wait for 3 seconds after queue is empty
                )
            messages = response.get('Messages', [])
            if messages:
                message = messages[0]  # Get the first (and only) message
                receipt_handle = message['ReceiptHandle']
                received_message = message['Body']
                print(f"Received message: {received_message}")

                # Optionally, you can delete the received message after processing
                self.sqs_client.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)

                return received_message
            else:
                print("No messages available in the queue.")
        except Exception as e:
            print(f"Error receiving messages from queue '{queue_url}': {str(e)}")