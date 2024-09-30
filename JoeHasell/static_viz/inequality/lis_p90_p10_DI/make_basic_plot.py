#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#%% Grab LIS data from OWID ETL

etl_path = 'grapher/lis/2024-06-13/luxembourg_income_study/luxembourg_income_study'
url = 'http://catalog.ourworldindata.org/' + etl_path + '.feather'

data = pd.read_feather(url)

#%%  Ensure the 'year' column is numeric and drop rows where 'year' is NaN
data['year'] = pd.to_numeric(data['year'], errors='coerce')
data_cleaned = data.dropna(subset=['year'])

#%% keep needed columns
keep_cols = ['country', 'year','thr_p90_dhi_eq','median_dhi_eq','thr_p10_dhi_eq', 'p90_p10_ratio_dhi_eq']
data_cleaned = data_cleaned[keep_cols].dropna()

#%% Keep latest year

# Sort by country and year, keeping the latest year for each country
data_sorted = data_cleaned.sort_values(by=['country', 'year'], ascending=[True, False])
# Drop duplicates to keep only the latest year per country
latest_per_country = data_sorted.drop_duplicates(subset=['country'], keep='first')


#%% Filter data for the specified countries
countries = ['South Africa', 'Brazil', 'China', 'Serbia', 'Uruguay', 'Poland', 'United Kingdom', 'United States', 'Norway']
filtered_data = latest_per_country[latest_per_country['country'].isin(countries)]


#%% Sort the data to match the specified order
filtered_data = filtered_data.set_index('country').loc[countries].reset_index()

#%% Divide the income values by 12 to express them per month
filtered_data['thr_p90_dhi_eq'] = filtered_data['thr_p90_dhi_eq'] / 12
filtered_data['median_dhi_eq'] = filtered_data['median_dhi_eq'] / 12
filtered_data['thr_p10_dhi_eq'] = filtered_data['thr_p10_dhi_eq'] / 12

#%% Export the plot data
filtered_data.to_csv('lis_p90_p10_median.csv')


#%% Prepare the positions for each country
positions = np.arange(len(filtered_data))

#%% Function to format y-axis ticks as currency with exact values like "$1,000"
def currency_format_exact(value, _):
    return f"${int(value):,}"

#%% Create the lollipop chart
fig, ax = plt.subplots(figsize=(10, 6))

for idx, row in enumerate(filtered_data.itertuples()):
    # Y-values: the income levels for P10, Median, and P90 (per month)
    y_values = [row.thr_p10_dhi_eq, row.median_dhi_eq, row.thr_p90_dhi_eq]
    # X-values: use the same x position for all three points
    x_values = [positions[idx]] * 3
    
    # Plot the individual points for P10, Median, and P90 using circular markers
    ax.scatter(x_values, y_values, color='blue', zorder=3, marker='o')

ax.set_xticks(positions)
country_labels_with_year = [f"{row.country} ({row.year})" for row in filtered_data.itertuples()]
ax.set_xticklabels(country_labels_with_year)

ax.set_yscale('log')
ax.set_yticks([100, 200, 500, 1000, 2000, 5000, 10000])
ax.get_yaxis().set_major_formatter(plt.FuncFormatter(currency_format_exact))

ax.set_ylabel('Income Level per Month (Log Scale)')
ax.set_title('Income Distribution (P10, Median, P90) per Month for Selected Countries (Latest Available Year)')


plt.tight_layout()

# Save the plot as an SVG file
plt.savefig("lis_p90_p10_lollipop.svg", format="svg")

plt.show()


# %%
