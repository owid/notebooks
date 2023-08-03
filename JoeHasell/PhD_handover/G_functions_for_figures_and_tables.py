
# %%


from plotnine import *
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import math

# %% [markdown]
#  This function grabs the observation nearest to a reference value of a particular column (e.g. a reference year). A parameter specifies how to break ties where a value greater and lower than the reference values are the equidistant closest values.
#  %
#   Function to get matching observation closest to ref year
#  Drop NAs
#  Calculate absolute distance from reference value
#  Drop any rows with a distance beyond threshold
#  Keep closest observation to reference value – including tie-breaks (where there is a match above and below the ref value)
#  Settle tie-breaks

# %%
#  Function to get matching observation closest to ref year
def closest_to_reference(
    df, 
    reference_val, 
    max_dist_from_ref, 
    reference_col, 
    group_by_col, 
    value_col, 
    tie_break):
  
  df = df.loc[:, [reference_col, group_by_col, value_col]]

  # Drop NAs
  df = df.dropna()

  # Calculate absolute distance from reference value
  df['ref_diff'] = abs(df[reference_col] - reference_val)

  # Drop any rows with a distance beyond threshold
  if not pd.isna(max_dist_from_ref):
    df = df.loc[df['ref_diff'] <= max_dist_from_ref]

  # Keep closest observation to reference value – including tie-breaks (where there is a match above and below the ref value)
  df = df[df.groupby(group_by_col)['ref_diff'].transform('min') == df['ref_diff']].reset_index(drop=True)

  # Settle tie-breaks
  if tie_break == 'below':
    df = df[df.groupby(group_by_col)[reference_col].transform('min') == df[reference_col]].reset_index(drop=True)
    
  elif tie_break == 'above':
    df = df[df.groupby(group_by_col)[reference_col].transform('max') == df[reference_col]].reset_index(drop=True)

  df = df.drop('ref_diff', axis=1)

  df = df\
    .rename(columns={value_col: "value"})


  return df

# %% [markdown]
#  This function uses the `closest_to_reference` function to find the closest observations for a *pair* of reference values (e.g. 1990 and 2018).

# %%
# Generate matches for two reference years and merge
def merge_two_ref_matches(
    df, 
    reference_vals, 
    max_dist_from_refs, 
    min_dist_between, 
    reference_col, 
    group_by_col, 
    value_col):

# Make sure the pair of reference values are in ascending order
  reference_vals.sort()

# Maximise distance between two refs by settling tie-breaks below the lowest ref and above the highest ref 

# Find matches for lower reference value
  lower_ref_matches = closest_to_reference(df, reference_vals[0], max_dist_from_refs, reference_col, group_by_col, value_col, 'below')

# Find matches for higher reference value
  higher_ref_matches = closest_to_reference(df, reference_vals[1], max_dist_from_refs, reference_col, group_by_col, value_col, 'above')

# Merge the two sets of matches
  merged_df = pd.merge(lower_ref_matches, higher_ref_matches, on=group_by_col, suffixes=(reference_vals[0], reference_vals[1]))

# Drop obs that do not have data for both ref values
  merged_df = merged_df.dropna()

# Drop obs where the matched data does not meet the min distance requirement
  if not pd.isna(min_dist_between):
  
  # Store the names of the reference column returned from the two matches
    ref_var_high = f'{reference_col}{reference_vals[1]}'
    ref_var_low = f'{reference_col}{reference_vals[0]}'

  # Keep only rows >= to the min distance
    merged_df = merged_df.loc[(merged_df[ref_var_high] - merged_df[ref_var_low]) >= min_dist_between, :]



  return merged_df




# %% [markdown]
#  The following function runs the `merge_two_ref_matches` function, but adjusts thing somewhat for the PIP data – to handle the mix of income and consumption data there. It gives priority to matched pairs of *income* observations, and then matched pairs of *consumption* observations. If there are no such matches, it allows for matches where the welfare concept differs.

# %%
def pip_welfare_routine(df, reference_vals, max_dist_from_refs, min_dist_between, reference_col, group_by_col, value_col):

  # Specify the name of the column in which the income/consumption welfare definition is stored
  welfare_colname = 'welfare_type'

  # Creat dataframes for thee scenarios:
  # Scenario 1: only allow income data
  df_inc_filter = df.loc[df[welfare_colname] == "income", :]
  df_inc_filter.name = "Income"

  # Scenario 2: only allow consumption data
  df_cons_filter = df.loc[df[welfare_colname] == "consumption", :]
  df_cons_filter.name = "Consumption"
  # Scenario 3: allow a mix – dropping consumption data where income data is available in the same year
  df_mixed = df.copy()

  df_mixed['welfare_count'] = df_mixed.groupby([reference_col, group_by_col])[welfare_colname].transform('count')

  df_mixed = df_mixed.loc[(df_mixed['welfare_count'] == 1) | (df_mixed[welfare_colname] == "income")]

  df_mixed.name = "Mixed"
  #  Store the scneario dataframes in a list
  df_scenarios = [df_inc_filter, df_cons_filter, df_mixed]

  # Run the matching function on each scenario
  scenario_matches = [merge_two_ref_matches(
    df_scenario, 
    reference_vals, 
    max_dist_from_refs, 
    min_dist_between, 
    reference_col, 
    group_by_col, 
    value_col) for df_scenario in df_scenarios]
  
  # Combine the first two scenarios.
  df_combined_matches = pd.concat([scenario_matches[0], scenario_matches[1]], keys=[df_scenarios[0].name, df_scenarios[1].name])

  # Tidy up indexes
  df_combined_matches = df_combined_matches.reset_index()
  
  df_combined_matches = df_combined_matches.drop('level_1', axis=1)

  df_combined_matches = df_combined_matches\
    .rename(columns={"level_0": "pip_welfare"})

  # Add in third scenario.
  df_combined_matches = pd.concat([df_combined_matches, scenario_matches[2]])

  # add scenario name to te pip_welfare column
  df_combined_matches['pip_welfare'] = df_combined_matches['pip_welfare'].fillna(df_scenarios[2].name)

  # Keep only one match per group (e.g. per Country) - in the priority laid out in the df_scenarios list above (income only -> consumption only -> mixed)
    # First count the matches
  df_combined_matches['match_count'] = df_combined_matches.groupby(group_by_col)['pip_welfare'].transform('count')
    # Then drop any matches from the lowest priority where there are multiple matches
  df_combined_matches = df_combined_matches.loc[(df_combined_matches['match_count']==1) | ~(df_combined_matches['pip_welfare']==df_scenarios[2].name)]
    #  Repeat at the next level of priority
  df_combined_matches['match_count'] = df_combined_matches.groupby(group_by_col)['pip_welfare'].transform('count')
  df_combined_matches = df_combined_matches.loc[(df_combined_matches['match_count']==1) | ~(df_combined_matches['pip_welfare']==df_scenarios[1].name)]
  
  # Drop the match count column
  df_combined_matches = df_combined_matches.drop('match_count', axis=1)


  return df_combined_matches



# %% [markdown]
#  This function is used to transform the names of data columns in different scenarios. It splits a list of strings in the format 'source: ineq_metric' into a dictionary where the sources and ineq metrics are listed separately.

# %%
def prep_selected_vars(selected_vars):

    # selected_vars = [
    #   'LIS: Top 10pc share_equiv_market',
    #   'WID: Bottom 50pc share_posttax_dis',
    #   'PIP: Top 10pc share']

    sep = ": "

    selected_sources = [var.split(sep, 1)[0] for var in selected_vars]
    selected_var_names = [var.split(sep, 1)[1] for var in selected_vars]


    match_data = {
        "sources": selected_sources,
        "var_names": selected_var_names
            }


    return match_data




# %% [markdown]
#  This is the main function that prepares the ref-year matched data – builiding on the functions above.
#  The first argument is a dictionary of data frames where the keys are the source name.
#  The 2nd and 3rd arguments are population data and region classifications.
#  The `tolerance_lookup` is a dictionary of lists that specify search terms in the name of the inequality indicator, and the 'tolerance' that should be applied when categorising whether a change in the indicator between the reference years was significant or not (i.e. +/- 1 point change).

# %%
def prep_data(
      source_dfs,
      df_pop,
      df_regions,
      region_col,
      selected_vars,
      reference_vals,
      max_dist_from_refs,
      min_dist_between,
      reference_col = "Year",
      group_by_col = "Entity",
      tolerance_lookup =  {
                'var_search_term': [
                    'Gini',
                    'Top 1pc share', 
                    'Top 10pc share',
                    'Bottom 50pc share'],
                'var_tolerance': [
                    1,
                    1,
                    1,
                    1
                ]
            },
      outlier_cut_off_upper = None):


    selected_source_var_dict = prep_selected_vars(selected_vars)

    prepped_data_dict = {}

    for obs_requirement in ['all_obs', 'matching_obs']:

      if obs_requirement == 'all_obs':
        all_metrics_requirement = False
      if obs_requirement == 'matching_obs':
        all_metrics_requirement = True

      matches = []

      for i in range(len(selected_source_var_dict['sources'])):
          
          source = selected_source_var_dict["sources"][i]
          var = selected_source_var_dict["var_names"][i]

          

          df = source_dfs[source]

          if source == "PIP":

              matched = pip_welfare_routine(
                  df = df,
                  reference_vals = reference_vals,
                  max_dist_from_refs = max_dist_from_refs,
                  min_dist_between = min_dist_between,
                  reference_col = reference_col,
                  group_by_col = group_by_col,
                  value_col = var
                  )

          else:

              matched = merge_two_ref_matches(
                  df = df,
                  reference_vals = reference_vals,
                  max_dist_from_refs = max_dist_from_refs,
                  min_dist_between = min_dist_between,
                  reference_col = reference_col,
                  group_by_col = group_by_col,
                  value_col = var
                  )

          matches.append(matched)


      prepped_data = pd.concat(matches, keys=selected_vars)

      # Tidy up indexes
      prepped_data = prepped_data.reset_index()
      
      prepped_data = prepped_data.drop('level_1', axis=1)

      prepped_data = prepped_data\
          .rename(columns={"level_0": "source_var"})




      # Store the names of the columns to be used onthe X and Y axis
      x_axis = f'value{reference_vals[0]}'
      y_axis = f'value{reference_vals[1]}'



      # Apply outlier cut off, if specified
      if not pd.isna(outlier_cut_off_upper):
          prepped_data = prepped_data.loc[prepped_data[x_axis] <= outlier_cut_off_upper]
          prepped_data = prepped_data.loc[prepped_data[y_axis] <= outlier_cut_off_upper]


      # Add a count by country – counting whether data is available from each source or not
      prepped_data['source_count'] = prepped_data.groupby(group_by_col)['source_var'].transform('count')


      # Apply metrics requirement (whether to include only observations with data from all metrics)
      if all_metrics_requirement:
          prepped_data = prepped_data.loc[prepped_data['source_count'] == prepped_data['source_count'].max()]

      # Drop source_count column
      prepped_data = prepped_data.drop('source_count', axis=1)

      # Add in region classification
      df_regions = df_regions[[group_by_col, region_col]]
      prepped_data = pd.merge(prepped_data, df_regions, how = 'left')

      # Add in population data
          # For first ref
      df_pop_ref = df_pop.loc[df_pop['Year'] == reference_vals[0], ['Entity', 'population'] ]

      prepped_data = pd.merge(prepped_data, df_pop_ref, how = 'left')

      prepped_data = prepped_data.rename(columns={'population':f'pop{reference_vals[0]}'})

          # For second ref
      df_pop_ref = df_pop.loc[df_pop['Year'] == reference_vals[1], ['Entity', 'population'] ]

      prepped_data = pd.merge(prepped_data, df_pop_ref, how = 'left')

      prepped_data = prepped_data.rename(columns={'population':f'pop{reference_vals[1]}'})




      # Calculate the change between the two ref periods
      prepped_data['change'] = (prepped_data[f'value{reference_vals[1]}'] - prepped_data[f'value{reference_vals[0]}'])


      # ABSOLUTE TOLERANCE: 
      # Add a tolerance column – the change the demarks a substnatial rise or fall.
      # Here this is measured in terms of absolute change.
      # It uses a dictionary passed as an argument to this function to
      # search for vars with particualr strings ('Gini') and the sub in
      # the tolerance specified in the dictionary
      for i in range(len(tolerance_lookup['var_search_term'])):

          prepped_data.loc[prepped_data['source_var']\
              .str.contains(
                  tolerance_lookup['var_search_term'][i]
                  ), 'absolute_tolerance'] = tolerance_lookup['var_tolerance'][i]


      # RELATIVE TOLERANCE: 
      # Add a tolerance column – the change the demarks a substnatial rise or fall.
      # Here this is measured in terms of relative change.
      # It uses a single value [0-1] irrespective of the variable.
      prepped_data['relative_tolerance'] = prepped_data[f'value{reference_vals[0]}'] * tolerance_lookup['relative_tolerance'][0]
      


      # Prepare fall/stable/rise categories 
      change_types = ['absolute', 'relative']
    
      for change_type in change_types:
        prepped_data[f'{change_type}_fall'] = prepped_data['change'] < -prepped_data[f'{change_type}_tolerance']

        prepped_data[f'{change_type}_stable'] = (prepped_data['change'] <= prepped_data[f'{change_type}_tolerance']) & (prepped_data['change'] >= -prepped_data[f'{change_type}_tolerance'])

        prepped_data[f'{change_type}_rise'] = prepped_data['change'] > prepped_data[f'{change_type}_tolerance']

        # Make sure the dichotomous vars are integers
        prepped_data[[f'{change_type}_fall', f'{change_type}_stable', f'{change_type}_rise']] = prepped_data[[f'{change_type}_fall', f'{change_type}_stable', f'{change_type}_rise']].astype(int)


      # Use a fixed name for the region column
      prepped_data = prepped_data.rename(columns={
        region_col:'region',
        group_by_col:'country',
        f'{reference_col}{reference_vals[0]}': f'year{reference_vals[0]}',
        f'{reference_col}{reference_vals[1]}': f'year{reference_vals[1]}'
        })

      prepped_data_dict[obs_requirement] = prepped_data
    
    return prepped_data_dict



# %%
def prepped_data_to_owid_format(
      prepped_data_all_obs,
      prepped_data_matching_obs,
      reference_vals
      ):

  step_1 = {}
  all_metrics_requirement_types = ['all_obs', 'matching_obs']

  for obs_requirement in all_metrics_requirement_types:

    if obs_requirement == 'all_obs':
      prepped_data = prepped_data_all_obs
    if obs_requirement == 'matching_obs':
      prepped_data = prepped_data_matching_obs

    # Reshape the data
    owid_format = pd.melt(prepped_data, id_vars=['source_var', 'country', 'region' ], value_vars=[f'year{reference_vals[0]}', f'year{reference_vals[1]}', f'value{reference_vals[0]}', f'value{reference_vals[1]}'])

    # Extract year and group information from variable column
    owid_format[['var', 'reference']] = owid_format['variable'].str.extract(r'(\D+)(\d+)$')
    owid_format['reference'] = owid_format['reference'].astype(int)

    #Reshape from long to wide
    owid_format=pd.pivot(owid_format, index=['source_var', 'country', 'region', 'reference' ], columns = 'var' ,values = 'value').reset_index() 

    # Drop the original reference column
    owid_format = owid_format.drop('reference', axis=1)

    # Pivot the melted dataframe wider – one value column per source_var
    owid_format = owid_format.pivot_table(index=['country', 'region', 'year'], columns='source_var', values='value').reset_index()

    step_1[obs_requirement] = owid_format

  # Merge the all_obs and matching_obs data for OWID format
  owid_format = pd.merge(step_1['all_obs'], step_1['matching_obs'], on=['country', 'year', 'region'], how='outer', suffixes=(' – all observations', ' – only matching observations'))


  # Reorder columns
  cols = list(owid_format.columns) # Get the list of column names
  cols.remove('country') # Remove col1 from the list
  cols.remove('year') # Remove col2 from the list
  cols = ['country', 'year'] + cols # Add col1 and col2 to the front of the list
  owid_format = owid_format[cols] # Reorder columns in the DataFrame

  owid_format['year'] = owid_format['year'].astype(int) # Year needs to be integer for OWID


  return(owid_format)








#%%
def prep_summary_tables(
      prepped_data_dict,
      df_pop_regions,
      selected_vars,
      reference_vals
      ):
  
  summary_tables_dict ={}

  all_metrics_requirement_types = ['all_obs', 'matching_obs']


  for obs_requirement in all_metrics_requirement_types:

    prepped_data = prepped_data_dict[obs_requirement]

    # Prepare pop-weighted averages for each ref year
    df_aggs = prepped_data.copy()

    df_aggs = df_aggs[df_aggs['source_var'].isin(selected_vars)]

     
    for ref in reference_vals:

      # Calulate regional pop weights, grouped by source-var 
      df_aggs[f'regional_pop_weights{ref}'] = df_aggs.groupby(['source_var', 'region'])[f'pop{ref}'].transform(lambda x: x/x.sum()) 

      # Calulate global pop weights, grouped by source-var
      df_aggs[f'global_pop_weights{ref}'] = df_aggs.groupby('source_var')[f'pop{ref}'].transform(lambda x: x/x.sum()) 

      # Multiply the values by the pop weights 
      df_aggs[f'region_weighted_value{ref}'] = df_aggs[f'value{ref}'] * df_aggs[f'regional_pop_weights{ref}']
      df_aggs[f'global_weighted_value{ref}'] = df_aggs[f'value{ref}'] * df_aggs[f'global_pop_weights{ref}']


    change_types = ['absolute', 'relative']
    cats = ['rise', 'stable', 'fall']

    for change_type in change_types:

      # Multiply change dummies by the regional and global pop weights – later we will sum these to get shares of rising and falling countries 
      for cat in cats:
        df_aggs[f'regional_pop_weights_{change_type}_{cat}'] = df_aggs[f'{change_type}_{cat}'] * df_aggs[f'regional_pop_weights{ref}']
        df_aggs[f'global_pop_weights_{change_type}_{cat}'] = df_aggs[f'{change_type}_{cat}'] * df_aggs[f'global_pop_weights{ref}']


    for change_type in change_types:
    
   

      # Summarise by region
      df_region_summary = df_aggs\
        .groupby(['source_var', 'region'])[[
            f'value{reference_vals[0]}',
            f'value{reference_vals[1]}',
            f'region_weighted_value{reference_vals[0]}',
            f'region_weighted_value{reference_vals[1]}',
            f'global_pop_weights{reference_vals[0]}', 
            f'global_pop_weights{reference_vals[1]}',
            f'pop{reference_vals[0]}',
            f'pop{reference_vals[1]}', 
            'absolute_fall', 
            'absolute_stable', 
            'absolute_rise',
            'relative_fall', 
            'relative_stable', 
            'relative_rise', 
            'regional_pop_weights_absolute_fall', 
            'regional_pop_weights_absolute_stable', 
            'regional_pop_weights_absolute_rise',
            'regional_pop_weights_relative_fall', 
            'regional_pop_weights_relative_stable', 
            'regional_pop_weights_relative_rise']]\
        .agg(['sum', 'mean', 'count'])


      df_region_summary = df_region_summary.loc[:, [
          (f'value{reference_vals[0]}', 'mean'),
          (f'value{reference_vals[1]}', 'mean'),
          (f'region_weighted_value{reference_vals[0]}', 'sum'),
          (f'region_weighted_value{reference_vals[1]}', 'sum'),
          ('absolute_fall', 'sum'),
          ('absolute_stable', 'sum'), 
          ('absolute_rise', 'sum'),
          ('relative_fall', 'sum'),
          ('relative_stable', 'sum'), 
          ('relative_rise', 'sum'),
          ('relative_rise', 'count'),
          ('regional_pop_weights_absolute_fall', 'sum'),
          ('regional_pop_weights_absolute_stable', 'sum'), 
          ('regional_pop_weights_absolute_rise', 'sum'),
          ('regional_pop_weights_relative_fall', 'sum'),
          ('regional_pop_weights_relative_stable', 'sum'), 
          ('regional_pop_weights_relative_rise', 'sum'),
          (f'global_pop_weights{reference_vals[0]}', 'sum'), 
          (f'global_pop_weights{reference_vals[1]}', 'sum'),
          (f'pop{reference_vals[0]}', 'sum'),
          (f'pop{reference_vals[1]}', 'sum')]]
    

    #  Define more helpful col names
      final_column_names =  [
          f'Avg {reference_vals[0]}',
          f'Avg {reference_vals[1]}',
          f'Wt. avg {reference_vals[0]}',
          f'Wt. avg {reference_vals[1]}',
          'absolute_fall',
          'absolute_stable',
          'absolute_rise',
          'relative_fall',
          'relative_stable',
          'relative_rise',
          'total',
          'share_absolute_fall',
          'share_absolute_stable',
          'share_absolute_rise',
          'share_relative_fall',
          'share_relative_stable',
          'share_relative_rise',
          f'Pop. weights {reference_vals[0]}',
          f'Pop. weights {reference_vals[1]}',
          f'Pop. sum {reference_vals[0]}',
          f'Pop. sum {reference_vals[1]}',        
      ]

      #  Sub in more helpful col names
      df_region_summary.columns = final_column_names


      # Summarise globally

      df_global_summary = df_aggs\
          .groupby(['source_var'])[[
              f'value{reference_vals[0]}',
              f'value{reference_vals[1]}',
              f'global_weighted_value{reference_vals[0]}',
              f'global_weighted_value{reference_vals[1]}',
              f'global_pop_weights{reference_vals[0]}', 
              f'global_pop_weights{reference_vals[1]}',
              f'pop{reference_vals[0]}',
              f'pop{reference_vals[1]}',  
              'absolute_fall', 
              'absolute_stable', 
              'absolute_rise',
              'relative_fall', 
              'relative_stable', 
              'relative_rise', 
              'global_pop_weights_absolute_fall', 
              'global_pop_weights_absolute_stable', 
              'global_pop_weights_absolute_rise',
              'global_pop_weights_relative_fall', 
              'global_pop_weights_relative_stable', 
              'global_pop_weights_relative_rise']]\
          .agg(['sum', 'mean', 'count'])


      df_global_summary = df_global_summary.loc[:, [
          (f'value{reference_vals[0]}', 'mean'),
          (f'value{reference_vals[1]}', 'mean'),
          (f'global_weighted_value{reference_vals[0]}', 'sum'),
          (f'global_weighted_value{reference_vals[1]}', 'sum'),
          ('absolute_fall', 'sum'),
          ('absolute_stable', 'sum'), 
          ('absolute_rise', 'sum'),
          ('relative_fall', 'sum'),
          ('relative_stable', 'sum'), 
          ('relative_rise', 'sum'),
          ('relative_rise', 'count'),
          ('global_pop_weights_absolute_fall', 'sum'),
          ('global_pop_weights_absolute_stable', 'sum'), 
          ('global_pop_weights_absolute_rise', 'sum'),
          ('global_pop_weights_relative_fall', 'sum'),
          ('global_pop_weights_relative_stable', 'sum'), 
          ('global_pop_weights_relative_rise', 'sum'),
          (f'global_pop_weights{reference_vals[0]}', 'sum'), 
          (f'global_pop_weights{reference_vals[1]}', 'sum'),
          (f'pop{reference_vals[0]}', 'sum'),
          (f'pop{reference_vals[1]}', 'sum')]]

      # Add 'World' region as key
      df_global_summary['region'] = "World"
      df_global_summary.set_index('region', append =True, inplace=True )

      #  Sub in more helpful col names
      df_global_summary.columns = final_column_names


      # Append regional and global summaries
      df_summary = pd.concat([df_region_summary, df_global_summary])



    # Merge in region data
      for ref in reference_vals:
        this_ref_pop_regions = df_pop_regions[df_pop_regions['year'] == ref].copy()
        
        this_ref_pop_regions = this_ref_pop_regions[['region', 'population']]\
          .rename(columns = {"population": f'regional_population {ref}'})\
          .set_index('region')

      # Repeat for each source_var in selected_vars (I couldn't find a more sensible way to do the merge at the next step)      
        df_list = [this_ref_pop_regions] * len(selected_vars)
        this_ref_pop_regions = pd.concat(df_list, keys = selected_vars)
        # rename the row indexes
        this_ref_pop_regions.index.names = ['source_var', 'region']
      

        df_summary = df_summary\
          .merge(this_ref_pop_regions, on=['source_var', 'region'], how = 'left')

        df_summary[f'Pop. coverage {ref}'] = df_summary[f'Pop. sum {ref}']/df_summary[f'regional_population {ref}']



      # To help with formatting the multi-level index, I make a dictionary
      dict = {
          ('Avg',reference_vals[0]): df_summary[f'Avg {reference_vals[0]}'], 
          ('Avg',reference_vals[1]): df_summary[f'Avg {reference_vals[1]}'],
          ('Wt. avg',reference_vals[0]): df_summary[f'Wt. avg {reference_vals[0]}'], 
          ('Wt. avg',reference_vals[1]): df_summary[f'Wt. avg {reference_vals[1]}'],
          ('Absolute','fall'): df_summary['absolute_fall'],
          ('Absolute','stable'): df_summary['absolute_stable'],
          ('Absolute','rise'): df_summary['absolute_rise'],
          ('Relative','fall'): df_summary['relative_fall'],
          ('Relative','stable'): df_summary['relative_stable'],
          ('Relative','rise'): df_summary['relative_rise'],
          ('Total','total'): df_summary['total'],
          ('Absolute','share_fall'): df_summary['share_absolute_fall'] * 100,
          ('Absolute','share_stable'): df_summary['share_absolute_stable'] * 100,
          ('Absolute','share_rise'): df_summary['share_absolute_rise'] * 100,
          ('Relative','share_fall'): df_summary['share_relative_fall'] * 100,
          ('Relative','share_stable'): df_summary['share_relative_stable'] * 100,
          ('Relative','share_rise'): df_summary['share_relative_rise'] * 100,
          ('Pop. weights',reference_vals[0]): df_summary[f'Pop. weights {reference_vals[0]}'],
          ('Pop. weights',reference_vals[1]): df_summary[f'Pop. weights {reference_vals[1]}'],
          ('Pop. coverage',reference_vals[0]): df_summary[f'Pop. coverage {reference_vals[0]}'],
          ('Pop. coverage',reference_vals[1]): df_summary[f'Pop. coverage {reference_vals[1]}']
          }
      
      # ... And then put it back to a dataframe
      df_summary = pd.DataFrame(dict)


      df_summary = df_summary.sort_index()

      # Split the original dataframe into a dictionary of dataframes by first row index value
      grouped = df_summary.groupby(level=0)
      dfs_dict = {name: group for name, group in grouped}

      # Drop the first row index level from each dataframe
      dfs_dict_dropped = {name: df.droplevel(0, axis=0) for name, df in dfs_dict.items()}

      df_summary = pd.concat(dfs_dict_dropped, axis=1, keys=dfs_dict_dropped.keys())

      # df_summary = df_summary.unstack(level=0).swaplevel(i=0, j=2, axis=1)

      # df_summary = df_summary.swaplevel(i=1, j=2, axis=1)

      # df_summary = df_summary.sort_index(level= 'source_var')
    
      for source_var in selected_vars:

        for ref in reference_vals:
          df_summary[(source_var,'Avg',ref)] = df_summary[(source_var,'Avg',ref)] .map('{:.1f}'.format)
          df_summary[(source_var,'Wt. avg',ref)] = df_summary[(source_var,'Wt. avg',ref)] .map('{:.1f}'.format)
          df_summary[(source_var,'Pop. weights',ref)] = df_summary[(source_var,'Pop. weights',ref)] .map('{:.2f}'.format)
          df_summary[(source_var,'Pop. coverage',ref)] = df_summary[(source_var,'Pop. coverage',ref)] .map('{:.2f}'.format)

        for change_type in ['Absolute', 'Relative']:
          for change_cat in ['rise', 'stable', 'fall']:
            df_summary[(source_var, change_type, change_cat)] = df_summary[(source_var, change_type, change_cat)] .map('{:.0f}'.format)
            df_summary[(source_var, change_type, f'share_{change_cat}')] = df_summary[(source_var, change_type,  f'share_{change_cat}')].map('{:.1f}'.format)

        df_summary[(source_var,'Total', 'total')] = df_summary[(source_var,'Total', 'total')] .map('{:.0f}'.format)


      # Make a dictionary storing the prepped data and different parts of the summary table
      summaries_dict = {}

      # The whole summary table
      summaries_dict['all'] = df_summary

      # The fall/stable/rise counts – for Absolute and Relative thresholds
      for change_type in ['Absolute', 'Relative']:
        summaries_dict[f'{change_type.lower()}_counts'] = df_summary.loc[:, (selected_vars, [change_type, 'Total'], ['fall','stable','rise','total'])].droplevel(level=1, axis=1)

      # The fall/stable/rise pop shares – for Absolute and Relative thresholds
      for change_type in ['Absolute', 'Relative']:
        summaries_dict[f'{change_type.lower()}_shares'] = df_summary.loc[:, (selected_vars, [change_type], ['share_fall','share_stable','share_rise'])].droplevel(level=1, axis=1)


      # The averages and population coverage
      summaries_dict['averages'] = df_summary.loc[:, (selected_vars, ['Avg', 'Wt. avg', 'Pop. coverage'], slice(None))]
    


    summary_tables_dict[obs_requirement] = summaries_dict

  return summary_tables_dict






# ---------------

# %% [markdown]
#  # Preparing tables and charts
#  This function prepares the table that is used a number of times in the data.

# %%
# def prep_data_and_change_summary(
#       source_dfs,
#       df_pop,
#       df_pop_regions,
#       df_regions,
#       region_col,
#       selected_vars,
#       reference_vals,
#       max_dist_from_refs,
#       min_dist_between,
#       reference_col,
#       group_by_col,
#       outlier_cut_off_upper,
#       tolerance_lookup
#       ):

#     output_dict = {}

#     for all_metrics_requirement in [False, True]:

#       prepped_data = prep_data(
#           source_dfs = source_dfs,
#           df_pop = df_pop,
#           df_regions = df_regions,
#           region_col = region_col,
#           selected_vars = selected_vars,
#           reference_vals = reference_vals,
#           max_dist_from_refs = max_dist_from_refs,
#           min_dist_between = min_dist_between,
#           all_metrics_requirement = all_metrics_requirement,
#           reference_col = reference_col,
#           group_by_col = group_by_col,
#           tolerance_lookup = tolerance_lookup,
#           outlier_cut_off_upper = outlier_cut_off_upper
#           )

#       # Prepare pop-weighted averages for each ref year
#       df_aggs = prepped_data.copy()

#       for ref in reference_vals:

#           # Calulate regional pop weights, grouped by source-var 
#           df_aggs[f'regional_pop_weights{ref}'] = df_aggs.groupby(['source_var', region_col])[f'pop{ref}'].transform(lambda x: x/x.sum()) 

#           # Calulate global pop weights, grouped by source-var
#           df_aggs[f'global_pop_weights{ref}'] = df_aggs.groupby('source_var')[f'pop{ref}'].transform(lambda x: x/x.sum()) 

#           # Multiply the values by the pop weights 
#           df_aggs[f'region_weighted_value{ref}'] = df_aggs[f'value{ref}'] * df_aggs[f'regional_pop_weights{ref}']
#           df_aggs[f'global_weighted_value{ref}'] = df_aggs[f'value{ref}'] * df_aggs[f'global_pop_weights{ref}']

#       # Select whether aboslute or relative rise/fall categories are to be used
#       change_types = ['absolute', 'relative']
#       cats = ['rise', 'stable', 'fall']

#       for change_type in change_types:
        
#         for cat in cats:

#           df_aggs[f'{change_type}_{cat}'] = df_aggs[f'{change_type}_{cat}']

      
#       # Summarise by region
#       df_region_summary = df_aggs\
#           .groupby(['source_var', region_col])[[
#               f'value{reference_vals[0]}',
#               f'value{reference_vals[1]}',
#               f'region_weighted_value{reference_vals[0]}',
#               f'region_weighted_value{reference_vals[1]}',
#               f'global_pop_weights{reference_vals[0]}', 
#               f'global_pop_weights{reference_vals[1]}',
#               f'pop{reference_vals[0]}',
#               f'pop{reference_vals[1]}', 
#               'absolute_fall', 
#               'absolute_stable', 
#               'absolute_rise',
#               'relative_fall', 
#               'relative_stable', 
#               'relative_rise']]\
#           .agg(['sum', 'mean', 'count'])


#       df_region_summary = df_region_summary.loc[:, [
#           (f'value{reference_vals[0]}', 'mean'),
#           (f'value{reference_vals[1]}', 'mean'),
#           (f'region_weighted_value{reference_vals[0]}', 'sum'),
#           (f'region_weighted_value{reference_vals[1]}', 'sum'),
#           ('absolute_fall', 'sum'),
#           ('absolute_stable', 'sum'), 
#           ('absolute_rise', 'sum'),
#           ('relative_fall', 'sum'),
#           ('relative_stable', 'sum'), 
#           ('relative_rise', 'sum'),
#           ('relative_rise', 'count'),
#           (f'global_pop_weights{reference_vals[0]}', 'sum'), 
#           (f'global_pop_weights{reference_vals[1]}', 'sum'),
#           (f'pop{reference_vals[0]}', 'sum'),
#           (f'pop{reference_vals[1]}', 'sum')]]
    

#     #  Define more helpful col names
#       final_column_names =  [
#           f'Avg {reference_vals[0]}',
#           f'Avg {reference_vals[1]}',
#           f'Wt. avg {reference_vals[0]}',
#           f'Wt. avg {reference_vals[1]}',
#           'absolute_fall',
#           'absolute_stable',
#           'absolute_rise',
#           'relative_fall',
#           'relative_stable',
#           'relative_rise',
#           'total',
#           f'Pop. weights {reference_vals[0]}',
#           f'Pop. weights {reference_vals[1]}',
#           f'Pop. sum {reference_vals[0]}',
#           f'Pop. sum {reference_vals[1]}',        
#       ]

#       #  Sub in more helpful col names
#       df_region_summary.columns = final_column_names


#       # Summarise globally

#       df_global_summary = df_aggs\
#           .groupby(['source_var'])[[
#               f'value{reference_vals[0]}',
#               f'value{reference_vals[1]}',
#               f'global_weighted_value{reference_vals[0]}',
#               f'global_weighted_value{reference_vals[1]}',
#               f'global_pop_weights{reference_vals[0]}', 
#               f'global_pop_weights{reference_vals[1]}',
#               f'pop{reference_vals[0]}',
#               f'pop{reference_vals[1]}',  
#               'absolute_fall', 
#               'absolute_stable', 
#               'absolute_rise',
#               'relative_fall', 
#               'relative_stable', 
#               'relative_rise']]\
#           .agg(['sum', 'mean', 'count'])


#       df_global_summary = df_global_summary.loc[:, [
#           (f'value{reference_vals[0]}', 'mean'),
#           (f'value{reference_vals[1]}', 'mean'),
#           (f'global_weighted_value{reference_vals[0]}', 'sum'),
#           (f'global_weighted_value{reference_vals[1]}', 'sum'),
#           ('absolute_fall', 'sum'),
#           ('absolute_stable', 'sum'), 
#           ('absolute_rise', 'sum'),
#           ('relative_fall', 'sum'),
#           ('relative_stable', 'sum'), 
#           ('relative_rise', 'sum'),
#           ('relative_rise', 'count'),
#           (f'global_pop_weights{reference_vals[0]}', 'sum'), 
#           (f'global_pop_weights{reference_vals[1]}', 'sum'),
#           (f'pop{reference_vals[0]}', 'sum'),
#           (f'pop{reference_vals[1]}', 'sum')]]

#       # Add 'World' region as key
#       df_global_summary[region_col] = "World"
#       df_global_summary.set_index(region_col, append =True, inplace=True )

#       #  Sub in more helpful col names
#       df_global_summary.columns = final_column_names


#       # Append regional and global summaries
#       df_summary = pd.concat([df_region_summary, df_global_summary])



#     # Merge in region data
#       for ref in reference_vals:
#         this_ref_pop_regions = df_pop_regions[df_pop_regions[reference_col] == ref].copy()
        
#         this_ref_pop_regions = this_ref_pop_regions[[region_col, 'population']]\
#           .rename(columns = {"population": f'regional_population {ref}'})\
#           .set_index(region_col)

#       # Repeat for each source_var in selected_vars (I couldn't find a more sensible way to do the merge at the next step)      
#         df_list = [this_ref_pop_regions] * len(selected_vars)
#         this_ref_pop_regions = pd.concat(df_list, keys = selected_vars)
#         # rename the row indexes
#         this_ref_pop_regions.index.names = ['source_var', region_col]
      

#         df_summary = df_summary\
#           .merge(this_ref_pop_regions, on=['source_var', region_col], how = 'outer')

#         df_summary[f'Pop. coverage {ref}'] = df_summary[f'Pop. sum {ref}']/df_summary[f'regional_population {ref}']



#       # To help with formatting the multi-level index, I make a dictionary
#       dict = {
#           ('Avg',reference_vals[0]): df_summary[f'Avg {reference_vals[0]}'], 
#           ('Avg',reference_vals[1]): df_summary[f'Avg {reference_vals[1]}'],
#           ('Wt. avg',reference_vals[0]): df_summary[f'Wt. avg {reference_vals[0]}'], 
#           ('Wt. avg',reference_vals[1]): df_summary[f'Wt. avg {reference_vals[1]}'],
#           ('Absolute','fall'): df_summary['absolute_fall'],
#           ('Absolute','stable'): df_summary['absolute_stable'],
#           ('Absolute','rise'): df_summary['absolute_rise'],
#           ('Relative','fall'): df_summary['relative_fall'],
#           ('Relative','stable'): df_summary['relative_stable'],
#           ('Relative','rise'): df_summary['relative_rise'],
#           ('Total','total'): df_summary['total'],
#           ('Pop. weights',reference_vals[0]): df_summary[f'Pop. weights {reference_vals[0]}'],
#           ('Pop. weights',reference_vals[1]): df_summary[f'Pop. weights {reference_vals[1]}'],
#           ('Pop. coverage',reference_vals[0]): df_summary[f'Pop. coverage {reference_vals[0]}'],
#           ('Pop. coverage',reference_vals[1]): df_summary[f'Pop. coverage {reference_vals[1]}']
#           }
      
#       # ... And then put it back to a dataframe
#       df_summary = pd.DataFrame(dict)


#       df_summary = df_summary.sort_index()

#       # Split the original dataframe into a dictionary of dataframes by first row index value
#       grouped = df_summary.groupby(level=0)
#       dfs_dict = {name: group for name, group in grouped}

#       # Drop the first row index level from each dataframe
#       dfs_dict_dropped = {name: df.droplevel(0, axis=0) for name, df in dfs_dict.items()}

#       df_summary = pd.concat(dfs_dict_dropped, axis=1, keys=dfs_dict_dropped.keys())

#       # df_summary = df_summary.unstack(level=0).swaplevel(i=0, j=2, axis=1)

#       # df_summary = df_summary.swaplevel(i=1, j=2, axis=1)

#       # df_summary = df_summary.sort_index(level= 'source_var')
    
#       for source_var in selected_vars:

#         for ref in reference_vals:
#           df_summary[(source_var,'Avg',ref)] = df_summary[(source_var,'Avg',ref)] .map('{:.1f}'.format)
#           df_summary[(source_var,'Wt. avg',ref)] = df_summary[(source_var,'Wt. avg',ref)] .map('{:.1f}'.format)
#           df_summary[(source_var,'Pop. weights',ref)] = df_summary[(source_var,'Pop. weights',ref)] .map('{:.2f}'.format)
#           df_summary[(source_var,'Pop. coverage',ref)] = df_summary[(source_var,'Pop. coverage',ref)] .map('{:.2f}'.format)

#         for change_type in ['Absolute', 'Relative']:
#           for change_cat in ['rise', 'stable', 'fall']:
#             df_summary[(source_var, change_type, change_cat)] = df_summary[(source_var, change_type, change_cat)] .map('{:.0f}'.format)

#         df_summary[(source_var,'Total', 'total')] = df_summary[(source_var,'Total', 'total')] .map('{:.0f}'.format)


#       # Make a dictionary storing the prepped data and different parts of the summary table
#       summaries_dict = {}

#       # The prepped data (not summarised)
#       summaries_dict["prepped_data"] = prepped_data

#       # The whole summary table
#       summaries_dict['all'] = df_summary

#       # The fall/stable/rise counts – for Absolute and Relative thresholds
#       for change_type in ['Absolute', 'Relative']:
#         summaries_dict[f'{change_type.lower()}_counts'] = df_summary.loc[:, (selected_vars, [change_type, 'Total'], ['fall','stable','rise','total'])].droplevel(level=1, axis=1)

#       # The averages and population coverage
#       summaries_dict['averages'] = df_summary.loc[:, (selected_vars, ['Avg', 'Wt. avg', 'Pop. coverage'], slice(None))]


#       # Reshape the data for OWID upload

#       owid_format = pd.melt(prepped_data, id_vars=['source_var', group_by_col, region_col ], value_vars=[f'{reference_col}{reference_vals[0]}', f'{reference_col}{reference_vals[1]}', f'value{reference_vals[0]}', f'value{reference_vals[1]}'])

#       # Extract year and group information from variable column
#       owid_format[['var', 'reference']] = owid_format['variable'].str.extract(r'(\D+)(\d+)$')
#       owid_format['reference'] = owid_format['reference'].astype(int)

#       #Reshape from long to wide
#       owid_format=pd.pivot(owid_format, index=['source_var', group_by_col, region_col, 'reference' ], columns = 'var' ,values = 'value').reset_index() 

#       # Drop the original reference column
#       owid_format = owid_format.drop('reference', axis=1)

#       # Pivot the melted dataframe wider – one value column per source_var
#       owid_format = owid_format.pivot_table(index=[group_by_col, region_col, reference_col], columns='source_var', values='value').reset_index()

#       summaries_dict['owid_format'] = owid_format
    
#       output_dict[f'all_sources_{all_metrics_requirement}'] = summaries_dict
    

#     # Merge the all_sources- True and False data for OWID format
#     owid_format = pd.merge(output_dict['all_sources_False']['owid_format'], output_dict['all_sources_True']['owid_format'], on=[group_by_col, reference_col, region_col], how='outer', suffixes=(' – all observations', ' – only matching observations'))

#     owid_format = owid_format.rename(columns={group_by_col: "country", reference_col: "year"})
    
#     # Reorder columns
#     cols = list(owid_format.columns) # Get the list of column names
#     cols.remove('country') # Remove col1 from the list
#     cols.remove('year') # Remove col2 from the list
#     cols = ['country', 'year'] + cols # Add col1 and col2 to the front of the list
#     owid_format = owid_format[cols] # Reorder columns in the DataFrame
    
#     owid_format['year'] = owid_format['year'].astype(int) # Year needs to be integer for OWID

#     output_dict['owid_format'] = owid_format
    
#     return output_dict





# %% [markdown]
#  This function builds the scatter charts used in the paper. It also returns the data being plotted.

# %%
# def plot_change_scatter(
#       plot_var,
#       source_dfs,
#       df_pop,
#       df_regions,
#       selected_vars,
#       reference_vals,
#       max_dist_from_refs,
#       min_dist_between,
#       all_metrics_requirement,
#       reference_col,
#       group_by_col,
#       outlier_cut_off_upper,
#       tolerance_lookup,
#       region_col,
#       ):


#     prepped_data = prep_data(
#         source_dfs = source_dfs,
#         df_pop = df_pop,
#         df_regions = df_regions,
#         selected_vars = selected_vars,
#         reference_vals = reference_vals,
#         max_dist_from_refs = max_dist_from_refs,
#         min_dist_between = min_dist_between,
#         all_metrics_requirement = all_metrics_requirement,
#         reference_col = reference_col,
#         group_by_col = group_by_col,
#         tolerance_lookup = tolerance_lookup,
#         outlier_cut_off_upper = outlier_cut_off_upper
#         )

#     if plot_var == 'diff' or plot_var == 'relative_diff':

#       prepped_data['change'] = prepped_data[f'value{reference_vals[1]}'] - prepped_data[f'value{reference_vals[0]}']

#       if plot_var == 'relative_diff':
#         prepped_data['change'] = prepped_data['change']/prepped_data[f'value{reference_vals[0]}']*100

#       prepped_data = prepped_data.pivot(index=['Entity', region_col], columns='source_var', values=['change', f'value{reference_vals[0]}',f'value{reference_vals[1]}', f'Year{reference_vals[0]}',f'Year{reference_vals[1]}',f'pop{reference_vals[0]}',f'pop{reference_vals[1]}', region_col, 'pip_welfare'])
      
#       prepped_data.columns = [' '.join(col).strip() for col in prepped_data.columns.values]

#       prepped_data =  prepped_data.reset_index()

      
#       # The scatter bubble size will be equal to transformed population for the later year
#         #  The transformation was adapted from here: https://stackoverflow.com/questions/63265123/size-of-bubbles-in-plotly-express-scatter-mapbox
#       number_of_steps = 40
#       selected_pop_var = f'pop{reference_vals[1]} {selected_vars[0]}'
#       pop_step = (prepped_data[selected_pop_var].max() - prepped_data[selected_pop_var].min()) / number_of_steps
#       prepped_data['plot_pop_scale'] = (prepped_data[selected_pop_var] - prepped_data[selected_pop_var].min()) / pop_step + 1

#       # The pivot converted many columns to 'object' data type.
#       # The chart below doesn't accept this type for the bubble size parameter
#       cols_to_convert = ['plot_pop_scale']
#       prepped_data[cols_to_convert] = prepped_data[cols_to_convert].apply(pd.to_numeric, errors='coerce')

#       # Sort to keep regions the same colours.
#       prepped_data = prepped_data.sort_values(by=[region_col])

#       # # To plot a 45 degree line we need to specify the points manually      
#       ymin = prepped_data[f'change {selected_vars[1]}'].min() 
#       ymax = prepped_data[f'change {selected_vars[1]}'].max()

#       xmin = prepped_data[f'change {selected_vars[0]}'].min()
#       xmax = prepped_data[f'change {selected_vars[0]}'].max()

#       fig = px.scatter(
#             prepped_data, 
#             x=f'change {selected_vars[0]}', 
#             y=f'change {selected_vars[1]}',
#             color=region_col, 
#             # facet_col='source_var', 
#             # facet_col_wrap=1, 
#             size='plot_pop_scale',
#             size_max= 30,
#             hover_name=group_by_col,
#             hover_data={
#               f'change {selected_vars[0]}':':.1f',
#               f'change {selected_vars[1]}':':.1f',
#               f'{reference_col}{reference_vals[0]} {selected_vars[0]}':':.0f',
#               f'{reference_col}{reference_vals[1]} {selected_vars[0]}':':.0f',
#               f'{reference_col}{reference_vals[0]} {selected_vars[1]}':':.0f',
#               f'{reference_col}{reference_vals[1]} {selected_vars[1]}':':.0f',
#               region_col: False,
#               'plot_pop_scale': False
#             },
#             title=f'Change in {selected_vars[0]} vs {selected_vars[1]} ({reference_vals[0]}-{reference_vals[1]} +/- {max_dist_from_refs})',
#             height=600
#             )


#       fig.update_layout(
#           shapes=[
#               dict(
#                   type= 'line',
#                   line=dict(color="#808080"),
#                   opacity=0.5,
#                   yref= 'y', y0=min(ymin, xmin), y1= max(ymax, xmax),
#                   xref= 'x', x0=min(ymin, xmin), x1= max(ymax, xmax)
                  
#               )
#           ])


#     else:
#     # Select only the data for the specified plot_var
#       prepped_data = prepped_data[prepped_data['source_var'] == plot_var]

#       # The scatter bubble size will be equal to transformed population for the later year
#         #  The transformation was adapted from here: https://stackoverflow.com/questions/63265123/size-of-bubbles-in-plotly-express-scatter-mapbox
#       number_of_steps = 40
#       prepped_data['plot_pop'] = prepped_data[f'pop{reference_vals[1]}']
#       pop_step = (prepped_data['plot_pop'].max() - prepped_data['plot_pop'].min()) / number_of_steps
#       prepped_data['plot_pop_scale'] = (prepped_data['plot_pop'] - prepped_data['plot_pop'].min()) / pop_step + 1
      
#       prepped_data = prepped_data.sort_values(by=[region_col])

#       # To plot a 45 degree line we need to specify the points manually
#       ymin = prepped_data[f'value{reference_vals[1]}'].min()
#       ymax = prepped_data[f'value{reference_vals[1]}'].max()

#       xmin = prepped_data[f'value{reference_vals[0]}'].min()
#       xmax = prepped_data[f'value{reference_vals[0]}'].max()

#       fig = px.scatter(
#         prepped_data, 
#         x=f'value{reference_vals[0]}', 
#         y=f'value{reference_vals[1]}',
#         color=region_col, 
#         # facet_col='source_var', 
#         # facet_col_wrap=1, 
#         size='plot_pop_scale',
#         # size_max= 60,
#         hover_name=group_by_col,
#         hover_data={
#           f'value{reference_vals[0]}':':.2f',
#           f'{reference_col}{reference_vals[0]}':True,
#           f'value{reference_vals[1]}':':.2f',
#           f'{reference_col}{reference_vals[1]}':True,
#           region_col: False,
#           'plot_pop_scale': False,
#           'source_var': False},
#         title=f'{plot_var}, {reference_vals[0]} vs {reference_vals[1]} (+/- {max_dist_from_refs})',
#         height=600
#         )


#       fig.update_layout(
#           shapes=[
#               dict(
#                   type= 'line',
#                   line=dict(color="#808080"),
#                   opacity=0.5,
#                   yref= 'y', y0=min(ymin, xmin), y1= max(ymax, xmax),
#                   xref= 'x', x0=min(ymin, xmin), x1= max(ymax, xmax)
                  
#               )
#           ])

    






#     return fig, prepped_data


# %% [markdown]
# This builds a filepath in which to save prepared data
# %%
# def filename_for_full_data(selected_vars,reference_vals):
    
#     vars_string = ' vs '.join(selected_vars)
#     refs_string = f'{reference_vals[0]} to {reference_vals[1]}'

#     filepath = f'{vars_string} – {refs_string}'

#     return filepath




#  %% [markdown]






# %% [markdown]
#  # Preparing summary tables 
#  This function prepares the table that is used a number of times in the data.

#%%
# def prep_summary_tables_OLD(
#       prepped_data_dict,
#       df_pop_regions,
#       selected_vars,
#       reference_vals
#       ):
  
#   summary_tables_dict ={}

#   all_metrics_requirement_types = ['all_obs', 'matching_obs']


#   for obs_requirement in all_metrics_requirement_types:

#     prepped_data = prepped_data_dict[obs_requirement]

#     # Prepare pop-weighted averages for each ref year
#     df_aggs = prepped_data.copy()

#     df_aggs = df_aggs[df_aggs['source_var'].isin(selected_vars)]

#     for ref in reference_vals:

#       # Calulate regional pop weights, grouped by source-var 
#       df_aggs[f'regional_pop_weights{ref}'] = df_aggs.groupby(['source_var', 'region'])[f'pop{ref}'].transform(lambda x: x/x.sum()) 

#       # Calulate global pop weights, grouped by source-var
#       df_aggs[f'global_pop_weights{ref}'] = df_aggs.groupby('source_var')[f'pop{ref}'].transform(lambda x: x/x.sum()) 

#       # Multiply the values by the pop weights 
#       df_aggs[f'region_weighted_value{ref}'] = df_aggs[f'value{ref}'] * df_aggs[f'regional_pop_weights{ref}']
#       df_aggs[f'global_weighted_value{ref}'] = df_aggs[f'value{ref}'] * df_aggs[f'global_pop_weights{ref}']

    

#     change_types = ['absolute', 'relative']
#     cats = ['rise', 'stable', 'fall']

#     for change_type in change_types:
      
#       # for cat in cats:

#       #   df_aggs[f'{change_type}_{cat}'] = df_aggs[f'{change_type}_{cat}']

    
#       # Summarise by region
#       df_region_summary = df_aggs\
#         .groupby(['source_var', 'region'])[[
#             f'value{reference_vals[0]}',
#             f'value{reference_vals[1]}',
#             f'region_weighted_value{reference_vals[0]}',
#             f'region_weighted_value{reference_vals[1]}',
#             f'global_pop_weights{reference_vals[0]}', 
#             f'global_pop_weights{reference_vals[1]}',
#             f'pop{reference_vals[0]}',
#             f'pop{reference_vals[1]}', 
#             'absolute_fall', 
#             'absolute_stable', 
#             'absolute_rise',
#             'relative_fall', 
#             'relative_stable', 
#             'relative_rise']]\
#         .agg(['sum', 'mean', 'count'])


#       df_region_summary = df_region_summary.loc[:, [
#           (f'value{reference_vals[0]}', 'mean'),
#           (f'value{reference_vals[1]}', 'mean'),
#           (f'region_weighted_value{reference_vals[0]}', 'sum'),
#           (f'region_weighted_value{reference_vals[1]}', 'sum'),
#           ('absolute_fall', 'sum'),
#           ('absolute_stable', 'sum'), 
#           ('absolute_rise', 'sum'),
#           ('relative_fall', 'sum'),
#           ('relative_stable', 'sum'), 
#           ('relative_rise', 'sum'),
#           ('relative_rise', 'count'),
#           (f'global_pop_weights{reference_vals[0]}', 'sum'), 
#           (f'global_pop_weights{reference_vals[1]}', 'sum'),
#           (f'pop{reference_vals[0]}', 'sum'),
#           (f'pop{reference_vals[1]}', 'sum')]]
    

#     #  Define more helpful col names
#       final_column_names =  [
#           f'Avg {reference_vals[0]}',
#           f'Avg {reference_vals[1]}',
#           f'Wt. avg {reference_vals[0]}',
#           f'Wt. avg {reference_vals[1]}',
#           'absolute_fall',
#           'absolute_stable',
#           'absolute_rise',
#           'relative_fall',
#           'relative_stable',
#           'relative_rise',
#           'total',
#           f'Pop. weights {reference_vals[0]}',
#           f'Pop. weights {reference_vals[1]}',
#           f'Pop. sum {reference_vals[0]}',
#           f'Pop. sum {reference_vals[1]}',        
#       ]

#       #  Sub in more helpful col names
#       df_region_summary.columns = final_column_names


#       # Summarise globally

#       df_global_summary = df_aggs\
#           .groupby(['source_var'])[[
#               f'value{reference_vals[0]}',
#               f'value{reference_vals[1]}',
#               f'global_weighted_value{reference_vals[0]}',
#               f'global_weighted_value{reference_vals[1]}',
#               f'global_pop_weights{reference_vals[0]}', 
#               f'global_pop_weights{reference_vals[1]}',
#               f'pop{reference_vals[0]}',
#               f'pop{reference_vals[1]}',  
#               'absolute_fall', 
#               'absolute_stable', 
#               'absolute_rise',
#               'relative_fall', 
#               'relative_stable', 
#               'relative_rise']]\
#           .agg(['sum', 'mean', 'count'])


#       df_global_summary = df_global_summary.loc[:, [
#           (f'value{reference_vals[0]}', 'mean'),
#           (f'value{reference_vals[1]}', 'mean'),
#           (f'global_weighted_value{reference_vals[0]}', 'sum'),
#           (f'global_weighted_value{reference_vals[1]}', 'sum'),
#           ('absolute_fall', 'sum'),
#           ('absolute_stable', 'sum'), 
#           ('absolute_rise', 'sum'),
#           ('relative_fall', 'sum'),
#           ('relative_stable', 'sum'), 
#           ('relative_rise', 'sum'),
#           ('relative_rise', 'count'),
#           (f'global_pop_weights{reference_vals[0]}', 'sum'), 
#           (f'global_pop_weights{reference_vals[1]}', 'sum'),
#           (f'pop{reference_vals[0]}', 'sum'),
#           (f'pop{reference_vals[1]}', 'sum')]]

#       # Add 'World' region as key
#       df_global_summary['region'] = "World"
#       df_global_summary.set_index('region', append =True, inplace=True )

#       #  Sub in more helpful col names
#       df_global_summary.columns = final_column_names


#       # Append regional and global summaries
#       df_summary = pd.concat([df_region_summary, df_global_summary])



#     # Merge in region data
#       for ref in reference_vals:
#         this_ref_pop_regions = df_pop_regions[df_pop_regions['year'] == ref].copy()
        
#         this_ref_pop_regions = this_ref_pop_regions[['region', 'population']]\
#           .rename(columns = {"population": f'regional_population {ref}'})\
#           .set_index('region')

#       # Repeat for each source_var in selected_vars (I couldn't find a more sensible way to do the merge at the next step)      
#         df_list = [this_ref_pop_regions] * len(selected_vars)
#         this_ref_pop_regions = pd.concat(df_list, keys = selected_vars)
#         # rename the row indexes
#         this_ref_pop_regions.index.names = ['source_var', 'region']
      

#         df_summary = df_summary\
#           .merge(this_ref_pop_regions, on=['source_var', 'region'], how = 'left')

#         df_summary[f'Pop. coverage {ref}'] = df_summary[f'Pop. sum {ref}']/df_summary[f'regional_population {ref}']



#       # To help with formatting the multi-level index, I make a dictionary
#       dict = {
#           ('Avg',reference_vals[0]): df_summary[f'Avg {reference_vals[0]}'], 
#           ('Avg',reference_vals[1]): df_summary[f'Avg {reference_vals[1]}'],
#           ('Wt. avg',reference_vals[0]): df_summary[f'Wt. avg {reference_vals[0]}'], 
#           ('Wt. avg',reference_vals[1]): df_summary[f'Wt. avg {reference_vals[1]}'],
#           ('Absolute','fall'): df_summary['absolute_fall'],
#           ('Absolute','stable'): df_summary['absolute_stable'],
#           ('Absolute','rise'): df_summary['absolute_rise'],
#           ('Relative','fall'): df_summary['relative_fall'],
#           ('Relative','stable'): df_summary['relative_stable'],
#           ('Relative','rise'): df_summary['relative_rise'],
#           ('Total','total'): df_summary['total'],
#           ('Pop. weights',reference_vals[0]): df_summary[f'Pop. weights {reference_vals[0]}'],
#           ('Pop. weights',reference_vals[1]): df_summary[f'Pop. weights {reference_vals[1]}'],
#           ('Pop. coverage',reference_vals[0]): df_summary[f'Pop. coverage {reference_vals[0]}'],
#           ('Pop. coverage',reference_vals[1]): df_summary[f'Pop. coverage {reference_vals[1]}']
#           }
      
#       # ... And then put it back to a dataframe
#       df_summary = pd.DataFrame(dict)


#       df_summary = df_summary.sort_index()

#       # Split the original dataframe into a dictionary of dataframes by first row index value
#       grouped = df_summary.groupby(level=0)
#       dfs_dict = {name: group for name, group in grouped}

#       # Drop the first row index level from each dataframe
#       dfs_dict_dropped = {name: df.droplevel(0, axis=0) for name, df in dfs_dict.items()}

#       df_summary = pd.concat(dfs_dict_dropped, axis=1, keys=dfs_dict_dropped.keys())

#       # df_summary = df_summary.unstack(level=0).swaplevel(i=0, j=2, axis=1)

#       # df_summary = df_summary.swaplevel(i=1, j=2, axis=1)

#       # df_summary = df_summary.sort_index(level= 'source_var')
    
#       for source_var in selected_vars:

#         for ref in reference_vals:
#           df_summary[(source_var,'Avg',ref)] = df_summary[(source_var,'Avg',ref)] .map('{:.1f}'.format)
#           df_summary[(source_var,'Wt. avg',ref)] = df_summary[(source_var,'Wt. avg',ref)] .map('{:.1f}'.format)
#           df_summary[(source_var,'Pop. weights',ref)] = df_summary[(source_var,'Pop. weights',ref)] .map('{:.2f}'.format)
#           df_summary[(source_var,'Pop. coverage',ref)] = df_summary[(source_var,'Pop. coverage',ref)] .map('{:.2f}'.format)

#         for change_type in ['Absolute', 'Relative']:
#           for change_cat in ['rise', 'stable', 'fall']:
#             df_summary[(source_var, change_type, change_cat)] = df_summary[(source_var, change_type, change_cat)] .map('{:.0f}'.format)

#         df_summary[(source_var,'Total', 'total')] = df_summary[(source_var,'Total', 'total')] .map('{:.0f}'.format)


#       # Make a dictionary storing the prepped data and different parts of the summary table
#       summaries_dict = {}

#       # The whole summary table
#       summaries_dict['all'] = df_summary

#       # The fall/stable/rise counts – for Absolute and Relative thresholds
#       for change_type in ['Absolute', 'Relative']:
#         summaries_dict[f'{change_type.lower()}_counts'] = df_summary.loc[:, (selected_vars, [change_type, 'Total'], ['fall','stable','rise','total'])].droplevel(level=1, axis=1)

#       # The averages and population coverage
#       summaries_dict['averages'] = df_summary.loc[:, (selected_vars, ['Avg', 'Wt. avg', 'Pop. coverage'], slice(None))]
    


#     summary_tables_dict[obs_requirement] = summaries_dict

#   return summary_tables_dict

