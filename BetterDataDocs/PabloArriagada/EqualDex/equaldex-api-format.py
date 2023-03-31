import json
from pathlib import Path

import requests
from access_key import API_KEY

PARENT_DIR = Path(__file__).parent.absolute()

url = "https://www.equaldex.com/api/region"

querystring = {"regionid": "gb", "apiKey": API_KEY}

headers = {"Content-Type": "application/json"}

response = requests.request("GET", url, headers=headers, params=querystring)

response_dict = json.loads(response.text)

print(response.text)

with open(PARENT_DIR / "equalidex.json", "w") as fp:
    json.dump(response_dict, fp, indent=4)
