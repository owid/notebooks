import pandas as pd


def read():
    return pd.read_csv(
        "scraped_data.csv",
        usecols=["object.launch.stateOfRegistry_s1", "object.launch.dateOfLaunch_s1"],
    ).rename(
        columns={
            "object.launch.stateOfRegistry_s1": "entity",
            "object.launch.dateOfLaunch_s1": "year",
        }
    )


def aggregate_world(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("year", as_index=False)
        .size()
        .rename(columns={"size": "yearly_launches"})
        .assign(entity="World")
    )


def clean_entities(df: pd.DataFrame) -> pd.DataFrame:
    df.loc[
        df.entity.str.contains("[\(\[]for .*[\)\]]$"), "entity"
    ] = df.entity.str.extract("[\(\[]for (.*)[\)\]]$", expand=False)
    df["entity"] = df.entity.str.split(",|&| and ")
    df = df.explode("entity")
    df["entity"] = df.entity.str.strip()

    mapping = pd.read_csv("entities.csv")
    df = pd.merge(df, mapping, on="entity", how="left")
    df = df[df.clean_entity != "REMOVE"]
    if any(df.clean_entity.isnull()):
        print(df.loc[df.clean_entity.isnull(), "entity"].drop_duplicates())
        raise Exception("Missing entities in mapping!")

    return df.drop(columns="entity").rename(columns={"clean_entity": "entity"})


def main():
    df = read()

    df["year"] = df.year.str.slice(0, 4)

    world = aggregate_world(df)

    df = (
        clean_entities(df)
        .groupby(["entity", "year"], as_index=False)
        .size()
        .rename(columns={"size": "yearly_launches"})
    )

    df = pd.concat([df, world], ignore_index=True).sort_values(["entity", "year"])

    df["cumulative_launches"] = (
        df[["entity", "yearly_launches"]].groupby("entity", as_index=False).cumsum()
    )

    df.to_csv(
        "United Nations - Online Index of Objects Launched into Outer Space.csv",
        index=False,
    )


if __name__ == "__main__":
    main()
