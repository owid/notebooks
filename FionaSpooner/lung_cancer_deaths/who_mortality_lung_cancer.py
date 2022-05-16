import requests
import pandas as pd
import io

# https://platform.who.int/mortality/themes/theme-details/topics/indicator-groups/indicator-group-details/MDB/trachea-bronchus-lung-cancers

# Download the data from the WHO Mortality Database
res = requests.get(
    "https://apps.who.int/data/mortality/api/EN/facts/data-export?queryJson=eyJkYXRhRmlsdGVycyI6W3siZW50aXR5TmFtZSI6IkFnZUdyb3VwIiwib3JkZXJJbmRleCI6IjEiLCJ2YWx1ZXMiOlsiQWdlX2FsbCIsIkFnZTAwIiwiQWdlMDFfMDQiLCJBZ2UwNV8wOSIsIkFnZTEwXzE0IiwiQWdlMTVfMTkiLCJBZ2UyMF8yNCIsIkFnZTI1XzI5IiwiQWdlMzBfMzQiLCJBZ2UzNV8zOSIsIkFnZTQwXzQ0IiwiQWdlNDVfNDkiLCJBZ2U1MF81NCIsIkFnZTU1XzU5IiwiQWdlNjBfNjQiLCJBZ2U2NV82OSIsIkFnZTcwXzc0IiwiQWdlNzVfNzkiLCJBZ2U4MF84NCIsIkFnZTg1X292ZXIiLCJBZ2VfdW5rbm93biJdfSx7ImVudGl0eU5hbWUiOiJZZWFyIiwib3JkZXJJbmRleCI6IjIiLCJ2YWx1ZXMiOltdfSx7ImVudGl0eU5hbWUiOiJJbmRpY2F0b3IiLCJvcmRlckluZGV4IjoiMyIsInZhbHVlcyI6WyJDRzA2NzAiXX1dLCJkaXZpc2lvbkZhY3RvcnMiOltdLCJxdWVyeSI6W119&indicatorCode=CG0670",
    "data/input/trachea_bronchus_lung_cancer_mortality.csv",
)
res_con = res.content
df = pd.read_csv(io.StringIO(res_con.decode("utf-8")), skiprows=6)
# The columns are a little messed up, so we need to tidy them up
df_cols = df.columns.drop("Region Code")
df = df.iloc[:, :-1]
df.columns = df_cols
# Saving out the original data
df.to_csv(
    "FionaSpooner/lung_cancer_deaths/data/input/who_trachea_bronchus_lung_cancer_mortality.zip",
    index=False,
    compression="gzip",
)

# Filter out the data for all age groups, and only the columns we want
df_fil = df[df["Age group code"] == "Age_all"]

df_sel = df_fil[
    [
        "Country Name",
        "Year",
        "Sex",
        "Age-standardized death rate per 100 000 standard population",
    ]
]

# Pivoting the data so there is a column for male, female and all sexes
df_piv = df_sel.pivot_table(
    index=["Country Name", "Year"],
    columns=["Sex"],
    values=["Age-standardized death rate per 100 000 standard population"],
).reset_index()
df_piv.columns = ["_".join(a) for a in df_piv.columns.to_flat_index()]
df_piv.rename(
    columns={
        "Country Name_": "Country",
        "Year_": "year",
        "Age-standardized death rate per 100 000 standard population_All": "age-standardized_death_rate_per_100k_both_sexes",
        "Age-standardized death rate per 100 000 standard population_Female": "age-standardized_death_rate_per_100k_female",
        "Age-standardized death rate per 100 000 standard population_Male": "age-standardized_death_rate_per_100k_male",
    },
    inplace=True,
)

# Standardising the country names

df_piv["Country"].drop_duplicates().to_csv(
    "FionaSpooner/lung_cancer_deaths/data/input/who_mortality_countries_to_standardise.csv",
    index=False,
)

countries = pd.read_csv(
    "FionaSpooner/lung_cancer_deaths/data/input/who_mortality_countries_to_standardise_country_standardized.csv"
)

df_fin = df_piv.merge(countries, on="Country", how="left").rename(
    columns={"Our World In Data Name": "entity"}
)[
    [
        "entity",
        "year",
        "age-standardized_death_rate_per_100k_both_sexes",
        "age-standardized_death_rate_per_100k_female",
        "age-standardized_death_rate_per_100k_male",
    ]
]

# Rounding the rates to 2 d.p.
df_fin[
    [
        "age-standardized_death_rate_per_100k_both_sexes",
        "age-standardized_death_rate_per_100k_female",
        "age-standardized_death_rate_per_100k_male",
    ]
] = round(
    df_fin[
        [
            "age-standardized_death_rate_per_100k_both_sexes",
            "age-standardized_death_rate_per_100k_female",
            "age-standardized_death_rate_per_100k_male",
        ]
    ],
    2,
)

# Saving out the final data
df_fin.to_csv(
    "FionaSpooner/lung_cancer_deaths/data/output/who_age_standardized_trachea_bronchus_lung_cancer_mortality.csv",
    index=False,
)
