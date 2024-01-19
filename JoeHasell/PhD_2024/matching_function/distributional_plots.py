#%% 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plot_income_distribution(file_path, save_file_path, *country_years):
    # Load the data from the CSV file
    income_data = pd.read_csv(file_path)

    # Define the tick marks for the x-axis
    tick_values = [1, 2, 5, 10, 20, 50, 100, 200]

    # Adjusting the figure size for a 3:2 aspect ratio (width:height)
    fig_width = 10
    fig_height = fig_width * (2 / 3) * len(country_years)  # Adjusted based on the number of country-years

    # Creating the faceted plot
    fig, axes = plt.subplots(len(country_years), 1, figsize=(fig_width, fig_height), sharex=True)

    for i, (country, year) in enumerate(country_years):
        # Filter the data for each specified country and year
        filtered_data = income_data[(income_data['Entity'] == country) & (income_data['Year'] == year)]

        # Plotting the country's income distribution
        sns.kdeplot(np.log(filtered_data['percentile_value']), ax=axes[i], bw_adjust=0.5)
        axes[i].set_title(f'{country} - {year}')
        axes[i].set_xticks(np.log(tick_values))
        axes[i].grid(True)

        # Setting labels for the last subplot (common x-axis)
        if i == len(country_years) - 1:
            axes[i].set_xticklabels(tick_values)
            axes[i].set_xlabel('Income')

    plt.tight_layout()

    # Save the plot as an SVG file
    plt.savefig(save_file_path, format='svg')

    plt.show()

#%% 
# Example usage of the function
file_path = 'percentiles.csv'  # Replace with your file path
save_to = 'dist_plot.svg'
plot_income_distribution(file_path, save_to, ("Ethiopia", 2015), ("Bangladesh", 2016), ("Vietnam", 2018), ("Turkiye", 2017), ("United States", 2019))
#%% 