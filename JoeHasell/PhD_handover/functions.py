#%%
import pandas as pd

#%% RETURN OBSERVATIONS FOR BENCHMARK YEARS
# This is a set of nested functions used to
# prepare a dataset 

# %%
# This function selects data from a dataframe according to a dictionary of many id cols that selects a number of series
# e.g. 'WID' - 'Pre-tax' - 'Gini'
# As well as dropping non-selected rows, it names the selected data – according to the size of the dictionary
# e.g. 'series0', 'series1'
def map_to_series_names(
        df,
        selection_dict
    ):

    # Add an empty 'series' column
    df['series_short_name'] = ''

    # Count the number of series specified in the dictionary
    series_count = len(selection_dict['series_short_name'])  

    # Cycle through each series for be identified in the dataframe
    for i in range(series_count):

        # Short name for the series
        series_name = selection_dict['series_short_name'][i]

        # Initiate a flag
        df['flag'] = 0
        
        # Add one to the flag for every matching column of data 
        for key in selection_dict:

            if key!='series_short_name':
    
                df.loc[df[key]==selection_dict[key][i], 'flag'] = df.loc[df[key]==selection_dict[key][i], 'flag'] + 1

        # Those rows with all matches are the right series, and are given the series name
        df.loc[df['flag']==len(selection_dict)-1, 'series_short_name'] = series_name

    # Drop any rows without a series name (i.e. that have not been matched to the dictionary)
    df = df[df['series_short_name']!='']

    return df

# %% Function to get matching observation closest to ref year
def closest_to_reference(
    df, 
    selection_dict,
    reference_year, 
    max_dist_from_ref, 
    tie_break):
  
    # Select data and give series a shorthand name name
    df = map_to_series_names(
        df,
        selection_dict
    )

    # Drop any unnecessary columns
    df = df.loc[:, ['year', 'country', 'series_short_name', 'value']]

    # Calculate absolute distance from reference value
    df['diff'] = abs(df['year'] - reference_year)

    # Drop any rows with a distance beyond threshold
    if not pd.isna(max_dist_from_ref):
        df = df.loc[df['diff'] <= max_dist_from_ref]

    # Keep closest observation to reference value – including tie-breaks (where there is a match above and below the ref value)
    df = df[df.groupby(['country', 'series_short_name'])['diff'].transform('min') == df['diff']].reset_index(drop=True)

    # Settle tie-breaks
    if tie_break == 'below':
        df = df[df.groupby(['country', 'series_short_name'])['year'].transform('min') == df['year']].reset_index(drop=True)

    elif tie_break == 'above':
        df = df[df.groupby(['country', 'series_short_name'])['year'].transform('max') == df['year']].reset_index(drop=True)

    df = df.drop('diff', axis=1)


    return df


#%%
def add_selection_vars_back_in(
        df,
        selection_dict
    ):

    # Make a dataframe from the selection_dict
    selection_df = pd.DataFrame(selection_dict)

    # Merge the selection into the dataframe, on 'series_short_name'
    df = pd.merge(df, selection_df)

    return df

# %%
# Generate matches for two reference years and merge
# Assumes PIP data is not being passed within df
def matched_pairs_not_pip(
    df, 
    selection_dict,
    reference_years, 
    max_dist_from_ref, 
    min_dist_between):


    # Make sure the pair of reference values are in ascending order
    reference_years.sort()

    # Maximise distance between two refs by settling tie-breaks below the lowest ref and above the highest ref 

    # Find matches for lower reference value
    lower_ref_matches = closest_to_reference(df, selection_dict, reference_years[0], max_dist_from_ref, 'below')

    # Find matches for higher reference value
    higher_ref_matches = closest_to_reference(df, selection_dict, reference_years[1], max_dist_from_ref, 'above')

    # Merge the two sets of matches
    merged_df = pd.merge(lower_ref_matches, higher_ref_matches, on=['country', 'series_short_name'], suffixes=(reference_years[0], reference_years[1]))

    # Drop obs that do not have data for both ref values
    merged_df = merged_df.dropna()

    # Drop obs where the matched data does not meet the min distance requirement
    if not pd.isna(min_dist_between):

    # Keep only rows >= to the min distance
        merged_df = merged_df.loc[(merged_df[f'year{reference_years[1]}'] - merged_df[f'year{reference_years[0]}']) >= min_dist_between, :]

    merged_df = add_selection_vars_back_in(
        merged_df,
        selection_dict
    )

    return merged_df

#%% Test the functions above

#%% test data

data = {
    'year': [
        2000, 
        2009, 
        2013, 
        2011, 
        2012, 
        2013, 
        2000, 
        2008, 
        2014, 
        2011, 
        2012, 
        2013,
        2000, 
        2009, 
        2013, 
        2011, 
        2012, 
        2013, 
        2000, 
        2008, 
        2014, 
        2011, 
        2012, 
        2013],
    'country': [
        'A', 
        'A', 
        'A', 
        'B', 
        'B', 
        'B',
        'A', 
        'A', 
        'A', 
        'B', 
        'B', 
        'B', 
        'A', 
        'A', 
        'A', 
        'B', 
        'B', 
        'B',
        'A', 
        'A', 
        'A', 
        'B', 
        'B', 
        'B'],
    'source': [
        'source1', 
        'source1', 
        'source1', 
        'source1', 
        'source1', 
        'source1', 
        'source1', 
        'source1', 
        'source1', 
        'source1', 
        'source1', 
        'source1', 
        'source2', 
        'source2', 
        'source2', 
        'source2', 
        'source2', 
        'source2', 
        'source2', 
        'source2', 
        'source2', 
        'source2', 
        'source2', 
        'source2'],
    'type': [
        'type1', 
        'type1', 
        'type1', 
        'type1', 
        'type1', 
        'type1', 
        'type2', 
        'type2', 
        'type2', 
        'type2', 
        'type2', 
        'type2',
        'type1', 
        'type1', 
        'type1', 
        'type1', 
        'type1', 
        'type1', 
        'type3', 
        'type3', 
        'type3', 
        'type3', 
        'type3', 
        'type3'],
    'value': [
        100, 
        110, 
        105, 
        200, 
        210, 
        198, 
        100, 
        110, 
        105, 
        200, 
        210, 
        198,
        100, 
        110, 
        105, 
        200, 
        210, 
        198, 
        100, 
        110, 
        105, 
        200, 
        210, 
        198]
}

df_test = pd.DataFrame(data)


# A test selection of series
dict1 = {
    'series_short_name': ['seriesX', 'seriesY'],
    'source': ['source1', 'source2'],
    'type': ['type1', 'type3'] 
}



# %%
map_to_series_names(
        df = df_test,
        selection_dict = dict1
    )

#%%
closest_to_reference(
    df = df_test,
    selection_dict = dict1,
    reference_year = 2011,
    max_dist_from_ref = 2,
    tie_break = 'below')

#%%
matched_pairs_not_pip(
    df = df_test,
    selection_dict = dict1,
    reference_years = [2000, 2011],
    max_dist_from_ref = 5,
    min_dist_between = 0)






    


# %% 
# Same function as above, but structured aroud PIP data
# i.e. presence of overlapping income/consumption data and different reporting levels (urban/rural/national)
def matched_pairs_pip(
    df, 
    selection_dict,
    reference_years, 
    max_dist_from_ref, 
    min_dist_between,
    constant_reporting_level,
    constant_welfare_type):

    # df = df_data
    # selection_dict = pip_selection_dict
    # reference_years = [1990, 2018]
    # max_dist_from_ref = 5
    # min_dist_between = 0
  
    # Create dataframes for thee scenarios:
    # Scenario 1: only allow income data
    df_inc_filter = df.loc[df['pip_welfare'] == "income", :]
    df_inc_filter.name = "Income"

    # Scenario 2: only allow consumption data
    df_cons_filter = df.loc[df['pip_welfare'] == "consumption", :]
    df_cons_filter.name = "Consumption"

    # Scenario 3: allow a mix – dropping consumption data where income data is available in the same year
    df_mixed = df.copy()

    df_mixed['welfare_count'] = df_mixed.groupby(['year', 'country', 'indicator_code'])['pip_welfare'].transform('count')

    df_mixed = df_mixed.loc[(df_mixed['welfare_count'] == 1) | (df_mixed['pip_welfare'] == "income")]

    df_mixed.name = "Mixed"

    #  Store the scenario dataframes in a list
    df_scenarios = [df_inc_filter, df_cons_filter, df_mixed]

    # Run the non-pip matching function on each scenario
    scenario_matches = [matched_pairs_not_pip(
        df = df_scenario, 
        selection_dict = selection_dict,
        reference_years = reference_years, 
        max_dist_from_ref = max_dist_from_ref, 
        min_dist_between = min_dist_between
        ) for df_scenario in df_scenarios]

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
    df_combined_matches['match_count'] = df_combined_matches.groupby(['country', 'series_short_name'])['pip_welfare'].transform('count')
        # Then drop any matches from the lowest priority where there are multiple matches
    df_combined_matches = df_combined_matches.loc[(df_combined_matches['match_count']==1) | ~(df_combined_matches['pip_welfare']==df_scenarios[2].name)]
        #  Repeat at the next level of priority
    df_combined_matches['match_count'] = df_combined_matches.groupby(['country', 'series_short_name'])['pip_welfare'].transform('count')
    df_combined_matches = df_combined_matches.loc[(df_combined_matches['match_count']==1) | ~(df_combined_matches['pip_welfare']==df_scenarios[1].name)]
    
    # Drop the match count column
    df_combined_matches = df_combined_matches.drop('match_count', axis=1)

    return df_combined_matches





# #%% Load clean data
# df_data = pd.read_csv('data/clean/indicators_dataset.csv')

# #%% 
# pip_selection_dict = {
#     'series_short_name': ['PIP gini', 'PIP palma'],
#     'source': ['pip', 'pip'],
#     'indicator_name': ['Gini', 'Palma ratio']
# }
# # %%
# pipmatches = matched_pairs_pip(
#     df = df_data,
#     selection_dict = pip_selection_dict,
#     reference_years = [1990, 2018],
#     max_dist_from_ref = 5,
#     min_dist_between = 0,
#     constant_reporting_level=True,
#     constant_welfare_type=False)
# # %%
