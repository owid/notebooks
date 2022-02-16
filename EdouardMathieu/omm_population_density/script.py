import pandas as pd

from owid import site


def main():

    # Land area is fetched dynamically from the variable currently used an the input of our main
    # land area chart: https://ourworldindata.org/grapher/land-area-km
    land_area = (
        site.get_chart_data(slug="land-area-km")
        .rename(columns={"value": "land_area"})
        .groupby("entity", as_index=False)
        .head(1)
        .drop(columns=["year", "variable"])
    )

    # Population is fetched dynamically from the variable currently used an the input of our main
    # population chart: https://ourworldindata.org/grapher/population-past-future
    population = (
        site.get_chart_data(slug="population-past-future")
        .rename(columns={"value": "population"})
        .drop(columns=["variable"])
    )

    df = pd.merge(land_area, population, on="entity", validate="one_to_many")
    df["population_density"] = (df.population / df.land_area).round(3)
    df = df.drop(columns=["population", "land_area"]).sort_values(["entity", "year"])

    df.to_csv("Population density (World Bank, Gapminder, HYDE & UN).csv", index=False)


if __name__ == "__main__":
    main()
