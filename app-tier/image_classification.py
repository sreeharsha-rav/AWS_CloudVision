import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models
from urllib.request import urlopen
from PIL import Image
import numpy as np
import json


from s3_module import AWS_S3Client
from sqs_module import AWS_SQSClient

# AWS credentials
# Specify IAM User Credentials
AWS_ACCESS_KEY_ID = 'your_access_key'
AWS_SECRET_ACCESS_KEY = 'your_secret_access_key'
REGION = 'your_region'

# intialize an AWS_S3Client and AWS_SQSClient object
bucket = AWS_S3Client(
    aws_access_key_id = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name = REGION
)
queue = AWS_SQSClient(
    aws_access_key_id = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name = REGION
)

# bucket names
inp_bucket = 'your_input_bucket'
out_bucket = 'yout_output_bucket'

# queue urls
inp_queue = "your_input_queue"
out_queue = "your_output_queue"

# Loop
while True:
    # get image key from input SQS queue
    image_key = queue.receive_message(inp_queue)

    # Check if image_key was received
    if image_key:
        # get image from s3 bucket
        image_data = bucket.get_image(image_key, inp_bucket)

        # check if image data exits from s3 bucket
        if image_data:
            img = Image.open(image_data)

            # run image classification model
            model = models.resnet18(pretrained=True)

            model.eval()
            img_tensor = transforms.ToTensor()(img).unsqueeze_(0)
            outputs = model(img_tensor)
            _, predicted = torch.max(outputs.data, 1)

            # get image classification result
            with open('./imagenet-labels.json') as f:
                labels = json.load(f)
            result = labels[np.array(predicted)[0]]

            save_name = f"({image_key}, {result})"
            print(save_name)

            # put image classification result to s3 bucket
            bucket.write_result(image_key, save_name, out_bucket)

            # send result key to output SQS queue
            result_key = image_key  # result_key is same as image_key for input S3 bucket
            queue.send_message(out_queue, result_key)