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
