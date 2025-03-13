from pathlib import Path

import numpy as np
import pandas as pd
import seaborn as sns

PARENT_DIR = Path(__file__).parent.absolute()

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

# Select Chile in df_thousand_bins_2024
df_thousand_bins_chile = df_thousand_bins_2024[
    df_thousand_bins_2024["country"] == "Chile"
].reset_index(drop=True)

# Plot a kde with seaborn
sns.kdeplot(data=df_thousand_bins_chile["income"], fill=True)
