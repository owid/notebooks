#%%
import pandas as pd

from API_query_lists import percentiles

#%%
#Make an empty dataframe into which the data for each percentil will be appended
df = pd.DataFrame(columns=['entity', 'year', 'threshold', 'headcount'])
#%%

for p in percentiles:

    print(f"Reading P{p}")
    #Read in the csv as dataframe
    p_file = f'API_output/percentiles/filled_data/P{p}.csv'
    df_p = pd.read_csv(p_file)

    #Append to running dataframe
    df = pd.concat(df, df_p)

    # Write to .CSV
    df.to_csv(f'API_output/percentiles/all_percentiles.csv')


#%%