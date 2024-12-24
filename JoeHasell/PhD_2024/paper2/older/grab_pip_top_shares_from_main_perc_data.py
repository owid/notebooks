
#%%
import pandas as pd
import numpy as np

### PREP CHINA ETC. NATIONAL SHARES DATA

#%% Load data prepared by Pablo
fp = "https://catalog.ourworldindata.org/explorers/poverty_inequality/latest/poverty_inequality_export/percentiles.feather"
df_percentiles = pd.read_feather(fp)

#Select only the main percentile data
df_percentiles = df_percentiles[(df_percentiles['source']=='PIP') & (df_percentiles['indicator_name']=='share')]

# Drop NaNs
df_percentiles = df_percentiles.dropna(subset=['value'])

#%% A function that calculates top shares for a given year and country
# (it assumes the perc data is sorted)

def calc_top_share(df_group, p):    

    share_data = df_group[df_group['indicator_name']=='share']
    
    top_inc_data = share_data['value'].iloc[int((p * 100)):]

    if top_inc_data.empty:
        top_inc_share = float('nan')
    else:
        top_inc_share = top_inc_data.sum()
    
    return top_inc_share

#%% test function

df_group = df_percentiles[
    (df_percentiles['country']=='India') & \
    (df_percentiles['year']==1987) & \
    (df_percentiles['pipreportinglevel']=='rural') & \
    (df_percentiles['pipwelfare']=='consumption')         
    ]

test_share = calc_top_share(df_group, p=0.9)


#%% calc top 10% (p=0.9) shares and save

df_top_shares = df_percentiles.groupby(['country', 'year','pipreportinglevel','pipwelfare'])\
    .apply(calc_top_share, p=0.9)\
    .reset_index(name='value')

# Export as csv
df_top_shares.to_csv(f'data/top_pip_shares_comparison/main_perc_top10shares.csv', index=False)

#%% calc top 1% (p=0.99) shares and save

df_top_shares = df_percentiles.groupby(['country', 'year','pipreportinglevel','pipwelfare'])\
    .apply(calc_top_share, p=0.99)\
    .reset_index(name='value')



# Export as csv
df_top_shares.to_csv(f'data/top_pip_shares_comparison/main_perc_top1shares.csv', index=False)


#%% 