from utils.aws_sonet import AwsSonet35
from utils.groups import classify_entities

import ast
import json
from pathlib import Path
import pprint

import os
from dotenv import load_dotenv
load_dotenv(".env")

ACCESS_KEY = os.environ.get('ACCESS_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')
model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"

# Set up llm 
llm = AwsSonet35()
llm.setup(ACCESS_KEY, SECRET_KEY, model_id)

# list all categories
categories = [
    'location details', 'remote work details', 'smoking prevention details',
    'age and gender', 'employment type period', 'trial period',
    'contract renewal', 'job posting', 'salary information',
    'job working hour', 'recruiment and hiring', 'holidays and leaves',
    'welfare insurance'
]

target_categories = [
    'location_details', 'remote_work_details', 'smoking_prevention_details', 
    'age_and_gender', 'employment_type_period', 'trial_preiod', 
    'contract_renewal', 'job_posting', 'salary_informations', 
    'job_working_hours', 'recruiment_and_hiring', 'holidays_and_leaves', 
    'welfare_insurance'
]

# Get Example
with open('example_entities.json', 'r', encoding="utf-8") as file:
    # Load the dictionary from the JSON file
    example_dict = json.load(file)

# Open and read the JSON file
with open('entities.json', 'r', encoding="utf-8") as file:
    # Load the dictionary from the JSON file
    entities_dict = json.load(file)

# Replace 'data.json' with your file path
with open('test.json', 'r', encoding='utf-8') as file:
    info_extration = json.load(file)

classified_entities = classify_entities(info_extration)

# # Convert and write JSON object to file
# with open("cc.json", "w", encoding="utf-8") as outfile: 
#     json.dump(classified_entities, outfile)
# exit()

output = {}

for i in range(len(categories)):
    output_key = categories[i]
    entities_key = target_categories[i]

    response = llm.chat(target=str(entities_dict[entities_key]),
                        content=str(classified_entities[output_key]),
                        examples=str(example_dict[entities_key]))

    
    response = eval(response)
    output[output_key] = response


# Convert and write JSON object to file
with open("sample.json", "w", encoding="utf-8") as outfile: 
    json.dump(output, outfile)
