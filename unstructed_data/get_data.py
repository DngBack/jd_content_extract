import html_to_json

import json 

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))  # noqa

# Open the HTML file and read its content as a string
with open('test1.html', 'r', encoding='utf-8') as file:
    html_string = file.read()

tables = html_to_json.convert(html_string)
tables = json.dumps(tables, ensure_ascii=False)
print(tables)
