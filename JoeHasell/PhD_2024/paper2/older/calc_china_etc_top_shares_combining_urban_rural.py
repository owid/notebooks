#%%
import pandas as pd
import numpy as np


### GET RURAL/UBAN POPULATION DATA FOR CHINA, INDIA AND INDONESIA FROM PIP API
#%%

# Fetch the data (for an arbitrary poverty line) from the PIP API endpoint URL
url = "https://api.worldbank.org/pip/v1/pip?country=all&year=all&povline=2.15&fill_gaps=false&additional_ind=false&ppp_version=2017"
df_pip_api = pd.read_json(url)

# %%
# Filter for China, India and Indonesia's urban and rural population over time
keep_countries = ['China', 'India', 'Indonesia']
keep_reporting_levels = ['urban', 'rural']

df_patch_pops = df_pip_api[
    (df_pip_api['country_name'].isin(keep_countries)) & \
    (df_pip_api['reporting_level'].isin(keep_reporting_levels)) ]

# %%
# Keep only population and ID cols
columns_to_keep = ['country_name', 'reporting_year', 'reporting_level', 'welfare_type', 'reporting_pop']
df_patch_pops = df_patch_pops[columns_to_keep]

# %%
df_patch_pops.rename(columns={
    'country_name': 'country',
    'reporting_year': 'year',
    'reporting_level': 'pipreportinglevel', 
    'welfare_type': 'pipwelfare',
    'reporting_pop': 'population'
    }, inplace=True)


### PREP CHINA ETC. NATIONAL SHARES DATA

#%% Load data prepared by Pablo containing the rural and urban data for China, India and Indonesia
fp = "https://catalog.ourworldindata.org/explorers/poverty_inequality/latest/poverty_inequality_export/percentiles.feather"
df_percentiles = pd.read_feather(fp)

#%% Select the percentile averages for rural/urban China etc.
df_selected_avgs = df_percentiles[(
    df_percentiles['country'].isin(keep_countries)) \
    & (df_percentiles['pipreportinglevel'].isin(keep_reporting_levels)) \
    & (df_percentiles['series_code']=='average_pip_disposable_perCapita_2017ppp2017')
    ]
# %% Merge in population data
df_selected_avgs = pd.merge(df_selected_avgs, df_patch_pops, how='left')

# Calculate popualtion weights
df_selected_avgs['population_by_group'] = df_selected_avgs.groupby(['country', 'year', 'pipwelfare'])['population'].transform('sum')
df_selected_avgs['population_weight'] = df_selected_avgs['population'] / df_selected_avgs['population_by_group']


# %%
# This is a function that calculates the national top 1% income
# share from urban and rural percentile data (and populations).
# It calculates the cumulative income share and cumulative population share 
# over percentiles of both rural and urban reporting levels. 
# It uses linear interpolation to account for the discrete
# income bins (percentiles) in which the data is stored. It finds the first (urban or rural)
# percentile falling within the top 1% of the combined national population and then
# linearly interpolates the income share between that
# and the adjacent (poorer) percentile. This gives an estimate of national top
# 1% income share at exactly the p99 cut off (rather than the discrete cut offs resulting
# from the population size of the urban and rural percentiles). 
def linear_interp_top_share(df_group, p):    


    # sort by average income level, descending
    sorted_group = df_group.sort_values(by='value')

    #Calculate cumulative population share and total income
    sorted_group['cumulative_pop_share'] = sorted_group['population_weight'].cumsum()
    sorted_group['total_income'] = sorted_group['value'] * sorted_group['population_weight']


    # Total income
    total_income = sorted_group['total_income'].sum()

    # Cumulative income share
    sorted_group['income_share'] = sorted_group['total_income']/ total_income
    sorted_group['cumulative_income_share'] = sorted_group['income_share'].cumsum()

    # Check if any individual falls into the top 1%
    if not sorted_group[sorted_group['cumulative_pop_share'] > p].empty:

        # Identify the first indiviidual in the top 1%
        first_included = sorted_group[sorted_group['cumulative_pop_share']>p].iloc[0]
        first_included_index = sorted_group.index.get_loc(first_included.name)

        # Linearly interpolate the income share of bottom 99% between discrete bins
        x0 = sorted_group.iloc[first_included_index-1]['cumulative_pop_share']
        x1 = sorted_group.iloc[first_included_index]['cumulative_pop_share']

        y0 = sorted_group.iloc[first_included_index-1]['cumulative_income_share']
        y1 = sorted_group.iloc[first_included_index]['cumulative_income_share']

        x = p

        y = y0 + (x - x0) * ((y1 - y0)/(x1 - x0))

        # Top 1% share is 1 - bottom 99% share
        top_1_percent_share = 1 - y

    else: 
        # Return NaN if no rows meet the condition
        top_1_percent_share = float('nan')


    return top_1_percent_share





# %% test the function

df_group = df_selected_avgs[
    (df_selected_avgs['country']=='Indonesia') & \
    (df_selected_avgs['year']==1990) & \
    (df_selected_avgs['pipwelfare']=='consumption')        
    ]

test = linear_interp_top_share(df_group, p=0.99)

# %% Calculate top 1% share (p=.99) by group, add metadata cols, and save
china_etc_topshares = df_selected_avgs.groupby(['country', 'year', 'pipwelfare'])\
    .apply(linear_interp_top_share, p=0.99)\
    .reset_index(name='value')

# Export as csv
china_etc_topshares.to_csv(f'data/top_pip_shares_comparison/china_etc_top1shares.csv', index=False)

# %%


# %% Calculate top 10% share (p=.9) by group and save
china_etc_topshares = df_selected_avgs.groupby(['country', 'year', 'pipwelfare'])\
    .apply(linear_interp_top_share, p=0.9)\
    .reset_index(name='value')

# Export as csv
china_etc_topshares.to_csv(f'data/top_pip_shares_comparison/china_etc_top10shares.csv', index=False)

# %%