# settings.py
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from scrapegraphai.graphs import SmartScraperGraph
# scrapegrapthai packages

sys.path.append(str(Path(__file__).parent.parent))  # noqa

dotenv_path = '.env'
load_dotenv(dotenv_path)

OPENAI_KEY = os.environ.get('OPENAI_APIKEY')
print(OPENAI_KEY)

# Define the configuration for the scraping pipeline
graph_config = {
    'llm': {
        'api_key': OPENAI_KEY,
        'model': 'gpt-4o-mini',
    },
    'verbose': True,
    'headless': False,
}

# Create the SmartScraperGraph instance
smart_scraper_graph = SmartScraperGraph(
    prompt='Can you get all information about that job?',
    source='https://www.topcv.vn/viec-lam/senior-software-\
        architect-luong-upto-2-700-usd-tai-ha-noi/1414020.html?\
            ta_source=BoxFeatureJob_LinkDetail',
    config=graph_config
)

# Run the pipeline
result = smart_scraper_graph.run()
print(json.dumps(result, indent=5))