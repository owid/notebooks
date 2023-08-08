#%%
import pandas as pd
import numpy as np

from owid import catalog


#%%
lis_table = catalog.find('luxembourg_income_study').load()

df_lis = pd.DataFrame(lis_table).reset_index()




# %%


# %%
# Melt the DataFrame to convert it to a longer format
df_long = pd.melt(
    df_lis,
    id_vars=['country', 'year'],
    var_name='var_inc_concept',
    value_name='value'
)

# %%
df_long['welfare'] = ''
df_long['unit_resource_sharing'] = ''

# %%

for welfare_concept in ['dhi', 'mi', 'hcexp', 'dhci']:
    # tag the welfare concept
    df_long.loc[df_long['var_inc_concept'].str.contains(welfare_concept), 'welfare'] = welfare_concept
    # Remove the suffix (eventually we will be left with the indicator name)
    df_long['var_inc_concept'] = df_long['var_inc_concept'].str.replace(f'_{welfare_concept}', '')


# Count empty rows (should be 0)
df_long['welfare'].eq('').sum()

# %%
for unit in ['pc', 'eq']:
    # tag the unit of analysis/resource sharing concept
    df_long.loc[df_long['var_inc_concept'].str.contains(unit), 'unit_resource_sharing'] = unit
    # Remove the suffix (eventually we will be left with the indicator name)
    df_long['var_inc_concept'] = df_long['var_inc_concept'].str.replace(f'_{unit}', '')


# Count empty rows (should be 0)
df_long['unit_resource_sharing'].eq('').sum()


#%%
# Rename to 'indicator_code'
df_long.rename(columns={'var_inc_concept': 'indicator_code'}, inplace=True)



#%%
# Add indicator names

# Mapping dictionary for replacements
indicator_name_mapping = {
    'gini': 'Gini',
    'share_p90': 'Top 10% share',
    'share_p100': 'Top 1% share',
    'palma_ratio': 'Palma ratio',
    'headcount_ratio_50_median': 'Share below 50% median',
    # Add more mappings as needed
}


df_long['indicator_name'] = df_long['indicator_code'].map(indicator_name_mapping)


#%%
# Rename welfare concepts
keep_welfare = [
    'dhi',
    'mi',
    'hcexp'
]

df_long = df_long[df_long['welfare'].isin(keep_welfare)]

df_long['welfare'] = df_long['welfare'].replace('dhi', 'Disposable income')
df_long['welfare'] = df_long['welfare'].replace('mi', 'Market income')
df_long['welfare'] = df_long['welfare'].replace('hcexp', 'Expenditure')

# %% Keep only rows with indicator names
df_long = df_long.dropna(subset=['indicator_name'])

#%%
# Write to csv

df_long.to_csv('data/manipulation/lis_clean.csv', index=False)

