#%%

import pandas as pd
from functions.PIP_API_query import pip_query_country, pip_query_region
import time

#%%
id_vars = ['country_name', 'reporting_year','reporting_level','welfare_type']


#%%

start_time = time.time()

df_complete = pd.DataFrame()


povlines_cents = range(1,100, 1)

for povline in povlines_cents:

    povline_dollars = povline/100

    df = pip_query_country("povline", povline_dollars, 
                        "CHN&country=IND&country=IDN", 
                        "all", "false", "all", "all")



    df_complete = pd.concat([df_complete, df],ignore_index=True)

end_time = time.time()

# %%
elapsed_time = end_time - start_time
print('Execution time:', elapsed_time, 'seconds')


# %%
# Find closest to percentiles

percentiles = range(10, 100, 10)

df_closest_complete = pd.DataFrame()


for p in percentiles:

    df['distance_to_p'] = abs(df['headcount']-p/100)

    df_closest = df.groupby(['country_name', 'reporting_year','reporting_level','welfare_type'])['distance_to_p'].min().reset_index()

    df_closest = pd.merge(df_closest, df, how = 'left')

    df_closest['target_percentile'] = f'P{p}'

    df_closest = df_closest[['country_name', 'reporting_year','reporting_level','welfare_type', 'target_percentile', 'poverty_line', 'headcount', 'distance_to_p']]

    df_closest_complete = pd.concat([df_closest_complete, df_closest],ignore_index=True)

# %%
