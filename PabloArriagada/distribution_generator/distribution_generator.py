from pathlib import Path
from typing import List, Literal

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
    ["Denmark", "Syria"],
    ["United States", "Burundi"],
]

# Define values for different periods
PERIOD_VALUES = {
    "day": {"factor": 1, "log_ticks": [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]},
    "month": {
        "factor": 30,
        "log_ticks": [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000],
    },
    "year": {
        "factor": 365,
        "log_ticks": [
            100,
            200,
            500,
            1000,
            2000,
            5000,
            10000,
            20000,
            50000,
            100000,
            200000,
        ],
    },
}

# Set correction factor of the median to show the label in the plot
CORRECTION_FACTOR_LABEL = 0.8

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
            hue_order=countries,
            years=[2024],
            legend=True,
            common_norm=False,
            period="day",
        )
        distributional_plots(
            data=df_percentiles,
            df_main_indicators=df_main_indicators,
            x="avg",
            weights="pop",
            log_scale=True,
            multiple="layer",
            hue="country",
            hue_order=countries,
            years=[2024],
            legend=False,
            common_norm=False,
            period="day",
            survey_based=True,
            preferred_reporting_level="national",
            preferred_welfare_type="income",
        )

        distributional_plots_per_row(
            data=df_thousand_bins,
            df_main_indicators=df_main_indicators,
            x="avg",
            weights="pop",
            log_scale=True,
            multiple="layer",
            hue="country",
            hue_order=["Ethiopia", "Bangladesh", "Vietnam", "Turkey", "United States"],
            years=[2024],
            common_norm=False,
            period="day",
        )

        distributional_plots_per_row(
            data=df_percentiles,
            df_main_indicators=df_main_indicators,
            x="avg",
            weights="pop",
            log_scale=True,
            multiple="layer",
            hue="country",
            hue_order=["Ethiopia", "Bangladesh", "Vietnam", "Turkey", "United States"],
            years=[2024],
            common_norm=False,
            period="day",
            survey_based=True,
            preferred_reporting_level="national",
            preferred_welfare_type="income",
        )

    # Stacked distributions with common density estimate
    distributional_plots(
        data=df_thousand_bins,
        df_main_indicators=df_main_indicators,
        x="avg",
        weights="pop",
        log_scale=True,
        multiple="stack",
        hue="region",
        hue_order=None,
        years=[2024],
        legend=True,
        common_norm=True,
        period="day",
    )


def distributional_plots(
    data: pd.DataFrame,
    df_main_indicators: pd.DataFrame,
    x: str,
    weights: str,
    log_scale: bool,
    multiple: str,
    hue: str,
    hue_order: List[str] = None,
    years: List[int] = None,
    legend: bool = True,
    common_norm: bool = True,
    period: Literal["day", "month", "year"] = "day",
    survey_based: bool = False,
    preferred_reporting_level: Literal["national", "urban", "rural", None] = None,
    preferred_welfare_type: Literal["income", "consumption", None] = None,
) -> None:
    """
    Plot distributional data with seaborn, with multiple options for customization.
    """

    # Filter the data with the hue and hue_order
    if hue_order is not None:
        data = data[data[hue].isin(hue_order)].reset_index(drop=True)

    # If no years are provided, use all years in the data
    if years is None:
        years = list(data["year"].unique())

    # If the dataset is survey-based, filter the data differently
    if survey_based:
        data_reference_year = []
        # Assign a reference year
        for year in years:
            data_reference_year_by_year = data.copy()

            # Assign the reference year
            data_reference_year_by_year["reference_year"] = year

            # Calculate the difference between the reference year and the year
            data_reference_year_by_year["diff_year"] = (
                data_reference_year_by_year["reference_year"]
                - data_reference_year_by_year["year"]
            )

            # By country, select the data with the minimum difference
            data_reference_year_by_year = data_reference_year_by_year.loc[
                data_reference_year_by_year.groupby(
                    ["country", "reporting_level", "welfare_type", "percentile"],
                    observed=True,
                )["diff_year"].idxmin()
            ].reset_index(drop=True)

            # If there are duplicates for the same country in "reporting_level", select preferred_reporting_level if available
            data_reference_year_by_year = data_reference_year_by_year.sort_values(
                by=["reporting_level"],
                key=lambda col: col == preferred_reporting_level,
                ascending=False,
            ).drop_duplicates(
                subset=["country", "welfare_type", "percentile"], keep="first"
            )

            # If there are duplicates for the same country in "welfare_type", select preferred_welfare_tpye if available
            data_reference_year_by_year = data_reference_year_by_year.sort_values(
                by=["welfare_type"],
                key=lambda col: col == preferred_welfare_type,
                ascending=False,
            ).drop_duplicates(
                subset=["country", "reporting_level", "percentile"], keep="first"
            )

            # Resort the data
            data_reference_year_by_year = data_reference_year_by_year.sort_values(
                by=[
                    "country",
                    "year",
                    "reference_year",
                    "reporting_level",
                    "welfare_type",
                    "percentile",
                ]
            )

            # Append the data to the list
            data_reference_year.append(data_reference_year_by_year)

        # Concatenate the data
        data = pd.concat(data_reference_year, ignore_index=True)

    # If the data doesn't come from the survey-based data, use the data as is
    else:
        # Filter data by years
        data = data[data["year"].isin(years)].reset_index(drop=True)

    # Define filename according to the hue_order
    if hue_order is None:
        filename = "all_countries"
    elif len(hue_order) <= 5:
        filename = "_".join(hue_order)
    else:
        filename = "multiple_countries"

    # Define the income period values
    period_factor = PERIOD_VALUES[period]["factor"]
    log_ticks = PERIOD_VALUES[period]["log_ticks"]

    data[x] = data[x] * period_factor

    # Define IPL for the period
    ipl = INTERNATIONAL_POVERTY_LINE * period_factor

    for year in years:
        if survey_based:
            data_year = data[data["reference_year"] == year].reset_index(drop=True)
        else:
            data_year = data[data["year"] == year].reset_index(drop=True)

        # Define world mean
        world_mean_year = (
            df_main_indicators.loc[
                (df_main_indicators["country"] == "World")
                & (df_main_indicators["year"] == year),
                "mean",
            ].values[0]
            * period_factor
        )

        # Define world median
        world_median_year = (
            df_main_indicators.loc[
                (df_main_indicators["country"] == "World")
                & (df_main_indicators["year"] == year),
                "median",
            ].values[0]
            * period_factor
        )

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

        # Add a vertical line for the international poverty line
        plt.axvline(
            x=ipl,
            color="lightgrey",
            linestyle="--",
            linewidth=0.8,
        )
        plt.text(
            x=ipl,  # x-coordinate for the text
            y=plt.ylim()[1]
            * 0.99,  # y-coordinate for the text, positioned near the top of the plot
            s=f"International Poverty Line: ${round(ipl,2):.2f}",  # Text string to display
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
            # Make the title sentence case
            kde_plot.legend_.set_title(hue.capitalize())
        else:
            # For each plot, write the name of the country at the middle of the distribution, bottom
            for country in hue_order:
                country_data = data_year[data_year[hue] == country]
                year_to_write = country_data["year"].iloc[0] if survey_based else year
                plt.text(
                    x=country_data[x].median() * CORRECTION_FACTOR_LABEL,
                    y=plt.ylim()[0],
                    s=f"{country} ({year_to_write})",
                    color="black",
                    rotation=0,
                    verticalalignment="bottom",
                    fontsize=10,
                )

        if log_scale:
            # Customize x-axis ticks to show 1, 2, 5, 10, 20, 50, 100, etc.
            # kde_plot.set(xscale="log")
            kde_plot.set_xticks(log_ticks)
            kde_plot.get_xaxis().set_major_formatter(plt.ScalarFormatter())

        # Remove y-axis labels and ticks
        kde_plot.set_ylabel("")
        kde_plot.yaxis.set_ticks([])
        kde_plot.set_xlabel(f"Income or consumption ({period})")
        kde_plot.spines["top"].set_visible(False)
        kde_plot.spines["right"].set_visible(False)
        kde_plot.spines["bottom"].set_visible(False)
        kde_plot.spines["left"].set_visible(False)

        fig = kde_plot.get_figure()
        fig.set_size_inches(WIDTH / 100, HEIGHT / 100)
        fig.savefig(
            f"{PARENT_DIR}/{filename}_{year}_survey_{survey_based}_log_{log_scale}_multiple_{multiple}_common_norm_{common_norm}.svg"
        )
        plt.close(fig)

    return None


def distributional_plots_per_row(
    data: pd.DataFrame,
    df_main_indicators: pd.DataFrame,
    x: str,
    weights: str,
    log_scale: bool,
    multiple: str,
    hue: str,
    hue_order: List[str] = None,
    years: List[int] = None,
    common_norm: bool = True,
    period: Literal["day", "month", "year"] = "day",
    survey_based: bool = False,
    preferred_reporting_level: Literal["national", "urban", "rural", None] = None,
    preferred_welfare_type: Literal["income", "consumption", None] = None,
) -> None:
    """
    Plot distributional data with seaborn, with each distribution in a separate row.
    """
    # Filter the data with the hue and hue_order
    if hue_order is not None:
        data = data[data[hue].isin(hue_order)].reset_index(drop=True)

    # If no years are provided, use all years in the data
    if years is None:
        years = list(data["year"].unique())

        # If the dataset is survey-based, filter the data differently
    if survey_based:
        data_reference_year = []
        # Assign a reference year
        for year in years:
            data_reference_year_by_year = data.copy()

            # Assign the reference year
            data_reference_year_by_year["reference_year"] = year

            # Calculate the difference between the reference year and the year
            data_reference_year_by_year["diff_year"] = (
                data_reference_year_by_year["reference_year"]
                - data_reference_year_by_year["year"]
            )

            # By country, select the data with the minimum difference
            data_reference_year_by_year = data_reference_year_by_year.loc[
                data_reference_year_by_year.groupby(
                    ["country", "reporting_level", "welfare_type", "percentile"],
                    observed=True,
                )["diff_year"].idxmin()
            ].reset_index(drop=True)

            # If there are duplicates for the same country in "reporting_level", select preferred_reporting_level if available
            data_reference_year_by_year = data_reference_year_by_year.sort_values(
                by=["reporting_level"],
                key=lambda col: col == preferred_reporting_level,
                ascending=False,
            ).drop_duplicates(
                subset=["country", "welfare_type", "percentile"], keep="first"
            )

            # If there are duplicates for the same country in "welfare_type", select preferred_welfare_tpye if available
            data_reference_year_by_year = data_reference_year_by_year.sort_values(
                by=["welfare_type"],
                key=lambda col: col == preferred_welfare_type,
                ascending=False,
            ).drop_duplicates(
                subset=["country", "reporting_level", "percentile"], keep="first"
            )

            # Resort the data
            data_reference_year_by_year = data_reference_year_by_year.sort_values(
                by=[
                    "country",
                    "year",
                    "reference_year",
                    "reporting_level",
                    "welfare_type",
                    "percentile",
                ]
            )

            # Append the data to the list
            data_reference_year.append(data_reference_year_by_year)

        # Concatenate the data
        data = pd.concat(data_reference_year, ignore_index=True)

    # If the data doesn't come from the survey-based data, use the data as is
    else:
        # Filter data by years
        data = data[data["year"].isin(years)].reset_index(drop=True)

    # Define filename according to the hue_order
    if hue_order is None:
        filename = "all_countries"
    elif len(hue_order) <= 5:
        filename = "_".join(hue_order)
    else:
        filename = "multiple_countries"

    # Define the income period values
    period_factor = PERIOD_VALUES[period]["factor"]
    log_ticks = PERIOD_VALUES[period]["log_ticks"]

    data[x] = data[x] * period_factor

    # Define IPL for the period
    ipl = INTERNATIONAL_POVERTY_LINE * period_factor

    for year in years:
        if survey_based:
            data_year = data[data["reference_year"] == year].reset_index(drop=True)
        else:
            data_year = data[data["year"] == year].reset_index(drop=True)

        # Define world mean
        world_mean_year = (
            df_main_indicators.loc[
                (df_main_indicators["country"] == "World")
                & (df_main_indicators["year"] == year),
                "mean",
            ].values[0]
            * period_factor
        )

        # Define world median
        world_median_year = (
            df_main_indicators.loc[
                (df_main_indicators["country"] == "World")
                & (df_main_indicators["year"] == year),
                "median",
            ].values[0]
            * period_factor
        )

        # Create a figure with subplots for each country
        fig, axes = plt.subplots(
            nrows=len(hue_order),
            ncols=1,
            figsize=(WIDTH / 100, HEIGHT / 100),
            sharex=True,  # Share the x-axis across all subplots
        )

        for ax, country in zip(axes, hue_order):
            country_data = data_year[data_year[hue] == country]

            # Plot a kde with seaborn
            sns.kdeplot(
                data=country_data,
                x=x,
                weights=weights,
                fill=True,
                log_scale=log_scale,
                ax=ax,
                common_norm=common_norm,
            )

            # Add a vertical line for the international poverty line
            ax.axvline(
                x=ipl,
                color="lightgrey",
                linestyle="--",
                linewidth=0.8,
            )

            # Add a vertical line for the world mean
            ax.axvline(
                x=world_mean_year,
                color="lightgrey",
                linestyle="--",
                linewidth=0.8,
            )

            # Add a vertical line for the world median
            ax.axvline(
                x=world_median_year,
                color="lightgrey",
                linestyle="--",
                linewidth=0.8,
            )

            # Add line labels only to the last axis
            if ax == axes[-1]:
                ax.text(
                    x=ipl,
                    y=plt.ylim()[1],
                    s=f"International\nPoverty Line:\n${round(ipl,2):.2f}",
                    color="grey",
                    rotation=90,
                    verticalalignment="top",
                    horizontalalignment="left",
                    fontsize=8,
                )

                ax.text(
                    x=world_mean_year,
                    y=plt.ylim()[1],
                    s=f"World mean:\n${round(world_mean_year,2):.2f}",
                    color="grey",
                    rotation=90,
                    verticalalignment="top",
                    horizontalalignment="left",
                    fontsize=8,
                )

                ax.text(
                    x=world_median_year,
                    y=plt.ylim()[1],
                    s=f"World median:\n${round(world_median_year,2):.2f}",
                    color="grey",
                    rotation=90,
                    verticalalignment="top",
                    horizontalalignment="left",
                    fontsize=8,
                )

            # Add the name of the country at the middle of the distribution, bottom
            year_to_write = country_data["year"].iloc[0] if survey_based else year

            if survey_based:
                # Only plot the country
                ax.text(
                    x=country_data[x].median() * CORRECTION_FACTOR_LABEL,
                    y=ax.get_ylim()[0],
                    s=f"{country}",
                    color="black",
                    rotation=0,
                    verticalalignment="bottom",
                    fontsize=10,
                )
                # Add the year and welfare type to the plot
                reporting_level = country_data["reporting_level"].iloc[0]
                welfare_type = country_data["welfare_type"].iloc[0]

                ax.text(
                    x=data[x].max() * 1.5,
                    y=ax.get_ylim()[0],
                    s=f"{welfare_type.capitalize()} data from {year_to_write}",
                    color="lightgrey",
                    rotation=0,
                    verticalalignment="bottom",
                    fontsize=8,
                )

            else:
                ax.text(
                    x=country_data[x].median() * CORRECTION_FACTOR_LABEL,
                    y=ax.get_ylim()[0],
                    s=f"{country} ({year_to_write})",
                    color="black",
                    rotation=0,
                    verticalalignment="bottom",
                    fontsize=10,
                )

            if log_scale:
                # Customize x-axis ticks to show 1, 2, 5, 10, 20, 50, 100, etc.
                ax.set_xscale("log")
                ax.set_xticks(log_ticks)
                ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())

            # Remove y-axis labels and ticks
            ax.set_ylabel("")
            ax.yaxis.set_ticks([])
            ax.set_xlabel(f"Income or consumption ({period})")
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.spines["bottom"].set_visible(False)
            ax.spines["left"].set_visible(False)

            # Remove x-axis ticks for all axes except the last
            if ax != axes[-1]:
                ax.tick_params(
                    axis="x", which="both", bottom=False, top=False, labelbottom=False
                )

        # Adjust layout and save the figure
        plt.tight_layout()
        fig.savefig(
            f"{PARENT_DIR}/{filename}_{year}_survey_{survey_based}_log_{log_scale}_multiple_{multiple}_common_norm_{common_norm}_rows.svg"
        )
        plt.close(fig)

    return None


if __name__ == "__main__":
    run()
