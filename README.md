# Cloud Vision

*An scalable image recognition service built using AWS services.*

## Project Description

Cloud vision is an elastic image recognition service on AWS using Infrastructure as a Service (IaaS) resources. This service allows users to upload images, perform image recognition using a deep learning model, and receive recognition results.

![Cloud Vision Architecture](url)

### User
- Users can upload .JPEG images and will get results of the image classification.

### Web-Tier
- Handles multiples user requests concurrently
- Consists of 1 EC2 instance acting as a server.

### Messaging - SQS Queue
- Queues in message requests between web-tier to app-tier.
- Consists of 2 SQS queues:
    - one for sending messages from web tier to app tier (Input SQS Queue)
    - another for sending messages from app tier to web tier (Output SQS Queue)

### App-Tier
- Automatically scales up when demand increases (max 20) and drops when there are 0 messages in queue (min 1).
- Contains deep learning model provided as an AWS image (ami).
- Model is automatically run on launch.

### Storage - S3 Buckets
- All inputs (images) and outputs (classification results) are stored in S3 for persistence.
- 2 buckets are used, one for inputs (Input S3 Bucket) and one for outputs (Output S3 Bucket).
- Output objects contain image name, classification result tuples.

## Code Explanation

### web-tier
**Workload_multi.py**
- Functionality: Workload_multi.py is responsible for generating a workload using multithreading to send images for processing concurrently. It also waits for responses from the web tier and prints the image-solution pairs. It creates multiple threads of the Flask_Server's `upload()` function, which connects user input requests to the rest of the infrastructure.

**IaaSController.py**
- Functionality: IaaSController.py is responsible for controlling the order of execution and the concurrent execution of all the dependent scripts in the web tier of the service.

**flask_trial.py**
- Functionality: flask_trial.py serves as the web tier, responsible for uploading images to a bucket and sending the image file names into an input queue. It continuously checks the local data.json file for the model's solutions by searching the keys in the JSON dictionary. When a solution is found, it sends the solution to Workload_multi.py for display (printing).

**ReceiveQueue.py**
- Functionality: ReceiveQueue.py continuously checks the output queue. If there are items in the output queue, it retrieves those items and appends them to the data.json file. It is responsible for managing the output data from the service.

**AutoScaling.py**
- Functionality: AutoScaling.py is responsible for the creation and deletion of EC2 instances. It monitors the current queue size approximation and creates AMI (Amazon Machine Image) instances, scaling up to a maximum of 20 instances. It includes a global variable that allows you to determine the number of instances to be closed when the queue is empty. The script also continually checks if the queue is growing or empty and scales instances accordingly.

**QueueController.py**
- Functionality: QueueController.py serves as a repository for all the instance settings and the creation of instances used by AutoScaling.py. It allows access to the queue and stores instance AMIs, secret keys, regions, and other related information.

### App-Tier
**image_classification.py**
- Functionality: image_classification.py checks for SQS (Simple Queue Service) messages in the input SQS queue, pulls images from an input S3 bucket using the image key from the input SQS queue, runs an image classification model, and stores the results in an output S3 bucket using the same image key. It then sends the results to an output SQS queue.

**s3_module.py**
- Functionality: s3_module.py provides a class to initialize a Boto3 S3 client. It contains methods to retrieve objects from and store objects in S3 buckets.

**sqs_module.py**
- Functionality: sqs_module.py provides a class to initialize a Boto3 SQS client. It contains methods for receiving and sending messages to SQS queues.

### Data:
**Imagenet-100**
- Functionality: Imagenet-100 appears to be a directory or folder that holds all the user input files.

**Data.json**
- Functionality: Data.json is a file that holds all the image-solution pairs. It is populated by ReceiveQueue.py and read by Flask_Server. It acts as a data store for the image and solution data in the service.

## Getting Started

Before running the code, ensure that you have provided your AWS credentials in the code:

In `app-tier/image_classification.py`:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `REGION`
- `inp_bucket` = "S3 input bucket name or URL"
- `out_bucket` = "S3 output bucket name or URL"
- `inp_queue` = "SQS input queue URL"
- `out_queue` = "SQS output queue URL"

In `web-tier/QueueController.py`:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `REGION`
- `ami_id` = "custom ami id from app-tier"
- `sqs_AWS_ACCESS_KEY_ID` = 'sqs_access_key'
- `sqs_AWS_SECRET_ACCESS_KEY_ID` = 'sqs_secret_access_key'
- `sqs_queue_URL` = 'sqs_input_queue_url'
- `key1` = 'your_pem_key'

In `web-tier/flask_trial`:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `REGION`
- ` S3_BUCKET_NAME` = "your s3 input bucket name"
- `SQS_QUEUE_URL` = "your sqs input queue url"
- `SQS_OUT_QUEUE_URL` = "your sqs output queue url"

In `web-tier/ReceiveQueue`:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `REGION`
- `sqs_queue_URL` = 'sqs_output_queue_url'

In `workload_multi`:
- `url` = "URL for flask server"

Please note that the AWS credentials for EC2, SQS, and S3 should be consistent to ensure uniform user access and security.

## Installation and Usage

**Installation:**
To successfully install our programs, follow these steps:
1. Setup `app-tier`, go to the folder to follow `app-tier/README.md` to set it up.
2. From `web-tier`, ensure that all files are located in the same folder as the `imagenet-100` directory. These files should include:
    - Autoscaling.py
    - flask_trial.py
    - IaaSController.py
    - QueueController.py
    - ReceiveQueue.py
    - workload_multi.py
    - imagenet-100 folder

**Running the Programs:**
Once you have completed the installation, you can run the programs by following these steps:
1. Open your terminal or command prompt.
2. Navigate to the directory where you have placed the program files and the `imagenet-100` folder.
3. To start the service, execute the following command:
`python3 ./IaaSController.py`
4. Please allow approximately 3 minutes for the service to initialize. During this time, the system is setting up and processing tasks. Be

## Credits

This project is part of CSE 546 - Cloud Computing course curriculum at ASU.