import boto3
from .prompt import TEMP_MATCHING_ENTITTY

class AwsSonet35():
    def __init__(self):
        self.access_key = None
        self.secret_key = None

        self.client = None
        self.model_id = None
    
    def setup(self, access_key, secret_key, model_id):
        self.access_key = access_key
        self.secret_key = secret_key
        self.model_id = model_id

        self.client = boto3.client(
            service_name="bedrock-runtime",
            region_name="ap-northeast-1",
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
        )


    def chat(self, target, content):

        user_message = TEMP_MATCHING_ENTITTY.replace("{target}", target)
        user_message = user_message.replace("{content}", content)

        messages = [
            {
                'role': 'user',
                'content': [
                    {
                        'text': user_message,
                    }
                ],
            },
        ]
 
        response = self.client.converse(
            modelId=self.model_id,
            messages=messages,
            inferenceConfig={"maxTokens": 4096, "temperature": 0.0, "topP": 1.0},
            additionalModelRequestFields={"top_k":250}
        )
        return response["output"]["message"]["content"][0]["text"]
