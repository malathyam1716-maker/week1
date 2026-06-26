import json
import boto3
from datetime import datetime
from loaders.base_loader import RawDataLoader

class S3Loader(RawDataLoader):
    def __init__(self, aws_access_key_id: str, aws_secret_access_key: str, bucket_name: str):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        self.bucket_name = bucket_name

    def load_raw_data(self, data: list[dict], prefix: str) -> str:
        if not self.bucket_name:
            print("S3 Loader: Bucket name not configured. Skipping S3 upload.")
            return None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{prefix}/raw_{timestamp}.json"
        
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_name,
                Body=json.dumps(data),
                ContentType="application/json"
            )
            print(f"Successfully uploaded {len(data)} records to s3://{self.bucket_name}/{file_name}")
            return file_name
        except Exception as e:
            print(f"Failed to upload to S3: {e}")
            return None

    def read_raw_data(self, file_name: str) -> list[dict]:
        if not self.bucket_name or not file_name:
            return []
        
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=file_name
            )
            data = json.loads(response['Body'].read().decode('utf-8'))
            print(f"Successfully read {len(data)} records from s3://{self.bucket_name}/{file_name}")
            return data
        except Exception as e:
            print(f"Failed to read from S3: {e}")
            return []
