#%%
import pandas as pd

from PIP_API_query import pip_query_country, pip_query_regions

poverty_lines = [1, 1.9, 3.2, 5.5, 10, 20, 30, 40]
#%%
df_pov = pip_query_country("povline", 10)


#%%
df_regions_pov = pip_query_regions("povline", 10)


df_perc = pip_query_country("popshare", 10)

#%%
df_regions_perc = pip_query_regions("popshare", 10)

# %%
df = pd.read_csv("https://api.worldbank.org/pip/v1/pip-grp?country=all&year=all&popshare=0.2&group_by=wb&format=csv")
# %%
