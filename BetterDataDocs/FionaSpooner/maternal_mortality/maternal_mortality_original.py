# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     custom_cell_magics: kql
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.2
#   kernelspec:
#     display_name: Python 3.10.4 64-bit ('3.10.4')
#     language: python
#     name: python3
# ---

# %%
#%%[markdown]

# The definition of maternal mortality is:

# > "A death of a woman while pregnant or within 42 days of termination of pregnancy, irrespective of the duration and site of pregnancy, from any cause related or aggravated by the pregnancy or its management, but not from accidental or incidental causes."

#
#
# The definition of maternal mortality ratio is:
# > "The number of maternal deaths during a given time period per 100,000 live births during the same time period."


# In this notebook we will create a long-term time-series of maternal mortality ratio. To do this we will combine two existing datasets:

# * Gapminder (1751-2008)
# * World Health Organization (2000-2017)


#
# We make the assumption that their methods are comparable and that the data can be combined without transformation.

# In years where there is an overlap in both time-series we use the data from the WHO.

# ## Downloading the Gapminder data

# %%
import numpy as np
import pandas as pd
import requests
from pathlib import Path
import zipfile
import matplotlib.pyplot as plt

#%%[markdown]

# Firstly we download the data from Gapminder and save it locally. Then we read in the Gapminder data, clean up the column names and take a look at the data.


# %%

r = requests.get("https://www.gapminder.org/documentation/documentation/gapdata010.xls")

Path("data/input/").mkdir(parents=True, exist_ok=True)
output = open("data/input/gapminder.xls", "wb")
output.write(r.content)
output.close()


# %%
df = pd.read_excel("data/input/gapminder.xls")
df_d = df.drop(df.index[0:16]).reset_index()
df_d["Country"] = df_d["Country"].str.strip()
df_d = df_d[~pd.isna(df_d["MMR"])]

#%%[markdown]
## Cleaning the Gapminder data


# There are some issues with the Gapminder data - we will manually clean them here.


# * The first three rows in the 'year' column seem to be wrong as it seems as if each row covers 110 years, but in [another source](https://docs.google.com/spreadsheets/u/0/d/14ZtQy9kd0pMRKWg_zKsTg3qKHoGtflj-Ekal9gIPZ4A/pub?gid=1#) they cover only 10 years.

# * I will replace them manually here with the middle of each decade, as is used in the other data from the same source.

# * There are cases where the year for Finland has been entered incorrectly three times, there are two 1772s, 1775s & 1967s, the second of each should be 1872, 1875 and 1957 respectively.

# * There are also two errors for New Zealand, and one error for both Sweden and the US.

# * Sri Lanka's maternal mortality rate seems to drop to zero in 1990, we will drop this value.


# %%
df_d.loc[:2, "year"] = ["1875", "1885", "1895"]

df_d.loc[
    (df_d["year"] == 1772)
    & (df_d["Country"] == "Finland")
    & (df_d["Maternal deaths"] == 487),
    "year",
] = 1872
df_d.loc[
    (df_d["year"] == 1775)
    & (df_d["Country"] == "Finland")
    & (df_d["Maternal deaths"] == 629),
    "year",
] = 1875
df_d.loc[
    (df_d["year"] == 1967)
    & (df_d["Country"] == "Finland")
    & (df_d["Maternal deaths"] == 77),
    "year",
] = 1957
df_d.loc[
    (df_d["year"] == 1967)
    & (df_d["Country"] == "Sweden")
    & (df_d["Maternal deaths"] == 39),
    "year",
] = 1957
df_d.loc[
    (df_d["year"] == 1967)
    & (df_d["Country"] == "United States")
    & (df_d["Maternal deaths"] == 1766.28),
    "year",
] = 1957

# Drop any rows where MMR is zero or '...' (Ireland, Denmark and Sri Lanka)
df_d = df_d.drop(df_d[(df_d["MMR"] == 0) | (df_d["MMR"] == "...")].index)


df_d = df_d.drop(
    df_d[
        (df_d["Country"] == "New Zealand")
        & (df_d["year"] == 1950)
        & (df_d["MMR"] == 90)
    ].index
)

# Duplicates after get_mid_year()
df_d = df_d.drop(
    df_d[
        (df_d["year"].isin(["1989-02", "1899-03"])) & (df_d["Country"] == "New Zealand")
    ].index
)
# %%
# Check that there are no duplicates in the data.


# %%
assert (
    df_d[["Country", "year"]][df_d[["Country", "year"]].duplicated(keep=False)].shape[0]
    == 0
)

#%%[markdown]
# ## Finding the mid-point of each year range

# For some rows a range of years is given for a particular maternal mortality rate. We want to find the mid-point of that range. We use this function to find the mid-value of years given.


# %%
df_d.columns

# %% [markdown]
# Checking the given MMR matches a calculated MMR, where the data for live births and maternal deaths is given. It seems largely okay but the values for Ireland, particularly from 1901-1920. There is a drop of almost 1000 maternal deaths between 1920 and 1922.
#
# In the registrar general of Ireland it states that there were approximately 599 maternal deaths in Ireland in 1912 and on average 634 per year between 1903 and 1911. The estimated rate is 6 deaths per 1,000 births, so 600 per 100,000 births.
#
# I think this suggests that the Maternal deaths figures may be wrong for the period 1901-1920.

# %%
df_check = (
    df_d[["Country", "year", "Live Births", "Maternal deaths", "MMR"]]
    .dropna()
    .reset_index(drop=True)
)
df_check["mmr_calc"] = (
    ((df_check["Maternal deaths"] / df_check["Live Births"]) * 100000)
    .astype(float)
    .round(2)
)
df_check["MMR"] = df_check["MMR"].astype(float).round(2)


df_check[df_check["mmr_calc"].round(2) != df_check["MMR"].round(2)]


# %%
def get_mid_year(year: str):
    if "-" in str(year):
        year_begin = year.split("-")[0]
        year_end = year.split("-")[1]
        year_end_len = len(year.split("-")[1])
        year_end_pref = 4 - year_end_len
        if year_end_pref > 0:
            year_pref = year_begin[0:year_end_pref]
            year_end = year_pref + year_end
            year_out = int(np.mean([int(year_begin), int(year_end)]))
        else:
            year_out = int(np.mean([int(year_begin), int(year_end)]))
    else:
        year_begin = int(year)
        year_out = int(year)

    return pd.Series([year_begin, year_out])


#%%[markdown]

# Let's check the mid-year estimates have worked as expected. There is one case where the mid-year estimate is not the mid-point of the range of years. Let's fix this manually.


# %%

df_years = df_d["year"].apply(get_mid_year)
df_d["year_begin"] = df_years[0].astype(int)
df_d["mid_year"] = df_years[1].astype(int)

df_d[df_d["year_begin"] > df_d["mid_year"]]


# %%
df_d.loc[
    (df_d["year"] == "1897-01") & (df_d["Country"] == "New Zealand"), "mid_year"
] = 1899
assert df_d[df_d[["Country", "year"]].duplicated(keep=False)].shape[0] == 0

#%%[markdown]
# Rename the columns and keep only the columns we are interested in.


# %%
df_d = df_d.copy(deep=False)
df_d["year"] = df_d["mid_year"]

df_gap = df_d[["Country", "year", "MMR"]]
df_gap["source"] = "gapminder"
df_gap.rename(
    columns={"Country": "entity", "MMR": "maternal_mortality_rate"}, inplace=True
)


#%%[markdown]
# Standardise the country names and drop rows with NA values.
# %%
stand_countries = pd.read_csv(
    "data/input/countries_to_standardise_country_standardized.csv"
)
stan_dict = stand_countries.set_index("Country").squeeze().to_dict()
df_gap["entity"] = df_gap["entity"].map(stan_dict)
df_gap = df_gap.dropna()
#%%[markdown]

# ## Reading in the WHO data

# Read in data from WDI - in future iterations we will read this in from ETL so it is auto updated. The WDI sources this variable from the WHO so we will henceforth refer to it as the WHO data.
# This data covers from the year 2000 onwards. A previous version had data from the year 1990 onwards, we will also read this in and use this preferentially over the GapMinder data.

# %%
r_who = requests.get(
    "https://api.worldbank.org/v2/en/indicator/SH.STA.MMRT?downloadformat=csv"
)
output = open("data/input/who_mmr.zip", "wb")
output.write(r_who.content)
output.close()
with zipfile.ZipFile("data/input/who_mmr.zip", "r") as zip_ref:
    zip_ref.extractall("data/input/who_mmr")
who = pd.read_csv(
    "data/input/who_mmr/API_SH.STA.MMRT_DS2_en_csv_v2_4252399.csv", skiprows=4
)

#%%[markdown]
## Cleaning the WHO data
# Pivot and clean the WHO data and standardise the country names and drop values with NA values.

# %%
year_cols = list(range(1960, 2022))
year_cols = [str(int) for int in year_cols]

who_df = pd.melt(who, id_vars=["Country Name"], value_vars=year_cols)
who_df.rename(
    columns={
        "Country Name": "entity",
        "variable": "year",
        "value": "maternal_mortality_rate",
    },
    inplace=True,
)
who_df["source"] = "who"
who_df["entity"] = who_df["entity"].map(stan_dict)
who_df = who_df.dropna()
#%%[markdown]
# ## Merging the WHO data with the Gapminder data

# Combine the two datasets. For years where there is data from both datasets we preferentially keep data from the WHO.

# %% [markdown]
# Add in the OECD Stat Health data

# %%
oecd_df = pd.read_csv("data/input/HEALTH_STAT_21072022104153993.csv")
oecd_df = oecd_df[["Country", "Year", "Value"]].rename(
    columns={"Country": "entity", "Year": "year", "Value": "maternal_mortality_rate"}
)
oecd_df["source"] = "oecd"

oecd_df["entity"] = oecd_df["entity"].map(stan_dict)


# %% [markdown]
# Get the first years data from WHO and the last years data from Gapminder - to compare the values when the source changes.

# %%
who_2015 = pd.read_csv("data/input/maternal-mortality_wb_2015.csv")
who_2015["source"] = "who"
who_2015 = who_2015[
    [
        "Entity",
        "Year",
        "Maternal Mortality Ratio (Gapminder (2010) and World Bank (2015))",
        "source",
    ]
].rename(
    columns={
        "Entity": "entity",
        "Year": "year",
        "Maternal Mortality Ratio (Gapminder (2010) and World Bank (2015))": "maternal_mortality_rate",
    }
)
who_2015 = who_2015[(who_2015["year"] < 2000) & (who_2015["year"] >= 1990)]

# %%
df = pd.concat([df_gap, who_2015, who_df, oecd_df], ignore_index=True)
df["year"] = df["year"].astype(int)
df


# %% [markdown]
# Get the first years data from WHO and the last years data from GapMinder - to compare the values when the source changes.
#

# %%
df_gap.sort_values(by=["entity", "year"], inplace=True)
df_gap_gr = df_gap.groupby("entity")
who_df.sort_values(by=["entity", "year"], inplace=True)
who_df_gr = who_df.groupby("entity")

first_last_df = (
    pd.concat([who_df_gr.head(1), df_gap_gr.tail(1)])
    .drop_duplicates()
    .reset_index(drop=True)
    .dropna()
)

# %% [markdown]
# We want to look at countries which feature in both datasets.
#

# %%
df_c = first_last_df.entity.value_counts()
first_last_df = first_last_df[
    first_last_df.entity.isin(df_c.index[df_c.gt(1)])
].sort_values(by=["entity", "year"], ascending=[True, False])

# %%
df_dup = df[(df.entity.isin(first_last_df.entity)) & (df.year >= 1970)]


# %% [markdown]
# Plotting time-series of the data from 1985 onwards. GapMinder is shown in orange, WHO is shown in blue and OECD n green.
#

# %%
plt.figure(figsize=(10, 8), facecolor="white")

# plot numbering starts at 1, not 0
plot_number = 1
for countryname, selection in df_dup.groupby("entity"):
    # Inside of an image that's a 15x13 grid, put this
    # graph in the in the plot_number slot.
    ax = plt.subplot(5, 3, plot_number)
    selection_gap = selection[selection["source"] == "gapminder"]
    selection_who = selection[selection["source"] == "who"]
    selection_oecd = selection[selection["source"] == "oecd"]
    if selection_who.shape[0] > 0:
        selection_who.plot(
            x="year",
            y="maternal_mortality_rate",
            ax=ax,
            label=countryname,
            legend=False,
        )
    if selection_gap.shape[0] > 0:
        selection_gap.plot(
            x="year",
            y="maternal_mortality_rate",
            ax=ax,
            label=countryname,
            legend=False,
        )
    if selection_oecd.shape[0] > 0:
        selection_oecd.plot(
            x="year",
            y="maternal_mortality_rate",
            ax=ax,
            label=countryname,
            legend=False,
        )
    ax.set_title(countryname)
    # Go to the next plot for the next loop
    plot_number = plot_number + 1
plt.tight_layout()

# %%
#%%[markdown]
# ## Cleaning geographic entities
# We don't want to include all of the available regions in the data as it is difficult for us to define them clearly, so we drop out a selection here.
entities_to_drop = [
    "Africa Eastern and Southern",
    "Africa Western and Central",
    "Arab World",
    "Early-demographic dividend",
    "East Asia & Pacific (excluding high income)",
    "East Asia & Pacific (IDA & IBRD countries)",
    "Euro area",
    "Europe & Central Asia (excluding high income)",
    "Europe & Central Asia (IDA & IBRD countries)",
    "Fragile and conflict affected situations",
    "Heavily indebted poor countries (HIPC)",
    "IBRD only",
    "IDA & IBRD total",
    "IDA blend",
    "IDA only",
    "IDA total",
    "Late-demographic dividend",
    "Latin America & Caribbean (excluding high income)",
    "Latin America & the Caribbean (IDA & IBRD countries)",
    "Least developed countries: UN classification",
    "Middle East & North Africa (excluding high income)",
    "Middle East & North Africa (IDA & IBRD countries)",
    "Not classified",
    "Other small states",
    "Pacific island small states",
    "Post-demographic dividend",
    "Pre-demographic dividend",
    "Small states",
    "South Asia (IDA & IBRD)",
    "Sub-Saharan Africa (excluding high income)",
    "Sub-Saharan Africa (IDA & IBRD countries)",
]

df = df[~df["entity"].isin(entities_to_drop)]
df = df.dropna()
df = df[["entity", "year", "maternal_mortality_rate"]]
df.to_csv("data/output/maternal_mortality_rate.csv", index=False)
