import json
import re
from utils.aws_sonet import AwsSonet35
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv(".env")

ACCESS_KEY = os.environ.get('ACCESS_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')

model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"
# Set up llm 
llm = AwsSonet35()
llm.setup(ACCESS_KEY, SECRET_KEY, model_id)

class JsonProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.read_json_file()

    def read_json_file(self):
        """Read JSON data from the file."""
        with open(self.file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    @staticmethod
    def contains_html(text):
        """Check if a string contains HTML tags."""
        html_pattern = re.compile('<.*?>')
        return bool(html_pattern.search(text))

    @staticmethod
    def is_datetime_string(text):
        """Check if a string is in a datetime format."""
        try:
            datetime.fromisoformat(text.rstrip('Z'))
            return True
        except ValueError:
            return False

    @staticmethod
    def contains_url(text):
        """Check if a string contains a URL."""
        url_pattern = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        )
        return bool(url_pattern.search(text))

    def remove_html_values(self, data):
        """Remove all key-value pairs where the value contains HTML."""
        if isinstance(data, dict):
            return {key: self.remove_html_values(value) for key, value in data.items() if not (isinstance(value, str) and self.contains_html(value))}
        elif isinstance(data, list):
            return [self.remove_html_values(item) for item in data]
        else:
            return data

    def remove_keys_with_id(self, data):
        """Remove all key-value pairs where the key contains 'Id' or 'id'."""
        if isinstance(data, dict):
            return {key: self.remove_keys_with_id(value) for key, value in data.items() if 'Id' not in key and 'id' not in key}
        elif isinstance(data, list):
            return [self.remove_keys_with_id(item) for item in data]
        else:
            return data

    def remove_datetime_values(self, data):
        """Remove all key-value pairs where the value is a datetime string."""
        if isinstance(data, dict):
            return {key: self.remove_datetime_values(value) for key, value in data.items() if not (isinstance(value, str) and self.is_datetime_string(value))}
        elif isinstance(data, list):
            return [self.remove_datetime_values(item) for item in data]
        else:
            return data

    def remove_url_values(self, data):
        """Remove all key-value pairs where the value contains a URL."""
        if isinstance(data, dict):
            return {key: self.remove_url_values(value) for key, value in data.items() if not (isinstance(value, str) and self.contains_url(value))}
        elif isinstance(data, list):
            return [self.remove_url_values(item) for item in data]
        else:
            return data

    def remove_boolean_values(self, data):
        """Remove all key-value pairs where the value is a boolean."""
        if isinstance(data, dict):
            return {key: self.remove_boolean_values(value) for key, value in data.items() if not isinstance(value, bool)}
        elif isinstance(data, list):
            return [self.remove_boolean_values(item) for item in data]
        else:
            return data

    def json_to_paragraph(self, data=None):
        """Convert JSON data into a paragraph format."""
        if data is None:
            data = self.data
        
        # Remove keys with 'Id' or 'id'
        data = self.remove_keys_with_id(data)
        # Remove values containing HTML
        data = self.remove_html_values(data)
        # Remove values that are datetime strings
        data = self.remove_datetime_values(data)
        # Remove values containing URLs
        data = self.remove_url_values(data)
        # Remove boolean values
        data = self.remove_boolean_values(data)

        paragraphs = []
        
        def recursive_format(data, prefix=""):
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, (dict, list)):
                        recursive_format(value, f"{prefix}{key}: ")
                    else:
                        paragraphs.append(f"{prefix}{key}: {value}")
            elif isinstance(data, list):
                for item in data:
                    recursive_format(item, prefix)
            else:
                paragraphs.append(f"{prefix}{data}")

        recursive_format(data)
        
        return " ".join(paragraphs)

    def get_paragraph(self):
        """Return the JSON data formatted as a paragraph."""
        return self.json_to_paragraph()

# Usage
file_path = 'test_1.json'
processor = JsonProcessor(file_path)

# Get the paragraph
paragraph = processor.get_paragraph()

# Print the paragraph
print(paragraph)

# Save the paragraph to a text file
output_file_path = 'output_paragraph.txt'
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write(paragraph)
