import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_USER = os.getenv("DB_USER", "your_db_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "your_db_password")
    DB_HOST = os.getenv("DB_HOST", "your_rds_host.rds.amazonaws.com")
    DB_NAME = os.getenv("DB_NAME", "your_db_name")
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY", "your_aws_access_key")
    AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY", "your_aws_secret_key")
    AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN", "your_aws_session_token")
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
    BUCKET_NAME = os.getenv("BUCKET_NAME", "your_s3_bucket_name")
    SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN", "arn:aws:sns:us-east-1:123456789012:your-topic")
