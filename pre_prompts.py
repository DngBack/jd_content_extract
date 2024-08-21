from enum import Enum
import json
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
    'age_and_gender', 'employment_type_period', 'trial_period',
    'contract_renewal', 'job_posting', 'salary_informations', 
    'job_working_hours', 'recruiment_and_hiring', 'holidays_and_leaves', 
    'welfare_insurance'
]

key_mapping = {categories[i]: target_categories[i] for i in range(len(target_categories))}

def replace_keys(d, mapping):
    if isinstance(d, dict):
        return {mapping.get(k, k): replace_keys(v, mapping) for k, v in d.items()}
    elif isinstance(d, list):
        return [replace_keys(item, mapping) for item in d]
    else:
        return d

# Open and read the JSON file
with open('master_data.json', 'r', encoding="utf-8") as file:
    # Load the dictionary from the JSON file
    master_dict = json.load(file)

# Open and read the JSON file
with open('entities.json', 'r', encoding="utf-8") as file:
    # Load the dictionary from the JSON file
    entities_dict = json.load(file)

# Open and read the JSON file
with open('entities_sub.json', 'r', encoding="utf-8") as file:
    # Load the dictionary from the JSON file
    entities_sub_dict = json.load(file)   

# Replace 'data.json' with your file path
with open('3.json', 'r', encoding='utf-8') as file:
    info_extration = json.load(file)

result = {item['type']['en']: item['detail'] for item in info_extration["categories"]}

result = replace_keys(result, key_mapping)
output = {}

other_element = result["other"]

for i in range(len(entities_dict)):
    index_target = list(entities_dict.keys())[i]

    target = entities_dict[index_target]
    content = result[index_target]

    prompt_add = ""

    for element in target.keys():
            if element in master_dict.keys():
                
                prompt_add = prompt_add + (element + ": " + 
                                str((master_dict[element]).values()) + "\n")
        
    response = llm.chat(target=str(target),
                    content=str(content + other_element),
                prompt_add=str(prompt_add),
                task = "field")

    response = eval(response)
    output[index_target] = response

# Save output with json file
with open('pre_data_3.json', 'wb') as fp:
    fp.write(json.dumps(output, ensure_ascii=False).encode("utf8"))

for field in entities_sub_dict.keys():
    content = str(result[field])
    target = entities_sub_dict[field]
    # check prompt_add 
    prompt_add = ""
    for sub_field in entities_sub_dict[field].keys():
        content = content + str(str(sub_field) + str(output[field][sub_field]))
        adding_content = str(output[field][sub_field])

        for element in entities_sub_dict[field][sub_field].keys():
            
            if element in master_dict.keys():
                prompt_add = (element + ": " + 
                            str((master_dict[element]).values()) + "\n")
                
    response = llm.chat(target=str(target),
                content=str(adding_content + content),
                prompt_add=str(prompt_add),
                task = "sub_field")
    response = eval(response)
    
    for sub_field in entities_sub_dict[field].keys(): 
        output[field][sub_field] = response[sub_field]


# Save output with json file
with open('data_3.json', 'wb') as fp:
    fp.write(json.dumps(output, ensure_ascii=False).encode("utf8"))

