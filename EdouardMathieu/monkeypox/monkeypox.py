import datetime
from functools import reduce

import pandas as pd

SOURCE_MONKEYPOX = (
    "https://raw.githubusercontent.com/globaldothealth/monkeypox/main/latest.csv"
)
SOURCE_COUNTRY_MAPPING = "country_mapping.csv"
SOURCE_POPULATION = "https://github.com/owid/covid-19-data/raw/master/scripts/input/un/population_latest.csv"
OUTPUT_FILE = "owid-monkeypox-data.csv"


def aggregate(df, pop, date_type, metric_name):
    assert date_type in ["confirmation", "death"]
    assert metric_name in ["cases", "deaths"]

    df = df.rename(columns={f"Date_{date_type}": "date"})
    df = df.loc[-df.date.isnull(), ["location", "date"]]
    df = df[df.date.str.match("\d{4}-\d{2}-\d{2}")]

    world = df.groupby(["date"], as_index=False).size().assign(location="World")
    df = df.groupby(["location", "date"], as_index=False).size()
    df = pd.concat([df, world]).rename(columns={"size": "n"})

    # Fill missing dates with 0 for all countries
    def get_loc_range(loc, df):
        dates = df.loc[df.location == loc, "date"]
        return pd.DataFrame(
            {
                "date": pd.date_range(
                    start=dates.min(), end=dates.max(), freq="D"
                ).astype(str),
                "location": loc,
            }
        )

    df_range = pd.concat([get_loc_range(loc, df) for loc in df.location.unique()])
    df = (
        pd.merge(
            df, df_range, on=["location", "date"], how="outer", validate="one_to_one"
        )
        .fillna(0)
        .sort_values(["location", "date"])
        .reset_index(drop=True)
    )

    # Add 7-day average
    df["rolling_avg"] = (
        df.groupby("location")["n"]
        .rolling(window=7, min_periods=7, center=False)
        .mean()
        .round(2)
        .reset_index(drop=True)
    )

    # Add cumulative version
    df["cumulative"] = df.groupby("location")["n"].cumsum()

    # Add per-capita metrics
    df = pd.merge(df, pop, how="left", validate="many_to_one", on="location")
    df = df.assign(
        n_pm=round(df.n * 1000000 / df.population, 3),
        cumulative_pm=round(df.cumulative * 1000000 / df.population, 3),
        rolling_avg_pm=round(df.rolling_avg * 1000000 / df.population, 3),
    ).drop(columns="population")

    df = df.rename(
        columns={
            "n": f"new_{metric_name}",
            "rolling_avg": f"new_{metric_name}_smoothed",
            "cumulative": f"total_{metric_name}",
            "n_pm": f"new_{metric_name}_per_million",
            "rolling_avg_pm": f"new_{metric_name}_smoothed_per_million",
            "cumulative_pm": f"total_{metric_name}_per_million",
        }
    )

    return df


def main():

    # Import all data from GitHub
    # The GitHub repo is updated after quality checks have run on the Google sheet
    # so sometimes data is delayed by a day (usually few hours) while the issues are fixed.
    # G.H recommends using the GitHub repo as that has passed QC checks.
    df = pd.read_csv(SOURCE_MONKEYPOX, low_memory=False)
    df = df.loc[
        (df.Date_confirmation >= "2022-05-06")
        & (df.Status == "confirmed")
        & (-df.Country.isnull()),
        ["Country", "Date_confirmation", "Date_death"],
    ].rename(columns={"Country": "location"})

    # Entity cleaning
    country_mapping = pd.read_csv(SOURCE_COUNTRY_MAPPING)
    df = pd.merge(
        df, country_mapping, on="location", how="left", validate="many_to_one"
    )
    missing_locations = set(df.location) - set(country_mapping.location)
    if len(missing_locations) > 0:
        raise Exception(
            f"Missing locations in country mapping file: {missing_locations}"
        )
    df = df.drop(columns="location").rename(columns={"new": "location"})[
        ["location", "Date_confirmation", "Date_death"]
    ]

    # Population data
    pop = pd.read_csv(SOURCE_POPULATION, usecols=["entity", "population"]).rename(
        columns={"entity": "location"}
    )
    missing_locations = set(df.location) - set(pop.location)
    if len(missing_locations) > 0:
        raise Exception(f"Missing locations in population file: {missing_locations}")

    dataframes = [
        aggregate(df, pop, date_type="confirmation", metric_name="cases"),
        aggregate(df, pop, date_type="death", metric_name="deaths"),
    ]

    df = reduce(
        lambda df1, df2: pd.merge(
            df1, df2, on=["location", "date"], how="outer", validate="one_to_one"
        ),
        dataframes,
    )
    df = df[df.date < str(datetime.date.today())].sort_values(["location", "date"])

    df.to_csv(OUTPUT_FILE, index=False)


if __name__ == "__main__":
    main()
