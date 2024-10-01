from langchain.llms import Bedrock

import boto3

client = boto3.client("bedrock-runtime")

llm = Bedrock(client=client, model_id="anthropic.claude-instant-v1")
prompt = "who are you?"
print(llm.get_num_tokens(prompt))

result = llm(prompt)
print(result, llm.get_num_tokens(result))