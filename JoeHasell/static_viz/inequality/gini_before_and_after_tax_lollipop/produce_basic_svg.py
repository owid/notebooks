#%%
import pandas as pd
import matplotlib.pyplot as plt


url = 'http://catalog.ourworldindata.org/grapher/oecd/2023-06-06/income_distribution_database/income_distribution_database.feather'

# set arguments
#%%
target_year = 2019
year_tolerance = 3
tie_break_before = False
working_age_pop_only = True

svg_chart_path = f'before_after_tax_gini_lollipop_{target_year}_working_age_{working_age_pop_only}.svg'

#### LOAD AND CLEAN THE ORIG OECD DATA ####
# This is the newer OECD data

#%% 
# This is the new OECD data also with working age pop 
fp = "oecd_data_IDD_2024_03_29.csv"
df_oecd = pd.read_csv(fp)

#%% 
if working_age_pop_only:
    df_oecd = df_oecd[df_oecd['Age']=='From 18 to 65 years']
else: 
    df_oecd = df_oecd[df_oecd['Age']=='Total']

#%% 
df_oecd = df_oecd[['Reference area', 'Measure', 'TIME_PERIOD', 'OBS_VALUE']]

#%% 

# Pivot the dataframe to have separate columns for each 'Measure' value
df_oecd = df_oecd.pivot_table(index=["Reference area", "TIME_PERIOD"], 
                            columns="Measure", 
                            values="OBS_VALUE", 
                            aggfunc='first').reset_index()

# Rename columns to remove multi-level indexing after pivot
df_oecd.columns.name = None  # Remove the hierarchy name
df_oecd.reset_index(drop=True, inplace=True)

# Rename the columns
df_oecd = df_oecd.rename(columns={
    "Gini (market income)": "gini_market",
    "Gini (disposable income)": "gini_disposable",
    "Reference area" : "country",
    "TIME_PERIOD" : "year"
})


#%% 
#### LOAD AND CLEAN THE ETL DATA ####

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




#### SELECT MATCHES ####
#%%
# select which data we're using
data = df_oecd
#%%
# Define the year range based on the target year
year_start = target_year - year_tolerance
year_end = target_year + year_tolerance

#%%
# Filter the data for the given year range
data_filtered_years = data[(data['year'] >= year_start) & (data['year'] <= year_end)]

#%%
# Clean the data to remove rows with NaN values in Gini columns
cleaned_data = data_filtered_years.dropna(subset=[
    'gini_disposable',
    'gini_market'
])


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



#### MAKE THE PLOT ####

#%%
# Sort the data by the disposable income Gini coefficient
sorted_closest_data = closest_data.sort_values(by='gini_disposable')


#%%
# Create the plot
fig, ax = plt.subplots(figsize=(12, 8))
bar_length = 0.6  # The length of the vertical bars for the markers

for i, (gini_market, gini_disposable) in enumerate(zip(
    sorted_closest_data['gini_market'],
    sorted_closest_data['gini_disposable']
)):
    ax.vlines(x=gini_market, ymin=i - bar_length/2, ymax=i + bar_length/2, color='red', linewidth=1.5)
    ax.vlines(x=gini_disposable, ymin=i - bar_length/2, ymax=i + bar_length/2, color='blue', linewidth=1.5)

for i, (country, year) in enumerate(zip(sorted_closest_data['country'], sorted_closest_data['year'])):
    year_annotation = '' if year == target_year else f' (in {year})'
    ax.text(0, i, f'{country}{year_annotation}', ha='right', va='center', alpha=0.7, fontsize=8)

for i, (gini_disposable, gini_market) in enumerate(zip(
    sorted_closest_data['gini_disposable'],
    sorted_closest_data['gini_market']
)):
    ax.text(gini_disposable + 0.002, i, f'{gini_disposable:.2f}', ha='left', va='center', color='blue', alpha=0.7, fontsize=8)
    ax.text(gini_market + 0.002, i, f'{gini_market:.2f}', ha='left', va='center', color='red', alpha=0.7, fontsize=8)

ax.yaxis.set_visible(False)
ax.set_xlabel('Gini Coefficient')
ax.set_title(f'Gini Coefficient of Market vs Disposable Income (Closest to {target_year} – working age pop: {working_age_pop_only})', fontsize=16)
ax.xaxis.grid(True, linestyle='--', which='major', color='grey', alpha=.25)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()

plt.savefig(svg_chart_path, format='svg')
plt.show()
#%%


