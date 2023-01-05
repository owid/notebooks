import pandas as pd


def main():

    df = pd.read_csv("https://www.gw-openscience.org/eventapi/csv/GWTC/")

    df = df.groupby("commonName", as_index=False).GPS.min()

    df["time"] = pd.to_datetime(df["GPS"], unit="s", origin="1980-01-06", utc=True)
    df["year"] = df["time"].dt.year

    df = df.groupby("year").size().reset_index(name="N")

    df["cumulative_gwt"] = df["N"].cumsum()

    df["entity"] = "World"

    df = df[["entity", "year", "cumulative_gwt"]]

    df.to_csv("Gravitational wave transients (GWOSC).csv", index=False)


if __name__ == "__main__":
    main()
