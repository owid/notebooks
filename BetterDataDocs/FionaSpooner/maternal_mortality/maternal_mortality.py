#%%[markdown]

# The definition of maternal mortality is:

# > "A death of a woman while pregnant or within 42 days of termination of pregnancy, irrespective of the duration and site of pregnancy, from any cause related or aggravated by the pregnancy or its management, but not from accidental or incidental causes."

# The definition of maternal mortality ratio is:
# > "The number of maternal deaths during a given time period per 100,000 live births during the same time period."


# In this notebook we will create a long-term time-series of maternal mortality ratio. To do this we will combine two existing datasets:

# * GapMinder (1751-2008)
# * World Health Organization (2000-2017)

# We make the assumption that their methods are comparable and that the data can be combined without transformation.

# In years where there is an overlap in both time-series we use the data from the WHO.

# ## Downloading the GapMinder data

#%%
import numpy as np
import pandas as pd
import requests
from pathlib import Path
import zipfile

#%%[markdown]

# Firstly we download the data from GapMinder and save it locally. Then we read in the GapMinder data, clean up the column names and take a look at the data.


#%%

r = requests.get("https://www.gapminder.org/documentation/documentation/gapdata010.xls")

Path("data/input/").mkdir(parents=True, exist_ok=True)
output = open("data/input/gapminder.xls", "wb")
output.write(r.content)
output.close()


#%%
df = pd.read_excel("data/input/gapminder.xls")
df_d = df.drop(df.index[0:16]).reset_index()
df_d["Country"] = df_d["Country"].str.strip()
df_d = df_d[~pd.isna(df_d["MMR"])]

#%%[markdown]
## Cleaning the GapMinder data


# There are some issues with the GapMinder data - we will manually clean them here.


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

df_d = df_d.drop(df_d[(df_d["year"] == 1990) & (df_d["Country"] == "Sri Lanka")].index)

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


#%%
assert (
    df_d[["Country", "year"]][df_d[["Country", "year"]].duplicated(keep=False)].shape[0]
    == 0
)

#%%[markdown]
# ## Finding the mid-point of each year range

# For some rows a range of years is given for a particular maternal mortality rate. We want to find the mid-point of that range. We use this function to find the mid-value of years given.


#%%
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


#%%

df_years = df_d["year"].apply(get_mid_year)
df_d["year_begin"] = df_years[0].astype(int)
df_d["mid_year"] = df_years[1].astype(int)

df_d[df_d["year_begin"] > df_d["mid_year"]]


#%%
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
# Standardise the country names.
#%%
stand_countries = pd.read_csv(
    "data/input/countries_to_standardise_country_standardized.csv"
)
stan_dict = stand_countries.set_index("Country").squeeze().to_dict()
df_gap["entity"] = df_gap["entity"].map(stan_dict)

#%%[markdown]

# ## Reading in the WHO data

# Read in data from WDI - in future iterations we will read this in from ETL so it is auto updated. The WDI sources this variable from the WHO so we will henceforth refer to it as the WHO data.

#%%
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
# Pivot and clean the WHO data and standardise the country names.
#%%
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

#%%[markdown]
# ## Merging the WHO data with the GapMinder data

# Combine the two datasets. For years where there is data from both datasets we preferentially keep data from the WHO.

#%%
df = pd.concat([df_gap, who_df], ignore_index=True)
df["year"] = df["year"].astype(int)
df = df.dropna()
# Arranging by source so the WHO data is last
df = df.sort_values(by=["source"])
df = df.drop_duplicates(subset=["entity", "year"], keep="last")

#%%[markdown]
# ## Cleaning geographic entities
# We don't want to include all of the available regions in the data as it is difficult for us to define them clearly, so we drop out a selection here.
#%%
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
