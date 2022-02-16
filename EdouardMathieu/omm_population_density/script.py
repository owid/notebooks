import requests

from bs4 import BeautifulSoup
import pandas as pd


def get_var_from_chart(chart_slug: str, var_name: str) -> pd.DataFrame:
    url = f"https://ourworldindata.org/grapher/{chart_slug}"
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    for link in soup.find_all("link"):
        if link.get("rel") == ["preload"]:
            json_url = f"https://ourworldindata.org/{link.get('href')}"
    response = requests.get(json_url).json()

    data = list(response["variables"].values())[0]
    data = pd.DataFrame(
        {
            "year": data["years"],
            "entity_id": data["entities"],
            var_name: data["values"],
        }
    )

    entities = (
        pd.DataFrame.from_dict(response["entityKey"], orient="index")
        .reset_index()
        .rename(columns={"index": "entity_id"})
    )
    entities["entity_id"] = entities["entity_id"].astype(int)

    df = (
        pd.merge(data, entities, on="entity_id", validate="many_to_one")
        .drop(columns=["entity_id", "code"])
        .rename(columns={"name": "entity"})
    )
    return df


def main():

    # Land area is fetched dynamically from the variable currently used an the input of our main
    # land area chart: https://ourworldindata.org/grapher/land-area-km
    land_area = (
        get_var_from_chart(chart_slug="land-area-km", var_name="land_area")
        .groupby("entity", as_index=False)
        .head(1)
        .drop(columns="year")
    )

    # Population is fetched dynamically from the variable currently used an the input of our main
    # population chart: https://ourworldindata.org/grapher/population-past-future
    population = get_var_from_chart(
        chart_slug="population-past-future", var_name="population"
    )

    df = pd.merge(land_area, population, on="entity", validate="one_to_many")
    df["population_density"] = (df.population / df.land_area).round(3)
    df = df.drop(columns=["population", "land_area"]).sort_values(["entity", "year"])

    df.to_csv("Population density (World Bank, Gapminder, HYDE & UN).csv", index=False)


if __name__ == "__main__":
    main()
