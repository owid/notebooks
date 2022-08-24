import pandas as pd
import json
# ## Staging

# +
match = pd.read_excel('data/variable_matching/variable_matching.xlsx', sheet_name='Staging')
match = match.dropna(subset=['new_var_id']).reset_index(drop=True)
match = match.dropna(subset=['old_var_id']).reset_index(drop=True)

match['new_var_id'] = match['new_var_id'].astype(int)
match['old_var_id'] = match['old_var_id'].astype(int)
match['new_var_id'] = match['new_var_id'].astype(str)
match['old_var_id'] = match['old_var_id'].astype(str)
# -

match

var_dict = pd.Series(match.new_var_id.values,index=match.old_var_id).to_dict()
var_dict

with open('data/variable_matching/variable_replacements_staging.json', 'w') as fp:
    json.dump(var_dict, fp, indent=4)

# ## Live (careful)

# +
match = pd.read_excel('data/variable_matching/variable_matching.xlsx', sheet_name='Live')
match = match.dropna(subset=['new_var_id']).reset_index(drop=True)
match = match.dropna(subset=['old_var_id']).reset_index(drop=True)

match['new_var_id'] = match['new_var_id'].astype(int)
match['old_var_id'] = match['old_var_id'].astype(int)
match['new_var_id'] = match['new_var_id'].astype(str)
match['old_var_id'] = match['old_var_id'].astype(str)
# -

match

var_dict = pd.Series(match.new_var_id.values,index=match.old_var_id).to_dict()
var_dict

with open('data/variable_matching/variable_replacements.json', 'w') as fp:
    json.dump(var_dict, fp, indent=4)
