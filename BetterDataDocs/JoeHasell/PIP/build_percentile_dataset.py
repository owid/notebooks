#%%
import pandas as pd
from pathlib import Path


#%%
# Make a list of all csv files in the relevant folder using pathlib
all_files = Path('API_output/percentiles/filled_data').glob('*.csv')

# Read in and concat (append together) all the files
df = pd.concat((pd.read_csv(f) for f in all_files))
# %%

# Write to .CSV
df.to_csv(f'API_output/percentiles/all_percentiles.csv', index=False)
#%%