from pathlib import Path

import pandas as pd
from owid import catalog

PARENT_DIR = Path(__file__).parent.absolute()

df = pd.read_feather(f'{PARENT_DIR}/pip_percentiles.feather')

# Filter data to only include country=World and ppp_version = 2017
df = df[(df['country'] == 'World') & (df['ppp_version'] == 2017)].reset_index(drop=True)


# Compare thr values with the one in the previous row
df['thr_previous'] = df['thr'].groupby(df['year']).shift(1)
df['thr_check'] = df['thr'] >= df['thr_previous']

# Assert that all values are True
df_check = df[(df['thr_check']) & (df['target_percentile'] != 1)]
assert df_check['thr_check'].all(), 'The global distribution is not monotonically increasing'

# Assert that distance to p is always less than 0.5
assert (df['distance_to_p'] <= 0.5).all(), 'There are estimations that are more than 0.5 away from target_percentile'

# Keep only the relevant columns
df = df[['country', 'year', 'target_percentile', "thr"]]

# Filter for the latest year
df = df[df['year'] == df['year'].max()].reset_index(drop=True)

# Export to csv
df.to_csv(f'{PARENT_DIR}/pip_global_percentiles.csv', index=False)

# PPP CONVERSION FACTORS
# Load ppp conversion factors and CPI
df_ppp_factors = pd.read_csv(f'{PARENT_DIR}/API_PA.NUS.PRVT.PP_DS2_en_csv_v2_5996116.csv', skiprows=4)
df_cpi = pd.read_csv(f'{PARENT_DIR}/API_FP.CPI.TOTL_DS2_en_csv_v2_5994751.csv', skiprows=4)

# Remove columns containing "Unnamed" in their name
columns_to_drop = [col for col in df_ppp_factors.columns if 'Unnamed' in col]
df_ppp_factors = df_ppp_factors.drop(columns=columns_to_drop)

# Remove columns containing "Unnamed" in their name
columns_to_drop = [col for col in df_cpi.columns if 'Unnamed' in col]
df_cpi = df_cpi.drop(columns=columns_to_drop)

# Drop "Indicator Name","Indicator Code"
columns_to_drop = ['Indicator Name', 'Indicator Code']
df_ppp_factors = df_ppp_factors.drop(columns=columns_to_drop)
df_cpi = df_cpi.drop(columns=columns_to_drop)

# Select in df_ppp_factors only the columns of interest (Country Name, Country Code, 2017)
df_ppp_factors = df_ppp_factors[['Country Name', 'Country Code', '2017']]
df_ppp_factors = df_ppp_factors.rename(columns={'Country Name': 'country', 'Country Code': 'country_code', '2017': 'pa_nus_prvt_pp_2017'})

# Make df_cpi long
df_cpi = df_cpi.melt(id_vars=['Country Name', 'Country Code'], var_name='year', value_name='cpi')
df_cpi = df_cpi.rename(columns={'Country Name': 'country', 'Country Code': 'country_code'})

# Make year integer
df_cpi['year'] = df_cpi['year'].astype(int)

# Find maximum year
MAX_YEAR = df_cpi['year'].max()

# Filter for 2017 and the maximum year
df_cpi = df_cpi[(df_cpi['year'] == 2017) | (df_cpi['year'] == MAX_YEAR)].reset_index(drop=True)

# Make table wide, by naming the columns cpi_2017 and cpi_max
df_cpi = df_cpi.pivot(index='country_code', columns='year', values='cpi').reset_index()

# Rename columns
df_cpi = df_cpi.rename(columns={2017: 'cpi_2017', MAX_YEAR: 'cpi_max'})

# Calculate the inflation rate between 2017 and the maximum year
df_cpi['inflation_rate'] = df_cpi['cpi_max'] / df_cpi['cpi_2017']

# Merge df_ppp_factors and df_cpi
df_ppp = df_ppp_factors.merge(df_cpi[["country_code", "cpi_2017", "cpi_max", "inflation_rate"]], on='country_code', how='left')

# Calculate the ppp conversion factor for the most recent year
df_ppp['ppp_factor'] = df_ppp['pa_nus_prvt_pp_2017'] * df_ppp['inflation_rate']

# Remove empty values of pa_nus_prvt_pp
df_ppp = df_ppp[~df_ppp['ppp_factor'].isna()].reset_index(drop=True)

# Sort by country
df_ppp = df_ppp.sort_values(by=['country']).reset_index(drop=True)

# Export to csv
df_ppp.to_csv(f'{PARENT_DIR}/wdi_ppp.csv', index=False)


# # Extract data from WDI
# df_wdi = catalog.find('wdi', version='2023-05-29').load()
# df_wdi = pd.DataFrame(df_wdi)

# df_wdi = df_wdi[['pa_nus_ppp', 'pa_nus_prvt_pp']].reset_index()

# # Filter for the latest year
# df_wdi = df_wdi[df_wdi['year'] == df_wdi['year'].max()].reset_index(drop=True)

# # Remove countries including "(WB)", World and WB groups
# for agg in ['\\(WB\\)', 'World', 'income countries']:
#     df_wdi = df_wdi[~df_wdi['country'].str.contains(agg)].reset_index(drop=True)

# # Remove nans in pa_nus_prvt_pp
# df_wdi = df_wdi[~df_wdi['pa_nus_prvt_pp'].isna()].reset_index(drop=True)

# # Drop pa_nus_ppp
# df_wdi = df_wdi.drop(columns=['pa_nus_ppp'])

# # Sort by country
# df_wdi = df_wdi.sort_values(by=['country']).reset_index(drop=True)

# # Export to csv
# df_wdi.to_csv(f'{PARENT_DIR}/wdi_conversion_factors.csv', index=False)



