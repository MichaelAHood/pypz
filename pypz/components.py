import localstack_client.session as boto3

s3 = boto3.client("s3")
sqs = boto3.client("sqs")
lambda_client = boto3.client("lambda")


def create_bucket(bucket_name: str) -> None:
    """Create an S3 bucket."""
    existing_buckets = [bucket["Name"] for bucket in s3.list_buckets()["Buckets"]]
    if bucket_name not in existing_buckets:
        s3.create_bucket(Bucket=bucket_name)


def create_queue(queue_name: str) -> None:
    """Create an SQS queue."""
    existing_queues = [
        queue_url
        for queue_url in sqs.list_queues().get("QueueUrls", [])
        if queue_name in queue_url
    ]
    if not existing_queues:
        sqs.create_queue(QueueName=queue_name)


def create_lambda(function_name: str, zip_file_path: str, handler: str) -> None:
    """Create a Lambda function from zipfile."""
    existing_functions = [
        function["FunctionName"]
        for function in lambda_client.list_functions()["Functions"]
    ]
    if function_name not in existing_functions:
        with open(zip_file_path, "rb") as f:
            zipped_code = f.read()

        lambda_client.create_function(
            FunctionName=function_name,
            Runtime="python3.11",
            Role="arn:aws:iam::123456789123:role/execution_role",
            Handler=handler,
            Code={"ZipFile": zipped_code},
        )


def delete_bucket(bucket_name: str) -> dict:
    """Delete a bucket."""
    return s3.delete_bucket(Bucket=bucket_name)


def delete_queue(queue_name: str) -> dict:
    """Delete a SQS queue."""
    queue_url = sqs.get_queue_url(QueueName=queue_name)["QueueUrl"]
    return sqs.delete_queue(QueueUrl=queue_url)


def delete_lambda(function_name: str) -> dict:
    """Delete a lambda function."""
    return lambda_client.delete_function(FunctionName=function_name)
