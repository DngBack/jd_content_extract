from tests.test_groups_entity import groups_entity
from test_apim import AzureOpenAI
from pathlib import Path

import os
from dotenv import load_dotenv

load_dotenv('.env')
api_key = os.environ.get('API_KEY')
base_url = os.environ.get('BASE_URL')

TEMP_LLM_EXTRACT = """
This is Information Provide: 

{data}

Your task is to arrange the above information about the fields provided below into each group.
There is a lot of noise, you need to be careful when taking information.
Only give me json str format.

Categories and attributes:  
{
  "job_working_hours": {
    "working_hours_patterns_attributes": null, 
      "scheduled_working_hours_start": null,
      "scheduled_working_hours_end": null,
      "actual_working_hour": null,
      "actual_working_minute": null,
      "break_time_hour": null,
      "break_time_minute": null,
      "overtime_working_flag": null,
      "working_hours_detail": null,
      "min_ave_month_overtime_hour": null,
      "min_ave_month_overtime_minute": null,
      "max_ave_month_overtime_hour": null,
      "max_ave_month_overtime_minute": null,
      "deemed_working_hour": null,
      "deemed_working_minute": null,
      "ave_working_hour": null,
      "ave_working_minute": null,
      "standard_working_hour": null,
      "standard_working_minute": null,
      "core_time_flag": null,
      "regular_week_working_hour": null,
      "regular_week_working_minute": null,
      "core_time_hours_start": null,
      "core_time_hours_end": null,
      "flex_time_hours_start": null,
      "flex_time_hours_end": null,
      "second_flex_time_hours_start": null,
      "second_flex_time_hours_end": null,
      "overtime_max_hour": null,
      "overtime_min_hour": null,
      "overtime_max_minute": null,
      "overtime_min_minute": null,
      "working_hours_condition": null
  },
  "remote_work_details": {
    "remote_flag": null,
    "remote_type_ids": null,
    "remote_day_min": null,
    "remote_day_max": null,
    "remote_detail": null
  },
  "smoking_prevention_details": {
    "smoking_prevention_flag": null,
    "smoking_prevention_detail": null
  },
  "age_and_gender": {
    "age_genders": null
  }
}

"""

data = Path("enti_extraction.txt").read_text()
data = groups_entity(data)
prompt = TEMP_LLM_EXTRACT.replace("{data}", str(data))

client = AzureOpenAI(
    api_key=api_key ,
    base_url=base_url
)

generated_text = client.generate_text(
    model_name="gpt-4o-2024-05-13",
    messages=[
        {"role": "system", "content": "You are AI Assistant."},
        {"role": "user", "content": prompt},
    ],
)

print(generated_text['choices'][0]['message']['content'])
