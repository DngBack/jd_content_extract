# import html2text

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))  # noqa

from custom.html2text_v2 import HTML2TextWithTiers # noqa

# Open the HTML file and read its content as a string
with open('test1.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# html2text_parse = HTML2TextWithTiers()
# html2text_parse.ignore_links = True

# html2text_output = html2text_parse.handle(html_content)

# # Can not parse with japanese
# print(html2text_output)
# Usage
converter = HTML2TextWithTiers()

converter.feed(html_content)
output = converter.get_output()
print(output)
