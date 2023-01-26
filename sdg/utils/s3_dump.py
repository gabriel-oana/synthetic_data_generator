import boto3
from utils.base_dump import BaseDump


class S3Dump(BaseDump):

    def __init__(self, s3_client: boto3.client):
        self.s3_client = s3_client

    def write(self, path: str, body: str):
        """
        Writes the file to a specific path in S3
        The path needs to be of the format s3://<bucket_name>/<key>
        """
        bucket_name = path.replace("s3://", "").split('/')[0]
        key = "/".join(path.replace("s3://", "").split("/")[1:])

        self.s3_client.put_object(
            Body=body,
            Bucket=bucket_name,
            Key=key
        )
