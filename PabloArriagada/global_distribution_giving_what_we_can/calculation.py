"""
LAST UPDATED: October 2025

SCRIPT TO CALCULATE GLOBAL DISTRIBUTION OF GIVING WHAT WE CAN
This script calculates the global distribution of Giving What We Can, using the World Bank PIP data, together with CPI and PPP conversion factors from the World Development Indicators.
The script exports the results to a csv file.

The script requires the following files:
    - A global distribution of income, created by Our World in Data using the World Bank PIP API.
    - PPP conversion factors from the World Development Indicators.
    - CPI data from the World Development Indicators.

Follow these steps to run the script:
    1. Update PIP_VERSION with the latest version of the PIP data, available at Our World in Data (it's the version of the garden step).
    2. Download the PPP conversion factors from https://api.worldbank.org/v2/en/indicator/PA.NUS.PRVT.PP?downloadformat=csv
    3. Download the CPI data from https://api.worldbank.org/v2/en/indicator/FP.CPI.TOTL?downloadformat=csv
    4. Extract the data files to the same directory as this script.
    5. Modify the file paths (PPP_FILE_PATH and CPI_FILE_PATH) if necessary, to coincide with the names of these new files.
    6. Update MAX_YEAR_CPI with the latest year for which CPI data is available, if necessary.
    7. Run this script.
"""

from pathlib import Path

import pandas as pd

PARENT_DIR = Path(__file__).parent.absolute()

# Define OWID version of PIP data
PIP_VERSION = "2025-10-09"

# Define PIP percentiles URL
PIP_URL = f"http://catalog.ourworldindata.org/garden/wb/{PIP_VERSION}/world_bank_pip/world_bank_pip_percentiles.feather"

# Define paths for the PPP and CPI data
PPP_FILE_PATH = f"{PARENT_DIR}/API_PA.NUS.PRVT.PP_DS2_en_csv_v2_5762.csv"
CPI_FILE_PATH = f"{PARENT_DIR}/API_FP.CPI.TOTL_DS2_en_csv_v2_129887.csv"

# Define maximum year for CPI
MAX_YEAR_CPI = 2024

# Define PPP year
PPP_YEAR = 2021


def run() -> None:
    # Load data
    df_percentiles = pd.read_feather(PIP_URL)
    df_ppp_factors = pd.read_csv(PPP_FILE_PATH, skiprows=4)
    df_cpi = pd.read_csv(CPI_FILE_PATH, skiprows=4)

    # In df_percentiles, select ppp_version == PPP_YEAR
    df_percentiles = df_percentiles[
        df_percentiles["ppp_version"] == PPP_YEAR
    ].reset_index(drop=True)

    process_percentiles_and_export(df_percentiles)
    combine_ppp_cpi_and_export(df_ppp_factors, df_cpi)


def process_percentiles_and_export(df_percentiles: pd.DataFrame) -> None:
    """
    Process the percentiles dataframe to calculate the global distribution of Giving What We Can.
    """
    # Filter data to only include country=World and year MAX_YEAR_CPI
    df_percentiles = df_percentiles[
        (df_percentiles["country"] == "World")
        & (df_percentiles["year"] == MAX_YEAR_CPI)
    ].reset_index(drop=True)

    # Compare thr values with the one in the previous row
    df_percentiles["thr_previous"] = (
        df_percentiles["thr"].groupby(df_percentiles["year"]).shift(1)
    )
    df_percentiles["thr_check"] = (
        df_percentiles["thr"] >= df_percentiles["thr_previous"]
    )

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


def combine_ppp_cpi_and_export(
    df_ppp_factors: pd.DataFrame, df_cpi: pd.DataFrame
) -> None:
    """
    Combine the PPP and CPI dataframes and export the result.
    """
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

    # Select in df_ppp_factors only the columns of interest (Country Name, Country Code, PPP_YEAR)
    df_ppp_factors = df_ppp_factors[["Country Name", "Country Code", str(PPP_YEAR)]]
    df_ppp_factors = df_ppp_factors.rename(
        columns={
            "Country Name": "country",
            "Country Code": "country_code",
            str(PPP_YEAR): f"ppp_{PPP_YEAR}",
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

    # Assert if I filter by MAX_YEAR_CPI I will get a non-empty dataframe
    mask = df_cpi["year"] == MAX_YEAR_CPI
    assert not df_cpi[mask].empty, f"No CPI data for {MAX_YEAR_CPI}"

    # Assert if I filter by MAX_YEAR_CPI I will get a cpi column full of nan
    assert (
        not df_cpi[mask]["cpi"].isna().all()
    ), f"CPI column is full of empty values for {MAX_YEAR_CPI}"

    # Filter for PPP_YEAR and the maximum year
    df_cpi = df_cpi[
        (df_cpi["year"] == PPP_YEAR) | (df_cpi["year"] == MAX_YEAR_CPI)
    ].reset_index(drop=True)

    # Make table wide, by naming the columns cpi_PPP_YEAR and cpi_max
    df_cpi = df_cpi.pivot(
        index="country_code", columns="year", values="cpi"
    ).reset_index()

    # Rename columns
    df_cpi = df_cpi.rename(
        columns={PPP_YEAR: f"cpi_{PPP_YEAR}", MAX_YEAR_CPI: f"cpi_{MAX_YEAR_CPI}"}
    )

    # Calculate the inflation rate between PPP_YEAR and the maximum year
    df_cpi["inflation_rate"] = df_cpi[f"cpi_{MAX_YEAR_CPI}"] / df_cpi[f"cpi_{PPP_YEAR}"]

    # Merge df_ppp_factors and df_cpi
    df_ppp = pd.merge(
        df_ppp_factors,
        df_cpi[
            ["country_code", f"cpi_{PPP_YEAR}", f"cpi_{MAX_YEAR_CPI}", "inflation_rate"]
        ],
        on="country_code",
        how="left",
    )

    # Calculate the ppp conversion factor for the most recent year
    df_ppp["ppp_factor"] = df_ppp[f"ppp_{PPP_YEAR}"] * df_ppp["inflation_rate"]

    # Remove empty values of pa_nus_prvt_pp
    df_ppp = df_ppp[~df_ppp["ppp_factor"].isna()].reset_index(drop=True)

    # Sort by country
    df_ppp = df_ppp.sort_values(by=["country"]).reset_index(drop=True)

    # Export to csv
    df_ppp.to_csv(f"{PARENT_DIR}/wdi_ppp.csv", index=False)


if __name__ == "__main__":
    run()
