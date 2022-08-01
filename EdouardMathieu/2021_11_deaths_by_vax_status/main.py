import requests

import epiweeks
import pandas as pd


SOURCE_USA = "https://data.cdc.gov/api/views/ukww-au2k/rows.csv?accessType=DOWNLOAD"
SOURCE_CHL = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto89/incidencia_en_vacunados_edad.csv"
SOURCE_ENG = "input/referencetable2.xlsx"
SOURCE_CHE = "https://www.covid19.admin.ch/api/data/context"


def epiweek_to_date(row, system):
    return epiweeks.Week(row.Year, row.Week, system=system).enddate()


def process_usa(source: str):
    df = pd.read_csv(source)
    df = df[(df.outcome == "death") & (df.vaccine_product == "all_types")].rename(
        columns={
            "age_group": "Entity",
            "crude_unvax_ir": "unvaccinated",
            "crude_vax_ir": "fully_vaccinated",
            "crude_one_booster_ir": "one_booster",
            "crude_two_booster_ir": "two_boosters",
        }
    )

    df.loc[df.Entity == "all_ages_adj", "unvaccinated"] = df.age_adj_unvax_ir
    df.loc[df.Entity == "all_ages_adj", "fully_vaccinated"] = df.age_adj_vax_ir
    df.loc[df.Entity == "all_ages_adj", "one_booster"] = df.age_adj_one_booster_ir
    df.loc[df.Entity == "all_ages_adj", "two_boosters"] = df.age_adj_two_booster_ir

    df = df.assign(Week=df.mmwr_week.mod(100), Year=df.mmwr_week.div(100).astype(int))
    df["Year"] = df.apply(epiweek_to_date, system="cdc", axis=1)
    df["Year"] = (pd.to_datetime(df.Year) - pd.to_datetime("20210101")).dt.days
    df = df.drop(columns="mmwr_week")[
        [
            "Entity",
            "Year",
            "unvaccinated",
            "fully_vaccinated",
            "one_booster",
            "two_boosters",
        ]
    ]

    df["Entity"] = df.Entity.replace({"all_ages_adj": "All ages"})

    df.to_csv(
        "output/COVID-19 - Deaths by vaccination status - United States.csv",
        index=False,
    )


def process_chl(source: str):
    df = (
        pd.read_csv(source)
        .drop_duplicates()[
            [
                "semana_epidemiologica",
                "edad",
                "estado_vacunacion",
                "casos_def",
                "poblacion",
            ]
        ]
        .rename(
            columns={
                "semana_epidemiologica": "Week",
                "edad": "Entity",
                "estado_vacunacion": "status",
                "casos_def": "deaths",
                "poblacion": "population",
            }
        )
    )

    status_mapping = {
        "Sin esquema completo": "0 or 1 dose",
        "Esquema completo > 6 meses": "2 doses",
        "Esquema completo > 14 días y < 6 meses": "2 doses",
        "1° Dosis refuerzo > 6 meses": "3 doses",
        "1° Dosis refuerzo > 14 días y < 6 meses": "3 doses",
        "2° Dosis refuerzo > 6 meses": "4 doses",
        "2° Dosis refuerzo > 14 días y < 6 meses": "4 doses",
    }
    assert set(status_mapping.keys()) == set(df.status)
    df["status"] = df.status.replace(status_mapping)

    df = df[df.Entity != "Total"]
    age_mapping = {
        "03 - 05 años": "03-05",
        "06 - 11 años": "06-11",
        "12 - 20 años": "12-20",
        "21 - 30 años": "21-30",
        "31 - 40 años": "31-40",
        "41 - 50 años": "41-50",
        "51 - 60 años": "51-60",
        "61 - 70 años": "61-70",
        "71 - 80 años": "71-80",
        "80 años o más": "80+",
    }
    assert set(age_mapping.keys()) == set(df.Entity)
    df["Entity"] = df.Entity.replace(age_mapping)

    # Simplify the groups
    df = df.groupby(["Week", "Entity", "status"], as_index=False).sum()
    df["rate"] = 100000 * df.deaths / df.population
    df = df.drop(columns=["deaths", "population"])

    # Age standardization based on single-year population estimates by the United Nations
    age_pyramid = {
        "03-05": 705492,
        "06-11": 1480115,
        "12-20": 2219549,
        "21-30": 3106433,
        "31-40": 3036552,
        "41-50": 2637028,
        "51-60": 2357671,
        "61-70": 1768265,
        "71-80": 982466,
        "80+": 508961,
    }
    df["age_group_standard"] = df.Entity.replace(age_pyramid)
    df["age_group_proportion"] = df.age_group_standard / sum(age_pyramid.values())
    df["age_specific_adjusted_rate"] = df.rate * df.age_group_proportion
    all_ages = (
        df[["Week", "status", "age_specific_adjusted_rate"]]
        .groupby(["Week", "status"], as_index=False)
        .sum()
        .rename(columns={"age_specific_adjusted_rate": "rate"})
        .assign(Entity="All ages")
    )
    df = df.drop(
        columns=[
            "age_group_standard",
            "age_group_proportion",
            "age_specific_adjusted_rate",
        ]
    )
    df = pd.concat([df, all_ages], ignore_index=True)

    df[["Year", "Week"]] = df.Week.str.split("-", expand=True).astype(int)
    df["Year"] = df.apply(epiweek_to_date, system="iso", axis=1)
    df["Year"] = (pd.to_datetime(df.Year) - pd.to_datetime("20210101")).dt.days
    df = df[df.Year < df.Year.max()].drop(columns="Week")

    df = df.pivot(
        index=["Entity", "Year"], columns="status", values="rate"
    ).reset_index()

    df.to_csv(
        "output/COVID-19 - Deaths by vaccination status - Chile.csv",
        index=False,
    )


def process_che(source: str):
    response = requests.get(source).json()
    context = response["sources"]["individual"]["csv"]
    data_url = context["weekly"]["byAge"]["deathVaccPersons"]
    df = pd.read_csv(data_url)

    assert set(df.vaccination_status) == {
        "not_vaccinated",
        "fully_vaccinated_no_booster",
        "fully_vaccinated_first_booster",
        "partially_vaccinated",
        "fully_vaccinated",
        "unknown",
    }, f"New vaccination_status: {set(df.vaccination_status)}"

    df = df[
        (df.vaccine == "all")
        & (
            df.vaccination_status.isin(
                [
                    "not_vaccinated",
                    "fully_vaccinated_no_booster",
                    "fully_vaccinated_first_booster",
                ]
            )
        )
        & (df.geoRegion == "CHFL")
        & (df.type == "COVID19Death")
        & (df.timeframe_all == True)
        & (df["pop"].notnull())
        & (df["pop"] >= 100)
        & (df.date < df.date.max())
    ][["date", "altersklasse_covid19", "vaccination_status", "entries", "pop"]].rename(
        columns={
            "date": "Year",
            "altersklasse_covid19": "Entity",
        }
    )

    df[["Year", "Week"]] = (
        df.Year.astype(str).str.extract(r"(\d{4})(\d{2})").astype(int)
    )
    df["Year"] = df.apply(epiweek_to_date, system="iso", axis=1)
    df["Year"] = (pd.to_datetime(df.Year) - pd.to_datetime("20210101")).dt.days
    df = df.drop(columns="Week")

    df = df[-df.Entity.isin(["all", "Unbekannt"])]
    age_dict = {
        "0 - 9": "00-09",
        "10 - 19": "10-19",
        "20 - 29": "20-29",
        "30 - 39": "30-39",
        "40 - 49": "40-49",
        "50 - 59": "50-59",
        "60 - 69": "60-69",
        "70 - 79": "70-79",
        "80+": "80+",
    }
    df = df[df.Entity.isin(age_dict.keys())]
    df["Entity"] = df.Entity.replace(age_dict)

    df["rate"] = 100000 * df.entries / df["pop"]

    # Age standardization based on single-year population estimates by the United Nations
    age_pyramid = {
        "00-09": 878021,
        "10-19": 851711,
        "20-29": 1025207,
        "30-39": 1243830,
        "40-49": 1201683,
        "50-59": 1300832,
        "60-69": 983365,
        "70-79": 741352,
        "80+": 463613,
    }
    df["age_group_standard"] = df.Entity.replace(age_pyramid)
    df["age_group_proportion"] = df.age_group_standard / sum(age_pyramid.values())
    df["age_specific_adjusted_rate"] = df.rate * df.age_group_proportion
    all_ages = (
        df[["Year", "vaccination_status", "age_specific_adjusted_rate"]]
        .groupby(["Year", "vaccination_status"], as_index=False)
        .sum()
        .rename(columns={"age_specific_adjusted_rate": "rate"})
        .assign(Entity="All ages")
    )
    df = df.drop(
        columns=[
            "age_group_standard",
            "age_group_proportion",
            "age_specific_adjusted_rate",
        ]
    )
    df = pd.concat([df, all_ages], ignore_index=True)

    df = (
        df.drop(columns=["entries", "pop"])
        .pivot(index=["Entity", "Year"], columns="vaccination_status", values="rate")
        .reset_index()
        .rename(
            columns={
                "fully_vaccinated_no_booster": "Fully vaccinated, no booster",
                "not_vaccinated": "Unvaccinated",
                "fully_vaccinated_first_booster": "Fully vaccinated + booster",
            }
        )
    )

    df.to_csv(
        "output/COVID-19 - Deaths by vaccination status - Switzerland and Liechtenstein.csv",
        index=False,
    )


def main():
    process_che(SOURCE_CHE)
    process_usa(SOURCE_USA)
    process_chl(SOURCE_CHL)


if __name__ == "__main__":
    main()
