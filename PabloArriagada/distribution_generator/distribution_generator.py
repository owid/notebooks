import textwrap
from pathlib import Path
from typing import List, Literal, cast

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.offsetbox import AnnotationBbox, TextArea, VPacker
from scipy.optimize import minimize
from scipy.stats import norm

PARENT_DIR = Path(__file__).parent.absolute()

# Define International Poverty Line
INTERNATIONAL_POVERTY_LINE = 3

# Define poverty line for high-income countries
POVERTY_LINE_HIGH_INCOME = 30

# PIP PPP version used throughout (filter applied when reading the dimensional tables).
PPP_VERSION = 2021

# Define latest year
LATEST_YEAR = 2026

# Define width and height of the plot
WIDTH = 1500
HEIGHT = 750

# For Pen Parade — roughly 1:1
WIDTH_PEN = 1000
HEIGHT_PEN = 1000

# Color used for reference lines (IPL, World median, $900/$500 lines, country medians, etc.)
REFERENCE_LINE_COLOR = "#6c7a89"


# Define gridsize for when I need higher resolution
GRIDSIZE_HIGHER_RESOLUTION = 1000

# Define pair of countries to estimate data
COUNTRIES = [
    ["Denmark", "Ethiopia"],
    ["Denmark", "Democratic Republic of Congo"],
    ["Denmark", "Madagascar"],
    ["Denmark", "Niger"],
    ["Denmark", "Syria"],
    ["United States", "Burundi"],
]

# Define poverty lines to plot areas under the curve in the global distribution
POVERTY_LINES_AREA_GLOBAL = [
    [30],
    [3, 10, 30, 100],
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

# Version of harmonized national poverty lines (only stale garden dep left; everything else uses external/latest).
NATIONAL_LINES_VERSION = "2025-06-11"

# Define URLs
EXTERNAL_BASE = "http://catalog.ourworldindata.org/external/poverty_inequality/latest"

THOUSAND_BINS_URL = f"{EXTERNAL_BASE}/thousand_bins_distribution/thousand_bins_distribution.feather?nocache"
THOUSAND_BINS_HISTORICAL_URL = f"{EXTERNAL_BASE}/historical_poverty/thousand_bins_interpolated_ginis.feather?nocache"
THOUSAND_BINS_HISTORICAL__ALL_LOGNORMAL_URL = f"{EXTERNAL_BASE}/historical_poverty/thousand_bins_interpolated_ginis_all_lognormal.feather?nocache"

PERCENTILES_URL = f"{EXTERNAL_BASE}/world_bank_pip/percentiles.feather?nocache"
COMPLETE_SERIES_URL = f"{EXTERNAL_BASE}/world_bank_pip/complete_series.feather?nocache"

NATIONAL_LINES_URL = f"http://catalog.ourworldindata.org/garden/wb/{NATIONAL_LINES_VERSION}/harmonized_national_poverty_lines/harmonized_national_poverty_lines.feather?nocache"


def run() -> None:
    # Skipped while iterating on pen parade — re-enable along with the disabled plot blocks below.
    # df_thousand_bins = pd.read_feather(THOUSAND_BINS_URL)
    # df_thousand_bins_historical = pd.read_feather(THOUSAND_BINS_HISTORICAL_URL)
    # df_thousand_bins_historical_all_lognormal = pd.read_feather(
    #     THOUSAND_BINS_HISTORICAL__ALL_LOGNORMAL_URL
    # )
    # df_national_lines = pd.read_feather(NATIONAL_LINES_URL)

    # World Bank PIP dimensional tables → flat shapes the plotting code expects.
    # Percentiles: legacy table was filtered to ppp_version=2021; replicate by filtering here.
    df_percentiles = pd.read_feather(PERCENTILES_URL)
    df_percentiles = df_percentiles[
        df_percentiles["ppp_version"] == PPP_VERSION
    ].reset_index(drop=True)

    # Main indicators (used only for World aggregates): rebuild a flat per-(country, year)
    # frame from complete_series by selecting the right slice for each column family.
    df_complete = pd.read_feather(COMPLETE_SERIES_URL)
    base = (df_complete["ppp_version"] == PPP_VERSION) & (
        df_complete["welfare_type"] == "income or consumption"
    )
    df_summary = df_complete[
        base & df_complete["decile"].isna() & df_complete["poverty_line"].isna()
    ][["country", "year", "mean", "median", "top1_thr"]]
    df_decile9 = df_complete[
        base & (df_complete["decile"] == "9") & df_complete["poverty_line"].isna()
    ][["country", "year", "thr"]].rename(columns={"thr": "decile9_thr"})
    df_pov30 = df_complete[
        base & df_complete["decile"].isna() & (df_complete["poverty_line"] == "3000")
    ][["country", "year", "headcount_ratio"]].rename(
        columns={"headcount_ratio": "headcount_ratio_3000"}
    )
    # PIP stores poverty_line in cents/day, so the IPL ($3/day) is "300".
    df_pov_ipl = df_complete[
        base & df_complete["decile"].isna() & (df_complete["poverty_line"] == "300")
    ][["country", "year", "headcount_ratio"]].rename(
        columns={"headcount_ratio": "headcount_ratio_300"}
    )
    df_main_indicators = (
        df_summary.merge(df_decile9, on=["country", "year"], how="left")
        .merge(df_pov30, on=["country", "year"], how="left")
        .merge(df_pov_ipl, on=["country", "year"], how="left")
    )
    # Add country-level rows for a handful of reference countries. PIP stores each country's
    # smoothed combined series under either welfare_type="income" or "consumption"
    # (whichever the country reports primarily); the combined "income or consumption" label
    # is only used for the World aggregate. Prefer consumption when both are available
    # (PIP's preferred welfare measure for most countries), fall back to income otherwise.
    country_extras = df_complete[
        (df_complete["ppp_version"] == PPP_VERSION)
        & df_complete["welfare_type"].isin(["consumption", "income"])
        & df_complete["decile"].isna()
        & df_complete["poverty_line"].isna()
        & df_complete["country"].isin(
            ["Norway", "United States", "Sweden", "United Kingdom"]
        )
    ][["country", "year", "mean", "median", "top1_thr", "welfare_type"]]
    # "consumption" sorts before "income" alphabetically, so keep="first" prefers consumption.
    country_extras = (
        country_extras.sort_values(["country", "year", "welfare_type"])
        .drop_duplicates(subset=["country", "year"], keep="first")
        .drop(columns="welfare_type")
    )
    df_main_indicators = pd.concat(
        [df_main_indicators, country_extras], ignore_index=True
    )

    # Skipped while iterating on pen parade (no national-lines consumer enabled).
    # df_national_lines.loc[
    #     (df_national_lines["country"] == "United States"),
    #     "harmonized_national_poverty_line",
    # ] = 27.10

    # Set seaborn style and color palette
    sns.set_style("ticks")
    sns.set_palette("deep")

    # Show texts and not curves for annotations
    plt.rcParams["svg.fonttype"] = "none"

    """  # disabled while iterating on pen parade — flip to delete this and the matching closer to re-enable
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
            years=[LATEST_YEAR],
            fill=False,
            legend=True,
            common_norm=False,
            period="day",
            survey_based=False,
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
        years=[LATEST_YEAR],
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
        years=[LATEST_YEAR],
        fill=False,
        legend=True,
        common_norm=False,
        gridsize=GRIDSIZE_HIGHER_RESOLUTION,
        period="day",
        survey_based=False,
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
            years=[LATEST_YEAR],
            legend=True,
            common_norm=False,
            period="day",
            survey_based=False,
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
            years=[LATEST_YEAR],
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
        years=[LATEST_YEAR],
        fill=False,
        common_norm=False,
        gridsize=GRIDSIZE_HIGHER_RESOLUTION,
        period="day",
        survey_based=False,
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
        years=[LATEST_YEAR],
        fill=False,
        common_norm=False,
        gridsize=GRIDSIZE_HIGHER_RESOLUTION,
        period="day",
        survey_based=True,
        preferred_reporting_level="national",
        preferred_welfare_type="income",
        add_ipl="line",
        add_world_mean=None,
        add_world_median=None,
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
        years=[LATEST_YEAR],
        legend=True,
        common_norm=True,
        period="day",
        survey_based=False,
    )
    """  # end of block disabled while iterating on pen parade

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
        years=[LATEST_YEAR],
        fill=True,
        legend=False,
        add_lines=True,
        period="month",
        survey_based=False,
        cut_percentile=95,
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
        years=[LATEST_YEAR],
        fill=False,
        legend=True,
        add_lines=False,
        period="day",
        survey_based=True,
        preferred_reporting_level="national",
        preferred_welfare_type="income",
    )

    """  # disabled while iterating on pen parade — flip to delete this and the matching closer to re-enable
    # Historical data
    distributional_plots(
        data=df_thousand_bins_historical,
        df_main_indicators=None,
        x="avg",
        weights="pop",
        log_scale=True,
        multiple="layer",
        hue="country",
        hue_order=["Sweden"],
        years=[1820, 1920, LATEST_YEAR],
        fill=False,
        legend=False,
        common_norm=False,
        gridsize=GRIDSIZE_HIGHER_RESOLUTION,
        period="day",
        survey_based=False,
        add_ipl=None,
        add_world_mean=None,
        add_world_median=None,
        add_multiple_lines_day=[3, 30],
        x_axis_range=(0.05, 300),
        width=1150,
        height=220,
    )

    distributional_plots(
        data=df_thousand_bins_historical_all_lognormal,
        df_main_indicators=None,
        x="avg",
        weights="pop",
        log_scale=True,
        multiple="layer",
        hue="country",
        hue_order=["Sweden"],
        years=[LATEST_YEAR],
        fill=False,
        legend=False,
        common_norm=False,
        gridsize=GRIDSIZE_HIGHER_RESOLUTION,
        period="day",
        survey_based=False,
        add_ipl=None,
        add_world_mean=None,
        add_world_median=None,
        add_multiple_lines_day=[3, 30],
        x_axis_range=(0.05, 300),
        width=1150,
        height=220,
    )
    """  # end of block disabled while iterating on pen parade

    # # For synthetic data

    # (
    #     synthetic_data_uk_gapminder,
    #     generated_mean_uk_gapminder,
    #     generated_gini_uk_gapminder,
    #     target_mean_uk_gapminder,
    #     target_gini_uk_gapminder,
    # ) = generate_synthetic_data_from_mean_gini(
    #     country="United Kingdom-Gapminder",
    #     year=1820,
    #     target_mean=3784.226727,
    #     target_gini=0.5845,
    # )

    # (
    #     synthetic_data_uk_moatsos,
    #     generated_mean_uk_moatsos,
    #     generated_gini_uk_moatsos,
    #     target_mean_uk_moatsos,
    #     target_gini_uk_moatsos,
    # ) = generate_synthetic_data_from_mean_gini(
    #     country="United Kingdom-Moatsos",
    #     year=1820,
    #     target_mean=1250.072,
    #     target_gini=0.5927,
    # )
    # (
    #     synthetic_data_uk_mpd_gapminder,
    #     generated_mean_uk_mpd_gapminder,
    #     generated_gini_uk_mpd_gapminder,
    #     target_mean_uk_mpd_gapminder,
    #     target_gini_uk_mpd_gapminder,
    # ) = generate_synthetic_data_from_mean_gini(
    #     country="United Kingdom-MPD-Gapminder",
    #     year=1820,
    #     target_mean=3306,
    #     target_gini=0.5845,
    # )
    # (
    #     synthetic_data_uk_mpd_moatsos,
    #     generated_mean_uk_mpd_moatsos,
    #     generated_gini_uk_mpd_moatsos,
    #     target_mean_uk_mpd_moatsos,
    #     target_gini_uk_mpd_moatsos,
    # ) = generate_synthetic_data_from_mean_gini(
    #     country="United Kingdom-MPD-Moatsos",
    #     year=1820,
    #     target_mean=3306,
    #     target_gini=0.5927,
    # )

    # (
    #     synthetic_data_sweden_gapminder,
    #     generated_mean_sweden_gapminder,
    #     generated_gini_sweden_gapminder,
    #     target_mean_sweden_gapminder,
    #     target_gini_sweden_gapminder,
    # ) = generate_synthetic_data_from_mean_gini(
    #     country="Sweden-Gapminder",
    #     year=1820,
    #     target_mean=1619.685668,
    #     target_gini=0.4956,
    # )
    # (
    #     synthetic_data_sweden_moatsos,
    #     generated_mean_sweden_moatsos,
    #     generated_gini_sweden_moatsos,
    #     target_mean_sweden_moatsos,
    #     target_gini_sweden_moatsos,
    # ) = generate_synthetic_data_from_mean_gini(
    #     country="Sweden-Moatsos",
    #     year=1820,
    #     target_mean=445.4332,
    #     target_gini=0.5544166,
    # )
    # (
    #     synthetic_data_sweden_mpd_gapminder,
    #     generated_mean_sweden_mpd_gapminder,
    #     generated_gini_sweden_mpd_gapminder,
    #     target_mean_sweden_mpd_gapminder,
    #     target_gini_sweden_mpd_gapminder,
    # ) = generate_synthetic_data_from_mean_gini(
    #     country="Sweden-MPD-Gapminder",
    #     year=1820,
    #     target_mean=1415,
    #     target_gini=0.4956,
    # )
    # (
    #     synthetic_data_sweden_mpd_moatsos,
    #     generated_mean_sweden_mpd_moatsos,
    #     generated_gini_sweden_mpd_moatsos,
    #     target_mean_sweden_mpd_moatsos,
    #     target_gini_sweden_mpd_moatsos,
    # ) = generate_synthetic_data_from_mean_gini(
    #     country="Sweden-MPD-Moatsos",
    #     year=1820,
    #     target_mean=1415,
    #     target_gini=0.5544166,
    # )

    # distributional_plots(
    #     data=synthetic_data_uk_gapminder,
    #     df_main_indicators=None,
    #     x="avg",
    #     weights=None,
    #     log_scale=True,
    #     multiple="layer",
    #     hue="country",
    #     hue_order=["United Kingdom-Gapminder"],
    #     years=[1820],
    #     fill=False,
    #     legend=False,
    #     common_norm=False,
    #     period="day",
    #     add_ipl=None,
    #     add_world_mean=None,
    #     add_world_median=None,
    #     add_multiple_lines_day=[2.15 * 365],
    #     gridsize=GRIDSIZE_HIGHER_RESOLUTION,
    #     width=1500,
    #     height=400,
    #     survey_based=False,
    #     add_fade_in_tails=False,
    # )

    # distributional_plots(
    #     data=synthetic_data_sweden_mpd_moatsos,
    #     df_main_indicators=None,
    #     x="avg",
    #     weights=None,
    #     log_scale=True,
    #     multiple="layer",
    #     hue="country",
    #     hue_order=["Sweden-MPD-Moatsos"],
    #     years=[1820],
    #     fill=False,
    #     legend=False,
    #     common_norm=False,
    #     period="day",
    #     add_ipl=None,
    #     add_world_mean=None,
    #     add_world_median=None,
    #     add_multiple_lines_day=[1.90 * 365],
    #     gridsize=GRIDSIZE_HIGHER_RESOLUTION,
    #     width=1500,
    #     height=400,
    #     survey_based=False,
    #     add_fade_in_tails=False,
    # )


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
    add_fade_in_tails: bool = True,
    percentiles_to_fade: List[float] = [1, 99],
    x_axis_range: tuple = None,
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

        if df_main_indicators is not None:
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

        # Define values of percentiles
        if add_fade_in_tails:
            # Check if the dataframe has a percentile or a quantile column
            if "percentile" in data_year.columns:
                percentile_or_quantile = "percentile"
                percentiles_quantiles_to_fade = percentiles_to_fade
            elif "quantile" in data_year.columns:
                percentile_or_quantile = "quantile"

                # Divide values in percentiles_to_fade by 10
                percentiles_quantiles_to_fade = [p * 10 for p in percentiles_to_fade]
            else:
                raise KeyError(
                    "Expected either 'percentile' or 'quantile' column in data_year"
                )

            data_year = data_year[
                (data_year[percentile_or_quantile] > percentiles_quantiles_to_fade[0])
                & (data_year[percentile_or_quantile] < percentiles_quantiles_to_fade[1])
            ]

        # Filter data by x_axis_range if specified
        # This ensures KDE calculation only uses data within the specified range
        if x_axis_range is not None:
            data_year = data_year[
                (data_year[x] >= x_axis_range[0]) & (data_year[x] <= x_axis_range[1])
            ].reset_index(drop=True)

        # Determine clip parameter for KDE
        # When log_scale=True, KDE is computed in log-space, so clip needs log-transformed values
        if x_axis_range is not None and log_scale:
            clip_param = (np.log(x_axis_range[0]), np.log(x_axis_range[1]))
        else:
            clip_param = x_axis_range

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
            clip=clip_param,
        )

        # Set x-axis range immediately after plotting, before drawing areas
        # This ensures all subsequent drawing operations respect the axis limits
        if x_axis_range is not None:
            kde_plot.set_xlim(x_axis_range[0], x_axis_range[1])
            # Also set margins to 0 to prevent automatic padding
            plt.margins(x=0)

        if not fill:
            draw_complete_area_under_curve(
                kde_plot=kde_plot, number_of_countries=number_of_countries
            )

        if add_ipl == "line":
            # Add a vertical line for the international poverty line
            plt.axvline(
                x=ipl,
                color="lightgrey",
                linestyle=":",
                linewidth=0.8,
            )
            plt.text(
                x=ipl,  # x-coordinate for the text
                y=plt.ylim()[1]
                * 0.99,  # y-coordinate for the text, positioned near the top of the plot
                s=f"International Poverty Line: ${round(ipl, 2):.2f}",  # Text string to display
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
                linestyle=":",
                linewidth=0.8,
            )
            plt.text(
                x=world_mean_year,
                y=plt.ylim()[1] * 0.99,
                s=f"World mean: ${round(world_mean_year, 2):.2f}",
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
                linestyle=":",
                linewidth=0.8,
            )
            plt.text(
                x=world_median_year,
                y=plt.ylim()[1] * 0.99,
                s=f"World median: ${round(world_median_year, 2):.2f}",
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
            # Filter ticks to only include values within x_axis_range if specified
            if x_axis_range is not None:
                filtered_ticks = [
                    tick
                    for tick in log_ticks
                    if x_axis_range[0] <= tick <= x_axis_range[1]
                ]
                kde_plot.set_xticks(filtered_ticks)
            else:
                kde_plot.set_xticks(log_ticks)
            # Add dollar sign prefix to tick labels with integer formatting
            kde_plot.get_xaxis().set_major_formatter(
                plt.FuncFormatter(lambda x, p: f"${x:.0f}")
            )
        else:
            # Show data in multiples of 10
            kde_plot.set_xticks(range(0, int(data[x].max()) + 10, 10))
            # Add dollar sign prefix to tick labels with integer formatting
            kde_plot.get_xaxis().set_major_formatter(
                plt.FuncFormatter(lambda x, p: f"${x:.0f}")
            )

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

        # When using fixed axis range, use fixed subplot adjustments for perfect alignment
        if x_axis_range is not None:
            plt.subplots_adjust(left=0.04, right=0.96, top=0.95, bottom=0.22)

        # Use bbox_inches="tight" only when x_axis_range is not specified
        # to maintain alignment when using fixed axis ranges
        save_kwargs = {} if x_axis_range is not None else {"bbox_inches": "tight"}
        fig.savefig(
            f"{PARENT_DIR}/{filename}_{year}_survey_{survey_based}_log_{log_scale}_multiple_{multiple}_common_norm_{common_norm}_multiple_areas_{filename_multiple_areas}.svg",
            **save_kwargs,
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
    add_fade_in_tails: bool = True,
    percentiles_to_fade: List[float] = [1, 99],
    x_axis_range: tuple = None,
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

            # Define values of percentiles
            if add_fade_in_tails:
                # Check if the dataframe has a percentile or a quantile column
                if "percentile" in country_data.columns:
                    percentile_or_quantile = "percentile"
                    percentiles_quantiles_to_fade = percentiles_to_fade
                elif "quantile" in country_data.columns:
                    percentile_or_quantile = "quantile"

                    # Divide values in percentiles_to_fade by 10
                    percentiles_quantiles_to_fade = [
                        p * 10 for p in percentiles_to_fade
                    ]
                else:
                    raise KeyError(
                        "Expected either 'percentile' or 'quantile' column in country_data"
                    )

                country_data = country_data[
                    (
                        country_data[percentile_or_quantile]
                        > percentiles_quantiles_to_fade[0]
                    )
                    & (
                        country_data[percentile_or_quantile]
                        < percentiles_quantiles_to_fade[1]
                    )
                ]

            # Filter data by x_axis_range if specified
            # This ensures KDE calculation only uses data within the specified range
            if x_axis_range is not None:
                country_data = country_data[
                    (country_data[x] >= x_axis_range[0])
                    & (country_data[x] <= x_axis_range[1])
                ].reset_index(drop=True)

            # Determine clip parameter for KDE
            # When log_scale=True, KDE is computed in log-space, so clip needs log-transformed values
            if x_axis_range is not None and log_scale:
                clip_param = (np.log(x_axis_range[0]), np.log(x_axis_range[1]))
            else:
                clip_param = x_axis_range

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
                clip=clip_param,
            )

            # Set x-axis range immediately after plotting, before drawing areas
            # This ensures all subsequent drawing operations respect the axis limits
            if x_axis_range is not None:
                ax.set_xlim(x_axis_range[0], x_axis_range[1])
                # Also set margins to 0 to prevent automatic padding
                ax.margins(x=0)

            if not fill:
                draw_complete_area_under_curve(kde_plot=kde_plot)

            if add_national_lines:
                # Calculate national_poverty_line
                national_poverty_line = df_national_lines.loc[
                    (df_national_lines["country"] == country),
                    "harmonized_national_poverty_line",
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
                    linestyle=":",
                    linewidth=0.8,
                )

            if add_world_mean == "line":
                # Add a vertical line for the world mean
                ax.axvline(
                    x=world_mean_year,
                    color="lightgrey",
                    linestyle=":",
                    linewidth=0.8,
                )

            if add_world_median == "line":
                # Add a vertical line for the world median
                ax.axvline(
                    x=world_median_year,
                    color="lightgrey",
                    linestyle=":",
                    linewidth=0.8,
                )

            if add_national_lines:
                # Add a vertical line for the national poverty line
                ax.text(
                    x=national_poverty_line,
                    y=plt.ylim()[0] - 0.05 * (plt.ylim()[1] - plt.ylim()[0]),
                    s=f"${round(national_poverty_line, 2):.2f} The poverty line in {country}*",
                    color="grey",
                    rotation=0,
                    verticalalignment="top",
                    horizontalalignment="left",
                    fontsize=8,
                )

            # Add line labels only to the last axis
            if ax == axes[-1]:
                if add_ipl == "line":
                    ax.text(
                        x=ipl,
                        y=plt.ylim()[1],
                        s=f"International\nPoverty Line:\n${round(ipl, 2):.2f}",
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
                        s=f"World mean:\n${round(world_mean_year, 2):.2f}",
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
                        s=f"World median:\n${round(world_median_year, 2):.2f}",
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
                # Filter ticks to only include values within x_axis_range if specified
                if x_axis_range is not None:
                    filtered_ticks = [
                        tick
                        for tick in log_ticks
                        if x_axis_range[0] <= tick <= x_axis_range[1]
                    ]
                    ax.set_xticks(filtered_ticks)
                else:
                    ax.set_xticks(log_ticks)
                # Add dollar sign prefix to tick labels with integer formatting
                ax.get_xaxis().set_major_formatter(
                    plt.FuncFormatter(lambda x, p: f"${x:.0f}")
                )
            else:
                # Add dollar sign prefix to tick labels with integer formatting for non-log scale
                ax.get_xaxis().set_major_formatter(
                    plt.FuncFormatter(lambda x, p: f"${x:.0f}")
                )

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
        if x_axis_range is not None:
            # Use fixed subplot adjustments for perfect alignment
            plt.subplots_adjust(left=0.04, right=0.96, top=0.98, bottom=0.20)
        else:
            plt.tight_layout()

        # Remove the clipping of the figure
        for o in fig.findobj():
            o.set_clip_on(False)

        # Use bbox_inches="tight" only when x_axis_range is not specified
        # to maintain alignment when using fixed axis ranges
        save_kwargs = {} if x_axis_range is not None else {"bbox_inches": "tight"}
        fig.savefig(
            f"{PARENT_DIR}/{filename}_{year}_survey_{survey_based}_log_{log_scale}_multiple_{multiple}_common_norm_{common_norm}_rows.svg",
            **save_kwargs,
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


def interpolate_x_at_y(xs: np.ndarray, ys: np.ndarray, y_target: float) -> float | None:
    """
    Return the x at which a piecewise-linear curve defined by (xs, ys) first
    reaches y_target, by linearly interpolating between the two flanking points.
    Returns None if the curve never reaches y_target.

    Assumes xs is sorted ascending. Used by the pen parade to land bracket end-caps
    and dotted reference lines exactly on the curve, instead of snapping to the
    nearest integer-percentile data point.
    """
    crossings = ys >= y_target
    if not crossings.any():
        return None
    i_hi = int(np.argmax(crossings))
    if i_hi == 0:
        return float(xs[0])
    y_lo, y_hi_val = ys[i_hi - 1], ys[i_hi]
    x_lo, x_hi = xs[i_hi - 1], xs[i_hi]
    if y_hi_val == y_lo:
        return float(x_hi)
    return float(x_lo + (y_target - y_lo) * (x_hi - x_lo) / (y_hi_val - y_lo))


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
    cut_percentile: float = 100,
) -> None:
    """
    Plot Pen parades (percentiles vs. income) with seaborn, with multiple options for customization.

    ``cut_percentile`` truncates the x-axis at the given percentile (default 95) so the
    rapidly rising top tail doesn't dominate the y-axis. Reference lines whose y-value sits
    above the visible range (e.g. the 99th-percentile threshold when ``cut_percentile=95``)
    are skipped automatically.
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

    # Define the income period values. PERIOD_VALUES mixes int factors with list
    # log_ticks under the same dict, so cast each lookup back to its concrete type.
    period_factor = cast(int, PERIOD_VALUES[period]["factor"])
    log_ticks = cast(List[int], PERIOD_VALUES[period]["log_ticks"])
    # Show cents only for daily figures; monthly/yearly values are large enough that decimals are noise.
    dollar_decimals = 2 if period == "day" else 0

    data[y] = data[y] * period_factor

    # Define IPL for the period
    ipl = INTERNATIONAL_POVERTY_LINE * period_factor

    for year in years:
        if survey_based:
            data_year = data[data["reference_year"] == year].reset_index(drop=True)
        else:
            data_year = data[data["year"] == year].reset_index(drop=True)

        # Anchor each per-hue line at (x=0, y=0) so the curve starts at the origin instead
        # of at percentile=1. Skipped on log-scale because log(0) = -inf would blank the
        # plot (the line/fill points get clipped and nothing renders).
        if len(data_year) > 0 and not log_scale:
            zero_rows = data_year.drop_duplicates(subset=[hue]).copy()
            zero_rows[x] = 0
            zero_rows[y] = 0
            data_year = pd.concat(
                [zero_rows, data_year], ignore_index=True
            ).reset_index(drop=True)

        # Compute the y-value at cut_percentile (used to set the y-axis cap and to anchor
        # the p99 annotation). Keep ALL x rows so the curve spans the full x range, and
        # CLAMP y values above the cut to y_at_cut so the curve plateaus at the top rather
        # than disappearing (or relying on axes clipping, which we keep disabled globally
        # for Figma editing). Also extend the plateau to x=100 so the cap line reaches the
        # right edge of the chart, even when the source data tops out at percentile 99.
        if cut_percentile < 100 and len(data_year) > 0:
            cut_subset = data_year[data_year[x] <= cut_percentile]
            y_at_cut = float(cut_subset[y].max()) if len(cut_subset) else None
            # Fade band runs from 88% of the cap up to the cap.
            y_at_fade_floor = y_at_cut * 0.88 if y_at_cut is not None else None
            if y_at_cut is not None:
                data_year = data_year.copy()
                data_year.loc[data_year[y] > y_at_cut, y] = y_at_cut
                plateau_end = data_year.drop_duplicates(
                    subset=[hue], keep="last"
                ).copy()
                plateau_end[x] = 100
                plateau_end[y] = y_at_cut
                data_year = pd.concat(
                    [data_year, plateau_end], ignore_index=True
                ).reset_index(drop=True)
        else:
            y_at_cut = None
            y_at_fade_floor = None

        # Keep raw float values for POSITIONING (bracket caps, dotted reference lines,
        # and fill crossings all land on the curve at the semantically meaningful
        # percentile — e.g. the world median ends up at p=50, not p≈49.93). The
        # f-string `.{dollar_decimals}f` formatting in each label rounds for DISPLAY
        # (e.g. $289.50 → "$289"), so labels still match the rounded numbers shown
        # elsewhere in OWID's online data.

        # Define world mean
        world_mean_year = float(
            df_main_indicators.loc[
                (df_main_indicators["country"] == "World")
                & (df_main_indicators["year"] == year),
                "mean",
            ].values[0]
            * period_factor
        )

        # Define world median
        world_median_year = float(
            df_main_indicators.loc[
                (df_main_indicators["country"] == "World")
                & (df_main_indicators["year"] == year),
                "median",
            ].values[0]
            * period_factor
        )

        # Define the 90th percentile of the world
        world_90th_percentile = float(
            df_main_indicators.loc[
                (df_main_indicators["country"] == "World")
                & (df_main_indicators["year"] == year),
                "decile9_thr",
            ].values[0]
            * period_factor
        )

        # Define the 99th percentile of the world
        world_99th_percentile = float(
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
            linewidth=2.5,
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

        # Reference-line ticks collected here become the y-axis tick labels, replacing the
        # default dollar-amount labels with the labels that previously sat on each reference line.
        reference_ticks: list[tuple[float, str]] = []

        if add_lines:
            # Sorted (x, y) arrays for the curve — shared by the fill polygons,
            # axhline_over_curve, and the bracket loop so they all interpolate
            # against the same data.
            ref_sorted = data_year.sort_values(x).reset_index(drop=True)
            ref_xs = ref_sorted[x].to_numpy()
            ref_ys = ref_sorted[y].to_numpy()

            # Poverty bands shaded in the same blue as the main fill — one per poverty
            # line where the curve sits below that threshold. Overlapping fills stack
            # their alphas, deepening the blue as the poverty line gets stricter.
            # We build each polygon with the exact crossing point appended, because
            # matplotlib's fill_between `interpolate=True` only kicks in when y1 and
            # y2 actually cross — with y1=0 the curves never meet, so the fill would
            # otherwise snap to the last integer percentile instead of the crossing.
            poverty_fill_color = sns.color_palette("deep")[0]
            for poverty_y in (
                POVERTY_LINE_HIGH_INCOME * period_factor,
                world_median_year,
                ipl,
            ):
                x_cross = interpolate_x_at_y(ref_xs, ref_ys, float(poverty_y))
                if x_cross is None:
                    continue
                below_mask = ref_ys < poverty_y
                fill_xs = np.concatenate([ref_xs[below_mask], [x_cross]])
                fill_ys = np.concatenate([ref_ys[below_mask], [poverty_y]])
                line_plot.fill_between(
                    fill_xs,
                    0,
                    fill_ys,
                    alpha=0.3,
                    color=poverty_fill_color,
                    linewidth=0,
                )

            def axhline_over_curve(y_value):
                """Dotted reference line at y_value, but only over the filled curve
                area (from where the curve crosses y_value to the right edge), so the
                line doesn't clutter the white space where the brackets live. The
                crossing x is interpolated so the dotted line meets the curve exactly,
                rather than snapping to the next integer percentile."""
                crossing_x = interpolate_x_at_y(ref_xs, ref_ys, y_value)
                xmin_frac = 0.0 if crossing_x is None else crossing_x / 100.0
                plt.axhline(
                    y=y_value,
                    xmin=xmin_frac,
                    color=REFERENCE_LINE_COLOR,
                    linestyle=":",
                    linewidth=0.8,
                )

            # International poverty line
            axhline_over_curve(ipl)
            reference_ticks.append((ipl, f"← ${ipl:.{dollar_decimals}f} per {period}"))

            # Reference lines at the equivalent of $900/month and $500/month, in the
            # chart's current period units. Defined in monthly terms then rescaled by
            # period_factor / month_factor so the same real-world amounts shift correctly
            # when the chart switches between day / month / year periods.
            month_factor = cast(int, PERIOD_VALUES["month"]["factor"])
            for monthly_value in (900, 500):
                line_y = monthly_value * period_factor / month_factor
                axhline_over_curve(line_y)
                reference_ticks.append(
                    (line_y, f"← ${line_y:.{dollar_decimals}f} per {period}")
                )

            # World median
            axhline_over_curve(world_median_year)
            reference_ticks.append(
                (
                    world_median_year,
                    f"← ${world_median_year:.{dollar_decimals}f} per {period} — the global median income",
                )
            )
            # 90th percentile of the world
            axhline_over_curve(world_90th_percentile)
            reference_ticks.append(
                (
                    world_90th_percentile,
                    f"← The richest 10% have an income of more than ${world_90th_percentile:.{dollar_decimals}f} per {period}",
                )
            )

            # 99th percentile of the world.
            # If the chart was cut below percentile 99, the 99th threshold sits above the
            # visible y range — draw the label above the cropped top of the chart, anchored
            # at x = cut_percentile (the right edge of the visible plot), as in the reference.
            p99_label = f"↑ The richest 1% live on more than ${world_99th_percentile:.{dollar_decimals}f} per {period}"
            if cut_percentile < 99:
                wrapped_p99 = textwrap.fill(p99_label, width=28)
                # Anchor at the top-right of the axes so the label sits in the same
                # right-margin column as the other y-tick labels, just above the topmost
                # tick. ha="left" + a small +x offset mirror the default tick-label pad.
                line_plot.annotate(
                    wrapped_p99,
                    xy=(1.0, 1.0),
                    xycoords="axes fraction",
                    xytext=(4, 4),
                    textcoords="offset points",
                    ha="left",
                    va="bottom",
                    fontsize=8,
                    linespacing=1.5,
                    annotation_clip=False,
                )
            else:
                axhline_over_curve(world_99th_percentile)
                reference_ticks.append(
                    (world_99th_percentile, p99_label.replace("↑", "→"))
                )

            # Country median reference lines (most-recent value at or before the plot year).
            # Pairs in COUNTRY_MEDIAN_MERGE_PAIRS that fall within MEDIAN_MERGE_TOLERANCE of
            # each other are averaged into a single line; otherwise we assert so the chart
            # author notices the divergence and decides how to lay them out.
            COUNTRY_MEDIAN_MERGE_PAIRS = [("Sweden", "United Kingdom")]
            MEDIAN_MERGE_TOLERANCE = 0.05  # 5%
            # Display names: PIP's full country names → the shorter forms we want shown
            # in the labels. Countries not listed fall back to their PIP name.
            COUNTRY_DISPLAY_NAMES = {
                "United States": "the USA",
                "United Kingdom": "the UK",
            }

            def display_name(country: str) -> str:
                return COUNTRY_DISPLAY_NAMES.get(country, country)

            country_medians_lookup = {}
            for country_name in ["Norway", "United States", "Sweden", "United Kingdom"]:
                country_rows = df_main_indicators[
                    (df_main_indicators["country"] == country_name)
                    & (df_main_indicators["year"] <= year)
                    & df_main_indicators["median"].notna()
                ]
                if country_rows.empty:
                    continue
                country_medians_lookup[country_name] = float(
                    country_rows.sort_values("year")["median"].iloc[-1] * period_factor
                )

            merged_country_labels = set()
            merged_groups: list[tuple[float, list[str]]] = []
            for a, b in COUNTRY_MEDIAN_MERGE_PAIRS:
                if a not in country_medians_lookup or b not in country_medians_lookup:
                    continue
                med_a = country_medians_lookup[a]
                med_b = country_medians_lookup[b]
                relative_diff = abs(med_a - med_b) / max(med_a, med_b)
                assert relative_diff <= MEDIAN_MERGE_TOLERANCE, (
                    f"Country medians for {a} (${med_a:.2f}) and {b} (${med_b:.2f}) differ by "
                    f"{relative_diff:.1%}, exceeding the {MEDIAN_MERGE_TOLERANCE:.0%} merge "
                    f"tolerance. Adjust COUNTRY_MEDIAN_MERGE_PAIRS or lay them out separately."
                )
                merged_groups.append(((med_a + med_b) / 2, [a, b]))
                merged_country_labels.update({a, b})

            for country_name, country_median in country_medians_lookup.items():
                if country_name in merged_country_labels:
                    continue
                axhline_over_curve(country_median)
                reference_ticks.append(
                    (
                        country_median,
                        f"← ${country_median:.{dollar_decimals}f} per {period} — the median income in {display_name(country_name)}",
                    )
                )

            for group_median, group_countries in merged_groups:
                group_label = " and ".join(display_name(c) for c in group_countries)
                # If this merged country median is also within MEDIAN_MERGE_TOLERANCE of the
                # world's 90th percentile, combine the two into a single reference label
                # (and replace the existing p90 tick instead of adding a duplicate).
                p90_diff = abs(group_median - world_90th_percentile) / max(
                    group_median, world_90th_percentile
                )
                if p90_diff <= MEDIAN_MERGE_TOLERANCE:
                    # Reuse the existing p90 axhline (already drawn) — don't add another at
                    # the merged y, otherwise two near-identical lines would overlap.
                    combined_value = world_90th_percentile
                    combined_label = (
                        f"← ${combined_value:.{dollar_decimals}f} per {period} — "
                        f"the median income in {group_label}, and the income above "
                        f"which the richest 10% of the world live"
                    )
                    # Replace the existing p90 tick (matched by "richest 10%" fragment).
                    for idx, (_, label_text) in enumerate(reference_ticks):
                        if "richest 10%" in label_text:
                            reference_ticks[idx] = (combined_value, combined_label)
                            break
                    continue
                axhline_over_curve(group_median)
                reference_ticks.append(
                    (
                        group_median,
                        f"← ${group_median:.{dollar_decimals}f} per {period} — the median income in {group_label}",
                    )
                )

            # Red square brackets ([) ABOVE selected reference lines, spanning from x=0
            # out to where the curve crosses that y value — a simple bracket with vertical
            # end-caps and a flat top, marking the share of the world earning less than
            # each threshold.
            brace_values = [
                ipl,
                world_median_year,
                POVERTY_LINE_HIGH_INCOME * period_factor,
            ]
            y_range = y_at_cut if y_at_cut is not None else line_plot.get_ylim()[1]
            brace_height_data = y_range * 0.012  # height of the bracket

            red = sns.color_palette("deep")[3]

            def styled_annotation(x, y, title, text, box_alignment, wrap_width=32):
                """Multi-line annotation: bold title on top, regular text below. The
                `text` is auto-wrapped at `wrap_width` characters (preserving any explicit
                ``\\n`` you do add). All lines are right-aligned within the box so their
                right edges sit flush against the y-axis."""
                common = {
                    "color": red,
                    "fontsize": 9,
                    "ha": "right",
                    "multialignment": "right",
                }
                children = [TextArea(title, textprops={**common, "fontweight": "bold"})]
                wrapped_lines = []
                for raw in text.split("\n"):
                    wrapped_lines.extend(
                        textwrap.fill(raw, width=wrap_width).split("\n")
                    )
                for line in wrapped_lines:
                    children.append(TextArea(line, textprops=common))
                packer = VPacker(children=children, align="right", pad=0, sep=2)
                line_plot.add_artist(
                    AnnotationBbox(
                        packer,
                        (x, y),
                        xycoords="data",
                        xybox=(-5, 0),
                        boxcoords="offset points",
                        box_alignment=box_alignment,
                        frameon=False,
                        pad=0,
                    )
                )

            high_income_value = POVERTY_LINE_HIGH_INCOME * period_factor
            for brace_y in brace_values:
                # Interpolate so the bracket's right cap lands exactly where the
                # curve crosses brace_y, rather than snapping to the next integer
                # percentile (which would leave a visible gap).
                x_brace_end = interpolate_x_at_y(ref_xs, ref_ys, brace_y)
                if x_brace_end is None or x_brace_end <= 1:
                    continue
                y_low = brace_y
                y_high = brace_y + brace_height_data
                bx = [0.0, 0.0, x_brace_end, x_brace_end]
                by = [y_low, y_high, y_high, y_low]
                line_plot.plot(
                    bx,
                    by,
                    color=sns.color_palette("deep")[3],
                    linewidth=1.5,
                    clip_on=False,
                    solid_capstyle="butt",
                    solid_joinstyle="miter",
                )
                # Annotate the high-income bracket with the headcount share at $X.
                if brace_y == high_income_value:
                    world_share_hi = df_main_indicators.loc[
                        (df_main_indicators["country"] == "World")
                        & (df_main_indicators["year"] == year),
                        "headcount_ratio_3000",
                    ].values[0]
                    styled_annotation(
                        0,
                        y_high,
                        title="Poverty",
                        text=f"{world_share_hi:.0f}% of the world population live on less than ${brace_y:.0f} per {period}",
                        box_alignment=(1.0, 0.0),
                    )
                if brace_y == world_median_year:
                    styled_annotation(
                        0,
                        y_high,
                        title="Deep poverty",
                        text=f"The poorer half of the world population — 4 billion people — live on less than ${brace_y:.{dollar_decimals}f} per {period}",
                        box_alignment=(1.0, 0.0),
                    )
                if brace_y == ipl:
                    world_share_ipl = df_main_indicators.loc[
                        (df_main_indicators["country"] == "World")
                        & (df_main_indicators["year"] == year),
                        "headcount_ratio_300",
                    ].values[0]
                    styled_annotation(
                        0,
                        y_high,
                        title="Extreme poverty",
                        text=f"The poorest {world_share_ipl:.0f}% live on less than ${brace_y:.{dollar_decimals}f} per {period}",
                        box_alignment=(1.0, 0.0),
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
            plt.FuncFormatter(lambda x, _: f"{x / 100:.0%}")
        )

        # Replace the default dollar-amount y-tick labels with the reference-line labels.
        # Falls back to the dollar formatter when there are no reference lines (add_lines=False).
        if reference_ticks:
            sorted_refs = sorted(reference_ticks)
            yticks = [t[0] for t in sorted_refs]
            wrap_width = 36  # characters; tune with the right-margin adjust below
            yticklabels = [textwrap.fill(t[1], width=wrap_width) for t in sorted_refs]
            line_plot.set_yticks(yticks)
            # Hide the default tick labels; we'll place them manually below via annotate so
            # we can actually apply a vertical offset (matplotlib's tick-label renderer
            # ignores the offset_copy transform we'd otherwise use).
            line_plot.set_yticklabels([""] * len(yticks))

            # Reserve room on the right so long labels like "International Poverty Line" don't get clipped.
            line_plot.get_figure().subplots_adjust(right=0.55)

            # Per-label vertical offsets (with va="center", default places the block centered on tick):
            # - 1-line label: no offset needed (text is centered on tick).
            # - n-line wrapped label: shift block DOWN by (n-1)*line_height/2 so the FIRST line sits on the tick.
            # - When the tick above is too close (would overlap given label heights), drop this label entirely
            #   BELOW its tick by ~one label height so the two labels separate.
            line_height_points = 8 * 1.5  # fontsize × linespacing
            # Anchor overrides for specific labels that sit too close to their neighbour
            # for the automatic collision logic to look right. "above" lifts the label so
            # its bottom sits at the tick; "below" drops it so its top sits at the tick.
            anchor_overrides = {
                "median income in Sweden": "above",
                "richest 10%": "below",
            }

            def matched_anchor(text: str) -> str | None:
                # If both the country-median and the p90 phrasings appear, the labels were
                # already merged into one combined tick — keep it centered, not above/below.
                if "median income in Sweden" in text and "richest 10%" in text:
                    return None
                for fragment, position in anchor_overrides.items():
                    if fragment in text:
                        return position
                return None

            # Place each label manually as an annotation in the right-margin column. This
            # gives us actual vertical offset control (matplotlib's tick-label renderer
            # ignores transform offsets, but annotate's textcoords="offset points" works).
            tick_pad_points = 4  # mirrors matplotlib's default tick-label pad
            for tick_y, text in zip(yticks, yticklabels):
                n = text.count("\n") + 1
                override = matched_anchor(text)
                if override == "above":
                    # bottom of the label block sits at the tick → text extends upward
                    offset_y = 0
                    va = "bottom"
                elif override == "below":
                    # top of the label block sits at the tick → text extends downward
                    offset_y = 0
                    va = "top"
                else:
                    # First line centered on the tick. With va="center", the bbox center
                    # is at tick + offset_y; shifting down by (n-1)*line_height/2 puts the
                    # first line at the tick. For n=1 the offset is zero.
                    offset_y = -line_height_points * (n - 1) / 2
                    va = "center"
                line_plot.annotate(
                    text,
                    xy=(1.0, tick_y),
                    xycoords=("axes fraction", "data"),
                    xytext=(tick_pad_points, offset_y),
                    textcoords="offset points",
                    ha="left",
                    va=va,
                    fontsize=8,
                    linespacing=1.5,
                    annotation_clip=False,
                )
        else:
            line_plot.get_yaxis().set_major_formatter(
                plt.FuncFormatter(lambda x, _: f"${x:.0f} per {period}")
            )

        # The full distribution stays visible on the x-axis (0–100). The y-axis is clamped
        # to the y-value at cut_percentile so the steeply-rising top tail doesn't dominate.
        line_plot.set_xlim(0, 100)
        if y_at_cut is not None:
            line_plot.set_ylim(0, y_at_cut)
            line_plot.set_autoscaley_on(False)
        else:
            line_plot.set_ylim(0, line_plot.get_ylim()[1])

        # Fade the top band of the chart: clear at the very top, opaque white everywhere
        # at and below the plateau line. The opaque region covers the plateau line entirely
        # (so we don't see the faint top edge), while above the plateau the band fades
        # smoothly into the chart background.
        if y_at_cut is not None:
            fade_y_bottom = (
                y_at_fade_floor if y_at_fade_floor is not None else y_at_cut * 0.85
            )
            fade_y_top = y_at_cut * 1.10
            plateau_frac = (y_at_cut - fade_y_bottom) / (fade_y_top - fade_y_bottom)
            n = 256
            plateau_idx = int(n * plateau_frac)
            alpha = np.ones(n)
            # The portion of the band above the plateau fades from opaque (at plateau)
            # to transparent (at the very top).
            alpha[plateau_idx:] = np.linspace(1, 0, n - plateau_idx)
            fade = np.ones((n, 1, 4))
            fade[:, :, :3] = 1.0  # white RGB
            fade[:, :, 3] = alpha.reshape(-1, 1)
            line_plot.imshow(
                fade,
                extent=[0, 99.75, fade_y_bottom, fade_y_top],
                aspect="auto",
                zorder=3,
                interpolation="bilinear",
            )

        # Move y axis to the right
        line_plot.yaxis.tick_right()

        # Draw a line for each axis
        line_plot.axhline(y=0, color="black", linewidth=0.5)
        # Right-hand y-axis line. When the chart is cut, extend it slightly above the cap
        # (clip_on=False), visually hinting that the data continues above the visible range.
        if y_at_cut is not None:
            line_plot.plot(
                [100, 100],
                [0, y_at_cut * 1.10],
                color="black",
                linewidth=0.5,
                clip_on=False,
            )
        else:
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

            # interpolate=True extends the fill to the exact x where the `where`
            # condition flips, rather than ending at the nearest KDE grid point.
            kde_plot.fill_between(
                x=x_line,
                y1=y_line,
                where=(x_line <= value),
                interpolate=True,
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


#######################################
# SYNTHETIC DATA GENERATION
#######################################


def generate_synthetic_data_from_mean_gini(
    country: str, year: int, target_mean, target_gini, size=100_000_000, seed=2_000
):
    """
    Generate synthetic data from a lognormal distribution that approximates a given mean and Gini coefficient.

    Parameters:
        target_mean (float): Desired mean of the synthetic distribution.
        target_gini (float): Desired Gini coefficient of the distribution.
        size (int): Number of samples to generate (default: 1000).
        seed (int or None): Random seed for reproducibility (default: None).

    Returns:
        np.ndarray: Synthetic data array.
    """

    # Set random seed if provided
    if seed is not None:
        np.random.seed(seed)

    # Gini of a lognormal: G = 2 * Φ(σ/√2) - 1
    def lognormal_gini(sigma: float) -> float:
        return 2 * norm.cdf(sigma / np.sqrt(2)) - 1

    # Objective function to minimize: match mean and Gini
    def objective(params: np.ndarray) -> float:
        mu, sigma = params
        mean = np.exp(mu + sigma**2 / 2)
        gini = lognormal_gini(sigma)
        # Weighted sum to prioritize Gini matching (since mean is easier to match)
        return 1 * (mean - target_mean) ** 2 + 100 * (gini - target_gini) ** 2

    def gini(array: np.ndarray) -> float:
        # Use the definition for population Gini
        array = np.sort(array)
        n = array.size
        index = np.arange(1, n + 1)
        return (2 * np.sum(index * array)) / (n * np.sum(array)) - (n + 1) / n

    # Initial guess
    initial_guess = [np.log(target_mean), 1.0]

    # Use a deterministic optimizer and tighter tolerance for reproducibility
    result = minimize(
        objective,
        initial_guess,
        bounds=[(None, None), (1e-6, None)],
        method="L-BFGS-B",
        options={"ftol": 1e-12, "gtol": 1e-8, "maxiter": 1e12},
    )
    mu_opt, sigma_opt = result.x

    # Use a fixed random seed for reproducibility
    rng = np.random.default_rng(seed)
    synthetic_data = rng.lognormal(mean=mu_opt, sigma=sigma_opt, size=size)

    # Calculate the mean and Gini of the generated data
    generated_mean = np.mean(synthetic_data)
    generated_gini = gini(synthetic_data)

    # Make synthetic data a dataframe, with the column name "avg"
    synthetic_data = pd.DataFrame(synthetic_data, columns=["avg"])

    # Add the columns "country" and "year"
    synthetic_data["country"] = country
    synthetic_data["year"] = year

    return synthetic_data, generated_mean, generated_gini, target_mean, target_gini


if __name__ == "__main__":
    run()
