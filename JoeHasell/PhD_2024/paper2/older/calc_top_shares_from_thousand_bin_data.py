#%%
import pandas as pd
import numpy as np

#%% Load percentile data prepared by Pablo
fp = "https://catalog.ourworldindata.org/explorers/poverty_inequality/latest/poverty_inequality_export/percentiles.feather"
df_percentiles = pd.read_feather(fp)


#%%# Select thousand bins data
df_thou = df_percentiles[df_percentiles['source']=='PIP (thousand bins)']

#%% A function that calculates top shares for a given year and country
# (it assumes the perc data is sorted)

def calc_top_share(df_group, p):    

    total_inc = df_group['value'].sum()

    top_inc = df_group['value'].iloc[int((p*1000)):].sum()


    top_inc_share = top_inc/total_inc

    return top_inc_share

#%% test function

df_group = df_thou[
    (df_thou['country']=='Indonesia') & \
    (df_thou['year']==1990)       
    ]
test_share = calc_top_share(df_group, p=0.9)

#%% calc top 10% (p=0.9) shares across thousand bin dataset and save

df_top_shares = df_thou.groupby(['country', 'year'])\
    .apply(calc_top_share, p=0.9)\
    .reset_index(name='value')

# Export as csv
df_top_shares.to_csv(f'data/top_pip_shares_comparison/thou_bin_top10shares.csv', index=False)

#%% calc top 1% (p=0.99) shares across thousand bin dataset and save

df_top_shares = df_thou.groupby(['country', 'year'])\
    .apply(calc_top_share, p=0.99)\
    .reset_index(name='value')

# Export as csv
df_top_shares.to_csv(f'data/top_pip_shares_comparison/thou_bin_top1shares.csv', index=False)

#%%

