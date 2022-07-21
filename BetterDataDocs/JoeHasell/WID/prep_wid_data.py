#%%
import pandas as pd

from functions import upload_to_s3

#%%
df_ginis = pd.read_csv("stata_code_and_output/ginis.csv", keep_default_na=False)

df_ginis = df_ginis[['country', 'year', 'value']].rename(columns={
    'value': 'wid_gini'
})

#%%
df_topshares = pd.read_csv("stata_code_and_output/topshares.csv",keep_default_na=False)

df_topshares = df_topshares[['country', 'year', 'percentile', 'value']]

df_topshares = df_topshares.pivot(
    index=['country', 'year'],
    columns= 'percentile',
    values = 'value'
    )

df_topshares = df_topshares.rename(columns = {
    "p90p100": "wid_top_10_share",
    "p99p100": "wid_top_1_share"
}).reset_index()

#%%


#%%
# Merge in ginis

df_wid = df_topshares.merge(df_ginis)


# %%
#write to csv in s3
upload_to_s3(df_wid,
            "wid",
            "gini_and_topshares.csv")