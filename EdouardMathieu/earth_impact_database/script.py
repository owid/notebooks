import datetime
import requests

from bs4 import BeautifulSoup
import pandas as pd

DOMAIN = "http://www.passc.net/EarthImpactDatabase/New%20website_05-2018"


def get_impact(row):
    url = f'{DOMAIN}/{row.find_all("td")[0].find("a")["href"]}'
    print(url)
    df = pd.read_html(url)[0]
    return df[["Crater Name", "Location", "Diameter (km)", "Age (Ma)"]]


def clean_names(series):
    return series.replace(
        {
            "South Australia": "Australia",
            "Queensland": "Australia",
            "Western Australia": "Australia",
            "U.S.A.": "United States",
        }
    )


def main():
    soup = BeautifulSoup(
        requests.get(f"{DOMAIN}/Diametersort.html").content, "html.parser"
    )
    top20 = soup.find("table").find_all("tr")[-20:]
    results = [get_impact(row) for row in top20]

    df = pd.concat(results).rename(columns={"Diameter (km)": "crater_diameter"})

    df["Location"] = df.Location.str.replace(".*, ", "", regex=True).pipe(clean_names)
    df["entity"] = df["Crater Name"] + " (" + df.Location + ")"
    df["year"] = (
        df["Age (Ma)"].str.extract(r"([\d\.]+)").astype(float).mul(-1000000).astype(int)
    )

    df = df[["entity", "year", "crater_diameter"]]
    df.to_csv(
        "output/Earth Impact Database - Top 20 craters by diameter.csv", index=False
    )


if __name__ == "__main__":
    main()
