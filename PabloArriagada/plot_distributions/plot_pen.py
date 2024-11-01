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

# Plot a line chart with  the columns percentile vs thr in plotly express
fig = px.line(
    df_percentiles_world,
    x="percentile",
    y="thr",
    title="World Bank PIP Percentiles",
    labels={"percentile": "Percentile", "thr": "Threshold"},
    log_y=False,
)

# Add a horizontal line for the IPL
fig.add_hline(
    y=INTERNATIONAL_POVERTY_LINE,
    line_dash="dot",
    line_color="red",
    annotation_text="IPL",
    annotation_position="top right",
)

fig.show()
