#%%
import pandas as pd
import numpy as np

#%% For the bulk of countries, we use data from the 'percentiles file'
fp = 'data/top_pip_shares_comparison/main_perc_top1shares.csv'
df_top_1_percentile_file = pd.read_csv(fp)


#%% But this data does not have national data points for 
# China, India and Indonesia – only rural and urban.
# For these countries, I use data calculated from the 'thousand bins'
# dataset. This is based on an earlier version of the PIP data.
# However, as demonstrated in the 'compare_different_pip_top_shares.py' script,
# for the top 10% share (which *is* available directly from PIP) we see 
# there is good agreement between the datasets for 1990 and 2018 – our reference years.

fp = 'data/top_pip_shares_comparison/china_etc_top1shares.csv'
df_top_1_china_etc = pd.read_csv(fp)
df_top_1_china_etc['pipreportinglevel']='national'



#%% Merge the two source

df_top1shares = pd.concat([df_top_1_percentile_file, df_top_1_china_etc])


#%% Add metadata
df_top1shares['unit'] = '%'
df_top1shares['source'] = 'PIP'
df_top1shares['welfare'] = 'Disposable income or consumption'
df_top1shares['resource_sharing'] = 'Per capita'

df_top1shares['series_code']="p99p100Share_pip_disposable_perCapita"
df_top1shares['indicator_name']="p99p100Share"

# Express as percent not share
df_top1shares['value'] = df_top1shares['value']*100

# %% Export as csv
df_top1shares.to_csv("data/df_top1shares.csv", index=False)

# %%
