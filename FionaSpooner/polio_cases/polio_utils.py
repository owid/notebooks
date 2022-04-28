import requests
from datetime import date, timedelta
import pdfplumber
import pandas as pd
from owid import catalog
import numpy as np


def find_latest_polio_data(url_stub: str, days_to_sub: int):
    day = date.today() - timedelta(days=days_to_sub)
    polio_date = day.strftime("%Y%m%d")
    url = f"{url_stub}{polio_date}.pdf"
    res = requests.get(url)
    return res


def extract_wild_cases(file_path: str) -> pd.DataFrame:
    pdf = pdfplumber.open(file_path)
    table = pdf.pages[0].extract_table()
    df = pd.DataFrame(table)
    df.columns = df.iloc[2]
    df.drop([0, 1, 2], inplace=True)
    col_lim = date.today().year - 2015
    df = df.iloc[:, 0:col_lim]
    df.rename(columns={None: "entity"}, inplace=True)
    years = df.columns.drop("entity")
    dfe = df.set_index("entity")
    df_sel = dfe.loc[:"Total\xa0(Type1)"]
    df_sel = df_sel.reset_index(level=0)
    df_cases = pd.melt(df_sel, id_vars=["entity"], value_vars=years)
    df_cases.columns = ["entity", "year", "wild_polio_cases"]
    df_cases = df_cases[df_cases.entity != "Total\xa0(Type1)"]
    return df_cases


def extract_historical_wild_cases(file_path: str) -> pd.DataFrame:
    pdf = pdfplumber.open(file_path)
    table = pdf.pages[0].extract_table()
    df = pd.DataFrame(table)
    df.columns = df.iloc[2]
    df.drop([0, 1, 2], inplace=True)
    df = df.iloc[:, 0:6]
    df.rename(columns={None: "entity"}, inplace=True)
    years = df.columns.drop("entity")
    dfe = df.set_index("entity")
    df_sel = dfe.loc[:"Total"]
    df_sel = df_sel.reset_index(level=0)
    df_cases = pd.melt(df_sel, id_vars=["entity"], value_vars=years)
    df_cases.columns = ["entity", "year", "wild_polio_cases"]

    return df_cases


def download_polio_data(url_stub: str):
    i = 0
    download_available = False
    while not download_available:
        res = find_latest_polio_data(url_stub, days_to_sub=i)
        if res.ok:
            download_available = True
        else:
            i += 1
    return res


# Manually transcribed the cases into a csv - pdfreading was too glitchy!
def extract_vd_cases() -> pd.DataFrame:
    vdpv_cases = pd.read_csv("data/polio_cVDPV_cases.csv")

    return vdpv_cases


def owid_population() -> pd.DataFrame:
    population = (
        catalog.find("population", dataset="key_indicators", namespace="owid")
        .load()
        .reset_index()
        .rename(columns={"country": "entity"})[["entity", "year", "population"]]
    )

    return population


def standardise_countries(country=pd.Series) -> pd.DataFrame:
    owid_countries = pd.read_csv(
        "data/countries_to_standardise_country_standardized.csv",
        usecols=["Country", "Our World In Data Name"],
    )
    owid_countries["Country"] = owid_countries["Country"].apply(lambda x: x.strip())
    country = country.apply(lambda x: x.strip())
    owid_countries = owid_countries.set_index("Country").squeeze().to_dict()
    countries_standardised = country.apply(lambda x: owid_countries[x])
    return countries_standardised


def get_who_data_and_regions():

    who_polio = pd.read_excel("data/incidence_series.xls", sheet_name="Polio")
    who_polio
    regions = (
        who_polio[["WHO_REGION", "Cname"]]
        .drop_duplicates()
        .rename(columns={"Cname": "entity"})
    )
    regions["entity"] = standardise_countries(regions["entity"])
    who_polio.drop(
        columns=[
            "Disease",
            "WHO_REGION",
            "ISO_code",
        ],
        inplace=True,
    )
    who_melt = pd.melt(who_polio, id_vars=["Cname"])
    who_melt["entity"] = standardise_countries(who_melt["Cname"])
    who_melt = who_melt[["entity", "variable", "value"]].rename(
        columns={"variable": "year", "value": "total_polio"}
    )
    who_melt[["year"]] = who_melt[["year"]].astype(int)

    return who_melt, regions


def add_years_to_polio_status(polio_free: pd.DataFrame) -> pd.DataFrame:
    entities = polio_free["Entity"].drop_duplicates().to_list()

    appended_data = []
    for entity in entities:
        polio_ent = polio_free[polio_free["Entity"] == entity]
        max_year = polio_ent["Year"].max()
        new_years = [2018, 2019, 2020]
        polio_max = polio_ent.loc[polio_ent["Year"] == max_year]
        polio_new = pd.DataFrame(
            np.repeat(polio_max.values, 3, axis=0), columns=polio_max.columns
        )
        polio_new["Year"] = new_years
        appended_data.append(polio_new)

    polio_new = pd.concat(appended_data, ignore_index=True)
    return polio_new
