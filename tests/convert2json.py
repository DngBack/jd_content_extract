import json

# Your JSON string
json_string = '''
{
    "user": {
        "name": "Jane Doe",
        "age": 25,
        "address": {
            "street": "123 Main St",
            "city": "New York",
            "zip": "10001"
        },
        "hobbies": ["reading", "gaming", "hiking"]
    },
    "active": true,
    "projects": [
        {
            "name": "Project Alpha",
            "duration": 12
        },
        {
            "name": "Project Beta",
            "duration": 6,
            "details": {
                "team_size": 5,
                "budget": 10000
            }
        }
    ]
}
'''

# Step 1: Parse the JSON string into a Python dictionary
data = json.loads(json_string)

# Step 2: Write the dictionary to a JSON file
with open('output.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)  # 'indent=4' for pretty formatting

print("JSON data has been written to 'output.json'")