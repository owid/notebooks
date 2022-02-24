import requests

import pandas as pd

SOURCE = "https://thebulletin.org/third-party/nuclear-notebook/data/nn_data.json"


def main():
    data = requests.get(SOURCE).json()
    df = (
        pd.DataFrame.from_records(data)
        .melt(
            id_vars="year",
            var_name="Entity",
            value_name="Nuclear weapons inventory by country (FAS Nuclear Notebook)",
        )
        .rename(columns={"year": "Year"})
        .replace(
            {
                "USA": "United States",
                "UK": "United Kingdom",
                "NorthKorea": "North Korea",
            }
        )
    )
    df = df[
        [
            "Entity",
            "Year",
            "Nuclear weapons inventory by country (FAS Nuclear Notebook)",
        ]
    ]
    df.to_csv(
        "Nuclear weapons inventory by country - FAS Nuclear Notebook.csv", index=False
    )


if __name__ == "__main__":
    main()
