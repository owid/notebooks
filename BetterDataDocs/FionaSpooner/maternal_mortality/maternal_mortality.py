# %%
import numpy as np
import pandas as pd
import requests
from pathlib import Path
import zipfile

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


# %%
df_d[["Country", "year"]][df_d[["Country", "year"]].duplicated(keep=False)]


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


# %%

df_years = df_d["year"].apply(get_mid_year)
df_d["year_begin"] = df_years[0].astype(int)
df_d["mid_year"] = df_years[1].astype(int)

df_d[df_d["year_begin"] > df_d["mid_year"]]


# %%
df_d.loc[
    (df_d["year"] == "1897-01") & (df_d["Country"] == "New Zealand"), "mid_year"
] = 1899

# %%
df_d[df_d[["Country", "year"]].duplicated(keep=False)]

# %%
df_d = df_d.copy(deep=False)
df_d["year"] = df_d["mid_year"]

df_gap = df_d[["Country", "year", "MMR"]]
df_gap["source"] = "gapminder"
df_gap.rename(
    columns={"Country": "entity", "MMR": "maternal_mortality_rate"}, inplace=True
)

#%%
stand_countries = pd.read_csv(
    "data/input/countries_to_standardise_country_standardized.csv"
)
stan_dict = stand_countries.set_index("Country").squeeze().to_dict()
df_gap["entity"] = df_gap["entity"].map(stan_dict)

#%%[markdown]

# Reading in the WHO data

# %%
r_who = requests.get(
    "https://api.worldbank.org/v2/en/indicator/SH.STA.MMRT?downloadformat=csv"
)
output = open("data/input/who_mmr.zip", "wb")
output.write(r_who.content)
output.close()
with zipfile.ZipFile("data/input/who_mmr.zip", "r") as zip_ref:
    zip_ref.extractall("data/input/who_mmr")
# %%
who = pd.read_csv(
    "data/input/who_mmr/API_SH.STA.MMRT_DS2_en_csv_v2_4252399.csv", skiprows=4
)
# %%
year_cols = list(range(1960, 2022))
year_cols = [str(int) for int in year_cols]
# year_cols.insert(0,'Country Name')
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
# Combine the two datasets


# %%

df = df_gap.append(who_df)
# Check for duplicates
df[df[["entity", "year"]].duplicated(keep=False)]
# %%
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
