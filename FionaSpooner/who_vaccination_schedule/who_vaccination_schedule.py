import pandas as pd

# Data downloaded from - https://immunizationdata.who.int/pages/indicators-by-category/new_and_under_utilized_vaccines_introduction.html?ISO_3_CODE=&YEAR=


def main():
    df = load_and_clean_data()
    df = standardise_countries(df)
    df.to_csv(
        "data/vax_schedule_upload.csv",
        index=False,
    )


def load_and_clean_data() -> pd.DataFrame:
    df = pd.read_excel(
        "data/New and under utilized vaccines introduction 2022-025-08 13-23 UTC.xlsx"
    )
    df = df.dropna(subset="COUNTRYNAME")
    df = df.drop(
        columns=[
            "ISO_3_CODE",
            "DESCRIPTION",
            "INDCAT_DESCRIPTION",
            "INDSORT",
            "WHO_REGION",
        ]
    )
    df["INDCODE"] = df["INDCODE"].str.replace("INSCHEDULE_", "")
    df["YEAR"] = df["YEAR"].astype(int)
    df["VALUE"] = df["VALUE"].replace(
        {
            "Yes": "Entire country",
            "No": "Not administered",
            "Yes (P)": "Regions of the country",
            "Yes (R)": "Specific risk groups",
            "Yes (A)": "Adolescents",
        }
    )

    df = df.pivot(index=["COUNTRYNAME", "YEAR"], columns="INDCODE", values="VALUE")
    df = df.reset_index()
    df.columns = list(map("".join, df.columns))
    df = df.rename(columns={"COUNTRYNAME": "Country"})
    return df


def standardise_countries(df: pd.DataFrame) -> pd.DataFrame:

    df_con = pd.read_csv("data/country_names_country_standardized.csv")
    country_map = df_con.set_index("Country").squeeze().to_dict()
    df["Country_stan"] = df["Country"].map(country_map)
    missing_countries = (
        df["Country"][df["Country_stan"].isna()].drop_duplicates().tolist()
    )

    assert (
        df["Country_stan"].isna().sum() == 0
    ), f"{missing_countries} are not standardised"

    df["Country"] = df["Country_stan"]
    df = df.drop(columns="Country_stan")
    return df


if __name__ == "__main__":
    main()
