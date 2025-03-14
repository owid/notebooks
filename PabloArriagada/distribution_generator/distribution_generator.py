from pathlib import Path

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

# Define  version of PIP and 1000 bins data
PIP_VERSION = "2024-10-07"
THOUSAND_BINS_VERSION = "2025-03-10"

# Define URLs

THOUSAND_BINS_URL = f"http://catalog.ourworldindata.org/garden/wb/{THOUSAND_BINS_VERSION}/thousand_bins_distribution/thousand_bins_distribution.feather?nocache"
PERCENTILES_URL = f"http://catalog.ourworldindata.org/garden/wb/{PIP_VERSION}/world_bank_pip/percentiles_income_consumption_2017.feather?nocache"
MAIN_INDICATORS_URL = f"http://catalog.ourworldindata.org/garden/wb/{PIP_VERSION}/world_bank_pip/income_consumption_2017.feather?nocache"


# Read data
df_thousand_bins = pd.read_feather(THOUSAND_BINS_URL)
df_percentiles = pd.read_feather(PERCENTILES_URL)
df_main_indicators = pd.read_feather(MAIN_INDICATORS_URL)

# Use data from 2024
df_thousand_bins_2024 = df_thousand_bins[df_thousand_bins["year"] == 2024].reset_index(
    drop=True
)

# # Select Chile in df_thousand_bins_2024
# df_thousand_bins_2024 = df_thousand_bins_2024[
#     df_thousand_bins_2024["country"].isin(["Chile", "Peru", "United States"])
# ].reset_index(drop=True)


# Plot a kde with seaborn
kde_plot = sns.kdeplot(
    data=df_thousand_bins_2024,
    x="avg",
    fill=True,
    log_scale=True,
    hue="country",
    hue_order=["Chile", "Peru", "United States"],
    multiple="stack",
    legend=True,
)

# Customize x-axis ticks to show 1, 2, 5, 10, 20, 50, 100, etc.
# kde_plot.set(xscale="log")
kde_plot.set_xticks([1, 2, 5, 10, 20, 50, 100, 200, 500, 1000])
kde_plot.get_xaxis().set_major_formatter(plt.ScalarFormatter())

# Add a vertical line for the international poverty line
plt.axvline(
    x=INTERNATIONAL_POVERTY_LINE, color="lightgrey", linestyle="--", linewidth=0.8
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

# Move the legend inside the plot
kde_plot.legend_.set_bbox_to_anchor((0.8, 0.8))
kde_plot.legend_.set_loc("upper left")

fig = kde_plot.get_figure()
fig.set_size_inches(WIDTH / 100, HEIGHT / 100)
fig.savefig("out.svg")
