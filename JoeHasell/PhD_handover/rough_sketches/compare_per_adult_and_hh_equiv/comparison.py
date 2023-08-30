#%%
import plotly.express as px
import pandas as pd
import statsmodels.api as sm
# from sklearn import linear_model

#%% Load data (provided in email from PabloA)
na_values = ['.']

df_pip_world = pd.read_csv('lis_keyvars_pc.csv', na_values=na_values)
df_pip_world = df_pip_world[df_pip_world['variable']=='dhi']

df_wid_world = pd.read_csv('lis_keyvars_pc_adults.csv', na_values=na_values)
df_wid_world = df_wid_world[df_wid_world['variable']=='mi']


#%% merge
df = df_pip_world.merge(df_wid_world, on=['dataset'],suffixes=('_pip_world', '_wid_world') )




#%% compare inequality
select_metric = 'gini'

df_selected = df[['dataset', f'{select_metric}_pip_world', f'{select_metric}_wid_world', 'mean_pip_world',]].dropna()

df_selected['ratio'] = df[f'{select_metric}_pip_world']/df[f'{select_metric}_wid_world']

fig = px.scatter(
    df_selected, 
    x="mean_pip_world", y="ratio",
    title=f'{select_metric}_pip_world/{select_metric}_wid_world'
)
fig.show()

#%% compare means

df_selected = df[['dataset', 'mean_pip_world', 'mean_wid_world']].dropna()

df_selected['ratio'] = df['mean_pip_world']/df['mean_wid_world']

fig = px.scatter(
    df_selected, 
    x="mean_pip_world", y="ratio",
    title="mean_pip_world/mean_wid_world"
)
fig.show()

#%% Scatter with plotly


# %%
