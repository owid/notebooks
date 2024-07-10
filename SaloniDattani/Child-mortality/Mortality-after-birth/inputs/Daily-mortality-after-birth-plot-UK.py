import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.interpolate import interp1d

file_path = ""

# 2021 data
# Data source: https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/childmortalitystatisticschildhoodinfantandperinatalchildhoodinfantandperinatalmortalityinenglandandwales
# 2021 data
infant_2021 = pd.read_excel(file_path + "cim2021deathcohortworkbook.xlsx", sheet_name=4, skiprows=9)

# Create daily mortality variables
infant_2021["Day 1"] = infant_2021["Early neonatal under 1 day mortality rate"]
infant_2021["Day 7"] = infant_2021["Early neonatal 1 day and under 1 week mortality rate"] / 6
infant_2021["Day 28"] = infant_2021["Late neonatal 1 week and under 4 weeks mortality rate"] / 21
infant_2021["Day 91"] = infant_2021["Postneonatal 4 weeks and under 3 months mortality rate"] / 63
infant_2021["Day 182"] = infant_2021["Postneonatal 3 months and under 6 months mortality rate"] / 91
infant_2021["Day 365"] = infant_2021["Postneonatal 6 months and under 1 year mortality rate"] / 182

# Convert to long format
infant_g_2021 = infant_2021.melt(id_vars=['Year'], value_vars=["Day 1", "Day 7", "Day 28", "Day 91", "Day 182", "Day 365"], 
                                 var_name="Age", value_name="Mortality")

# 1921 to 2013 data
# Data source: https://cy.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/childmortalitystatisticschildhoodinfantandperinatalchildhoodinfantandperinatalmortalityinenglandandwales/2013
infant_m = pd.read_excel(file_path + "cmstables2013correction.xls", sheet_name="Table 17", skiprows=19, header=None)

# Rename columns
columns = [
    "Year", "Under.1.year", "Under.4.weeks", "Under.1.week", "Under.1.day", 
    "One.day.and.under.1.week", "One.week.and.under.4.weeks", "Four.weeks.and.under.1.year", 
    "Four.weeks.and.under.3.months", "Three.months.and.under.6.months", "Six.months.and.under.1.year", 
    "Stillbirths", "Stillbirths.plus.deaths.under.1.week", "Stillbirths.plus.deaths.under.4.weeks", 
    "Stillbirths.plus.deaths.under.1.year"
]
infant_m.columns = columns

# Change to numeric
for column in columns:
    infant_m[column] = pd.to_numeric(infant_m[column], errors='coerce')

# Create daily mortality variables
# Assuming infant_m is your original dataframe
infant_n = infant_m.copy()  # Creating a copy to avoid modifying the original dataframe

# Create new columns
infant_n["Day 1"] = infant_n["Under.1.day"]
infant_n["Day 7"] = infant_n["One.day.and.under.1.week"] / 6
infant_n["Day 28"] = infant_n["One.week.and.under.4.weeks"] / 21
infant_n["Day 91"] = infant_n["Four.weeks.and.under.3.months"] / 63
infant_n["Day 182"] = infant_n["Three.months.and.under.6.months"] / 91
infant_n["Day 365"] = infant_n["Six.months.and.under.1.year"] / 182


# Convert to long format
infant_g = infant_n.melt(id_vars=['Year'], value_vars=["Day 1", "Day 7", "Day 28", "Day 91", "Day 182", "Day 365"], 
                         var_name="Age", value_name="Mortality")

# Filter data
infant_g = infant_g[infant_g['Year'] < 1980]

# Combine datasets
combined = pd.concat([infant_g, infant_g_2021])

# Age column: string to numeric
age_mapping = {
    "Day 1": 1, "Day 7": 7, "Day 28": 28, "Day 91": 91, "Day 182": 182, "Day 365": 365
}
combined['Age'] = combined['Age'].map(age_mapping).astype(int)

# Filter the dataframe
years_to_show = [1921, 1931, 1941, 1951, 1961, 1971, 1981, 1991, 2001, 2011, 2021]
combined = combined[combined["Year"].isin(years_to_show)]

# Convert Year to categorical
combined["Year"] = combined["Year"].astype('category')

# Colors
sunset = ["#fcde9c","#faa476","#f0746e","#e34f6f","#dc3977","#b9257a","#7c1d6f"]
unique_years = sorted(combined["Year"].unique())
color_count = len(unique_years)
colors = plt.cm.viridis(np.linspace(0, 1, color_count))  # Use Viridis colormap as an alternative

def interp_fun_by_year(year, df):
    subset_df = df[df["Year"] == year]
    log_x = np.log(subset_df["Age"].values + 1e-5)  # added a small constant to avoid log(0)
    log_y = np.log(subset_df["Mortality"].values + 1e-5)
    log_x_new = np.log(x_vals + 1e-5)
    log_y_new = np.interp(log_x_new, log_x, log_y)
    return np.exp(log_y_new)

# Plotting
fig, ax = plt.subplots(figsize=(15, 12))

x_vals = np.linspace(combined["Age"].min(), combined["Age"].max(), 1000)

for idx, year in enumerate(unique_years):
    subset_df = combined[combined["Year"] == year]
    ax.scatter(subset_df["Age"], subset_df["Mortality"], label=str(year), color=colors[idx], s=10)
    
    # Compute interpolated values using the function
    y_vals = interp_fun_by_year(year, combined)
    ax.plot(x_vals, y_vals, color=colors[idx])

ax.set_yscale('log')  # log scale for y-axis
ax.set_title("Infant mortality rates decline sharply after birth")
ax.set_xlabel("Age (days)")
ax.set_ylabel("Daily mortality rate (per 1,000 live births)")
ax.legend(title="Year")

plt.tight_layout()
plt.savefig(file_path + "daily_infant_mortality.png")
plt.show()
