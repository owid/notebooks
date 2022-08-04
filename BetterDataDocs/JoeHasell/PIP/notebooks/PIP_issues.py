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
pio.renderers.default='jupyterlab+png+colab+notebook_connected+vscode'


# %%
def pip_query_country(popshare_or_povline, value, country_code="all", year="all", fill_gaps="true", welfare_type="all", reporting_level="all"):

    # Build query
    request_url = f'https://api.worldbank.org/pip/v1/pip?{popshare_or_povline}={value}&country={country_code}&year={year}&fill_gaps={fill_gaps}&welfare_type={welfare_type}&reporting_level={reporting_level}&format=csv'

    df = pd.read_csv(request_url)

    return df


# %%
# For world regions, the popshare query is not available (or rather, it returns nonsense).
def pip_query_region(povline, year="all"):

    # Build query
    request_url = f'https://api.worldbank.org/pip/v1/pip-grp?povline={povline}&year={year}&group_by=wb&format=csv'

    df = pd.read_csv(request_url)

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

    #... for both the interpolated ('filled') data and the survey-year only data
    for is_filled in ['true', 'false']:
    
        #.. and for both countries and WB regional aggregates
        for ent_type in ['country', 'region']:

            # Make the API query for country data
            if ent_type == 'country':
        
                df = pip_query_country(
                    popshare_or_povline = "povline", 
                    value = p_dollar, 
                    fill_gaps=is_filled)

                df = df.rename(columns={'country_name': 'entity'})
                
                # Keep only these variables:
                keep_vars = [ 
                    'entity',
                    'reporting_year',
                    'reporting_level',
                    'welfare_type', 
                    'headcount',
                    'poverty_gap',
                    'reporting_pop'
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
                    'reporting_pop'
                ]
        

            df = df[keep_vars]

            # rename columns
            df = df.rename(columns={
            'headcount':'headcount_ratio',
            'poverty_gap': 'poverty_gap_index'})

            # Calculate number in poverty
            df['headcount'] = df['headcount_ratio'] * df['reporting_pop']  

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
            df['filled'] = is_filled
            df['ent_type'] = ent_type

            #Concatenate all the results
            df_complete = pd.concat([df_complete, df],ignore_index=True)

end_time = time.time()
elapsed_time = end_time - start_time
print('Execution time:', elapsed_time, 'seconds')

# %%
# Create different combinations of dataframe from df_complete

# Select data for countries and filled or not
headcounts_country = df_complete[(df_complete['ent_type'] == 'country') & (df_complete['filled'] == 'true')].reset_index(drop=True)

# Select data for regions and filled or not
headcounts_region = df_complete[(df_complete['ent_type'] == 'region')  & (df_complete['filled'] == 'true')].reset_index(drop=True)

#Create pivot tables to make the data wide
headcounts_country_wide = headcounts_country.pivot_table(index=['entity', 'reporting_year','reporting_level','welfare_type'], 
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

#Keep only one reporting_pop variable (multiple columns with the same values were generated for each poverty line)
for i in range(len(poverty_lines_cents)):
    if i == 0:
        df_final.rename(columns={f'reporting_pop_{poverty_lines_cents[i]}': 'reporting_pop'}, inplace=True)
    else:
        df_final.drop(columns=[f'reporting_pop_{poverty_lines_cents[i]}'], inplace=True)

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

for i in range(len(poverty_lines_cents)):
    col_avg_shortfall.append(f'avg_shortfall_{poverty_lines_cents[i]}')
    col_headcount.append(f'headcount_{poverty_lines_cents[i]}')
    col_headcount_ratio.append(f'headcount_ratio_{poverty_lines_cents[i]}')
    col_incomegap.append(f'income_gap_ratio_{poverty_lines_cents[i]}')
    col_povertygap.append(f'poverty_gap_index_{poverty_lines_cents[i]}')
    col_tot_shortfall.append(f'total_shortfall_{poverty_lines_cents[i]}')

#Concatenate the entire list (including the previously estimated col_stacked_n and col_stacked_pct) and reorder
cols = col_ids + col_headcount + col_headcount_ratio + col_povertygap + col_tot_shortfall + col_avg_shortfall + col_incomegap + col_stacked_n + col_stacked_pct
df_final = df_final[cols]

# %% [markdown]
# ## Missing values
# In this section I look for observations which are missing or with a zero value for the poverty variables. First, I check the null observations:

# %%
cols_to_check = ['reporting_pop'] + col_headcount + col_headcount_ratio + col_povertygap + col_tot_shortfall + col_avg_shortfall + col_incomegap + col_stacked_n + col_stacked_pct

df_null = df_final[df_final[cols_to_check].isna().any(1)].copy().reset_index(drop=True)
df_null

# %% [markdown]
# 885 rows have at least one null value. But the distribution of them by variable is not uniform:

# %%
# Count number of nulls in all columns of Dataframe
for column_name in cols_to_check:
    column = df_null[column_name]
    # Get the count of nulls in column 
    count = (column.isnull()).sum()
    print(f'Count of nulls in column {column_name} is : {count}')

# %% [markdown]
# Only the average shortfall and income gap ratio variables have much more null values compared to the rest. If I exclude them from the analysis I only have 14 observations with nulls: **Guinea-Bissau** 1981-1992 and **Sierra Leone** 1999 and 2001:

# %%
cols_to_check = col_headcount + col_headcount_ratio + col_povertygap + col_tot_shortfall + col_stacked_n + col_stacked_pct

df_null_selected = df_final[df_final[cols_to_check].isna().any(1)].copy().reset_index(drop=True)
df_null_selected

# %% [markdown]
# 76 different countries show null values for average shortfall and income gap ratio variables.

# %%
cols_to_check = col_avg_shortfall + col_incomegap

df_null_selected = df_final[df_final[cols_to_check].isna().any(1)].copy().reset_index(drop=True)
df_null_selected['entity'].value_counts()

# %% [markdown]
# ## Zero values
# What about zero values? 1051 observations include at least one value equal to zero.

# %%
cols_to_check = ['reporting_pop'] + col_headcount + col_headcount_ratio + col_povertygap + col_tot_shortfall + col_stacked_n + col_stacked_pct
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
# | 1.0 | 863 | 863 | 0 | 0 |
# | 1.9 | 406 | 406 | 0 | 0 |
# | 3.2 | 200 | 200 | 0 | 0 |
# | 5.5 | 67 | 79 | 12 | 12 |
# | 10 | 35 | 47 | 12 | 12 |
# | 20 | 18 | 30 | 12 | 12 |
# | 30 | 6 | 18 | 12 | 12 |
# | 40 | 0 | 14 | 14 | 14 |

# %%
cols_to_check = col_headcount

df_zero_selected = df_final[(df_final[cols_to_check] == 0).any(1)].reset_index(drop=True)
df_zero_selected['entity'].value_counts()

# %% [markdown]
# ## Percentage on different poverty lines do not add up to 100%
# For each country-year the total number of people below, between and over multiple poverty lines are estimated to create a stacked chart with the distribution of income/consumption of the population. It is important then that these numbers add together to the total population (the aggregated percentage is 100%)

# %% [markdown]
# There are two countries with issues on several years, which are the same two reported before: **Guinea-Bissau**'s total for the years 1981-1992 is less than 1 (around 0.7). In the table we can see why: there are no estimation of poor people living below \\$5.5 or any higher poverty line. A similar case happens with **Sierra Leone**, but with less impact: 1999 and 2001 show totals very close to 1, but there is a tiny fraction of people not considered because the query does not generate results for people earning less than \\$40 a day. As this number is very close to 1 we consider to only exclude the Guinea-Bissau cases.

# %%
df_final['sum_pct'] = df_final[col_stacked_pct].sum(axis=1)
df_not_1 = df_final[(df_final['sum_pct'] >= 1.00000001) | (df_final['sum_pct'] <= 0.99999999)].copy().reset_index(drop=True)
df_not_1

# %% [markdown]
# Note this is the dataset including both survey and inter/extrapolated data, as we can see here by querying again. Only Guinea-Bissau data from 1991 is from a survey, all the other 13 rows with issues come from filled data.

# %%
df = pip_query_country(
                    popshare_or_povline = "povline", 
                    value = 1.9, 
                    fill_gaps='false')
df[(df['country_name'] == 'Sierra Leone') | (df['country_name'] == 'Guinea-Bissau')][['country_name', 'reporting_year', 'reporting_level', 'welfare_type', 'estimation_type']]

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
# **Croatia, Guinea-Bissau, Sierra Leone and United Arab Emirates** show issues:

# %%
df_check = df_final[(df_final['m_check_1'] == False) 
        | (df_final['m_check_2'] == False)
        | (df_final['m_check_3'] == False)
        | (df_final['m_check_4'] == False)
        | (df_final['m_check_5'] == False)
        | (df_final['m_check_6'] == False)
        | (df_final['m_check_7'] == False)
        ].copy()
df_check[['entity', 'year'] + m_check_vars]

# %%
print('Percentage of errors for each variable')
(len(df_check) - df_check[m_check_vars].sum(0))/len(df_check)*100

# %% [markdown]
# This is because for Croatia there are not headcount values for the \\$5.5 poverty line for years between 1981 and 1988. Guinea Bissau and Sierra Leone cases are the same considered for the stacked variables in the previous section and the UAE situation is the strangest of the group: the headcount below the \\$10 poverty line is one order of magnitude greater than the headcount below \\$20

# %%
df_check[['entity', 'year'] + col_headcount]

# %% [markdown]
# Only Croatia-1988, UAE-2018 and Guinea-Bissau 1991 come from survey data. The other 21 rows come from filled data. This is the same situation for the headcount ratio, poverty gap and total shortfall variables.

# %%
df = pip_query_country(
                    popshare_or_povline = "povline", 
                    value = 1.9, 
                    fill_gaps='false')
df[(df['country_name'] == 'Croatia') |(df['country_name'] == 'United Arab Emirates')][['country_name', 'reporting_year', 'reporting_level', 'welfare_type', 'estimation_type']]

# %% [markdown]
# ### Average shortfall
# With this variable there are much more monotonicity issues: 1349 observations are affected (*though I am not sure monotonicity should exist*)

# %%
m_check_vars = []
for i in range(len(col_avg_shortfall)):
    if i > 0:
        check_varname = f'm_check_{i}'
        df_final[check_varname] = df_final[f'{col_avg_shortfall[i]}'] >= df_final[f'{col_avg_shortfall[i-1]}']
        m_check_vars.append(check_varname)


# %%
df_check = df_final[(df_final['m_check_1'] == False) 
        | (df_final['m_check_2'] == False)
        | (df_final['m_check_3'] == False)
        | (df_final['m_check_4'] == False)
        | (df_final['m_check_5'] == False)
        | (df_final['m_check_6'] == False)
        | (df_final['m_check_7'] == False)
        ].copy()
df_check[['entity', 'year'] + m_check_vars]

# %%
print('Percentage of errors for each variable')
(len(df_check) - df_check[m_check_vars].sum(0))/len(df_check)*100

# %%
df_check[['entity', 'year'] + col_avg_shortfall]

# %% [markdown]
# ### Income gap ratio
# With this variable there are even more monotonicity issues: 3630 observations are affected (*though I am not sure monotonicity should exist*)

# %%
m_check_vars = []
for i in range(len(col_incomegap)):
    if i > 0:
        check_varname = f'm_check_{i}'
        df_final[check_varname] = df_final[f'{col_incomegap[i]}'] >= df_final[f'{col_incomegap[i-1]}']
        m_check_vars.append(check_varname)


# %%
df_check = df_final[(df_final['m_check_1'] == False) 
        | (df_final['m_check_2'] == False)
        | (df_final['m_check_3'] == False)
        | (df_final['m_check_4'] == False)
        | (df_final['m_check_5'] == False)
        | (df_final['m_check_6'] == False)
        | (df_final['m_check_7'] == False)
        ].copy()
df_check[['entity', 'year'] + m_check_vars]

# %%
print('Percentage of errors for each variable')
(len(df_check) - df_check[m_check_vars].sum(0))/len(df_check)*100

# %%
df_check[['entity', 'year'] + col_incomegap]

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
# On a first visual inspection we can see a big bump in the headcount data between 1988 and 1989, mainly driven by China. Another bump in 1998 is driven by Indonesia. There is missing headcount data for South Asia between 1997 and 2001 and in Sub Saharan Africa before 1990, but it seems not to be affected for the world aggregation.

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
# We can see the countries aggregations for headcount in different poverty lines are fairly similar to the world aggregation: the countries aggregation ranges between 97.5% and 99%, concentrated mostly around 98%. Similar situation happens with the total shortfall.

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
# Regional aggregations are a different story. The missing data for South Asia and Sub Saharan Africa makes the aggregations less reliable: ranging from 55-70% to almost 100% of the world aggregation. We recommend to not use the regional aggregations together without any transformation. Similar situation happens with the total shortfall.

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
