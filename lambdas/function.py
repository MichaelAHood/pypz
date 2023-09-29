import json
import localstack_client.session as boto3


def lambda_handler(event, context):
    s3 = boto3.client("s3")
    sqs = boto3.client("sqs")

    # Assume the SQS message body is a string
    for record in event["Records"]:
        message_body = record["body"]

        # Upload the message to S3
        s3.put_object(
            Body=message_body, Bucket="my-bucket", Key=f"messages/{record['messageId']}"
        )

    return {"statusCode": 200, "body": json.dumps("Done!")}
