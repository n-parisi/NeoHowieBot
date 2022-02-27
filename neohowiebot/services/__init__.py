import boto3
import os


class FileService():
    def __init__(self):
        s3 = boto3.client('s3')
        response = s3.list_objects_v2(
            Bucket=os.getenv("RESOURCE_BUCKET"),
            Prefix=os.getenv("CLIPS_PREFIX")
        )
        self.clips = [content['Key'].split('/')[2].split('.')[0] for content in response['Contents']][1:]


file_service = FileService()
