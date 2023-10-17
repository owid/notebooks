"""
If the file doesn't execute correctly, try
pip install requirements.txt
"""
from pathlib import Path

import pandas as pd
from structlog import get_logger

# Initialize logger.
log = get_logger()

PARENT_DIR = Path(__file__).parent.absolute()

df = pd.read_feather(f"{PARENT_DIR}/tb.feather")
df_percentiles = pd.read_feather(f"{PARENT_DIR}/tb_percentiles.feather")

##############################################
# FUNCTION SETTINGS

series_type = "series_code"  # series_name or series_code

# `series` depends on series_type: if series_type is series_name, series is a list of series names, e.g. ["WID Gini", "PIP Top 1% share"]; if series_type is series_code, series is a list of series codes, e.g. ["gini_wid_pretaxNational_perAdult", "p99p100Share_pip_disposable_perCapita"]
series = [
    "gini_wid_pretaxNational_perAdult",
    "gini_lis_market_perCapita",
    "gini_pip_disposable_perCapita",
]

# reference_years is the list of years to match the series to. Each year is a dictionary with the year as key and a dictionary of parameters as value. The parameters are:
# - maximum_distance: the maximum distance between the series and the reference year
# - tie_break_strategy: the strategy to use to break ties when there are multiple series that match the reference year. The options are "lower" (select the series with the lowest distance to the reference year) or "higher" (select the series with the highest distance to the reference year)
# - min_interval: the minimum distance between reference years. The value of min_interval for the last reference year is ignored.
reference_years = {
    # 1980: {"maximum_distance": 0, "tie_break_strategy": "lower", "min_interval": 5},
    1990: {"maximum_distance": 3, "tie_break_strategy": "higher", "min_interval": 7},
    2000: {"maximum_distance": 0, "tie_break_strategy": "higher", "min_interval": 8},
    2010: {"maximum_distance": 3, "tie_break_strategy": "lower", "min_interval": 5},
    2018: {"maximum_distance": 5, "tie_break_strategy": "higher", "min_interval": 2},
}

# In case of PIP series, we need to define three parameters:
# - constant_reporting_level: if True (no quotes), the series will be matched only to series with pipreportinglevel = "national". If False, series with pipreportinglevel = "urban" or "rural" will also be matched.
# - constant_welfare_type: if True (no quotes), the series will be matched only to series with the pipwelfare defined in the income_or_consumpion parameter. If False, income or consumption can be selected.
# - income_or_consumption: if constant_welfare_type is False, this parameter defines whether to match the series to income or consumption data. The options are "income" or "consumption".
constant_reporting_level = True
constant_welfare_type = False
income_or_consumption = "income"

##############################################


def match_ref_years(
    df: pd.DataFrame,
    series_type: str,
    series: list,
    reference_years: dict,
    pip_strategy=dict,
) -> pd.DataFrame:
    """
    Match series to reference years.
    """

    # Assert if the series belong to the df
    assert set(series).issubset(set(df[series_type])), log.error(
        f"The series {set(series) - set(df[series_type])} is not in the dataset."
    )
    df_match = pd.DataFrame()
    df_series = df[df[series_type].isin(series)].reset_index(drop=True)

    reference_years_list = []
    for y in reference_years:
        # keep reference year in a list
        reference_years_list.append(y)
        # Filter df_series according to reference year and maximum distance from it
        df_year = df_series[
            (df_series["year"] <= y + reference_years[y]["maximum_distance"])
            & (df_series["year"] >= y - reference_years[y]["maximum_distance"])
        ].reset_index(drop=True)

        assert not df_year.empty, log.error(
            f"No data found for reference year {y}. Please check `maximum_distance` ({reference_years[y]['maximum_distance']})."
        )

        df_year["distance"] = abs(df_year["year"] - y)

        # If source is PIP, filter df_year according to constant_reporting_level and constant_welfare_type
        # Filter df_year according to constant_reporting_level, constant_welfare_type and income_or_consumption

        # Check if constant_reporting_level and constant_welfare_type are boolean
        assert isinstance(constant_reporting_level, bool), log.error(
            "`constant_reporting_level` must be boolean: True or False (without quotes)."
        )
        assert isinstance(constant_welfare_type, bool), log.error(
            "`constant_welfare_type` must be boolean: True or False (without quotes)."
        )
        # Check if income_or_consumption is income or consumption
        assert income_or_consumption in ["income", "consumption"], log.error(
            "`income_or_consumption` must be either 'income' or 'consumption'."
        )
        if constant_reporting_level:
            df_year = df_year[
                (df_year["pipreportinglevel"] == "national")
                | (df_year["pipreportinglevel"].isnull())
            ].reset_index(drop=True)
        if constant_welfare_type:
            df_year = df_year[
                (df_year["pipwelfare"] == income_or_consumption)
                | (df_year["pipwelfare"].isnull())
            ].reset_index(drop=True)

        # Merge the different reference years into a single dataframe
        if df_match.empty:
            df_match = df_year
        else:
            df_match = pd.merge(
                df_match,
                df_year,
                how="outer",
                on=["country", "series_code"],
                suffixes=("", f"_{y}"),
            )
            if len(reference_years_list) == 2:
                df_match[f"distance_{reference_years_list[-2]}_{y}"] = abs(
                    df_match["year"] - df_match[f"year_{y}"]
                )
            else:
                df_match[f"distance_{reference_years_list[-2]}_{y}"] = abs(
                    df_match[f"year_{reference_years_list[-2]}"] - df_match[f"year_{y}"]
                )
            # Filter df_match according to min_interval
            df_match = df_match[
                df_match[f"distance_{reference_years_list[-2]}_{y}"]
                >= reference_years[reference_years_list[-2]]["min_interval"]
            ].reset_index(drop=True)

            assert not df_match.empty, log.error(
                f"No matching data found for reference years {reference_years_list[-2]} and {y}. Please check `min_interval` ({reference_years[reference_years_list[-2]]['min_interval']})."
            )

    # Rename columns related to the first reference year
    df_match = df_match.rename(
        columns={
            "year": f"year_{reference_years_list[0]}",
            "distance": f"distance_{reference_years_list[0]}",
            "value": f"value_{reference_years_list[0]}",
        }
    )
    df_match.to_csv(f"{PARENT_DIR}/df_match_raw.csv", index=False)
    # Filter df_match according to tie_break_strategy
    for y in reference_years_list:
        if reference_years[y]["tie_break_strategy"] == "lower":
            # Remove duplicates and keep the row with the minimum distance
            df_match = df_match.sort_values(by=f"distance_{y}").drop_duplicates(
                subset=["country", "series_code"], keep="first"
            )
        elif reference_years[y]["tie_break_strategy"] == "higher":
            # Remove duplicates and keep the row with the maximum distance
            df_match = df_match.sort_values(by=f"distance_{y}").drop_duplicates(
                subset=["country", "series_code"], keep="last"
            )
        else:
            raise ValueError("tie_break_strategy must be either 'lower' or 'higher'")

        assert not df_match.empty, log.error(
            f"No matching data data found for reference year {y}. Please check `tie_break_strategy` ({reference_years[y]['tie_break_strategy']})."
        )

    # Create a list with the variables year_y and value_y for each reference year
    year_y_list = []
    value_y_list = []
    year_value_y_list = []
    for y in reference_years_list:
        year_y_list.append(f"year_{y}")
        value_y_list.append(f"value_{y}")
        year_value_y_list.append(f"year_{y}")
        year_value_y_list.append(f"value_{y}")

    # Make columns in year_y_list integer
    df_match[year_y_list] = df_match[year_y_list].astype(int)

    # Keep the columns I need
    df_match = df_match[
        ["country", "series_code", "indicator_name"] + year_value_y_list
    ].reset_index(drop=True)

    # Sort by country and year_y
    df_match = df_match.sort_values(
        by=["series_code", "country"] + year_y_list
    ).reset_index(drop=True)

    df_match.to_csv(f"{PARENT_DIR}/df_match.csv", index=False)

    return df_match


df_match = match_ref_years(df, series_type, series, reference_years)
