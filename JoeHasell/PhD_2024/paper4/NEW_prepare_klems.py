#%% 
import pandas as pd


# MAIN DATA (2011) ----
#%%
# Import
fp = 'data/original/all_countries_09I 2.csv'

df_09 =  pd.read_csv(fp)

#%%
# Reshape the DataFrame from wide to long format
df_09 = pd.melt(df_09, id_vars=['country', 'var', 'code'], var_name='year', value_name='value')

# Remove the underscore from the year column
df_09['year'] = df_09['year'].str.strip('_')


# CANADA DATA (2008) ----
#%%
# Import
fp = 'data/original/can_output_08I.xls'

dfs_can = {}
transactions = ["VA", "COMP", "LAB", "CAP"]

for transaction in ["VA", "COMP", "LAB", "CAP"]:
    dfs_can[transaction] =  pd.read_excel(fp, sheet_name = transaction)
#%%
# add a new 'transaction' column with the 
df_can = pd.concat(dfs_can, keys=transactions)

    
# %%
#  

# %% Keep industry descriptions to merge back in later
industry_descriptions = {}

industry_descriptions['CAN'] = df_can[['desc','code']]



# %%

# Reshape the DataFrame from long to wide format
df_wide = df_can.pivot(index='year', columns='code', values='value').reset_index()
