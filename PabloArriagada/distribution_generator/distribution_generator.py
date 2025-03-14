from pathlib import Path
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

PARENT_DIR = Path(__file__).parent.absolute()

# Define International Poverty Line
INTERNATIONAL_POVERTY_LINE = 2.15

# Define width and height of the plot
WIDTH = 1500
HEIGHT = 750

# Define pair of countries to estimate data
COUNTRIES = [
    ["Denmark", "Ethiopia"],
    ["Denmark", "Democratic Republic of Congo"],
    ["Denmark", "Kenya"],
    ["Denmark", "Niger"],
    {"Denmark", "Syria"},
    {"United States", "Burundi"},
]

# Define  version of PIP and 1000 bins data
PIP_VERSION = "2024-10-07"
THOUSAND_BINS_VERSION = "2025-03-10"

# Define URLs

THOUSAND_BINS_URL = f"http://catalog.ourworldindata.org/garden/wb/{THOUSAND_BINS_VERSION}/thousand_bins_distribution/thousand_bins_distribution.feather?nocache"
PERCENTILES_URL = f"http://catalog.ourworldindata.org/garden/wb/{PIP_VERSION}/world_bank_pip/percentiles_income_consumption_2017.feather?nocache"
MAIN_INDICATORS_URL = f"http://catalog.ourworldindata.org/garden/wb/{PIP_VERSION}/world_bank_pip/income_consumption_2017.feather?nocache"


def run() -> None:
    # Read data
    df_thousand_bins = pd.read_feather(THOUSAND_BINS_URL)
    df_percentiles = pd.read_feather(PERCENTILES_URL)
    df_main_indicators = pd.read_feather(MAIN_INDICATORS_URL)

    for countries in COUNTRIES:
        # Overlapping distributions with independent density estimates
        distributional_plots(
            data=df_thousand_bins,
            df_main_indicators=df_main_indicators,
            x="avg",
            weights="pop",
            log_scale=True,
            multiple="layer",
            hue="country",
            ridge_plot=False,
            hue_order=countries,
            years=None,
            legend=True,
            common_norm=False,
        )

    # Stacked distributions with common density estimate
    distributional_plots(
        data=df_thousand_bins,
        df_main_indicators=df_main_indicators,
        x="avg",
        weights="pop",
        log_scale=True,
        multiple="stack",
        hue="country",
        ridge_plot=False,
        hue_order=["Denmark", "Ethiopia"],
        years=[2024],
        legend=True,
        common_norm=True,
    )


def distributional_plots(
    data: pd.DataFrame,
    df_main_indicators: pd.DataFrame,
    x: str,
    weights: str,
    log_scale: bool,
    multiple: str,
    hue: str,
    ridge_plot: bool = False,
    hue_order: List[str] = None,
    years: List[int] = None,
    legend: bool = True,
    common_norm: bool = True,
) -> None:
    """
    Plot distributional data with seaborn, with multiple options for customization.
    """

    # If no years are provided, use all years in the data
    if years is None:
        years = list(data["year"].unique())

    # Filter data by years
    data = data[data["year"].isin(years)].reset_index(drop=True)

    # Define filename according to the hue_order
    if len(hue_order) <= 5:
        filename = "_".join(hue_order)
    elif len(hue_order) > 5:
        filename = "multiple_countries"
    else:
        filename = "all_countries"

    for year in years:
        data_year = data[data["year"] == year].reset_index(drop=True)

        # Define world mean
        world_mean_year = df_main_indicators.loc[
            (df_main_indicators["country"] == "World")
            & (df_main_indicators["year"] == year),
            "mean",
        ].values[0]

        # Define world median
        world_median_year = df_main_indicators.loc[
            (df_main_indicators["country"] == "World")
            & (df_main_indicators["year"] == year),
            "median",
        ].values[0]

        # Plot a kde with seaborn
        kde_plot = sns.kdeplot(
            data=data_year,
            x=x,
            weights=weights,
            fill=True,
            log_scale=log_scale,
            hue=hue,
            hue_order=hue_order,
            multiple=multiple,
            legend=legend,
            common_norm=common_norm,
        )

        if log_scale:
            # Customize x-axis ticks to show 1, 2, 5, 10, 20, 50, 100, etc.
            # kde_plot.set(xscale="log")
            kde_plot.set_xticks([1, 2, 5, 10, 20, 50, 100, 200, 500, 1000])
            kde_plot.get_xaxis().set_major_formatter(plt.ScalarFormatter())

        # Add a vertical line for the international poverty line
        plt.axvline(
            x=INTERNATIONAL_POVERTY_LINE,
            color="lightgrey",
            linestyle="--",
            linewidth=0.8,
        )
        plt.text(
            x=INTERNATIONAL_POVERTY_LINE,  # x-coordinate for the text
            y=plt.ylim()[1]
            * 0.99,  # y-coordinate for the text, positioned near the top of the plot
            s=f"International Poverty Line: ${INTERNATIONAL_POVERTY_LINE}",  # Text string to display
            color="grey",  # Color of the text
            rotation=90,  # Rotate the text 90 degrees
            verticalalignment="top",  # Align the text vertically at the top
            fontsize=8,  # Font size of the text
        )

        # Add a vertical line for the world mean, in the same format as the international poverty line
        plt.axvline(
            x=world_mean_year,
            color="lightgrey",
            linestyle="--",
            linewidth=0.8,
        )
        plt.text(
            x=world_mean_year,
            y=plt.ylim()[1] * 0.99,
            s=f"World mean: ${round(world_mean_year,2):.2f}",
            color="grey",
            rotation=90,
            verticalalignment="top",
            fontsize=8,
        )

        # Add a vertical line for the world median, in the same format as the international poverty line
        plt.axvline(
            x=world_median_year,
            color="lightgrey",
            linestyle="--",
            linewidth=0.8,
        )
        plt.text(
            x=world_median_year,
            y=plt.ylim()[1] * 0.99,
            s=f"World median: ${round(world_median_year,2):.2f}",
            color="grey",
            rotation=90,
            verticalalignment="top",
            fontsize=8,
        )

        if legend:
            # Move the legend inside the plot
            kde_plot.legend_.set_bbox_to_anchor((0.8, 0.8))
            kde_plot.legend_.set_loc("upper left")

        fig = kde_plot.get_figure()
        fig.set_size_inches(WIDTH / 100, HEIGHT / 100)
        fig.savefig(
            f"{PARENT_DIR}/{filename}_{year}_log_{log_scale}_multiple_{multiple}_common_norm_{common_norm}.svg"
        )
        plt.close(fig)

    return None


if __name__ == "__main__":
    run()
