import boto3

TEMP_MATCHING_ENTITY = """
Please fill in the following recruitment and hiring attributes with relevant information based on the provided descriptions. 
The input attributes include (json format):
{attributes}

Context (json format):
{context}

The recruitment and hiring process covers various aspects such as the job title, employment type, salary, work location, and required qualifications for a Data Engineer position in Tokyo. The job offers an annual salary range of 5,493,636 - 7,687,392 yen and includes several allowances and bonuses. The work environment is located in Shibuya, Tokyo, with a non-smoking indoor policy. Opportunities for skill development and salary increases are provided annually in May.

Task: Based on the above context, fill in the details for the attributes listed.
Requirements:
- Only give me json format
- Answer with Enlish
- If you don not fill infor, instead null by None
- Using "True" or "False" for boolean
"""

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


    def chat(self, attributes, context):
        user_message = TEMP_MATCHING_ENTITY.replace("{attributes}", attributes)
        user_message = user_message.replace("{context}", context)

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
