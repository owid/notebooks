import os
from pathlib import Path

import click
import pandas as pd
from flu_utils import (
    aggregate_regions,
    aggregate_surveillance_type,
    calculate_fluid_rates,
    clean_fluid_data,
    combine_columns_calc_percent,
    combine_country_datasets,
    download_country_flu_data,
    get_country_codes,
    get_metadata,
    standardise_countries,
)
from structlog import getLogger

log = getLogger()

PATH = str(Path(__file__).parent.resolve())
# PATH = "/Users/fionaspooner/Documents/OWID/repos/notebooks/FionaSpooner/flunet/"
FLUNET_DATA_DIR = os.path.join(PATH, "data/flunet/")
FLUNET_URL = "https://frontdoor-l4uikgap6gz3m.azurefd.net/FLUMART/VIW_FNT"
FLUID_DATA_DIR = os.path.join(PATH, "data/fluid/")
FLUID_URL = "https://frontdoor-l4uikgap6gz3m.azurefd.net/FLUMART/VIW_FID"


@click.command()
@click.option(
    "--download_data/--skip_download",
    default=True,
    help="Whether or not to download the data from the source as it often takes quite some time.",
)
def main(download_data: bool):
    log.info("Get metadata...")
    get_metadata(os.path.join(PATH, "data", "metadata.csv"))
    log.info("Get FluNet...")
    flunet_df = run_flunet(download_data_bool=download_data)
    log.info("Get FluID...")
    fluid_df = run_fluid(download_data_bool=download_data)
    flu_df = pd.merge(flunet_df, fluid_df, on=["Country", "date"], how="outer")
    flu_df.to_csv(
        os.path.join(PATH, "data", "flu.csv"),
        index=False,
    )


def run_flunet(download_data_bool: bool):
    country_codes = get_country_codes(base_url=FLUNET_URL)
    if download_data_bool:
        log.info("Download Flunet...")
        download_country_flu_data(
            data_dir=FLUNET_DATA_DIR, base_url=FLUNET_URL, country_codes=country_codes
        )
    combined_df = combine_country_datasets(
        data_dir=FLUNET_DATA_DIR, country_codes=country_codes
    )
    df = aggregate_surveillance_type(combined_df)
    df = aggregate_regions(df)
    df = combine_columns_calc_percent(df)
    flunet_df = standardise_countries(df, PATH)
    return flunet_df


def run_fluid(download_data_bool: bool):
    country_codes = get_country_codes(base_url=FLUID_URL)
    if download_data_bool:
        log.info("Download FluID...")
        download_country_flu_data(
            data_dir=FLUID_DATA_DIR, base_url=FLUID_URL, country_codes=country_codes
        )
    combined_df = combine_country_datasets(
        data_dir=FLUID_DATA_DIR, country_codes=country_codes
    )
    df = clean_fluid_data(combined_df)
    df = aggregate_regions(df)
    df = calculate_fluid_rates(df)
    fluid_df = standardise_countries(df, PATH)
    return fluid_df


if __name__ == "__main__":
    main()
