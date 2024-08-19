TEMP_MATCHING_ENTITTY = """
-Goal-
Given an json that like content have information. 
Your task that will filling the empty variable in target json based on content json.
Filiing all content

-Requirements-
- Output is only finaly output json format
- Answer with Japanese 
- If you don not fill infor, instead null by None
- Using "True" or "False" for boolean
- Convert all other datatype to string in answer. I mean that integer to string, boolean to string
- With the attribute that are based on list data, only give the elements nót give number id.
######################
-Real Data-
######################
List_data:
{List_data}

Content Json: 
{content}

Target Json: 
{target}
######################

Output: 
"""