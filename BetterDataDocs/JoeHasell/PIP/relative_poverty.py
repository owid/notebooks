# %% [markdown]
# # Get relative poverty values from PIP

# %%
import pandas as pd
import numpy as np

from functions.PIP_API_query import pip_query_country, pip_query_region
from functions.standardize_entities import standardize_entities
from functions.upload import upload_to_s3

import time

# %%
# A $1.9 poverty line query to get the median data from each observation
df = pip_query_country(
                    popshare_or_povline = "povline", 
                    value = 1.9, 
                    fill_gaps="false")

# Generate relative poverty lines for each observation
df['median_40'] = df['median'] * 0.4
df['median_50'] = df['median'] * 0.5
df['median_60'] = df['median'] * 0.6

# %%
start_time = time.time()

# Initialise list to fill with headcount (ratio) data for 40%, 50% and 60% of the median
headcount_40_list = []
headcount_50_list = []
headcount_60_list = []

# For each row of the dataset
for i in range(len(df)):

    # Run 3 queries, one for each relative poverty line, to get the headcount (ratio)
    df_query_40 = pip_query_country(popshare_or_povline = "povline",
                                    country_code = df['country_code'][i],
                                    year = df['reporting_year'][i],
                                    welfare_type = df['welfare_type'][i],
                                    reporting_level = df['reporting_level'][i],
                                    value = df['median_40'][i],
                                    fill_gaps="true")
    
    df_query_50 = pip_query_country(popshare_or_povline = "povline",
                                    country_code = df['country_code'][i],
                                    year = df['reporting_year'][i],
                                    welfare_type = df['welfare_type'][i],
                                    reporting_level = df['reporting_level'][i],
                                    value = df['median_50'][i],
                                    fill_gaps="true")
    
    df_query_60 = pip_query_country(popshare_or_povline = "povline",
                                    country_code = df['country_code'][i],
                                    year = df['reporting_year'][i],
                                    welfare_type = df['welfare_type'][i],
                                    reporting_level = df['reporting_level'][i],
                                    value = df['median_60'][i],
                                    fill_gaps="true")
    
    # If there is no error, get the headcount value and append it to a list
    try:
        headcount_40_value = df_query_40['headcount'][0]
        headcount_40_list.append(headcount_40_value)
        
        headcount_50_value = df_query_50['headcount'][0]
        headcount_50_list.append(headcount_50_value)
        
        headcount_60_value = df_query_60['headcount'][0]
        headcount_60_list.append(headcount_60_value)
    
    # If there is an error, append a null value to the list
    except:
        headcount_40_list.append(np.nan)
        headcount_50_list.append(np.nan)
        headcount_60_list.append(np.nan)

# The three lists converted into new columns
df['headcount_ratio_40'] = headcount_40_list
df['headcount_ratio_50'] = headcount_50_list
df['headcount_ratio_60'] = headcount_60_list

df['headcount_40'] = df['headcount_ratio_40'] * df['reporting_pop']
df['headcount_50'] = df['headcount_ratio_50'] * df['reporting_pop']
df['headcount_60'] = df['headcount_ratio_60'] * df['reporting_pop']

df['headcount_ratio_40'] = df['headcount_ratio_40'] * 100
df['headcount_ratio_50'] = df['headcount_ratio_50'] * 100
df['headcount_ratio_60'] = df['headcount_ratio_60'] * 100

end_time = time.time()
elapsed_time = end_time - start_time
print('Execution time:', elapsed_time, 'seconds')

# %%
df = standardize_entities(
    orig_df = df,
    entity_mapping_url = "https://joeh.fra1.digitaloceanspaces.com/PIP/country_mapping.csv",
    mapping_varname_raw ='Original Name',
    mapping_vaname_owid = 'Our World In Data Name',
    data_varname_old = 'country_name',
    data_varname_new = 'Entity'
)


# Amend the entity to reflect if data refers to urban or rural only
df.loc[(\
    df['reporting_level'].isin(["urban", "rural"])),'Entity'] = \
    df.loc[(\
    df['reporting_level'].isin(["urban", "rural"])),'Entity'] + \
        ' - ' + \
    df.loc[(\
    df['reporting_level'].isin(["urban", "rural"])),'reporting_level']

# Tidying – Rename cols
#Year is only recognised as a Year type when titlecase
df = df.rename(columns={'reporting_year': 'Year'})

# %%
df.to_csv('data/relative_poverty.csv', index=False)

# %%
