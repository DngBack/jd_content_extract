import html2text


import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))  # noqa
from get_content.utils.scrape import scrape_html
# from custom.html2text_v2 import HTML2TextWithTiers # noqa

# Open the HTML file and read its content as a string
with open('test1.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

html2text_output, type_html2text_output = scrape_html(html_content)

# Can not parse with japanese
print(html2text_output)
print(type_html2text_output)
# Usage
# converter = HTML2TextWithTiers()

# converter.feed(html_content)
# output = converter.get_output()
# print(output)
