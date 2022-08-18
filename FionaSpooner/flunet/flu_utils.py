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


def combine_country_datasets(data_dir: str, country_codes: list) -> pd.DataFrame:
    data_dfs = [
        pd.read_csv(f"{data_dir}{country_code}.csv") for country_code in country_codes
    ]
    combined_df = pd.concat(data_dfs)
    return combined_df


def aggregate_surveillance_type(
    combined_df: pd.DataFrame, sel_cols: list
) -> pd.DataFrame:

    df = combined_df[sel_cols]
    df = df.copy(deep=True)
    df["date"] = pd.to_datetime(
        df["ISO_WEEKSTARTDATE"], format="%Y-%m-%d", utc=True
    ).dt.date
    df_agg = (
        df.groupby(["COUNTRY_CODE", "COUNTRY/AREA/TERRITORY", "ISO_YEAR", "date"])
        .sum()
        .reset_index()
    )
    # Check we haven't lost any cases along the way
    assert combined_df["INF_ALL"].sum() == df_agg["INF_ALL"].sum()
    return df_agg


def combine_columns_calc_percent(df: pd.DataFrame) -> pd.DataFrame:
    df["ANOTSUBTYPED"] = (
        df["ANOTSUBTYPED"] + df["ANOTSUBTYPABLE"] + df["AOTHER_SUBTYPE"]
    )
    df["BVIC"] = (
        df["BVIC_2DEL"] + df["BVIC_3DEL"] + df["BVIC_NODEL"] + df["BVIC_DELUNK"]
    )
    df["pcnt_pos"] = (df["INF_ALL"] / (df["INF_ALL"] + df["INF_NEGATIVE"])) * 100
    df["pcnt_pos"] = df["pcnt_pos"].fillna(0).round(2)
    df["year"] = df["ISO_YEAR"].astype(int)
    assert (df["pcnt_pos"] <= 100).all()
    df = df.drop(
        [
            "ANOTSUBTYPABLE",
            "AOTHER_SUBTYPE",
            "BVIC_2DEL",
            "BVIC_3DEL",
            "BVIC_NODEL",
            "BVIC_DELUNK",
            "ISO_YEAR",
            "COUNTRY_CODE",
        ],
        axis=1,
    )
    df.rename(columns={"COUNTRY/AREA/TERRITORY": "Country"}, inplace=True)

    return df


def standardise_countries(df: pd.DataFrame) -> pd.DataFrame:
    stan_countries = pd.read_csv(
        "FionaSpooner/flunet/country_codes_country_standardized.csv"
    )
    stan_dict = stan_countries.set_index("Country").squeeze().to_dict()
    df["Country"] = df["Country"].map(stan_dict)

    return df
