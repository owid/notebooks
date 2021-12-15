import requests

import pandas as pd
from tqdm import tqdm

URL = 'https://www.unoosa.org/oosa/osoindex/waxs-search.json?criteria={"filters":[],"startAt":0,"sortings":[{"fieldName":"object.launch.dateOfLaunch_s1","dir":"desc"}]}'


def get_n_objects():
    data = requests.get(URL).json()
    return data["found"]


def offset_url(offset):
    return URL.replace('"startAt":0', '"startAt":' + str(offset))


def get_rows(offset):
    url = offset_url(offset)
    data = requests.get(url).json()
    return pd.DataFrame.from_records([result["values"] for result in data["results"]])


def main():
    n = get_n_objects()

    data = []
    for i in tqdm(range(0, n + 1, 15)):
        data.append(get_rows(i))

    data = pd.concat(data)
    assert len(data) == n
    data.to_csv("scraped_data.csv", index=False)


if __name__ == "__main__":
    main()
