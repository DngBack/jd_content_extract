import json
import re

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
    def remove_html_tags(text):
        """Remove HTML tags from a string."""
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)

    def remove_keys_with_id(self, data):
        """Remove all key-value pairs where the key contains 'Id' or 'id'."""
        if isinstance(data, dict):
            return {key: self.remove_keys_with_id(value) for key, value in data.items() if 'Id' not in key and 'id' not in key}
        elif isinstance(data, list):
            return [self.remove_keys_with_id(item) for item in data]
        else:
            return data

    def json_to_string(self, data=None, indent_level=0, seen_values=None):
        """Convert JSON data to a formatted string."""
        if data is None:
            data = self.data
        
        # Remove keys with 'Id' or 'id' before processing
        data = self.remove_keys_with_id(data)
        
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
                    # Remove HTML tags before checking if the value has been seen
                    cleaned_value = self.remove_html_tags(str(value))
                    if cleaned_value not in seen_values:
                        result.append(f"{indent}{key}: {cleaned_value}")
                        seen_values.add(cleaned_value)
        elif isinstance(data, list):
            for item in data:
                result.append(self.json_to_string(item, indent_level + 1, seen_values))
        else:
            # Remove HTML tags before checking if the value has been seen
            cleaned_data = self.remove_html_tags(str(data))
            if cleaned_data not in seen_values:
                result.append(f"{indent}{cleaned_data}")
                seen_values.add(cleaned_data)

        return "\n".join(result)

    def get_formatted_string(self):
        """Return the formatted JSON data as a string."""
        return self.json_to_string()

# Usage
file_path = 'test_1.json'
processor = JsonProcessor(file_path)

# Get the formatted string
formatted_string = processor.get_formatted_string()

# Print the formatted string
print(formatted_string)

# Save the formatted string to a text file
output_file_path = 'output.txt'
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write(formatted_string)
