import boto3
from config import Config

s3_client = boto3.client(
    's3',
    aws_access_key_id=Config.AWS_ACCESS_KEY,
    aws_secret_access_key=Config.AWS_SECRET_KEY,
    aws_session_token=Config.AWS_SESSION_TOKEN,
    region_name=Config.AWS_REGION
)

sns_client = boto3.client(
    'sns',
    aws_access_key_id=Config.AWS_ACCESS_KEY,
    aws_secret_access_key=Config.AWS_SECRET_KEY,
    aws_session_token=Config.AWS_SESSION_TOKEN,
    region_name=Config.AWS_REGION
)

dynamodb_res = boto3.resource(
    'dynamodb',
    aws_access_key_id=Config.AWS_ACCESS_KEY,
    aws_secret_access_key=Config.AWS_SECRET_KEY,
    aws_session_token=Config.AWS_SESSION_TOKEN,
    region_name=Config.AWS_REGION
)

dynamo_table = dynamodb_res.Table('sesiones-alumnos')
