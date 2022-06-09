import datetime
import pdb

import pandas as pd

from owid.datautils.geo import harmonize_countries

COUNTRY_MAPPING = "input/countries_standardized.json"

# https://aerospace.csis.org/data/international-astronaut-database/
# Scroll down to table > click on CSV button
ASTRONAUTS_FILE = "input/International Astronaut Database.csv"

NASA_BUDGET_SPREADSHEET = "https://sheets.googleapis.com/v4/spreadsheets/1TNgeonCjrQQKIc8keK4pGSHaZ70bH620RuCCwKW0V80/values/A1:ZZ/?alt=json&majorDimension=COLUMNS&valueRenderOption=UNFORMATTED_VALUE&dateTimeRenderOption=FORMATTED_STRING&key=AIzaSyCMZ7e8ujOnA5hVanuXSFOP5bJf9b6jBgg"
LEO_COSTS_SPREADSHEET = "https://sheets.googleapis.com/v4/spreadsheets/1FGdaphIbRjDpXsOdU3omWGRpH5DTImmzWW-H43lLOms/values/A1:ZZ/?alt=json&majorDimension=COLUMNS&valueRenderOption=UNFORMATTED_VALUE&dateTimeRenderOption=FORMATTED_STRING&key=AIzaSyCMZ7e8ujOnA5hVanuXSFOP5bJf9b6jBgg"


def download_data(url):
    data = pd.read_json(url)["values"]
    cols = [lst[0] for lst in data]
    values = [lst[1:] for lst in data]
    df = pd.DataFrame(values).T
    df.columns = cols
    return df


def import_astronauts():
    astronauts = pd.read_csv(ASTRONAUTS_FILE)

    # Extract years from list of flights
    years = (
        astronauts.Flights.str.extractall(r"(\d{4})")
        .rename(columns={0: "Year"})
        .droplevel(1)
    )
    years["Year"] = years.Year.astype(int)
    years = years[years.Year < datetime.date.today().year]
    df = pd.merge(astronauts, years, left_index=True, right_index=True)[
        ["Name", "Country", "Year"]
    ]

    # Harmonize countries
    df = df.pipe(
        harmonize_countries,
        countries_file=COUNTRY_MAPPING,
        country_col="Country",
        warn_on_missing_countries=True,
        warn_on_unused_countries=True,
        show_full_warning=True,
    )

    # Derive cumulative individuals (i.e. count only first flights)
    people = df.groupby(["Name", "Country"], as_index=False).min()
    people_world = (
        people.groupby("Year", as_index=False)
        .size()
        .rename(columns={"size": "annual_individuals"})
        .assign(Country="World")
    )
    people = (
        people.groupby(["Country", "Year"], as_index=False)
        .size()
        .reset_index(drop=True)
        .rename(columns={"size": "annual_individuals"})
    )
    people = pd.concat([people, people_world], ignore_index=True)
    people = people.sort_values(["Country", "Year"])
    people["cumulative_individuals"] = people.groupby("Country")[
        "annual_individuals"
    ].cumsum()

    # Derive cumulative visits (i.e. count all flights)
    visits_world = (
        df.groupby("Year", as_index=False)
        .size()
        .rename(columns={"size": "annual_visits"})
        .assign(Country="World")
    )
    visits = (
        df.groupby(["Country", "Year"], as_index=False)
        .size()
        .reset_index(drop=True)
        .rename(columns={"size": "annual_visits"})
    )
    visits = pd.concat([visits, visits_world], ignore_index=True)
    visits = visits.sort_values(["Country", "Year"])
    visits["cumulative_visits"] = visits.groupby("Country")["annual_visits"].cumsum()

    df = (
        pd.merge(
            people,
            visits,
            on=["Country", "Year"],
            how="outer",
            validate="one_to_one",
        )
        .sort_values(["Country", "Year"])
        .drop(columns=["annual_individuals"])
    )

    return df


def import_leo_costs():
    df = download_data(LEO_COSTS_SPREADSHEET)
    df = df[
        ["Launch Vehicle", "First Successful Launch", "FY21", "Launch Class"]
    ].rename(
        columns={
            "Launch Vehicle": "entity",
            "First Successful Launch": "year",
            "FY21": "cost_per_kg",
            "Launch Class": "launch_class",
        }
    )
    df = df[df.entity != ""]
    return df


def import_nasa_budget():
    df = download_data(NASA_BUDGET_SPREADSHEET)
    df["Value"] = df.Value.mul(1000000)  # Convert back to millions
    df = (
        df[df.Type == "FY20 Dollars"][["Year", "Value"]]
        .groupby("Year", as_index=False)
        .sum()
        .rename(columns={"Value": "Budget"})
        .assign(Country="United States")
    )
    return df[["Country", "Year", "Budget"]]


def main():
    import_astronauts().to_csv(
        "output/CSIS - Astronauts launched by year.csv", index=False
    )
    import_leo_costs().to_csv("output/CSIS - Cost of space launches.csv", index=False)
    import_nasa_budget().to_csv("output/CSIS - NASA budget history.csv", index=False)


if __name__ == "__main__":
    main()
