list_data = {
    "salary_fixed_allowances_attributes": ["Allowance1", "Allowance2", "Allowance3"],
    "salary_variable_allowances_attributes": ["Variable1", "Variable2", "Variable3"],
    "salary_type_id": ["Fixed", "Hourly", "Commission"],
    "overtime_salary_id": ["Standard", "Enhanced"],
    "exceeding_overtime_id": ["None", "Overtime1", "Overtime2"],
    "overtime_excluded_object_id": ["None", "SpecificTask"],
    "salary_payment_method_id": ["BankTransfer", "Cash", "Cheque"],
    "allowance_commute_money_type_id": ["Fixed", "Variable"],
    "salary_raise_id": ["Annual", "Performance"],
    "working_hours_type_id": ["Standard", "Flexible", "Discretionary"],
    "office_work_id": ["Onsite", "Remote"],
    "variable_working_hours_type_id": ["Fixed", "Variable"],
    "contract_working_hours_system_id": ["FullTime", "PartTime"]
}

salary_informations = {
    "salary_fixed_allowances_attributes": {
        "fixed_allowance_id": "Information of Fixed Allowances. Choose one in here: {list_name}",
        "fixed_allowance_memo": "string: Record of Uniform (fixed) allowance",
        "fixed_allowance_min": "string: An integer of min uniform (fixed) allowance",
        "fixed_allowance_max": "string: An integer of max uniform (fixed) allowance"
    },
    "salary_variable_allowances_attributes": {
        "variable_allowance_id": "Information of variable_allowance. Choose one in here: {list_name}",
        "variable_allowance_memo": "string: Record of variable allowance",
        "variable_allowance_content": "string: Content of variable allowance"
    },
    "salary_type_id": "Type of salary. Choose one in here: {list_name}",
    "min_basic_salary": "string: Integer of min basic salary",
    "max_basic_salary": "string: Integer of max basic salary",
    "overtime_salary_id": "Choose one in here: {list_name}",
    "overtime_salary_min": "string: Integer of min overtime salary",
    "overtime_salary_max": "string: Integer of max overtime salary",
    "exceeding_overtime_id": "Choose one in here: {list_name}",
    "allowance_flag": "string: boolean Indicates whether any type of allowance is provided (true or false)",
    "allowance_detail": "string: Provides specific details about any allowances offered (e.g., type of allowance, conditions).",
    "overtime_excluded_object_id": "Choose one in here: {list_name}",
    "min_monthly_salary": "string: The integer of The minimum monthly salary offered for a job or employee.",
    "max_monthly_salary": "string: The integer of The maximum monthly salary offered for a job or employee.",
    "salary_detail": "string: Additional details or breakdown of the salary offered, such as components, conditions, or bonuses.",
    "salary_payment_method_id": "Choose one in here: {list_name}",
    "salary_payment_method_detail": "string: Information on how the salary is paid ",
    "daily_salary": "string: The amount of salary calculated on a daily basis",
    "hourly_salary": "string: The amount of salary calculated on a hourly basis",
    "hybrid_payment_method_memo": "string: Notes or details about a mixed or hybrid salary payment method",
    "skip_entry_flag": "string:  Likely a boolean flag to indicate whether to skip entry or processing for this record or a specific section.",
    "max_annual_income": "string: Integer of The maximum annual income that can be earned",
    "min_annual_income": "string: Integer of The minimum annual income that can be earned",
    "allowance_commute_money_type_id": "commuting allowance. Choose one in here: {list_name}",
    "allowance_commute_flag": "string: The boolean Indicates whether a commuting allowance is provided",
    "allowance_commute_money_value": "string: Integer of The monetary value of the commuting allowance, if provided.",
    "allowance_commute_detail": "string: Additional details about the commuting allowance ",
    "bonus_flag": "string: boolean that whether a bonus is provided",
    "bonus": "string: The amount or details of the bonus offered.",
    "salary_raise_id": "Choose one in here: {list_name}",
    "salary_raise_memo": "string: Notes or information about salary increases or raises",
    "salary_model": "string: Describes the salary structure or model (e.g., fixed, commission-based, mixed)."
}

def replace_list_names(data, list_data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict):
                replace_list_names(value, list_data)
            elif isinstance(value, str) and '{list_name}' in value:
                list_name_key = key.replace("_id", "")
                if list_name_key in list_data:
                    options = ", ".join(str(list_data[list_name_key]))
                    data[key] = value.replace("{list_name}", options)
    return data

updated_salary_informations = replace_list_names(salary_informations, list_data)
print(updated_salary_informations)
