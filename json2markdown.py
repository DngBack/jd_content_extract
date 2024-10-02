import json
import re

# Define the set of allowed keys that we want to include
ALLOWED_KEYS = {"positionName", "jobName", "content", "markdownFreeText", "corporate"}

# Regular expression to find HTTP links
HTTP_LINK_PATTERN = r'https?://[^\s]+'
# Regular expression to remove unwanted characters
UNWANTED_CHARACTERS_PATTERN = r'[###■□□■■]+'

def clean_text(text):
    # Remove unwanted characters and HTTP links
    cleaned_text = re.sub(UNWANTED_CHARACTERS_PATTERN, '', text)
    cleaned_text = re.sub(HTTP_LINK_PATTERN, '', cleaned_text)
    return cleaned_text.strip()  # Remove leading/trailing whitespace

def json_to_markdown(data, indent_level=0, include_all=False, numbering=None):
    markdown_str = ""
    
    if numbering is None:
        numbering = []  # Initialize numbering for the first call

    if isinstance(data, dict):
        # Iterate through dictionary
        for key, value in data.items():
            # Skip keys with value None or empty string
            if value is None or value == "":
                continue
            
            # Only process allowed keys, or continue processing inside a chosen key
            if include_all or key in ALLOWED_KEYS:
                # Create the current number based on the level
                current_number = f"{'.'.join(map(str, numbering))}.{len(numbering) + 1}" if numbering else f"{len(numbering) + 1}"
                numbering.append(len(numbering) + 1)  # Add the next level to the numbering

                # If value is dict or list, nest it, else write key-value on one line
                if isinstance(value, (dict, list)):
                    markdown_str += f"{current_number} {key}:\n"
                    markdown_str += json_to_markdown(value, indent_level + 1, include_all or key in ALLOWED_KEYS, numbering)
                else:
                    # Clean the value if it's a string
                    if isinstance(value, str):
                        cleaned_value = clean_text(value)
                        markdown_str += f"{current_number} {key}: {cleaned_value}\n"
                    else:
                        markdown_str += f"{current_number} {key}: {value}\n"

                numbering.pop()  # Remove the last number after processing

    elif isinstance(data, list):
        # Iterate through lists
        for idx, item in enumerate(data):
            current_number = f"{'.'.join(map(str, numbering))}.{idx + 1}" if numbering else str(idx + 1)
            if isinstance(item, dict) and len(item) == 2:
                # If the dict has exactly 2 elements, format as key: value on one line
                keys = list(item.keys())
                if isinstance(item[keys[1]], str):
                    cleaned_value = clean_text(item[keys[1]])
                    markdown_str += f"- \"{item[keys[0]]}\": \"{cleaned_value}\"\n"
                else:
                    markdown_str += f"- \"{item[keys[0]]}\": \"{item[keys[1]]}\"\n"
            else:
                # Otherwise, treat as a nested list
                markdown_str += f"- {current_number} "
                if isinstance(item, (dict, list)):
                    markdown_str += "\n"  # Move to next line for nested items
                markdown_str += json_to_markdown(item, indent_level + 1, include_all)

    return markdown_str

# Function to load JSON from a file
def load_json_file(file_path):
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
