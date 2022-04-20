import pandas as pd


def read_html_table(url, position):
    return (
        pd.read_html(url, header=0)[position]
        .iloc[1:, :2]
        .set_axis(["year", "price"], axis=1)
        .dropna(subset="year")
    )


def download():
    memory = read_html_table("https://jcmit.net/memoryprice.htm", 0)
    ddrives = read_html_table("https://jcmit.net/diskprice.htm", 0)
    flash = read_html_table("https://jcmit.net/flashprice.htm", 0)
    ssd = read_html_table("https://jcmit.net/flashprice.htm", 1)
    return memory, ddrives, ssd, flash


def calculate_cheapest_over_time(df, metric):
    df["price"] = df.price.astype(float)
    df["year"] = df.year.astype(float).astype(int)
    df = df.groupby("year", as_index=False).min().sort_values("year")
    df["price"] = df.price.cummin()
    return df.groupby("price", as_index=False).first().rename(columns={"price": metric})


def main():
    memory, ddrives, ssd, flash = download()

    memory = calculate_cheapest_over_time(memory, metric="memory")
    ddrives = calculate_cheapest_over_time(ddrives, metric="disk_drives")
    ssd = calculate_cheapest_over_time(ssd, metric="ssd")
    flash = calculate_cheapest_over_time(flash, metric="flash")

    df = (
        memory.merge(ddrives, on="year", how="outer", validate="1:1")
        .merge(ssd, on="year", how="outer", validate="1:1")
        .merge(flash, on="year", how="outer", validate="1:1")
        .sort_values("year")
        .assign(entity="World")[
            ["entity", "year", "memory", "disk_drives", "ssd", "flash"]
        ]
    )
    df.to_csv(
        "Historical cost of computer memory and storage - John C. McCallum.csv",
        index=False,
    )


if __name__ == "__main__":
    main()
