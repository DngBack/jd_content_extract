import html2text

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))  # noqa

# Open the HTML file and read its content as a string
with open('test1.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

html2text_parse = html2text.HTML2Text()
html2text_parse.ignore_links = True

html2text_output = html2text_parse.handle(html_content)

# Can not parse with japanese
print(html2text_output)
