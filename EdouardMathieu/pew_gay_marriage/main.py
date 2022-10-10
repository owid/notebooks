import datetime
import requests

import pandas as pd
from bs4 import BeautifulSoup

from owid import catalog

URL = "https://www.pewresearch.org/religion/fact-sheet/gay-marriage-around-the-world/"
MAPPING = "country_mapping.csv"


def scrape_data(url: str) -> pd.DataFrame:
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    country_list = soup.select("[data-title='Alphabetical list of countries']")[
        0
    ].find_all("li")
    return pd.DataFrame({"country": [c.text for c in country_list]})


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df["year"] = df.country.str.extract("\((\d{4})\)").astype(int)
    df["country"] = df.country.str.replace(" \(\d{4}\)", "", regex=True)
    return df


def add_manual_points(df: pd.DataFrame) -> pd.DataFrame:
    """
    Sometimes the source is not perfectly up to date yet. In this case, we add the latest data
    points manually here.
    """
    manual = pd.DataFrame(
        {"country": ["Chile", "Slovenia", "Switzerland"], "year": [2022, 2022, 2022]}
    )

    common = set(manual.country).intersection(set(df.country))
    if len(common) > 0:
        raise Exception(
            f"The following countries are included both by the source and added manually: {common}"
        )

    return pd.concat([df, manual]).drop_duplicates()


def rename_countries(df: pd.DataFrame) -> pd.DataFrame:
    mapping = pd.read_csv(MAPPING)
    df = (
        df.merge(mapping, left_on="country", right_on="source", validate="1:1")
        .drop(columns=["country", "source"])
        .rename(columns={"owid": "country"})
        .groupby("country", as_index=False)
        .max()
    )
    return df


def explode_country_years(df: pd.DataFrame) -> pd.DataFrame:
    """
    Given that we need to calculate a running total of the world's population that has the access
    to same-sex marriage, we need to create a dataframe that, for each country, has a row for each
    year where same-sex marriage has been legal.

    e.g. it became legal in Australia in 2017, so we need:

    Australia 2017
    Australia 2018
    …
    Australia current_year
    """

    def _explode(row, current_year):
        return pd.DataFrame(
            {"country": row.country, "year": range(row.year, current_year + 1)}
        )

    return pd.concat(
        [
            *df.apply(
                _explode,
                current_year=datetime.date.today().year,
                axis=1,
            )
        ]
    )


def calculate_metrics(df: pd.DataFrame) -> pd.DataFrame:
    pop = (
        catalog.find(dataset="key_indicators", table="population")
        .iloc[0]
        .load()
        .reset_index()
        .drop(columns="world_pop_share")
    )
    world_pop = pop[pop.country == "World"]
    df = df.merge(pop, on=["country", "year"], validate="1:1")

    df = (
        df.groupby("year", as_index=False)
        .agg({"country": "count", "population": "sum"})
        .rename(columns={"country": "number_of_countries"})
        .assign(entity="World")[["entity", "year", "number_of_countries", "population"]]
    )

    df = df.merge(
        world_pop,
        left_on=["entity", "year"],
        right_on=["country", "year"],
        validate="1:1",
    )
    df["population_without_rights"] = df.population_y - df.population_x
    df = df.rename(columns={"population_x": "population_with_rights"}).drop(
        columns=["population_y", "country"]
    )

    return df


def main():
    (
        scrape_data(URL)
        .pipe(clean_data)
        .pipe(rename_countries)
        .pipe(add_manual_points)
        .pipe(explode_country_years)
        .pipe(calculate_metrics)
        .to_csv(
            "Same-sex marriage around the world - Pew Research Center.csv", index=False
        )
    )


if __name__ == "__main__":
    main()
