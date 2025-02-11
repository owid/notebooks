from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

PARENT_DIR = Path(__file__).parent.absolute()

# Define OWID version of WDI data
WDI_VERSION = "2025-01-24"

# Define GDP variables
GDP_VARIABLES = ["ny_gdp_pcap_cd_adjusted", "ny_gdp_pcap_pp_kd"]

# Define countries with data
COUNTRIES = ["Burkina Faso", "India", "Brazil", "Spain", "United States"]

# Define WDI URL
WDI_URL = f"https://catalog.ourworldindata.org/garden/worldbank_wdi/{WDI_VERSION}/wdi/wdi.feather?nocache"

# Open file
df_wdi = pd.read_feather(WDI_URL)

# Select variables I need:
df_wdi = df_wdi[["country", "year"] + GDP_VARIABLES]

# Select latest year
latest_year = df_wdi["year"].max()
df_wdi = df_wdi[df_wdi["year"] == latest_year].reset_index(drop=True)

# Select countries
df_wdi = df_wdi[df_wdi["country"].isin(COUNTRIES)].reset_index(drop=True)

# Sort countries by GDP_VARIABLES[1]
df_wdi = df_wdi.sort_values(by=GDP_VARIABLES[1], ascending=True).reset_index(drop=True)

# Plot a horizontal bar chart with each country in the y-axis and the GDP variables as colors
fig = go.Figure()

for variable in GDP_VARIABLES:
    fig.add_trace(
        go.Bar(
            y=df_wdi["country"],
            x=df_wdi[variable],
            name=variable,
            orientation="h",
        )
    )

fig.update_layout(
    title=f"GDP per capita in {latest_year}",
    yaxis_title="Country",
    xaxis_title="GDP per capita",
    barmode="group",
)
# Add values as labels
for i, variable in enumerate(GDP_VARIABLES):
    fig.data[i].text = df_wdi[variable]
    fig.data[i].texttemplate = "$%{text:,.0f}"
    fig.data[i].textposition = "outside"

# Update trace names
fig.data[0].name = "Constant 2021 US$"
fig.data[1].name = "International-$ at 2021 prices"

# Add a dotted line for the value of the United States
fig.add_shape(
    type="line",
    y0=-0.5,
    y1=len(COUNTRIES) - 0.5,
    x0=df_wdi[df_wdi["country"] == "United States"][GDP_VARIABLES[1]].values[0],
    x1=df_wdi[df_wdi["country"] == "United States"][GDP_VARIABLES[1]].values[0],
    line=dict(
        color="grey",
        width=1,
        dash="dash",
    ),
)

fig.show()
