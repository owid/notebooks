import requests
import pandas as pd
import json


def get_country_codes(base_url: str) -> list:
    url = f"{base_url}?$apply=groupby((COUNTRY_CODE))"
    res = requests.get(url)
    assert res.ok
    value_json = json.loads(res.content)["value"]
    countries = pd.DataFrame.from_records(value_json)
    country_codes = countries["COUNTRY_CODE"].unique().tolist()
    return country_codes


def get_flu_data(base_url: str, code: str):
    country_url = f"{base_url}?$filter=COUNTRY_CODE%20eq%20%27{code}%27"
    data_json = requests.get(country_url).json()
    data_df = pd.DataFrame.from_records(data_json["value"])
    return data_df


def download_country_flu_data(
    data_dir: str, base_url: str, country_codes: list
) -> None:
    for country_code in country_codes:
        data_df = get_flu_data(base_url, country_code)
        data_df.to_csv(f"{data_dir}{country_code}.csv", index=False, escapechar="\\")
