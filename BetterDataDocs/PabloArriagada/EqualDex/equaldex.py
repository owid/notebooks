import ast
import json

import pandas as pd
import requests

url = "https://www.equaldex.com/api/region"

querystring = {
    "regionid": "sa",
    # "formatted": "true",
    "apiKey": "487549175181c7bcaeef608e90b1cb46916bc734",
}

headers = {"Content-Type": "application/json"}

status = 0

while status != 200:
    response = requests.get(url, headers=headers, params=querystring, timeout=500)
    content = response.content
    status = response.status_code

# response = requests.request("GET", url, headers=headers, params=querystring)

# print(response.text)
# response_dict = response.text.to_dict()
# response_dict = ast.literal_eval(response.text)
response_dict = json.loads(content)
# print(response_dict)
print(response_dict["regions"]["region"]["issues"]["homosexuality"]["current_status"])

df = pd.DataFrame(
    response_dict["regions"]["region"]["issues"]["homosexuality"]["current_status"],
    index=[0],
)
print(df)

# with open("equalidex.json", "w") as fp:
#     json.dump(response_dict, fp, indent=4)
