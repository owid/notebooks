# %% [markdown]
# # PIP issues
# This document is to find issues in the data extracted with World Bank's PIP query

# %% [markdown]
# ## Imports and functions from *functions* folder

# %%
import pandas as pd
import numpy as np
import time
import plotly.express as px
import plotly.io as pio
import requests
import io
pio.renderers.default='jupyterlab+png+colab+notebook_connected+vscode'


# %%
def pip_query_country(popshare_or_povline, value, country_code="all", year="all", fill_gaps="true", welfare_type="all", reporting_level="all"):

    # Build query
    request_url = f'https://api.worldbank.org/pip/v1/pip?{popshare_or_povline}={value}&country={country_code}&year={year}&fill_gaps={fill_gaps}&welfare_type={welfare_type}&reporting_level={reporting_level}&format=csv'

    #df = pd.read_csv(request_url)
    response = requests.get(request_url, timeout=50).content
    df = pd.read_csv(io.StringIO(response.decode('utf-8')))

    return df


# %%
# For world regions, the popshare query is not available (or rather, it returns nonsense).
def pip_query_region(povline, year="all"):

    # Build query
    request_url = f'https://api.worldbank.org/pip/v1/pip-grp?povline={povline}&year={year}&group_by=wb&format=csv'

    #df = pd.read_csv(request_url)
    response = requests.get(request_url, timeout=50).content
    df = pd.read_csv(io.StringIO(response.decode('utf-8')))

    return df


# %%
def standardize_entities(orig_df,
                        entity_mapping_url,
                        mapping_varname_raw,
                        mapping_vaname_owid,
                        data_varname_old,
                        data_varname_new):


    # Read in mapping table which maps PWT names onto OWID names.
    df_mapping = pd.read_csv(entity_mapping_url)

    # Merge in mapping to raw
    df_harmonized = pd.merge(orig_df,df_mapping,
      left_on=data_varname_old,right_on=mapping_varname_raw, how='left')
    
    # Drop the old entity names column, and the matching column from the mapping file
    df_harmonized = df_harmonized.drop(columns=[data_varname_old, mapping_varname_raw])
    
    # Rename the new entity column
    df_harmonized = df_harmonized.rename(columns={mapping_vaname_owid:data_varname_new})

    # Move the entity column to front:

    # get a list of columns
    cols = list(df_harmonized)
    
    # move the country column to the first in the list of columns
    cols.insert(0, cols.pop(cols.index(data_varname_new)))
    
    # reorder the columns of the dataframe according to the list
    df_harmonized = df_harmonized.loc[:, cols]

    return df_harmonized

# %% [markdown]
# ## Generating the data

# %% [markdown]
# The code to extract the data is replicated here:

# %%
#Create a dataframe for each poverty line on the list, including and excluding interpolations and for countries and regions
#Each of these combinations are concatenated in a larger data frame.

start_time = time.time()

# Here we define the poverty lines to query as cents
poverty_lines_cents = [100, 190, 320, 550, 1000, 2000, 3000, 4000]

df_complete = pd.DataFrame()

# Run the API query and clean the response...
#... for each poverty line
for p in poverty_lines_cents:

    p_dollar = p/100

    #.. and for both countries and WB regional aggregates
    for ent_type in ['country', 'region']:

        # Make the API query for country data
        if ent_type == 'country':

            df = pip_query_country(
                popshare_or_povline = "povline", 
                value = p_dollar, 
                fill_gaps="false")

            df = df.rename(columns={'country_name': 'entity'})
            
            # Keep only these variables:
            keep_vars = [ 
                'entity',
                'reporting_year',
                'reporting_level',
                'welfare_type', 
                'headcount',
                'poverty_gap',
                'reporting_pop',
                'survey_year',
                'survey_comparability', 
                'comparable_spell', 
                'poverty_severity', 
                'watts', 
                'mean', 
                'median', 
                'mld',
                'gini', 
                'polarization', 
                'decile1', 'decile2', 'decile3', 'decile4','decile5', 'decile6', 'decile7', 'decile8', 'decile9', 'decile10',
                'cpi', 'ppp', 'reporting_gdp', 'reporting_pce', 
                'distribution_type', 'estimation_type'
            ]

        # Make the API query for region data
        # Note that the filled and not filled data is the same in this case .
        # The code runs it twice anyhow.
        if ent_type == 'region':

            df = pip_query_region(p_dollar)

            df = df.rename(columns={'region_name': 'entity'})

            keep_vars = [ 
                'entity',
                'reporting_year',
                'headcount',
                'poverty_gap',
                'reporting_pop',
                'poverty_severity',
                'watts',
                'mean'
            ]


        df = df[keep_vars]

        # rename columns
        df = df.rename(columns={
        'headcount':'headcount_ratio',
        'poverty_gap': 'poverty_gap_index'})

        # Calculate number in poverty
        df['headcount'] = df['headcount_ratio'] * df['reporting_pop']
        df['headcount'] = df['headcount'].round(0)

        # Calculate shortfall of incomes
        df['total_shortfall'] = df['poverty_gap_index'] * p_dollar * df['reporting_pop']                      

        # Calculate average shortfall of incomes (averaged across population in poverty)
        df['avg_shortfall'] = df['total_shortfall'] / df['headcount']

        # Calculate income gap ratio (according to Ravallion's definition)
        df['income_gap_ratio'] = (df['total_shortfall'] / df['headcount']) / p_dollar


        # Shares to percentages
        # executing the function over list of vars
        var_list = ['headcount_ratio', 'income_gap_ratio', 'poverty_gap_index' ]

        #df[var_list] = df[var_list].apply(multiply_by_100)
        df.loc[:, var_list] = df[var_list] * 100


        # Add poverty line as a var (I add the '_' character, because it being treated as a float later on was causing headaches)
        df['poverty line'] = f'_{p}'
        #df['filled'] = is_filled
        df['ent_type'] = ent_type

        #Concatenate all the results
        df_complete = pd.concat([df_complete, df],ignore_index=True)

end_time = time.time()
elapsed_time = end_time - start_time
print('Execution time:', elapsed_time, 'seconds')

# %%
# Create different combinations of dataframe from df_complete

# Select data for countries
headcounts_country = df_complete[(df_complete['ent_type'] == 'country')].reset_index(drop=True)

# Select data for regions
headcounts_region = df_complete[(df_complete['ent_type'] == 'region')].reset_index(drop=True)

#Create pivot tables to make the data wide
headcounts_country_wide = headcounts_country.pivot_table(index=['entity', 'reporting_year','reporting_level','welfare_type',
                                                               'comparable_spell', 'distribution_type', 'estimation_type'],
                                                         columns='poverty line')

headcounts_region_wide = headcounts_region.pivot_table(index=['entity', 'reporting_year'],
                                                       columns='poverty line')

#Join multi index columns
headcounts_country_wide.columns = [''.join(col).strip() for col in headcounts_country_wide.columns.values]
headcounts_country_wide = headcounts_country_wide.reset_index()

headcounts_region_wide.columns = [''.join(col).strip() for col in headcounts_region_wide.columns.values]
headcounts_region_wide = headcounts_region_wide.reset_index()

#Concatenate country and regional wide datasets
df_final = pd.concat([headcounts_country_wide, headcounts_region_wide], ignore_index=False)

#Keep only one variable (multiple columns with the same values were generated for each poverty line)
for i in range(len(poverty_lines_cents)):
    if i == 0:
        df_final.rename(columns={f'reporting_pop_{poverty_lines_cents[i]}': 'reporting_pop',
                                 f'survey_year_{poverty_lines_cents[i]}': 'survey_year',
                                 f'survey_comparability_{poverty_lines_cents[i]}': 'survey_comparability',
                                 f'mean_{poverty_lines_cents[i]}': 'mean',
                                 f'median_{poverty_lines_cents[i]}': 'median',
                                 f'mld_{poverty_lines_cents[i]}': 'mld',
                                 f'gini_{poverty_lines_cents[i]}': 'gini',
                                 f'polarization_{poverty_lines_cents[i]}': 'polarization',
                                 f'cpi_{poverty_lines_cents[i]}': 'cpi',
                                 f'ppp_{poverty_lines_cents[i]}': 'ppp',
                                 f'reporting_gdp_{poverty_lines_cents[i]}': 'reporting_gdp',
                                 f'reporting_pce_{poverty_lines_cents[i]}': 'reporting_pce',
                                 f'decile1_{poverty_lines_cents[i]}': 'decile1',
                                 f'decile2_{poverty_lines_cents[i]}': 'decile2',
                                 f'decile3_{poverty_lines_cents[i]}': 'decile3',
                                 f'decile4_{poverty_lines_cents[i]}': 'decile4',
                                 f'decile5_{poverty_lines_cents[i]}': 'decile5',
                                 f'decile6_{poverty_lines_cents[i]}': 'decile6',
                                 f'decile7_{poverty_lines_cents[i]}': 'decile7',
                                 f'decile8_{poverty_lines_cents[i]}': 'decile8',
                                 f'decile9_{poverty_lines_cents[i]}': 'decile9',
                                 f'decile10_{poverty_lines_cents[i]}': 'decile10'
                                }, 
                        inplace=True)
    else:
        df_final.drop(columns=[f'reporting_pop_{poverty_lines_cents[i]}',
                               f'survey_year_{poverty_lines_cents[i]}',
                               f'survey_comparability_{poverty_lines_cents[i]}',
                               f'mean_{poverty_lines_cents[i]}',
                               f'median_{poverty_lines_cents[i]}',
                               f'mld_{poverty_lines_cents[i]}',
                               f'gini_{poverty_lines_cents[i]}',
                               f'polarization_{poverty_lines_cents[i]}',
                               f'cpi_{poverty_lines_cents[i]}',
                               f'ppp_{poverty_lines_cents[i]}',
                               f'reporting_gdp_{poverty_lines_cents[i]}',
                               f'reporting_pce_{poverty_lines_cents[i]}',
                               f'decile1_{poverty_lines_cents[i]}',
                               f'decile2_{poverty_lines_cents[i]}',
                               f'decile3_{poverty_lines_cents[i]}',
                               f'decile4_{poverty_lines_cents[i]}',
                               f'decile5_{poverty_lines_cents[i]}',
                               f'decile6_{poverty_lines_cents[i]}',
                               f'decile7_{poverty_lines_cents[i]}',
                               f'decile8_{poverty_lines_cents[i]}',
                               f'decile9_{poverty_lines_cents[i]}',
                               f'decile10_{poverty_lines_cents[i]}'
                              ],
                      inplace=True)

#Calculate numbers in poverty between pov lines for stacked area charts
#Make sure the poverty lines are in order, lowest to highest
poverty_lines_cents.sort()

col_stacked_n = []
col_stacked_pct = []

#For each poverty line in poverty_lines_cents
for i in range(len(poverty_lines_cents)):
    #if it's the first value only get people below this poverty line (and percentage)
    if i == 0:
        varname_n = f'number_below_{poverty_lines_cents[i]}'
        df_final[varname_n] = df_final[f'headcount_{poverty_lines_cents[i]}']
        col_stacked_n.append(varname_n)

        varname_pct = f'percentage_below_{poverty_lines_cents[i]}'
        df_final[varname_pct] = df_final[varname_n] / df_final['reporting_pop']
        col_stacked_pct.append(varname_pct)

    #If it's the last value calculate the people between this value and the previous 
    #and also the people over this poverty line (and percentages)
    elif i == len(poverty_lines_cents)-1:

        varname_n = f'number_between_{poverty_lines_cents[i-1]}_{poverty_lines_cents[i]}'
        df_final[varname_n] = df_final[f'headcount_{poverty_lines_cents[i]}'] - df_final[f'headcount_{poverty_lines_cents[i-1]}']
        col_stacked_n.append(varname_n)

        varname_pct = f'percentage_between_{poverty_lines_cents[i-1]}_{poverty_lines_cents[i]}'
        df_final[varname_pct] = df_final[varname_n] / df_final['reporting_pop']
        col_stacked_pct.append(varname_pct)

        varname_n = f'number_over_{poverty_lines_cents[i]}'
        df_final[varname_n] = df_final['reporting_pop'] - df_final[f'headcount_{poverty_lines_cents[i]}']
        col_stacked_n.append(varname_n)

        varname_pct = f'percentage_over_{poverty_lines_cents[i]}'
        df_final[varname_pct] = df_final[varname_n] / df_final['reporting_pop']
        col_stacked_pct.append(varname_pct)

    #If it's any value between the first and the last calculate the people between this value and the previous (and percentage)
    else:
        varname_n = f'number_between_{poverty_lines_cents[i-1]}_{poverty_lines_cents[i]}'
        df_final[varname_n] = df_final[f'headcount_{poverty_lines_cents[i]}'] - df_final[f'headcount_{poverty_lines_cents[i-1]}']
        col_stacked_n.append(varname_n)

        varname_pct = f'percentage_between_{poverty_lines_cents[i-1]}_{poverty_lines_cents[i]}'
        df_final[varname_pct] = df_final[varname_n] / df_final['reporting_pop']
        col_stacked_pct.append(varname_pct)
        
# Standardize entity names
df_final = standardize_entities(
    orig_df = df_final,
    entity_mapping_url = "https://joeh.fra1.digitaloceanspaces.com/PIP/country_mapping.csv",
    mapping_varname_raw ='Original Name',
    mapping_vaname_owid = 'Our World In Data Name',
    data_varname_old = 'entity',
    data_varname_new = 'entity'
)

# Amend the entity to reflect if data refers to urban or rural only
df_final.loc[(\
    df_final['reporting_level'].isin(["urban", "rural"])),'entity'] = \
    df_final.loc[(\
    df_final['reporting_level'].isin(["urban", "rural"])),'entity'] + \
        ' - ' + \
    df_final.loc[(\
    df_final['reporting_level'].isin(["urban", "rural"])),'reporting_level']

# Tidying – Rename cols
df_final = df_final.rename(columns={'reporting_year': 'year'})

#Order columns by categorising them
col_ids = ['entity', 'year', 'reporting_level', 'welfare_type', 'reporting_pop']
col_avg_shortfall = []
col_headcount = []
col_headcount_ratio = []
col_incomegap = []
col_povertygap = []
col_tot_shortfall = []
col_poverty_severity = []
col_watts = []
col_central = ['mean', 'median']
col_deciles = ['decile1', 'decile2', 'decile3', 'decile4','decile5', 'decile6', 'decile7', 'decile8', 'decile9', 'decile10']
col_inequality = ['mld', 'gini', 'polarization']
col_extra = ['survey_year', 'survey_comparability', 'comparable_spell', 'distribution_type', 'estimation_type',
            'cpi', 'ppp', 'reporting_gdp', 'reporting_pce']

for i in range(len(poverty_lines_cents)):
    col_avg_shortfall.append(f'avg_shortfall_{poverty_lines_cents[i]}')
    col_headcount.append(f'headcount_{poverty_lines_cents[i]}')
    col_headcount_ratio.append(f'headcount_ratio_{poverty_lines_cents[i]}')
    col_incomegap.append(f'income_gap_ratio_{poverty_lines_cents[i]}')
    col_povertygap.append(f'poverty_gap_index_{poverty_lines_cents[i]}')
    col_tot_shortfall.append(f'total_shortfall_{poverty_lines_cents[i]}')
    col_poverty_severity.append(f'poverty_severity_{poverty_lines_cents[i]}')
    col_watts.append(f'watts_{poverty_lines_cents[i]}')

#Concatenate the entire list (including the previously estimated col_stacked_n and col_stacked_pct) and reorder
cols = col_ids + col_central + col_headcount + col_headcount_ratio + col_povertygap + col_tot_shortfall + col_avg_shortfall + col_incomegap + col_stacked_n + col_stacked_pct + col_poverty_severity + col_watts + col_deciles + col_inequality + col_extra
df_final = df_final[cols]

# %% [markdown]
# ## Missing values
# In this section I look for observations which are missing or with a zero value for the poverty variables. First, I check the null observations:

# %%
cols_to_check = ['reporting_pop'] + col_central + col_headcount + col_headcount_ratio + col_povertygap + col_tot_shortfall + col_avg_shortfall + col_incomegap + col_stacked_n + col_stacked_pct + col_poverty_severity + col_watts + col_deciles + col_inequality

df_null = df_final[df_final[cols_to_check].isna().any(1)].copy().reset_index(drop=True)
df_null

# %% [markdown]
# 701 rows have at least one null value. But the distribution of them by variable is not uniform:

# %%
# Count number of nulls in all columns of Dataframe
for column_name in cols_to_check:
    column = df_null[column_name]
    # Get the count of nulls in column 
    count = (column.isnull()).sum()
    print(f'Count of nulls in column {column_name} is : {count}')

# %% [markdown]
# ### Selected poverty variables

# %% [markdown]
# The average shortfall and income gap ratio have much more null values compared to the rest of poverty variables. If I exclude them from the analysis (besides poverty severity and the Watts index) I only have one observation with nulls: **Guinea-Bissau** in 1991:

# %%
cols_to_check = col_headcount + col_headcount_ratio + col_povertygap + col_tot_shortfall + col_stacked_n + col_stacked_pct

df_null_selected = df_final[df_final[cols_to_check].isna().any(1)].copy().reset_index(drop=True)
df_null_selected[['entity', 'year', 'reporting_level', 'welfare_type'] + cols_to_check]

# %% [markdown]
# ### Poverty severity and Watts index

# %% [markdown]
# Isolating the poverty severity and the Watts index they have 8 null observations, including **Guinea-Bissau 1991**. The others are in **China (2012, 2014, 2015, 2018 and 2019), El Salvador 1989 and Sierra Leone 1989**. 

# %%
cols_to_check = col_poverty_severity + col_watts

df_null_selected = df_final[df_final[cols_to_check].isna().any(1)].copy().reset_index(drop=True)
df_null_selected[['entity', 'year', 'reporting_level', 'welfare_type'] + cols_to_check]

# %% [markdown]
# ### Average shortfall and income gap ratio

# %% [markdown]
# 76 different countries show null values for average shortfall and income gap ratio variables.

# %%
cols_to_check = col_avg_shortfall + col_incomegap

df_null_selected = df_final[df_final[cols_to_check].isna().any(1)].copy().reset_index(drop=True)
df_null_selected['entity'].value_counts()

# %% [markdown]
# ### Mean, median, decile shares and inequality measures

# %% [markdown]
# If mean, median, deciles and inequality statistics are grouped together we have a larger group of nulls:

# %%
cols_to_check = col_central + col_deciles + col_inequality

df_null_selected = df_final[df_final[cols_to_check].isna().any(1)].copy().reset_index(drop=True)
df_null_selected[['entity', 'year', 'reporting_level', 'welfare_type'] + cols_to_check]

# %% [markdown]
# Though a considerable part of the nulls are concentrated on the regional data, so I filter out them:

# %%
#Defining the different aggregations
world_list = ['World']

regions_list = ['East Asia and Pacific', 
           'Europe and Central Asia',
           'Latin America and the Caribbean', 
           'Middle East and North Africa', 
           'South Asia', 
           'Sub-Saharan Africa']

high_income_list = ['High income countries']

redundant_countries = ['China - urban', 
                       'China - rural', 
                       'India - urban', 
                       'India - rural', 
                       'Indonesia - urban',
                       'Indonesia - rural']

countries_list = list(set(list(df_final['entity'].unique())) - set(regions_list) - set(world_list) - set(high_income_list) - set(redundant_countries))

# %% [markdown]
# Now they are 65 different observations with null values for these variables

# %%
df_null_selected_noregions = df_null_selected[~df_null_selected['entity'].isin(world_list + regions_list + high_income_list)]
df_null_selected_regions = df_null_selected[df_null_selected['entity'].isin(world_list + regions_list + high_income_list)]
df_null_selected_noregions[['entity', 'year', 'reporting_level', 'welfare_type'] + cols_to_check]

# %% [markdown]
# The nulls for mean, median, deciles and inequality statistics are concentrated mostly in Indonesia, China and India:

# %%
df_null_selected_noregions['entity'].value_counts()

# %% [markdown]
# This is actually all the observations for these three countries.

# %%
df_excluding_null = df_final[~df_final[cols_to_check].isna().any(1)].copy().reset_index(drop=True)
df_excluding_null = df_excluding_null[df_excluding_null['entity'].isin(['Indonesia', 'China', 'India'])]
df_excluding_null[['entity', 'year', 'reporting_level', 'welfare_type'] + cols_to_check]

# %% [markdown]
# And for these three countries only the median is missing.

# %%
# Count number of nulls in all columns of Dataframe
df_null_chn_ind_idn = df_null_selected_noregions[df_null_selected_noregions['entity'].isin(['Indonesia', 'China', 'India'])].copy().reset_index(drop=True)

for column_name in cols_to_check:
    column = df_null_chn_ind_idn[column_name]
    # Get the count of nulls in column 
    count = (column.isnull()).sum()
    print(f'Count of nulls in column {column_name} is : {count}')

# %% [markdown]
# It is interesting that there are less null values for the share of decile 5 (9) than for the median (62), because one should be obtained from the other. 56/62 missing median values are concentrated in China, India and Indonesia:

# %%
# Count number of nulls in all columns of Dataframe
for column_name in cols_to_check:
    column = df_null_selected_noregions[column_name]
    # Get the count of nulls in column 
    count = (column.isnull()).sum()
    print(f'Count of nulls in column {column_name} is : {count}')

# %% [markdown]
# For regions only mean values are included:

# %%
# Count number of nulls in all columns of Dataframe
for column_name in cols_to_check:
    column = df_null_selected_regions[column_name]
    # Get the count of nulls in column 
    count = (column.isnull()).sum()
    print(f'Count of nulls in column {column_name} is : {count}')

# %% [markdown]
# ### Median

# %% [markdown]
# Missing median data can actually be obtained by using the `popshare` command instead of `povline`. While `povline` returns the headcount (and other poverty/inequality values) when a poverty line is given, `popshare` returns the poverty line when a population share (headcount) is given. This way, the poverty line the latter command returns when the popshare value is 0.5 is the median income/consumption value. See for example China

# %%
df_popshare = pip_query_country(
                    popshare_or_povline = "popshare",
                    country_code = "CHN",
                    value = 0.5,
                    reporting_level = "national",
                    fill_gaps="false")

# %% [markdown]
# The poverty_line column corresponds to the missing median. We can see that for the cases where the median is not null, i.e. the urban and rural data.

# %%
df_popshare[['country_name','reporting_year', 'reporting_level', 'welfare_type', 'poverty_line', 'headcount',
             'mean', 'median', 'mld','gini', 'polarization']].head(10)

# %% [markdown]
# This is not possible though for regions. Even if there is a `popshare` option available, the query returns poverty lines equal to 1.9.

# %%
popshare = 0.5
year = "all"
request_url = f'https://api.worldbank.org/pip/v1/pip-grp?popshare={popshare}&year={year}&group_by=wb&format=csv'
df_popshare_regions = pd.read_csv(request_url)

# %%
df_popshare_regions

# %% [markdown]
# The median income values besides of their own value allow to estimate relative poverty measures. So it is essential to have median for each entity as possible.

# %% [markdown]
# ### Inequality indices
# Six observations have their mean log deviation, gini and polarization measures missing: El Salvador 89, Guatemala 98, Guinea-Bissau 91, Guyana 92, Namibia 93 and Sierra Leone 89.

# %%
cols_to_check = col_inequality

df_null_selected = df_final[df_final[cols_to_check].isna().any(1)].copy().reset_index(drop=True)
df_null_selected[['entity', 'year', 'reporting_level', 'welfare_type'] + cols_to_check]
df_null_selected_noregions = df_null_selected[~df_null_selected['entity'].isin(world_list + regions_list + high_income_list)]
df_null_selected_regions = df_null_selected[df_null_selected['entity'].isin(world_list + regions_list + high_income_list)]
df_null_selected_noregions[['entity', 'year', 'reporting_level', 'welfare_type'] + cols_to_check]

# %% [markdown]
# ## Zero values
# What about zero values? 613 observations include at least one value equal to zero.

# %%
cols_to_check = ['reporting_pop'] + col_central + col_headcount + col_headcount_ratio + col_povertygap + col_tot_shortfall + col_avg_shortfall + col_incomegap + col_stacked_n + col_stacked_pct + col_poverty_severity + col_watts + col_deciles + col_inequality
df_zero = df_final[(df_final[cols_to_check] == 0).any(1)].reset_index(drop=True)
df_zero

# %% [markdown]
# The distribution of zeros is certainly more uniform compared to the nulls:

# %%
# Count number of zeros in all columns of Dataframe
for column_name in cols_to_check:
    column = df_zero[column_name]
    # Get the count of zeros in column 
    count = (column == 0).sum()
    print(f'Count of zeros in column {column_name} is : {count}')

# %% [markdown]
# This is for a reason. See for example this table: the higher number of nulls for the average shortfall and income gap ratio variables is directly associated with the number of zero values for the headcount variable, as this is generated by dividing by the headcount. The higher number of nulls is explained by the sum of headcount zeros and nulls.
#
# | Poverty line | Zero values<br>Headcount | Null values<br>Average shortfall<br>Income gap ratio | Difference | Null values<br>Headcount |
# | --- | --- | --- | --- | --- |
# | 1.0 | 358 | 358 | 0 | 0 |
# | 1.9 | 154 | 154 | 0 | 0 |
# | 3.2 | 54 | 54 | 0 | 0 |
# | 5.5 | 8 | 9 | 1 | 1 |
# | 10 | 3 | 4 | 1 | 1 |
# | 20 | 0 | 1 | 1 | 1 |
# | 30 | 0 | 1 | 1 | 1 |
# | 40 | 0 | 1 | 1 | 1 |

# %% [markdown]
# 76 different countries have 0 values for headcount:

# %%
cols_to_check = col_headcount

df_zero_selected = df_final[(df_final[cols_to_check] == 0).any(1)].reset_index(drop=True)
df_zero_selected['entity'].value_counts()

# %% [markdown]
# There are more zero values for the Watts index than for the other poverty variables

# %%
cols_to_check = col_poverty_severity + col_watts

df_zero_selected = df_final[(df_final[cols_to_check] == 0).any(1)].copy().reset_index(drop=True)
df_zero_selected[['entity', 'year', 'reporting_level', 'welfare_type'] + cols_to_check]

# %% [markdown]
# 77 different countries have zero values for the Watts index (and the poverty severity as well)

# %%
df_zero_selected['entity'].value_counts()

# %% [markdown]
# If mean, median, deciles and inequality statistics are grouped together we only find one zero value, and it is for `decile1` in the case of <b>Suriname - urban</b>

# %%
cols_to_check = col_central + col_deciles + col_inequality

df_zero_selected = df_final[(df_final[cols_to_check] == 0).any(1)].copy().reset_index(drop=True)
df_zero_selected[['entity', 'year', 'reporting_level', 'welfare_type'] + cols_to_check]

# %% [markdown]
# ## Percentage on different poverty lines do not add up to 100%
# For each country-year the total number of people below, between and over multiple poverty lines are estimated to create a stacked chart with the distribution of income/consumption of the population. It is important then that these numbers add together to the total population (the aggregated percentage is 100%)

# %% [markdown]
# One country show issues and it is again **Guinea-Bissau** in 1991: the total for this year is less than 1 (0.64). In the table we can see why: there are no estimation of poor people living below \\$5.5 or any higher poverty line.

# %%
df_final['sum_pct'] = df_final[col_stacked_pct].sum(axis=1)
df_not_1 = df_final[(df_final['sum_pct'] >= 1.00000001) | (df_final['sum_pct'] <= 0.99999999)].copy().reset_index(drop=True)
df_not_1

# %% [markdown]
# ## Percentage for decile shares do not add up to 100%
# Similarly, in the case of decile shares, in every row the sum of `decile1` to `decile10` should be 1

# %% [markdown]
# 9 different countries-years fail in this requirement: **El Salvador 1989, Guatemala 1998, Guinea-Bissau 1991 (again), Guyana 1992, Namibia 1993, Sierra Leone 1989, Somalia 2017, South Sudan 2016 and Zimbabwe 2019**. And this is because every `decile` variable for these observations is null.

# %%
df_final['sum_deciles'] = df_final[col_deciles].sum(axis=1)
df_not_1 = df_final[((df_final['sum_deciles'] >= 1.00000001) | (df_final['sum_deciles'] <= 0.99999999))].copy().reset_index(drop=True)
df_not_1 = df_not_1[~df_not_1['entity'].isin(regions_list + world_list + high_income_list)].reset_index(drop=True)
df_not_1[['entity', 'year', 'reporting_level', 'welfare_type'] + cols_to_check + ['sum_deciles']]

# %%
df_final['sum_deciles'] = df_final[col_deciles].sum(axis=1)
df_not_1 = df_final[((df_final['sum_deciles'] >= 1.001) | (df_final['sum_deciles'] <= 0.999))].copy().reset_index(drop=True)
df_not_1 = df_not_1[~df_not_1['entity'].isin(regions_list + world_list + high_income_list)].reset_index(drop=True)
df_not_1[['entity', 'year', 'reporting_level', 'welfare_type'] + cols_to_check + ['sum_deciles']]

# %% [markdown]
# ## Monotonicity checks
# ###  Headcount poverty
#
# As poverty lines increase, the number of people below these poverty lines should increase as well. Let's see if that's the case

# %%
m_check_vars = []
for i in range(len(col_headcount)):
    if i > 0:
        check_varname = f'm_check_{i}'
        df_final[check_varname] = df_final[f'{col_headcount[i]}'] >= df_final[f'{col_headcount[i-1]}']
        m_check_vars.append(check_varname)


# %% [markdown]
# **Croatia, Guinea-Bissau and United Arab Emirates** show issues. This is because for Croatia there are not headcount values for the \\$5.5 poverty line for years between 1981 and 1988. Guinea Bissau 1991 is the same considered for the stacked variables in the previous section and the UAE situation is the strangest of the group: the headcount below the \\$10 poverty line is one order of magnitude greater than the headcount below \\$20

# %%
df_final['check_total'] = df_final[m_check_vars].all(1)
df_check = df_final[df_final['check_total'] == False]
df_check[['entity', 'year', 'reporting_level', 'welfare_type'] + col_headcount]

# %%
print('Percentage of errors for each variable')
(len(df_check) - df_check[m_check_vars].sum(0))/len(df_check)*100

# %% [markdown]
# What if the condition is more strict? If filter the values not strictly increasing I have more rows: 

# %%
m_check_vars = []
for i in range(len(col_headcount)):
    if i > 0:
        check_varname = f'm_check_{i}'
        df_final[check_varname] = (df_final[f'{col_headcount[i]}'] > df_final[f'{col_headcount[i-1]}'])
        m_check_vars.append(check_varname)


# %% [markdown]
# 382 observations have at least one headcount value equal to the previous one.

# %%
df_final['check_total'] = df_final[m_check_vars].all(1)
df_check = df_final[df_final['check_total'] == False]
df_check[['entity', 'year', 'reporting_level', 'welfare_type'] + col_headcount]

# %% [markdown]
# If the zero values for the second headcount are filtered out, we exclude the richest countries with multiple zero headcounts. If I also exclude the second to last headcount ratio values greater than 99, the repeated valued at the top 1% are gone. There are 153 observations left

# %%
df_check = df_check[(df_check[col_headcount[1]] != 0) & (df_check[col_headcount_ratio[-2]] <= 99)]
df_check[['entity', 'year', 'reporting_level', 'welfare_type'] + col_headcount]

# %%
df_check.to_csv('repeated_headcounts.csv')

# %% [markdown]
# All of these issues are concentrated for the first three comparisons (the first four headcounts)

# %%
print('Percentage of errors for each variable')
(len(df_check) - df_check[m_check_vars].sum(0))/len(df_check)*100

# %% [markdown]
# And this is the list of countries showing the issue (mostly advanced economies, probably very few observations at the bottom of the distribution):

# %%
df_check['entity'].value_counts()

# %% [markdown]
# Further evidence to think about few observations at the bottom is that the fourth headcount ratio for this group of countries ($5.5 poverty line) has a median of 0.73\% and a maximum of 6.36%

# %%
fig = px.histogram(df_check, x=col_headcount_ratio[3], histnorm="percent", marginal="box")
fig.show()

# %% [markdown]
# ### Average shortfall
# With this variable there are much more monotonicity issues: 573 observations are affected (*though I am not sure monotonicity should exist*)

# %%
m_check_vars = []
for i in range(len(col_avg_shortfall)):
    if i > 0:
        check_varname = f'm_check_{i}'
        df_final[check_varname] = df_final[f'{col_avg_shortfall[i]}'] >= df_final[f'{col_avg_shortfall[i-1]}']
        m_check_vars.append(check_varname)


# %%
df_final['check_total'] = df_final[m_check_vars].all(1)
df_check = df_final[df_final['check_total'] == False]
df_check[['entity', 'year', 'reporting_level', 'welfare_type'] + col_avg_shortfall]

# %% [markdown]
# Excluding null values for the lowest poverty line there are 215 rows with the issue

# %%
df_check = df_check[~df_check[col_avg_shortfall[0]].isnull()]
df_check[['entity', 'year', 'reporting_level', 'welfare_type'] + col_avg_shortfall]

# %%
print('Percentage of errors for each variable')
(len(df_check) - df_check[m_check_vars].sum(0))/len(df_check)*100

# %% [markdown]
# ### Income gap ratio
# With this variable there are even more monotonicity issues: 1670 observations are affected (*though I am not sure monotonicity should exist*)

# %%
m_check_vars = []
for i in range(len(col_incomegap)):
    if i > 0:
        check_varname = f'm_check_{i}'
        df_final[check_varname] = df_final[f'{col_incomegap[i]}'] >= df_final[f'{col_incomegap[i-1]}']
        m_check_vars.append(check_varname)


# %%
df_final['check_total'] = df_final[m_check_vars].all(1)
df_check = df_final[df_final['check_total'] == False]
df_check[['entity', 'year', 'reporting_level', 'welfare_type'] + col_incomegap]

# %% [markdown]
# Excluding null values for the lowest poverty line there are 1321 rows with the issue

# %%
df_check = df_check[~df_check[col_incomegap[0]].isnull()]
df_check[['entity', 'year', 'reporting_level', 'welfare_type'] + col_incomegap]

# %%
print('Percentage of errors for each variable')
(len(df_check) - df_check[m_check_vars].sum(0))/len(df_check)*100

# %% [markdown]
# ## Reporting and survey year comparison
# The dataset contains two different year variables. One is `reporting_year`, renamed `year` for OWID processing, which is an integer value, but there is also a `survey_year` which represents when the income/consumption survey is ran in more than one year: the value has decimals representing the weight of the years. 
#
# >The decimal year notation is used when data are collected over **two calendar years**. The number before the decimal
# point refers to the first year of data collection, while the numbers after the decimal point show the proportion of data
# collected in the second year. For example, the Fiji survey (2013.24) was conducted in 2013 and 2014, with 24% of
# the data collected in 2014. For these countries, we use a weighted average of the annual CPI series, where the weights
# are based on the data collection. In the case of Fiji, we use a CPI that is the weighted average of the 2013 and 2014
# CPIs, with weights of 76% and 24%, respectively.
#
# (Atamanov et al. 2018. “April 2018 PovcalNet update: What’s new.” Global Poverty Monitoring Technical Note 1. Washington, DC: World Bank. Footnote 2, available [here](https://documents1.worldbank.org/curated/en/173171524715215230/pdf/April-2018-Povcalnet-Update-What-s-New.pdf))
#
# We can compare these values by dividing them and see how different they are.
# The ratio between the reporting year and the survey year is almost always less or equal than 1, except for the case of Tanzania in 2018: the survey year is 2017.92. The ratio is also very close to 1, from 0.99954 to 1.00004.

# %%
df_final['year_ratio'] = df_final['year'] / df_final['survey_year']

fig = px.scatter(df_final, x="year", y="year_ratio", color="entity",
                 hover_data=['survey_year'], opacity=0.5,
                 title="<b>Reporting year vs Survey year</b><br>Ratio between both measures vs year",
                 log_y=False,
                 height=600)
fig.update_traces(marker=dict(size=10, line=dict(width=0, color='blue')))
fig.show()

# %% [markdown]
# The absolute difference between the values is always 1. The cases which they are more apart are when the survey year is 0.92 greater than the reporting year (Tanzania 91, Vietnam 97, Eswatini 2000)

# %%
df_final['year_diff'] = df_final['year'] - df_final['survey_year']

fig = px.scatter(df_final, x="year", y="year_diff", color="entity",
                 hover_data=['survey_year'], opacity=0.5,
                 title="<b>Reporting year vs Survey year</b><br>Difference between both measures vs year",
                 log_y=False,
                 height=600)
fig.update_traces(marker=dict(size=10, line=dict(width=0, color='blue')))
fig.show()

# %% [markdown]
# Most of the data though is the same. The ratio is 1 for about 89% of the data.

# %%
fig = px.histogram(df_final, x="year_ratio", nbins=50, histnorm="percent", marginal="box")
fig.show()

# %% [markdown]
# For OWID purposes, `reporting_year` is preferred, though `survey_year` is also available.

# %% [markdown]
# ## Aggregation of data
# This section shows how countries and regions aggregations are compared to the world aggregation.

# %%
#Defining the different aggregations
world = ['World']

regions = ['East Asia and Pacific', 
           'Europe and Central Asia',
           'Latin America and the Caribbean', 
           'Middle East and North Africa', 
           'South Asia', 
           'Sub-Saharan Africa']

high_income = ['High income countries']

redundant_countries = ['China - urban', 
                       'China - rural', 
                       'India - urban', 
                       'India - rural', 
                       'Indonesia - urban',
                       'Indonesia - rural']

countries = list(set(list(df_final['entity'].unique())) - set(regions) - set(world) - set(high_income) - set(redundant_countries))

# %% [markdown]
# On a first visual inspection we can hardly compare the countries data without inter/extrapolations with the world aggregation, because all the countries are never available for the same year. Regarding regional aggregations there is missing headcount data for South Asia between 1997 and 2001 and in Sub Saharan Africa before 1990, but it seems not to be affected for the world aggregation.

# %%
for i in col_headcount:
    fig = px.area(df_final[df_final['entity'].isin(countries)], x="year", y=i, color="entity",
                  title=f'Variable: <b>{i}, countries</b>', template='none', height=450)
    fig.show()
    fig = px.area(df_final[df_final['entity'].isin(regions)], x="year", y=i, color="entity",
                  title=f'Variable: <b>{i}, regions</b>', template='none', height=450)
    fig.show()
    fig = px.area(df_final[df_final['entity'].isin(world)], x="year", y=i, color="entity",
                  title=f'Variable: <b>{i}, world</b>', template='none', height=450)
    fig.show()

# %% [markdown]
# For a more direct comparison we calculate the ratio between the headcount aggregate for countries or regions and the World aggregate provided by the World Bank.

# %%
#Generate dataframes for each level of aggregation
df_countries = df_final[df_final['entity'].isin(countries)].copy().reset_index(drop=True)
df_regions = df_final[df_final['entity'].isin(regions)].copy().reset_index(drop=True)
df_world = df_final[df_final['entity'].isin(world)].copy().reset_index(drop=True)

# %% [markdown]
# We can see the countries aggregations for headcount in different poverty lines fluctuate a lot: between a 2 and 70% of the world aggregation. Similar situation happens with the total shortfall. These aggregations can't be compared.

# %%
df_countries_year = df_countries.groupby(['year']).sum().reset_index()
df_countries_year['entity'] = "World (countries)"
df_countries_year = df_countries_year[['entity', 'year'] + col_headcount]
df_countries_year = pd.melt(df_countries_year, id_vars=['year', 'entity'], value_vars=col_headcount,
                            var_name='headcount_name', value_name='headcount_value')

df_world_year = df_world[['entity', 'year'] + col_headcount]
df_world_year = pd.melt(df_world_year, id_vars=['year', 'entity'], value_vars=col_headcount,
                            var_name='headcount_name', value_name='headcount_value')

df_world_comparison = pd.merge(df_countries_year,df_world_year, on=['year','headcount_name'])
df_world_comparison['ratio'] = df_world_comparison['headcount_value_x'] / df_world_comparison['headcount_value_y']

fig = px.line(df_world_comparison, x="year", y="ratio", color="headcount_name", title='<b>Headcount</b>: Countries aggregations vs. World')
fig.show()

# %% [markdown]
# Regional aggregations are a similar story. The missing data for South Asia and Sub Saharan Africa makes the aggregations less reliable: ranging from 55-70% to almost 100% of the world aggregation. We recommend to not use the regional aggregations together without any transformation. Similar situation happens with the total shortfall.

# %%
df_regions_year = df_regions.groupby(['year']).sum().reset_index()
df_regions_year['entity'] = "World (regions)"
df_regions_year = df_regions_year[['entity', 'year'] + col_headcount]
df_regions_year = pd.melt(df_regions_year, id_vars=['year', 'entity'], value_vars=col_headcount,
                            var_name='headcount_name', value_name='headcount_value')

df_world_year = df_world[['entity', 'year'] + col_headcount]
df_world_year = pd.melt(df_world_year, id_vars=['year', 'entity'], value_vars=col_headcount,
                            var_name='headcount_name', value_name='headcount_value')

df_world_comparison = pd.merge(df_regions_year,df_world_year, on=['year','headcount_name'])
df_world_comparison['ratio'] = df_world_comparison['headcount_value_x'] / df_world_comparison['headcount_value_y']

fig = px.line(df_world_comparison, x="year", y="ratio", color="headcount_name", title='<b>Headcount</b>: Regional aggregation vs. World')
fig.show()

# %%
# For world regions, the popshare query is not available (or rather, it returns nonsense).


# %%
regions = pip_query_region(1.9)
regions.columns


# %%
def p90_10_ratio(select_country, select_year, p90, p10):
    #Check p90 headcount is extremely close to 90%
    print(f"In {select_country}, {select_year}:")

    print(f"We see from the 'popshare' query that P90 and P10 were {p90} and {p10}.")

    print(f"P90/P10 raio is: {p90/p10}")
    
    print("Let's double check these yield the right headcount ratios (i.e. 90% and 10%)")

    fill_gaps = 'true'

    df_p90 = pd.read_csv(f'https://api.worldbank.org/pip/v1/pip?country={select_country}&year={select_year}&povline={p90}&fill_gaps={fill_gaps}&welfare_type=all&reporting_level=all&format=csv')

    heacount_p90 = df_p90['headcount'].values[0]
    print(f"P90 headcount is: {heacount_p90}")

    #Check p10 headcount is extremely close to 10%
    df_p10 = pd.read_csv(f'https://api.worldbank.org/pip/v1/pip?country={select_country}&year={select_year}&povline={p10}&fill_gaps={fill_gaps}&welfare_type=all&reporting_level=all&format=csv')

    heacount_p10 = df_p10['headcount'].values[0]
    print(f"P10 headcount is: {heacount_p10}")

    

# %%
select_country = "BWA"
select_year = 1985

p90 = 8.299255
p10 = 0.731530

p90_10_ratio(select_country,select_year, p90, p10)

# %%
select_country = "BWA"
select_year = 2003

p90 = 19.033194
p10 = 1.021057

p90_10_ratio(select_country,select_year, p90, p10)

# %%
#Check p90 headcount is extremely close to 90%
fill_gaps = 'true'

df_p90 = pd.read_csv(f'https://api.worldbank.org/pip/v1/pip?country={select_country}&year={select_year}&povline={p90}&fill_gaps={fill_gaps}&welfare_type=all&reporting_level=all&format=csv')

p90 = df_p90['headcount'].values[0]






# %%
select_country = "BWA"
select_year = 2003

p90 = 19.868751

# %%
#Check p90 headcount is extremely close to 90%
fill_gaps = 'true'

df_p90 = pd.read_csv(f'https://api.worldbank.org/pip/v1/pip?country={select_country}&year={select_year}&povline={p90}&fill_gaps={fill_gaps}&welfare_type=all&reporting_level=all&format=csv')

p90 = df_p90['headcount'].values[0]





# %%
df_p90_filled = df_p90_filled[["country_name", "reporting_year"]]

# %%
fill_gaps = 'false' 
popshare = '0.90'
request_url = f'https://api.worldbank.org/pip/v1/pip?country=all&year=all&popshare={popshare}&fill_gaps={fill_gaps}&welfare_type=all&reporting_level=all&format=csv'

df_p90_survey = pd.read_csv(request_url)
df_p10_survey = pd.read_csv(request_url)


#Then compare – say for Botswansa – inequality changes over the interpolation. 

# %%
# Note: region aggregates return incorrect/broken headcount data when requesting popshare.


# %%
# Note: distributional data (median, Dini, deciles etc.) are missing for ~2000 rows,
#  without it being clear why or what the patten is. For instnce Angola in 2000 yes, but 2001 no. 
# Perhaps something to do with interpolation vs extrpolation


# %%
#Note on negative poverty lines returned by Sierra Leone and El Salvador.
# For instance, see El Salvador povshare=0.19 in 1981. Or Sierra Leone 
# poveshare =0.14 in 1990, using the following request

fill_gaps = 'true' 
popshare = '0.19'
request_url = f'https://api.worldbank.org/pip/v1/pip?country=all&year=all&popshare={popshare}&fill_gaps={fill_gaps}&welfare_type=all&reporting_level=all&format=csv'

df = pd.read_csv(request_url)

df[(df['country_name']=='El Salvador') & (df['request_year']==1981)]


# %%
# Monotonicity issues.

# In the filled percentile data (at percentile resolution) it's only Ghana and Guyana.

# In the survey percentile data:
#Ghana 1987 – headcount= .10
#Guyana 1992 – headcoutn - .20
# India 1977 national and rural – headcount - ~.18

# Odd issue with India 1977: the National distribution seems to be (exactly) equal to the Rural distribution.
df_survey %>% filter(country_name=="India", reporting_year ==1977, requested_p<20, requested_p>15) %>% arrange(reporting_level, headcount)


# Sierra Leone in general (filled data) – lots of negative values and lots of monotonicity issues.
