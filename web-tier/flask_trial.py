from flask import Flask, request, render_template
import os
import time
import boto3
import json

app = Flask(__name__)

# Folder to store uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

AWS_ACCESS_KEY = 'your aws access key'
AWS_SECRET_KEY = 'your aws secret key'
REGION = 'your region'
S3_BUCKET_NAME = 'your s3 input bucket name'

sqs = boto3.client('sqs', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY, region_name = REGION)
s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY, region_name = REGION)

# Ensure the upload folder exists

@app.route('/')
def index():
    return '''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>File Upload</title>
  </head>
  <body>
    <h1>Upload File</h1>
    <form method="POST" action="/upload" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
  </body>
</html>'''

@app.route('/upload', methods=['POST'])
def upload():

    #print(request.files)

    if 'myfile' not in request.files:
        return "No file part"

    file = request.files['myfile']

    if file.filename == '':
        return "No selected file"
    
    user_ip = request.remote_addr

    #print(user_ip)

    s3.upload_fileobj(file, S3_BUCKET_NAME, file.filename)

    # Get the S3 URL of the uploaded file
    file_url = f'https://{S3_BUCKET_NAME}.s3.amazonaws.com/{file.filename}'

    #print("Uploaded to s3")

    # Add S3 object ID to SQS queue
    SQS_QUEUE_URL = "your sqs input queue url"
    SQS_OUT_QUEUE_URL = "your sqs output queue url"
    # Create a new message
    sqs_response = sqs.send_message(QueueUrl=SQS_QUEUE_URL, MessageBody=f"{file.filename}")
    #print("sqs respond sent")

    
    #print("sqs recieved")
    # Extract message bodies from the response
    while True:
        with open('data.json') as json_file:
            data = json.load(json_file)

        if file.filename in data.keys():
            return data[file.filename]

        time.sleep(2)

if __name__ == '__main__':
    app.run(debug=True)
