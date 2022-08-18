import os
from pathlib import Path
from .flu_utils import aggregate_surveillance_type, standardise_countries
from flu_utils import (
    get_country_codes,
    download_country_flu_data,
    combine_country_datasets,
    aggregate_surveillance_type,
    combine_columns_calc_percent,
)

path = str(Path(__file__).parent.resolve())
path = "/Users/fionaspooner/Documents/OWID/repos/notebooks/FionaSpooner/flunet/"
flunet_data_dir = os.path.join(path, "data/flunet/")
flunet_url = "https://frontdoor-l4uikgap6gz3m.azurefd.net/FLUMART/VIW_FNT"
flunet_cols = [
    "COUNTRY/AREA/TERRITORY",
    "COUNTRY_CODE",
    "ISO_WEEKSTARTDATE",
    "ISO_YEAR",
    "ORIGIN_SOURCE",
    "AH1N12009",
    "AH1",
    "AH3",
    "AH5",
    "AH7N9",
    "ANOTSUBTYPED",
    "ANOTSUBTYPABLE",
    "AOTHER_SUBTYPE",
    "INF_A",
    "BVIC_2DEL",
    "BVIC_3DEL",
    "BVIC_NODEL",
    "BVIC_DELUNK",
    "BYAM",
    "BNOTDETERMINED",
    "INF_B",
    "INF_ALL",
    "INF_NEGATIVE",
]

fluid_data_dir = os.path.join(path, "data/fluid/")
fluid_url = "https://frontdoor-l4uikgap6gz3m.azurefd.net/FLUMART/VIW_FID"


def main():
    # Get country codes and download Flunet data for each country
    country_codes = get_country_codes(base_url=flunet_url)
    download_country_flu_data(
        data_dir=flunet_data_dir, base_url=flunet_url, country_codes=country_codes
    )
    combined_df = combine_country_datasets(
        data_dir=flunet_data_dir, country_codes=country_codes
    )
    df = aggregate_surveillance_type(combined_df, flunet_cols)
    df = combine_columns_calc_percent(df)
    flunet_df = standardise_countries(df)
    flunet_df.to_csv(os.path.join(path, "data", "flunet.csv"), index=False)
    # Get country codes and download Fluid data for each country
    country_codes = get_country_codes(base_url=fluid_url)
    download_country_flu_data(
        data_dir=fluid_data_dir, base_url=fluid_url, country_codes=country_codes
    )


if __name__ == "__main__":
    main()
