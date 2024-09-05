import json
import re
import os
from datetime import datetime
import boto3
from dotenv import load_dotenv

class AwsSonet35:
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

    def chat(self, prompt):
        messages = [
            {
                'role': 'user',
                'content': [{'text': prompt}],
            },
        ]
        
        response = self.client.converse(
            modelId=self.model_id,
            messages=messages,
            inferenceConfig={"maxTokens": 4096, "temperature": 0.0, "topP": 1.0}
        )
        
        return response["output"]["message"]["content"][0]["text"]
    

class JsonProcessor:
    def __init__(self, file_path, llm: AwsSonet35):
        self.file_path = file_path
        self.llm = llm
        self.data = self.read_json_file()

    def read_json_file(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    def generate_template(self, key, subfields):
        subfield_names = ", ".join(subfields)
        prompt = f"Generate a template describing the {key} with the following attributes: {subfield_names}."
        template = self.llm.chat(prompt)
        return template

    def fill_template(self, template, values):
        for subkey, value in values.items():
            placeholder = f"{{{subkey}_value}}"
            template = template.replace(placeholder, str(value))
        return template

    def process_json(self, data, parent_key=None):
        if isinstance(data, dict):
            results = []
            for key, value in data.items():
                if isinstance(value, dict):
                    results.append(self.process_json(value, key))
                else:
                    # Assuming each dict under `key` is a group like 'Salary'
                    if parent_key:
                        template = self.generate_template(parent_key, data.keys())
                        filled_template = self.fill_template(template, data)
                        return filled_template
                    else:
                        results.append(f"{key}: {value}")
            return "\n".join(results)
        elif isinstance(data, list):
            return "\n".join([self.process_json(item) for item in data])
        else:
            return str(data)

    def get_formatted_string(self):
        return self.process_json(self.data)

# Usage
load_dotenv(".env")
ACCESS_KEY = os.environ.get('ACCESS_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')

model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"
llm = AwsSonet35()
llm.setup(ACCESS_KEY, SECRET_KEY, model_id)

file_path = 'test_1.json'
processor = JsonProcessor(file_path, llm)

# Get the formatted string
formatted_string = processor.get_formatted_string()

# Print the formatted string
print(formatted_string)

# Save the formatted string to a text file
output_file_path = 'output.txt'
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write(formatted_string)
