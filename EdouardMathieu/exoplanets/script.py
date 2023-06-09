import pandas as pd

import datetime

DATA_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+distinct+pl_name,disc_year,discoverymethod+from+ps&format=csv"


def main():
    df = pd.read_csv(DATA_URL)

    df = df[df.disc_year < datetime.date.today().year]

    # Clean discovery methods
    # Keep the 3 top discovery methods, and label the rest as "Other methods"
    top_methods = [*df.discoverymethod.value_counts().head(3).index]
    df.loc[-df.discoverymethod.isin(top_methods), "discoverymethod"] = "Other methods"
    # Capitalize the discovery methods
    df["discoverymethod"] = df.discoverymethod.str.capitalize()

    # Count discoveries by year and method
    df = df.groupby(["disc_year", "discoverymethod"], as_index=False).size()

    # Pivot then melt dataset to ensure all combinations of year & method are present
    df = (
        df.pivot(columns="discoverymethod", index="disc_year", values="size")
        .fillna(0)
        .reset_index()
        .melt(id_vars="disc_year", var_name="discoverymethod", value_name="N")
    )

    # Calculate cumulative exoplanets by method
    df = df.sort_values("disc_year")
    df["cumulative_exoplanets"] = df.groupby("discoverymethod").N.cumsum().astype(int)
    df = df.drop(columns="N")

    # Rename and reorder columns
    df = df.rename(columns={"discoverymethod": "entity", "disc_year": "year"})

    df.to_csv("output/NASA - Exoplanets.csv", index=False)


if __name__ == "__main__":
    main()
