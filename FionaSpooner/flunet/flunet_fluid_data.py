import os
from pathlib import Path
from flu_utils import get_country_codes, download_country_flu_data

path = str(Path(__file__).parent.resolve())
flunet_data_dir = os.path.join(path, "data/flunet/")
flunet_url = "https://frontdoor-l4uikgap6gz3m.azurefd.net/FLUMART/VIW_FNT"
fluid_data_dir = os.path.join(path, "data/fluid/")
fluid_url = "https://frontdoor-l4uikgap6gz3m.azurefd.net/FLUMART/VIW_FID"


def main():
    # Get country codes and download Flunet data for each country
    country_codes = get_country_codes(base_url=flunet_url)
    download_country_flu_data(
        data_dir=flunet_data_dir, base_url=flunet_url, country_codes=country_codes
    )
    # Get country codes and download Fluid data for each country
    country_codes = get_country_codes(base_url=fluid_url)
    download_country_flu_data(
        data_dir=fluid_data_dir, base_url=fluid_url, country_codes=country_codes
    )


if __name__ == "__main__":
    main()
