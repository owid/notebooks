
#%%

import pandas as pd

#%%
source_data = {}

for source in ['wid', 'wid_extrapolated', 'pip', 'lis']:
    print(source)
    #Load clean data
    df = pd.read_csv(f'data/manipulation/{source}_clean.csv')

    #Add to dict
    source_data[source] = df


#%% Concat into single df and tidy index
df = pd.concat(source_data)\
        .reset_index()\
        .rename(columns={
             'level_0': 'source'
            })\
        .drop(columns=['level_1'])


#%% Drop any NaN rows
df = df.dropna(subset=['value'])




# Add population data


# Add region classification

#%% Write to csv
df.to_csv('data/clean/indicators_dataset.csv', index=False)