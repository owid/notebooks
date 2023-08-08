
#%%
import pandas as pd

from owid import catalog


# %%
wid_table = catalog.find('world_inequality_database').load()
df_wid = pd.DataFrame(wid_table).reset_index()


# %%
# Melt the DataFrame to convert it to a longer format
df_long = pd.melt(
    df_wid,
    id_vars=['country', 'year'],
    var_name='var_inc_concept',
    value_name='value'
)


# %%
df_long['welfare'] = ''

# %%

for welfare_concept in ['pretax', 'posttax_dis', 'posttax_nat', 'wealth']:
    # tag the welfare concept
    df_long.loc[df_long['var_inc_concept'].str.contains(welfare_concept), 'welfare'] = welfare_concept
    # Remove the suffix (eventually we will be left with the indicator name)
    df_long['var_inc_concept'] = df_long['var_inc_concept'].str.replace(f'_{welfare_concept}', '')


# Count empty rows (should be 0)
df_long['welfare'].eq('').sum()


#%%
# Rename welfare concepts
keep_welfare = [
    'pretax',
    'posttax_nat',
    'posttax_dis'
]

df_long = df_long[df_long['welfare'].isin(keep_welfare)]

df_long['welfare'] = df_long['welfare'].replace('pretax', 'Pre-tax national income')
df_long['welfare'] = df_long['welfare'].replace('posttax_nat', 'Post-tax national income')
df_long['welfare'] = df_long['welfare'].replace('posttax_dis', 'Disposable income')



# %%
# Dummy for extrapolated series or not
df_long['extrapolated_series'] = 0

# tag if extrapolated series
df_long.loc[df_long['var_inc_concept'].str.contains('_extrapolated'), 'extrapolated_series'] = 1
# Remove the suffix (eventually we will be left with the indicator name)
df_long['var_inc_concept'] = df_long['var_inc_concept'].str.replace('_extrapolated', '')


# %%
# Rename to 'indicator_code'
df_long.rename(columns={'var_inc_concept': 'indicator_code'}, inplace=True)



# %%
# Search for indicator codes
# check = df_long[df_long['indicator_code'].str.contains('palma')]
# check['indicator_code'].unique()

# %%
# Mapping indicator codes to names
# dictionary for replacements
indicator_name_mapping = {
    'p0p100_gini': 'Gini',
    'p90p100_share': 'Top 10% share',
    'p99p100_share': 'Top 1% share',
    'palma_ratio': 'Palma ratio',
    #'headcount_ratio_50_median': 'Share below 50% median',
    # Add more mappings as needed
}

# map to new columns
df_long['indicator_name'] = df_long['indicator_code'].map(indicator_name_mapping)


# %%
#Add description of unit of analysis/resource sharing concept (same for all WID data within OWID)
df_long['unit_resource_sharing'] = 'Household or tax unit, per adult'

# %% Keep only rows with indicator names
df_long = df_long.dropna(subset=['indicator_name'])


#%% Drop regions
# Regions are coded as 'Region name (WID), except for World

df_long = df_long[~df_long['country'].str.contains('(WID)')]
df_long = df_long[df_long['country']!='World']

#%% Drop subnational territories
# There are some entities with '- rural' and '-urban' suffixes
df_long = df_long[~df_long['country'].str.contains('rural')]
df_long = df_long[~df_long['country'].str.contains('urban')]


# %% Split extrapolated and not extrapolated series and write to csv

df_not_extrapolated = df_long[df_long['extrapolated_series']==0].drop(columns='extrapolated_series')

df_not_extrapolated.to_csv("data/manipulation/wid_clean.csv", index=False)


df_extrapolated = df_long[df_long['extrapolated_series']==1].drop(columns='extrapolated_series')

df_extrapolated.to_csv("data/manipulation/wid_extrapolated_clean.csv", index=False)

