import pandas as pd
import requests

# Cancer Today - Modelled estimates of current death rates of cancer in all countries: https://gco.iarc.fr/today/home

# We download the data for lung cancer death rates in men and women (per 100k)
url_now_male = "https://gco.iarc.fr/api/globocan/v2/2020/data/population/1/0/all/15/?sort=asr&grouped=1&ages_group=0_17&grouping_cancer=0&include_nmsc=0&include_nmsc_other=0&sex=1"
df_now_male = pd.read_json(url_now_male)
df_now_male["year"] = 2020
df_now_male = df_now_male[["label", "year", "asr"]].rename(
    columns={"asr": "asrMen_now"}
)

url_now_female = "https://gco.iarc.fr/api/globocan/v2/2020/data/population/1/0/all/15/?sort=asr&grouped=1&ages_group=0_17&grouping_cancer=0&include_nmsc=0&include_nmsc_other=0&sex=2"
df_now_female = pd.read_json(url_now_female)
df_now_female["year"] = 2020
df_now_female = df_now_female[["label", "year", "asr"]].rename(
    columns={"asr": "asrWomen_now"}
)

# This combines the male and female datasets
df_now_both = df_now_male.merge(df_now_female, on=["label", "year"])

df_now_both.to_csv(
    "FionaSpooner/lung_cancer_deaths/data/input/cancer_today_input.csv", index=False
)

# Cancer Over Time - Data taken from WHO Mortality Database, only available for countries with good data: https://gco.iarc.fr/overtime/en
# First we download the data in JSON format
url_time = "https://gco.iarc.fr/gateway_prod/api/overtime/v2/10//data/population/1/1_2/10000_75200_3200_3600_4000_5600_7600_12400_15200_17000_18800_19100_19200_20300_20800_21800_23300_24600_25000_27600_30000_34800_35200_37200_37600_38000_39200_41000_41700_42800_44000_47000_48400_52800_55400_57800_61600_62000_64200_70200_70300_70500_72400_75600_82600_84000_82630_82610_82620_84001_84002_85800/(11)/?ages_group=0_17&year_start=1943&year_end=2018"
res = requests.get(url_time)
json_data = res.json()

df_time = pd.json_normalize(json_data["dataset"])
df_time.to_csv(
    "FionaSpooner/lung_cancer_deaths/data/input/cancer_over_time_input.csv", index=False
)

# Pull out only the columns we want
df_sel = df_time[["label", "year", "asr", "sex"]]
# Replace the valuables in the 'sex' column with more meaningful values 1 -> Men, 2-> Women
df_sel.replace([1, 2], ["Men", "Women"], inplace=True)

# Pivot the table so we have separate columns for men and women
df_piv = df_sel.pivot_table(
    index=["label", "year"], columns=["sex"], values=["asr"]
).reset_index()

# Sort out the multi-index columns
df_piv.columns = ["".join(a) for a in df_piv.columns.to_flat_index()]

# Combine the Over Time and Today datasets
df_now_time = pd.concat([df_piv, df_now_both])

# Standardise the country names
df_now_time.drop_duplicates().rename(columns={"label": "Country"})["Country"].to_csv(
    "FionaSpooner/lung_cancer_deaths/data/input/globocan_entities_to_standardize.csv",
    index=False,
)

countries = pd.read_csv(
    "FionaSpooner/lung_cancer_deaths/data/input/globocan_entities_to_standardize_country_standardized.csv"
).drop_duplicates()

# Tidy the column names
df_fin = df_now_time.merge(
    countries, left_on="label", right_on="Country", how="left"
).rename(
    columns={
        "Our World In Data Name": "entity",
        "asrMen": "male_mortality_rate_lung_cancer_per_100k",
        "asrWomen": "female_mortality_rate_lung_cancer_per_100k",
        "asrMen_now": "modelled_male_mortality_rate_lung_cancer_per_100k",
        "asrWomen_now": "modelled_female_mortality_rate_lung_cancer_per_100k",
    }
)[
    [
        "entity",
        "year",
        "male_mortality_rate_lung_cancer_per_100k",
        "female_mortality_rate_lung_cancer_per_100k",
        "modelled_male_mortality_rate_lung_cancer_per_100k",
        "modelled_female_mortality_rate_lung_cancer_per_100k",
    ]
]

# Round the values to 2 d.p.
df_fin[
    [
        "male_mortality_rate_lung_cancer_per_100k",
        "female_mortality_rate_lung_cancer_per_100k",
        "modelled_male_mortality_rate_lung_cancer_per_100k",
        "modelled_female_mortality_rate_lung_cancer_per_100k",
    ]
] = round(
    df_fin[
        [
            "male_mortality_rate_lung_cancer_per_100k",
            "female_mortality_rate_lung_cancer_per_100k",
            "modelled_male_mortality_rate_lung_cancer_per_100k",
            "modelled_female_mortality_rate_lung_cancer_per_100k",
        ]
    ],
    2,
)


# Adding columns which have the Cancer Over Time and Cancer Today datasets combined
df_fin["combined_male_mortality_rate_lung_cancer_per_100k"] = df_fin[
    "male_mortality_rate_lung_cancer_per_100k"
].fillna(df_fin["modelled_male_mortality_rate_lung_cancer_per_100k"])

df_fin["combined_female_mortality_rate_lung_cancer_per_100k"] = df_fin[
    "female_mortality_rate_lung_cancer_per_100k"
].fillna(df_fin["modelled_female_mortality_rate_lung_cancer_per_100k"])

# Write out the data
df_fin.to_csv(
    "FionaSpooner/lung_cancer_deaths/data/output/globocan_over_time_mortality_rate.csv",
    index=False,
)
