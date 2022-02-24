import pandas as pd

from owid import site

COW_INPUT = "input/NMC_Documentation 6.0/NMC-60-abridged/NMC-60-abridged.csv"
COW_MAPPING = "config/cow_country_standardized.csv"

SIPRI_INPUT = "input/SIPRI-Milex-data-1949-2020_0.xlsx"
SIPRI_MAPPING = "config/sipri_country_standardized.csv"

USD_CPINDEX = "input/USCPI_1800-9999.csv"
USD_GBP_RATES = "input/EXCHANGEPOUND_1800-1913.csv"

CONTINENTS = site.get_chart_data(slug="continents-according-to-our-world-in-data")
NATO_COUNTRIES = "config/nato_member_states.csv"

POPULATION = site.get_chart_data(slug="population")


def import_cow(min_year=None, max_year=None) -> pd.DataFrame:
    """
    Downloaded from https://correlatesofwar.org/data-sets/national-material-capabilities
    NMC v6
    A zip file containing the data and documents for NMC version 6.
    application/zip NMC_Documentation 6.0.zip — 9372 KB
    """

    df = pd.read_csv(
        COW_INPUT, usecols=["stateabb", "year", "milex"], na_values=-9
    ).rename(columns={"milex": "military_expenditure"})

    # Expenditure is originally expressed in thousands of GBP or USD
    df["military_expenditure"] = df.military_expenditure * 1000

    # Filter years
    if min_year:
        df = df[df.year >= min_year]
    if max_year:
        df = df[df.year <= max_year]

    # Country mapping
    mapping = pd.read_csv(COW_MAPPING)
    df = (
        pd.merge(mapping, df, on="stateabb", validate="one_to_many")
        .rename(columns={"owid_name": "country"})
        .drop(columns=["cow_name", "stateabb"])
    )

    return df


def convert_gbp_to_usd(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts current GBP to current USD
    Exchange rate data downloaded from https://www.measuringworth.com/datasets/exchangepound/
    Initial Year: 1800
    Ending Year: 1913
    -> "Download the Results in a Spreadsheet Format"
    """

    exchange = pd.read_csv(USD_GBP_RATES, skiprows=2, usecols=["Year", "Rate"]).rename(
        columns={"Year": "year"}
    )
    df = df.merge(exchange, on="year", validate="many_to_one", how="left")
    df["military_expenditure"] = df.military_expenditure * df.Rate
    df = df.drop(columns="Rate")
    return df


def import_sipri_absolute() -> pd.DataFrame:
    """
    Downloaded from https://www.sipri.org/databases/milex
    -> "Data for all countries 1949–2020 (excel spreadsheet)"
    """

    df = pd.read_excel(
        SIPRI_INPUT, sheet_name="Current USD", skiprows=5, na_values=["xxx", ". ."]
    ).drop(columns="Notes")

    # Find end of table
    last_idx = df.index[df.Country.isna()].min()
    df = df.iloc[:last_idx]

    # Reshape table
    df = df.melt(id_vars="Country", var_name="year", value_name="military_expenditure")
    df["year"] = df.year.astype(int)

    # Expenditure is originally expressed in millions of USD
    df["military_expenditure"] = df.military_expenditure * 1000000

    # Country mapping
    mapping = pd.read_csv(SIPRI_MAPPING).dropna(subset=["Our World In Data Name"])
    df = (
        pd.merge(mapping, df, on="Country", validate="one_to_many")
        .rename(columns={"Our World In Data Name": "country"})
        .drop(columns=["Country"])
    )

    return df


def select_source(df: pd.DataFrame) -> pd.DataFrame:
    """
    Select one source per country-year, giving priority to:
    1. Correlates of War
    2. SIPRI
    """

    return (
        df.dropna(subset=["military_expenditure"])
        .sort_values(["country", "year", "source_rank"])
        .groupby(["country", "year"], as_index=False)
        .head(1)
        .drop(columns="source_rank")
    )


def adjust_for_inflation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts all values to constant 2020 US dollars
    Consumer price index data downloaded from https://www.measuringworth.com/datasets/uscpi/
    Initial Year: 1800
    Ending Year: 9999
    -> "Download the Results in a Spreadsheet Format"
    """

    cpi = pd.read_csv(USD_CPINDEX, skiprows=3).rename(
        columns={"Year": "year", "U.S. Consumer Price Index *": "cpi"}
    )
    cpi_2020 = cpi.loc[cpi.year == 2020, "cpi"].values[0]
    df = df.merge(cpi, on="year", validate="many_to_one", how="left")
    df["military_expenditure"] = (df.military_expenditure * cpi_2020 / df.cpi).round(0)
    df = df.drop(columns="cpi")
    return df


def build_aggregates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate our own totals according to OWID continent definitions.
    """
    df = df[
        -df.country.isin(
            [
                "North America",
                "South America",
                "Europe",
                "Africa",
                "Asia",
                "Oceania",
                "World",
            ]
        )
    ]

    mapping = CONTINENTS[["entity", "value"]].rename(
        columns={"entity": "country", "value": "continent"}
    )

    continents = (
        df.merge(mapping, on="country", how="inner", validate="many_to_one")
        .groupby(["continent", "year"], as_index=False)
        .sum()
        .rename(columns={"continent": "country"})
    )

    nato_members = pd.read_csv(NATO_COUNTRIES)
    nato = (
        df[df.country.isin(nato_members.country)][["year", "military_expenditure"]]
        .groupby("year")
        .sum()
        .reset_index()
        .assign(country="NATO member states")
    )

    world = (
        df[["year", "military_expenditure"]]
        .groupby("year")
        .sum()
        .reset_index()
        .assign(country="World")
    )

    return pd.concat([df, continents, nato, world], ignore_index=True)


def add_per_capita(df: pd.DataFrame) -> pd.DataFrame:
    """
    Derive per-capita military expenditure based on our long-run population dataset
    """

    population = POPULATION[["entity", "value", "year"]].rename(
        columns={"entity": "country", "value": "population"}
    )
    df = df.merge(
        population, how="left", on=["country", "year"], validate="many_to_one"
    )
    df["military_expenditure_per_capita"] = (
        df.military_expenditure / df.population
    ).round(2)
    df = df.drop(columns="population")

    return df


def add_share_gdp(df: pd.DataFrame) -> pd.DataFrame:
    """
    In the long run we should replace this precalculated data by a proper combination of the
    absolute expenditure data from CoW & SIPRI, divided by our long-run GDP data from Maddison.
    But these two series use different units (2020 USD vs. 2011 int$) so for now we use the data
    on expenditure as % of GDP as directly reported by SIPRI.
    """

    gdp = pd.read_excel(
        SIPRI_INPUT, sheet_name="Share of GDP", skiprows=5, na_values=["xxx", ". ."]
    ).drop(columns="Notes")

    # Find end of table
    last_idx = gdp.index[gdp.Country.isna()].min()
    gdp = gdp.iloc[:last_idx]

    # Reshape table
    gdp = gdp.melt(
        id_vars="Country", var_name="year", value_name="military_expenditure_share_gdp"
    ).dropna(subset=["military_expenditure_share_gdp"])
    gdp["year"] = gdp.year.astype(int)

    # Expenditure is originally expressed in percentage
    gdp["military_expenditure_share_gdp"] = (
        gdp.military_expenditure_share_gdp * 100
    ).round(2)

    # Country mapping
    mapping = pd.read_csv(SIPRI_MAPPING).dropna(subset=["Our World In Data Name"])
    gdp = (
        pd.merge(mapping, gdp, on="Country", validate="one_to_many")
        .rename(columns={"Our World In Data Name": "country"})
        .drop(columns=["Country"])
    )

    # Merge with expenditure
    df = df.merge(gdp, on=["country", "year"], how="outer", validate="one_to_one")

    return df


def main():

    cow_pre1914 = (
        import_cow(max_year=1913).pipe(convert_gbp_to_usd).assign(source_rank=1)
    )
    cow_post1914 = import_cow(min_year=1914).assign(source_rank=1)
    sipri = import_sipri_absolute().assign(source_rank=2)

    df = (
        pd.concat([cow_pre1914, cow_post1914, sipri])
        .pipe(select_source)
        .pipe(adjust_for_inflation)
        .pipe(build_aggregates)
        .pipe(add_per_capita)
        .pipe(add_share_gdp)
    )

    df.to_csv(
        "output/Military expenditure - OWID based on CoW & SIPRI.csv", index=False
    )


if __name__ == "__main__":
    main()
