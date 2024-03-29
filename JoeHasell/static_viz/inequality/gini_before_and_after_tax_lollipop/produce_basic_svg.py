#%%
import pandas as pd
import matplotlib.pyplot as plt



#### LOAD AND CLEAN THE ORIG OECD DATA ####
# This is the newer OECD data

#%% 
# This is the new OECD data also with working age pop 
fp = "oecd_data_IDD_2024_03_29.csv"
df_oecd = pd.read_csv(fp)

#%% 
df_oecd = df_oecd[['Reference area', 'Measure', 'Age', 'TIME_PERIOD', 'OBS_VALUE']]

data = df_oecd
#%% 
# Filter for the specified Age groups and Measures
filtered_data = data[data['Age'].isin(['Total', 'From 18 to 65 years']) & 
                     data['Measure'].isin(['Gini (disposable income)', 'Gini (market income)'])]

# Pivot the table
pivot_table = filtered_data.pivot_table(index=['Reference area', 'TIME_PERIOD'], 
                                        columns=['Age', 'Measure'], 
                                        values='OBS_VALUE')

# Rename the columns as specified
pivot_table.columns = ['_'.join(col).strip() for col in pivot_table.columns.values]
pivot_table.rename(columns={
    'From 18 to 65 years_Gini (disposable income)': 'gini_disposable_working_age',
    'Total_Gini (disposable income)': 'gini_disposable_total',
    'From 18 to 65 years_Gini (market income)': 'gini_market_working_age',
    'Total_Gini (market income)': 'gini_market_total'
}, inplace=True)

# Reset index to make it tidy
pivot_table.reset_index(inplace=True)

data = pivot_table
#%%

# Rename the ID columns
data = data.rename(columns={
    "Reference area" : "country",
    "TIME_PERIOD" : "year"
})


#%% 
#### LOAD AND CLEAN THE ETL DATA ####

#%% 
#url = 'http://catalog.ourworldindata.org/grapher/oecd/2023-06-06/income_distribution_database/income_distribution_database.feather'

# #%%
# # Load data from the ETL
# df_etl = pd.read_feather(url)

# #%% 
# # Rename columns for ease of reference
# df_etl = df_etl.rename(columns={
#     'gini': 'gini_disposable',
#     'ginib': 'gini_market'
# })

# df_etl['year'] = df_etl['year'].astype('int32')



########################
#### SELECT MATCHES ####
########################
#%%
# set arguments

target_year = 2019
year_tolerance = 3
tie_break_before = False




#%%
# Define the year range based on the target year
year_start = target_year - year_tolerance
year_end = target_year + year_tolerance

#%%
# Filter the data for the given year range
data_filtered_years = data[(data['year'] >= year_start) & (data['year'] <= year_end)]

#%%
# Clean the data to remove rows with NaN values in Gini columns
cleaned_data = data_filtered_years.dropna()

#%%

#%%
# A function to select the closest year to ta target year, within
# a tolerance range, with a tie-break condition where there are two
# equally distanced 'matches', one before the target year and one after.
def closest_year(group, target_year, tie_break_before):
    # Calculate the absolute distance from the target year
    group['distance'] = (group['year'] - target_year).abs()
    min_distance = group['distance'].min()
    closest_years = group[group['distance'] == min_distance]
    
    # Check if closest_years is empty
    if closest_years.empty:
        print(f"No match for country: {group.name}")
        return None 
    
    closest_years = closest_years.sort_values(by='year', ascending=False)

    # Handle tie-break scenario
        # Match to the year before the target year – only if there is indeed 
        # more than one match and the argument is specified 
    if len(closest_years) > 1 & ~tie_break_before:
        return closest_years.iloc[1]
        # Otherwise match to the later (or only) match year
    else:
        return closest_years.iloc[0]



#%%
# Apply the simplified function to find the closest year for each country
closest_data = cleaned_data.groupby('country').apply(closest_year, target_year=target_year, tie_break_before=tie_break_before).reset_index(drop=True)
#%%
# Drop the NaN rows resultingfrom countries with no matching data
closest_data.dropna(subset=['year', 'country'], inplace=True)
#%%

closest_data.to_csv(f'closest_datapoints_to_{target_year}.csv')

################################################
#### Lollipop plot of before and after tax Gini
################################################


#%%
#Specify the columns to compare

# higher_ineq_col = 'gini_market_total'
# lower_ineq_col = 'gini_market_working_age'

# higher_ineq_col = 'gini_market_total'
# lower_ineq_col = 'gini_disposable_total'

higher_ineq_col = 'gini_market_working_age'
lower_ineq_col = 'gini_disposable_working_age'
#### MAKE THE PLOT ####

#%%
# Sort the data by the disposable income Gini coefficient
sorted_closest_data = closest_data.sort_values(by=lower_ineq_col)


#%%
# Create the plot
fig, ax = plt.subplots(figsize=(12, 8))
bar_length = 0.6  # The length of the vertical bars for the markers

for i, (gini_market, gini_disposable) in enumerate(zip(
    sorted_closest_data[higher_ineq_col],
    sorted_closest_data[lower_ineq_col]
)):
    ax.vlines(x=gini_market, ymin=i - bar_length/2, ymax=i + bar_length/2, color='red', linewidth=1.5)
    ax.vlines(x=gini_disposable, ymin=i - bar_length/2, ymax=i + bar_length/2, color='blue', linewidth=1.5)

for i, (country, year) in enumerate(zip(sorted_closest_data['country'], sorted_closest_data['year'])):
    year_annotation = '' if year == target_year else f' (in {year})'
    ax.text(0, i, f'{country}{year_annotation}', ha='right', va='center', alpha=0.7, fontsize=8)

for i, (gini_disposable, gini_market) in enumerate(zip(
    sorted_closest_data[lower_ineq_col],
    sorted_closest_data[higher_ineq_col]
)):
    ax.text(gini_disposable + 0.002, i, f'{gini_disposable:.2f}', ha='left', va='center', color='blue', alpha=0.7, fontsize=8)
    ax.text(gini_market + 0.002, i, f'{gini_market:.2f}', ha='left', va='center', color='red', alpha=0.7, fontsize=8)

ax.yaxis.set_visible(False)
ax.set_xlabel('Gini Coefficient')
ax.set_title(f'Gini Coefficient {higher_ineq_col} vs {lower_ineq_col} (Closest to {target_year})', fontsize=16)
ax.xaxis.grid(True, linestyle='--', which='major', color='grey', alpha=.25)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()

chart_path = f'{higher_ineq_col}_vs_{lower_ineq_col}_{target_year}.svg'
plt.savefig(chart_path, format='svg')
plt.show()
#%%


############################################################
#### Plot comparison of working age and total pop Ginis ####
############################################################
#%%

#%%
# Scatter plot for both sets of Gini coefficients
plt.figure(figsize=(10, 6))
plt.scatter(closest_data['gini_disposable_working_age'], closest_data['gini_disposable_total'], color='blue', alpha=0.5, label='Disposable')
plt.scatter(closest_data['gini_market_working_age'], closest_data['gini_market_total'], color='red', alpha=0.5, label='Market')

plt.title('Gini Coefficients: Working Age vs Total')
plt.xlabel('Gini Working Age')
plt.ylabel('Gini Total')
plt.legend()
plt.grid(True)

chart_path = f'working_age_vs_total_pop_before_after_tax_gini_scatter.svg'
plt.savefig(chart_path, format='svg')
plt.show()

#%%