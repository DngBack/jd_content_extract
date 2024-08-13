import requests
import json

import os
from dotenv import load_dotenv

load_dotenv('.env')
api_key = os.environ.get('API_KEY')
base_url = os.environ.get('BASE_URL')

class AzureOpenAI:
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url

    def generate_text(self, model_name, messages, **kwargs):
        try:
            url = f"{self.base_url}/deployments/{model_name}/chat/completions"
            headers = {
                "Host": "en-apim-aoai.azure-api.net",
                "Content-Type": "application/json",
                "Ocp-Apim-Subscription-Key": self.api_key,
            }
            data = {"messages": messages, **kwargs}
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            response_data = response.json()
            return response_data
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"Other error occurred: {err}")

    def generate_embedding(self, model_name, input, **kwargs):
        try:
            url = f"{self.base_url}/deployments/{model_name}/embeddings"
            headers = {
                "Host": "en-apim-aoai.azure-api.net",
                "Content-Type": "application/json",
                "Ocp-Apim-Subscription-Key": self.api_key,
            }
            data = {"input": input, **kwargs}
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            response_data = response.json()
            return response_data

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            
        except Exception as err:
            print(f"Other error occurred: {err}")
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            response_data = response.json()
            return response_data


client = AzureOpenAI(
    api_key=api_key ,
    base_url=base_url
    )

generated_text = client.generate_text(
    model_name="gpt-4o-2024-05-13",
    messages=[
        {"role": "system", "content": "あなたはAIアシスタントです。"},
        {"role": "user", "content": "こんにちは"},
    ],
)

print(generated_text['choices'][0]['message']['content'])

generate_embedding = client.generate_embedding(
    model_name="text-embedding-3-small",
    input="こんにちは"
)

print(generate_embedding["data"][0]["embedding"])
