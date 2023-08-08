#%%
import pandas as pd

from functions import * 

#%% Load clean data
df = pd.read_csv('data/clean/indicators_dataset.csv')

#%% select series
selection_dict = {
    'series_short_name': ['WID gini', 'Lis Gini'],
    'source': ['wid', 'lis'],
    'indicator_name': ['Gini', 'Gini'],
    'welfare': ['Pre-tax national income', 'Disposable income'],
    'unit_resource_sharing': ['Household or tax unit, per adult', 'eq']
}
#%%
closest_to_reference(
    df = df,
    selection_dict = selection_dict,
    reference_year = 2011,
    max_dist_from_ref = 2,
    tie_break = 'below')

#%%
matches = matched_pairs_not_pip(
    df = df,
    selection_dict = selection_dict,
    reference_years = [1990, 2018],
    max_dist_from_ref = 5,
    min_dist_between = 0)

#%% 
pip_selection_dict = {
    'series_short_name': ['PIP gini', 'PIP palma'],
    'source': ['pip', 'pip'],
    'indicator_name': ['Gini', 'Palma ratio']
}
# %%
pipmatches = matched_pairs_pip(
    df = df_data,
    selection_dict = pip_selection_dict,
    reference_years = [1990, 2018],
    max_dist_from_ref = 5,
    min_dist_between = 0,
    constant_reporting_level=True,
    constant_welfare_type=False)
# %%

all_matches = pd.concat([matches, pipmatches])
# %%
