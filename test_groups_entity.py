import json
import re
from collections import defaultdict

from pathlib import Path
 
data = Path("age_and_gender_smoking_prevention_details_remote_work_details_location_details.txt").read_text()

# Regular expression to match the entity tuples
pattern = r'\("entity"<\|>"(.*?)"<\|>"(.*?)"<\|>"(.*?)"\)'

# Dictionary to hold grouped entities
grouped_entities = defaultdict(list)

# Find all matches
matches = re.findall(pattern, data)

# Group entities by their category
for match in matches:
    attribute, category, description = match
    grouped_entities[category].append({
        "attribute": attribute,
        "description": description
    })

# Convert to JSON format
output_json = json.dumps(grouped_entities, indent=4, ensure_ascii=False)

# Output the result
print(output_json)
print(type(output_json))