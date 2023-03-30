import datetime
from pathlib import Path

import pandas as pd

# Set directory path
PARENT_DIR = Path(__file__).parent.absolute()

df = pd.read_csv(PARENT_DIR / "historical.csv")

# Remove empty start_data_formatted and end_date_formatted
df = df[
    ~(df["start_date_formatted"].isnull()) & ~(df["end_date_formatted"].isnull())
].reset_index(drop=True)

# Get year after comma in the column name start_date_formatted and end_date_formatted
df["year_start"] = (
    df["start_date_formatted"].str.split(",").str[1].str.strip().astype(int)
)
df["year_end"] = df["end_date_formatted"].str.split(",").str[1].str.strip().astype(int)

# Show countries with year_start or year_end equal to -1
print(df[(df["year_start"] == -1) | (df["year_end"] == -1)]["country"].unique())

# Drop rows where year_start or year_end is -1
df = df[(df["year_start"] != -1) & (df["year_end"] != -1)]

# Create dataframe filling the years between year_start and year_end

df_historical_long = pd.DataFrame()
for i in range(len(df)):
    df_country = pd.DataFrame(
        {
            "country": df.iloc[i]["country"],
            "year": range(df.iloc[i]["year_start"], df.iloc[i]["year_end"]),
            "issue": df.iloc[i]["issue"],
            "id": df.iloc[i]["id"],
            "value": df.iloc[i]["value"],
            "value_formatted": df.iloc[i]["value_formatted"],
            "description": df.iloc[i]["description"],
        }
    )
    df_historical_long = pd.concat([df_historical_long, df_country], ignore_index=True)

# For current data
df = pd.read_csv(PARENT_DIR / "current.csv")

# Remove empty start_data_formatted
df = df[~df["start_date_formatted"].isnull()].reset_index(drop=True)

# Get year after comma in the column name start_date_formatted
df["year_start"] = (
    df["start_date_formatted"].str.split(",").str[1].str.strip().astype(int)
)

# Show countries with year_start or year_end equal to -1
print(df[df["year_start"] == -1]["country"].unique())

# Drop rows where year_start or year_end is -1
df = df[df["year_start"] != -1]

# Obtain current year
current_year = datetime.datetime.now().year

# Create dataframe filling the years between year_start and year_end

df_current_long = pd.DataFrame()
for i in range(len(df)):
    df_country = pd.DataFrame(
        {
            "country": df.iloc[i]["country"],
            "year": range(df.iloc[i]["year_start"], current_year + 1),
            "issue": df.iloc[i]["issue"],
            "id": df.iloc[i]["id"],
            "value": df.iloc[i]["value"],
            "value_formatted": df.iloc[i]["value_formatted"],
            "description": df.iloc[i]["description"],
        }
    )
    df_current_long = pd.concat([df_current_long, df_country], ignore_index=True)

# Concatenate historical and current data
df_long = pd.concat([df_historical_long, df_current_long], ignore_index=True)

df_long.to_csv(PARENT_DIR / "long.csv", index=False)

# Set index as country, year and issue and verify that there are no duplicates
df_long = df_long.set_index(
    ["country", "year", "issue"], verify_integrity=False
).sort_index()

# Show rows with duplicated index
df_duplicated = df_long[df_long.index.duplicated(keep=False)]
df_duplicated.to_csv(PARENT_DIR / "duplicated.csv", index=True)
