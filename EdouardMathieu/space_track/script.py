import datetime

import pandas as pd

# # Go to https://www.space-track.org and log in
# # Go to Query Builder
# # Use the following parameters: Class = gp, Order by = OBJECT_ID, Format = CSV
# # Click on BUILD QUERY then RUN QUERY to download the CSV
# # Move the CSV file to the script's folder

FILE = "https __www.space-track.org_basicspacedata_query_class_gp_orderby_object_id asc_format_csv_emptyresult_show.csv"


def define_orbits(df: pd.DataFrame) -> pd.DataFrame:
    df.loc[df.PERIAPSIS <= 2000, "ORBIT"] = "Low Earth orbit"
    df.loc[
        (df.PERIAPSIS >= 2000) & (df.PERIAPSIS <= 35586), "ORBIT"
    ] = "Medium Earth orbit"
    df.loc[
        (df.PERIAPSIS >= 35586) & (df.PERIAPSIS <= 35986), "ORBIT"
    ] = "Geostationary orbit"
    df.loc[df.PERIAPSIS >= 35986, "ORBIT"] = "High Earth orbit"
    return df


def create_year_cols(df: pd.DataFrame) -> pd.DataFrame:
    df["launch_year"] = pd.to_datetime(df.LAUNCH_DATE, format="%Y-%m-%d").dt.year
    df["decay_year"] = pd.to_datetime(df.DECAY_DATE, format="%Y-%m-%d").dt.year
    return df


def filter_years(df: pd.DataFrame) -> pd.DataFrame:
    # Remove events from current year
    df = df[df.launch_year < datetime.date.today().year]
    return df


def count_leo_by_type(df: pd.DataFrame) -> pd.DataFrame:
    # Objects in Lower Earth orbit over time, broken down by object type

    df = df[df.OBJECT_TYPE.isin(["PAYLOAD", "ROCKET BODY", "DEBRIS"])]
    df = df[df.ORBIT == "Low Earth orbit"]

    years = range(
        df.launch_year.min().astype(int), df.launch_year.max().astype(int) + 1
    )

    dataframes = []
    for year in years:
        # For each year, keep all launched objects up to that year & that haven't decayed yet
        df_year = df[
            (df.launch_year <= year) & (df.DECAY_DATE.isnull() | (df.decay_year > year))
        ]
        df_year = (
            df_year[["OBJECT_TYPE"]]
            .groupby("OBJECT_TYPE", as_index=False)
            .size()
            .assign(year=year)
        )
        dataframes.append(df_year)

    leo_by_type = (
        pd.concat(dataframes)
        .reset_index(drop=True)
        .rename(columns={"OBJECT_TYPE": "entity", "size": "objects"})
    )

    return leo_by_type


def count_non_debris_by_orbit(df: pd.DataFrame) -> pd.DataFrame:
    # Non-debris objects in space over time, broken down by orbit

    df = df[df.OBJECT_TYPE.isin(["PAYLOAD", "ROCKET BODY"])]

    years = range(
        df.launch_year.min().astype(int), df.launch_year.max().astype(int) + 1
    )

    dataframes = []
    for year in years:
        # For each year, keep all launched objects up to that year & that haven't decayed yet
        df_year = df[
            (df.launch_year <= year) & (df.DECAY_DATE.isnull() | (df.decay_year > year))
        ]
        df_year = (
            df_year[["ORBIT"]].groupby("ORBIT", as_index=False).size().assign(year=year)
        )
        dataframes.append(df_year)

    non_debris_by_orbit = (
        pd.concat(dataframes)
        .reset_index(drop=True)
        .rename(columns={"ORBIT": "entity", "size": "objects"})
    )

    return non_debris_by_orbit


def main():
    df = pd.read_csv(FILE)

    df = df.pipe(define_orbits).pipe(create_year_cols).pipe(filter_years)

    final = pd.concat([count_leo_by_type(df), count_non_debris_by_orbit(df)])
    final["entity"] = final["entity"].replace(
        {"ROCKET BODY": "Rocket bodies", "PAYLOAD": "Payloads", "DEBRIS": "Debris"}
    )

    final = final.rename(
        columns={"objects": "Number of objects", "entity": "ENTITY", "year": "YEAR"}
    )[["ENTITY", "YEAR", "Number of objects"]].sort_values(["ENTITY", "YEAR"])
    final.to_csv("Space-Track - Number of objects in space.csv", index=False)


if __name__ == "__main__":
    main()
