# # Historical poverty data from Michalis Moatsos

import pandas as pd
from functools import reduce
from functions.standardize_entities import standardize_entities
import plotly.express as px
import plotly.io as pio

# ## Import the data and merge

# +
#Get the data
global_oecd = pd.read_csv('data/input/GlobalOECD.csv')
global_5 = pd.read_csv('data/input/Global5.csv')
global_10 = pd.read_csv('data/input/Global10.csv')
global_30 = pd.read_csv('data/input/Global30.csv')

#Multiple merge
data_frames = [global_oecd, global_5, global_10, global_30]
df_final = reduce(lambda  left,right: pd.merge(left,right,on=['Region', 'Year'],
                                            how='outer'), data_frames)
df_final = df_final.rename(columns={'Region': 'Entity'})
#Keep data only up to 2018
df_final = df_final[df_final['Year']<=2018].reset_index(drop=True)

#Select columns and multiply by 100 (also keep a list of World Bank poverty method variables)
cols = ['PovRate', 'PovRate1.9', 'PovRateAt5DAD', 'PovRateAt10DAD', 'PovRateAt30DAD']
cols_wb = ['PovRate1.9', 'PovRateAt5DAD', 'PovRateAt10DAD', 'PovRateAt30DAD']
df_final.loc[:, cols] = df_final[cols] * 100
# -

# ## Create additional variables

# +
#Share of people above poverty lines
for c in cols:
    df_final[f'Above{c}'] = 100 - df_final[f'{c}']

#Share of people in between poverty lines (World Bank)
#For each poverty line in cols_wb
for i in range(len(cols_wb)):
    if i != 0:
        df_final[f'Between{cols_wb[i-1]}_{cols_wb[i]}'] = df_final[f'{cols_wb[i]}'] - df_final[f'{cols_wb[i-1]}']
# -

# ## Standardise entities

df_final = standardize_entities(df_final,
                        'data/input/entities_country_standardized.csv',
                        'Country',
                        'Our World In Data Name',
                        'Entity',
                        'Entity')

# ## Include metadata

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

# ## Plot the poverty lines

#Make the dataframe long to be able to plot it easily
df_long = pd.melt(df_final[['Entity', 'Year'] + cols], id_vars=['Entity', 'Year'], value_vars=cols,
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

# ## Sense checks

#Descriptive statistics for the shares in poverty
df_long[['headcount_ratio']].describe()

# +
#

# +
m_check_vars = []
cols_to_check = ['PovRate1.9', 'PovRateAt5DAD', 'PovRateAt10DAD', 'PovRateAt30DAD']
for i in range(len(cols_to_check)):
    if i > 0:
        check_varname = f'm_check_{i}'
        df_final[check_varname] = df_final[f'{cols_to_check[i]}'] >= df_final[f'{cols_to_check[i-1]}']
        m_check_vars.append(check_varname)
        
df_final['check_total'] = df_final[m_check_vars].all(1)
df_check = df_final[df_final['check_total'] == False]
df_check[['Entity', 'Year'] + cols_to_check]
