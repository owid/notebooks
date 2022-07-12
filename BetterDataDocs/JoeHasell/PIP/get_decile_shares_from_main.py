#%%
import pandas as pd

#%%
# We can do this with a single request – as all decile data is returned with any request

request_url = 'https://api.worldbank.org/pip/v1/pip?country=all&year=all&povline=1.9&fill_gaps=true&welfare_type=all&reporting_level=all&format=csv'

df_filled = pd.read_csv(request_url)

#%%
id_vars = ['country_name', 'reporting_year','reporting_level','welfare_type']

filter_col = [col for col in df_filled if col.startswith('decile')]

filter_col = id_vars + filter_col

df_filled[filter_col].head()

#%%

request_url = 'https://api.worldbank.org/pip/v1/pip?country=all&year=all&povline=1.9&fill_gaps=false&welfare_type=all&reporting_level=all&format=csv'

df_surveys = pd.read_csv(request_url)

#%%


for col in df_filled.columns:
    print(col)

# %%
df_filled[filter_col].describe()
# %%
df_filled[df_filled['decile1'].isnull()]
# %%

df_filled.to_csv(f'API_output_percentiles/test.csv')

# %%
