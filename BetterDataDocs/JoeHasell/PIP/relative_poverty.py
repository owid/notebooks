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
relative_poverty_lines = [40, 50, 60]

# %%
#Just as for the main data here we need to 'patch' missing median data for several countries, including China, India and Indonesia
start_time = time.time()

# A $1.9 poverty line query to get the median data from each observation
df = pip_query_country(
                    popshare_or_povline = "povline", 
                    value = 1.9, 
                    fill_gaps="false")

median_list = []

for i in range(len(df)):
    if np.isnan(df['median'][i]):
        df_popshare = pip_query_country(popshare_or_povline = "popshare",
                                        country_code = df['country_code'][i],
                                        year = df['reporting_year'][i],
                                        welfare_type = df['welfare_type'][i],
                                        reporting_level = df['reporting_level'][i],
                                        value = 0.5,
                                        fill_gaps="false")
        try:
            median_value = df_popshare['poverty_line'][0]
            median_list.append(median_value)
        
        except:
            median_list.append(np.nan)
        
        
    else:
        median_value = df['median'][i]
        median_list.append(median_value)
               

df['median2'] = median_list
df = df.rename(columns={'country_name': 'Entity',
                                    'reporting_year': 'Year'})
null_median = (df['median'].isnull()).sum()
null_median2 = (df['median2'].isnull()).sum()
print(f'Before patching: {null_median} nulls for median')
print(f'After patching: {null_median2} nulls for median')

df['median_ratio'] = df['median'] / df['median2']
median_ratio_median = (df['median_ratio']).median()
median_ratio_min = (df['median_ratio']).min()
median_ratio_max = (df['median_ratio']).max()

if median_ratio_median == 1 and median_ratio_min == 1 and median_ratio_max == 1:
    print(f'Patch successful.')
    print(f'Ratio between old and new variable: Median = {median_ratio_median}, Min = {median_ratio_min}, Max = {median_ratio_max}')
else:
    print(f'Patch changed some median values. Please check for errors.')
    print(f'Ratio between old and new variable: Median = {median_ratio_median}, Min = {median_ratio_min}, Max = {median_ratio_max}')

df.drop(columns=['median', 'median_ratio'], inplace=True)
df.rename(columns={'median2': 'median'}, inplace=True)

# Generate relative poverty lines for each observation
df['median_40'] = df['median'] * 0.4
df['median_50'] = df['median'] * 0.5
df['median_60'] = df['median'] * 0.6

end_time = time.time()
elapsed_time = end_time - start_time
print('Execution time:', elapsed_time, 'seconds')

# %%
start_time = time.time()

# Initialise list to fill with headcount (ratio) data for 40%, 50% and 60% of the median
headcount_40_list = []
headcount_50_list = []
headcount_60_list = []

pgi_40_list = []
pgi_50_list = []
pgi_60_list = []

pov_severity_40_list = []
pov_severity_50_list = []
pov_severity_60_list = []

watts_40_list = []
watts_50_list = []
watts_60_list = []

# For each row of the dataset
for i in range(len(df)):

    # Run 3 queries, one for each relative poverty line, to get the headcount (ratio)
    df_query_40 = pip_query_country(popshare_or_povline = "povline",
                                    country_code = df['country_code'][i],
                                    year = df['Year'][i],
                                    welfare_type = df['welfare_type'][i],
                                    reporting_level = df['reporting_level'][i],
                                    value = df['median_40'][i],
                                    fill_gaps="false")
    
    df_query_50 = pip_query_country(popshare_or_povline = "povline",
                                    country_code = df['country_code'][i],
                                    year = df['Year'][i],
                                    welfare_type = df['welfare_type'][i],
                                    reporting_level = df['reporting_level'][i],
                                    value = df['median_50'][i],
                                    fill_gaps="false")
    
    df_query_60 = pip_query_country(popshare_or_povline = "povline",
                                    country_code = df['country_code'][i],
                                    year = df['Year'][i],
                                    welfare_type = df['welfare_type'][i],
                                    reporting_level = df['reporting_level'][i],
                                    value = df['median_60'][i],
                                    fill_gaps="false")
    
    # If there is no error, get the headcount value and append it to a list
    try:
        headcount_40_value = df_query_40['headcount'][0]
        headcount_40_list.append(headcount_40_value)
        pgi_40_value = df_query_40['poverty_gap'][0]
        pgi_40_list.append(pgi_40_value)
        pov_severity_40_value = df_query_40['poverty_severity'][0]
        pov_severity_40_list.append(pov_severity_40_value)
        watts_40_value = df_query_40['watts'][0]
        watts_40_list.append(watts_40_value)
        
        headcount_50_value = df_query_50['headcount'][0]
        headcount_50_list.append(headcount_50_value)
        pgi_50_value = df_query_50['poverty_gap'][0]
        pgi_50_list.append(pgi_50_value)
        pov_severity_50_value = df_query_50['poverty_severity'][0]
        pov_severity_50_list.append(pov_severity_50_value)
        watts_50_value = df_query_50['watts'][0]
        watts_50_list.append(watts_50_value)
        
        headcount_60_value = df_query_60['headcount'][0]
        headcount_60_list.append(headcount_60_value)
        pgi_60_value = df_query_60['poverty_gap'][0]
        pgi_60_list.append(pgi_60_value)
        pov_severity_60_value = df_query_60['poverty_severity'][0]
        pov_severity_60_list.append(pov_severity_60_value)
        watts_60_value = df_query_60['watts'][0]
        watts_60_list.append(watts_60_value)
    
    # If there is an error, append a null value to the list
    except:
        headcount_40_list.append(np.nan)
        pgi_40_list.append(np.nan)
        pov_severity_40_list.append(np.nan)
        watts_40_list.append(np.nan)
        
        headcount_50_list.append(np.nan)
        pgi_50_list.append(np.nan)
        pov_severity_50_list.append(np.nan)
        watts_50_list.append(np.nan)
        
        headcount_60_list.append(np.nan)
        pgi_60_list.append(np.nan)
        pov_severity_60_list.append(np.nan)
        watts_60_list.append(np.nan)
        

# The three lists converted into new columns
df['headcount_ratio_40_median'] = headcount_40_list
df['headcount_ratio_50_median'] = headcount_50_list
df['headcount_ratio_60_median'] = headcount_60_list

df['poverty_gap_index_40_median'] = pgi_40_list
df['poverty_gap_index_50_median'] = pgi_50_list
df['poverty_gap_index_60_median'] = pgi_60_list

df['poverty_severity_40_median'] = pov_severity_40_list
df['poverty_severity_50_median'] = pov_severity_50_list
df['poverty_severity_60_median'] = pov_severity_60_list

df['watts_40_median'] = watts_40_list
df['watts_50_median'] = watts_50_list
df['watts_60_median'] = watts_60_list


df['headcount_40_median'] = df['headcount_ratio_40_median'] * df['reporting_pop']
df['headcount_50_median'] = df['headcount_ratio_50_median'] * df['reporting_pop']
df['headcount_60_median'] = df['headcount_ratio_60_median'] * df['reporting_pop']

df['total_shortfall_40_median'] = df['poverty_gap_index_40_median'] * df['median_40'] * df['reporting_pop']
df['total_shortfall_50_median'] = df['poverty_gap_index_50_median'] * df['median_50'] * df['reporting_pop']  
df['total_shortfall_60_median'] = df['poverty_gap_index_60_median'] * df['median_60'] * df['reporting_pop']

df['avg_shortfall_40_median'] = df['total_shortfall_40_median'] / df['headcount_40_median']
df['avg_shortfall_50_median'] = df['total_shortfall_50_median'] / df['headcount_50_median']
df['avg_shortfall_60_median'] = df['total_shortfall_60_median'] / df['headcount_60_median']

df['income_gap_ratio_40_median'] = (df['total_shortfall_40_median'] / df['headcount_40_median']) / df['median_40']
df['income_gap_ratio_50_median'] = (df['total_shortfall_50_median'] / df['headcount_50_median']) / df['median_50']
df['income_gap_ratio_60_median'] = (df['total_shortfall_60_median'] / df['headcount_60_median']) / df['median_60']

df['headcount_ratio_40_median'] = df['headcount_ratio_40_median'] * 100
df['headcount_ratio_50_median'] = df['headcount_ratio_50_median'] * 100
df['headcount_ratio_60_median'] = df['headcount_ratio_60_median'] * 100

df['income_gap_ratio_40_median'] = df['income_gap_ratio_40_median'] * 100
df['income_gap_ratio_50_median'] = df['income_gap_ratio_50_median'] * 100
df['income_gap_ratio_60_median'] = df['income_gap_ratio_60_median'] * 100

df['poverty_gap_index_40_median'] = df['poverty_gap_index_40_median'] * 100
df['poverty_gap_index_50_median'] = df['poverty_gap_index_50_median'] * 100
df['poverty_gap_index_60_median'] = df['poverty_gap_index_60_median'] * 100

df = df.rename(columns={'country_name': 'Entity',
                        'Year': 'Year'})

end_time = time.time()
elapsed_time = end_time - start_time
print('Execution time:', elapsed_time, 'seconds')

# %%
# for i in range(len(relative_poverty_lines)):
#     varname = f'headcount_{relative_poverty_lines[i]}_median'
#     df[varname] = df[f'headcount_ratio_{relative_poverty_lines[i]}_median'] * df['reporting_pop']
#     col_headcount_relative.append(varname)
    
#     varname = f'total_shortfall_{relative_poverty_lines[i]}_median'
#     df[varname] = df[f'poverty_gap_index_{relative_poverty_lines[i]}_median'] * df[f'median_{relative_poverty_lines[i]}'] * df['reporting_pop']
#     col_pgi_relative.append(varname)
    
#     varname = f'total_shortfall_{relative_poverty_lines[i]}_median'
#     df[varname] = df[f'poverty_gap_index_{relative_poverty_lines[i]}_median'] * df[f'median_{relative_poverty_lines[i]}'] * df['reporting_pop']
#     col_pgi_relative.append(varname)

# %%
#Calculate numbers in poverty between pov lines for stacked area charts
#Make sure the poverty lines are in order, lowest to highest
relative_poverty_lines.sort()

col_stacked_n = []
col_stacked_pct = []

#For each poverty line in relative_poverty_lines
for i in range(len(relative_poverty_lines)):
    #if it's the first value only get people below this poverty line (and percentage)
    if i == 0:
        varname_n = f'headcount_stacked_below_{relative_poverty_lines[i]}_median'
        df[varname_n] = df[f'headcount_{relative_poverty_lines[i]}_median']
        col_stacked_n.append(varname_n)

        varname_pct = f'headcount_ratio_stacked_below_{relative_poverty_lines[i]}_median'
        df[varname_pct] = df[varname_n] / df['reporting_pop']
        col_stacked_pct.append(varname_pct)

    #If it's the last value calculate the people between this value and the previous 
    #and also the people over this poverty line (and percentages)
    elif i == len(relative_poverty_lines)-1:

        varname_n = f'headcount_stacked_below_{relative_poverty_lines[i]}_median'
        df[varname_n] = df[f'headcount_{relative_poverty_lines[i]}_median'] - df[f'headcount_{relative_poverty_lines[i-1]}_median']
        col_stacked_n.append(varname_n)

        varname_pct = f'headcount_ratio_stacked_below_{relative_poverty_lines[i]}_median'
        df[varname_pct] = df[varname_n] / df['reporting_pop']
        col_stacked_pct.append(varname_pct)

        varname_n = f'headcount_stacked_above_{relative_poverty_lines[i]}_median'
        df[varname_n] = df['reporting_pop'] - df[f'headcount_{relative_poverty_lines[i]}_median']
        col_stacked_n.append(varname_n)

        varname_pct = f'headcount_ratio_stacked_above_{relative_poverty_lines[i]}_median'
        df[varname_pct] = df[varname_n] / df['reporting_pop']
        col_stacked_pct.append(varname_pct)

    #If it's any value between the first and the last calculate the people between this value and the previous (and percentage)
    else:
        varname_n = f'headcount_stacked_below_{relative_poverty_lines[i]}_median'
        df[varname_n] = df[f'headcount_{relative_poverty_lines[i]}_median'] - df[f'headcount_{relative_poverty_lines[i-1]}_median']
        col_stacked_n.append(varname_n)

        varname_pct = f'headcount_ratio_stacked_below_{relative_poverty_lines[i]}_median'
        df[varname_pct] = df[varname_n] / df['reporting_pop']
        col_stacked_pct.append(varname_pct)

df.loc[:, col_stacked_pct] = df[col_stacked_pct] * 100

# %%
col_povlines = ['median_40', 'median_40', 'median_60']
col_headcount = ['headcount_40_median', 'headcount_50_median', 'headcount_60_median']
col_headcount_ratio = ['headcount_ratio_40_median', 'headcount_ratio_50_median', 'headcount_ratio_60_median']
col_pgi = ['poverty_gap_index_40_median', 'poverty_gap_index_50_median', 'poverty_gap_index_60_median']
col_severity = ['poverty_severity_40_median', 'poverty_severity_50_median', 'poverty_severity_60_median']
col_watts = ['watts_40_median', 'watts_50_median', 'watts_60_median']
col_total_shortfall = ['total_shortfall_40_median', 'total_shortfall_50_median', 'total_shortfall_60_median']
col_avg_shortfall = ['avg_shortfall_40_median', 'avg_shortfall_50_median', 'avg_shortfall_60_median']
col_income_gap_ratio = ['income_gap_ratio_40_median', 'income_gap_ratio_50_median', 'income_gap_ratio_60_median']

# %%
df = df[['Entity', 'Year', 'reporting_level', 'welfare_type'] + col_povlines + col_headcount + col_headcount_ratio + col_pgi + col_severity + col_watts + col_total_shortfall + col_avg_shortfall + col_income_gap_ratio + col_stacked_n + col_stacked_pct]

# %%
df.to_csv('data/relative_poverty.csv', index=False)

# %%
