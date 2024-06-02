#%%

import pandas as pd
import statsmodels.api as sm
from statsmodels.iolib.summary2 import summary_col
import matplotlib.pyplot as plt


#%%
data = pd.read_csv('short_period_counterfactual2_only_matches.csv')

#%%
# Filter the data for the two specified metrics
metrics = ['gini_wid_pretaxNational_perAdult', 'gini_pip_disposable_perCapita']
filtered_data = data[data['series_code'].isin(metrics)]


#%%
# Pivot the data to get each metric as a column for each country for both years
pivoted_data = filtered_data.pivot_table(
    index='country',
    columns='series_code',
    values=['value_1993', 'value_2018']
).dropna()  # drop rows with missing values for any of the required metrics

#%%
# Calculate proportional change
proportional_change = (pivoted_data['value_2018'] - pivoted_data['value_1993']) / pivoted_data['value_1993']


#%%
# Extracting pipwelfare_1993 for gini_pip_disposable_perCapita and creating the 'pip_is_consumption' dummy
pipwelfare_1993 = data[data['series_code'] == 'gini_pip_disposable_perCapita'].set_index('country')['pipwelfare_1993']
proportional_change['pipwelfare_1993'] = pipwelfare_1993
proportional_change['pip_is_consumption'] = (proportional_change['pipwelfare_1993'] == 'consumption').astype(int)

#%%
# Extracting region data and creating dummy variables, excluding the first region category as a reference
region_dummies = data[['country', 'region']].drop_duplicates()
region_dummies = pd.get_dummies(region_dummies.set_index('country')['region'], drop_first=True)

#%%
# Merging region dummies with the existing proportional_change DataFrame
proportional_change = proportional_change.join(region_dummies, how='left')


#%%
Y = proportional_change['gini_wid_pretaxNational_perAdult']

#%%
# Baseline model
# Preparing data for regression with region dummies
X_baseline = proportional_change[['gini_pip_disposable_perCapita']]
X_baseline = sm.add_constant(X_baseline)  # adding a constant for the intercept

# Performing the regression with region dummies
model_baseline = sm.OLS(Y, X_baseline)
results_baseline = model_baseline.fit()

#%%
# Consumption dummy model
X_consumption = proportional_change[['gini_pip_disposable_perCapita', 'pip_is_consumption']]
X_consumption = sm.add_constant(X_consumption)  # adding a constant for the intercept

# Performing the regression with region dummies
model_consumption = sm.OLS(Y, X_consumption)
results_consumption = model_consumption.fit()


#%%
# Adding region dummies model
X_consumption_regions = proportional_change[['gini_pip_disposable_perCapita', 'pip_is_consumption'] \
    + list(region_dummies.columns)]
X_consumption_regions = sm.add_constant(X_consumption_regions)  # adding a constant for the intercept

# Performing the regression with region dummies
model_consumption_regions = sm.OLS(Y, X_consumption_regions)
results_consumption_regions = model_consumption_regions.fit()


#%%
# Creating a summary table with results from both models
summary_table = summary_col([results_baseline, results_consumption, results_consumption_regions], 
                            model_names=['Original Model', 'Consumption dummy', 'Plus region dummies'],
                            stars=True, 
                            float_format='%0.2f',
                            info_dict={'No. observations': lambda x: f"{int(x.nobs)}"})

#%%
# Output the summary table
summary_table




########################################
### COMPARE LEVELS (not change) ###
########################################


#%%
data_1993  = pivoted_data['value_1993'].copy()

#%%
# Extracting pipwelfare_1993 for gini_pip_disposable_perCapita and creating the 'pip_is_consumption' dummy
pipwelfare_1993 = data[data['series_code'] == 'gini_pip_disposable_perCapita'].set_index('country')['pipwelfare_1993']
data_1993['pipwelfare_1993'] = pipwelfare_1993
data_1993['pip_is_consumption'] = (data_1993['pipwelfare_1993'] == 'consumption').astype(int)

#%%
# Extracting region data and creating dummy variables, excluding the first region category as a reference
region_dummies = data[['country', 'region']].drop_duplicates()
region_dummies = pd.get_dummies(region_dummies.set_index('country')['region'], drop_first=True)
# Merging region dummies with the existing proportional_change DataFrame
data_1993 = data_1993.join(region_dummies, how='left')



#%%
Y = data_1993['gini_wid_pretaxNational_perAdult']


#%%
# Baseline model
# Preparing data for regression with region dummies
X_baseline = data_1993[['gini_pip_disposable_perCapita']]
X_baseline = sm.add_constant(X_baseline)  # adding a constant for the intercept

# Performing the regression with region dummies
model_baseline = sm.OLS(Y, X_baseline)
results_baseline = model_baseline.fit()



#%%
# Consumption dummy model
X_consumption = data_1993[['gini_pip_disposable_perCapita', 'pip_is_consumption']]
X_consumption = sm.add_constant(X_consumption)  # adding a constant for the intercept

# Performing the regression with region dummies
model_consumption = sm.OLS(Y, X_consumption)
results_consumption = model_consumption.fit()


#%%
# Adding region dummies model
X_consumption_regions = data_1993[['gini_pip_disposable_perCapita', 'pip_is_consumption'] \
    + list(region_dummies.columns)]
X_consumption_regions = sm.add_constant(X_consumption_regions)  # adding a constant for the intercept

# Performing the regression with region dummies
model_consumption_regions = sm.OLS(Y, X_consumption_regions)
results_consumption_regions = model_consumption_regions.fit()


#%%
# Creating a summary table with results from both models
summary_table = summary_col([results_baseline, results_consumption, results_consumption_regions], 
                            model_names=['Original Model', 'Consumption dummy', 'Plus region dummies'],
                            stars=True, 
                            float_format='%0.2f',
                            info_dict={'No. observations': lambda x: f"{int(x.nobs)}"})

#%%
# Output the summary table
summary_table



#%%

# Metrics of interest
metrics = ['gini_wid_pretaxNational_perAdult', 'gini_pip_disposable_perCapita']

ref_year = 2018

# Filter the data for the specified metrics and ensure there is data for both metrics in 1993
filtered_data = data[data['series_code'].isin(metrics)]
filtered_pivot = filtered_data.pivot_table(index='country', columns='series_code', values=f'value_{ref_year}', aggfunc='first').dropna()



# Plotting
plt.figure(figsize=(10, 6))
plt.scatter(filtered_pivot['gini_pip_disposable_perCapita'], filtered_pivot['gini_wid_pretaxNational_perAdult'], alpha=0.6)
plt.title(f'Scatter Plot of GINI Metrics for {ref_year}')
plt.xlabel(f'GINI Disposable Per Capita ({ref_year})')
plt.ylabel(f'GINI Pre-tax National Per Adult ({ref_year})')


# Annotating India's data point
if 'India' in filtered_pivot.index:
    india_x = filtered_pivot.loc['India', 'gini_pip_disposable_perCapita']
    india_y = filtered_pivot.loc['India', 'gini_wid_pretaxNational_perAdult']
    plt.annotate('India', (india_x, india_y), textcoords="offset points", xytext=(0,10), ha='center')

plt.grid(True)
plt.show()
# %%


###################################
### Main predictive regression ####
####################################

#%%

# Reshape from wide to long format
data_long = pd.wide_to_long(data, ["value", "year", "pipwelfare", "weight"], i=["country", "series_code"], j="ref_year", sep='_').reset_index()

# select metrics
metrics = ['gini_wid_pretaxNational_perAdult', 'gini_pip_disposable_perCapita']

filtered_data_long = data_long[data_long['series_code'].isin(metrics)].copy()

#%% code dummies
# is WID
filtered_data_long['is_wid'] = filtered_data_long['series_code'].str.contains('wid').astype(int)

# is pip_and_consumption
filtered_data_long['is_pip_consumption'] = (filtered_data_long['pipwelfare'] == 'consumption').astype(int)

# ref_year is 2018 
filtered_data_long['is_2018'] = (filtered_data_long['ref_year'] == 2018).astype(int)


# ref_year is 2018 X is_WID
filtered_data_long['is_2018_x_wid'] = ((filtered_data_long['ref_year'] == 2018) & (filtered_data_long['is_wid']==1)).astype(int)

#%% Region dummies
region_dummies = filtered_data_long[['country', 'region']].drop_duplicates()
region_dummies = pd.get_dummies(region_dummies.set_index('country')['region'], drop_first=True)
# Merging region dummies with the existing proportional_change DataFrame
filtered_data_long = filtered_data_long.merge(region_dummies, on='country', how='left')

#%% Region dummies X WID
interaction_columns = []

for column in region_dummies.columns:
    interaction_colname = f'is_wid_x_{column}'
    filtered_data_long[interaction_colname] = filtered_data_long['is_wid'] * filtered_data_long[column]
    interaction_columns.append(interaction_colname)


#%%
Y = filtered_data_long['value']


#%%
# Baseline model
# 
X_baseline = filtered_data_long[['is_wid', 'is_pip_consumption', 'is_2018','is_2018_x_wid' ]  \
    + list(region_dummies.columns) \
    + interaction_columns]
X_baseline = sm.add_constant(X_baseline)  # adding a constant for the intercept

# Performing the regression 
model_baseline = sm.OLS(Y, X_baseline)
results_baseline = model_baseline.fit()

# Pop weighted (weights are actual population weights within year – so as not to overweight the second year (following population growth))

weights = filtered_data_long['weight']

# Performing the weighted regression
model_weighted = sm.WLS(Y, X_baseline, weights=weights)
results_weighted = model_weighted.fit()


#%%
# Creating a summary table with results from both models
summary_table = summary_col([results_baseline, results_weighted], 
                            model_names=['Original Model', 'Pop weighted'],
                            stars=True, 
                            float_format='%0.2f',
                            info_dict={'No. observations': lambda x: f"{int(x.nobs)}"})

#%%
# Output the summary table
summary_table


# %%
