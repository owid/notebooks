# %% [markdown]
# # World Bank Poverty and Inequality Platform dataset
#
# ***To get the most updated dataset it is required to run the `relative_poverty.py` code first. It is not included here because it takes more than an hour to complete.***

# %%
import pandas as pd
import numpy as np

from functions.PIP_API_query import pip_query_country, pip_query_region
from functions.standardize_entities import standardize_entities
from functions.upload import upload_to_s3

import time

# %%
# Here we define the poverty lines to query as cents
poverty_lines_cents = [100, 190, 320, 550, 1000, 2000, 3000, 4000]

# %% [markdown]
# ## Querying the dataset from the PIP API

# %%
#Create a dataframe for each poverty line on the list, including and excluding interpolations and for countries and regions
#Each of these combinations are concatenated in a larger data frame.

start_time = time.time()

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

            #"Entity" when is in titlecase is automatically recognised as EntityName
            #Year is only recognised as a Year type when titlecase
            df = df.rename(columns={'country_name': 'Entity',
                                    'reporting_year': 'Year'})

            # Keep only these variables:
            keep_vars = [ 
                'Entity',
                'Year',
                'reporting_level',
                'welfare_type', 
                'headcount',
                'poverty_gap',
                'poverty_severity', 
                'watts',
                'reporting_pop'
            ]

        # Make the API query for region data
        # Note that the filled and not filled data is the same in this case .
        # The code runs it twice anyhow.
        if ent_type == 'region':

            df = pip_query_region(p_dollar)

            df = df.rename(columns={'region_name': 'Entity',
                                   'reporting_year': 'Year'})

            keep_vars = [ 
                'Entity',
                'Year',
                'headcount',
                'poverty_gap',
                'poverty_severity',
                'watts',
                'reporting_pop'
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
        df['ent_type'] = ent_type

        #Concatenate all the results
        df_complete = pd.concat([df_complete, df],ignore_index=True)
        
#I drop 'reporting_pop' for now to avoid it to get multiplied by all the poverty lines in the next section
df_complete = df_complete.drop(columns=['reporting_pop'])

end_time = time.time()
elapsed_time = end_time - start_time
print('Execution time:', elapsed_time, 'seconds')


# %% [markdown]
# ## Data transformations

# %%
# Create different combinations of dataframe from df_complete

# Select data for countries 
headcounts_country = df_complete[(df_complete['ent_type'] == 'country')].reset_index(drop=True)

# Select data for regions
headcounts_region = df_complete[(df_complete['ent_type'] == 'region')].reset_index(drop=True)

#Create pivot tables to make the data wide
headcounts_country_wide = headcounts_country.pivot_table(index=['Entity', 'Year', 'reporting_level', 'welfare_type'], 
                columns='poverty line')

headcounts_region_wide = headcounts_region.pivot_table(index=['Entity', 'Year'], 
                columns='poverty line')

#Join multi index columns
headcounts_country_wide.columns = [''.join(col).strip() for col in headcounts_country_wide.columns.values]
headcounts_country_wide = headcounts_country_wide.reset_index()

headcounts_region_wide.columns = [''.join(col).strip() for col in headcounts_region_wide.columns.values]
headcounts_region_wide = headcounts_region_wide.reset_index()

#Concatenate country and regional wide datasets
df_final = pd.concat([headcounts_country_wide, headcounts_region_wide], ignore_index=False)


#Integrate variables not coming from multiple poverty lines
df_query_country = pip_query_country(
                    popshare_or_povline = "povline", 
                    value = 1.9, 
                    fill_gaps="false")
df_query_country = df_query_country.rename(columns={'country_name': 'Entity',
                                                    'reporting_year': 'Year'})

df_query_regions = pip_query_region(1.9)
df_query_regions = df_query_regions.rename(columns={'region_name': 'Entity',
                                                    'reporting_year': 'Year'})

df_query_country = df_query_country[['Entity', 'Year', 'reporting_level', 'welfare_type',
                                     'reporting_pop',
                                     'survey_year',
                                     'survey_comparability', 
                                     'comparable_spell', 
                                     'mean', 
                                     'median', 
                                     'mld',
                                     'gini', 
                                     'polarization', 
                                     'decile1', 'decile2', 'decile3', 'decile4','decile5', 
                                     'decile6', 'decile7', 'decile8', 'decile9', 'decile10',
                                     'cpi', 'ppp', 'reporting_gdp', 'reporting_pce', 
                                     'distribution_type', 'estimation_type']]

for i in range(1,11):
    df_query_country = df_query_country.rename(columns={f'decile{i}': f'decile{i}_share'})


df_query_regions = df_query_regions[['Entity', 'Year', 'reporting_pop', 'mean']]

df_final = pd.merge(df_final, df_query_country,
                    how='left', 
                    on=['Entity', 'Year', 'welfare_type', 'reporting_level'],
                    validate='many_to_one')

df_final = pd.merge(df_final, df_query_regions,
                    how='left', 
                    on=['Entity', 'Year'],
                    validate='many_to_one')

df_final['mean'] = np.where((df_final['mean_x'].isnull()) & ~(df_final['mean_y'].isnull()), df_final['mean_y'], df_final['mean_x'])
df_final['reporting_pop'] = np.where((df_final['reporting_pop_x'].isnull()) & ~(df_final['reporting_pop_y'].isnull()), df_final['reporting_pop_y'], df_final['reporting_pop_x'])

df_final = df_final.drop(columns=['mean_x', 'mean_y', 'reporting_pop_x', 'reporting_pop_y'])

# %% [markdown]
# ## Patching missing median data
# A small but considerable part of the median data is not available by default (PIP does not provide China, India and Indonesia national medians). It can be obtained by getting the poverty line for the 50% of the population, with the `popshare` command.

# %%
start_time = time.time()

df_query = pip_query_country(
                    popshare_or_povline = "povline", 
                    value = 1.9, 
                    fill_gaps="false")

median_list = []

for i in range(len(df_query)):
    if np.isnan(df_query['median'][i]):
        df_popshare = pip_query_country(popshare_or_povline = "popshare",
                                        country_code = df_query['country_code'][i],
                                        year = df_query['reporting_year'][i],
                                        welfare_type = df_query['welfare_type'][i],
                                        reporting_level = df_query['reporting_level'][i],
                                        value = 0.5,
                                        fill_gaps="false")
        try:
            median_value = df_popshare['poverty_line'][0]
            median_list.append(median_value)
        
        except:
            median_list.append(np.nan)
        
        
    else:
        median_value = df_query['median'][i]
        median_list.append(median_value)
               

df_query['median2'] = median_list
df_query = df_query.rename(columns={'country_name': 'Entity',
                                    'reporting_year': 'Year'})
null_median = (df_query['median'].isnull()).sum()
null_median2 = (df_query['median2'].isnull()).sum()
print(f'Before patching: {null_median} nulls for median')
print(f'After patching: {null_median2} nulls for median')

df_final = pd.merge(df_final, df_query[['Entity', 'Year', 'welfare_type', 'reporting_level', 'median2']], 
                       how='left', 
                       on=['Entity', 'Year', 'welfare_type', 'reporting_level'], 
                       validate='many_to_one')
df_final['median_ratio'] = df_final['median'] / df_final['median2']
median_ratio_median = (df_final['median_ratio']).median()
median_ratio_min = (df_final['median_ratio']).min()
median_ratio_max = (df_final['median_ratio']).max()

if median_ratio_median == 1 and median_ratio_min == 1 and median_ratio_max == 1:
    print(f'Patch successful.')
    print(f'Ratio between old and new variable: Median = {median_ratio_median}, Min = {median_ratio_min}, Max = {median_ratio_max}')
else:
    print(f'Patch changed some median values. Please check for errors.')
    print(f'Ratio between old and new variable: Median = {median_ratio_median}, Min = {median_ratio_min}, Max = {median_ratio_max}')

df_final.drop(columns=['median', 'median_ratio'], inplace=True)
df_final.rename(columns={'median2': 'median'}, inplace=True)


end_time = time.time()
elapsed_time = end_time - start_time
print('Execution time:', elapsed_time, 'seconds')

# %% [markdown]
# ## Decile thresholds

# %%
df_threshold = pd.DataFrame()


for dec in range(1,10):

    popshare = dec/10
    
    df = pip_query_country(
                    popshare_or_povline = "popshare", 
                    value = popshare, 
                    fill_gaps='false')

    df['requested_decile'] = dec
    decile_number = dec + 1
    df['decile_name'] = f'decile{decile_number}_thr'

    df_threshold = pd.concat([df_threshold, df],ignore_index=True)
    
df_threshold = pd.pivot(df_threshold, index=['country_name', 'reporting_year', 'reporting_level', 'welfare_type'],
                       columns='decile_name', values='poverty_line').reset_index()

df_threshold = df_threshold.rename(columns={'country_name': 'Entity',
                                            'reporting_year': 'Year'})

df_final = pd.merge(df_final, df_threshold, 
                       how='left', 
                       on=['Entity', 'Year', 'welfare_type', 'reporting_level'],
                       validate='many_to_one')

# %% [markdown]
# ## Integrate the relative poverty data
# The data comes from an over 1 hour query in `relative_poverty.py`. Be warned you have to update it first when running a massive update to the dataset

# %%
file = 'data/relative_poverty.csv'
df_relative = pd.read_csv(file)

col_headcount_relative = ['headcount_40', 'headcount_50', 'headcount_60']
col_headcount_ratio_relative = ['headcount_ratio_40', 'headcount_ratio_50', 'headcount_ratio_60']

df_final = pd.merge(df_final, df_relative[['Entity', 'Year', 'reporting_level', 'welfare_type'] + col_headcount_relative + col_headcount_ratio_relative], 
                    how='left', on=['Entity', 'Year', 'reporting_level', 'welfare_type'])

# %%
#Calculate numbers in poverty between pov lines for stacked area charts
#Make sure the poverty lines are in order, lowest to highest
poverty_lines_cents.sort()

col_stacked_n = []
col_stacked_pct = []

#For each poverty line in poverty_lines_cents
for i in range(len(poverty_lines_cents)):
    #if it's the first value only get people below this poverty line (and percentage)
    if i == 0:
        varname_n = f'headcount_stacked_below_{poverty_lines_cents[i]}'
        df_final[varname_n] = df_final[f'headcount_{poverty_lines_cents[i]}']
        col_stacked_n.append(varname_n)

        varname_pct = f'headcount_ratio_stacked_below_{poverty_lines_cents[i]}'
        df_final[varname_pct] = df_final[varname_n] / df_final['reporting_pop']
        col_stacked_pct.append(varname_pct)

    #If it's the last value calculate the people between this value and the previous 
    #and also the people over this poverty line (and percentages)
    elif i == len(poverty_lines_cents)-1:

        varname_n = f'headcount_stacked_below_{poverty_lines_cents[i]}'
        df_final[varname_n] = df_final[f'headcount_{poverty_lines_cents[i]}'] - df_final[f'headcount_{poverty_lines_cents[i-1]}']
        col_stacked_n.append(varname_n)

        varname_pct = f'headcount_ratio_stacked_below_{poverty_lines_cents[i]}'
        df_final[varname_pct] = df_final[varname_n] / df_final['reporting_pop']
        col_stacked_pct.append(varname_pct)

        varname_n = f'headcount_stacked_above_{poverty_lines_cents[i]}'
        df_final[varname_n] = df_final['reporting_pop'] - df_final[f'headcount_{poverty_lines_cents[i]}']
        col_stacked_n.append(varname_n)

        varname_pct = f'headcount_ratio_stacked_above_{poverty_lines_cents[i]}'
        df_final[varname_pct] = df_final[varname_n] / df_final['reporting_pop']
        col_stacked_pct.append(varname_pct)

    #If it's any value between the first and the last calculate the people between this value and the previous (and percentage)
    else:
        varname_n = f'headcount_stacked_below_{poverty_lines_cents[i]}'
        df_final[varname_n] = df_final[f'headcount_{poverty_lines_cents[i]}'] - df_final[f'headcount_{poverty_lines_cents[i-1]}']
        col_stacked_n.append(varname_n)

        varname_pct = f'headcount_ratio_stacked_below_{poverty_lines_cents[i]}'
        df_final[varname_pct] = df_final[varname_n] / df_final['reporting_pop']
        col_stacked_pct.append(varname_pct)

df_final.loc[:, col_stacked_pct] = df_final[col_stacked_pct] * 100

# Create decile variables: average and threshold (besides share)
col_decile_share = []
col_decile_avg = []
col_decile_thr = []

for i in range(1,11):
    
    if i !=1:
        varname_thr = f'decile{i}_thr'
        col_decile_thr.append(varname_thr)
    
    varname_share = f'decile{i}_share'
    varname_avg = f'decile{i}_avg'
    df_final[varname_avg] = df_final[varname_share] * df_final['mean'] / 0.1
    
    col_decile_share.append(varname_share)
    col_decile_avg.append(varname_avg)

# Standardize entity names
df_final = standardize_entities(
    orig_df = df_final,
    entity_mapping_url = "https://joeh.fra1.digitaloceanspaces.com/PIP/country_mapping.csv",
    mapping_varname_raw ='Original Name',
    mapping_vaname_owid = 'Our World In Data Name',
    data_varname_old = 'Entity',
    data_varname_new = 'Entity'
)

# Amend the entity to reflect if data refers to urban or rural only
df_final.loc[(\
    df_final['reporting_level'].isin(["urban", "rural"])),'Entity'] = \
    df_final.loc[(\
    df_final['reporting_level'].isin(["urban", "rural"])),'Entity'] + \
        ' - ' + \
    df_final.loc[(\
    df_final['reporting_level'].isin(["urban", "rural"])),'reporting_level']

# Tidying – Rename cols

#Order columns by categorising them
col_ids = ['Entity', 'Year', 'reporting_level', 'welfare_type', 'reporting_pop']
col_avg_shortfall = []
col_headcount = []
col_headcount_ratio = []
col_incomegap = []
col_povertygap = []
col_tot_shortfall = []
col_poverty_severity = []
col_watts = []
col_central = ['mean', 'median']
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
    
#Multiplies decile columns by 100
df_final.loc[:, col_decile_share] = df_final[col_decile_share] * 100

#Concatenate the entire list of columns and reorder
cols = col_ids + col_central + col_headcount + col_headcount_ratio + col_povertygap + col_tot_shortfall + col_avg_shortfall + col_incomegap + col_stacked_n + col_stacked_pct + col_poverty_severity + col_watts + col_headcount_relative + col_headcount_ratio_relative + col_decile_share + col_decile_thr + col_decile_avg + col_inequality + col_extra
df_final = df_final[cols]

# %% [markdown]
# ## Dropping rows with issues

# %%
# stacked values not adding up to 100%
print(f'{len(df_final)} rows before stacked values check')
df_final['sum_pct'] = df_final[col_stacked_pct].sum(axis=1)
df_final = df_final[~((df_final['sum_pct'] >= 100.1) | (df_final['sum_pct'] <= 99.9))].reset_index(drop=True)
print(f'{len(df_final)} rows before stacked values check')

#missing poverty values (headcount, poverty gap, total shortfall)
print(f'{len(df_final)} rows before missing values check')
cols_to_check = col_headcount + col_headcount_ratio + col_povertygap + col_tot_shortfall + col_stacked_n + col_stacked_pct
df_final = df_final[~df_final[cols_to_check].isna().any(1)].reset_index(drop=True)
print(f'{len(df_final)} rows before missing values check')

# headcount monotonicity check
print(f'{len(df_final)} rows before headcount monotonicity check')
m_check_vars = []
for i in range(len(col_headcount)):
    if i > 0:
        check_varname = f'm_check_{i}'
        df_final[check_varname] = df_final[f'{col_headcount[i]}'] >= df_final[f'{col_headcount[i-1]}']
        m_check_vars.append(check_varname)       
df_final['check_total'] = df_final[m_check_vars].all(1)
df_final = df_final[df_final['check_total'] == True].reset_index(drop=True)
print(f'{len(df_final)} rows before headcount monotonicity  check')

# deciles values not adding up to 100% NOT READY*****************
print(f'{len(df_final)} rows before deciles values check')
world_list = ['World']

regions_list = ['East Asia and Pacific', 
           'Europe and Central Asia',
           'Latin America and the Caribbean', 
           'Middle East and North Africa', 
           'South Asia', 
           'Sub-Saharan Africa']

high_income_list = ['High income countries']

df_final['sum_deciles'] = df_final[col_decile_share].sum(axis=1)
#df_final = df_final[~((df_final['sum_deciles'] >= 100.1) | (df_final['sum_deciles'] <= 99.9)) 
#                    | (df_final['sum_deciles'].isna())].reset_index(drop=True)
print(f'{len(df_final)} rows before deciles values check CODE NOT READY YET')

# %%
df_final

# %% [markdown]
# ## Exporting the transformed dataset

# %%
# Separate out consumption-only, income-only, and both dataframes
df_inc_only = df_final[df_final['welfare_type']=="income"].reset_index(drop=True).copy()
df_cons_only = df_final[df_final['welfare_type']=="consumption"].reset_index(drop=True).copy()

df_inc_or_cons = df_final.copy()
# If both inc and cons are available in a given year, drop inc

# Flag duplicates – indicating multiple welfare_types
#Sort values to ensure the welfare_type consumption is marked as False when there are multiple welfare types
df_inc_or_cons.sort_values(by=['Entity', 'Year', 'reporting_level', 'welfare_type'], ignore_index=True)
df_inc_or_cons['duplicate_flag'] = df_inc_or_cons.duplicated(subset=['Entity', 'Year', 'reporting_level'])

print(f'Checking the data for years with both income and consumption. Before dropping duplicated, there were {len(df_inc_or_cons)} rows...')
# Drop income where income and consumption are available
df_inc_or_cons = df_inc_or_cons[(df_inc_or_cons['duplicate_flag']==False) | (df_inc_or_cons['welfare_type']=='consumption')]
df_inc_or_cons.drop(columns=['duplicate_flag'], inplace=True)

print(f'After dropping duplicates there were {len(df_inc_or_cons)} rows.')


# I think better would be to save this to s3 – but I don't know how to format the url from 
# digital ocean so that the data can be picked up in the explorer. But I know how to do this
# if it's stored in GitHub. So for now I write it as csvs to this folder.
# Save as csv
df_inc_only.to_csv(f'data/poverty_inc_only.csv', index=False)
df_cons_only.to_csv(f'data/poverty_cons_only.csv', index=False)
df_inc_or_cons.to_csv(f'data/poverty_inc_or_cons.csv', index=False)



#upload_to_s3(df_inc_only, 'PIP', f'poverty_inc_only_filled_{is_filled}.csv')

#upload_to_s3(df_cons_only, 'PIP', f'poverty_cons_only_filled_{is_filled}.csv')

#upload_to_s3(df_inc_or_cons, 'PIP', f'poverty_inc_or_cons_filled_{is_filled}.csv')

# %%
