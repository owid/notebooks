# %% [markdown]
#
#  # Passing data in
#
#  Our goal for this session: get ChatGPT to summarise data
#  directly from a prompt.
#

# %%
import json
from dataclasses import dataclass
from typing import Dict, List, Optional
import requests
import sh
from ipywidgets import interact
import pandas as pd

# %% [markdown]
#
# ## Helper functions
# %%


@dataclass
class Indicator:
    data: dict
    metadata: dict

    def to_dict(self):
        return {"data": self.data, "metadata": self.metadata}

    def to_frame(self):
        df = pd.DataFrame.from_dict(self.data)
        entities = pd.DataFrame.from_dict(self.metadata['])


@dataclass
class GrapherBundle:
    config: Optional[dict]
    dimensions: Dict[int, Indicator]
    origins: List[dict]

    def to_json(self):
        return json.dumps(
            {
                "config": self.config,
                "dimensions": {k: i.to_dict() for k, i in self.dimensions.items()},
                "origins": self.origins,
            }
        )

    def size(self):
        return len(self.to_json())


def fetch_grapher_config(slug):
    resp = requests.get(f"https://ourworldindata.org/grapher/{slug}")
    resp.raise_for_status()
    return json.loads(resp.content.decode("utf-8").split("//EMBEDDED_JSON")[1])


def fetch_dimension(id: int) -> Indicator:
    data = requests.get(
        f"https://api.ourworldindata.org/v1/indicators/{id}.data.json"
    ).json()
    metadata = requests.get(
        f"https://api.ourworldindata.org/v1/indicators/{id}.metadata.json"
    ).json()
    return Indicator(data, metadata)


def fetch_bundle(
    slug: Optional[str] = None, indicator_id: Optional[int] = None
) -> GrapherBundle:
    if slug:
        print(f"Fetching chart {slug}")
        config = fetch_grapher_config(slug)
        indicator_ids = [d["variableId"] for d in config["dimensions"]]
    else:
        print(f"Fetching indicator {indicator_id}")
        config = None
        indicator_ids = [indicator_id]
    dimensions = {
        indicator_id: fetch_dimension(indicator_id) for indicator_id in indicator_ids
    }
    origins = []
    for d in dimensions.values():
        if d.metadata.get("origins"):
            origins.append(d.metadata.pop("origins"))
    return GrapherBundle(config, dimensions, origins)


# %%

b = fetch_bundle('life-expectancy')

# %%
pd.DataFrame(b.dimensions.values().data).head()

# %%
