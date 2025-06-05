from pathlib import Path
from typing import List, Literal

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

PARENT_DIR = Path(__file__).parent.absolute()

# Define International Poverty Line
INTERNATIONAL_POVERTY_LINE = 2.15

# Define poverty line for high-income countries
POVERTY_LINE_HIGH_INCOME = 30

# Define width and height of the plot
WIDTH = 1500
HEIGHT = 750

# For Pen Parade
WIDTH_PEN = 1000
HEIGHT_PEN = 1000

# Define gridsize for when I need higher resolution
GRIDSIZE_HIGHER_RESOLUTION = 1000

# Define pair of countries to estimate data
COUNTRIES = [
    ["Denmark", "Ethiopia"],
    ["Denmark", "Democratic Republic of Congo"],
    ["Denmark", "Kenya"],
    ["Denmark", "Niger"],
    ["Denmark", "Syria"],
    ["United States", "Burundi"],
]

# Define poverty lines to plot areas under the curve in the global distribution
POVERTY_LINES_AREA_GLOBAL = [
    [30],
    [2.15, 10, 30, 100],
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
CORRECTION_FACTOR_LABEL = 1

# Define  version of PIP and 1000 bins data
PIP_VERSION = "2024-10-07"
THOUSAND_BINS_VERSION = "2025-03-10"

# Define URLs

THOUSAND_BINS_URL = f"http://catalog.ourworldindata.org/garden/wb/{THOUSAND_BINS_VERSION}/thousand_bins_distribution/thousand_bins_distribution.feather?nocache"
PERCENTILES_URL = f"http://catalog.ourworldindata.org/garden/wb/{PIP_VERSION}/world_bank_pip/percentiles_income_consumption_2017.feather?nocache"
MAIN_INDICATORS_URL = f"http://catalog.ourworldindata.org/garden/wb/{PIP_VERSION}/world_bank_pip/income_consumption_2017.feather?nocache"

# Define column names and their new names in the national_lines data
NATIONAL_LINES_COLUMNS = {
    "Entity": "country",
    "Year": "year",
    "World Bank income group": "income_group",
    "Harmonized national poverty line": "national_poverty_line",
}


def run() -> None:
    # Read data
    df_thousand_bins = pd.read_feather(THOUSAND_BINS_URL)
    df_percentiles = pd.read_feather(PERCENTILES_URL)
    df_main_indicators = pd.read_feather(MAIN_INDICATORS_URL)
    df_national_lines = pd.read_csv(f"{PARENT_DIR}/national_poverty_lines.csv")

    # Rename columns in the national_lines data
    df_national_lines = df_national_lines.rename(
        columns=NATIONAL_LINES_COLUMNS, errors="raise"
    )

    # Set seaborn style and color palette
    sns.set_style("ticks")
    sns.set_palette("deep")

    # Show texts and not curves for annotations
    plt.rcParams["svg.fonttype"] = "none"

    # Plot global distribution, separating in two with the International Poverty Line
    for lines in POVERTY_LINES_AREA_GLOBAL:
        distributional_plots(
            data=df_percentiles,
            df_main_indicators=df_main_indicators,
            x="thr",
            weights=None,
            log_scale=True,
            multiple="layer",
            hue="country",
            hue_order=["World"],
            years=[2024],
            fill=False,
            legend=True,
            common_norm=False,
            period="day",
            add_ipl=None,
            add_world_mean=None,
            add_world_median=None,
            add_multiple_lines_day=lines,
            gridsize=GRIDSIZE_HIGHER_RESOLUTION,
            width=1500,
            height=400,
        )

    # For UK vs Madagascar data
    distributional_plots(
        data=df_percentiles,
        df_main_indicators=df_main_indicators,
        x="avg",
        weights="pop",
        log_scale=True,
        multiple="layer",
        hue="country",
        hue_order=["Madagascar", "United Kingdom"],
        years=[2024],
        fill=False,
        legend=False,
        common_norm=False,
        period="day",
        add_ipl="area",
        add_world_mean=None,
        add_world_median=None,
        add_multiple_lines_day=None,
        gridsize=GRIDSIZE_HIGHER_RESOLUTION,
        width=1500,
        height=400,
        survey_based=True,
        preferred_reporting_level="national",
        preferred_welfare_type="income",
    )

    # For Chile
    distributional_plots(
        data=df_thousand_bins,
        df_main_indicators=df_main_indicators,
        x="avg",
        weights="pop",
        log_scale=True,
        multiple="layer",
        hue="country",
        hue_order=["Burundi", "Ethiopia", "Syria"],
        years=[2024],
        fill=False,
        legend=True,
        common_norm=False,
        gridsize=GRIDSIZE_HIGHER_RESOLUTION,
        period="day",
        add_ipl="area",
        add_world_mean="area",
        add_world_median="area",
    )

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
            width=1500,
            height=400,
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
            width=1500,
            height=400,
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
            fill=False,
            common_norm=False,
            gridsize=GRIDSIZE_HIGHER_RESOLUTION,
            period="day",
            add_ipl="line",
            add_world_mean="line",
            add_world_median="line",
            add_national_lines=True,
            df_national_lines=df_national_lines,
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
            fill=False,
            common_norm=False,
            gridsize=GRIDSIZE_HIGHER_RESOLUTION,
            period="day",
            survey_based=True,
            preferred_reporting_level="national",
            preferred_welfare_type="income",
            add_ipl="line",
            add_world_mean="line",
            add_world_median="line",
            add_national_lines=True,
            df_national_lines=df_national_lines,
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

    # Pen parades
    pen_parade(
        data=df_percentiles,
        df_main_indicators=df_main_indicators,
        x="percentile",
        y="thr",
        weights=None,
        log_scale=False,
        hue="country",
        hue_order=["World"],
        years=[2024],
        fill=True,
        legend=False,
        add_lines=True,
        period="day",
        survey_based=True,
        preferred_reporting_level="national",
        preferred_welfare_type="income",
    )

    pen_parade(
        data=df_percentiles,
        df_main_indicators=df_main_indicators,
        x="percentile",
        y="thr",
        weights=None,
        log_scale=True,
        hue="country",
        hue_order=["Chile", "Peru", "Uruguay"],
        years=[2024],
        fill=False,
        legend=True,
        add_lines=False,
        period="day",
        survey_based=True,
        preferred_reporting_level="national",
        preferred_welfare_type="income",
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
    fill: bool = True,
    legend: bool = True,
    common_norm: bool = True,
    gridsize: int = 200,
    period: Literal["day", "month", "year"] = "day",
    survey_based: bool = False,
    preferred_reporting_level: Literal["national", "urban", "rural", None] = None,
    preferred_welfare_type: Literal["income", "consumption", None] = None,
    add_ipl: Literal["line", "area", None] = "line",
    add_world_mean: Literal["line", "area", None] = "line",
    add_world_median: Literal["line", "area", None] = "line",
    add_multiple_lines_day: List[float] = None,
    width: int = WIDTH,
    height: int = HEIGHT,
) -> None:
    """
    Plot distributional data with seaborn, with multiple options for customization.
    """

    # Filter the data with the hue and hue_order
    if hue_order is not None:
        data = data[data[hue].isin(hue_order)].reset_index(drop=True)

        # Calculate the number of countries selected
        number_of_countries = len(hue_order)

    # If no years are provided, use all years in the data
    if years is None:
        years = list(data["year"].unique())

    # If the dataset is survey-based, filter the data differently
    if survey_based:
        data = filter_survey_data(
            data=data,
            years=years,
            preferred_reporting_level=preferred_reporting_level,
            preferred_welfare_type=preferred_welfare_type,
        )

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

    # Define multiple_areas, depending on the add_multiple_lines_day
    if add_multiple_lines_day is not None:
        # Define the filename according to the add_multiple_lines_day
        filename_multiple_areas = "_".join(
            [str(round(value, 2)) for value in add_multiple_lines_day]
        )
    else:
        filename_multiple_areas = "none"

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
            fill=fill,
            log_scale=log_scale,
            hue=hue,
            hue_order=hue_order,
            multiple=multiple,
            legend=legend,
            common_norm=common_norm,
            gridsize=gridsize,
        )

        if not fill:
            draw_complete_area_under_curve(
                kde_plot=kde_plot, number_of_countries=number_of_countries
            )

        if add_ipl == "line":
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
        elif add_ipl == "area":
            draw_area_under_curve(
                kde_plot=kde_plot,
                number_of_countries=number_of_countries,
                values=[ipl],
            )

        if add_world_mean == "line":
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

        elif add_world_mean == "area":
            draw_area_under_curve(
                number_of_countries=number_of_countries,
                kde_plot=kde_plot,
                values=[world_mean_year],
            )

        if add_world_median == "line":
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
        elif add_world_median == "area":
            draw_area_under_curve(
                kde_plot=kde_plot,
                number_of_countries=number_of_countries,
                values=[world_median_year],
            )

        if add_multiple_lines_day is not None:
            # Multiply the values by the period factor
            add_multiple_lines_day = [
                value * period_factor for value in add_multiple_lines_day
            ]
            draw_area_under_curve(
                kde_plot=kde_plot,
                number_of_countries=number_of_countries,
                values=add_multiple_lines_day,
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
                    horizontalalignment="center",
                    fontsize=10,
                )

        if log_scale:
            # Customize x-axis ticks to show 1, 2, 5, 10, 20, 50, 100, etc.
            # kde_plot.set(xscale="log")
            kde_plot.set_xticks(log_ticks)
            kde_plot.get_xaxis().set_major_formatter(plt.ScalarFormatter())
        else:
            # Show data in multiples of 10
            kde_plot.set_xticks(range(0, int(data[x].max()) + 10, 10))

        # Remove y-axis labels and ticks
        kde_plot.set_ylabel("")
        kde_plot.yaxis.set_ticks([])
        kde_plot.set_xlabel(f"Income or consumption ({period})")
        kde_plot.spines["top"].set_visible(False)
        kde_plot.spines["right"].set_visible(False)
        kde_plot.spines["bottom"].set_visible(False)
        kde_plot.spines["left"].set_visible(False)

        # Add a base line for each plot in the x axis
        plt.axhline(y=0, color="gray", linewidth=0.5)

        fig = kde_plot.get_figure()

        # Remove the clipping of the figure
        for o in fig.findobj():
            o.set_clip_on(False)

        fig.set_size_inches(width / 100, height / 100)
        fig.savefig(
            f"{PARENT_DIR}/{filename}_{year}_survey_{survey_based}_log_{log_scale}_multiple_{multiple}_common_norm_{common_norm}_multiple_areas_{filename_multiple_areas}.svg",
            bbox_inches="tight",
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
    fill: bool = True,
    common_norm: bool = True,
    gridsize: int = 200,
    period: Literal["day", "month", "year"] = "day",
    survey_based: bool = False,
    preferred_reporting_level: Literal["national", "urban", "rural", None] = None,
    preferred_welfare_type: Literal["income", "consumption", None] = None,
    add_ipl: Literal["line", "area", None] = "line",
    add_world_mean: Literal["line", "area", None] = "line",
    add_world_median: Literal["line", "area", None] = "line",
    add_national_lines: bool = False,
    df_national_lines: pd.DataFrame = None,
    width: int = WIDTH,
    height: int = HEIGHT,
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
        data = filter_survey_data(
            data=data,
            years=years,
            preferred_reporting_level=preferred_reporting_level,
            preferred_welfare_type=preferred_welfare_type,
        )

    # If the data doesn't come from the survey-based data, use the data as is
    else:
        # Filter data by years
        data = data[data["year"].isin(years)].reset_index(drop=True)

    if add_national_lines:
        # Filter national lines data by hue_order
        df_national_lines = df_national_lines[
            df_national_lines[hue].isin(hue_order)
        ].reset_index(drop=True)

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
            figsize=(width / 100, height / 100),
            sharex=True,  # Share the x-axis across all subplots
        )

        for ax, country in zip(axes, hue_order):
            country_data = data_year[data_year[hue] == country]

            # Plot a kde with seaborn
            kde_plot = sns.kdeplot(
                data=country_data,
                x=x,
                weights=weights,
                fill=fill,
                log_scale=log_scale,
                ax=ax,
                common_norm=common_norm,
                gridsize=gridsize,
            )

            if not fill:
                draw_complete_area_under_curve(kde_plot=kde_plot)

            if add_national_lines:
                # Calculate national_poverty_line
                national_poverty_line = df_national_lines.loc[
                    (df_national_lines["country"] == country),
                    "national_poverty_line",
                ].values[0]

                draw_area_under_curve(
                    kde_plot=kde_plot,
                    values=[national_poverty_line],
                )

            if add_ipl == "line":
                # Add a vertical line for the international poverty line
                ax.axvline(
                    x=ipl,
                    color="lightgrey",
                    linestyle="--",
                    linewidth=0.8,
                )

            if add_world_mean == "line":
                # Add a vertical line for the world mean
                ax.axvline(
                    x=world_mean_year,
                    color="lightgrey",
                    linestyle="--",
                    linewidth=0.8,
                )

            if add_world_median == "line":
                # Add a vertical line for the world median
                ax.axvline(
                    x=world_median_year,
                    color="lightgrey",
                    linestyle="--",
                    linewidth=0.8,
                )

            # Add line labels only to the last axis
            if ax == axes[-1]:
                if add_ipl == "line":
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

                if add_world_mean == "line":
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

                if add_world_median == "line":
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
                # Add the year and welfare type to the plot
                reporting_level = country_data["reporting_level"].iloc[0]
                welfare_type = country_data["welfare_type"].iloc[0]

                ax.text(
                    x=data[x].max() * 1.5,
                    y=ax.get_ylim()[0],
                    s=f"{welfare_type.capitalize()} data from {year_to_write}",
                    color="grey",
                    rotation=0,
                    verticalalignment="bottom",
                    fontsize=8,
                )

            # Only plot the country name
            ax.text(
                x=country_data[x].median() * CORRECTION_FACTOR_LABEL,
                y=ax.get_ylim()[0],
                s=f"{country}",
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

            # Add a base line for each plot in the x axis
            ax.axhline(y=0, color="gray", linewidth=0.5)

            # Remove x-axis ticks for all axes except the last
            if ax != axes[-1]:
                ax.tick_params(
                    axis="x", which="both", bottom=False, top=False, labelbottom=False
                )

        # Adjust layout and save the figure
        plt.tight_layout()

        # Remove the clipping of the figure
        for o in fig.findobj():
            o.set_clip_on(False)

        fig.savefig(
            f"{PARENT_DIR}/{filename}_{year}_survey_{survey_based}_log_{log_scale}_multiple_{multiple}_common_norm_{common_norm}_rows.svg",
            bbox_inches="tight",
        )
        plt.close(fig)

    return None


def filter_survey_data(
    data: pd.DataFrame,
    years: List[int],
    preferred_reporting_level: Literal["national", "urban", "rural", None] = None,
    preferred_welfare_type: Literal["income", "consumption", None] = None,
) -> pd.DataFrame:
    """
    Filter survey data by years, to select the most recent data available and preferring preferred_reporting_level and preferred_welfare_type.
    """

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

    return data


def pen_parade(
    data: pd.DataFrame,
    df_main_indicators: pd.DataFrame,
    x: str,
    y: str,
    weights: str,
    log_scale: bool,
    hue: str,
    hue_order: List[str] = None,
    years: List[int] = None,
    fill: bool = False,
    legend: Literal["auto", "brief", "full", False] = "auto",
    add_lines: bool = True,
    period: Literal["day", "month", "year"] = "day",
    survey_based: bool = False,
    preferred_reporting_level: Literal["national", "urban", "rural", None] = None,
    preferred_welfare_type: Literal["income", "consumption", None] = None,
    width: int = WIDTH_PEN,
    height: int = HEIGHT_PEN,
) -> None:
    """
    Plot Pen parades (percentiles vs. income) with seaborn, with multiple options for customization.
    """

    # Filter the data with the hue and hue_order
    if hue_order is not None:
        data = data[data[hue].isin(hue_order)].reset_index(drop=True)

    # If no years are provided, use all years in the data
    if years is None:
        years = list(data["year"].unique())

    # If the dataset is survey-based, filter the data differently
    if survey_based:
        data = filter_survey_data(
            data=data,
            years=years,
            preferred_reporting_level=preferred_reporting_level,
            preferred_welfare_type=preferred_welfare_type,
        )

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

    data[y] = data[y] * period_factor

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

        # Define the % of people below the high-income country poverty line
        world_share_below_high_income_line = df_main_indicators.loc[
            (df_main_indicators["country"] == "World")
            & (df_main_indicators["year"] == year),
            f"headcount_ratio_{POVERTY_LINE_HIGH_INCOME*100:.0f}",
        ].values[0]

        # Define the 90th percentile of the world
        world_90th_percentile = (
            df_main_indicators.loc[
                (df_main_indicators["country"] == "World")
                & (df_main_indicators["year"] == year),
                "decile9_thr",
            ].values[0]
            * period_factor
        )

        # Define the 99th percentile of the world
        world_99th_percentile = (
            df_main_indicators.loc[
                (df_main_indicators["country"] == "World")
                & (df_main_indicators["year"] == year),
                "top1_thr",
            ].values[0]
            * period_factor
        )

        # Create a line plot with seaborn
        line_plot = sns.lineplot(
            data=data_year,
            x=x,
            y=y,
            weights=weights,
            hue=hue,
            hue_order=hue_order,
            legend=legend,
        )

        if fill:
            # Fill the area under the curve
            line_plot.fill_between(
                data=data_year,
                x=x,
                y1=y,
                alpha=0.5,
            )

        if log_scale:
            # Customize y-axis ticks to show 1, 2, 5, 10, 20, 50, 100, etc.
            line_plot.set_yscale("log")
            line_plot.set_yticks(log_ticks)
            line_plot.get_yaxis().set_major_formatter(plt.ScalarFormatter())
        else:
            line_plot.get_yaxis().set_major_formatter(plt.ScalarFormatter())

        if add_lines:
            # Add a horizontal line for the international poverty line
            plt.axhline(
                y=ipl,
                color=sns.color_palette("deep")[3],
                linestyle="--",
                linewidth=0.8,
            )
            plt.text(
                x=99,
                y=ipl,
                s=f"International Poverty Line: ${round(ipl,2):.2f}\n",
                color="black",
                rotation=0,
                horizontalalignment="right",
                fontsize=8,
                linespacing=0.5,
            )

            # Add a horizontal line for the world mean
            plt.axhline(
                y=world_mean_year,
                color=sns.color_palette("deep")[3],
                linestyle="--",
                linewidth=0.8,
            )
            plt.text(
                x=99,
                y=world_mean_year,
                s=f"World mean: ${round(world_mean_year,2):.2f}\n",
                color="black",
                rotation=0,
                horizontalalignment="right",
                fontsize=8,
                linespacing=0.5,
            )

            # Add a horizontal line for the world median
            plt.axhline(
                y=world_median_year,
                color=sns.color_palette("deep")[3],
                linestyle="--",
                linewidth=0.8,
            )
            plt.text(
                x=99,
                y=world_median_year,
                s=f"World median: ${round(world_median_year,2):.2f}\n",
                color="black",
                rotation=0,
                horizontalalignment="right",
                fontsize=8,
                linespacing=0.5,
            )
            plt.text(
                x=0,
                y=world_median_year,
                s=f"The poorest 50% live on less than ${round(world_median_year,2):.2f} a {period}\n",
                color="black",
                rotation=0,
                horizontalalignment="left",
                fontsize=9,
                linespacing=0.5,
            )

            # Add an horizontal line for a poverty line representative of a high-income country
            plt.axhline(
                y=POVERTY_LINE_HIGH_INCOME * period_factor,
                color=sns.color_palette("deep")[3],
                linestyle="-",
                linewidth=1,
            )
            plt.text(
                x=0,
                y=POVERTY_LINE_HIGH_INCOME * period_factor,
                s=f"${round(POVERTY_LINE_HIGH_INCOME * period_factor,2):.0f} corresponds to the poverty line of a high-income country\n",
                color="black",
                rotation=0,
                horizontalalignment="left",
                fontsize=9,
                linespacing=0.5,
            )
            plt.text(
                x=0,
                y=POVERTY_LINE_HIGH_INCOME * period_factor,
                s=f"\nGlobally, {world_share_below_high_income_line/100:.1%} live on less than ${round(POVERTY_LINE_HIGH_INCOME * period_factor,2):.0f} a {period}",
                color="black",
                rotation=0,
                horizontalalignment="left",
                verticalalignment="top",
                fontsize=8,
                linespacing=0.5,
            )

            # Add a horizontal line for the 90th percentile of the world
            plt.axhline(
                y=world_90th_percentile,
                color=sns.color_palette("deep")[3],
                linestyle="--",
                linewidth=0.8,
            )
            plt.text(
                x=99,
                y=world_90th_percentile,
                s=f"${round(world_90th_percentile,2):.2f}\n",
                color="black",
                rotation=0,
                horizontalalignment="right",
                fontsize=8,
                linespacing=0.5,
            )
            plt.text(
                x=99,
                y=world_90th_percentile,
                s=f"\n10% is richer",
                color="black",
                rotation=0,
                horizontalalignment="right",
                verticalalignment="top",
                fontsize=8,
                linespacing=0.5,
            )

            # Add a horizontal line for the 99th percentile of the world
            plt.axhline(
                y=world_99th_percentile,
                color=sns.color_palette("deep")[3],
                linestyle="--",
                linewidth=0.8,
            )
            plt.text(
                x=99,
                y=world_99th_percentile,
                s=f"${round(world_99th_percentile,2):.2f}\n",
                color="black",
                rotation=0,
                horizontalalignment="right",
                fontsize=8,
                linespacing=0.5,
            )
            plt.text(
                x=99,
                y=world_99th_percentile,
                s=f"\n1% is richer",
                color="black",
                rotation=0,
                horizontalalignment="right",
                verticalalignment="top",
                fontsize=8,
                linespacing=0.5,
            )

        # Remove y-axis labels and ticks
        line_plot.set_ylabel("")
        line_plot.yaxis.set_label_position("right")
        line_plot.set_xlabel(f"Percentage of the population")
        line_plot.spines["top"].set_visible(False)
        line_plot.spines["right"].set_visible(False)
        line_plot.spines["bottom"].set_visible(False)
        line_plot.spines["left"].set_visible(False)

        # Change format of x-axis to percentage
        line_plot.get_xaxis().set_major_formatter(
            plt.FuncFormatter(lambda x, _: f"{x/100:.0%}")
        )

        # Do the same for the y-axis, with $
        line_plot.get_yaxis().set_major_formatter(
            plt.FuncFormatter(lambda x, _: f"${x:.0f} per {period}")
        )

        # Make the plot tighter, with the y axis closer to the plot and the x axis being shown between 0 and 100
        line_plot.set_xlim(0, 100)
        line_plot.set_ylim(0, line_plot.get_ylim()[1])

        # Move y axis to the right
        line_plot.yaxis.tick_right()

        # Draw a line for each axis
        line_plot.axhline(y=0, color="black", linewidth=0.5)
        line_plot.axvline(x=100, color="black", linewidth=0.5)

        fig = line_plot.get_figure()

        # Remove the clipping of the figure
        for o in fig.findobj():
            o.set_clip_on(False)

        fig.set_size_inches(width / 100, height / 100)
        fig.savefig(
            f"{PARENT_DIR}/{filename}_{year}_survey_{survey_based}_log_{log_scale}_fill_{fill}_pen.svg",
            bbox_inches="tight",
        )
        plt.close(fig)

    return None


def draw_area_under_curve(
    kde_plot: plt.Axes,
    values: List[float],
    number_of_countries: int = 1,
) -> None:
    """
    Draw the area under the curve for the distributional plots.
    """

    # For each of these countries, in order, highlight the area under the curve
    for i in range(0, number_of_countries):
        for value in values:
            # Obtain the line of the kde_plot
            line = kde_plot.lines[i]

            # Obtain the x and y data of the line
            x_line, y_line = line.get_data()

            # Fill the area under the curve for values below the international poverty line
            kde_plot.fill_between(
                x=x_line,
                y1=y_line,
                where=(x_line <= value),
                alpha=0.3,
                color=line.get_color(),
            )

    return None


def draw_complete_area_under_curve(
    kde_plot: plt.Axes, number_of_countries: int = 1
) -> None:
    """
    Draw the area under the curve for the distributional plots.
    """

    # For each of these countries, in order, highlight the area under the curve
    for i in range(0, number_of_countries):
        # Obtain the line of the kde_plot
        line = kde_plot.lines[i]

        # Obtain the x and y data of the line
        x_line, y_line = line.get_data()

        # Fill the area under the curve for values below the international poverty line
        kde_plot.fill_between(
            x=x_line,
            y1=y_line,
            alpha=0.2,
            color=line.get_color(),
        )

    return None


if __name__ == "__main__":
    run()
