import requests
import pandas as pd
import json
import numpy as np
import time


def get_metadata(output_path) -> pd.DataFrame:
    r = requests.get(
        "https://frontdoor-l4uikgap6gz3m.azurefd.net/FLUMART/VIW_FLU_METADATA"
    )
    value_json = json.loads(r.content)["value"]
    metadata = pd.DataFrame.from_records(value_json)
    metadata.to_csv(output_path, index=False)
    return metadata


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
    try:
        data_json = requests.get(country_url).json()
        data_df = pd.DataFrame.from_records(data_json["value"])
    except requests.exceptions.JSONDecodeError:
        time.sleep(5)
        data_json = requests.get(country_url).json()
        data_df = pd.DataFrame.from_records(data_json["value"])

    return data_df


def download_country_flu_data(
    data_dir: str, base_url: str, country_codes: list
) -> None:
    for country_code in country_codes:
        print(country_code, end=" ", flush=True)
        data_df = get_flu_data(base_url, country_code)
        data_df.to_csv(f"{data_dir}{country_code}.csv", index=False, escapechar="\\")


def combine_country_datasets(data_dir: str, country_codes: list) -> pd.DataFrame:
    data_dfs = [
        pd.read_csv(f"{data_dir}{country_code}.csv") for country_code in country_codes
    ]
    combined_df = pd.concat(data_dfs)
    combined_df = combined_df[combined_df["HEMISPHERE"].isin(["NH", "SH"])]
    return combined_df


def aggregate_surveillance_type(combined_df: pd.DataFrame) -> pd.DataFrame:
    sel_cols = [
        "COUNTRY/AREA/TERRITORY",
        "HEMISPHERE",
        "ISO_WEEKSTARTDATE",
        "ORIGIN_SOURCE",
        "AH1N12009",
        "AH1",
        "AH3",
        "AH5",
        "AH7N9",
        "ANOTSUBTYPED",
        "ANOTSUBTYPABLE",
        "AOTHER_SUBTYPE",
        "INF_A",
        "BVIC_2DEL",
        "BVIC_3DEL",
        "BVIC_NODEL",
        "BVIC_DELUNK",
        "BYAM",
        "BNOTDETERMINED",
        "INF_B",
        "INF_ALL",
        "INF_NEGATIVE",
        "SPEC_PROCESSED_NB",
        "SPEC_RECEIVED_NB",
    ]
    df = combined_df[sel_cols]
    df = df.copy(deep=True)
    df["date"] = pd.to_datetime(
        df["ISO_WEEKSTARTDATE"], format="%Y-%m-%d", utc=True
    ).dt.date
    df_agg = (
        df.groupby(["COUNTRY/AREA/TERRITORY", "HEMISPHERE", "date"]).sum().reset_index()
    )
    df_agg = df_agg.rename(columns={"COUNTRY/AREA/TERRITORY": "Country"})
    # Check we haven't lost any cases along the way
    assert combined_df["INF_ALL"].sum() == df_agg["INF_ALL"].sum()
    return df_agg


def aggregate_regions(df: pd.DataFrame) -> pd.DataFrame:

    glob_df = df.groupby(["date"]).sum().reset_index()
    glob_df["Country"] = "World"
    nh_df = df[df["HEMISPHERE"] == "NH"].groupby(["date"]).sum().reset_index()
    nh_df["Country"] = "Northern Hemisphere"
    sh_df = df[df["HEMISPHERE"] == "SH"].groupby(["date"]).sum().reset_index()
    sh_df["Country"] = "Southern Hemisphere"
    df.drop(["HEMISPHERE"], axis=1, inplace=True)
    df = pd.concat([df, glob_df, nh_df, sh_df])
    return df


def combine_columns_calc_percent(df: pd.DataFrame) -> pd.DataFrame:
    df["ANOTSUBTYPED"] = (
        df["ANOTSUBTYPED"] + df["ANOTSUBTYPABLE"] + df["AOTHER_SUBTYPE"]
    )
    df["BVIC"] = (
        df["BVIC_2DEL"] + df["BVIC_3DEL"] + df["BVIC_NODEL"] + df["BVIC_DELUNK"]
    )
    df["INF_NEGATIVE"] = df["INF_NEGATIVE"].replace(r"^\s*$", np.nan, regex=True)
    df["denom"] = (
        df[["INF_NEGATIVE", "SPEC_PROCESSED_NB"]]
        .replace(0, np.nan)
        .bfill(axis=1)
        .iloc[:, 0]
        .fillna(0)
    )
    df["denominator"] = (
        df[["denom", "SPEC_RECEIVED_NB"]]
        .replace(0, np.nan)
        .bfill(axis=1)
        .iloc[:, 0]
        .fillna(0)
    )
    df["pcnt_pos_neg"] = (df["INF_ALL"] / (df["INF_ALL"] + df["INF_NEGATIVE"])) * 100
    df["pcnt_pos_denom"] = (df["INF_ALL"] / df["denominator"]) * 100

    df_den = df[(df["INF_NEGATIVE"] == 0) & (df["denominator"] != 0)]
    df_neg = df[df["INF_NEGATIVE"] == df["denominator"]]

    assert (
        df_neg.shape[0] + df_den.shape[0] == df.shape[0]
    ), "Some rows are missing from one of the dataframes"

    df_neg = df_neg.drop(["denom", "denominator", "pcnt_pos_denom"], axis=1).rename(
        columns={"pcnt_pos_neg": "pcnt_pos"}
    )
    df_den = df_den.drop(["denom", "denominator", "pcnt_pos_neg"], axis=1).rename(
        columns={"pcnt_pos_denom": "pcnt_pos"}
    )

    df_com = pd.concat([df_neg, df_den])
    assert df_com.shape[0] == df.shape[0]

    df_com["pcnt_pos"] = df_com["pcnt_pos"].round(2)
    over_100_pcnt = df_com[df_com["pcnt_pos"] > 100].shape[0]
    print(
        f"{over_100_pcnt} variables with a percentage positive over 100. We'll set these to NA."
    )
    df_com.loc[df_com["pcnt_pos"] > 100, "pcnt_pos"] = np.nan

    # Rows where the percentage positive is 100 but all possible denominators are 0
    df_com.loc[
        (df_com["pcnt_pos"] == 100)
        & (df_com["INF_NEGATIVE"] == 0)
        & (df_com["SPEC_PROCESSED_NB"] == 0)
        & (df_com["SPEC_RECEIVED_NB"] == 0),
        "pcnt_pos",
    ] = np.nan

    df_com = df_com.drop(
        [
            "ANOTSUBTYPABLE",
            "AOTHER_SUBTYPE",
            "BVIC_2DEL",
            "BVIC_3DEL",
            "BVIC_NODEL",
            "BVIC_DELUNK",
        ],
        axis=1,
    )
    df_com.rename(columns={"COUNTRY/AREA/TERRITORY": "Country"}, inplace=True)

    return df_com


def standardise_countries(df: pd.DataFrame, path: str) -> pd.DataFrame:
    stan_countries = pd.read_csv(f"{path}/country_codes_country_standardized.csv")
    stan_dict = stan_countries.set_index("Country").squeeze().to_dict()

    df["Country_stan"] = df["Country"].map(stan_dict)
    missing_countries = (
        df["Country"][df["Country_stan"].isna()].drop_duplicates().tolist()
    )
    assert (
        df["Country_stan"].isna().sum() == 0
    ), f"{missing_countries} are not standardised"

    df = df.drop(columns=["Country"])
    df = df.rename(columns={"Country_stan": "Country"})
    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df = df[cols]
    return df


def clean_fluid_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.query("AGEGROUP_CODE == 'All' & CASE_INFO.isin(['ILI', 'SARI', 'ARI'])")
    df["date"] = pd.to_datetime(
        df["ISO_WEEKSTARTDATE"], format="%Y-%m-%d", utc=True
    ).dt.date
    df = df[
        [
            "HEMISPHERE",
            "COUNTRY/AREA/TERRITORY",
            "date",
            "REPORTED_CASES",
            "OUTPATIENTS",
            "INPATIENTS",
            "CASE_INFO",
        ]
    ]
    df = df.pivot(
        index=[
            "HEMISPHERE",
            "COUNTRY/AREA/TERRITORY",
            "date",
            "OUTPATIENTS",
            "INPATIENTS",
        ],
        columns="CASE_INFO",
        values=[
            "REPORTED_CASES",
        ],
    ).reset_index()

    df.columns = list(map("".join, df.columns))

    df = df.dropna(
        subset=["REPORTED_CASESARI", "REPORTED_CASESILI", "REPORTED_CASESSARI"],
        how="all",
    )
    df = df.rename(
        columns={
            "COUNTRY/AREA/TERRITORY": "Country",
            "REPORTED_CASESARI": "ari_cases",
            "REPORTED_CASESSARI": "sari_cases",
            "REPORTED_CASESILI": "ili_cases",
        }
    )
    return df


def calculate_fluid_rates(df: pd.DataFrame) -> pd.DataFrame:
    df["ili_cases_per_thousand_inpatients"] = round(
        (df["ili_cases"] / df["OUTPATIENTS"]) * 1000, 2
    )
    df["ari_cases_per_thousand_inpatients"] = round(
        (df["ari_cases"] / df["OUTPATIENTS"]) * 1000, 2
    )
    df["sari_cases_per_hundred_inpatients"] = round(
        (df["sari_cases"] / df["INPATIENTS"]) * 100, 2
    )

    return df
