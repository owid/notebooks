
#%%
import pandas as pd

#%% Read the prepared data file
df_prep = pd.read_feather("tb.feather")

#%% Get a list of unique country-year-welfare-reporting level ids from the PIP data
df = df_prep[df_prep['source']=='PIP']

df = df_prep[['country', 'year', 'welfare', 'pipreportinglevel', 'pipwelfare']].drop_duplicates()

#%% Read top 1 shares taken from the WB standalone percentile file
df_top1_wb = pd.read_csv("top1shares_from_WB_percentile_file.csv")

df_top1_wb = df_top1_wb[['country', 'year', 'reporting_level','welfare_type', 'top1_share_wb']]
df_top1_wb.rename(columns={'reporting_level': 'pipreportinglevel', 'welfare_type': 'pipwelfare'}, inplace=True)


# %% merge in top shares  
df = pd.merge(
    df,
    df_top1_wb,
    how = 'left'
)

#%% Read top 1 shares derived from Gpinter
df_top1_gpinter = pd.read_csv("top1shares_from_Gpinter.csv")


df_top1_gpinter = df_top1_gpinter[['country', 'year', 'reporting_level','welfare_type', 'top1_share_gpinter']]
df_top1_gpinter.rename(columns={'reporting_level': 'pipreportinglevel', 'welfare_type': 'pipwelfare'}, inplace=True)

# %% merge in Gpinter-derived shares
df = pd.merge(
    df,
    df_top1_gpinter,
    how = 'left'
)


# %% Create a new top 1 share column that take the WB direct value, but adds gpinter derrived value if missing
df['value']= df['top1_share_wb']

# %% Fill in NaN values with values from Gpinter top 1 shares
df['value'].fillna(df['top1_share_gpinter'], inplace=True)

# %% Keep only rows with top 1 share data
df = df[df['value'].notna()]
# %% drop unneeded cols
df.drop(['top1_share_gpinter','top1_share_wb'], axis=1, inplace=True)

# %% Add additional id cols
df['source'] = 'PIP'
df['series_code'] = 'p99p100Share_pip_disposable_perCapita'

# %% Save final pip top1 share data
df.to_csv("prepared_pip_top1shares.csv", index=False)

# %% 
