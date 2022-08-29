import pandas as pd


def main():
    download_vaccine_coverage()
    df = load_and_clean_vc_data()
    df = combine_coverage_columns(df)


def download_vaccine_coverage() -> None:
    df = pd.read_excel(
        "https://whowiise.blob.core.windows.net/upload/coverage--2021.xlsx",
        sheet_name="Data",
    )
    df.to_csv("FionaSpooner/who_vaccination/data/who_vaccine_coverage.csv", index=False)


def load_and_clean_vc_data() -> pd.DataFrame:
    df = pd.read_csv("FionaSpooner/who_vaccination/data/who_vaccine_coverage.csv")
    df = df.dropna(subset="CODE")
    return df


def combine_coverage_columns(df: pd.DataFrame) -> pd.DataFrame:
    df["target_pcnt"] = round((df["DOSES"] / df["TARGET_NUMBER"]) * 100, 2)
    df["target_pcnt"] = df["target_pcnt"].fillna(df["COVERAGE"])

    df = df.pivot(
        index=["GROUP", "NAME", "YEAR", "COVERAGE_CATEGORY_DESCRIPTION"],
        columns=["ANTIGEN"],
        values=["DOSES", "COVERAGE", "target_pcnt"],
    ).reset_index()

    df.columns = list(map("".join, df.columns))
    df = df.drop(columns=["GROUP"])
    df = df.rename(columns={"NAME": "Country"})
    df["YEAR"] = df["YEAR"].astype(int)
    return df


if __name__ == "__main__":
    main()
