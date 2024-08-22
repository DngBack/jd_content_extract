import json
from typing import List, Optional, Union
from enum import Enum
from pydantic import BaseModel

from enum import Enum
from typing import Literal
from typing import Optional
from typing import Union


class Master(str, Enum):
    FIXED_ALLOWANCE = 'm_fixed_allowance'
    VARIABLE_ALLOWANCE = 'm_variable_allowance'
    SALARY_TYPE = 'm_salary_type'
    OVERTIME_SALARY = 'm_overtime_salary'
    EXCEEDING_OVERTIME = 'm_exceeding_overtime'
    OVERTIME_EXCLUDED_OBJECT = 'm_overtime_excluded_object'
    SALARY_PAYMENT_METHOD = 'm_salary_payment_method'
    WORKING_HOURS_TYPE = 'm_working_hours_type'
    DISCRETIONARY_LABOR_SYSTEM_TYPE = 'm_discretionary_labor_system_type'
    OFFICE_WORK = 'm_office_work'
    VARIABLE_WORKING_HOURS_TYPE = 'm_variable_working_hours_type'
    CONTRACT_WORKING_HOURS_SYSTEM = 'm_contract_working_hours_system'
    OCCUPATIONAL_CATEGORY = 'm_occupational_category'
    PREFECTURE = 'm_prefecture'
    FUTURE_WORKPLACE = 'm_future_workplace'
    TRANSFER = 'm_transfer'
    REMOTE_TYPE = 'm_remote_type'
    SMOKING_PREVENTION_CONTENT = 'm_smoking_prevention_content'
    FUTURE_JOB_DESCRIPTION = 'm_future_job_description'
    ALLOWANCE_COMMUTE_MONEY_TYPE = 'm_allowance_commute_money_type'
    SALARY_RAISE = 'm_salary_raise'
    HOLIDAYS_SYSTEM = 'm_holidays_system'
    HOLIDAY = 'm_holiday'
    LANGUAGE_LEVEL = 'm_language_level'
    INSURANCE = 'm_insurance'
    EMPLOYMENT_TYPE = 'm_employment_type'
    EMPLOYMENT_PERIOD_TYPE = 'm_employment_period_type'
    TRIAL_PERIOD = 'm_trial_period'
    JOB_CHARM = 'm_job_charm'


class DataType(str, Enum):
    STR = 'string'
    INT = 'integer'
    LIST_INT = 'list[int]'
    LIST_SUB = 'list[SubField]'
    BOOL = 'boolean'

class Field(BaseModel):
    field_name: str
    data_type: Literal[
        DataType.STR, DataType.INT, DataType.LIST_INT,
        DataType.LIST_SUB, DataType.BOOL,
    ]
    value: Union[str, int, bool, list[int], list[SubField]]
    master_table: Optional[Master] = None
    description: Optional[str]

class SubFieldElements(BaseModel):
    name: str
    data_type: Literal[
        DataType.STR, DataType.INT, DataType.LIST_INT,
        DataType.LIST_INT, DataType.BOOL,
    ]
    value: Union[str, int, bool, list[int]] = None
    master_table: Optional[str] = None
    description: str

class Category(BaseModel):
    key_name: str
    en_name: str
    ja_name: str
    fields: list[Field]

class JDStructure(BaseModel):
    categories: list[Category]


class Category(BaseModel):
    key_name: str
    en_name: str
    ja_name: str
    fields: list[Field]


class SubField(BaseModel):
    pass


class FixedAllowance(SubField):
    id: Optional[SubFieldElements]
    memo: Optional[SubFieldElements]
    min: Optional[SubFieldElements]
    max: Optional[SubFieldElements]


class VariableAllowance(SubField):
    id: Optional[SubFieldElements]
    memo: Optional[SubFieldElements]
    content: Optional[SubFieldElements]


class WorkingHoursPattern(SubField):
    start: Optional[SubFieldElements]
    end: Optional[SubFieldElements]
    break_hour: Optional[SubFieldElements]
    break_minute: Optional[SubFieldElements]
    actual_work_hour: Optional[SubFieldElements]
    actual_work_minutes: Optional[SubFieldElements]


json_file_path = "test_config.json"

# # Read the JSON file

with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)
# data = """
# {
#     "categories": [
#         {
#             "key_name": "salary_informations",
#             "en_name": "Salary Information",
#             "ja_name": "給料情報",
#             "fields": [
#                 {
#                     "field_name": "fixed_allowance_id",
#                     "data_type": "integer",
#                     "value": 1,
#                     "master_table": "m_fixed_allowance",
#                     "description": "Information of Fixed Allowances. Choose one in salary_fixed_allowances."
#                 },
#                 {
#                     "field_name": "fixed_allowance_memo",
#                     "data_type": "string",
#                     "value": "Uniform allowance",
#                     "description": "Record of Uniform (fixed) allowance"
#                 },
#                 {
#                     "field_name": "fixed_allowance_min",
#                     "data_type": "integer",
#                     "value": 1000,
#                     "description": "Minimum uniform (fixed) allowance"
#                 },
#                 {
#                     "field_name": "fixed_allowance_max",
#                     "data_type": "integer",
#                     "value": 5000,
#                     "description": "Maximum uniform (fixed) allowance"
#                 }
#             ]
#         }
#     ]
# }
# """
print(data)
print(type(data))

# data = json.loads(data)
# print(data)
# print(type(data))
# Create an instance of JDStructure with the loaded data
jd_structure = JDStructure(**data)

print(jd_structure)
