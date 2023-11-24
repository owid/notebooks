import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Data folder
data_folder = ""

# Data source:
# https://www.mortality.org/
# Choose countries, then go to Cohort data > Death Rates > 1x1
# set filename to cMx_1x10_(name of country).txt
# Choose countries, then go to Period data > Death Rates > 1x1
# set filename to Mx_1x10_(name of country).txt

# List of countries
countries = ["FRA"]
cohort_mortality = {}
period_mortality = {}

# Import cohort data
for country in countries:
    cohort_mortality[country] = pd.read_csv(f"{data_folder}cMx_1x1_{country}.txt", skiprows=2, delim_whitespace=True, na_values=".")
    cohort_mortality[country].columns = ["Year", "Age", "Female", "Male", "Total"]
    cohort_mortality[country]['Country'] = country
    cohort_mortality[country]['Type'] = "Cohort"

# Import period data
for country in countries:
    period_mortality[country] = pd.read_csv(f"{data_folder}Mx_1x1_{country}.txt", skiprows=2, delim_whitespace=True, na_values=".")
    period_mortality[country].columns = ["Year", "Age", "Female", "Male", "Total"]
    period_mortality[country]['Country'] = country
    period_mortality[country]['Type'] = "Period"

# Combine cohort and period data
cohort_mortality_df = pd.concat(cohort_mortality.values(), ignore_index=True)
period_mortality_df = pd.concat(period_mortality.values(), ignore_index=True)

# Melt DataFrame to long format
cohort_mortality_df = cohort_mortality_df.melt(id_vars=['Year', 'Age', 'Country', 'Type'], var_name='Sex', value_name='Rate', value_vars=['Female', 'Male', 'Total'])
period_mortality_df = period_mortality_df.melt(id_vars=['Year', 'Age', 'Country', 'Type'], var_name='Sex', value_name='Rate', value_vars=['Female', 'Male', 'Total'])

mortality_df = pd.concat([cohort_mortality_df, period_mortality_df], ignore_index=True)

# Filter data for specific years and retain only 'Total'
years = [1910, 1918, 1920, 1930, 1940]
mortality_years = mortality_df[(mortality_df['Year'].isin(years)) & (mortality_df['Sex'] == 'Total')]

# Count unique years to determine the number of colors needed
n_colors = mortality_years['Year'].nunique()

# Create a palette
palette = sns.color_palette("Set2", n_colors)

# Plot comparison between cohort and period mortality rates
# Plot with Seaborn and use facetting with 'Type' to separate Cohort and Period data
g = sns.relplot(data=mortality_years, x='Age', y='Rate', hue='Year', col='Type', kind='line', palette=palette, facet_kws={'xlim': (0, 95)})

# Set y-axis to log scale
for ax in g.axes.flat:
    ax.set_yscale('log')

plt.suptitle('Annual death rate by age')
plt.subplots_adjust(top=0.9)  # Adjust title position
plt.savefig("period-cohort-age-specific-mortality.png")
plt.show()
