# %% [markdown]
# # World Bank Poverty and Inequality Platform dataset
#
# ***To get the most updated dataset it is required to run the `relative_poverty.py` and `extract_percentiles.py` codes first. They are not included here because it takes more than an hour to complete.***

# %%
import pandas as pd
import numpy as np
import time

#from functions.PIP_API_query import pip_query_country, pip_query_region
from functions.standardize_entities import standardize_entities
from functions.upload import upload_to_s3

from create_dataset_functions import *

# %%
print('CAUTION: If a full update is needed, first you have to run relative_poverty.py and extract_percentiles.py')
print('These codes take several hours to run, that\'s why they are not available here')
question = "Do you want to continue?"
query_yes_no(question)

# %%
start_time = time.time()
# Here we define the poverty lines to query as cents
poverty_lines_cents = [100, 190, 320, 550, 1000, 2000, 3000, 4000]
#Here we define the international poverty line
extreme_povline = 190

povlines_count = len(poverty_lines_cents)
print(f'{povlines_count} poverty lines were defined (in cents):')
print(f'{poverty_lines_cents}')

print(f'The extreme poverty line is defined as (in cents):')
print(f'{extreme_povline}')

# %%
df_final = query_all_and_merge(poverty_lines_cents)

# %%
df_final, cols = additional_variables_and_drop(df_final, poverty_lines_cents)

# %%
df_final = median_patch(df_final)

# %%
df_final = standardise(df_final)

# %%
df_inc_only, df_cons_only, df_inc_or_cons = export(df_final, cols)

# %%
include_metadata(df_inc_or_cons)

# %%
regional_headcount(extreme_povline/100)

# %%
end_time = time.time()
elapsed_time = end_time - start_time
print(f'The files were created in {elapsed_time} seconds :)')
print('Update the main PIP dataset with pip_final.csv')
print('Update the regional headcount dataset with pip_regional_headcount.csv')
