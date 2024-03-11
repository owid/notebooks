
#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde

def plot_weighted_log_income_density(country_code, year, data):
    """
    Plots the weighted log-income density for a given country and year.

    Parameters:
    country_code (str): The country code.
    year (int): The year for which the plot is required.
    data (DataFrame): The dataset containing the income information.
    """

    # Column names for the specified year
    income_col = f'welf{year}'
    pop_col = f'pop{year}'

    # Check if the specified columns exist in the data
    if income_col not in data.columns or pop_col not in data.columns:
        raise ValueError(f"Data for the year {year} is not available in the dataset.")

    # Filter the data for the specified country and year
    country_data = data[data['code'] == country_code][['obs', income_col, pop_col]]

    # Log-transform the income data
    country_data['log_income'] = np.log(country_data[income_col] + 1e-9)

    # Calculate the weighted density
    weights = country_data[pop_col]
    data_for_kde = country_data['log_income']

    # Creating a Gaussian Kernel Density Estimate with weights
    kde = gaussian_kde(data_for_kde, weights=weights, bw_method=0.3)

    # Creating a range of values for which we want to estimate the density
    log_income_range = np.linspace(data_for_kde.min(), data_for_kde.max(), 1000)

    # Calculating the density for each value in the range
    density_values = kde(log_income_range)

    # Define the income values at which to place the ticks
    income_ticks = [1, 2, 5, 10, 20, 50, 100]

    # Plotting the weighted density plot
    plt.figure(figsize=(12, 6))
    plt.plot(np.exp(log_income_range), density_values, color='blue')  # Convert back to actual income scale
    plt.xscale('log')
    plt.xticks(income_ticks, income_ticks)
    plt.title(f'Weighted Log-Income Density Distribution in {country_code}, {year}')
    plt.xlabel('Income')
    plt.ylabel('Density')
    plt.grid(True)
    plt.show()

#%%
data_path = 'GlobalDist1000bins_1990-2019.csv'
data = pd.read_csv(data_path)
plot_weighted_log_income_density('USA', 1990, data)


#%% ############ Global distribution – imputing sythetic data


#%%

def plot_stacked_density_chart(data, year, threshold=0.5, output_filepath=None):
    """
    Plots the Proportional Stacked Density Chart in Logs, Grouped by Region 
    for a specified year from the provided dataframe.

    Args:
    data (DataFrame): The dataframe containing the data.
    year (int): The year for which to generate the chart.
    threshold (float): The lower bound for income values to be considered.
    """
    # Selecting the relevant columns for the specified year
    welf_column = f'welf{year}'
    pop_column = f'pop{year}'

    # Filtering the dataset for the specified year and ensuring income values are above the threshold
    data_year = data[['code', 'region_code', welf_column, pop_column]].copy()
    data_year[welf_column] = data_year[welf_column].clip(lower=threshold)

    # Define income intervals for the specified year
    income_intervals_year = np.arange(threshold, data_year[welf_column].max() + 0.1, 0.1)

    # Generating synthetic data for each country for the specified year
    synthetic_data_year = pd.DataFrame()

    for country in data_year['code'].unique():
        country_data = data_year[data_year['code'] == country]
        log_welf = np.log(country_data[welf_column])
        weights = country_data[pop_column]
        
        # KDE with original data
        kde = gaussian_kde(log_welf, weights=weights)
        
        # Evaluate the density on each interval
        density = kde(np.log(income_intervals_year)) * weights.sum()
        
        # Create synthetic data for this country
        synthetic_country_data = pd.DataFrame({
            'code': country,
            'region_code': country_data['region_code'].iloc[0],
            'welf': income_intervals_year,
            'density': density
        })
        synthetic_data_year = pd.concat([synthetic_data_year, synthetic_country_data])

    # Normalizing the densities for the specified year
    synthetic_data_year['density'] /= synthetic_data_year['density'].sum()

    # Assigning colors to each region
    regions_year = synthetic_data_year['region_code'].unique()
    color_palette_year = plt.cm.get_cmap('tab20', len(regions_year))
    region_colors_year = {region: color_palette_year(i) for i, region in enumerate(regions_year)}

    # Plotting the chart for the specified year
    plt.figure(figsize=(12, 8))
    cumulative_density_year = None

    # Group the synthetic data by region and then by country for the specified year
    grouped_synthetic_year = synthetic_data_year.groupby(['region_code', 'code'])

    for i, (group_info, group) in enumerate(grouped_synthetic_year):
        region = group_info[0]
        if cumulative_density_year is None:
            cumulative_density_year = group['density'].values
        else:
            cumulative_density_year += group['density'].values
        plt.fill_between(group['welf'], cumulative_density_year, 
                         cumulative_density_year - group['density'].values, 
                         label=f"{region}: {group_info[1]}", 
                         alpha=0.7, color=region_colors_year[region])

    # Customizing the plot for the specified year
    plt.title(f'Proportional Stacked Density Chart in Logs, Grouped by Region (Year {year})')
    plt.xlabel(f'Average Income (welf{year})')
    plt.ylabel('Adjusted Density')
    plt.xscale('log')
    plt.xticks([threshold, 1, 2, 5, 10, 20, 50, 100, 200], [threshold, 1, 2, 5, 10, 20, 50, 100, 200])
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    
     
    # Show and/or save the plot
    if output_filepath:
        plt.savefig(output_filepath, format='svg')
    plt.show()

#%%
# Example usage
data_path = 'GlobalDist1000bins_1990-2019.csv'
data = pd.read_csv(data_path)
plot_stacked_density_chart(data, 2000, threshold=0.3, output_filepath='test_plot.svg')  


# %%
