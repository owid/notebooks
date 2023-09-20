import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Data source:
# https://www.mortality.org/
# Replace this with path to folder where you saved it
data_folder = ""
# Replace with names of countries
countries = ["Italy", "Sweden"]
mortality = {}

# Import data
for country in countries:
    # Import and rename cols
    path = f"{data_folder}cMx_1x10_{country}.txt"
    mortality[country] = pd.read_csv(path, delim_whitespace=True, skiprows=2, names=["Year", "Age", "Female", "Male", "Total"])
    mortality[country]['Country'] = country

# Join into single df
mortality_df = pd.concat(mortality.values())

# Convert to correct datatypes
mortality_df['Age'] = pd.to_numeric(mortality_df['Age'], errors='coerce')
mortality_df['Year'] = mortality_df['Year'].astype(str)
mortality_df = pd.melt(mortality_df, id_vars=['Year', 'Age', 'Country'], value_vars=['Female', 'Male', 'Total'], var_name='Demographic', value_name='Rate')
mortality_g_total = mortality_df[mortality_df['Demographic'] == "Total"]

# Log transformation of Rate for plotting
mortality_g_total['Rate'] = pd.to_numeric(mortality_g_total['Rate'], errors='coerce')
mortality_g_total = mortality_g_total.dropna(subset=['Rate'])
mortality_g_total = mortality_g_total[mortality_g_total['Rate'] > 0].reset_index(drop=True)
mortality_g_total['Log_Rate'] = np.log2(mortality_g_total['Rate'])


plt.figure(figsize=(12, 6))

# Create a color palette
n_colors = mortality_g_total['Year'].nunique()
colors = sns.color_palette("viridis", n_colors)
color_dict = dict(zip(mortality_g_total['Year'].unique(), colors))

# Line plot for each year's data
sns.lineplot(data=mortality_g_total, x='Age', y='Rate', hue='Year', palette=color_dict, alpha=0.5)

# Scatter plot for age 0 points
age_zero_data = mortality_g_total[mortality_g_total['Age'] == 0]
sns.scatterplot(data=age_zero_data, x='Age', y='Rate', hue='Year', palette=color_dict, legend=False, edgecolor='black')

# Set the y-axis scale to log2 and customize the appearance
plt.yscale('log', base=2)
plt.yticks([0.0001, 0.001, 0.01, 0.1, 1], ['0.01%', '0.1%', '1%', '10%', '100%'])
plt.ylim(0.0001, 1)

# Add title and labels
plt.title("Annual death rate by age")
plt.xlabel("Age")
plt.ylabel("Death rate (log2 scale)")

# Add grid and facet by Country
g = sns.FacetGrid(mortality_g_total, row="Country", margin_titles=True)
g.map_dataframe(sns.lineplot, x='Age', y='Rate', hue='Year', palette=color_dict, alpha=0.5)
g.map_dataframe(sns.scatterplot, data=age_zero_data, x='Age', y='Rate', hue='Year', palette=color_dict, edgecolor='black', legend=False)
g.set(yscale="log", base=2)
g.set(yticks=[0.0001, 0.001, 0.01, 0.1, 1], yticklabels=['0.01%', '0.1%', '1%', '10%', '100%'])

plt.show()

