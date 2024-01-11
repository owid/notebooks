#%%
import pandas as pd


#%%
df_name_mapping = pd.read_csv("wb_country_code_country_standardized.csv")

#%%
df_regions = pd.read_csv(f"{PARENT_DIR}/region_mapping.csv")
