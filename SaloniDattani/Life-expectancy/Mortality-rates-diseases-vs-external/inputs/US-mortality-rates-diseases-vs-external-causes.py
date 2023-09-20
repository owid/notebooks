import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Data source:
# CDC Wonder https://wonder.cdc.gov/
# 1. Underlying cause of death - group by single age - group by ICD chapter (By cause)
# 2. Underlying cause of death - group by single age (All causes)
# Download and replace this with path to folder
data_folder = ""

# Data Import
# Import all cause age-specific mortality
all_causes = pd.read_csv(f"{data_folder}underlying-cod-2018-2021-all-causes.txt", delimiter='\t', dtype=str)
all_causes = all_causes.replace('"', '', regex=True)

all_causes = all_causes.rename(columns={
    'Single-Year Ages Code': 'Age',
    'Crude Rate': 'Crude_rate'
})
all_causes['ICD_chapter'] = "All causes"
all_causes['ICD_chapter_code'] = "ALL"

all_causes['Age'] = pd.to_numeric(all_causes['Age'], errors='coerce')
all_causes['Deaths'] = pd.to_numeric(all_causes['Deaths'], errors='coerce')
all_causes['Population'] = pd.to_numeric(all_causes['Population'], errors='coerce')
all_causes['Crude_rate'] = pd.to_numeric(all_causes['Crude_rate'], errors='coerce')

all_causes = all_causes[(all_causes['Age'] >= 0) & (all_causes['Age'] <= 100)]

# Import age-specific mortality by ICD chapter
by_cause = pd.read_csv(f"{data_folder}underlying-cod-2018-2021-by-cause.txt", delimiter='\t', dtype=str)
by_cause = by_cause.replace('"', '', regex=True)

by_cause = by_cause.rename(columns={
    'Single-Year Ages Code': 'Age',
    'Crude Rate': 'Crude_rate',
    'ICD Chapter': 'ICD_chapter',
    'ICD Chapter Code': 'ICD_chapter_code'
})

by_cause['Age'] = pd.to_numeric(by_cause['Age'], errors='coerce')
by_cause['Deaths'] = pd.to_numeric(by_cause['Deaths'], errors='coerce')
by_cause['Population'] = pd.to_numeric(by_cause['Population'], errors='coerce')
by_cause['Crude_rate'] = pd.to_numeric(by_cause['Crude_rate'], errors='coerce')

by_cause = by_cause[(by_cause['Age'] >= 0) & (by_cause['Age'] <= 100)]

# Create category for disease-related
disease_related = by_cause[
    ~by_cause['ICD_chapter'].isin([
        "External causes of morbidity and mortality",
        "Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified"
    ])
].groupby('Age').agg({
    'Deaths': 'sum',
    'Population': 'min'
})
disease_related['ICD_chapter'] = "Disease related"
disease_related['Crude_rate'] = (disease_related['Deaths'] / disease_related['Population']) * 100000

# Joining data
mx_age = pd.concat([all_causes, by_cause, disease_related], ignore_index=True)

# Filter specific ICD chapters
mx_age = mx_age[
    mx_age['ICD_chapter'].isin([
        "All causes",
        "Disease related",
        "External causes of morbidity and mortality"
    ])
]
mx_age['ICD_chapter'] = mx_age['ICD_chapter'].replace(
    {"External causes of morbidity and mortality": "External causes"}
)

# Plotting
group_colors = {
    "All causes": "black",
    "Disease related": "#4C6A9C",
    "External causes": "#B16214"
}
linestyles = {
    "All causes": "-",
    "Disease related": "--",
    "External causes": "--"
}

plt.figure(figsize=(10, 6))
for cause, color in group_colors.items():
    subset = mx_age[mx_age['ICD_chapter'] == cause]
    plt.plot(subset['Age'], subset['Crude_rate'], color=color, linestyle=linestyles[cause], linewidth=1, label=cause)

plt.title("Annual mortality rate, per 100,000 people")
plt.xlabel("Age")
plt.ylabel("")
plt.legend()
plt.yscale('log')
plt.savefig(f"{data_folder}together_plot.svg")
plt.show()


