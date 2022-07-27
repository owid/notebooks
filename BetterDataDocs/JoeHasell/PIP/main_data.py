# %%
import pandas as pd
import numpy as np

from functions.PIP_API_query import pip_query_country, pip_query_region
from functions.standardize_entities import standardize_enities
from functions.upload import upload_to_s3

import time


# %%

# function for multiplying by 100
def multiply_by_100(number):
            return 100 * number

# Here we define the poverty lines to query as cents
poverty_lines_cents = [100, 190, 320, 550, 1000, 1500, 2000, 3000, 4000]

# We make dictionaries to store the API responses, which will be concatenated later
# %%
start_time = time.time()


df_complete = pd.DataFrame()


#headcount_dfs = {}
#headcount_dfs['filled_true'] = {}
#headcount_dfs['filled_false'] = {}
#headcount_dfs['filled_true']['country'] = {}
#headcount_dfs['filled_true']['region'] = {}

#headcount_dfs['filled_false']['country'] = {}
#headcount_dfs['filled_false']['region'] = {}


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
            df['total_shortall'] = df['poverty_gap_index'] * p_dollar * df['reporting_pop']                      

            # Calculate average shortfall of incomes (averaged across population in poverty)
            df['avg_shortfall'] = df['total_shortall'] / df['headcount']

            # Calculate income gap ratio (according to Ravallion's definition)
            df['income_gap_ratio'] = (df['total_shortall'] / df['headcount']) / p_dollar


            # Shares to percentages
            # executing the function over list of vars
            var_list = ['headcount_ratio', 'income_gap_ratio', 'poverty_gap_index' ]

            df[var_list] = df[var_list].apply(multiply_by_100)  


            # Add poverty line as a var (I add the '_' character, because it being treated as a float later on was causing headaches)
            df['poverty line'] = f'_{p}'
            df['filled'] = is_filled
            df['ent_type'] = ent_type

            #Add dataframe to rolling dictionary.

            #headcount_dfs[f'filled_{is_filled}'][ent_type][p] = df
            
            df_complete = pd.concat([df_complete, df],ignore_index=True)

end_time = time.time()
elapsed_time = end_time - start_time
print('Execution time:', elapsed_time, 'seconds')


# %%
df_complete

# %%
# Unpack the dictionaries into two dfs (one for filled=true one for false)
for is_filled in ['true', 'false']:

# Append the dataframes for differnt poverty lines together
    headcounts_country = df_complete[(df_complete['ent_type'] == 'country') & (df_complete['filled'] == is_filled)].reset_index(drop=True)
    #headcounts_country = pd.concat(headcount_dfs[f'filled_{is_filled}']['country']).reset_index().\
    #    drop(columns = ['level_0', 'level_1'])

    
    headcounts_region = df_complete[(df_complete['ent_type'] == 'region')  & (df_complete['filled'] == is_filled)].reset_index(drop=True)
    #headcounts_region = pd.concat(headcount_dfs[f'filled_{is_filled}']['region']).reset_index().\
    #    drop(columns = ['level_0', 'level_1'])


    headcounts_country_wide = headcounts_country.pivot_table(index=['entity', 'reporting_year','reporting_level','welfare_type'], 
                    columns='poverty line')


    headcounts_region_wide = headcounts_region.pivot_table(index=['entity', 'reporting_year'], 
                    columns='poverty line')

    #Join multi index columns
    headcounts_country_wide.columns = [''.join(col).strip() for col in headcounts_country_wide.columns.values]
    headcounts_country_wide = headcounts_country_wide.reset_index()

    headcounts_region_wide.columns = [''.join(col).strip() for col in headcounts_region_wide.columns.values]
    headcounts_region_wide = headcounts_region_wide.reset_index()

    # Add NAN columns for reporting_level and welfare_type in the region data, before appending to country data
    # (I'm sure there must be a way to append even though you don't have all the columns in both datasets but I haven't worked it out yet)
    # Pablo: It's solved by just concatenating. The columns not available are marked with nan by default
    
    #headcounts_region_wide['reporting_level'] = np.NaN
    #headcounts_region_wide['welfare_type'] = np.NaN
    
    df_final = pd.concat([headcounts_country_wide, headcounts_region_wide], ignore_index=False)

    #df_final = headcounts_country_wide.append(headcounts_region_wide, ignore_index=False)


    # TO DO: Calculate numbers in poverty between pov lines for stacked area charts
    # I started with this below, but I haven't finished it.
    #Make sure the poverty lines are in order, lowest to highest
    poverty_lines_cents.sort()

    # # for the lowest poverty line, we set a temporary var equal to the headcount 
    #lower_varname = f'number_below_{poverty_lines_cents[0]}
    
    #df_final[lower_varname] = df_final[f'headcount_{poverty_lines_cents[0]}']
    
    
    for i in range(len(poverty_lines_cents)):
        if i == 0:
            df_final.rename(columns={f'reporting_pop_{poverty_lines_cents[i]}': 'reporting_pop'}, inplace=True)
        else:
            df_final.drop(columns=[f'reporting_pop_{poverty_lines_cents[i]}'], inplace=True)


    for i in range(len(poverty_lines_cents)):
        if i == 0:
            varname_n = f'number_below_{poverty_lines_cents[i]}'
            df_final[varname_n] = df_final[f'headcount_{poverty_lines_cents[i]}']
            
            varname_pct = f'percentage_below_{poverty_lines_cents[i]}'
            df_final[varname_pct] = df_final[varname_n] / df_final['reporting_pop']
            
            
        elif i == len(poverty_lines_cents)-1:
            
            varname_n = f'number_between_{poverty_lines_cents[i-1]}_{poverty_lines_cents[i]}'
            df_final[varname_n] = df_final[f'headcount_{poverty_lines_cents[i]}'] - df_final[f'headcount_{poverty_lines_cents[i-1]}']
            
            varname_pct = f'percentage_between_{poverty_lines_cents[i-1]}_{poverty_lines_cents[i]}'
            df_final[varname_pct] = df_final[varname_n] / df_final['reporting_pop']
            
            varname_n = f'number_over_{poverty_lines_cents[i]}'
            df_final[varname_n] = df_final['reporting_pop'] - df_final[f'headcount_{poverty_lines_cents[i]}']
            
            varname_pct = f'percentage_over_{poverty_lines_cents[i]}'
            df_final[varname_pct] = df_final[varname_n] / df_final['reporting_pop']
        
        else:
            varname_n = f'number_between_{poverty_lines_cents[i-1]}_{poverty_lines_cents[i]}'
            df_final[varname_n] = df_final[f'headcount_{poverty_lines_cents[i]}'] - df_final[f'headcount_{poverty_lines_cents[i-1]}']
            
            varname_pct = f'percentage_between_{poverty_lines_cents[i-1]}_{poverty_lines_cents[i]}'
            df_final[varname_pct] = df_final[varname_n] / df_final['reporting_pop']
            

    # Standardize entity names
    df_final = standardize_enities(
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


    # Separate out consumption-only, income-only, and both dataframes
    df_inc_only = df_final[df_final['welfare_type']=="income"].reset_index(drop=True).copy()
    df_cons_only = df_final[df_final['welfare_type']=="consumption"].reset_index(drop=True).copy()

    df_inc_or_cons = df_final.copy()
    # If both inc and cons are available in a given year, drop inc

    # Flag duplicates – indicating multiple welfare_types
    #Sort values to ensure the welfare_type consumption is marked as False when there are multiple welfare types
    df_inc_or_cons.sort_values(by=['entity', 'year', 'reporting_level', 'welfare_type'], ignore_index=True)
    df_inc_or_cons['duplicate_flag'] = df_inc_or_cons.duplicated(subset=['entity', 'year', 'reporting_level'])

    print(f'Checking the filled = {is_filled} data for years with both income and consumption. Before dropping duplicated, there were {df_inc_or_cons.shape[0]} rows...')
    # Drop income where income and consumption are available
    df_inc_or_cons = df_inc_or_cons[(df_inc_or_cons['duplicate_flag']==False) | (df_inc_or_cons['welfare_type']=='consumption')]
    
    print(f'After dropping duplicates there were {df_inc_or_cons.shape[0]} rows.')


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
# I am still keeping the original version of the code here:

# %%
start_time = time.time()

headcount_dfs = {}
headcount_dfs['filled_true'] = {}
headcount_dfs['filled_false'] = {}
headcount_dfs['filled_true']['country'] = {}
headcount_dfs['filled_true']['region'] = {}

headcount_dfs['filled_false']['country'] = {}
headcount_dfs['filled_false']['region'] = {}


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
            df['total_shortall'] = df['poverty_gap_index'] * p_dollar * df['reporting_pop']                      

            # Calculate average shortfall of incomes (averaged across population in poverty)
            df['avg_shortfall'] = df['total_shortall'] / df['headcount']

            # Calculate income gap ratio (according to Ravallion's definition)
            df['income_gap_ratio'] = (df['total_shortall'] / df['headcount']) / p_dollar


            # Shares to percentages
            # executing the function over list of vars
            var_list = ['headcount_ratio', 'income_gap_ratio', 'poverty_gap_index' ]

            df[var_list] = df[var_list].apply(multiply_by_100)  


            # Add poverty line as a var (I add the '_' character, because it being treated as a float later on was causing headaches)
            df['poverty line'] = f'_{p}'

            #Add dataframe to rolling dictionary.

            headcount_dfs[f'filled_{is_filled}'][ent_type][p] = df
            
end_time = time.time()
elapsed_time = end_time - start_time
print('Execution time:', elapsed_time, 'seconds')


# %%
# Unpack the dictionaries into two dfs (one for filled=true one for false)
for is_filled in ['true', 'false']:

# Append the dataframes for differnt poverty lines together
    headcounts_country = pd.concat(headcount_dfs[f'filled_{is_filled}']['country']).reset_index().\
        drop(columns = ['level_0', 'level_1'])

    headcounts_region = pd.concat(headcount_dfs[f'filled_{is_filled}']['region']).reset_index().\
        drop(columns = ['level_0', 'level_1'])


    headcounts_country_wide = headcounts_country.pivot_table(index=['entity', 'reporting_year','reporting_level','welfare_type'], 
                    columns='poverty line')


    headcounts_region_wide = headcounts_region.pivot_table(index=['entity', 'reporting_year'], 
                    columns='poverty line')


    headcounts_country_wide.columns = [''.join(col).strip() for col in headcounts_country_wide.columns.values]
    headcounts_country_wide = headcounts_country_wide.reset_index()

    headcounts_region_wide.columns = [''.join(col).strip() for col in headcounts_region_wide.columns.values]
    headcounts_region_wide = headcounts_region_wide.reset_index()

    # Add NAN columns for reporting_level and welfare_type in the region data, before appending to country data
    # (I'm sure there must be a way to append even though you don't have all the columns in both datasets but I haven't worked it out yet)
    headcounts_region_wide['reporting_level'] = np.NaN
    headcounts_region_wide['welfare_type'] = np.NaN

    df_final = headcounts_country_wide.append(headcounts_region_wide, ignore_index=False)


    # TO DO: Calculate numbers in poverty between pov lines for stacked area charts
    # I started with this below, but I haven't finished it.
    #Make sure the poverty lines are in order, lowest to highest
    # poverty_lines_cents.sort()

    # # for the lowest poverty line, we set a temporary var equal to the headcount 
    # lower_varname<- f'number_below_{poverty_lines_cents[0]}
    
    # df_final[lower_varname] = df_final[f'headcount_{poverty_lines_cents[0]}']


    # for i in range(1,len(poverty_lines_cents)-1):

  
    #     higher_varname<- f'number_below_{poverty_lines_cents[i]}'
    #     lower_varname<- f'number_below_{poverty_lines_cents[i-1]}'

    #     # Calculate the in between share

    #     df_final[lower_varname] = df_final[f'headcount_{poverty_lines_cents[0]}']


    # Standardize entity names
    standardize_enities(
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


    # Separate out consumption-only, income-only, and both dataframes
    df_inc_only = df_final.copy()
    df_inc_only = df_inc_only[df_inc_only['welfare_type']=="income"]

    df_cons_only = df_final.copy()
    df_cons_only = df_cons_only[df_cons_only['welfare_type']=="consumption"]

    df_inc_or_cons = df_final.copy()
    # If both inc and cons are available in a given year, drop inc

    # Flag duplicates – indicating multiple welfare_types
    df_inc_or_cons['duplicate_flag'] = df_inc_or_cons\
        .duplicated(subset=['entity', 'year', 'reporting_level'])

    print(f'Checking the filled = {is_filled} data for years with both income and consumption. Before dropping duplicated, there were {df_inc_or_cons.shape[0]} rows...')
    # Drop income where income and consumption are available
    df_inc_or_cons = df_inc_or_cons[(df_inc_or_cons['duplicate_flag']==False) | (df_inc_or_cons['welfare_type']=='consumption')]
    
    print(f'After dropping duplicates there were {df_inc_or_cons.shape[0]} rows.')


    # I think better would be to save this to s3 – but I don't know how to format the url from 
    # digital ocean so that the data can be picked up in the explorer. But I know how to do this
    # if it's stored in GitHub. So for now I write it as csvs to this folder.
    # Save as csv
    df_inc_only.to_csv(f'data/poverty_inc_only_filled_{is_filled}.csv', index=False)
    df_cons_only.to_csv(f'data/poverty_cons_only_filled_{is_filled}.csv', index=False)
    df_inc_or_cons.to_csv(f'data/poverty_inc_or_cons_filled_{is_filled}.csv', index=False)



    # 
    # upload_to_s3(df_inc_only, 
    #             'PIP', 
    #             f'poverty_inc_only_filled_{is_filled}.csv')

    # upload_to_s3(df_cons_only, 
    #             'PIP', 
    #             f'poverty_cons_only_filled_{is_filled}.csv')

    # upload_to_s3(df_inc_or_cons, 
    #             'PIP', 
    #             f'poverty_inc_or_cons_filled_{is_filled}.csv')

# %%
