import json
import re
from collections import defaultdict

from pathlib import Path

def groups_entity(data: str = ""):
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
    str_output_json = json.dumps(grouped_entities, indent=4, ensure_ascii=False)
    dict_output_json = json.loads(str_output_json)

    return str_output_json, dict_output_json
