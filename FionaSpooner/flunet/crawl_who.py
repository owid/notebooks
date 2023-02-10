import requests
import json
import pandas as pd

base_url = "https://frontdoor-l4uikgap6gz3m.azurefd.net/FLUMART/"
r = requests.get(base_url)
vals = json.loads(r.content)["value"]
df = pd.DataFrame.from_records(vals)
urls = df["url"].unique().tolist()

urls.remove("GEM_FACTS_BY_YEAR_SEX_AGE")

for url in urls:
    # print(url)
    test_url = f"{base_url}{url}"
    res = requests.get(test_url)
    res_out = json.loads(res.content)
    if res_out != {"error": "NOT_ALLOWED"}:
        print(test_url + " has data!")
