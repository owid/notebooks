from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

PARENT_DIR = Path(__file__).parent.absolute()

# Define  version of PIP data
VERSION = "2025-03-10"

# Define PIP percentiles URL

DATASET_URL = f"http://catalog.ourworldindata.org/garden/wb/{VERSION}/thousand_bins_distribution/thousand_bins_distribution.feather?nocache"

# Read data
df = pd.read_feather(DATASET_URL)

# Select only for the maximum year
df = df[df["year"] == df["year"].max()].reset_index(drop=True)

# Sort data by avg
df = df.sort_values(by="avg", ascending=True).reset_index(drop=True)

# Calculate the cumulative sum of the population
df["cum_pop"] = df["pop"].cumsum()

# Calculate the global population as the last value of cum_pop
global_population = df["cum_pop"].iloc[-1]

# Calculate the cumulative sum of the population as a percentage of the global population
df["cum_pop_perc"] = df["cum_pop"] / global_population * 100

# Define the cum_pop_perc that is closest to 10, 20, 30, ..., 100 and assign it to all the other rows
df["decile"] = df["cum_pop_perc"].apply(lambda x: np.ceil(x / 10))

# Calculate the weighted average of avg, using pop as weights, by decile
df["avg"] = df["avg"] * df["pop"]
df = df.groupby("decile").agg(
    {
        "avg": "sum",
        "pop": "sum",
    }
).reset_index()

# Divide avg by the total avg, to get the share of the total income
df["share"] = df["avg"] / df["avg"].sum() * 100

# Divide avg by the total population, to get the average income per person
df["avg"] = df["avg"] / df["pop"]

print(df)

# Save to csv
df.to_csv(PARENT_DIR / "global_income_distribution.csv", index=False)
