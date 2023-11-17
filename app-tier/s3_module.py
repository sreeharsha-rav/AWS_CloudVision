import boto3
from botocore.exceptions import ClientError
from io import BytesIO

# AWS S3 interaction class
class AWS_S3Client:
    # Intialize an S3 client
    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name):
        self.s3_client = boto3.client(
            's3',
            region_name = region_name,
            aws_access_key_id = aws_access_key_id,
            aws_secret_access_key = aws_secret_access_key
        )
    
    # Get image data from S3 bucket given object_key
    def get_image(self, object_key, bucket_name):
        try:
            response = self.s3_client.get_object(
                Bucket = bucket_name, 
                Key = object_key
                )
            image_data = response['Body'].read()
            image_data = BytesIO(image_data)
            print(f'Got "{object_key}" from "{bucket_name}".')

            return image_data

        except ClientError as e:
            print(f'Error downloading image from S3: {e}')

    # Write data to S3 object from S3 client
    def write_result(self, object_key, result, bucket_name):
        try:
            # Upload the image to S3
            response = self.s3_client.put_object(
                Bucket = bucket_name,
                Key = object_key,
                Body = result
            )
            print("Response: ", response)
            print(f'Put "{result}" to "{bucket_name}".')
        except ClientError as e:
            print(f'Error uploading image to S3: {e}')