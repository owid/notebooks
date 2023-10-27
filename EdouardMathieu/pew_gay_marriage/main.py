import datetime

import pandas as pd

from owid import catalog

URL = "https://www.pewresearch.org/religion/fact-sheet/gay-marriage-around-the-world/"
MAPPING = "country_mapping.csv"


def scrape_data(url: str) -> pd.DataFrame:
    df = pd.read_html(url)[0]
    df = df[["Country", "Year"]].rename(columns={"Country": "country", "Year": "year"})
    return df


def rename_countries(df: pd.DataFrame) -> pd.DataFrame:
    mapping = pd.read_csv(MAPPING)

    # Check that we have a 1:1 mapping
    missing = set(df.country.unique()) - set(mapping.source.unique())
    if missing:
        raise ValueError(
            f"Missing countries in mapping: {missing}. Please update {MAPPING}."
        )

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
    # Load population data from catalog
    pop = (
        catalog.find(dataset="key_indicators", table="population")
        .iloc[0]
        .load()
        .reset_index()
        .drop(columns="world_pop_share")
    )

    # Get world population data
    world_pop = pop[pop.country == "World"]

    # Merge population data with input DataFrame
    df = df.merge(pop, on=["country", "year"], validate="1:1")

    # Group by year and calculate metrics
    df = (
        df.groupby("year", as_index=False)
        .agg({"country": "count", "population": "sum"})
        .rename(columns={"country": "number_of_countries"})
        .assign(entity="World")[["entity", "year", "number_of_countries", "population"]]
    )

    # Merge with world population data and calculate population without rights
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
        .pipe(rename_countries)
        .pipe(explode_country_years)
        .pipe(calculate_metrics)
        .to_csv(
            "Same-sex marriage around the world - Pew Research Center.csv", index=False
        )
    )


if __name__ == "__main__":
    main()
