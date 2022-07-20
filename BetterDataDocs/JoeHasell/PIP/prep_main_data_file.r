# %%
library(tidyverse)

# %%
id_vars <- c('country_name', 'reporting_year','reporting_level','welfare_type')

# %%
# PERCENTILE DATA

# Import 'calculated' percentiles (after GPinter alignment)

df = pd.read_csv('clean_data/percentiles/example_response_filled.csv')





# %%
df_filled = pd.read_csv('API_output/example_response_filled.csv')

# %%

filter_col = [col for col in df_filled if col.startswith('decile')]

filter_col = id_vars + filter_col

df_filled[filter_col].head()

# %%

df_surveys = pd.read_csv('API_output/example_response_survey.csv')


# %%


for col in df_filled.columns:
    print(col)

# %%
df_filled[filter_col].describe()
# %%
df_filled[df_filled['decile1'].isnull()]
# %%

df_filled.to_csv(f'API_output_percentiles/test.csv')

# %%
