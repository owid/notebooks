from pathlib import Path

import numpy as np
import pandas as pd

PARENT_DIR = Path(__file__).parent.absolute()

# Define  version of PIP data
VERSION = "2025-06-11"

# Define PIP percentiles URL

DATASET_URL = f"http://catalog.ourworldindata.org/garden/wb/{VERSION}/thousand_bins_distribution/thousand_bins_distribution.feather?nocache"

# Read data
df = pd.read_feather(DATASET_URL)

# Sort data by year and avg
df = df.sort_values(by=["year", "avg"], ascending=[True, True]).reset_index(drop=True)

# Calculate the cumulative sum of the population by year
df["cum_pop"] = df.groupby("year")["pop"].cumsum()

# Calculate the global population as the last value of cum_pop by year
df["global_population"] = df.groupby("year")["cum_pop"].transform("max")

# Calculate the cumulative sum of the population as a percentage of the global population by year
df["cum_pop_perc"] = df["cum_pop"] / df["global_population"] * 100

# Define the cum_pop_perc that is closest to 10, 20, 30, ..., 100 and assign it to all the other rows by year
df["decile"] = df["cum_pop_perc"].apply(lambda x: np.ceil(x / 10))

# Calculate the weighted average of avg, using pop as weights, by decile and year
df["avg"] = df["avg"] * df["pop"]
df = (
    df.groupby(["year", "decile"])
    .agg(
        {
            "avg": "sum",
            "pop": "sum",
        }
    )
    .reset_index()
)

# Divide avg by the total avg, to get the share of the total income by year
df["share"] = df.groupby("year")["avg"].transform(lambda x: x / x.sum() * 100)

# Divide avg by the total population, to get the average income per person by year
df["avg"] = df["avg"] / df["pop"]

# Save to csv
df.to_csv(PARENT_DIR / "global_income_distribution.csv", index=False)
