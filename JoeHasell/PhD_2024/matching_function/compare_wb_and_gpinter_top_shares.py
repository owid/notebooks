#%%
import pandas as pd
import matplotlib.pyplot as plt



#%% Read WB percentile data, downloaded from https://datacatalog.worldbank.org/search/dataset/0063646
df_wb = pd.read_csv("world_bank_percentiles.csv")

#%% Read country name mapping file
df_name_mapping = pd.read_csv("wb_country_code_country_standardized.csv")

#%% Swap in OWID country names to WB data
df_wb = pd.merge(
    df_wb,
    df_name_mapping,
    how = "left",
    left_on="country_code",
    right_on="country"
)

# Drop original country column and rename new country column
df_wb.drop(['country','country_code'], axis=1, inplace=True)

df_wb.rename(columns={'Our World In Data Name': 'country'}, inplace=True)

# %% Keep top 1% shares and rename cols
df_wb_top_shares = df_wb.loc[df_wb['percentile']==100].copy()
df_wb_top_shares.rename(columns={'welfare_share': 'top1_share_wb'}, inplace=True)



# %% Read aligned gpinter data
df_gpinter = pd.read_csv("gpinter_aligned_percentiles_and_shares.csv")

# %% Keep top 1% shares and rename cols
df_gpinter_top_shares = df_gpinter.loc[df_gpinter['p']==0.99].copy()
df_gpinter_top_shares.rename(columns={'shares': 'top1_share_gpinter'}, inplace=True)


# %% Merge gpinter and wb top shares
df_compare = pd.merge(
    df_wb_top_shares,
    df_gpinter_top_shares,
    how = 'outer'
)

# %% Calculate a comparison column
df_compare['ratio']= df_compare['top1_share_gpinter']/df_compare['top1_share_wb']

# %% Calculate a comparison column
plt.scatter(df_compare['top1_share_gpinter'], df_compare['top1_share_wb'])

# %%
check = df_compare[df_compare['ratio']>1]

#%% Read our original scraped percentiles
df_scraped_original= pd.read_csv("percentiles.csv")


# %%
