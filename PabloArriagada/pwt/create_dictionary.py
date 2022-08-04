import pandas as pd
import json
# +
match = pd.read_excel('staging.xlsx', sheet_name='9.1')
match = match.dropna(subset=['new_var_id']).reset_index(drop=True)

match['new_var_id'] = match['new_var_id'].astype(int)
match['old_var_id'] = match['old_var_id'].astype(int)
match['new_var_id'] = match['new_var_id'].astype(str)
match['old_var_id'] = match['old_var_id'].astype(str)
# -

match

var_dict = pd.Series(match.new_var_id.values,index=match.old_var_id).to_dict()
var_dict

with open('variable_replacements_staging.json', 'w') as fp:
    json.dump(var_dict, fp, indent=4)

# +
# Specify sheet id and sheet (tab) name for the metadata google sheet 
sheet_id = '1gbk8lBc4ZTjzE94pG8vgFX1Ta5baIQhpdD158GhPJsc'
var_meta_sheetname = 'variable_metadata'
data_meta_sheetname = 'dataset_metadata'

# Read in variable metadata as dataframe
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={var_meta_sheetname}'
match = pd.read_csv(url)
# -

match

# +
match = match.dropna(subset=['old_var_id']).reset_index(drop=True)

match['new_var_id'] = match['new_var_id'].astype(int)
match['old_var_id'] = match['old_var_id'].astype(int)
match['new_var_id'] = match['new_var_id'].astype(str)
match['old_var_id'] = match['old_var_id'].astype(str)
# -

var_dict = pd.Series(match.new_var_id.values,index=match.old_var_id).to_dict()
var_dict

with open('variable_replacements_live.json', 'w') as fp:
    json.dump(var_dict, fp, indent=4)
