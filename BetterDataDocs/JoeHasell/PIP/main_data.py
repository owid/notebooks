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

# %%
#Create a dataframe for each poverty line on the list, including and excluding interpolations and for countries and regions
#Each of these combinations are concatenated in a larger data frame.

start_time = time.time()

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

                #"Entity" when is in titlecase is automatically recognised as EntityName
                df = df.rename(columns={'country_name': 'Entity'})
                
                # Keep only these variables:
                keep_vars = [ 
                    'Entity',
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

                df = df.rename(columns={'region_name': 'Entity'})

                keep_vars = [ 
                    'Entity',
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
for is_filled in ['true', 'false']:

    # Select data for countries and filled or not
    headcounts_country = df_complete[(df_complete['ent_type'] == 'country') & (df_complete['filled'] == is_filled)].reset_index(drop=True)

    # Select data for regions and filled or not
    headcounts_region = df_complete[(df_complete['ent_type'] == 'region')  & (df_complete['filled'] == is_filled)].reset_index(drop=True)

    #Create pivot tables to make the data wide
    headcounts_country_wide = headcounts_country.pivot_table(index=['Entity', 'reporting_year','reporting_level','welfare_type'], 
                    columns='poverty line')

    headcounts_region_wide = headcounts_region.pivot_table(index=['Entity', 'reporting_year'], 
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
            
    print(f'{len(df_final)} rows before stacked values check (Filled: {is_filled})')
    df_final['sum_pct'] = df_final[col_stacked_pct].sum(axis=1)
    #df_final = df_final[df_final['sum_pct'] == 1].reset_index(drop=True)
    df_final = df_final[~((df_final['sum_pct'] >= 100.1) | (df_final['sum_pct'] <= 99.9))].reset_index(drop=True)
    print(f'{len(df_final)} rows before stacked values check (Filled: {is_filled})')
            

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
    #Year is only recognised as a Year type when titlecase
    df_final = df_final.rename(columns={'reporting_year': 'Year'})
    
    #Order columns by categorising them
    col_ids = ['Entity', 'Year', 'reporting_level', 'welfare_type', 'reporting_pop']
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

    # Separate out consumption-only, income-only, and both dataframes
    df_inc_only = df_final[df_final['welfare_type']=="income"].reset_index(drop=True).copy()
    df_cons_only = df_final[df_final['welfare_type']=="consumption"].reset_index(drop=True).copy()

    df_inc_or_cons = df_final.copy()
    # If both inc and cons are available in a given year, drop inc

    # Flag duplicates – indicating multiple welfare_types
    #Sort values to ensure the welfare_type consumption is marked as False when there are multiple welfare types
    df_inc_or_cons.sort_values(by=['Entity', 'Year', 'reporting_level', 'welfare_type'], ignore_index=True)
    df_inc_or_cons['duplicate_flag'] = df_inc_or_cons.duplicated(subset=['Entity', 'Year', 'reporting_level'])

    print(f'Checking the filled = {is_filled} data for years with both income and consumption. Before dropping duplicated, there were {len(df_inc_or_cons)} rows...')
    # Drop income where income and consumption are available
    df_inc_or_cons = df_inc_or_cons[(df_inc_or_cons['duplicate_flag']==False) | (df_inc_or_cons['welfare_type']=='consumption')]
    df_inc_or_cons.drop(columns=['duplicate_flag'], inplace=True)
    
    print(f'After dropping duplicates there were {len(df_inc_or_cons)} rows.')


    # I think better would be to save this to s3 – but I don't know how to format the url from 
    # digital ocean so that the data can be picked up in the explorer. But I know how to do this
    # if it's stored in GitHub. So for now I write it as csvs to this folder.
    # Save as csv
    df_inc_only.to_csv(f'data/poverty_inc_only_filled_{is_filled}.csv', index=False)
    df_cons_only.to_csv(f'data/poverty_cons_only_filled_{is_filled}.csv', index=False)
    df_inc_or_cons.to_csv(f'data/poverty_inc_or_cons_filled_{is_filled}.csv', index=False)



    #upload_to_s3(df_inc_only, 'PIP', f'poverty_inc_only_filled_{is_filled}.csv')

    #upload_to_s3(df_cons_only, 'PIP', f'poverty_cons_only_filled_{is_filled}.csv')

    #upload_to_s3(df_inc_or_cons, 'PIP', f'poverty_inc_or_cons_filled_{is_filled}.csv')

# %% [markdown]
# ## Relative poverty

# %%
df = pip_query_country(
                    popshare_or_povline = "povline", 
                    value = 1.9, 
                    fill_gaps="true")

# %%
df.columns

# %%
df[['median']].describe()

# %%
df['median_40'] = df['median'] * 0.4
df['median_50'] = df['median'] * 0.5
df['median_60'] = df['median'] * 0.6

# %%
df.to_csv('complete.csv')

# %%
df = df.iloc[0:10,:]

# %%
import numpy as np

start_time = time.time()

headcount_40_list = []
headcount_50_list = []
headcount_60_list = []

for i in range(len(df)):

    df_query_40 = pip_query_country(popshare_or_povline = "povline",
                                    country_code = df['country_code'][i],
                                    year = df['reporting_year'][i],
                                    welfare_type = df['welfare_type'][i],
                                    reporting_level = df['reporting_level'][i],
                                    value = df['median_40'][i],
                                    fill_gaps="true")
    
    df_query_50 = pip_query_country(popshare_or_povline = "povline",
                                    country_code = df['country_code'][i],
                                    year = df['reporting_year'][i],
                                    welfare_type = df['welfare_type'][i],
                                    reporting_level = df['reporting_level'][i],
                                    value = df['median_50'][i],
                                    fill_gaps="true")
    
    df_query_60 = pip_query_country(popshare_or_povline = "povline",
                                    country_code = df['country_code'][i],
                                    year = df['reporting_year'][i],
                                    welfare_type = df['welfare_type'][i],
                                    reporting_level = df['reporting_level'][i],
                                    value = df['median_60'][i],
                                    fill_gaps="true")
    
    try:
        headcount_40_value = df_query_40['headcount'][0]
        headcount_40_list.append(headcount_40_value)
        
        headcount_50_value = df_query_50['headcount'][0]
        headcount_50_list.append(headcount_50_value)
        
        headcount_60_value = df_query_60['headcount'][0]
        headcount_60_list.append(headcount_60_value)
        
    except:
        headcount_40_list.append(np.nan)
        headcount_50_list.append(np.nan)
        headcount_60_list.append(np.nan)
        
df['headcount_ratio_40'] = headcount_40_list
df['headcount_ratio_50'] = headcount_50_list
df['headcount_ratio_60'] = headcount_60_list

end_time = time.time()
elapsed_time = end_time - start_time
print('Execution time:', elapsed_time, 'seconds')

# %%
import numpy as np

start_time = time.time()

headcount_40_list = []
headcount_50_list = []
headcount_60_list = []

median = 0

for i in range(len(df)):
    
    if median == df['median'][i]:
        
        headcount_40_list.append(headcount_40_value)
        headcount_50_list.append(headcount_50_value)
        headcount_60_list.append(headcount_60_value)
        
    else:
        
        median = df['median'][i]

        df_query_40 = pip_query_country(popshare_or_povline = "povline",
                                        country_code = df['country_code'][i],
                                        year = df['reporting_year'][i],
                                        welfare_type = df['welfare_type'][i],
                                        reporting_level = df['reporting_level'][i],
                                        value = df['median_40'][i],
                                        fill_gaps="true")

        df_query_50 = pip_query_country(popshare_or_povline = "povline",
                                        country_code = df['country_code'][i],
                                        year = df['reporting_year'][i],
                                        welfare_type = df['welfare_type'][i],
                                        reporting_level = df['reporting_level'][i],
                                        value = df['median_50'][i],
                                        fill_gaps="true")

        df_query_60 = pip_query_country(popshare_or_povline = "povline",
                                        country_code = df['country_code'][i],
                                        year = df['reporting_year'][i],
                                        welfare_type = df['welfare_type'][i],
                                        reporting_level = df['reporting_level'][i],
                                        value = df['median_60'][i],
                                        fill_gaps="true")

        try:
            headcount_40_value = df_query_40['headcount'][0]
            headcount_50_value = df_query_50['headcount'][0]
            headcount_60_value = df_query_60['headcount'][0]

        except:
            headcount_40_value = np.nan
            headcount_50_value = np.nan
            headcount_60_value = np.nan
            
        headcount_40_list.append(headcount_40_value)
        headcount_50_list.append(headcount_50_value)
        headcount_60_list.append(headcount_60_value)
        
df['headcount_ratio_40'] = headcount_40_list
df['headcount_ratio_50'] = headcount_50_list
df['headcount_ratio_60'] = headcount_60_list

end_time = time.time()
elapsed_time = end_time - start_time
print('Execution time:', elapsed_time, 'seconds')

# %%
