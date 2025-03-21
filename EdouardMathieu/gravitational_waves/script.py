import pandas as pd


def main():
    df = pd.read_csv("https://www.gw-openscience.org/eventapi/csv/GWTC/")

    # Only keep events considered "confident", i.e. with "confident" in their catalog.shortName
    df = df[df["catalog.shortName"].str.contains("confident")]

    # In case events are recorded multiple times
    # we keep only the earliest GPS time for each commonName
    df = df.groupby("commonName", as_index=False).GPS.min()

    # Origin for GPS time is on 1980-01-06
    df["time"] = pd.to_datetime(df["GPS"], unit="s", origin="1980-01-06", utc=True)

    # Count events by year, and calculate the cumsum
    df["year"] = df["time"].dt.year
    df = df.groupby("year").size().reset_index(name="N")
    df["cumulative_gwt"] = df["N"].cumsum()

    # Add entity and select columns
    df = df.assign(entity="World")[["entity", "year", "cumulative_gwt"]]

    df.to_csv("Gravitational wave transients (GWOSC).csv", index=False)


if __name__ == "__main__":
    main()
