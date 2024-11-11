from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px

PARENT_DIR = Path(__file__).parent.absolute()

# Define OWID version of PIP data
PIP_VERSION = "2024-10-07"
POPULATION_VERSION = "2024-07-15"

# Define PIP percentiles URL
PERCENTILES_URL = f"http://catalog.ourworldindata.org/garden/wb/{PIP_VERSION}/world_bank_pip/percentiles_income_consumption_2017.feather"
MAIN_INDICATORS_URL = f"http://catalog.ourworldindata.org/garden/wb/{PIP_VERSION}/world_bank_pip/income_consumption_2017.feather"

POPULATION_URL = f"http://catalog.ourworldindata.org/garden/demography/{POPULATION_VERSION}/population/population.feather"

# Define IPL
INTERNATIONAL_POVERTY_LINE = 2.15

# Define latest year
LATEST_YEAR = 2024

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

US_MEDIAN = df_percentiles.loc[
    (df_percentiles["country"] == "United States")
    & (df_percentiles["year"] == latest_year_us)
    & (df_percentiles["percentile"] == 50),
    "thr",
].values[0]


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
    xaxis=dict(ticksuffix="%"),
    yaxis=dict(
        side="right",
        title="Daily income or consumption",
        tickprefix="$",
        ticksuffix=" a day",
    ),
)

# Add a horizontal line for the IPL
fig.add_hline(
    y=INTERNATIONAL_POVERTY_LINE,
    line_dash=LINE_DASH,
    line_color="red",
    line_width=LINE_WIDTH,
    annotation_text=f"International Poverty Line: ${INTERNATIONAL_POVERTY_LINE}",
    annotation_position="top right",
)

# Add median
fig.add_hline(
    y=WORLD_MEDIAN,
    line_dash=LINE_DASH,
    line_color="red",
    line_width=LINE_WIDTH,
    annotation_text=f"World median: ${WORLD_MEDIAN:.2f}",
    annotation_position="top right",
)

# Add 90th percentile
fig.add_hline(
    y=WORLD_90TH,
    line_dash=LINE_DASH,
    line_color="red",
    line_width=LINE_WIDTH,
    annotation_text=f"World 90th percentile: ${WORLD_90TH:.2f}",
    annotation_position="top right",
)

# Add 99th percentile
fig.add_hline(
    y=WORLD_99TH,
    line_dash=LINE_DASH,
    line_color="red",
    line_width=LINE_WIDTH,
    annotation_text=f"World 99th percentile: ${WORLD_99TH:.2f}",
    annotation_position="top right",
)

# Add mean
fig.add_hline(
    y=WORLD_MEAN,
    line_dash=LINE_DASH,
    line_color="red",
    line_width=LINE_WIDTH,
    annotation_text=f"World mean: ${WORLD_MEAN:.2f}",
    annotation_position="top right",
)

# Add US median
fig.add_hline(
    y=US_MEDIAN,
    line_dash=LINE_DASH,
    line_color="red",
    line_width=LINE_WIDTH,
    annotation_text=f"US median: ${US_MEDIAN:.2f}",
    annotation_position="top right",
)


# Add a vertical line to say "50% of the world population lives with less than ${WORLD_MEDIAN} per day"
fig.add_shape(
    type="line",
    x0=50,
    x1=50,
    y0=0,
    y1=1,
    yref="paper",
    line=dict(dash=LINE_DASH, color="red", width=LINE_WIDTH),
)
fig.add_annotation(
    x=50,
    y=0.2,
    yref="paper",
    text=f"50% of the world population lives with less than<br><b>${WORLD_MEDIAN:.2f} per day</b>",
    showarrow=False,
    xanchor="left",
    align="left",
)

fig.show()
