#%%
import pandas as pd
from pathlib import Path


#%%
# Make a list of all csv files in the relevant folder using pathlib
all_files = Path('API_output/percentiles/filled_data').glob('*.csv')

# Read in and concat (append together) all the files
df = pd.concat((pd.read_csv(f) for f in all_files))

#%%

# Write to .CSV
df.to_csv('API_output/percentiles/all_percentiles.csv', index=False)
#%%

# Cleaning - see notebook for discussion

# Drop headcount=0 observations
# Drop El Salvador and Sierra Leone (negative poverty lines)

