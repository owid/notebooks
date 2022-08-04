#%%
import pandas as pd

from functions import upload_to_s3
#%%

# Pull in PIP data

df_pip = pd.read_csv("https://joeh.fra1.digitaloceanspaces.com/PIP/main_data.csv")

# %%
# Filter to keep only national reporting level when there are duplcates
df_pip['duplicate'] = df_pip.\
    duplicated(subset=['entity', 'reporting_year', 'welfare_type'], keep=False)

df_pip = df_pip[(df_pip["duplicate"]== False) | (df_pip["reporting_level"]== "national")]

#%%
# Pull in WID data

df_wid = pd.read_csv("https://joeh.fra1.digitaloceanspaces.com/wid/gini_and_topshares_standardized.csv")

#%%
# Merge the two data frames
df_pip = df_pip.rename(columns = {"reporting_year":"year"})
#%%
df = pd.merge(df_wid, df_pip, on = ['entity', 'year'], how = 'outer')

#%%
# Save to s3
upload_to_s3(df,"phd_global_dist", "wid_pip_gini_and_topshares.csv")
# %%
