import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))  # noqa

from utils.wrapper import Wrapper

# Open the HTML file and read its content as a string
with open('test1.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Example usage of the Wrapper class
wrapper = Wrapper(body_width=0)
wrapped_text = wrapper.optwrap(html_content)
print(wrapped_text)