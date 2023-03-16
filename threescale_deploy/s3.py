import boto3
from . import logger


CORS_RULES = {
    "CORSRules": [{"AllowedOrigins": ["https://*"], "AllowedMethods": ["GET"]}]
}


def create_bucket(bucket_name):
    logger.info(f"Creating bucket {bucket_name}")

    client = boto3.client("s3")
    bucket = client.create_bucket(
        ACL="private",
        Bucket=bucket_name,
    )
    client.put_bucket_cors(Bucket=bucket_name, CORSConfiguration=CORS_RULES)
    return bucket["Location"]


def remove_bucket(bucket_name):
    client = boto3.client("s3")
    should_delete = True
    logger.info(f"Starting clean of bucket: {bucket_name}")
    while should_delete:
        objects = client.list_objects(Bucket=bucket_name)
        logger.debug(f"Deleting objects in bucket")
        if objects.get("Contents", None) is None:
            break
        should_delete = objects["IsTruncated"]
        client.delete_objects(
            Bucket=bucket_name,
            Delete={"Objects": [{"Key": key["Key"]} for key in objects["Contents"]]},
        )
    client.delete_bucket(Bucket=bucket_name)
    logger.info(f"Bucket {bucket_name} deleted")
