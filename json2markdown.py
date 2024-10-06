import json
import re
from typing import Any, Dict, List, Union

# Define the set of allowed keys that we want to include
ALLOWED_KEYS = {"positionName", "jobName", "content", "markdownFreeText", "corporate"}

# Regular expression to find HTTP links
HTTP_LINK_PATTERN = r'https?://[^\s]+'
# Regular expression to remove unwanted characters
UNWANTED_CHARACTERS_PATTERN = r'[###■□□■■]+'

def clean_text(text: str) -> str:
    """Cleans the text by removing unwanted characters and HTTP links."""
    cleaned_text = re.sub(UNWANTED_CHARACTERS_PATTERN, '', text)
    cleaned_text = re.sub(HTTP_LINK_PATTERN, '', cleaned_text)
    cleaned_text = cleaned_text.replace('([', '')
    return cleaned_text.strip()  # Remove leading/trailing whitespace

def json_to_markdown(
    data: Union[Dict[str, Any], List[Any]], 
    indent_level: int = 0, 
    include_all: bool = False
) -> str:
    """Converts a JSON structure (dict or list) into a formatted Markdown string with indentation."""
    
    markdown_str: str = ""
    indent: str = " " * (indent_level * 2)  # Indentation based on the layer depth
    
    if isinstance(data, dict):
        # Iterate through dictionary
        for key, value in data.items():
            # Skip keys with value None or empty string
            if value is None or value == "":
                continue
            
            # Only process allowed keys, or continue processing inside a chosen key
            if include_all or key in ALLOWED_KEYS:
                # If value is dict or list, nest it, else write key-value on one line
                if isinstance(value, (dict, list)):
                    markdown_str += f"{indent}{key}:\n"
                    markdown_str += json_to_markdown(value, indent_level + 1, include_all or key in ALLOWED_KEYS)
                else:
                    # Clean the value if it's a string
                    if isinstance(value, str):
                        cleaned_value = clean_text(value)
                        markdown_str += f"{indent}{key}: {cleaned_value}\n"
                    else:
                        markdown_str += f"{indent}{key}: {value}\n"

    elif isinstance(data, list):
        # Iterate through lists
        for idx, item in enumerate(data):
            if isinstance(item, (dict, list)):
                markdown_str += json_to_markdown(item, indent_level + 1, include_all)
            else:
                markdown_str += f"{indent}- {clean_text(str(item))}\n"

    return markdown_str

def load_json_file(file_path: str) -> Union[Dict[str, Any], List[Any]]:
    """Loads JSON data from a file and returns it as a Python object (dict or list)."""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Example usage
file_path = "1.json"  # Replace with your JSON file path
json_data = load_json_file(file_path)

# Convert JSON to Markdown
markdown = json_to_markdown(json_data)

# Output the result
print(markdown)

# Write the result to a file
with open('output.txt', 'w', encoding='utf-8') as f:
    f.write(markdown)
