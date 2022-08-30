
#%%
import pandas as pd
import plotly.express as px



#%%
df_filled = pd.read_csv('data/API_output/example_response_filled.csv')

df_survey = pd.read_csv('data/API_output/example_response_survey.csv')


#%%
select_country = 'Botswana'
select_var = 'gini'

df_filled_filter = df_filled[(df_filled['country_name']==select_country) & (df_filled['reporting_level']=='national')][['reporting_year', select_var]]
df_filled_filter['filled_status'] = 'filled'

df_survey_filter = df_survey[(df_survey['country_name']==select_country) & (df_survey['reporting_level']=='national')][['reporting_year', select_var]]
df_survey_filter['filled_status'] = 'not filled'

df_plot = pd.concat([df_filled_filter, df_survey_filter])

#%%
fig = px.line(df_plot, x="reporting_year", y=select_var, color='filled_status', title=f"{select_country} – {select_var}", markers=True)
fig.show()


# %%
