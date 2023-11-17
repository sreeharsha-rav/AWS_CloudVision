# App-Tier Summary

This directory contains a pre-trained image recognition model. The model performs the following steps:

1. Reads an `image_key` from a predefined SQS (Simple Queue Service) input queue.
2. Retrieves the corresponding image from a predefined S3 (Simple Storage Service) input bucket using the `image_key`.
3. Executes the model on the image.
4. Stores the output of the model in the predefined S3 output bucket using the same `image_key`.
5. Sends the `image_key` back to another predefined SQS output queue.

Once the predefined SQS input queue is empty, the program waits for 5 seconds before completing its execution. This code is intended to be run on an AWS EC2 instance, hardcoded into a custom Amazon Machine Image (AMI). It interacts with two SQS queues: an SQS input queue and an SQS output queue, as well as two S3 buckets: an S3 input bucket and an S3 output bucket.

## Getting Started

Before running the code, ensure that you have provided your AWS credentials in the code:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `REGION`

Additionally, provide the names or URLs of the S3 buckets and SQS queues:

- `inp_bucket` = "S3 input bucket name or URL"
- `out_bucket` = "S3 output bucket name or URL"
- `inp_queue` = "SQS input queue URL"
- `out_queue` = "SQS output queue URL"

Please note that the AWS credentials for EC2, SQS, and S3 should be consistent to ensure uniform user access and security.

## Creating a Custom AMI

After defining AWS credentials and specifying the S3 and SQS names or URLs, follow these steps:

1. Take a snapshot of the EC2 instance.
2. Create a new custom AMI (Amazon Machine Image) ID from the snapshot.

## Running App-Tier

To run App-Tier, use boto3 to create and run EC2 instances. Provide UserData for running EC2 instances below:

```python
user_data = """#!/bin/bash
cd /home/ubuntu/app-tier
chmod 777 image_classification.py
su ubuntu
sudo -u ubuntu python3 image_classification.py
"""
```

Make sure to provide this script as UserData during instance launch. This script will configure and execute the App-Tier application on the EC2 instance.
