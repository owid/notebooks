
#%%
import pandas as pd

# PERCENTILE DATA
#%%
# Percentile data is here:
# https://datacatalog.worldbank.org/search/dataset/0063646

# Load locally-saved file
fp = "data/original/pip_percentiles.csv"

df_pip_percentiles = pd.read_csv(fp)
#%%

#%%
# Select top 1% shares to add to 'main metrics'

# drop/rename cols
drop_cols = ['percentile', 'avg_welfare', 'pop_share', 'quantile']

df_pip_percentiles = df_pip_percentiles[df_pip_percentiles['percentile'] == 100]\
  .drop(drop_cols, axis=1)\
  .rename(columns={
    'welfare_share': 'p99p100_share'
  })


# Convert shares to percent
df_pip_percentiles['p99p100_share'] = df_pip_percentiles['p99p100_share'] * 100

#%%
# Standardize country names in percentile data

# # Initially I save a csv of country-codes included in the percentile data, to pass through the OWID country name standardization tool
# unique_countries = df_pip_percentiles['country_code'].unique()
# df_pip_percentiles_countries = pd.DataFrame({'country': unique_countries})

# df_pip_percentiles_countries.to_csv('data/original/pip_percentiles_countries.csv', index=False)


# Read in name mapping file
fp = 'data/original/pip_percentiles_countries_country_standardized.csv'
name_mapping = pd.read_csv(fp)


# Merge mapping into data

df_pip_percentiles = pd.merge(df_pip_percentiles, name_mapping, left_on='country_code', right_on='country', how = 'left')

# Drop columns used in the construction of the standardized country column
df_pip_percentiles = df_pip_percentiles.drop(columns=['country','country_code'])

df_pip_percentiles = df_pip_percentiles.rename(columns = {'Our World In Data Name': 'country'})


#%%
# Inspect
df_pip_percentiles.head()

#%%
# Write clean top shares data to csv

df_pip_percentiles.to_csv(
    'data/manipulation/pip_clean_top1_shares.csv',
    index=False)



# MAIN INDICATORS
#%%
# Load PIP main data

df_pip = pd.read_csv("https://raw.githubusercontent.com/owid/poverty-data/main/datasets/pip_dataset.csv")

#  A local version, in case internet isn't available 
# df_pip = pd.read_csv("data/original/pip_dataset.csv")
#%%
# Inspect
df_pip.head()

# %%
# Select 2017 PPP version
df_pip = df_pip.loc[df_pip["ppp_version"] == 2017]


#%%
# Merge top 1% shares from percentile data into main PIP data
df_pip = pd.merge(df_pip, df_pip_percentiles, on=['country', 'year', 'reporting_level', 'welfare_type'], how='left')

df_pip.head()



# Drop regional data

#%%
# The dataset includes aggregated estiates for world regions.
# Here we define a list of these aggregate entities and drop them from the data.

drop_aggs = [
  "East Asia and Pacific",
  "South Asia",
  "Europe and Central Asia",
  "High income countries",
  "Latin America and the Caribbean",
  "Middle East and North Africa",
  "Sub-Saharan Africa",
  "World"
]

df_pip = df_pip.loc[~df_pip.country.isin(drop_aggs)]



# Drop sub-national data
# %%
# The PIP data includes observations for national, urban and rural populations
df_pip.groupby('reporting_level').count()

# %%
# Add a count of number of reporting levels
df_pip['n_reporting_level'] = df_pip\
  .groupby(["country", "year"])['reporting_level']\
  .transform('nunique')


# %%
# NB some country-years have three reporting levels.
df_pip.groupby('n_reporting_level').count()
# %%

multi_reporting_level_countries = df_pip.loc[df_pip['n_reporting_level'] == 3, "country"].unique()
print('These countries have three reporting levels: ')
multi_reporting_level_countries

# %%
# For country-years with 3 reporting levels, we keep only the national estimates. 
df_pip = df_pip.loc[(df_pip['n_reporting_level'] != 3) | (df_pip['reporting_level'] == 'national') ]

# %% Drop non-ID, non-value cols
df_pip = df_pip.drop(columns=['ppp_version','survey_year','survey_comparability'])


# %%
# Melt the DataFrame to convert it to a longer format
df_long = pd.melt(
    df_pip,
    id_vars=['country', 'year', 'reporting_level', 'welfare_type'],
    var_name='indicator_code',
    value_name='value'
)


# %%
# Search for indicator codes
check = df_long[df_long['indicator_code'].str.contains('headcount_ratio_50_median')]
check['indicator_code'].unique()

#%%
# Add indicator names

# Mapping dictionary for replacements
indicator_name_mapping = {
    'gini': 'Gini',
    'decile10_share': 'Top 10% share',
    'p99p100_share': 'Top 1% share',
    'palma_ratio': 'Palma ratio',
    'headcount_ratio_50_median': 'Share below 50% median',
    # Add more mappings as needed
}


df_long['indicator_name'] = df_long['indicator_code'].map(indicator_name_mapping)



# %% Keep only rows with indicator names
df_long = df_long.dropna(subset=['indicator_name'])


#%% Rename PIP-only columns
df_long = df_long.rename(columns={
    'reporting_level': 'pip_reporting_level',
    'welfare_type': 'pip_welfare'
  })

#%% Add a welfare column (harmonized structure with other sources)
df_long['welfare'] = ''

df_long.loc[df_long['pip_welfare']=='income', 'welfare'] = 'Disposable income'
df_long.loc[df_long['pip_welfare']=='consumption', 'welfare'] = 'Consumption'



#Add description of unit of analysis/resource sharing concept
df_long['unit_resource_sharing'] = 'Household, per capita'


#%%
# Write to csv

df_long.to_csv('data/manipulation/pip_clean.csv', index=False)

