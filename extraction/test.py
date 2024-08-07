import boto3
from botocore.exceptions import ClientError
from .gleaning.graph import GraphExtractor
import os 
from dotenv import load_dotenv

load_dotenv('.env')
ACCESS_KEY = os.environ.get('ACCESS_KEY ')
SECRET_KEY = os.environ.get('SECRET_KEY')

# Create a Bedrock Runtime client in the AWS Region you want to use.
client = boto3.client(
    service_name="bedrock-runtime",
    region_name="ap-northeast-1",
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    )

# Set the model ID, e.g., Titan Text Premier.
model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"

extractor = GraphExtractor(
    llm_invoker=client,
    encoding_model= "cl100k_base",
    max_gleanings=1,
    )


text_list = []

results = extractor(
    list(text_list),
    model = "gpt-4o-mini"
)