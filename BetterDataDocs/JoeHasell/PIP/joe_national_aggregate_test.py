#%%

import pandas as pd
from functions.PIP_API_query import pip_query_country, pip_query_region
import time
import plotly.express as px

#%%
id_vars = ['country_name', 'reporting_year','reporting_level','welfare_type']

#%%
query_durations = {"povline":[],"duration":[]}

#%%
# Define list of poverty lines to query

under_10_dollars = list(range(1,1000, 1))

between_10_and_30_dollars = list(range(1000,3000, 2))

between_30_and_100_dollars = list(range(3000,10000, 5))

#%%
povline_list_dict = {
    'under_10_dollars': under_10_dollars, 
    'between_10_and_30_dollars': between_10_and_30_dollars,
    'between_30_and_100_dollars': between_30_and_100_dollars
                    }


#povlines_cents = under_10_dollars + between_10_and_30_dollars + between_30_and_100_dollars

#povlines_cents_test = range(100,200,1)

#%%

start_time_overall = time.time()

for key in povline_list_dict:


    df_complete = pd.DataFrame()


    for povline in povline_list_dict[key]:

        start_time = time.time()

        povline_dollars = povline/100
        print(f'Fetching headcounts for: ${povline_dollars} a day')


        #For China, India and Indonesia use on the second line: CHN&country=IND&country=IDN
        df = pip_query_country("povline", povline_dollars, 
                        "all", 
                        "all", "false", "all", "all")



        df_complete = pd.concat([df_complete, df],ignore_index=True)


        end_time = time.time()
        query_durations["povline"].append(povline_dollars)
        query_durations["duration"].append(end_time - start_time)


    #Write the complete data to csv
    df_complete.to_csv(f'data/full_dist/{key}.csv')

end_time_overall = time.time()


#%%


# %%
elapsed_time_overall = end_time_overall - start_time_overall

print(f'Execution time: {elapsed_time_overall/60} minutes')

#%%
# Take a look at how long each query took
df_query_durations = pd.DataFrame.from_dict(query_durations)

fig = px.line(df_query_durations, x="povline", y="duration", title=f'Execution time for poverty line queries')
fig.show()

fig.write_image(f'graphics/time_plot.svg')


# %%
# Find closest to percentiles

percentiles = range(1, 100, 1)

df_closest_complete = pd.DataFrame()

for p in percentiles:

    df_complete['distance_to_p'] = abs(df_complete['headcount']-p/100)

    df_closest = df_complete.sort_values("distance_to_p").groupby(['country_name', 'reporting_year','reporting_level','welfare_type'], as_index=False).first()

    df_closest['target_percentile'] = f'P{p}'

    df_closest = df_closest[['country_name', 'reporting_year','reporting_level','welfare_type', 'target_percentile', 'poverty_line', 'headcount', 'distance_to_p']]

    df_closest_complete = pd.concat([df_closest_complete, df_closest],ignore_index=True)

# %%
