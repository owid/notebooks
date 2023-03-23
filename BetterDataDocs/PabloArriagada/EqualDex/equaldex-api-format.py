import json
from pathlib import Path

import requests

PARENT_DIR = Path(__file__).parent.absolute()

url = "https://www.equaldex.com/api/region"

querystring = {"regionid": "gb", "apiKey": "487549175181c7bcaeef608e90b1cb46916bc734"}

headers = {"Content-Type": "application/json"}

response = requests.request("GET", url, headers=headers, params=querystring)

response_dict = json.loads(response.text)

print(response.text)

with open(PARENT_DIR / "equalidex.json", "w") as fp:
    json.dump(response_dict, fp, indent=4)
