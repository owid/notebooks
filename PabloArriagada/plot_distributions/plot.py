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

# Define IPL
INTERNATIONAL_POVERTY_LINE = 2.15

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

# Calculate avg_log as the logarithm of the average income. Same for thr_log
df_percentiles["avg_log"] = np.log(df_percentiles["avg"])
df_percentiles["thr_log"] = np.log(df_percentiles["thr"])

# Drop percentile 100
df_percentiles = df_percentiles[df_percentiles["percentile"] != 100].reset_index(
    drop=True
)

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

# Get values of thr and thr_log for US at percentile 50
df_percentiles_us_50 = df_percentiles_us[df_percentiles_us["percentile"] == 50][
    ["thr", "thr_log", "avg", "avg_log"]
].values[0]


# Filter Burundi
df_percentiles_burundi = (
    df_percentiles[
        (df_percentiles["country"] == "Burundi") & (df_percentiles["year"] == 2020)
    ]
    .reset_index(drop=True)
    .copy()
)

# Get values of thr and thr_log for Burundi at percentile 50
df_percentiles_burundi_50 = df_percentiles_burundi[
    df_percentiles_burundi["percentile"] == 50
][["thr", "thr_log", "avg", "avg_log"]].values[0]

data_list = [
    df_percentiles_us["thr_log"],
    df_percentiles_burundi["thr_log"],
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
    np.log(1),
    np.log(10),
    np.log(20),
    np.log(50),
    np.log(100),
]
ticktext = [f"{int(round(np.exp(val),1))}" for val in tickvals]

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

fig.add_vline(
    x=df_percentiles_us_50[1], line_width=0.5, line_dash="dot", line_color="grey"
)
fig.add_vline(
    x=df_percentiles_burundi_50[1], line_width=0.5, line_dash="dot", line_color="grey"
)
fig.add_vline(
    x=df_percentiles_us_50[3], line_width=0.5, line_dash="dot", line_color="grey"
)
fig.add_vline(
    x=df_percentiles_burundi_50[3], line_width=0.5, line_dash="dot", line_color="grey"
)

# For the International Poverty Line
fig.add_vline(
    x=np.log(INTERNATIONAL_POVERTY_LINE),
    line_width=0.5,
    line_dash="dot",
    line_color="red",
    annotation_text="International Poverty Line",
    annotation_position="bottom right",
    annotation_textangle=-90,
)

# Export png
fig.write_image(
    PARENT_DIR / "density_curve_us_burundi_2020.png", width=1000, height=600
)

# Export svg
fig.write_image(
    PARENT_DIR / "density_curve_us_burundi_2020.svg", width=1000, height=600
)

# fig.show()
