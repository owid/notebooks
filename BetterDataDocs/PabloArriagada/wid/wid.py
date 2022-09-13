# # World Inequality Database indicators
# The [World Inequality Database (WID.world)](https://wid.world/wid-world/) aims to provide open and convenient access to the most extensive available database on the historical evolution of the world distribution of income and wealth, both within countries and between countries. The dataset addresses some of the main limitations household surveys produce in national statistics of this kind: under-coverage at the top of the distribution due to non-response (the richest tend to not answer this kind of surveys or omit their income) or measurement error (the richest underreport their income for convenience or not actually knowing an exact figure if all their activities are added). The problem is handled with the combination of fiscal and national accounts data along household surveys based on the work of the leading researchers in the area: Anthony B. Atkinson, Thomas Piketty, Emmanuel Saez, Facundo Alvaredo, Gabriel Zucman, and hundreds of others. The initiative is based in the Paris School of Economics (as the [World Inequality Lab](https://inequalitylab.world/)) and compiles the World Inequality Report, a yearly publication about how inequality has evolved until the last year.
#
# Besides income and wealth distribution data, the WID has recently added carbon emissions to generate carbon inequality indices. It also offers decomposed stats on national income. The data can be obtained from the website and by R and Stata commands.

# Three income distributions are considered:
# - **Pretax income distribution** `ptinc`, which includes social insurance benefits (and remove corresponding contributions), but exclude other forms of redistribution (income tax, social assistance benefits, etc.).
# - **Post-tax national income distribution** `diinc`, which includes both in-kind and in-cash redistribution.
# - **Post-tax disposable income distribution** `cainc`, which excludes in-kind transfers (because the distribution of in-kind transfers requires a lot of assumptions).
#
# These distributions are the main DINA (distributional national accounts) income variables available at WID. DINA income concepts are distributed income concepts that are consistent with national accounts aggregates. The precise definitions are outlined in the [DINA guidelines](https://wid.world/es/news-article/2020-distributional-national-accounts-guidelines-dina-4/) and country-specific papers. 
#
# All of these distributions are generated using equal-split adults (j) as the population unit, meaning that the unit is the individual, but that income or wealth is distributed equally among all household members. The age group is individuals over age 20 (992, adult population), which excludes children (with 0 income in most of the cases). Extrapolations and interpolations are excluded from these files, as WID discourages its use at the level of individual countries (see the `exclude` description at `help wid` in Stata). More information about the variables and definitions can be found on [WID's codes dictionary](https://wid.world/codes-dictionary/).
#
# The variables processed in this notebook come from commands given in the `wid` function in Stata. These commands are located in the `wid_indices.do` file from this same folder. Opening the file and pressing the *Execute (do)* button will generate the most recent data from WID. Both `.csv` and `.dta` files are available for analysis.

import pandas as pd
from functions.standardize_entities import *

# +
#Load the complete Stata output
#keep_default_na and na_values are included because there is a country labeled NA, Namibia, which becomes null without the parameters
df_final = pd.read_csv('data/raw/wid_indices_992j.csv',
                       keep_default_na=False,
                       na_values=['-1.#IND', '1.#QNAN', '1.#IND', '-1.#QNAN', '#N/A N/A', '#N/A', 'N/A', 'n/a', '', '#NA', 
                                    'NULL', 'null', 'NaN', '-NaN', 'nan', '-nan', ''])

#Standardize entities and year
df_final = standardize_entities(df_final,
                        'data/raw/countries_country_standardized.csv',
                        'country',
                        'Our World In Data Name',
                        'country',
                        'Entity')
df_final = df_final.rename(columns={'year': 'Year'})

#Multiply share numbers by 100
share_cols = df_final.filter(like="share", axis=1).columns
df_final.loc[:, share_cols] = df_final[share_cols] * 100
# -

df_final

# +
# Specify sheet id and sheet (tab) name for the metadata google sheet 

sheet_id = '1ntYtYF0NqIW2oXuXl_ZJHvuI7n-bik94BEIOvWHrJAI'
sheet_name = 'wid_pretax'

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
df_dataset.to_csv('data/final/wid_dataset.csv', index=False)
