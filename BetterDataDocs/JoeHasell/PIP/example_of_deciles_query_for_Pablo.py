
#%%
import pandas as pd

from functions.PIP_API_query import pip_query_country, pip_query_region

import plotly.express as px


#%%
deciles = [1,2,3,4,5,6,7,8,9]

#%%
deciles = [1, 2]

df_complete = pd.DataFrame()


for dec in deciles:

    popshare = dec/10
    
    df = pip_query_country(
                    popshare_or_povline = "popshare", 
                    value = popshare, 
                    fill_gaps='false')

    df = df[["country_name",'reporting_year', 'reporting_level', 'survey_acronym',
       'survey_coverage', 'survey_year', 'welfare_type', 'poverty_line', 'headcount']]

    df['requested_decile'] = dec

    df_complete = pd.concat([df_complete, df],ignore_index=True)

#%%
# Note that the returned headcount is not exactly equal to the requested percentile 
# (presumably due to the descrete nature of the survey data)
df['compare_requested_actual_p'] = (df['requested_decile']/10)/df['headcount']

fig = px.histogram(df, x="compare_requested_actual_p")
fig.show()

# %%
