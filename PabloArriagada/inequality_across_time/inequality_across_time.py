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


# Set line dash, dot or solid
LINE_DASH = "dot"
LINE_WIDTH = 1

# Read data
df = pd.read_feather(DATASET_URL)

# Rename rows in only_all_series
df["only_all_series"] = df["only_all_series"].replace(ONLY_ALL_SERIES)

# Keep the data in unique rows using this index ["country", "ref_year", "only_all_series"]
df = df.groupby(["country", "ref_year", "only_all_series"], as_index=False).first()


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

# Remove rows with missing values (except for country)
df = df.dropna(subset=[col for col in df.columns if col != "country"])

# Calculate the difference between values
for indicator in INDICATORS:
    for only_all_series in ONLY_ALL_SERIES.values():
        df[f"{indicator}_{only_all_series}_diff"] = (
            df[f"{indicator}_2019_{only_all_series}"]
            - df[f"{indicator}_1993_{only_all_series}"]
        )

# Sort df by gini_pip_disposable_percapita_all_true_diff
df = df.sort_values(by="gini_pip_disposable_percapita_all_true_diff", ascending=False)

print(df)

# With plotly express, plot dumbbells for each country (shown by row), using gini_pip_disposable_percapita_1993_all_true and gini_pip_disposable_percapita_2019_all_true
fig = go.Figure()

for i, row in df.iterrows():
    fig.add_trace(
        go.Scatter(
            x=[row["gini_pip_disposable_percapita_1993_all_true"]],
            y=[row["country"]],
            mode="markers",
            marker=dict(color="red", size=10),
            name=f"{row['country']} 1993",
            showlegend=False,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[row["gini_pip_disposable_percapita_2019_all_true"]],
            y=[row["country"]],
            mode="markers",
            marker=dict(color="green", size=10),
            name=f"{row['country']} 2019",
            showlegend=False,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[
                row["gini_pip_disposable_percapita_1993_all_true"],
                row["gini_pip_disposable_percapita_2019_all_true"],
            ],
            y=[row["country"], row["country"]],
            mode="lines",
            line=dict(color="gray", width=1, dash="dot"),
            showlegend=False,
        )
    )

fig.update_layout(
    title="Gini coefficient in 1993 vs 2019",
    xaxis_title="Gini coefficient",
    yaxis_title="Country",
    yaxis=dict(type="category"),
    xaxis=dict(range=[0, 1]),
)

# Show the plot
fig.show()
