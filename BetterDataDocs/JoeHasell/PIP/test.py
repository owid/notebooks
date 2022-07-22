#%%
import pandas as pd

#%%
id_vars = ['country_name', 'reporting_year','reporting_level','welfare_type']

#%%
df_filled = pd.read_csv("data/intermediate/percentiles/filled_true/percentiles_before_Gpinter.csv")

select_cols = id_vars.copy()
select_cols.append("requested_p")
select_cols.append("poverty_line")
#%%
df_p90 = df_filled[df_filled['requested_p'] == 90][select_cols]
df_p90 = df_p90.rename(columns = {"poverty_line":"p90"})
df_p90 = df_p90.drop(columns = ["requested_p"])
#%%

df_p10 = df_filled[df_filled['requested_p'] == 10][select_cols]
df_p10 = df_p10.rename(columns = {"poverty_line":"p10"})
df_p10 = df_p10.drop(columns = ["requested_p"])

#%%

df_p90_10 = pd.merge(df_p90, df_p10, on = id_vars, how = "inner")

#%%
df_p90_10['ratio'] = df_p90_10['p90'] /df_p90_10['p10'] 
# %%


#%%

