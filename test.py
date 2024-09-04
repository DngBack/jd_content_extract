import json
import re
from datetime import datetime

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

    def json_to_string(self, data=None, indent_level=0, seen_values=None):
        """Convert JSON data to a formatted string."""
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

        if seen_values is None:
            seen_values = set()

        result = []
        indent = ' ' * (indent_level * 4)

        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    result.append(f"{indent}{key}:")
                    result.append(self.json_to_string(value, indent_level + 1, seen_values))
                else:
                    if str(value) not in seen_values:
                        result.append(f"{indent}{key}: {value}")
                        seen_values.add(str(value))
        elif isinstance(data, list):
            for item in data:
                result.append(self.json_to_string(item, indent_level + 1, seen_values))
        else:
            if str(data) not in seen_values:
                result.append(f"{indent}{data}")
                seen_values.add(str(data))

        return "\n".join(result)

    def get_formatted_string(self):
        """Return the formatted JSON data as a string."""
        return self.json_to_string()

# Usage
file_path = 'test_2.json'
processor = JsonProcessor(file_path)

# Get the formatted string
formatted_string = processor.get_formatted_string()

# Print the formatted string
print(formatted_string)

# Save the formatted string to a text file
output_file_path = 'output.txt'
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write(formatted_string)
