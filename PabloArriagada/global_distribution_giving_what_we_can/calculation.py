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

# Extract data from WDI
df_wdi = catalog.find('wdi', version='2023-05-29').load()
df_wdi = pd.DataFrame(df_wdi)

df_wdi = df_wdi[['pa_nus_ppp', 'pa_nus_prvt_pp']].reset_index()

# Filter for the latest year
df_wdi = df_wdi[df_wdi['year'] == df_wdi['year'].max()].reset_index(drop=True)

# Remove countries including "(WB)", World and WB groups
for agg in ['\\(WB\\)', 'World', 'income countries']:
    df_wdi = df_wdi[~df_wdi['country'].str.contains(agg)].reset_index(drop=True)

# Remove nans in pa_nus_prvt_pp
df_wdi = df_wdi[~df_wdi['pa_nus_prvt_pp'].isna()].reset_index(drop=True)

# Drop pa_nus_ppp
df_wdi = df_wdi.drop(columns=['pa_nus_ppp'])

# Sort by country
df_wdi = df_wdi.sort_values(by=['country']).reset_index(drop=True)

# Export to csv
df_wdi.to_csv(f'{PARENT_DIR}/wdi_conversion_factors.csv', index=False)



