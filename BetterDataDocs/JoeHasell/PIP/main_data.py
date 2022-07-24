#%%
import pandas as pd
import numpy as np

from PIP_API_query import pip_query_country, pip_query_region
from standardize_entities import standardize_enities
from functions import upload_to_s3

# function for multiplying by 100
def multiply_by_100(number):
            return 100 * number

poverty_lines_cents = [100, 190, 320, 550, 1000, 1500, 2000, 3000, 4000]
poverty_lines_cents = [100, 190]

#%%

headcount_dfs = {}
headcount_dfs['filled_true'] = {}
headcount_dfs['filled_false'] = {}
headcount_dfs['filled_true']['country'] = {}
headcount_dfs['filled_true']['region'] = {}

headcount_dfs['filled_false']['country'] = {}
headcount_dfs['filled_false']['region'] = {}


for p in poverty_lines_cents:

    p_dollar = p/100

    for is_filled in ['true', 'false']:
    
        for ent_type in ['country', 'region']:

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
            
            # This runs for both is_filled= true and false, 
            # even though it yields the same values each time 
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


            # Add poverty line as a var

            df['poverty line'] = f'_{p}'

            #Add dataframe to rolling dictionary.

            headcount_dfs[f'filled_{is_filled}'][ent_type][p] = df


#%%
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
    headcounts_region_wide['reporting_level'] = np.NaN
    headcounts_region_wide['welfare_type'] = np.NaN

    df_final = headcounts_country_wide.append(headcounts_region_wide, ignore_index=False)


    # TO DO: Calculate numbers in poverty between pov lines for stacked area charts
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
    df_final = df_final.rename(columns={'reporting_year': 'Year',
                                        "entity": "Entity"})


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


    # Save as csv
    df_inc_only.to_csv(f'data/poverty_inc_only_filled_{is_filled}.csv')
    df_cons_only.to_csv(f'data/poverty_cons_only_filled_{is_filled}.csv')
    df_inc_or_cons.to_csv(f'data/poverty_inc_or_cons_filled_{is_filled}.csv')


    # I was saving this to s3 – but I don't know how to format the url from digital ocean so that the data can be picked up in the explorer
    # upload_to_s3(df_inc_only, 
    #             'PIP', 
    #             f'poverty_inc_only_filled_{is_filled}.csv')

    # upload_to_s3(df_cons_only, 
    #             'PIP', 
    #             f'poverty_cons_only_filled_{is_filled}.csv')

    # upload_to_s3(df_inc_or_cons, 
    #             'PIP', 
    #             f'poverty_inc_or_cons_filled_{is_filled}.csv')

#%%