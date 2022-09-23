# Download file from https://data.oecd.org/healthcare/influenza-vaccination-rates.htm -
# click 'Download' and then select 'Full indicator data'


import pandas as pd

df = pd.read_csv("FionaSpooner/oecd_flu_vaccination/DP_LIVE_23092022095558878.csv")

df["Country"] = df["LOCATION"]
df = df.drop(columns=["LOCATION"])
df["Country"].to_csv("FionaSpooner/oecd_flu_vaccination/countries.csv", index=False)

country_stan = pd.read_csv(
    "FionaSpooner/oecd_flu_vaccination/countries_country_standardized.csv"
).drop_duplicates()

df = df.merge(country_stan, on="Country")

df = df[["Our World In Data Name", "TIME", "Value"]].rename(
    columns={
        "Our World In Data Name": "Country",
        "TIME": "Year",
        "Value": "Vaccination_rate_gt_65",
    }
)

df.to_csv("FionaSpooner/oecd_flu_vaccination/clean_oecd_vaccination.csv", index=False)
