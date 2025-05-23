from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

PARENT_DIR = Path(__file__).parent.absolute()

# Define  version of PIP data
VERSION = "2025-01-22"

# Select indicators to analyze
INDICATORS = ["gini_pip_disposable_percapita"]

# Define only_all_series categories and a shorter name
ONLY_ALL_SERIES = {
    "Only countries in all sources": "all_false",
    "All data points": "all_true",
}

# Define PIP percentiles URL

DATASET_URL = f"http://catalog.ourworldindata.org/garden/poverty_inequality/{VERSION}/inequality_comparison/inequality_comparison.feather?nocache"

# Define percentage change where we consider an insignificant change
PERCENTAGE_CHANGE_THRESHOLD = 0.025

# Define dimensions of exported image
WIDTH = 1000
HEIGHT = 1500

# Read data
df = pd.read_feather(DATASET_URL)

# Rename rows in only_all_series
df["only_all_series"] = df["only_all_series"].cat.rename_categories(ONLY_ALL_SERIES)


# Keep the data in unique rows using this index ["country", "ref_year", "only_all_series"]
df = df.groupby(["country", "ref_year", "only_all_series"], as_index=False, observed=True).first()


# Pivot data with ref_year as columns
df = df.pivot(
    index=["country"],
    columns=["ref_year", "only_all_series"],
    values=INDICATORS,
).reset_index()


# Flatten columns
df.columns = ["_".join(map(str, col)).strip() for col in df.columns.values]

# Remove trailing underscore
df.columns = df.columns.str.rstrip("_")

# Remove rows with an entire row of missing values (except for country)
df = df.dropna(how="all", subset=[col for col in df.columns if col != "country"])

# Calculate the difference between values
for indicator in INDICATORS:
    for only_all_series in ONLY_ALL_SERIES.values():
        df[f"{indicator}_{only_all_series}_diff"] = (
            df[f"{indicator}_2019_{only_all_series}"]
            - df[f"{indicator}_1993_{only_all_series}"]
        )

        # Also calculate the percentage change
        df[f"{indicator}_{only_all_series}_perc_diff"] = (
            df[f"{indicator}_{only_all_series}_diff"]
            / df[f"{indicator}_1993_{only_all_series}"]
            * 100
        )

# Sort df by gini_pip_disposable_percapita_all_true_diff
df = df.sort_values(
    by="gini_pip_disposable_percapita_all_true_diff", ascending=False
)


# With plotly express, plot dumbbells for each country (shown by row), using gini_pip_disposable_percapita_1993_all_true and gini_pip_disposable_percapita_2019_all_true
fig = go.Figure()

# Add bars for the difference in Gini Coefficient
fig.add_trace(
    go.Bar(
        x=df["gini_pip_disposable_percapita_all_true_diff"],
        y=df["country"],
        orientation="h",
        marker=dict(
            color=[
                "#E56E5A"
                if val > PERCENTAGE_CHANGE_THRESHOLD
                else "#286BBB"
                if val < -PERCENTAGE_CHANGE_THRESHOLD
                else "#D3D3D3"
                for val in df["gini_pip_disposable_percapita_all_true_diff"]
            ],
        ),
    )
)

fig.update_layout(
    title="Change in Gini Coefficient from 1993 to 2019",
    xaxis_title="Change in Gini Coefficient",
    yaxis_title="Country",
    yaxis=dict(type="category", dtick=1),  # Ensure all countries are shown
    xaxis=dict(
        range=[
            df["gini_pip_disposable_percapita_all_true_diff"].min(),
            df["gini_pip_disposable_percapita_all_true_diff"].max(),
        ],
    ),
)

# Export png
fig.write_image(
    PARENT_DIR / "global_income_distribution.png", width=WIDTH, height=HEIGHT
)

# Export svg
fig.write_image(
    PARENT_DIR / "global_income_distribution.svg", width=WIDTH, height=HEIGHT
)

# Show the plot
fig.show()
