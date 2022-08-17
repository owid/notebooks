#%%
# Close and reopen VS code before running this each time.

#%%

import pandas as pd
from functions.PIP_API_query import pip_query_country, pip_query_region
import time
import gc # for tidying up memory
import plotly.express as px


#%%
id_vars = ['country_name', 'reporting_year','reporting_level','welfare_type']

#%%
# Define list of poverty lines to query
povlines_cents_test = range(170,200,1)

#%%
query_durations = {"povline":[],"duration":[]}


#%%
df_complete = pd.DataFrame()


#%%
clear_memory = False

for povline in povlines_cents_test:

    start_time = time.time()

    povline_dollars = povline/100
    print(f'Fetching headcounts for: ${povline_dollars} a day')


    #For China, India and Indonesia use on the second line: CHN&country=IND&country=IDN
    df = pip_query_country("povline", povline_dollars, 
                        "all", 
                        "all", "false", "all", "all")



    df_complete = pd.concat([df_complete, df],ignore_index=True)

    if clear_memory:
        del df
        gc.collect()
    
    end_time = time.time()


    query_durations["povline"].append(povline_dollars)
    query_durations["duration"].append(end_time - start_time)


#%%
df_query_durations = pd.DataFrame.from_dict(query_durations)

fig = px.line(df_query_durations, x="povline", y="duration", title=f'Execution time for poverty line queries – clear memory = {clear_memory}')
fig.show()

fig.write_image(f'graphics/time_plot_clear_memory_{clear_memory}.svg')

# %%
