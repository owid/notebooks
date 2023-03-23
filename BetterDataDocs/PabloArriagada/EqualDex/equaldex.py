import json
from pathlib import Path

import pandas as pd
import requests
from structlog import get_logger

PARENT_DIR = Path(__file__).parent.absolute()


def extract_from_api(country_list: list, issue: str) -> pd.DataFrame:
    # Initialize logger.
    log = get_logger()

    url = "https://www.equaldex.com/api/region"
    headers = {"Content-Type": "application/json"}

    df = pd.DataFrame()
    df_historic = pd.DataFrame()

    for country in country_list:
        querystring = {
            "regionid": country,
            # "formatted": "true",
            "apiKey": "487549175181c7bcaeef608e90b1cb46916bc734",
        }

        status = 0
        # Status 404 = region not found
        while status != 200:
            response = requests.get(
                url, headers=headers, params=querystring, timeout=500
            )
            content = response.content
            status = response.status_code

        print(status)

        # if status == 404:
        #     log.warning(f"No data for {country}")

        response_dict = json.loads(content)

        try:
            country_name = response_dict["regions"]["region"]["name"]

        except:
            country_name = ""

        try:
            current_data = pd.DataFrame(
                response_dict["regions"]["region"]["issues"][issue]["current_status"],
                index=[0],
            )

        except:
            current_data = pd.DataFrame()

        try:
            historic_data = pd.DataFrame(
                response_dict["regions"]["region"]["issues"][issue]["history"],
            )

        except:
            historic_data = pd.DataFrame()

        current_data["country"] = country_name
        historic_data["country"] = country_name

        df_historic = pd.concat([df_historic, historic_data], ignore_index=True)
        df = pd.concat([df, current_data], ignore_index=True)

    return df, df_historic


country_list = ["gb", "us", "cl", "sa", "il", "asdf"]
df, df_historic = extract_from_api(country_list, issue="blood")

# Move country and year to the beginning
cols_to_move = ["country"]
df = df[cols_to_move + [col for col in df.columns if col not in cols_to_move]]
df_historic = df_historic[
    cols_to_move + [col for col in df_historic.columns if col not in cols_to_move]
]


df.to_csv(PARENT_DIR / "current.csv", index=False)
df_historic.to_csv(PARENT_DIR / "historic.csv", index=False)
