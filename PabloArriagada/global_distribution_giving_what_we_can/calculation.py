"""
SCRIPT TO CALCULATE GLOBAL DISTRIBUTION OF GIVING WHAT WE CAN
This script calculates the global distribution of Giving What We Can, using the World Bank PIP data, together with CPI and PPP conversion factors from the World Development Indicators. The script exports the results to a csv file.

https://api.worldbank.org/v2/en/indicator/PA.NUS.PRVT.PP?downloadformat=csv
https://api.worldbank.org/v2/en/indicator/FP.CPI.TOTL?downloadformat=csv
"""

from pathlib import Path

import pandas as pd

PARENT_DIR = Path(__file__).parent.absolute()

# Define OWID version of PIP data
PIP_VERSION = "2024-03-27"

# Define PIP percentiles URL
PIP_URL = f"http://catalog.ourworldindata.org/garden/wb/{PIP_VERSION}/world_bank_pip/percentiles_income_consumption_2017.feather"

# Define paths for the PPP and CPI data
PPP_FILE_PATH = f"{PARENT_DIR}/API_PA.NUS.PRVT.PP_DS2_en_csv_v2_374406.csv"
CPI_FILE_PATH = f"{PARENT_DIR}/API_FP.CPI.TOTL_DS2_en_csv_v2_381228.csv"

# Define maximum year for CPI
MAX_YEAR_CPI = 2022

df_percentiles = pd.read_feather(PIP_URL)

# Filter data to only include country=World and ppp_version = 2017
df_percentiles = df_percentiles[(df_percentiles["country"] == "World")].reset_index(
    drop=True
)

# Compare thr values with the one in the previous row
df_percentiles["thr_previous"] = (
    df_percentiles["thr"].groupby(df_percentiles["year"]).shift(1)
)
df_percentiles["thr_check"] = df_percentiles["thr"] >= df_percentiles["thr_previous"]

# Assert that all values are True
df_percentiles_check = df_percentiles[
    (df_percentiles["thr_check"]) & (df_percentiles["percentile"] != 1)
]
assert df_percentiles_check[
    "thr_check"
].all(), "The global distribution is not monotonically increasing"

# Keep only the relevant columns
df_percentiles = df_percentiles[["country", "year", "percentile", "thr"]]

# Filter for the latest year
df_percentiles = df_percentiles[
    df_percentiles["year"] == df_percentiles["year"].max()
].reset_index(drop=True)

# Export to csv
df_percentiles.to_csv(f"{PARENT_DIR}/pip_global_percentiles.csv", index=False)

# PPP CONVERSION FACTORS
# Load ppp conversion factors and CPI
df_ppp_factors = pd.read_csv(PPP_FILE_PATH, skiprows=4)
df_cpi = pd.read_csv(CPI_FILE_PATH, skiprows=4)

# Remove columns containing "Unnamed" in their name
columns_to_drop = [col for col in df_ppp_factors.columns if "Unnamed" in col]
df_ppp_factors = df_ppp_factors.drop(columns=columns_to_drop)

# Remove columns containing "Unnamed" in their name
columns_to_drop = [col for col in df_cpi.columns if "Unnamed" in col]
df_cpi = df_cpi.drop(columns=columns_to_drop)

# Drop "Indicator Name","Indicator Code"
columns_to_drop = ["Indicator Name", "Indicator Code"]
df_ppp_factors = df_ppp_factors.drop(columns=columns_to_drop)
df_cpi = df_cpi.drop(columns=columns_to_drop)

# Select in df_ppp_factors only the columns of interest (Country Name, Country Code, 2017)
df_ppp_factors = df_ppp_factors[["Country Name", "Country Code", "2017"]]
df_ppp_factors = df_ppp_factors.rename(
    columns={
        "Country Name": "country",
        "Country Code": "country_code",
        "2017": "ppp_2017",
    }
)

# Make df_cpi long
df_cpi = df_cpi.melt(
    id_vars=["Country Name", "Country Code"], var_name="year", value_name="cpi"
)
df_cpi = df_cpi.rename(
    columns={"Country Name": "country", "Country Code": "country_code"}
)

# Make year integer
df_cpi["year"] = df_cpi["year"].astype(int)

# Filter for 2017 and the maximum year
df_cpi = df_cpi[
    (df_cpi["year"] == 2017) | (df_cpi["year"] == MAX_YEAR_CPI)
].reset_index(drop=True)

# Make table wide, by naming the columns cpi_2017 and cpi_max
df_cpi = df_cpi.pivot(index="country_code", columns="year", values="cpi").reset_index()

# Rename columns
df_cpi = df_cpi.rename(columns={2017: "cpi_2017", MAX_YEAR_CPI: f"cpi_{MAX_YEAR_CPI}"})

print(df_cpi)

# Calculate the inflation rate between 2017 and the maximum year
df_cpi["inflation_rate"] = df_cpi[f"cpi_{MAX_YEAR_CPI}"] / df_cpi["cpi_2017"]

# Merge df_ppp_factors and df_cpi
df_ppp = df_ppp_factors.merge(
    df_cpi[["country_code", "cpi_2017", f"cpi_{MAX_YEAR_CPI}", "inflation_rate"]],
    on="country_code",
    how="left",
)

# Calculate the ppp conversion factor for the most recent year
df_ppp["ppp_factor"] = df_ppp["ppp_2017"] * df_ppp["inflation_rate"]

# Remove empty values of pa_nus_prvt_pp
df_ppp = df_ppp[~df_ppp["ppp_factor"].isna()].reset_index(drop=True)

# Sort by country
df_ppp = df_ppp.sort_values(by=["country"]).reset_index(drop=True)

# Export to csv
df_ppp.to_csv(f"{PARENT_DIR}/wdi_ppp.csv", index=False)
