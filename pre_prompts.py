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

list_name_dict = {
    "salary_fixed_allowances": "m_fixed_allowance",
    "salary_variable_allowances": "m_variable_allowance",
    "salary_type_id": "m_salary_type",
    "overtime_salary_id": "m_overtime_salary",
    "exceeding_overtime_id": "m_exceeding_overtime",
    "overtime_excluded_object_id": "m_overtime_excluded_object",
    "salary_payment_method_id": "m_salary_payment_method",
    "working_hours_type_id": "m_working_hours_type",
    "job_name_main_id": "m_occupational_category",
    "discretionary_labor_system_type_id": "m_discretionary_labor_system_type",
    "office_work_id": "m_office_work",
    "variable_working_hours_type_id": "m_variable_working_hours_type",
    "contract_working_hours_system_id": "m_contract_working_hours_system",
    "occupational_category_ids": "m_occupational_category",
    "prefecture_ids": "m_prefecture",
    "future_workplace_id": "m_future_workplace",
    "transfer_id": "m_transfer",
    "remote_type_ids": "m_remote_type",
    "smoking_prevention_content_id": "m_smoking_prevention_content",
    "future_job_description_id": "m_future_job_description",
    "allowance_commute_money_type_id": "m_allowance_commute_money_type",
    "salary_raise_id": "m_salary_raise",
    "holidays_system_id": "m_holidays_system",
    "holidays_breakdown_ids": "m_holiday",
    "english_ids": "m_language_level",
    "insurance_ids": "m_insurance",
    "employment_type_ids": "m_employment_type",
    "employment_period_type_id": "m_employment_period_type",
    "trial_period_id": "m_trial_period",
    "job_charm_details1": "m_job_charm",
    "job_charm_details2": "m_job_charm",
    "job_charm_details3": "m_job_charm",
}

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

# Open and read the JSON file
with open('master.json', 'r', encoding="utf-8") as file:
    # Load the dictionary from the JSON file
    master_dict = json.load(file)

# Open and read the JSON file
with open('entities.json', 'r', encoding="utf-8") as file:
    # Load the dictionary from the JSON file
    entities_dict = json.load(file)

# Replace 'data.json' with your file path
with open('2.json', 'r', encoding='utf-8') as file:
    info_extration = json.load(file)

result = {item['type']['en']: item['detail'] for item in info_extration["categories"]}

# check = "employment_type_ids" in list_name_dict.keys()

# output = {}
# # for i in range(len(categories)):
# i = 4
# index_target = target_categories[i]
# index_input = categories[i]

# target = entities_dict[index_target]
# content = result[index_input]

# prompt_add = ""

# for element in target.keys():
#     if element in list_name_dict.keys():
#         prompt_add = prompt_add + (element + ": " + 
#                         list_name[list_name_dict[element]] + "\n")

output = {}

for i in range(len(categories)):
    index_target = target_categories[i]
    index_input = categories[i]

    target = entities_dict[index_target]
    content = result[index_input]

    prompt_add = ""

    for element in target.keys():
        if element in list_name_dict.keys():
            
            prompt_add = prompt_add + (element + ": " + 
                            str((master_dict[list_name_dict[element]]).values()) + "\n")

    
    response = llm.chat(target=str(target),
                    content=str(content),
                prompt_add=str(prompt_add))

    response = eval(response)
    output[index_target] = response

# Convert and write JSON object to file

# print(output)
with open('data.json', 'wb') as fp:
    fp.write(json.dumps(output, ensure_ascii=False).encode("utf8"))
# Check preprompt
# print(list_name_dict[index_target])
# print(list_name[list_name_dict[index_target]])
