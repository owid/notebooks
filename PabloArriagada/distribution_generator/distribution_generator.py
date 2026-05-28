import hashlib
import textwrap
import time
from pathlib import Path
from typing import List, Literal, cast

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.lines import Line2D
from matplotlib.offsetbox import AnnotationBbox, TextArea, VPacker
from matplotlib.patches import Patch
from matplotlib.transforms import blended_transform_factory

PARENT_DIR = Path(__file__).parent.absolute()

# The source feathers are large (the all-lognormal one is ~35M rows / ~80s to
# download) and are re-fetched every run because the URLs carry `?nocache`. Cache
# them on local disk and reuse the copy until it is older than CACHE_TTL_HOURS,
# so repeated runs load in seconds while still refreshing periodically.
CACHE_DIR = PARENT_DIR / ".cache"
CACHE_TTL_HOURS = 24

# Define International Poverty Line
INTERNATIONAL_POVERTY_LINE = 3

# Define poverty line for high-income countries
POVERTY_LINE_HIGH_INCOME = 30

# PIP PPP version used throughout (filter applied when reading the dimensional tables).
PPP_VERSION = 2021

# Define latest year
LATEST_YEAR = 2026

# Years kept in the slim local cache of the two big historical feathers (see
# read_feather_cached). These must cover every year charted from each file — if
# you add a chart for a new year, add it here so the cache re-slices to include
# it (otherwise that chart gets empty data).
HISTORICAL_CACHE_YEARS = [1820, 1920, 1980, LATEST_YEAR]
ALL_LOGNORMAL_CACHE_YEARS = [1820, 1920, LATEST_YEAR]

# Subdivision (e.g. per-country) separator styling on the hierarchical stacked
# charts: each band's edge is its region's own colour at full opacity (no
# darkening). The seaborn stacked fill renders the face at alpha 0.75, so the
# fully-opaque same-hue edge reads as a subtle separator without introducing a
# second colour dimension.
SUBDIVIDE_EDGE_LINEWIDTH = 0.3

# Define width and height of the plot
WIDTH = 1500
HEIGHT = 750

# For Pen Parade — roughly 1:1
WIDTH_PEN = 1000
HEIGHT_PEN = 1000

# Color used for reference lines (IPL, World median, $900/$500 lines, country medians, etc.)
REFERENCE_LINE_COLOR = "#6c7a89"


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
        # Includes 1, 2, 5 at the low end so the stacked charts (which keep the
        # full distribution down to ~$1/month) get labelled ticks there. Every
        # tick site filters these to the visible x-range, so charts that don't
        # reach the low end (e.g. country comparisons) won't show them.
        "log_ticks": [
            1,
            2,
            5,
            10,
            20,
            50,
            100,
            200,
            500,
            1000,
            2000,
            5000,
            10000,
            20000,
        ],
    },
    "year": {
        "factor": 365,
        # Low-end ticks (1, 2, 5, 10, 20, 50) mirror the month scale so the
        # stacked charts get labelled ticks where the full distribution reaches.
        # Every tick site filters these to the visible x-range, so charts that
        # don't reach the low end won't show them.
        "log_ticks": [
            1,
            2,
            5,
            10,
            20,
            50,
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
    df_thousand_bins = read_feather_cached(THOUSAND_BINS_URL)
    # The two historical files are ~35M rows each; we only chart a handful of
    # years, so cache just those (and drop the unused region_old column). The
    # cold run still downloads the full file once; warm runs load a tiny slice.
    df_thousand_bins_historical = read_feather_cached(
        THOUSAND_BINS_HISTORICAL_URL,
        years=HISTORICAL_CACHE_YEARS,
        drop_columns=["region_old"],
    )
    df_thousand_bins_historical_all_lognormal = read_feather_cached(
        THOUSAND_BINS_HISTORICAL__ALL_LOGNORMAL_URL,
        years=ALL_LOGNORMAL_CACHE_YEARS,
        drop_columns=["region_old"],
    )
    df_national_lines = read_feather_cached(NATIONAL_LINES_URL)

    # World Bank PIP dimensional tables → flat shapes the plotting code expects.
    # Percentiles: legacy table was filtered to ppp_version=2021; replicate by filtering here.
    df_percentiles = read_feather_cached(PERCENTILES_URL)
    df_percentiles = df_percentiles[
        df_percentiles["ppp_version"] == PPP_VERSION
    ].reset_index(drop=True)

    # Main indicators (used only for World aggregates): rebuild a flat per-(country, year)
    # frame from complete_series by selecting the right slice for each column family.
    df_complete = read_feather_cached(COMPLETE_SERIES_URL)
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

    df_national_lines.loc[
        (df_national_lines["country"] == "United States"),
        "harmonized_national_poverty_line",
    ] = 27.10

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
            years=[LATEST_YEAR],
            fill=False,
            legend=True,
            common_norm=False,
            period="day",
            survey_based=False,
            add_ipl=None,
            add_world_median=None,
            add_multiple_lines_day=lines,            width=1500,
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
        add_world_median=None,
        add_multiple_lines_day=None,        width=1500,
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
        common_norm=False,        period="day",
        survey_based=False,
        add_ipl="line",
        add_world_median="line",
        add_multiple_lines_day=[3],
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
            period="month",
            survey_based=False,
            width=1500,
            height=400,
            add_multiple_lines_day=[3],
            fill=False,
            add_ipl="line",
            add_world_median=None,
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
            period="month",
            survey_based=True,
            preferred_reporting_level="national",
            preferred_welfare_type="income",
            width=1500,
            height=400,
            add_multiple_lines_day=[3],
            fill=False,
            add_ipl="line",
            add_world_median=None,
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
        common_norm=False,        period="day",
        survey_based=False,
        add_ipl="line",
        add_national_lines=True,
        df_national_lines=df_national_lines,
        share_y_axis=False,
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
        common_norm=False,        period="day",
        survey_based=True,
        preferred_reporting_level="national",
        preferred_welfare_type="income",
        add_ipl="line",
        add_national_lines=True,
        df_national_lines=df_national_lines,
        share_y_axis=False,
    )

    # Stacked distributions with common density estimate
    distributional_plots(
        data=df_thousand_bins_historical,
        df_main_indicators=None,
        x="avg",
        weights="pop",
        log_scale=True,
        multiple="stack",
        hue="region",
        hue_order=None,
        subdivide_hue="country",
        years=[1820, 1980, LATEST_YEAR],
        legend=True,
        common_norm=True,
        period="month",
        survey_based=False,
        add_ipl="line",
        add_world_median=None,
        add_high_income_pl="line",
        # add_multiple_lines_day=[3, 30],
        share_y_axis=True,
        share_x_axis=True,
        add_fade_in_tails=False,
    )

    # Same hierarchical region/country stack, but with the three years stacked
    # as rows in a single figure (shared x and y) instead of one SVG per year.
    distributional_plots_per_row(
        data=df_thousand_bins_historical,
        df_main_indicators=None,
        x="avg",
        weights="pop",
        log_scale=True,
        multiple="stack",
        hue="region",
        subdivide_hue="country",
        years=[1820, 1980, LATEST_YEAR],
        common_norm=True,
        period="month",
        survey_based=False,
        add_ipl="line",
        add_high_income_pl="line",
        row_by="year",
        width=1150,
        height=260,
        share_y_axis=True,
        share_x_axis=True,
        add_fade_in_tails=False,
    )

    # Same stacked charts (per-year SVGs + the multi-row figure) for the other
    # region groupings, alongside the default `region` ones above. A filename
    # suffix keeps each grouping's outputs separate.
    for region_column in ["owid_region", "mpd_region"]:
        distributional_plots(
            data=df_thousand_bins_historical,
            df_main_indicators=None,
            x="avg",
            weights="pop",
            log_scale=True,
            multiple="stack",
            hue=region_column,
            hue_order=None,
            subdivide_hue="country",
            years=[1820, 1980, LATEST_YEAR],
            legend=True,
            common_norm=True,
            period="month",
            survey_based=False,
            add_ipl="line",
            add_world_median=None,
            add_high_income_pl="line",
            share_y_axis=True,
            share_x_axis=True,
            add_fade_in_tails=False,
            filename_suffix=f"_{region_column}",
        )
        distributional_plots_per_row(
            data=df_thousand_bins_historical,
            df_main_indicators=None,
            x="avg",
            weights="pop",
            log_scale=True,
            multiple="stack",
            hue=region_column,
            subdivide_hue="country",
            years=[1820, 1980, LATEST_YEAR],
            common_norm=True,
            period="month",
            survey_based=False,
            add_ipl="line",
            add_high_income_pl="line",
            row_by="year",
            width=1150,
            height=260,
            share_y_axis=True,
            share_x_axis=True,
            add_fade_in_tails=False,
            filename_suffix=f"_{region_column}",
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

    # Historical data — Option A: three separate SVGs (1820, 1920, 2026) that all
    # share a y-limit so peak heights are visually comparable across years.
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
        common_norm=False,        period="month",
        survey_based=False,
        add_ipl="line",
        add_high_income_pl="line",
        add_world_median=None,
        add_multiple_lines_day=[3, 30],
        width=1150,
        height=220,
        share_y_axis=True,
        share_x_axis=True,
    )

    # Historical data — Option B: single SVG with all three years stacked,
    # sharing both x and y axes (via row_by="year"). Filled KDE with shaded
    # regions under each curve at the $3/day IPL and the $30/day high-income line.
    distributional_plots_per_row(
        data=df_thousand_bins_historical,
        df_main_indicators=None,
        x="avg",
        weights="pop",
        log_scale=True,
        multiple="layer",
        hue="country",
        hue_order=["Sweden"],
        years=[1820, 1920, LATEST_YEAR],
        fill=True,
        common_norm=False,        period="month",
        survey_based=False,
        add_ipl="line",
        add_high_income_pl="line",
        width=1150,
        height=220,
        row_by="year",
        add_multiple_lines_day=[3, 30],
    )

    # Same years from the all-lognormal companion dataset. Only the 2026 row
    # actually differs from df_thousand_bins_historical; 1820 and 1920 are
    # byte-identical between the two datasets but we render them anyway so the
    # _lognormal SVGs are a complete drop-in set that shares its own y-max and
    # x-range pre-pass (independent of the mix dataset).
    distributional_plots(
        data=df_thousand_bins_historical_all_lognormal,
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
        common_norm=False,        period="month",
        survey_based=False,
        add_ipl="line",
        add_high_income_pl="line",
        add_world_median=None,
        add_multiple_lines_day=[3, 30],
        width=1150,
        height=220,
        share_y_axis=True,
        share_x_axis=True,
        filename_suffix="_lognormal",
    )

    distributional_plots_per_row(
        data=df_thousand_bins_historical_all_lognormal,
        df_main_indicators=None,
        x="avg",
        weights="pop",
        log_scale=True,
        multiple="layer",
        hue="country",
        hue_order=["Sweden"],
        years=[1820, 1920, LATEST_YEAR],
        fill=True,
        common_norm=False,        period="month",
        survey_based=False,
        add_ipl="line",
        add_high_income_pl="line",
        width=1150,
        height=220,
        row_by="year",
        add_multiple_lines_day=[3, 30],
        filename_suffix="_lognormal",
    )


def read_feather_cached(
    url: str,
    years: List[int] | None = None,
    drop_columns: List[str] | None = None,
) -> pd.DataFrame:
    """Read a feather from ``url``, caching a slimmed copy under ``CACHE_DIR``.

    Re-downloads when the cached copy is missing or older than ``CACHE_TTL_HOURS``.
    The source feathers are large (the all-lognormal one is ~35M rows) and carry
    ``?nocache``, so without this every run re-fetches ~135s of data — and even a
    full local cache still spends ~80s deserialising 35M rows. ``years`` and
    ``drop_columns`` slim the cached copy to only what the charts use, so the cold
    run downloads once but every warm run loads a <1M-row file in ~1s. The filter
    is part of the cache key, so a different slice caches separately.
    """
    CACHE_DIR.mkdir(exist_ok=True)
    # Key on the URL (without the ?nocache buster) plus the filter, so the path
    # stays stable and distinct slices don't collide.
    key_src = url.split("?")[0]
    if years is not None:
        key_src += f"|years={sorted(years)}"
    if drop_columns is not None:
        key_src += f"|drop={sorted(drop_columns)}"
    key = hashlib.md5(key_src.encode()).hexdigest()[:16]
    local = CACHE_DIR / f"{key}.feather"
    if (
        local.exists()
        and (time.time() - local.stat().st_mtime) < CACHE_TTL_HOURS * 3600
    ):
        return pd.read_feather(local)
    df = pd.read_feather(url)
    if drop_columns is not None:
        df = df.drop(columns=drop_columns, errors="ignore")
    if years is not None:
        df = df[df["year"].isin(years)].reset_index(drop=True)
    df.to_feather(local)
    return df


def _subdivide_palette(data: pd.DataFrame, hue: str, subdivide_hue: str):
    """Build the colour scheme for a hierarchical stacked KDE.

    Returns ``(region_order, region_palette, palette)`` where ``region_order`` is
    the parent groups (``hue``, e.g. region) sorted alphabetically, each given one
    base colour in ``region_palette``, and ``palette`` maps every sub-level value
    (``subdivide_hue``, e.g. country) to its parent's colour so a region reads as
    one colour block.
    """
    region_order = sorted(data[hue].dropna().unique())
    region_palette = dict(
        zip(region_order, sns.color_palette(n_colors=len(region_order)))
    )
    palette = {}
    for region in region_order:
        for member in data[data[hue] == region][subdivide_hue].dropna().unique():
            palette[member] = region_palette[region]
    return region_order, region_palette, palette


def _subdivide_order(
    frame: pd.DataFrame,
    hue: str,
    subdivide_hue: str,
    weights: str,
    region_order: List[str],
) -> List[str]:
    """Sub-level values grouped by parent ``hue`` (region order fixed), sorted
    within each group by descending population so the largest sits at the top of
    the stack and the smallest at the bottom. seaborn stacks the first hue_order
    entry at the top, so descending population = largest first."""
    pops = frame.groupby([hue, subdivide_hue], observed=True)[weights].sum()
    ordered: List[str] = []
    for region in region_order:
        if region not in pops.index.get_level_values(0):
            continue
        ordered.extend(pops.loc[region].sort_values(ascending=False).index.tolist())
    return ordered


def _apply_subdivide_edges(ax: plt.Axes) -> None:
    """For a hierarchical stacked KDE (``subdivide_hue``), set each band's edge
    to its own face colour at full opacity. The seaborn stacked fill renders the
    face at alpha 0.75, so the fully-opaque same-hue edge reads as a subtle
    separator without introducing a second colour dimension."""
    for coll in ax.collections:
        face = np.asarray(coll.get_facecolor(), dtype=float)
        if face.size == 0:
            continue
        r, g, b = (float(face[0, i]) for i in range(3))
        coll.set_edgecolor((r, g, b, 1.0))
        coll.set_linewidth(SUBDIVIDE_EDGE_LINEWIDTH)


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
    add_world_median: Literal["line", "area", None] = "line",
    add_high_income_pl: Literal["line", "area", None] = None,
    add_multiple_lines_day: List[float] = None,
    width: int = WIDTH,
    height: int = HEIGHT,
    add_fade_in_tails: bool = True,
    percentiles_to_fade: List[float] = [1, 99],
    share_y_axis: bool = False,
    share_x_axis: bool = False,
    filename_suffix: str = "",
    subdivide_hue: str = None,
) -> None:
    """
    Plot distributional data with seaborn, with multiple options for customization.

    ``share_y_axis``: when True, run a hidden pre-pass across all `years` to find
    the maximum KDE density and lock every per-year figure's y-axis to that value.
    Required if you want the saved SVGs to be visually comparable — without it,
    matplotlib auto-scales each year independently and hides the inequality signal
    (narrower distributions look the same height as wider ones).

    ``share_x_axis``: when True, the pre-pass also computes the union of x-values
    across years (after fading tails) and uses that as the shared x range —
    applied to KDE clip, the data filter, and the figure's xlim — so every
    per-year SVG shares the same horizontal scale.
    """

    # Filter the data with the hue and hue_order
    number_of_countries = 1
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

    # Order/colour passed to seaborn. By default we stack by `hue` (e.g. region).
    # When `subdivide_hue` is set (e.g. "country"), we instead stack by that finer
    # level but colour every sub-band with its parent `hue`'s colour, so each
    # region reads as one colour block striped into per-country bands by thin
    # white separators. `region_palette` is kept for the custom region legend.
    seaborn_hue = hue
    palette = None
    fill_kwargs: dict = {}
    region_palette: dict = {}
    region_order: List[str] = []

    if subdivide_hue is not None:
        region_order, region_palette, palette = _subdivide_palette(
            data, hue, subdivide_hue
        )
        # The actual stack order is recomputed per year (by population) inside the
        # loop; this pre-loop order only feeds the share_y pre-pass, where order
        # is irrelevant to the total stack height.
        plot_hue_order = _subdivide_order(
            data, hue, subdivide_hue, weights, region_order
        )
        seaborn_hue = subdivide_hue
        # Per-country separators are drawn after plotting (see
        # _apply_subdivide_edges) as each band's region colour at full opacity —
        # they sit on the shared 0.75-alpha colour block as subtle subdivisions
        # without introducing a second colour dimension.
        fill_kwargs = {"linewidth": SUBDIVIDE_EDGE_LINEWIDTH}
    else:
        # When no explicit hue_order is given (e.g. the all-regions stack), sort
        # the hue values alphabetically so both the stacked bands and the legend
        # read A→Z instead of seaborn's arbitrary encounter order. The original
        # `hue_order` (None) is kept for the filename logic above.
        plot_hue_order = hue_order
        if plot_hue_order is None:
            plot_hue_order = sorted(data[hue].dropna().unique())

    # Define multiple_areas, depending on the add_multiple_lines_day
    if add_multiple_lines_day is not None:
        # Define the filename according to the add_multiple_lines_day
        filename_multiple_areas = "_".join(
            [str(round(value, 2)) for value in add_multiple_lines_day]
        )
    else:
        filename_multiple_areas = "none"

    # Define the income period values. PERIOD_VALUES mixes int factors with
    # list log_ticks under the same dict, so cast each lookup back to its
    # concrete type.
    period_factor = cast(int, PERIOD_VALUES[period]["factor"])
    log_ticks = cast(List[int], PERIOD_VALUES[period]["log_ticks"])
    # Cents only make sense at the daily scale; monthly and yearly values are
    # large enough that the decimal noise is distracting (matches pen_parade).
    dollar_decimals = 2 if period == "day" else 0

    data[x] = data[x] * period_factor

    # Define IPL for the period
    ipl = INTERNATIONAL_POVERTY_LINE * period_factor

    # Optional pre-pass: pre-compute the union x-range and/or the max KDE density
    # across years so per-year figures can share x / y limits.
    x_axis_range: tuple | None = None  # set by the share_x_axis pre-pass below
    shared_y_max: float | None = None
    if share_x_axis or share_y_axis:

        def _filter_year(year_value):
            if survey_based:
                sub = data[data["reference_year"] == year_value]
            else:
                sub = data[data["year"] == year_value]
            if add_fade_in_tails:
                if "percentile" in sub.columns:
                    pq, bounds = "percentile", percentiles_to_fade
                elif "quantile" in sub.columns:
                    pq, bounds = "quantile", [p * 10 for p in percentiles_to_fade]
                else:
                    return sub
                sub = sub[(sub[pq] > bounds[0]) & (sub[pq] < bounds[1])]
            return sub

        # Step 1: compute shared x range from data if requested. When the chart is
        # log-scaled, extend each year's bounds to where seaborn's KDE actually
        # ends (data ± cut*bw in log10 space, matching seaborn's default cut=3
        # and Scott's bandwidth), then take the union across years. This means
        # the axis right edge lands exactly where the curve naturally tapers to
        # near-zero, rather than chopping the tail.
        if share_x_axis:
            x_min = float("inf")
            x_max = float("-inf")
            for year in years:
                sub = _filter_year(year)
                if not len(sub):
                    continue
                year_min = float(sub[x].min())
                year_max = float(sub[x].max())
                if log_scale:
                    v = np.log10(sub[x].to_numpy(dtype=float))
                    if weights is not None:
                        w = sub[weights].to_numpy(dtype=float)
                    else:
                        w = np.ones(len(sub))
                    mean_v = float(np.average(v, weights=w))
                    var_v = float(np.average((v - mean_v) ** 2, weights=w))
                    std_v = float(np.sqrt(max(var_v, 0.0)))
                    w_sum = float(w.sum())
                    w_sq_sum = float((w * w).sum())
                    n_eff = (w_sum * w_sum / w_sq_sum) if w_sq_sum > 0 else 1.0
                    bw = std_v * n_eff ** (-1 / 5) if n_eff > 0 else 0.0
                    cut = 3  # matches seaborn's default
                    year_min = year_min / 10 ** (cut * bw)
                    year_max = year_max * 10 ** (cut * bw)
                x_min = min(x_min, year_min)
                x_max = max(x_max, year_max)
            if x_min < float("inf"):
                x_axis_range = (x_min, x_max)

        # Step 2: compute shared y max if requested (uses x_axis_range from step 1)
        if share_y_axis:
            if log_scale and x_axis_range is not None:
                clip_pre = (np.log(x_axis_range[0]), np.log(x_axis_range[1]))
            else:
                clip_pre = x_axis_range
            shared_y_max = 0.0
            for year in years:
                data_year_pre = _filter_year(year)
                if x_axis_range is not None:
                    data_year_pre = data_year_pre[
                        (data_year_pre[x] >= x_axis_range[0])
                        & (data_year_pre[x] <= x_axis_range[1])
                    ]
                if len(data_year_pre) == 0:
                    continue
                fig_pre, ax_pre = plt.subplots()
                sns.kdeplot(
                    data=data_year_pre,
                    x=x,
                    weights=weights,
                    fill=False,
                    log_scale=log_scale,
                    hue=seaborn_hue,
                    hue_order=plot_hue_order,
                    multiple=multiple,
                    legend=False,
                    common_norm=common_norm,
                    gridsize=gridsize,
                    clip=clip_pre,
                    ax=ax_pre,
                )
                for line in ax_pre.lines:
                    ys = np.asarray(line.get_data()[1])
                    if ys.size:
                        shared_y_max = max(shared_y_max, float(np.nanmax(ys)))
                plt.close(fig_pre)

    for year in years:
        if survey_based:
            data_year = data[data["reference_year"] == year].reset_index(drop=True)
        else:
            data_year = data[data["year"] == year].reset_index(drop=True)

        if df_main_indicators is not None:
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

        # KDE clip in log space when log_scale=True; pinned to the shared x range so
        # each year's curve extends across the same horizontal extent.
        if x_axis_range is not None and log_scale:
            clip_param = (np.log(x_axis_range[0]), np.log(x_axis_range[1]))
        else:
            clip_param = x_axis_range

        # For the hierarchical stack, order each region's countries by this
        # year's population (largest on top). Other modes keep the fixed order.
        current_hue_order = (
            _subdivide_order(data_year, hue, subdivide_hue, weights, region_order)
            if subdivide_hue is not None
            else plot_hue_order
        )

        # Plot a kde with seaborn
        kde_plot = sns.kdeplot(
            data=data_year,
            x=x,
            weights=weights,
            fill=fill,
            log_scale=log_scale,
            hue=seaborn_hue,
            hue_order=current_hue_order,
            palette=palette,
            multiple=multiple,
            legend=legend,
            common_norm=common_norm,
            gridsize=gridsize,
            clip=clip_param,
            **fill_kwargs,
        )
        if subdivide_hue is not None:
            _apply_subdivide_edges(kde_plot)

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
            _styled_reference_label(
                kde_plot,
                ipl,
                1.0,
                title="International Poverty Line",
                value=f"${ipl:.{dollar_decimals}f} per {period}",
                ha="right",
                xycoords=kde_plot.get_xaxis_transform(),
            )
        elif add_ipl == "area":
            draw_area_under_curve(
                kde_plot=kde_plot,
                number_of_countries=number_of_countries,
                values=[ipl],
            )

        if add_world_median == "line" and df_main_indicators is not None:
            # Add a vertical line for the world median, in the same format as the international poverty line
            plt.axvline(
                x=world_median_year,
                color="lightgrey",
                linestyle=":",
                linewidth=0.8,
            )
            _styled_reference_label(
                kde_plot,
                world_median_year,
                1.0,
                title="World median",
                value=f"${world_median_year:.{dollar_decimals}f} per {period}",
                ha="left",
                xycoords=kde_plot.get_xaxis_transform(),
            )
        elif add_world_median == "area" and df_main_indicators is not None:
            draw_area_under_curve(
                kde_plot=kde_plot,
                number_of_countries=number_of_countries,
                values=[world_median_year],
            )

        high_income_pl = POVERTY_LINE_HIGH_INCOME * period_factor
        if add_high_income_pl == "line":
            plt.axvline(
                x=high_income_pl,
                color="lightgrey",
                linestyle=":",
                linewidth=0.8,
            )
            _styled_reference_label(
                kde_plot,
                high_income_pl,
                1.0,
                title="High-income poverty line",
                value=f"${high_income_pl:.{dollar_decimals}f} per {period}",
                ha="left",
                xycoords=kde_plot.get_xaxis_transform(),
            )
        elif add_high_income_pl == "area":
            draw_area_under_curve(
                kde_plot=kde_plot,
                number_of_countries=number_of_countries,
                values=[high_income_pl],
            )

        if add_multiple_lines_day is not None:
            # Use a fresh local each iteration; otherwise the multiplied list
            # leaks across years and the second year fills get multiplied again.
            scaled_lines = [v * period_factor for v in add_multiple_lines_day]
            draw_area_under_curve(
                kde_plot=kde_plot,
                number_of_countries=number_of_countries,
                values=scaled_lines,
            )

        if legend and subdivide_hue is not None:
            # Stacking by the fine level (e.g. country) would yield a legend with
            # one entry per sub-band. Replace it with one entry per parent `hue`
            # group (e.g. region), coloured by the shared base colour.

            # seaborn renders stacked fills at alpha < 1; match the legend swatch
            # opacity to the rendered bands so the legend isn't bolder than the plot.
            fill_alpha = (
                float(kde_plot.collections[0].get_facecolor()[0][3])
                if len(kde_plot.collections)
                else 1.0
            )
            handles = [
                Patch(facecolor=region_palette[region], label=region, alpha=fill_alpha)
                for region in region_order
            ]
            kde_plot.legend(
                handles=handles,
                title=hue.capitalize(),
                loc="upper left",
                bbox_to_anchor=(0.8, 0.8),
            )
        elif legend:
            # Move the legend inside the plot
            kde_plot.legend_.set_bbox_to_anchor((0.8, 0.8))
            kde_plot.legend_.set_loc("upper left")
            # Make the title sentence case
            kde_plot.legend_.set_title(hue.capitalize())
        else:
            # For each plot, write the name of the country at the middle of the distribution, bottom
            for country in plot_hue_order:
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
            # Restrict ticks to the visible range. Calling set_xticks with values
            # past the current xlim makes matplotlib widen the axis to fit them,
            # which silently breaks share_x_axis (xlim jumps to the last tick).
            # When there's no shared range, fall back to the autoscaled xlim so
            # low ticks (1, 2, 5) only appear on charts that actually reach them.
            lo, hi = x_axis_range if x_axis_range is not None else kde_plot.get_xlim()
            ticks = [t for t in log_ticks if lo <= t <= hi]
            kde_plot.set_xticks(ticks)
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

        # Lock y-axis to the shared max so the per-year SVGs can be visually compared.
        if shared_y_max is not None and shared_y_max > 0:
            kde_plot.set_ylim(0, shared_y_max * 1.05)

        # Add a base line for each plot in the x axis
        plt.axhline(y=0, color="gray", linewidth=0.5)

        fig = kde_plot.get_figure()

        # Remove the clipping of the figure
        for o in fig.findobj():
            o.set_clip_on(False)

        fig.set_size_inches(width / 100, height / 100)

        # Use bbox_inches="tight" so reference-line labels above the chart are
        # included in the saved SVG. For shared-axis cases the label content is
        # the same across years (same IPL / high-income / world median), so the
        # tight bbox produces consistent dimensions across SVGs.
        fig.savefig(
            f"{PARENT_DIR}/{filename}_{year}_survey_{survey_based}_log_{log_scale}_multiple_{multiple}_common_norm_{common_norm}_multiple_areas_{filename_multiple_areas}{filename_suffix}.svg",
            bbox_inches="tight",
        )
        plt.close(fig)

    return None


def distributional_plots_per_row(
    data: pd.DataFrame,
    df_main_indicators: pd.DataFrame | None,
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
    add_world_median: Literal["line", "area", None] = "line",
    add_national_lines: bool = False,
    df_national_lines: pd.DataFrame = None,
    width: int = WIDTH,
    height: int = HEIGHT,
    add_fade_in_tails: bool = True,
    percentiles_to_fade: List[float] = [1, 99],
    row_by: Literal["country", "year"] = "country",
    add_multiple_lines_day: List[float] | None = None,
    add_high_income_pl: Literal["line", "area", None] = None,
    filename_suffix: str = "",
    share_x_axis: bool = True,
    share_y_axis: bool = True,
    subdivide_hue: str = None,
) -> None:
    """
    Plot distributional data with seaborn, with each distribution in a separate row.

    ``row_by="country"`` (default): one figure per year, rows = countries in
    ``hue_order``. Use this when you want to compare a fixed set of countries at
    a single moment.

    ``row_by="year"``: one figure with rows = years, country fixed to
    ``hue_order[0]``. Axes share both x and y, so peak heights are directly
    comparable across years. Use this when comparing one country across time.
    """
    if row_by == "year" and subdivide_hue is not None:
        _stacked_year_rows(
            data=data,
            x=x,
            weights=weights,
            hue=hue,
            subdivide_hue=subdivide_hue,
            years=years,
            log_scale=log_scale,
            multiple=multiple,
            common_norm=common_norm,
            gridsize=gridsize,
            period=period,
            add_ipl=add_ipl,
            add_high_income_pl=add_high_income_pl,
            width=width,
            height=height,
            add_fade_in_tails=add_fade_in_tails,
            percentiles_to_fade=percentiles_to_fade,
            filename_suffix=filename_suffix,
            share_x_axis=share_x_axis,
            share_y_axis=share_y_axis,
        )
        return None

    if row_by == "year":
        _distributional_plots_year_rows(
            data=data,
            df_main_indicators=df_main_indicators,
            x=x,
            weights=weights,
            country=hue_order[0],
            years=years,
            log_scale=log_scale,
            gridsize=gridsize,
            period=period,
            fill=fill,
            add_multiple_lines_day=add_multiple_lines_day,
            add_ipl=add_ipl,
            add_world_median=add_world_median,
            add_high_income_pl=add_high_income_pl,
            width=width,
            height=height,
            add_fade_in_tails=add_fade_in_tails,
            percentiles_to_fade=percentiles_to_fade,
            filename_suffix=filename_suffix,
            share_x_axis=share_x_axis,
            share_y_axis=share_y_axis,
        )
        return None

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

    # Define the income period values. PERIOD_VALUES mixes int factors with
    # list log_ticks under the same dict, so cast each lookup back to its
    # concrete type.
    period_factor = cast(int, PERIOD_VALUES[period]["factor"])
    log_ticks = cast(List[int], PERIOD_VALUES[period]["log_ticks"])
    dollar_decimals = 2 if period == "day" else 0

    data[x] = data[x] * period_factor

    # Define IPL for the period
    ipl = INTERNATIONAL_POVERTY_LINE * period_factor

    # row_by="country" needs the world reference lookups; row_by="year" returned earlier.
    assert df_main_indicators is not None, (
        "distributional_plots_per_row(row_by='country') requires df_main_indicators"
    )

    for year in years:
        if survey_based:
            data_year = data[data["reference_year"] == year].reset_index(drop=True)
        else:
            data_year = data[data["year"] == year].reset_index(drop=True)

        # Define world median
        world_median_year = (
            df_main_indicators.loc[
                (df_main_indicators["country"] == "World")
                & (df_main_indicators["year"] == year),
                "median",
            ].values[0]
            * period_factor
        )

        # Create a figure with subplots for each country. Share both axes so peak
        # Share both axes by default so peak heights and x-range are directly
        # comparable across rows. For mixed-spread comparisons (e.g. Ethiopia
        # vs the United States) the caller can pass share_y_axis=False to let
        # each country auto-scale its own y.
        fig, axes = plt.subplots(
            nrows=len(hue_order),
            ncols=1,
            figsize=(width / 100, height / 100),
            sharex=share_x_axis,
            sharey=share_y_axis,
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
                    "harmonized_national_poverty_line",
                ].values[0]

                draw_area_under_curve(
                    kde_plot=kde_plot,
                    values=[national_poverty_line],
                )

            # IPL and world-median lines are constant across rows in this layout
            # (one figure per year), so they're drawn once for the whole figure
            # outside this loop via `_add_figure_spanning_vline`. Per-row axvlines
            # leave a visible gap between subplots.

            if add_national_lines:
                # Add a vertical line for the national poverty line
                ax.text(
                    x=national_poverty_line,
                    y=plt.ylim()[0] - 0.05 * (plt.ylim()[1] - plt.ylim()[0]),
                    s=f"${national_poverty_line:.{dollar_decimals}f} The poverty line in {country}*",
                    color="grey",
                    rotation=0,
                    verticalalignment="top",
                    horizontalalignment="left",
                    fontsize=8,
                )

            # IPL / world-median labels are placed once in the figure margin
            # below (via _add_figure_spanning_vline_label) so they appear above
            # the whole stack rather than inside one of the subplots.

            # Add the name of the country at the middle of the distribution, bottom
            year_to_write = country_data["year"].iloc[0] if survey_based else year

            if survey_based:
                # Add the year and welfare type to the plot
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
                # Customize x-axis ticks to show 1, 2, 5, 10, 20, 50, 100, etc.,
                # filtered to the visible range so low ticks only appear where the
                # data reaches them (otherwise set_xticks would widen the axis).
                ax.set_xscale("log")
                lo, hi = ax.get_xlim()
                ax.set_xticks([t for t in log_ticks if lo <= t <= hi])
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

        plt.tight_layout()

        reference_labels: list[tuple[float, str, str, str]] = []
        if add_ipl == "line":
            _add_figure_spanning_vline(
                fig, axes, ipl, color="lightgrey", linestyle=":", linewidth=0.8
            )
            reference_labels.append(
                (
                    ipl,
                    "International Poverty Line",
                    f"${ipl:.{dollar_decimals}f} per {period}",
                    "right",
                )
            )
        if add_world_median == "line":
            _add_figure_spanning_vline(
                fig,
                axes,
                world_median_year,
                color="lightgrey",
                linestyle=":",
                linewidth=0.8,
            )
            reference_labels.append(
                (
                    world_median_year,
                    "World median",
                    f"${world_median_year:.{dollar_decimals}f} per {period}",
                    "left",
                )
            )
        _add_figure_spanning_vline_labels(fig, axes, reference_labels)

        # Remove the clipping of the figure
        for o in fig.findobj():
            o.set_clip_on(False)

        fig.savefig(
            f"{PARENT_DIR}/{filename}_{year}_survey_{survey_based}_log_{log_scale}_multiple_{multiple}_common_norm_{common_norm}_rows{filename_suffix}.svg",
            bbox_inches="tight",
        )
        plt.close(fig)

    return None


def _distributional_plots_year_rows(
    data: pd.DataFrame,
    x: str,
    weights: str,
    country: str,
    years: List[int],
    df_main_indicators: pd.DataFrame | None = None,
    log_scale: bool = True,
    gridsize: int = 200,
    period: Literal["day", "month", "year"] = "day",
    fill: bool = False,
    add_multiple_lines_day: List[float] | None = None,
    add_ipl: Literal["line", "area", None] = None,
    add_world_median: Literal["line", "area", None] = None,
    add_high_income_pl: Literal["line", "area", None] = None,
    width: int = WIDTH,
    height: int = HEIGHT,
    add_fade_in_tails: bool = True,
    percentiles_to_fade: List[float] = [1, 99],
    filename_suffix: str = "",
    share_x_axis: bool = True,
    share_y_axis: bool = True,
) -> None:
    """
    Private helper for ``distributional_plots_per_row(row_by="year")``: one country
    across several years, one row per year, sharing both x and y axes.
    """
    period_factor = cast(int, PERIOD_VALUES[period]["factor"])
    log_ticks = cast(List[int], PERIOD_VALUES[period]["log_ticks"])
    dollar_decimals = 2 if period == "day" else 0
    ipl = INTERNATIONAL_POVERTY_LINE * period_factor
    high_income_pl = POVERTY_LINE_HIGH_INCOME * period_factor

    def _world_median_for(year_value: int) -> float | None:
        if df_main_indicators is None:
            return None
        rows = df_main_indicators.loc[
            (df_main_indicators["country"] == "World")
            & (df_main_indicators["year"] == year_value),
            "median",
        ]
        if rows.empty:
            return None
        return float(rows.values[0]) * period_factor

    data = data[data["country"] == country].copy()
    data[x] = data[x] * period_factor

    def _fade(sub: pd.DataFrame) -> pd.DataFrame:
        if not add_fade_in_tails:
            return sub
        if "percentile" in sub.columns:
            pq, bounds = "percentile", percentiles_to_fade
        elif "quantile" in sub.columns:
            pq, bounds = "quantile", [p * 10 for p in percentiles_to_fade]
        else:
            return sub
        return sub[(sub[pq] > bounds[0]) & (sub[pq] < bounds[1])]

    # Pre-pass: compute the shared x range across years, extended to where each
    # year's KDE naturally tapers (data ± cut*bw in log10 space), then unioned.
    # Mirrors the share_x_axis logic in distributional_plots.
    x_axis_range: tuple | None = None
    if log_scale:
        x_min = float("inf")
        x_max = float("-inf")
        for year in years:
            sub = _fade(data[data["year"] == year])
            if not len(sub):
                continue
            year_min = float(sub[x].min())
            year_max = float(sub[x].max())
            v = np.log10(sub[x].to_numpy(dtype=float))
            if weights is not None:
                w = sub[weights].to_numpy(dtype=float)
            else:
                w = np.ones(len(sub))
            mean_v = float(np.average(v, weights=w))
            var_v = float(np.average((v - mean_v) ** 2, weights=w))
            std_v = float(np.sqrt(max(var_v, 0.0)))
            w_sum = float(w.sum())
            w_sq_sum = float((w * w).sum())
            n_eff = (w_sum * w_sum / w_sq_sum) if w_sq_sum > 0 else 1.0
            bw = std_v * n_eff ** (-1 / 5) if n_eff > 0 else 0.0
            cut = 3  # seaborn default
            year_min = year_min / 10 ** (cut * bw)
            year_max = year_max * 10 ** (cut * bw)
            x_min = min(x_min, year_min)
            x_max = max(x_max, year_max)
        if x_min < float("inf"):
            x_axis_range = (x_min, x_max)

    if log_scale and x_axis_range is not None:
        clip_param = (np.log(x_axis_range[0]), np.log(x_axis_range[1]))
    else:
        clip_param = None

    fig, axes = plt.subplots(
        nrows=len(years),
        ncols=1,
        figsize=(width / 100, height / 100 * len(years)),
        sharex=share_x_axis,
        sharey=share_y_axis,
    )
    if len(years) == 1:
        axes = [axes]

    for ax, year in zip(axes, years):
        data_year = _fade(data[data["year"] == year])
        # Always draw the line (fill=False) so we have a Line2D to read x/y from.
        # If `fill` is requested, layer a full-area shading on top via
        # draw_complete_area_under_curve. seaborn's own fill=True returns a
        # PolyCollection instead of a Line2D, which breaks draw_area_under_curve.
        kde_plot = sns.kdeplot(
            data=data_year,
            x=x,
            weights=weights,
            log_scale=log_scale,
            gridsize=gridsize,
            ax=ax,
            fill=False,
            legend=False,
            clip=clip_param,
        )
        if fill:
            draw_complete_area_under_curve(kde_plot=kde_plot)
        if add_multiple_lines_day is not None:
            draw_area_under_curve(
                kde_plot=kde_plot,
                values=[v * period_factor for v in add_multiple_lines_day],
            )
        ref_line_kw = dict(color="lightgrey", linestyle=":", linewidth=0.8)

        # `add_ipl` and `add_high_income_pl` are constant across years, so the line
        # is drawn once for the whole figure outside the per-row loop (below) to
        # avoid the visible gap between subplots that ax.axvline would leave.
        if add_ipl == "area":
            draw_area_under_curve(kde_plot=kde_plot, values=[ipl])
        if add_high_income_pl == "area":
            draw_area_under_curve(kde_plot=kde_plot, values=[high_income_pl])

        world_median_year = _world_median_for(year)
        if add_world_median == "line" and world_median_year is not None:
            ax.axvline(x=world_median_year, **ref_line_kw)
        elif add_world_median == "area" and world_median_year is not None:
            draw_area_under_curve(kde_plot=kde_plot, values=[world_median_year])

        # IPL and high-income labels are constant across rows and rendered once
        # in the figure margin (below). World-median varies per year so its label
        # stays in the top row inline.
        if (
            ax is axes[0]
            and add_world_median == "line"
            and world_median_year is not None
        ):
            _styled_reference_label(
                ax,
                world_median_year,
                ax.get_ylim()[1],
                title="World median",
                value=f"${world_median_year:.{dollar_decimals}f} per {period}",
                ha="left",
                box_alignment=(0.0, 1.0),
            )

        ax.text(
            x=data_year[x].median() if len(data_year) else 1.0,
            y=ax.get_ylim()[0],
            s=f"{country} ({year})",
            color="black",
            verticalalignment="bottom",
            horizontalalignment="center",
            fontsize=10,
        )
        ax.set_ylabel("")
        ax.yaxis.set_ticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.axhline(y=0, color="gray", linewidth=0.5)
        if ax is not axes[-1]:
            ax.tick_params(axis="x", which="both", bottom=False, labelbottom=False)

    if log_scale:
        # Filter ticks to within the shared x range so set_xticks doesn't widen
        # the axis past the data, matching the share_x_axis logic in distributional_plots.
        if x_axis_range is not None:
            ticks = [t for t in log_ticks if x_axis_range[0] <= t <= x_axis_range[1]]
        else:
            ticks = log_ticks
        axes[-1].set_xticks(ticks)
        axes[-1].get_xaxis().set_major_formatter(
            plt.FuncFormatter(lambda v, _: f"${v:g}")
        )
    if x_axis_range is not None:
        axes[-1].set_xlim(*x_axis_range)
    axes[-1].set_xlabel(f"Income or consumption ({period})")

    # Lay out first so axes positions are stable before placing the spanning lines.
    fig.tight_layout()
    reference_labels: list[tuple[float, str, str, str]] = []
    if add_ipl == "line":
        _add_figure_spanning_vline(
            fig, axes, ipl, color="lightgrey", linestyle=":", linewidth=0.8
        )
        reference_labels.append(
            (
                ipl,
                "International Poverty Line",
                f"${ipl:.{dollar_decimals}f} per {period}",
                "right",
            )
        )
    if add_high_income_pl == "line":
        _add_figure_spanning_vline(
            fig, axes, high_income_pl, color="lightgrey", linestyle=":", linewidth=0.8
        )
        reference_labels.append(
            (
                high_income_pl,
                "High-income poverty line",
                f"${high_income_pl:.{dollar_decimals}f} per {period}",
                "left",
            )
        )
    _add_figure_spanning_vline_labels(fig, axes, reference_labels)

    for o in fig.findobj():
        o.set_clip_on(False)

    fig.savefig(
        PARENT_DIR / f"{country}_per_year_row_log_{log_scale}{filename_suffix}.svg",
        bbox_inches="tight",
    )
    plt.close(fig)


def _stacked_year_rows(
    data: pd.DataFrame,
    x: str,
    weights: str,
    hue: str,
    subdivide_hue: str,
    years: List[int],
    log_scale: bool = True,
    multiple: str = "stack",
    common_norm: bool = True,
    gridsize: int = 200,
    period: Literal["day", "month", "year"] = "day",
    add_ipl: Literal["line", "area", None] = "line",
    add_high_income_pl: Literal["line", "area", None] = None,
    width: int = WIDTH,
    height: int = HEIGHT,
    add_fade_in_tails: bool = True,
    percentiles_to_fade: List[float] = [1, 99],
    filename_suffix: str = "",
    share_x_axis: bool = True,
    share_y_axis: bool = True,
) -> None:
    """Private helper for ``distributional_plots_per_row(row_by="year",
    subdivide_hue=...)``: the all-countries hierarchical stack (stack by
    ``subdivide_hue``, colour by parent ``hue``) laid out one row per year,
    sharing both axes. Mirrors ``distributional_plots(subdivide_hue=...)`` but
    stacked as rows in a single figure instead of one SVG per year.
    """
    period_factor = cast(int, PERIOD_VALUES[period]["factor"])
    log_ticks = cast(List[int], PERIOD_VALUES[period]["log_ticks"])
    dollar_decimals = 2 if period == "day" else 0
    ipl = INTERNATIONAL_POVERTY_LINE * period_factor
    high_income_pl = POVERTY_LINE_HIGH_INCOME * period_factor

    data = data[data["year"].isin(years)].copy()
    data[x] = data[x] * period_factor

    region_order, region_palette, palette = _subdivide_palette(data, hue, subdivide_hue)

    def _fade(sub: pd.DataFrame) -> pd.DataFrame:
        if not add_fade_in_tails:
            return sub
        if "percentile" in sub.columns:
            pq, bounds = "percentile", percentiles_to_fade
        elif "quantile" in sub.columns:
            pq, bounds = "quantile", [p * 10 for p in percentiles_to_fade]
        else:
            return sub
        return sub[(sub[pq] > bounds[0]) & (sub[pq] < bounds[1])]

    # Pre-pass: shared x range = union across years of each year's pooled data,
    # extended by cut*bw in log10 space (mirrors the other share_x_axis logic).
    x_axis_range: tuple | None = None
    if log_scale:
        x_min, x_max = float("inf"), float("-inf")
        for year in years:
            sub = _fade(data[data["year"] == year])
            if not len(sub):
                continue
            v = np.log10(sub[x].to_numpy(dtype=float))
            w = sub[weights].to_numpy(dtype=float)
            mean_v = float(np.average(v, weights=w))
            std_v = float(np.sqrt(max(np.average((v - mean_v) ** 2, weights=w), 0.0)))
            w_sum, w_sq = float(w.sum()), float((w * w).sum())
            n_eff = (w_sum * w_sum / w_sq) if w_sq > 0 else 1.0
            bw = std_v * n_eff ** (-1 / 5) if n_eff > 0 else 0.0
            cut = 3  # seaborn default
            x_min = min(x_min, float(sub[x].min()) / 10 ** (cut * bw))
            x_max = max(x_max, float(sub[x].max()) * 10 ** (cut * bw))
        if x_min < float("inf"):
            x_axis_range = (x_min, x_max)

    clip_param = (
        (np.log(x_axis_range[0]), np.log(x_axis_range[1]))
        if log_scale and x_axis_range is not None
        else None
    )

    fig, axes = plt.subplots(
        nrows=len(years),
        ncols=1,
        figsize=(width / 100, height / 100 * len(years)),
        sharex=share_x_axis,
        sharey=share_y_axis,
    )
    if len(years) == 1:
        axes = [axes]

    for ax, year in zip(axes, years):
        data_year = _fade(data[data["year"] == year])
        # Stack the countries of each region (largest population on top), all
        # sharing their region's colour; separators are each band's region
        # colour at full opacity, applied after plotting (_apply_subdivide_edges).
        order = _subdivide_order(data_year, hue, subdivide_hue, weights, region_order)
        sns.kdeplot(
            data=data_year,
            x=x,
            weights=weights,
            fill=True,
            log_scale=log_scale,
            hue=subdivide_hue,
            hue_order=order,
            palette=palette,
            multiple=multiple,
            legend=False,
            common_norm=common_norm,
            gridsize=gridsize,
            clip=clip_param,
            linewidth=SUBDIVIDE_EDGE_LINEWIDTH,
            ax=ax,
        )
        _apply_subdivide_edges(ax)
        if x_axis_range is not None:
            ax.set_xlim(*x_axis_range)
        # Year label at the top-left of each row.
        ax.text(
            x=x_axis_range[0] if x_axis_range is not None else 1.0,
            y=ax.get_ylim()[1],
            s=str(year),
            color="black",
            va="top",
            ha="left",
            fontsize=11,
            fontweight="bold",
        )
        ax.set_ylabel("")
        ax.yaxis.set_ticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.axhline(y=0, color="gray", linewidth=0.5)
        if ax is not axes[-1]:
            ax.tick_params(axis="x", which="both", bottom=False, labelbottom=False)

    if log_scale:
        ticks = (
            [t for t in log_ticks if x_axis_range[0] <= t <= x_axis_range[1]]
            if x_axis_range is not None
            else log_ticks
        )
        axes[-1].set_xticks(ticks)
        axes[-1].get_xaxis().set_major_formatter(
            plt.FuncFormatter(lambda v, _: f"${v:g}")
        )
    if x_axis_range is not None:
        axes[-1].set_xlim(*x_axis_range)
    axes[-1].set_xlabel(f"Income or consumption ({period})")

    # Lay out first so axes positions are stable before placing the spanning lines.
    fig.tight_layout()

    reference_labels: list[tuple[float, str, str, str]] = []
    if add_ipl == "line":
        _add_figure_spanning_vline(
            fig, axes, ipl, color="lightgrey", linestyle=":", linewidth=0.8
        )
        reference_labels.append(
            (
                ipl,
                "International Poverty Line",
                f"${ipl:.{dollar_decimals}f} per {period}",
                "right",
            )
        )
    if add_high_income_pl == "line":
        _add_figure_spanning_vline(
            fig, axes, high_income_pl, color="lightgrey", linestyle=":", linewidth=0.8
        )
        reference_labels.append(
            (
                high_income_pl,
                "High-income poverty line",
                f"${high_income_pl:.{dollar_decimals}f} per {period}",
                "left",
            )
        )
    _add_figure_spanning_vline_labels(fig, axes, reference_labels)

    # Region legend on the top row; match swatch opacity to the rendered fills.

    fill_alpha = (
        float(axes[0].collections[0].get_facecolor()[0][3])
        if len(axes[0].collections)
        else 1.0
    )
    handles = [
        Patch(facecolor=region_palette[region], label=region, alpha=fill_alpha)
        for region in region_order
    ]
    axes[0].legend(
        handles=handles,
        title=hue.capitalize(),
        loc="upper left",
        bbox_to_anchor=(0.8, 0.8),
        fontsize=7,
    )

    for o in fig.findobj():
        o.set_clip_on(False)

    fig.savefig(
        PARENT_DIR / f"all_countries_per_year_row_log_{log_scale}{filename_suffix}.svg",
        bbox_inches="tight",
    )
    plt.close(fig)


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
            # Customize y-axis ticks to show 1, 2, 5, 10, 20, 50, 100, etc.,
            # filtered to the visible range so low ticks only appear where the
            # data reaches them (otherwise set_yticks would widen the axis).
            line_plot.set_yscale("log")
            lo, hi = line_plot.get_ylim()
            line_plot.set_yticks([t for t in log_ticks if lo <= t <= hi])
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

            # International Poverty Line
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
        line_plot.set_xlabel("Percentage of the population")
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

            # Obtain the x and y data of the line. Coerce to ndarray because
            # `Line2D.get_data` returns whatever was originally set — sometimes
            # a plain list — and the `<=` comparison below requires array math.
            x_line = np.asarray(line.get_data()[0], dtype=float)
            y_line = np.asarray(line.get_data()[1], dtype=float)

            # Build the polygon explicitly so it terminates at exactly x=value.
            # matplotlib's `where=(x_line <= value)` with `interpolate=True` only
            # interpolates `y1` vs `y2` crossings, not the where boundary on x —
            # so without this manual construction the polygon snaps to the last
            # grid point ≤ value, leaving a visible gap between the fill edge
            # and the reference line at x=value.
            order = np.argsort(x_line)
            xs_sorted = x_line[order]
            ys_sorted = y_line[order]
            if xs_sorted.size == 0 or value <= xs_sorted[0]:
                continue
            inside = xs_sorted < value
            if inside.any():
                fill_xs = np.append(xs_sorted[inside], value)
                fill_ys = np.append(
                    ys_sorted[inside],
                    float(np.interp(value, xs_sorted, ys_sorted)),
                )
            else:
                # Entire grid is at or past `value` — nothing to fill.
                continue
            kde_plot.fill_between(
                x=fill_xs,
                y1=0,
                y2=fill_ys,
                alpha=0.3,
                color=line.get_color(),
                linewidth=0,
            )

    return None


def _add_figure_spanning_vline(fig, axes, x, **kwargs) -> None:
    """Draw a single dashed vertical line across every stacked subplot.

    Per-axis ``ax.axvline(...)`` leaves a visible gap between subplots
    (the per-axes line is clipped to its data area). This helper instead
    adds a Line2D in a blended transform — data x from ``axes[0]``, figure-
    fraction y — so the line spans from the bottom of the last axes to the
    top of the first axes uninterrupted.
    """
    trans = blended_transform_factory(axes[0].transData, fig.transFigure)
    y_top = axes[0].get_position().y1
    y_bottom = axes[-1].get_position().y0
    line = Line2D([x, x], [y_bottom, y_top], transform=trans, **kwargs)
    fig.add_artist(line)


def _styled_reference_label(
    parent,
    x,
    y,
    title: str,
    value: str,
    ha: str,
    xycoords="data",
    box_alignment=None,
) -> None:
    """Render a reference-line label as a bold *title* (one or more lines,
    separated by ``\\n``) stacked above a regular-weight *value* line.

    ``parent`` is any matplotlib artist container that accepts ``add_artist``
    (an Axes or a Figure). ``x``/``y`` are in the coordinate system named by
    ``xycoords`` ("data", "axes fraction", "figure fraction", etc.). ``ha``
    determines the horizontal alignment of each text row and whether the
    label sits to the left ("right") or to the right ("left") of the anchor.
    """
    common = {
        "color": "grey",
        "fontsize": 8,
        "ha": ha,
        "multialignment": ha,
    }
    children = [
        TextArea(line, textprops={**common, "fontweight": "bold"})
        for line in title.split("\n")
    ]
    children.append(TextArea(value, textprops=common))
    packer = VPacker(children=children, align=ha, pad=0, sep=2)
    if box_alignment is None:
        # Anchor by the bottom edge, and by the left or right edge depending on ha.
        box_alignment = (1.0 if ha == "right" else 0.0, 0.0)
    annotation = AnnotationBbox(
        packer,
        (x, y),
        xycoords=xycoords,
        box_alignment=box_alignment,
        frameon=False,
        pad=0,
    )
    parent.add_artist(annotation)


def _add_figure_spanning_vline_labels(fig, axes, labels) -> None:
    """Place a batch of figure-spanning reference-line labels at the same
    vertical level. ``labels`` is an iterable of ``(x, title, value, ha)``
    tuples — ``title`` is rendered bold (use ``\\n`` for multi-line titles)
    and ``value`` is rendered regular weight on the line below. ``ha``
    controls each label's horizontal alignment ("left" puts text to the
    right of the line, "right" puts text to the left of the line).

    If any label's x lands in a region where the topmost curve leaves less
    than half the axes height free above it (e.g. Ethiopia at the IPL), ALL
    labels in the batch are placed *above* axes[0] (anchored in figure
    fraction y) so they line up. Otherwise (e.g. Sweden 1820 at the IPL)
    they all hang from the top edge of axes[0].
    """
    label_list = list(labels)
    if not label_list:
        return

    ax = axes[0]
    use_outside = False
    if ax.lines:
        xs = np.asarray(ax.lines[0].get_data()[0])
        ys = np.asarray(ax.lines[0].get_data()[1])
        if xs.size and ys.size:
            order = np.argsort(xs)
            ylim_max = ax.get_ylim()[1]
            for x, *_ in label_list:
                y_at_x = float(np.interp(x, xs[order], ys[order]))
                if ylim_max > 0 and y_at_x > 0.5 * ylim_max:
                    use_outside = True
                    break

    if use_outside:
        trans = blended_transform_factory(ax.transData, fig.transFigure)
        y_anchor = ax.get_position().y1 + 0.005
        parent = fig
        xycoords = trans
    else:
        trans = blended_transform_factory(ax.transData, ax.transAxes)
        y_anchor = 1.0
        parent = ax
        xycoords = trans

    for x, title, value, ha in label_list:
        _styled_reference_label(
            parent,
            x,
            y_anchor,
            title=title,
            value=value,
            ha=ha,
            xycoords=xycoords,
        )


def _add_figure_spanning_vline_label(
    fig, axes, x, title, value, ha: str = "left"
) -> None:
    """Single-label convenience wrapper around :func:`_add_figure_spanning_vline_labels`."""
    _add_figure_spanning_vline_labels(fig, axes, [(x, title, value, ha)])


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
