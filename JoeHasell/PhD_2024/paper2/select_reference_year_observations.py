"""
If the file doesn't execute correctly, try
pip install requirements.txt
"""
#%% 

import pandas as pd



##### PREPARE DATA #####
#%% Load the main dataset prepared by Pablo
fp = "https://catalog.ourworldindata.org/explorers/poverty_inequality/latest/poverty_inequality_export/keyvars.feather"
df = pd.read_feather(fp)

#%% Add in dataset with top1 shares from PIP – built in build_pip_top1shares.py
df_top1shares = pd.read_csv("data/df_top1shares.csv")
df = pd.concat([df, df_top1shares], ignore_index=True)


#%% Load region categorization and popualtion data
df_regions = pd.read_csv("region_mapping.csv")
df_regions = df_regions.rename(columns={'Entity': 'country'})


df_pop = pd.read_csv("population.csv")
df_pop = df_pop.drop(columns='world_pop_share')
df_pop = df_pop.rename(columns={'Entity': 'country'})

#%% 




##############################################
#%% PIP DATA SELECTION FUNCTIONS
# The PIP data has reporting level (national, urban, rural) and
# welfare type (income or consumption).
# Sometimes, taking observations closest to the reference years may
# result in non-matching data points in these two dimensions.
# These two functions are called within the main function below
# so as to prioritize matches with consistent definitions.abs
 
 
# A function that 'scores' PIP data pairs of years as to
# their welfare concept. A pair of income observations is best,
# a pair of consumption observations is second best
# and non-matching welfare is ranked third.
def cat_welfare(row,col1,col2):
    if row[col1] == 'income' and row[col2] == 'income':
        return 1
    elif row[col1] == 'consumption' and row[col2] == 'consumption':
        return 2
    else:
        return 3

# A function that 'scores' PIP data pairs of years as to 
# their 'reporting_level' (urban, rural, or national). 
# A pair of national observations is best,
# a pair of urban observations is second best,
# a pair of rural observations is third best,
# and non-matching observations is ranked fourth.
def cat_reportinglevel(row,col1,col2):
    if row[col1] == 'national' and row[col2] == 'national':
        return 1
    elif row[col1] == 'urban' and row[col2] == 'urban':
        return 2
    elif row[col1] == 'rural' and row[col2] == 'rural':
        return 3
    else:
        return 4

##############################################

def match_ref_years(
    df: pd.DataFrame,
    series: list,
    reference_years: dict,
    only_all_series: bool
) -> pd.DataFrame:
    """
    Match series to reference years.
    """

    df_match = pd.DataFrame()
    df_series = df[df['series_code'].isin(series)].reset_index(drop=True)

    reference_years_list = []
    for y in reference_years:
        # keep reference year in a list
        reference_years_list.append(y)
        # Filter df_series according to reference year and maximum distance from it
        df_year = df_series[
            (df_series["year"] <= y + reference_years[y]["maximum_distance"])
            & (df_series["year"] >= y - reference_years[y]["maximum_distance"])
        ].reset_index(drop=True)

        assert not df_year.empty, log.error(
            f"No data found for reference year {y}. Please check `maximum_distance` ({reference_years[y]['maximum_distance']})."
        )

        df_year["distance"] = abs(df_year["year"] - y)


        # Merge the different reference years into a single dataframe

        if df_match.empty:
            df_match = df_year
        else:
            df_match = pd.merge(
                df_match,
                df_year,
                how="outer",
                on=["country", "series_code"],
                suffixes=("", f"_{y}"),
            )
           
            # References to column names work differently depending on if there are 
            # 2 or more reference years. Treat these cases separately.
            if len(reference_years_list) == 2:

                # Categorise the pipwelfare match
                df_match["pipwelfarecat"] = df_match.apply(cat_welfare, args=('pipwelfare', f'pipwelfare_{y}'), axis=1)

                # Categorise the pipreportinglevel match
                df_match["pipreportinglevelcat"] = df_match.apply(cat_reportinglevel, args=('pipreportinglevel', f'pipreportinglevel_{y}'), axis=1)

                # Add a column that gives the distance between the observation years
                df_match[f"distance_{reference_years_list[-2]}_{y}"] = abs(
                    df_match["year"] - df_match[f"year_{y}"]
                )

            else:
                # Categorise the pipwelfare match
                df_match["pipwelfarecat"] = df_match.apply(cat_welfare, args=(f"pipwelfare_{reference_years_list[-2]}", f'pipwelfare_{y}'), axis=1)

                # Categorise the pipreportinglevel match
                df_match["pipreportinglevelcat"] = df_match.apply(cat_reportinglevel, args=(f'pipreportinglevel_{reference_years_list[-2]}', f'pipreportinglevel_{y}'), axis=1)

                # Add a column that gives the distance between the observation years
                df_match[f"distance_{reference_years_list[-2]}_{y}"] = abs(
                    df_match[f"year_{reference_years_list[-2]}"] - df_match[f"year_{y}"]
                )

            # Filter df_match according to best pipwelfarecat
            min_values = df_match.groupby(['country', 'series_code'])['pipwelfarecat'].transform('min')
            df_match = df_match[df_match['pipwelfarecat'] == min_values]

            # Filter df_match according to best pipreportinglevelcat
            min_values = df_match.groupby(['country', 'series_code'])['pipreportinglevelcat'].transform('min')
            df_match = df_match[df_match['pipreportinglevelcat'] == min_values]

            # Filter df_match according to min_interval
            df_match = df_match[
                df_match[f"distance_{reference_years_list[-2]}_{y}"]
                >= reference_years[reference_years_list[-2]]["min_interval"]
            ].reset_index(drop=True)


            assert not df_match.empty, log.error(
                f"No matching data found for reference years {reference_years_list[-2]} and {y}. Please check `min_interval` ({reference_years[reference_years_list[-2]]['min_interval']})."
            )

    # Rename columns related to the first reference year
    df_match = df_match.rename(
        columns={
            "year": f"year_{reference_years_list[0]}",
            "distance": f"distance_{reference_years_list[0]}",
            "value": f"value_{reference_years_list[0]}",
            "pipwelfare": f"pipwelfare_{reference_years_list[0]}",
            "pipreportinglevel": f"pipreportinglevel_{reference_years_list[0]}"
        }
    )
   
    
    # Filter df_match according to tie_break_strategy
    for y in reference_years_list:

        # Calculate the minimum of distance for each country-series_code
        min_per_group = df_match.groupby(["country", "series_code"])[f"distance_{y}"].transform('min')

        # Keep only the rows where distance is equal to the group minimum
        df_match = df_match[df_match[f"distance_{y}"] == min_per_group]

        # count how many different years got matched to the reference year
        df_match['unique_years_count'] = df_match.groupby(["country", "series_code"])[f"year_{y}"].transform('nunique')

        if reference_years[y]["tie_break_strategy"] == "lower":
            # drop observations where the year is above the reference year, when there is more than one year that has been matched
            df_match = df_match[(df_match['unique_years_count']==1) | (df_match[f"year_{y}"]<y)]

        elif reference_years[y]["tie_break_strategy"] == "higher":
             # drop observations where the year is below the reference year, when there is more than one year that has been matched
            df_match = df_match[(df_match['unique_years_count']==1) | (df_match[f"year_{y}"]>y)]
        else:
            raise ValueError("tie_break_strategy must be either 'lower' or 'higher'")

        assert not df_match.empty, log.error(
            f"No matching data data found for reference year {y}. Please check `tie_break_strategy` ({reference_years[y]['tie_break_strategy']})."
        )

    # Create a list with the variables year_y and value_y for each reference year
    year_y_list = []
    value_y_list = []
    year_value_y_list = []
    pipwelfare_y_list = []
    pipreportinglevel_y_list = []

    for y in reference_years_list:
        year_y_list.append(f"year_{y}")
        value_y_list.append(f"value_{y}")
        year_value_y_list.append(f"year_{y}")
        year_value_y_list.append(f"value_{y}")
        pipwelfare_y_list.append(f"pipwelfare_{y}")
        pipreportinglevel_y_list.append(f"pipreportinglevel_{y}")

    # Make columns in year_y_list integer
    df_match[year_y_list] = df_match[year_y_list].astype(int)

    # Keep the columns I need
    df_match = df_match[
        ["country", "series_code", "indicator_name"] + year_value_y_list + pipwelfare_y_list + pipreportinglevel_y_list
    ].reset_index(drop=True)

    # Sort by country and year_y
    df_match = df_match.sort_values(
        by=["series_code", "country"] + year_y_list
    ).reset_index(drop=True)

    df_match = pd.merge(
    df_match,
    df_regions,
    how='left'
    )


    # If set in the function arguments, filter for only those countries
    #  avaiable in all series.
    if only_all_series:
        # A very strange bug was happening where the following code was looking across
        # all values of series_code available in the original feather files – 
        # not just those that are in df_match. 
        # To get round this I just read in the exported file, which seems to avoid the problem.
        df_match.to_csv("data/selected_reference_year_obs.csv", index=False)
        df_match = pd.read_csv("data/selected_reference_year_obs.csv")


        # Identify countries present for every unique series_code
        countries_per_series_code = df_match.groupby('series_code')['country'].unique()
        all_countries = set(df_match['country'])

        # Find countries that are present in every series_code
        countries_in_all_series = set(countries_per_series_code.iloc[0])
        for countries in countries_per_series_code:
            countries_in_all_series &= set(countries)

        # Filter the dataframe to keep only rows where country is in the identified set
        df_match = df_match[df_match['country'].isin(countries_in_all_series)]




    # Calculate population weights 
    for y in reference_years_list:
        df_pop_year = df_pop[df_pop['Year']==y]
        df_pop_year = df_pop_year.drop(columns='Year')

        df_match = pd.merge(
        df_match,
        df_pop_year,
        how='left'
        )

        df_match = df_match.rename(columns={'population': f'population_{y}'})

        # Calculate pop-weights and pop-weighted values

        # Group by 'series_code' and calculate total population for each group
        grouped_totals = df_match.groupby('series_code')[f'population_{y}'].sum().rename(f'population_{y}_total')

        # Merge the total populations back to the original DataFrame
        df_match = df_match.merge(grouped_totals, on='series_code', suffixes=('', '_total'))

        # Calculate the weight and weighted-value for each country within its 'series_code' group for both years
        df_match[f'weight_{y}'] = df_match[f'population_{y}'] / df_match[f'population_{y}_total']
        df_match[f'weightedvalue_{y}'] = df_match[f'weight_{y}'] * df_match[f'value_{y}']



    # Export as csv
    df_match.to_csv("data/selected_reference_year_obs.csv", index=False)

  
    return df_match


#### SET ARGUMENTS AND RUN FUNCTION ####
#%%
# Set the series codes that observations will be drawn from
series = [
    "gini_pip_disposable_perCapita",
    "p99p100Share_pip_disposable_perCapita",
    "p90p100Share_pip_disposable_perCapita",
    "headcountRatio50Median_pip_disposable_perCapita",    
    "gini_widExtrapolated_pretaxNational_perAdult",
    "p99p100Share_widExtrapolated_pretaxNational_perAdult",           
    "p90p100Share_widExtrapolated_pretaxNational_perAdult",
    "headcountRatio50Median_widExtrapolated_pretaxNational_perAdult",
    # "gini_wid_pretaxNational_perAdult",
    # "p99p100Share_wid_pretaxNational_perAdult",           
    # "p90p100Share_wid_pretaxNational_perAdult",
    # "headcountRatio50Median_wid_pretaxNational_perAdult" 
]

# Set the reference years, max distance, tie-break strategy and min interval between reference years
# reference_years is the list of years to match the series to. Each year is a dictionary with the year as key and a dictionary of parameters as value. The parameters are:
# - maximum_distance: the maximum distance between the series and the reference year
# - tie_break_strategy: the strategy to use to break ties when there are multiple series that match the reference year. The options are "lower" (select the series with the lowest distance to the reference year) or "higher" (select the series with the highest distance to the reference year)
# - min_interval: the minimum distance between reference years. The value of min_interval for the last reference year is ignored.
reference_years = {
    1993: {"maximum_distance": 5, "tie_break_strategy": "lower", "min_interval": 0},
    2018: {"maximum_distance": 5, "tie_break_strategy": "higher", "min_interval": 0},    
    # 1980: {"maximum_distance": 5, "tie_break_strategy": "lower", "min_interval": 0},
    # 2018: {"maximum_distance": 5, "tie_break_strategy": "higher", "min_interval": 0},
}


#%% Run the main function using the series and ref years specified above
output = match_ref_years(
    df = df, 
    series = series, 
    reference_years = reference_years, 
    only_all_series = True)


#%%