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