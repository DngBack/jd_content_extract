import boto3

from langchain_aws import ChatBedrock
import os
from dotenv import load_dotenv

load_dotenv('.env')
ACCESS_KEY = os.environ.get('ACCESS_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')

# Create a Bedrock Runtime client in the AWS Region you want to use.
client = boto3.client(
    service_name="bedrock-runtime",
    region_name="ap-northeast-1",
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
)

# # Set the model ID, e.g., Titan Text Premier.
model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"

# llm = Bedrock(region_name="ap-northeast-1",
#               streaming=True, credentials_profile_name="bedrock-admin",
#               model_id=model_id, aws_access_key_id="AKIAVIBLBCMKY", aws_secret_access_key="3rP9OIy+1WaAPJxHrS8XenWbm1Kb0zEIQ8q08H75")

# llm = BedrockLLM(model_id="anthropic.claude-3-5-sonnet-20240620-v1:0", client=client)
llm = ChatBedrock(client=client, model_id=model_id)

prompt = "資源循環を促進する新素材の開発や資源循環型モデルを構築、更には ECサイトを通じた一般消費者向けの D2C事業を開始するなど、サステナビリティ領域で事業を拡張しています。"
input_tokens = llm.get_num_tokens(prompt)
# result = llm(prompt)
# output_tokens = llm.get_num_tokens(result)
# print(f"Input Tokens: {input_tokens}, Output Tokens: {output_tokens}")
print(input_tokens)