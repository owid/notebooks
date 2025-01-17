from pathlib import Path

import numpy as np
import pandas as pd
import plotly.figure_factory as ff

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

# Define countries and years
COUNTRIES_YEARS = {
    1: {
        "United States": 2022,
        "Burundi": 2020,
    },
    2: {
        "Ethiopia": 2015,
        "Denmark": 2021,
    },
}

# Define latest year for world mean
LATEST_YEAR = 2024

# Define minimum log income
MIN_LOG_INCOME = -2

# Define maximum income
MAX_INCOME = 1000

# Define width and height for the plot
WIDTH = 1500
HEIGHT = 750

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

# Define world mean
WORLD_MEAN = df_main_indicators.loc[
    (df_main_indicators["country"] == "World")
    & (df_main_indicators["year"] == LATEST_YEAR),
    "mean",
].values[0]

# Define world median
WORLD_MEDIAN = df_main_indicators.loc[
    (df_main_indicators["country"] == "World")
    & (df_main_indicators["year"] == LATEST_YEAR),
    "median",
].values[0]

for set, countries_years in COUNTRIES_YEARS.items():
    # Filter first country in set
    df_percentiles_country_1 = (
        df_percentiles[
            (df_percentiles["country"] == list(countries_years.keys())[0])
            & (df_percentiles["year"] == list(countries_years.values())[0])
        ]
        .reset_index(drop=True)
        .copy()
    )

    # Get values of thr and thr_log for country 1 at percentile 50
    df_percentiles_country_1_50 = df_percentiles_country_1[
        df_percentiles_country_1["percentile"] == 50
    ][["thr", "thr_log", "avg", "avg_log"]].values[0]

    # Get values of mean
    MEAN_COUNTRY_1 = df_main_indicators.loc[
        (df_main_indicators["country"] == list(countries_years.keys())[0])
        & (df_main_indicators["year"] == list(countries_years.values())[0]),
        "mean",
    ].values[0]

    # Get value of median as shown in the main indicators
    MEDIAN_COUNTRY_1 = df_main_indicators.loc[
        (df_main_indicators["country"] == list(countries_years.keys())[0])
        & (df_main_indicators["year"] == list(countries_years.values())[0]),
        "median",
    ].values[0]

    # NOTE: I omitted this bit, because the curve is distorted when adding the percentiles 0 and 100
    # # Add percentile 0 to df_percentiles_country_1, with country = list(countries_years.keys())[0], year = list(countries_years.values())[0]
    # df_percentile_0_country_1 = pd.DataFrame.from_dict(
    #     data={
    #         "country": [list(countries_years.keys())[0]],
    #         "year": [list(countries_years.values())[0]],
    #         "percentile": [0],
    #         "thr": [0],
    #         "thr_log": [MIN_LOG_INCOME],
    #     }
    # )

    # # Add percentile 100 to df_percentiles_country_1, with country = list(countries_years.keys())[0], year = list(countries_years.values())[0]
    # df_percentile_100_country_1 = pd.DataFrame.from_dict(
    #     data={
    #         "country": [list(countries_years.keys())[0]],
    #         "year": [list(countries_years.values())[0]],
    #         "percentile": [100],
    #         "thr": [MAX_INCOME],
    #         "thr_log": [np.log(MAX_INCOME)],
    #     }
    # )

    # # Concatenate
    # df_percentiles_country_1 = pd.concat(
    #     [
    #         df_percentile_0_country_1,
    #         df_percentiles_country_1,
    #         df_percentile_100_country_1,
    #     ],
    #     ignore_index=True,
    # )

    # Filter second country in set
    df_percentiles_country_2 = (
        df_percentiles[
            (df_percentiles["country"] == list(countries_years.keys())[1])
            & (df_percentiles["year"] == list(countries_years.values())[1])
        ]
        .reset_index(drop=True)
        .copy()
    )

    # Get values of thr and thr_log for country 2 at percentile 50
    df_percentiles_country_2_50 = df_percentiles_country_2[
        df_percentiles_country_2["percentile"] == 50
    ][["thr", "thr_log", "avg", "avg_log"]].values[0]

    # Get values of mean
    MEAN_COUNTRY_2 = df_main_indicators.loc[
        (df_main_indicators["country"] == list(countries_years.keys())[1])
        & (df_main_indicators["year"] == list(countries_years.values())[1]),
        "mean",
    ].values[0]

    # Get value of median as shown in the main indicators
    MEDIAN_COUNTRY_2 = df_main_indicators.loc[
        (df_main_indicators["country"] == list(countries_years.keys())[1])
        & (df_main_indicators["year"] == list(countries_years.values())[1]),
        "median",
    ].values[0]

    # NOTE: I omitted this bit, because the curve is distorted when adding the percentiles 0 and 100
    # # Add percentile 0 to df_percentiles_country_2, with country = list(countries_years.keys())[1], year = list(countries_years.values())[1]
    # df_percentile_0_country_2 = pd.DataFrame.from_dict(
    #     data={
    #         "country": [list(countries_years.keys())[1]],
    #         "year": [list(countries_years.values())[1]],
    #         "percentile": [0],
    #         "thr": [0],
    #         "thr_log": [MIN_LOG_INCOME],
    #     }
    # )

    # # Add percentile 100 to df_percentiles_country_2, with country = list(countries_years.keys())[1], year = list(countries_years.values())[1]
    # df_percentile_100_country_2 = pd.DataFrame.from_dict(
    #     data={
    #         "country": [list(countries_years.keys())[1]],
    #         "year": [list(countries_years.values())[1]],
    #         "percentile": [100],
    #         "thr": [MAX_INCOME],
    #         "thr_log": [np.log(MAX_INCOME)],
    #     }
    # )

    # # Concatenate
    # df_percentiles_country_2 = pd.concat(
    #     [
    #         df_percentile_0_country_2,
    #         df_percentiles_country_2,
    #         df_percentile_100_country_2,
    #     ],
    #     ignore_index=True,
    # )

    data_list = [
        df_percentiles_country_1["thr_log"],
        df_percentiles_country_2["thr_log"],
    ]
    label_list = [list(countries_years.keys())[0], list(countries_years.keys())[1]]

    ########################################################
    # PLOT
    ########################################################

    # Plot density curve for thr_log
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
        np.log(2),
        np.log(5),
        np.log(10),
        np.log(20),
        np.log(50),
        np.log(100),
        np.log(200),
        np.log(500),
    ]
    ticktext = [f"{int(round(np.exp(val),1))}" for val in tickvals]

    # Update layout
    fig.update_layout(
        title=f"Density curve of income for {list(countries_years.keys())[0]} and {list(countries_years.keys())[1]}",
        xaxis_title="Income (log scale)",
        yaxis_title="Density",
        xaxis=dict(
            tickvals=tickvals,
            ticktext=ticktext,
        ),
        yaxis={"visible": False, "showticklabels": False},
        showlegend=False,
        plot_bgcolor="rgba(0, 0, 0, 0)",
    )

    fig.update_yaxes(range=[0, 0.9])

    fig.add_vline(
        x=df_percentiles_country_1_50[1],
        line_width=0.5,
        line_dash="dot",
        line_color="grey",
        annotation_text=f"<b>{list(countries_years.keys())[0]} ({list(countries_years.values())[0]})</b><br>Median income: &#36;{round(MEDIAN_COUNTRY_1,1):.2f}<br>Mean income: &#36;{round(MEAN_COUNTRY_1,1):.2f}",
        annotation_position="top right",
        annotation_align="left",
    )
    fig.add_vline(
        x=df_percentiles_country_2_50[1],
        line_width=0.5,
        line_dash="dot",
        line_color="grey",
        annotation_text=f"<b>{list(countries_years.keys())[1]} ({list(countries_years.values())[1]})</b><br>Median income: &#36;{round(MEDIAN_COUNTRY_2,1):.2f}<br>Mean income: &#36;{round(MEAN_COUNTRY_2,1):.2f}",
        annotation_position="top left",
        annotation_align="right",
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

    # For the World mean
    fig.add_vline(
        x=np.log(WORLD_MEAN),
        line_width=0.5,
        line_dash="dot",
        line_color="black",
        annotation_text=f"World mean: &#36;{round(WORLD_MEAN,1):.2f}",
        annotation_position="bottom right",
        annotation_textangle=-90,
    )

    # For the World median
    fig.add_vline(
        x=np.log(WORLD_MEDIAN),
        line_width=0.5,
        line_dash="dot",
        line_color="black",
        annotation_text=f"World median: &#36;{round(WORLD_MEDIAN,1):.2f}",
        annotation_position="bottom right",
        annotation_textangle=-90,
    )

    # Add line at y=0
    fig.add_hline(y=0, line_width=2, line_color="grey")

    # Format ticks
    fig.update_xaxes(
        showgrid=True, ticks="outside", tickson="boundaries", ticklen=5, color="grey"
    )

    # Fill area under each curve
    x1 = [xc for xc in fig.data[0].x]
    y1 = fig.data[0].y[: len(x1)]

    x2 = [xc for xc in fig.data[1].x]
    y2 = fig.data[1].y[: len(x2)]
    fig.add_scatter(
        x=x1, y=y1, fill="tozeroy", mode="none", fillcolor="#67b1e5"
    )  # original #1f77b4
    fig.add_scatter(
        x=x2, y=y2, fill="tozeroy", mode="none", fillcolor="#ffa04d"
    )  # original #ff7f0e

    # Export png
    fig.write_image(
        PARENT_DIR
        / f"density_curve_{list(countries_years.keys())[0]}_{list(countries_years.keys())[1]}.png",
        width=WIDTH,
        height=HEIGHT,
    )

    # Export svg
    fig.write_image(
        PARENT_DIR
        / f"density_curve_{list(countries_years.keys())[0]}_{list(countries_years.keys())[1]}.svg",
        width=WIDTH,
        height=HEIGHT,
    )

    fig.show()
