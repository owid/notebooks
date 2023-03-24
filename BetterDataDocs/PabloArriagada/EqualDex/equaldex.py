import json
from pathlib import Path

import pandas as pd
import requests
from access_key import API_KEY
from structlog import get_logger

# Set directory path
PARENT_DIR = Path(__file__).parent.absolute()


def extract_from_api(country_list: list) -> pd.DataFrame:
    # Initialize logger.
    log = get_logger()

    # Set equaldex parameters: url and headers
    url = "https://www.equaldex.com/api/region"
    headers = {"Content-Type": "application/json"}

    # Define empty dataframes. df is for current data and df_historical for historical data
    df = pd.DataFrame()
    df_historical = pd.DataFrame()

    # Create an empty list of the countries with no data
    countries_no_data = []

    # For each country in the list
    for country in country_list:
        # Define query parameters
        querystring = {
            "regionid": country,
            # "formatted": "true",
            "apiKey": API_KEY,
        }

        # Run query, ensuring it delivers output with status 200
        status = 0
        while status != 200:
            response = requests.get(
                url, headers=headers, params=querystring, timeout=500
            )
            content = response.content
            status = response.status_code

            if status != 200:
                log.error(f"{country}: Status {status}")

        # Create a dictionary with the output
        response_dict = json.loads(content)

        # Get the country name from the response
        try:
            country_name = response_dict["regions"]["region"]["name"]

        except:
            country_name = ""

        # Get the list of issues available
        try:
            issue_list = list(response_dict["regions"]["region"]["issues"].keys())

        except:
            # If no issue list is found, add this country to the "countries with no data" list
            countries_no_data.append(country)
            issue_list = []

        # For each issue on the list
        for issue in issue_list:
            # Get the current status
            try:
                current_data = pd.DataFrame(
                    response_dict["regions"]["region"]["issues"][issue][
                        "current_status"
                    ],
                    index=[0],
                )

            except:
                log.warning(f"{country_name}: No current data for {issue}")
                current_data = pd.DataFrame()

            # Get the history of the issue in the country
            try:
                historical_data = pd.DataFrame(
                    response_dict["regions"]["region"]["issues"][issue]["history"],
                )

            except:
                log.warning(f"{country_name}: No historical data for {issue}")
                historical_data = pd.DataFrame()

            # Add country name column to the dataframe
            current_data["country"] = country_name
            historical_data["country"] = country_name

            # Add issue column to the dataframe
            current_data["issue"] = issue
            historical_data["issue"] = issue

            # Concatenate data from previous countries with current country
            df_historical = pd.concat(
                [df_historical, historical_data], ignore_index=True
            )
            df = pd.concat([df, current_data], ignore_index=True)

    # Move country and issue to the beginning
    cols_to_move = ["country", "issue"]
    df = df[cols_to_move + [col for col in df.columns if col not in cols_to_move]]
    df_historical = df_historical[
        cols_to_move + [col for col in df_historical.columns if col not in cols_to_move]
    ]

    # Export files
    df.to_csv(PARENT_DIR / "current.csv", index=False)
    df_historical.to_csv(PARENT_DIR / "historical.csv", index=False)

    # Error message with a summary of countries with no data
    if countries_no_data:
        log.error(
            f"Data was not found for the following {len(countries_no_data)} countries: \n{countries_no_data}"
        )


# Define country list
# country_list = ["gb", "us", "cl", "querty", "sa", "il", "asdf"]
country_list = [
    "AF",
    "AL",
    "DZ",
    "AS",
    "AD",
    "AO",
    "AI",
    "AQ",
    "AG",
    "AR",
    "AM",
    "AW",
    "AU",
    "AT",
    "AZ",
    "BS",
    "BH",
    "BD",
    "BB",
    "BY",
    "BE",
    "BZ",
    "BJ",
    "BM",
    "BT",
    "BO",
    "BQ",
    "BA",
    "BW",
    "BV",
    "BR",
    "IO",
    "BN",
    "BG",
    "BF",
    "BI",
    "CV",
    "KH",
    "CM",
    "CA",
    "KY",
    "CF",
    "TD",
    "CL",
    "CN",
    "CX",
    "CC",
    "CO",
    "KM",
    "CD",
    "CG",
    "CK",
    "CR",
    "HR",
    "CU",
    "CW",
    "CY",
    "CZ",
    "CI",
    "DK",
    "DJ",
    "DM",
    "DO",
    "EC",
    "EG",
    "SV",
    "GQ",
    "ER",
    "EE",
    "SZ",
    "ET",
    "FK",
    "FO",
    "FJ",
    "FI",
    "FR",
    "GF",
    "PF",
    "TF",
    "GA",
    "GM",
    "GE",
    "DE",
    "GH",
    "GI",
    "GR",
    "GL",
    "GD",
    "GP",
    "GU",
    "GT",
    "GG",
    "GN",
    "GW",
    "GY",
    "HT",
    "HM",
    "VA",
    "HN",
    "HK",
    "HU",
    "IS",
    "IN",
    "ID",
    "IR",
    "IQ",
    "IE",
    "IM",
    "IL",
    "IT",
    "JM",
    "JP",
    "JE",
    "JO",
    "KZ",
    "KE",
    "KI",
    "KP",
    "KR",
    "KW",
    "KG",
    "LA",
    "LV",
    "LB",
    "LS",
    "LR",
    "LY",
    "LI",
    "LT",
    "LU",
    "MO",
    "MG",
    "MW",
    "MY",
    "MV",
    "ML",
    "MT",
    "MH",
    "MQ",
    "MR",
    "MU",
    "YT",
    "MX",
    "FM",
    "MD",
    "MC",
    "MN",
    "ME",
    "MS",
    "MA",
    "MZ",
    "MM",
    "NA",
    "NR",
    "NP",
    "NL",
    "NC",
    "NZ",
    "NI",
    "NE",
    "NG",
    "NU",
    "NF",
    "MK",
    "MP",
    "NO",
    "OM",
    "PK",
    "PW",
    "PS",
    "PA",
    "PG",
    "PY",
    "PE",
    "PH",
    "PN",
    "PL",
    "PT",
    "PR",
    "QA",
    "RO",
    "RU",
    "RW",
    "RE",
    "BL",
    "SH",
    "KN",
    "LC",
    "MF",
    "PM",
    "VC",
    "WS",
    "SM",
    "ST",
    "SA",
    "SN",
    "RS",
    "SC",
    "SL",
    "SG",
    "SX",
    "SK",
    "SI",
    "SB",
    "SO",
    "ZA",
    "GS",
    "SS",
    "ES",
    "LK",
    "SD",
    "SR",
    "SJ",
    "SE",
    "CH",
    "SY",
    "TW",
    "TJ",
    "TZ",
    "TH",
    "TL",
    "TG",
    "TK",
    "TO",
    "TT",
    "TN",
    "TM",
    "TC",
    "TV",
    "TR",
    "UG",
    "UA",
    "AE",
    "GB",
    "UM",
    "US",
    "UY",
    "UZ",
    "VU",
    "VE",
    "VN",
    "VG",
    "VI",
    "WF",
    "EH",
    "YE",
    "ZM",
    "ZW",
    "AX",
]

extract_from_api(country_list)
