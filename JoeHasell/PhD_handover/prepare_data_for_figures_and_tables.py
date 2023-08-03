

#%%

from plotnine import *
import plotly.express as px
import pandas as pd
import numpy as np
# from IPython.display import display, HTML, IFrame, Markdown
# import dataframe_image as dfi
# import imgkit

from data_appendix.G_functions_for_figures_and_tables import * 

# pd.set_option('display.max_rows', None)


#%%
fp = 'data_appendix/data/clean/pip.csv'
        
df_pip = pd.read_csv(fp)


fp = 'data_appendix/data/clean/wid.csv'

df_wid = pd.read_csv(fp)

fp = 'data_appendix/data/clean/lis.csv'

df_lis = pd.read_csv(fp)


fp = 'data_appendix/data/clean/region_mapping.csv'

df_regions = pd.read_csv(fp)


fp = 'data_appendix/data/clean/population.csv'

df_pop = pd.read_csv(fp)

fp = 'data_appendix/data/clean/region_population.csv'

df_pop_regions = pd.read_csv(fp)


# Gather data into dictionary
source_dfs = {
    "PIP": df_pip,
    "WID": df_wid,
    "LIS": df_lis
    }


# This specifies the +/- for the 'stable' category in the tables below
tolerance_lookup =  {
                'var_search_term': [
                    'Gini',
                    'Top 1pc share', 
                    'Top 10pc share',
                    'Bottom 50pc share',
                    "Ratio Top 10 Bottom 50 share"],
                'var_tolerance': [
                    2,
                    1,
                    2,
                    1,
                    10
                ], 
                'relative_tolerance': [
                    0.05
                ]
            }

#%%

selected_vars_no_top1 = [
        'PIP: Gini',
        "PIP: Top 10pc share",
        'PIP: Bottom 50pc share',
        'PIP: Ratio Top 10 Bottom 50 share',
        'WID: Gini – pretax',
        "WID: Top 10pc share – pretax",
        'WID: Bottom 50pc share – pretax',
        'WID: Ratio Top 10 Bottom 50 share – pretax'
        ]

selected_vars_top1 = [
        'PIP: Top 1pc share',
        "WID: Top 1pc share – pretax"
        ]


   
#%%
#Prep data for 1993-2015 period


def prep_shorter_period_data_no_top1():
    reference_vals = [1993, 2015]
    max_dist_from_refs = 3



    prepped_data_dict = prep_data(
        source_dfs = source_dfs,
        df_pop = df_pop,
        df_regions = df_regions,
        region_col = 'region',
        selected_vars = selected_vars_no_top1,
        reference_vals = reference_vals,
        max_dist_from_refs = max_dist_from_refs,
        min_dist_between = 1,
        reference_col = "Year",
        group_by_col = "Entity",
        tolerance_lookup =  tolerance_lookup,
        outlier_cut_off_upper = None
        )


    owid_format = prepped_data_to_owid_format(
        prepped_data_all_obs = prepped_data_dict['all_obs'],
        prepped_data_matching_obs = prepped_data_dict['matching_obs'],
        reference_vals = reference_vals
        )
    owid_format

    # # 
    # Save data to be uploaded to OWID to make charts
    fp = 'data_appendix/figures_and_tables/Compare WID and PIP inequality data 1993 vs 2015 (Joe temp).csv'

    owid_format.to_csv(fp, index=False)

    return prepped_data_dict


def prep_shorter_period_data_top1():
    reference_vals = [1993, 2015]
    max_dist_from_refs = 3



    prepped_data_dict = prep_data(
        source_dfs = source_dfs,
        df_pop = df_pop,
        df_regions = df_regions,
        region_col = 'region',
        selected_vars = selected_vars_top1,
        reference_vals = reference_vals,
        max_dist_from_refs = max_dist_from_refs,
        min_dist_between = 1,
        reference_col = "Year",
        group_by_col = "Entity",
        tolerance_lookup =  tolerance_lookup,
        outlier_cut_off_upper = None
        )


    owid_format = prepped_data_to_owid_format(
        prepped_data_all_obs = prepped_data_dict['all_obs'],
        prepped_data_matching_obs = prepped_data_dict['matching_obs'],
        reference_vals = reference_vals
        )
    owid_format

    # # 
    # Save data to be uploaded to OWID to make charts
    fp = 'data_appendix/figures_and_tables/Compare WID and PIP Top 1% share 1993 vs 2015 (Joe temp).csv'

    owid_format.to_csv(fp, index=False)

    return prepped_data_dict

#%%
# Prep data for 1980-2018 period


def prep_longer_period_data_no_top1():

    reference_vals = [1980, 2018]
    max_dist_from_refs = 5



    prepped_data_dict = prep_data(
        source_dfs = source_dfs,
        df_pop = df_pop,
        df_regions = df_regions,
        region_col = 'region',
        selected_vars = selected_vars_no_top1,
        reference_vals = reference_vals,
        max_dist_from_refs = max_dist_from_refs,
        min_dist_between = 1,
        reference_col = "Year",
        group_by_col = "Entity",
        tolerance_lookup =  tolerance_lookup,
        outlier_cut_off_upper = None
        )


    owid_format = prepped_data_to_owid_format(
        prepped_data_all_obs = prepped_data_dict['all_obs'],
        prepped_data_matching_obs = prepped_data_dict['matching_obs'],
        reference_vals = reference_vals
        )

    # # 
    # Save data to be uploaded to OWID to make charts
    fp = 'data_appendix/figures_and_tables/Compare WID and PIP inequality data 1980 vs 2018 (Joe temp).csv'

    owid_format.to_csv(fp, index=False)

    return prepped_data_dict



def prep_longer_period_data_top1():

    reference_vals = [1980, 2018]
    max_dist_from_refs = 5



    prepped_data_dict = prep_data(
        source_dfs = source_dfs,
        df_pop = df_pop,
        df_regions = df_regions,
        region_col = 'region',
        selected_vars = selected_vars_top1,
        reference_vals = reference_vals,
        max_dist_from_refs = max_dist_from_refs,
        min_dist_between = 1,
        reference_col = "Year",
        group_by_col = "Entity",
        tolerance_lookup =  tolerance_lookup,
        outlier_cut_off_upper = None
        )


    owid_format = prepped_data_to_owid_format(
        prepped_data_all_obs = prepped_data_dict['all_obs'],
        prepped_data_matching_obs = prepped_data_dict['matching_obs'],
        reference_vals = reference_vals
        )

    # # 
    # Save data to be uploaded to OWID to make charts
    fp = 'data_appendix/figures_and_tables/Compare WID and PIP Top 1% share 1980 vs 2018 (Joe temp).csv'

    owid_format.to_csv(fp, index=False)

    return prepped_data_dict



#%%
def adjust_averages_summary_for_multiple_indices(df_summary,reference_vals):
    df_summary = df_summary.stack(level=0).loc['World']

    df_summary = df_summary.loc[:, df_summary.columns.get_level_values(0) != 'Pop. coverage']


    df_summary[(('Avg', 'Change (pt.)'))] = pd.to_numeric(df_summary[('Avg', int(f'{reference_vals[1]}'))]) - pd.to_numeric(df_summary[('Avg', int(f'{reference_vals[0]}'))])

    df_summary[(('Wt. avg', 'Change (pt.)'))] = pd.to_numeric(df_summary[('Wt. avg', int(f'{reference_vals[1]}'))]) - pd.to_numeric(df_summary[('Wt. avg', int(f'{reference_vals[0]}'))])

    df_summary[(('Avg', 'Change (%)'))] = (pd.to_numeric(df_summary[('Avg', int(f'{reference_vals[1]}'))]) - pd.to_numeric(df_summary[('Avg', int(f'{reference_vals[0]}'))]))/pd.to_numeric(df_summary[('Avg', int(f'{reference_vals[0]}'))])*100

    df_summary[(('Avg', 'Change (%)'))] = df_summary[(('Avg', 'Change (%)'))].round(1)

    df_summary[(('Wt. avg', 'Change (%)'))] = (pd.to_numeric(df_summary[('Wt. avg', int(f'{reference_vals[1]}'))]) - pd.to_numeric(df_summary[('Wt. avg', int(f'{reference_vals[0]}'))]))/pd.to_numeric(df_summary[('Wt. avg', int(f'{reference_vals[0]}'))])*100

    df_summary[(('Wt. avg', 'Change (%)'))] = df_summary[(('Wt. avg', 'Change (%)'))].round(1)

    sorted_cols = sorted(df_summary.columns, key=lambda x: x[0])
    df_summary = df_summary.loc[:, sorted_cols]



    # rename vars
    new_index = df_summary.index.str.replace('Ratio Top 10 Bottom 50 share','Top 10%/Bottom 50% share')
    new_index = new_index.str.replace('pc','%')
    new_index = new_index.str.replace(' – pretax','')
    new_index = new_index.str.replace('WID','WID (pretax)')

    df_summary.index = new_index


    # Split source from var into two indexes
    new_index = df_summary.index.str.split(': ', expand=True)
    df_summary.index = new_index


    # Shift the column index of the two average twpes to be a row index
    df_summary = df_summary.stack(level=0).sort_index()

    # Shift the source to be a column index
    df_summary = df_summary.unstack(level=0).stack(level=0).unstack(level=2)



    return df_summary



#%%
def adjust_relative_counts_summary_for_multiple_indices(df_summary,reference_vals):
    
    df_summary = df_summary.stack(level=0).loc['World']


    # df_summary[(('Avg', 'Change (pt.)'))] = pd.to_numeric(df_summary[('Avg', int(f'{reference_vals[1]}'))]) - pd.to_numeric(df_summary[('Avg', int(f'{reference_vals[0]}'))])

    # df_summary[(('Wt. avg', 'Change (pt.)'))] = pd.to_numeric(df_summary[('Wt. avg', int(f'{reference_vals[1]}'))]) - pd.to_numeric(df_summary[('Wt. avg', int(f'{reference_vals[0]}'))])

    # df_summary[(('Avg', 'Change (%)'))] = (pd.to_numeric(df_summary[('Avg', int(f'{reference_vals[1]}'))]) - pd.to_numeric(df_summary[('Avg', int(f'{reference_vals[0]}'))]))/pd.to_numeric(df_summary[('Avg', int(f'{reference_vals[0]}'))])*100

    # df_summary[(('Avg', 'Change (%)'))] = df_summary[(('Avg', 'Change (%)'))].round(1)

    # df_summary[(('Wt. avg', 'Change (%)'))] = (pd.to_numeric(df_summary[('Wt. avg', int(f'{reference_vals[1]}'))]) - pd.to_numeric(df_summary[('Wt. avg', int(f'{reference_vals[0]}'))]))/pd.to_numeric(df_summary[('Wt. avg', int(f'{reference_vals[0]}'))])*100

    # df_summary[(('Wt. avg', 'Change (%)'))] = df_summary[(('Wt. avg', 'Change (%)'))].round(1)

    # sorted_cols = sorted(df_summary.columns, key=lambda x: x[0])
    




    # rename vars
    new_index = df_summary.index.str.replace('Ratio Top 10 Bottom 50 share','Top 10%/Bottom 50% share')
    new_index = new_index.str.replace('pc','%')
    new_index = new_index.str.replace(' – pretax','')
    new_index = new_index.str.replace('WID','WID (pretax)')

    df_summary.index = new_index


    # Split source from var into two indexes
    new_index = df_summary.index.str.split(': ', expand=True)
    df_summary.index = new_index

    # Shift the source to be a column index
    df_summary = df_summary.unstack(level=0).stack(level=0).unstack(level=1)

    return df_summary




#%%
# #Make coverage charts
#%%


data_to_check = {
    'Source': ['PIP', 'WID'],
    'Metric': ['Gini', 'Top 1pc share – pretax'],
    'df': [df_pip, df_wid]
    }


df_coverage_3_years = pd.DataFrame()


max_dist_from_ref = 3


for yr in range(1960, 2023):

    for i in [0,1]:

        matched_data = closest_to_reference(
            df=data_to_check['df'][i], 
            reference_val = yr, 
            max_dist_from_ref = max_dist_from_ref, 
            reference_col = 'Year', 
            group_by_col = 'Entity', 
            value_col = data_to_check['Metric'][i], 
            tie_break = 'above')

        df_pop_ref_year = df_pop[df_pop['Year']==yr].drop(columns=['Year', 'population'])

        matched_data = matched_data.merge(df_pop_ref_year, how='left')

        coverage_yr = pd.DataFrame({
            'Year': [yr],
            'No. of countries': [matched_data['world_pop_share'].count()],
            'Share of World population': [matched_data['world_pop_share'].sum()]
        })
        
        source = data_to_check['Source'][i]
        metric = data_to_check['Metric'][i]
        coverage_yr['Data'] = f'{source} – {metric}'

        df_coverage_3_years = pd.concat([df_coverage_3_years, coverage_yr])
        
#%%

df_coverage_5_years = pd.DataFrame()

data_to_check = {
    'Source': ['PIP', 'WID'],
    'Metric': ['Gini', 'Top 1pc share – pretax'],
    'df': [df_pip, df_wid]
    }

max_dist_from_ref = 5


for yr in range(1960, 2023):

    for i in [0,1]:

        matched_data = closest_to_reference(
            df=data_to_check['df'][i], 
            reference_val = yr, 
            max_dist_from_ref = max_dist_from_ref, 
            reference_col = 'Year', 
            group_by_col = 'Entity', 
            value_col = data_to_check['Metric'][i], 
            tie_break = 'above')

        df_pop_ref_year = df_pop[df_pop['Year']==yr].drop(columns=['Year', 'population'])

        matched_data = matched_data.merge(df_pop_ref_year, how='left')

        coverage_yr = pd.DataFrame({
            'Year': [yr],
            'No. of countries': [matched_data['world_pop_share'].count()],
            'Share of World population': [matched_data['world_pop_share'].sum()]
        })
        
        source = data_to_check['Source'][i]
        metric = data_to_check['Metric'][i]
        coverage_yr['Data'] = f'{source} – {metric}'

        df_coverage_5_years = pd.concat([df_coverage_5_years, coverage_yr])
        
#%%



fig = px.line(df_coverage_3_years, x="Year", y="No. of countries", color='Data')

fig.update_layout(
    title = f'Number of countries with data – within 3 years',
    legend_title="",
    legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
))

fig.write_image("images/coverage_number_countries_3_years.png")
        

#%%

fig = px.line(df_coverage_5_years, x="Year", y="No. of countries", color='Data')

fig.update_layout(
    title = f'Number of countries with data – within 5 years',
    legend_title="",
    legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
))

fig.write_image("images/coverage_number_countries_5_years.png")
        
#%%

fig = px.line(df_coverage_3_years, x="Year", y="Share of World population", color='Data')

fig.update_layout(
    title = f'Population coverage – within 3 years',
    legend_title="",
    legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
))

fig.write_image("images/coverage_population_3_years.png")
        

#%%

fig = px.line(df_coverage_5_years, x="Year", y="Share of World population", color='Data')

fig.update_layout(
    title = f'Population coverage – within 5 years',
    legend_title="",
    legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
))

fig.write_image("images/coverage_population_5_years.png")
        

#%%
def prep_counts_and_counterfactuals(
    selected_vars,
    summary_tables_dict
    ):
    all_metrics_requirement_types = ['all_obs', 'matching_obs']

    var_level_dict = {}

    for var in selected_vars:

        obs_level_dict = {}

        for obs_requirement in all_metrics_requirement_types:


            df = summary_tables_dict[obs_requirement]['relative_counts']

            df = df.loc[('World', ), (var, )]

            df.iloc[0] = pd.to_numeric(df.iloc[0])

            percentages = (df.iloc[0] / df.iloc[0, -1]) * 100
            df.loc[1] = percentages

            df.index = ['No. countries', 'Share of countries']

            obs_level_dict[obs_requirement] = df


        concatenated = pd.concat(obs_level_dict)
        
        var_level_dict[var] = concatenated


    df1 = var_level_dict[selected_vars[0]]
    df2 = var_level_dict[selected_vars[1]]


    # Add cols to df1
    difference = df1.iloc[0] + df2.iloc[0] - df2.iloc[2]

    new_row = pd.DataFrame(difference).T
    new_row.index = pd.MultiIndex.from_tuples([('Counterfactual 1', 'No. countries')])
    df1 = pd.concat([df1,new_row])
    percentages = (df1.loc[('Counterfactual 1', 'No. countries')] / df1.loc[('Counterfactual 1', 'No. countries'), 'total']) * 100
    new_row = pd.DataFrame(percentages).T
    new_row.index = pd.MultiIndex.from_tuples([('Counterfactual 1', 'Share of countries')])
    df1 = pd.concat([df1,new_row])

    
    # Add cols to df2
    difference = df2.iloc[0] + df1.iloc[0] - df1.iloc[2]

    new_row = pd.DataFrame(difference).T
    new_row.index = pd.MultiIndex.from_tuples([('Counterfactual 1', 'No. countries')])
    df2 = pd.concat([df2,new_row])
    percentages = (df2.loc[('Counterfactual 1', 'No. countries')] / df2.loc[('Counterfactual 1', 'No. countries'), 'total']) * 100
    new_row = pd.DataFrame(percentages).T
    new_row.index = pd.MultiIndex.from_tuples([('Counterfactual 1', 'Share of countries')])
    df2 = pd.concat([df2,new_row])

    df = pd.concat([df1,df2], axis =1, keys = selected_vars)


    # select 'Share of countries' rows
    mask = df.index.get_level_values(0) == 'Share of countries'
    share_of_countries = df.loc[mask]

    # define formatting function
    def format_share(val):
        return '{:.1f}'.format(val)

    # apply formatting function to selected rows
    df.loc[mask] = share_of_countries.applymap(format_share)

    # df[('all_obs', 'Share of countries')] = df[('all_obs', 'Share of countries')] .map('{:.1f}'.format)
    # df[('Counterfactual 1', 'Share of countries')] = df[('Counterfactual 1', 'Share of countries')] .map('{:.1f}'.format)

    return df