# Download and extract data from the appendix of this paper - https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5935243/
# Data extraction was carried out using Tabula app - column names were not included as these were formatted trickily

import pandas as pd

cols = [
    "Country",
    "rate_median_lt65",
    "rate_ci_lt_65",
    "rate_median_65_74",
    "rate_ci_65_74",
    "rate_median_gt_75",
    "rate_ci_gt_75",
    "number_median_lt65",
    "number_ci_lt_65",
    "number_median_65_74",
    "number_ci_65_74",
    "number_median_gt_75",
    "number_ci_gt_75",
]

df = pd.read_csv(
    "FionaSpooner/cdc_influenza/tabula-NIHMS962240-supplement-Appendix.csv", header=None
)

df.columns = cols

df = df.drop(
    columns=[
        "rate_ci_lt_65",
        "rate_ci_65_74",
        "rate_ci_gt_75",
        "number_ci_lt_65",
        "number_ci_65_74",
        "number_ci_gt_75",
    ]
)

med_cols = [
    "rate_median_lt65",
    "rate_median_65_74",
    "rate_median_gt_75",
    "number_median_lt65",
    "number_median_65_74",
    "number_median_gt_75",
]

df[med_cols] = (
    df[med_cols]
    .apply(lambda x: x.str.replace("\\u00b7", "."), axis=1)
    .apply(lambda x: x.str.replace(",", ""), axis=1)
)

df = df.dropna()
df.Country.to_csv("FionaSpooner/cdc_influenza/countries.csv", index=False)
### Standardize countries
countries_stan = pd.read_csv(
    "FionaSpooner/cdc_influenza/countries_country_standardized.csv"
)

df["Country"] = df["Country"].astype(str)
countries_stan["Country"] = countries_stan["Country"].astype(str)
df = df.merge(countries_stan, on="Country")
# Year is estimate for annual data between 1999 and 2015, except for swine flu years
df["year"] = 1999
cols_clean = [
    "Our World In Data Name",
    "year",
    "rate_median_lt65",
    "rate_median_65_74",
    "rate_median_gt_75",
    "number_median_lt65",
    "number_median_65_74",
    "number_median_gt_75",
]
df = df[cols_clean].rename(columns={"Our World In Data Name": "Country"})


df.to_csv("FionaSpooner/cdc_influenza/clean_cdc_influenza.csv", index=False)
