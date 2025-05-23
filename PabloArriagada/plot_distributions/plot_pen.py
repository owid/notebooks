from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

PARENT_DIR = Path(__file__).parent.absolute()

# Define OWID version of PIP data
PIP_VERSION = "2024-10-07"
POPULATION_VERSION = "2024-07-15"

# Define PIP percentiles URL
PERCENTILES_URL = f"http://catalog.ourworldindata.org/garden/wb/{PIP_VERSION}/world_bank_pip/percentiles_income_consumption_2017.feather?nocache"
MAIN_INDICATORS_URL = f"http://catalog.ourworldindata.org/garden/wb/{PIP_VERSION}/world_bank_pip/income_consumption_2017.feather?nocache"

POPULATION_URL = f"http://catalog.ourworldindata.org/garden/demography/{POPULATION_VERSION}/population/population.feather?nocache"

# Define IPL
INTERNATIONAL_POVERTY_LINE = 2.15

# Define latest year
LATEST_YEAR = 2024

# Define maximum income
MAX_INCOME = 500

# Define maximum income for the plot
MAX_INCOME_PLOT = 150

# Set line dash, dot or solid
LINE_DASH = "dot"
LINE_WIDTH = 1

df_percentiles = pd.read_feather(PERCENTILES_URL)
df_main_indicators = pd.read_feather(MAIN_INDICATORS_URL)
df_population = pd.read_feather(POPULATION_URL)


# Select World in df_percentiles
df_percentiles_world = (
    df_percentiles[
        (df_percentiles["country"] == "World") & (df_percentiles["year"] == LATEST_YEAR)
    ]
    .reset_index(drop=True)
    .copy()
)

# Add percentiles 0 and 100
df_percentile_0_world = pd.DataFrame.from_dict(
    data={
        "country": ["World"],
        "year": [LATEST_YEAR],
        "percentile": [0],
        "thr": [0],
    }
)

df_percentile_100_world = pd.DataFrame.from_dict(
    data={
        "country": ["World"],
        "year": [LATEST_YEAR],
        "percentile": [100],
        "thr": [MAX_INCOME],
    }
)

# Concatenate
df_percentiles_world = pd.concat(
    [df_percentile_0_world, df_percentiles_world, df_percentile_100_world],
    ignore_index=True,
)

# Define world median
WORLD_MEDIAN = df_percentiles_world.loc[
    df_percentiles_world["percentile"] == 50, "thr"
].values[0]

# Define world mean
WORLD_MEAN = df_main_indicators.loc[
    (df_main_indicators["country"] == "World")
    & (df_main_indicators["year"] == LATEST_YEAR),
    "mean",
].values[0]

# Define world 90th percentile
WORLD_90TH = df_percentiles_world.loc[
    df_percentiles_world["percentile"] == 90, "thr"
].values[0]

# Define world 99th percentile
WORLD_99TH = df_percentiles_world.loc[
    df_percentiles_world["percentile"] == 99, "thr"
].values[0]

# Define US median
# Calculate most recent year in the US, calculating the maximum year with a valid median
latest_year_us = df_main_indicators.loc[
    (df_main_indicators["country"] == "United States")
    & (df_main_indicators["median"].notna()),
    "year",
].max()

US_MEDIAN = df_main_indicators.loc[
    (df_main_indicators["country"] == "United States")
    & (df_main_indicators["year"] == latest_year_us),
    "median",
].values[0]


# Create dataframes to plot subareas of the world, depending on the percentile
df_percentiles_world_below_10th = (
    df_percentiles_world[df_percentiles_world["percentile"] <= 10]
    .copy()
    .reset_index(drop=True)
)

df_percentiles_world_below_median = (
    df_percentiles_world[df_percentiles_world["percentile"] <= 50]
    .copy()
    .reset_index(drop=True)
)

df_percentiles_world_below_90th = (
    df_percentiles_world[df_percentiles_world["percentile"] <= 90]
    .copy()
    .reset_index(drop=True)
)

########################################################
# PLOT
########################################################

# Plot a line chart with  the columns percentile vs thr in plotly express
fig = px.area(
    df_percentiles_world,
    x="percentile",
    y="thr",
    title="World income distribution",
    labels={"percentile": "Percentage of the population", "thr": "Threshold"},
    log_y=False,
)
fig.update_layout(
    xaxis=dict(ticksuffix="%", range=[0, 100]),
    yaxis=dict(
        side="right",
        title="Daily income or consumption",
        tickprefix="$",
        ticksuffix=" a day",
    ),
    showlegend=False,
    plot_bgcolor="rgba(0, 0, 0, 0)",
)

fig.update_yaxes(range=[0, MAX_INCOME_PLOT])

# Add overlapping areas for the different percentiles
fig.add_trace(
    go.Scatter(
        x=df_percentiles_world_below_10th["percentile"],
        y=df_percentiles_world_below_10th["thr"],
        fill="tozeroy",
        mode="none",
    )
)
fig.add_trace(
    go.Scatter(
        x=df_percentiles_world_below_median["percentile"],
        y=df_percentiles_world_below_median["thr"],
        fill="tozeroy",
        mode="none",
    )
)
fig.add_trace(
    go.Scatter(
        x=df_percentiles_world_below_90th["percentile"],
        y=df_percentiles_world_below_90th["thr"],
        fill="tozeroy",
        mode="none",
    )
)


# Add a horizontal line for the IPL
fig.add_hline(
    y=INTERNATIONAL_POVERTY_LINE,
    line_dash=LINE_DASH,
    line_color="red",
    line_width=LINE_WIDTH,
    annotation_text=f"International Poverty Line: ${INTERNATIONAL_POVERTY_LINE}",
    annotation_position="top right",
    x0=1,
    x1=0.09,
)

# Add median
fig.add_hline(
    y=WORLD_MEDIAN,
    line_dash=LINE_DASH,
    line_color="red",
    line_width=LINE_WIDTH,
    annotation_text=f"World median: ${WORLD_MEDIAN:.2f}",
    annotation_position="top right",
    x0=1,
    x1=0.5,
)

# Add 90th percentile
fig.add_hline(
    y=WORLD_90TH,
    line_dash=LINE_DASH,
    line_color="red",
    line_width=LINE_WIDTH,
    annotation_text=f"World 90th percentile: ${WORLD_90TH:.2f}",
    annotation_position="top right",
    x0=1,
    x1=0.9,
)


# Add 99th percentile
fig.add_hline(
    y=WORLD_99TH,
    line_dash=LINE_DASH,
    line_color="red",
    line_width=LINE_WIDTH,
    annotation_text=f"World 99th percentile: ${WORLD_99TH:.2f}",
    annotation_position="top right",
    x0=1,
    x1=0.99,
)

# Add mean
fig.add_hline(
    y=WORLD_MEAN,
    line_dash=LINE_DASH,
    line_color="red",
    line_width=LINE_WIDTH,
    annotation_text=f"World mean: ${WORLD_MEAN:.2f}",
    annotation_position="top right",
    x0=1,
    x1=0.75,
)


# Add US median
fig.add_hline(
    y=US_MEDIAN,
    line_dash=LINE_DASH,
    line_color="red",
    line_width=LINE_WIDTH,
    annotation_text=f"US median: ${US_MEDIAN:.2f}",
    annotation_position="top right",
    x0=1,
    x1=0.9325,
)


# Add a vertical line to say "50% of the world population lives with less than ${WORLD_MEDIAN} per day"
fig.add_annotation(
    x=50,
    y=0.08,
    yref="paper",
    text=f"50% of the world population lives<br>with less than<br><b>${WORLD_MEDIAN:.2f} per day</b>",
    showarrow=False,
    xanchor="left",
    align="left",
)

# Format ticks
fig.update_xaxes(
    showgrid=True, ticks="outside", tickson="boundaries", ticklen=5, color="grey"
)
fig.update_yaxes(
    showgrid=True, ticks="outside", tickson="boundaries", ticklen=5, color="grey"
)

# Export png
fig.write_image(PARENT_DIR / "global_income_distribution.png", width=1100, height=1000)

# Export svg
fig.write_image(PARENT_DIR / "global_income_distribution.svg", width=1100, height=1000)

# fig.show()
