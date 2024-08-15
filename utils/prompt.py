TEMP_MATCHING_ENTITTY = """
-Goal-
Given an json that like content have information. 
Your task that will filling the empty variable in target json based on content json.
Filiing all content

-Requirements-
- Output is only finaly output json format
- Answer with Enlish
- Convert Japanese to English
- If you don not fill infor, instead null by None
- Using "True" or "False" for boolean
- Convert all other datatype to string in answer. I mean that integer to string, boolean to string

######################
-Real Data-
######################
Content Json: {content}
Target Json: {target}
######################

Output: 
"""