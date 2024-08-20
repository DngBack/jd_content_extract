TEMP_MATCHING_ENTITTY = """
-Goal-
Given an json that like content have information. 
Your task that will filling the empty variable in target json based on content json.
Filiing all content

-Requirements-
- Output is only finaly output json format
- Answer with Japanese. Without transfer_id, transfer_id will answer by English.
- If you don not fill infor, instead null by None. 
- Using "True" or "False" for boolean
- Convert all other datatype to string in answer. I mean that integer to string, boolean to string
- With the attribute that are based on list data, only give the elements not give number id.
- In choose task, ONLY choose from list data, not change or replace by new words.
- Attributes end with _id, output is only one string
- Attributes end with _ids, output is list string(even in case only one element)
- Did not answer ramblingly, to the point. Not fabricated, only based on the information given. \
With unknown or non-existent information, return None, not fabricated or inferred.
- Return "None" not null in case of can not any information about attrubutes.

######################
-Real Data-
######################
List_data:
{prompt_add}

Content Json: 
{content}

Target Json: 
{target}
######################

Output: 
"""

TEMP_SUB_FIELD_MATCHING = """
-Goal-
Given an json that like content have information. 
Your task that will filling the empty variable in target json based on content json.
Filiing all content

-Requirements-
- Ouput is LIST of dictionary like example
- Answer with Japanese. Without transfer_id, transfer_id will answer by English.
- If you don not fill infor, instead null by "None". 
- Using "True" or "False" for boolean
- Convert all other datatype to string in answer. I mean that integer to string, boolean to string
- With the attribute that are based on list data, only give the elements not give number id.
- In choose task, ONLY choose from list data, not change or replace by new words.
- Attributes end with _id, output is only one string
- Attributes end with _ids, output is list string(even in case only one element)
- Did not answer ramblingly, to the point. Not fabricated, only based on the information given. \
With unknown or non-existent information, return "None", not fabricated or inferred.
- In here under attribute is list of dict, that means its have alot of smaller attrubute in dict type. 
- Return "None" not null in case of can not have any information about attrubutes.
- Use "None" not use null
- Only give list of dict, even if it only gives a dictionary
For example: 
Input: 
{
  "salary_informations_attributes": [
    "The employee receives a Housing Allowance with a minimum of 2000 and a maximum of 5000, a Transportation Allowance with a minimum of 500 and a maximum of 1500, and a Medical Allowance with a minimum of 300 and a maximum of 1000.",
    "The employee receives a Food Allowance with a minimum of 100 and a maximum of 300, an Internet Allowance with a minimum of 50 and a maximum of 200, and Health Insurance with a minimum of 400 and a maximum of 1000."
  ]
}

Output: 
{
      "salary_fixed_allowances_attributes": [
        {
          "id": "A",
          "fixed_allowance_memo": "Housing Allowance",
          "fixed_allowance_min": "2000",
          "fixed_allowance_max": "5000"
        },
        {
          "id": "B",
          "fixed_allowance_memo": "Transportation Allowance",
          "fixed_allowance_min": "500",
          "fixed_allowance_max": "1500"
        },
        {
          "id": "C",
          "fixed_allowance_memo": "Medical Allowance",
          "fixed_allowance_min": "300",
          "fixed_allowance_max": "1000"
        }
      ]
},

######################
-Real Data-
######################
List_data:
{prompt_add}

Content Json: 
{content}

Target Json: 
{target}
######################

Output: 
"""
