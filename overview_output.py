import json

# Get Example
with open('sample.json', 'r', encoding="utf-8") as file:
    # Load the dictionary from the JSON file
    output_dict = json.load(file)

print(len(output_dict))