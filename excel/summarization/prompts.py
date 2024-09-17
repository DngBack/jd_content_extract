from __future__ import annotations

import json
from typing import Tuple


OUTPUT_FORMAT = json.dumps(
    {'content': 'paragraph from the input table data'},
)

SYSTEM_MESSAGE = """
# 1. Instruction
You are an expert in analyzing table content.
Given table header and a list positions, contents represented in table cells, your mission is converting the input data table into a comprehensive paragraph.
"""

USER_MESSAGE = """
# 2. Required rules
- {header_prompt}
- Your output must represent structure of table
- Your output must be written by Vietnamese

# 3. Output format: JSON
{output_format}

# 4. Input table data
{input_data}

# 5. Explanation of input
Input data has 2 keys: headers contains list of horizontal and vertical header cell information in table, and table_rows contains list of row cell information in table.
Each cell element in list is represented in key-value format:
- coordinate key is the excel coordinate of cell
- text key is the text content in cell
"""
