import os
from dotenv import load_dotenv

load_dotenv()


class Configuration:
    client_token = os.environ.get('CLIENT_TOKEN')
    redis_host = os.environ.get('REDIS_HOST')
    redis_port = int(os.environ.get('REDIS_PORT'))
    dynamodb_endpoint = os.environ.get('DYNAMODB_ENDPOINT')
    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')