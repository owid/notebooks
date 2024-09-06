from pathlib import Path

import numpy as np
import pandas as pd
import plotly.figure_factory as ff

PARENT_DIR = Path(__file__).parent.absolute()

# Define OWID version of PIP data
PIP_VERSION = "2024-03-27"
POPULATION_VERSION = "2024-07-15"

# Define PIP percentiles URL
PERCENTILES_URL = f"http://catalog.ourworldindata.org/garden/wb/{PIP_VERSION}/world_bank_pip/percentiles_income_consumption_2017.feather"
MAIN_INDICATORS_URL = f"http://catalog.ourworldindata.org/garden/wb/{PIP_VERSION}/world_bank_pip/income_consumption_2017.feather"

POPULATION_URL = f"http://catalog.ourworldindata.org/garden/demography/{POPULATION_VERSION}/population/population.feather"

df_percentiles = pd.read_feather(PERCENTILES_URL)
df_main_indicators = pd.read_feather(MAIN_INDICATORS_URL)
df_population = pd.read_feather(POPULATION_URL)


# Add population to df_percentiles
df_percentiles = pd.merge(
    df_percentiles,
    df_population[["country", "year", "population"]],
    on=["country", "year"],
    how="left",
)

# Multiply share column by population to get the number of people in each percentile
df_percentiles["people"] = df_percentiles["share"] * df_percentiles["population"]

# Calculate avg_log as the logarithm of the average income
df_percentiles["avg_log"] = np.log(df_percentiles["avg"])

# Filter Chile
df_percentiles_chile = (
    df_percentiles[df_percentiles["country"] == "Chile"].reset_index(drop=True).copy()
)

# Filter US
df_percentiles_us = (
    df_percentiles[
        (df_percentiles["country"] == "United States")
        & (df_percentiles["year"] == 2020)
    ]
    .reset_index(drop=True)
    .copy()
)

# Filter Burundi
df_percentiles_burundi = (
    df_percentiles[
        (df_percentiles["country"] == "Burundi") & (df_percentiles["year"] == 2020)
    ]
    .reset_index(drop=True)
    .copy()
)

data_list = [
    df_percentiles_us["avg_log"],
    df_percentiles_burundi["avg_log"],
]
label_list = ["US", "Burundi"]

# data_list = []
# label_list = []
# for year in df_percentiles_chile["year"].unique():
#     df_percentiles_year = (
#         df_percentiles_chile[(df_percentiles_chile["year"] == year)]
#         .reset_index(drop=True)
#         .copy()
#     )
#     data_list.append(df_percentiles_year["avg"])
#     label_list.append(str(year))


# Plot density curve for avg vs people for Chile in 2017
# The probability numers should be multiplied bt population to get the number of people in each percentile
fig = ff.create_distplot(
    hist_data=data_list,
    group_labels=label_list,
    curve_type="normal",
    show_hist=False,
    show_rug=False,
)

# Define tick values and labels for the x-axis
tickvals = [
    2.718281828,
    7.389056099,
    148.4131591,
    22026.46579,
    485165195.4,
]
ticktext = [f"{np.exp(val)}" for val in tickvals]

# Update layout
fig.update_layout(
    title="Density curve of income for US and Burundi in 2020",
    xaxis_title="Income (log scale)",
    yaxis_title="Density",
    xaxis=dict(
        tickvals=tickvals,
        ticktext=ticktext,
    ),
)

# Export png
fig.write_image(PARENT_DIR / "density_curve_us_burundi_2020.png")

fig.show()
