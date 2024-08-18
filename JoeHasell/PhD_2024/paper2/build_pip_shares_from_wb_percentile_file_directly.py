#%%
import pandas as pd


#%% Load the data from PIP percentiles file
fp = 'data/original/pip_percentile_file_20240613.csv'
df_pip_perc = pd.read_csv(fp)




#%% Read country name mapping file
df_name_mapping = pd.read_csv("data/original/wb_country_code_country_standardized.csv")


#%%

#%% Swap in OWID country names to WB data
df_pip_perc = pd.merge(
    df_pip_perc,
    df_name_mapping,
    how = "left",
    left_on="country_code",
    right_on="country"
)


#%% Check all countries were matched
test = df_pip_perc[df_pip_perc['Our World In Data Name'].isna()]

#%% # Drop original country column and rename new country column
df_pip_perc.drop(['country','country_code'], axis=1, inplace=True)

df_pip_perc.rename(columns={'Our World In Data Name': 'country'}, inplace=True)



# %% Keep top 1% shares and rename cols
df_top1shares = df_pip_perc.loc[df_pip_perc['percentile']==100].copy()


#%% Add metadata
df_top1shares['unit'] = '%'
df_top1shares['source'] = 'PIP'
df_top1shares['welfare'] = 'Disposable income or consumption'
df_top1shares['resource_sharing'] = 'Per capita'

df_top1shares['series_code']="p99p100Share_pip_disposable_perCapita"
df_top1shares['indicator_name']="p99p100Share"

#Rename pip-specific metadata columns
df_top1shares.rename(columns={
    'welfare_share': 'value',
    'welfare_type': 'pipwelfare',
    'reporting_level':'pipreportinglevel'}, inplace=True)


# Express as percent not share
df_top1shares['value'] = df_top1shares['value']*100


#%% Keep needed to columns (to match up with main indicators file from Pablo)
df_top1shares = df_top1shares[[
    'country',
    'year',
    'series_code',
    'indicator_name',
    'source',
    'welfare',
    'resource_sharing',
    'pipreportinglevel',
    'pipwelfare',
    'unit',
    'value'
]]



# %% Export as csv
df_top1shares.to_csv("data/df_top1shares.csv", index=False)



# %%
