# # Historical poverty data from Michalis Moatsos

import pandas as pd
from functools import reduce
from functions.standardize_entities import standardize_entities
import plotly.express as px
import plotly.io as pio

global_oecd = pd.read_csv('data/input/GlobalOECD.csv')
global_5 = pd.read_csv('data/input/Global5.csv')
global_10 = pd.read_csv('data/input/Global10.csv')
global_30 = pd.read_csv('data/input/Global30.csv')

data_frames = [global_oecd, global_5, global_10, global_30]
df_final = reduce(lambda  left,right: pd.merge(left,right,on=['Region', 'Year'],
                                            how='outer'), data_frames)
df_final = df_final.rename(columns={'Region': 'Entity'})

cols = ['PovRate', 'PovRate1.9', 'PovRateAt5DAD', 'PovRateAt10DAD', 'PovRateAt30DAD']
df_final.loc[:, cols] = df_final[cols] * 100

df_final

df_final = standardize_entities(df_final,
                        'data/input/entities_country_standardized.csv',
                        'Country',
                        'Our World In Data Name',
                        'Entity',
                        'Entity')
df_final

# +
# Specify sheet id and sheet (tab) name for the metadata google sheet 

sheet_id = '1ntYtYF0NqIW2oXuXl_ZJHvuI7n-bik94BEIOvWHrJAI'
sheet_name = 'moatsos'

# Read in variable metadata as dataframe
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
df_variable_metadata = pd.read_csv(url)

# Keep only id vars (country and year) and vars with metadata

# Select country, year and only those variables with metadata specified
# in the metadata folder.

id_vars = ['Entity', 'Year']

var_list = df_variable_metadata['slug'].tolist()

var_list = id_vars + var_list 

df_dataset = df_final[df_final.columns.intersection(var_list)].copy()

# Replace var names with those defined in the variable metadata ('name')

# Make a dictionary of var code_names and names
keys_code_names = df_variable_metadata['slug'].tolist()
values_names = df_variable_metadata['name'].tolist()
    #pair keys and values with zip
varnames_dict = dict(zip(keys_code_names, values_names))

# Rename the columns using the dictionary
df_dataset = df_dataset.rename(columns=varnames_dict)

#Export the dataset
df_dataset.to_csv('data/output/moatsos_dataset.csv', index=False)
# -

df_long = pd.melt(df_final, id_vars=['Entity', 'Year'], value_vars=cols,
        var_name='povline', value_name='headcount_ratio')

fig = px.line(df_long, x="Year", y="headcount_ratio", 
              title=f"<b>Poverty - Headcount ratios from Moatsos (2021)</b><br>‘cost of basic needs’ approach and 1.90, 5, 10 and 30 USD poverty lines",
              color='Entity', facet_col="povline", facet_col_wrap=3, markers=False, height=600)
fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
fig.update_yaxes(matches=None)
fig.show()
fig.write_html(f'graphics/moatsos_povlines_1.html')

fig = px.line(df_long, x="Year", y="headcount_ratio", 
              title=f"<b>Poverty - Headcount ratios from Moatsos (2021)</b><br>‘cost of basic needs’ approach and 1.90, 5, 10 and 30 USD poverty lines",
              color='povline', facet_col="Entity", facet_col_wrap=3, markers=False, height=600)
fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
fig.update_yaxes(matches=None)
fig.show()
fig.write_html(f'graphics/moatsos_povlines_2.html')

df_long[['headcount_ratio']].describe()


