import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import re

# Filepath
file_path = ""

# 2020 US CDC Wonder data
infant_2020 = pd.read_csv(file_path + "Linked Birth  Infant Death Records, 2017-2020 Expanded.txt", delimiter="\t")

# Rename columns
infant_2020.columns = ["Notes", "Age_days", "Age_code", "Deaths", "Births", "Death_rate"]

# Remove string that says unreliable from Death_rate column
infant_2020['Death_rate'] = infant_2020['Death_rate'].str.replace(r' \(Unreliable\)', '', regex=True)

# Convert Death_rate to numeric
infant_2020['Death_rate'] = pd.to_numeric(infant_2020['Death_rate'], errors='coerce')

# PLOT 1: Daily mortality rates across the first year, per 1,000 births
# Plotting
fig, ax = plt.subplots(figsize=(15, 12))

sns.scatterplot(data=infant_2020, x='Age_code', y='Death_rate', ax=ax, s=10)

ax.set_yscale('log')
ax.set_ylim(0.001, 10)
ax.set_xlim(0, 360)
ax.set_yticks([0.001, 0.01, 0.1, 1, 10])
ax.get_yaxis().set_major_formatter(plt.ScalarFormatter())

# Set x-axis breaks
ax.set_xticks([0, 60, 120, 180, 240, 300, 360])

# Formatting and labels
ax.set_title("Infant mortality rates decline sharply after birth", fontsize=16, fontweight='bold')
ax.set_xlabel("Age (days)", fontsize=14)
ax.set_ylabel("Mortality rate (per 1,000)", fontsize=14)
subtitle = "The chances of dying are highest during the first few days of an infant's life.\nOver the following days, weeks and months, their chances of dying decrease sharply.\nOver time, the mortality rate has declined across the entire first year of an infant's life."
fig.text(0.5, -0.08, subtitle, ha='center', fontsize=12)
ax.annotate("Source: US Centers for Disease Control and Prevention.", (0,0), (0, -45), xycoords='axes fraction', textcoords='offset points', va='top', fontsize=10)

# Save plot
plt.tight_layout()
plt.savefig(file_path + "daily_infant_mortality_US.png")
plt.show()


# Cumulative deaths calculation
infant_2020['Cumulative_deaths'] = infant_2020['Deaths'].cumsum()

# PLOT 2: Cumulative share of infants who have died by a given age
# Plotting
fig, ax = plt.subplots(figsize=(15, 12))

# Plot the line
ax.plot(infant_2020['Age_code'], infant_2020['Cumulative_deaths'] / infant_2020['Births'], color="#b16214", linewidth=1.5)

# Setting y-axis to percent format
def to_percent(y, position):
    return f"{100 * y:.3f}%"

from matplotlib.ticker import FuncFormatter
formatter = FuncFormatter(to_percent)
ax.yaxis.set_major_formatter(formatter)

# Setting breaks for y and x axis
ax.set_yticks(np.arange(0, 0.0061, 0.001))
ax.set_xticks(np.arange(0, 361, 60))

# Axis labels and title
ax.set_xlabel("Age (days)")
ax.set_ylabel("")
ax.set_title("Share of infants who have died over the first year", fontweight='bold')
ax.text(0, -0.0008, "The cumulative share of infants who have died by a given age.\nBased on US infant mortality rates between 2017-2020, using death certificates.", fontsize=10)
ax.text(0, -0.0011, "Source: US Centers for Disease Control and Prevention.", fontsize=9)

# Ensure data view limits are set
ax.set_xlim(0, 360)
ax.set_ylim(0, 0.006)

plt.tight_layout()
plt.savefig(file_path + "cumulative_infant_mortality_US.svg")
plt.show()

