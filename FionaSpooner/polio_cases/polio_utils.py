import requests
from datetime import date, timedelta
import pdfplumber
import pandas as pd
import tabula


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
    df_sel = dfe.loc[:"Total (Type1)"]
    df_sel = df_sel.reset_index(level=0)
    df_cases = pd.melt(df_sel, id_vars=["entity"], value_vars=years)

    df_cases.columns = ["entity", "year", "wild_polio_1_cases"]
    df_cases

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


def extract_vd_cases(file_path: str):
    table = tabula.read_pdf(file_path, pages=1)

    df = pd.DataFrame(table[0])
    df.iloc[:, 0] = df.iloc[:, 0].fillna(method="ffill")
    col_lim = date.today().year - 2014
    df = df.iloc[:, 0:col_lim]
    years = range(2016, df.shape[1] - 2 + 2016)
    years_str = [str(x) for x in years]
    cols = ["strain", "entity"]
    cols = cols + years_str
    df.columns = cols
    df.drop([0], inplace=True)

    dfm = pd.melt(df, id_vars=["entity", "strain"], value_vars=years_str)
    dfm = dfm[dfm.strain != "Gender"]

    df_p = pd.pivot_table(
        dfm, values="value", index=["entity", "variable"], columns=["strain"]
    ).reset_index()
    df_p.rename(
        columns={"cVDPV11": "cVDPV1", "cVDPV21": "cVDPV2", "cVDPV31": "cVDPV3"},
        inplace=True,
    )
    df_p["total_cVDPV"] = df_p[["cVDPV1", "cVDPV2", "cVDPV3"]].sum(axis=1)
    return df_p
