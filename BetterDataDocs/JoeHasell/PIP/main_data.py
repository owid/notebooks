#%%
import pandas as pd
import numpy as np

from PIP_API_query import pip_query_country, pip_query_region

# function for multiplying by 100
def multiply_by_100(number):
            return 100 * number

poverty_lines_cents = [100, 190, 320, 550, 1000, 2000, 3000, 4000]
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

    df_final.loc[(\
        df_final['reporting_level'].isin(["urban", "rural"])),'entity'] = \
        df_final.loc[(\
        df_final['reporting_level'].isin(["urban", "rural"])),'entity'] + \
            ' - ' + \
        df_final.loc[(\
        df_final['reporting_level'].isin(["urban", "rural"])),'reporting_level']

    # Write filled and survey data to csv
    df_final.to_csv(f'data/poverty_vars_filled_{is_filled}.csv')



#%%