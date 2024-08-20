from utils.aws_sonet import AwsSonet35
from utils.groups import groups_entity, classify_entities

import ast
import json
from pathlib import Path

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
    'age and gender details', 'emplyment type period', 'trial preiod',
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

# Get data 
data = Path("enti_extraction.txt").read_text(encoding="utf-8")
str_output_json, dict_output_json = groups_entity(data)

print(dict_output_json)

# Open and read the JSON file
with open('entities.json', 'r', encoding="utf-8") as file:
    # Load the dictionary from the JSON file
    entities_dict = json.load(file)

output = {}

for i in range(len(categories)):
    output_key = categories[i]
    entities_key = target_categories[i]

    response = llm.chat(attributes=str(entities_dict[entities_key]),
                        context=str(dict_output_json[output_key]))
    response = eval(response)
    output[output_key] = response


# Convert and write JSON object to file
with open("sample.json", "w") as outfile: 
    json.dump(output, outfile)
