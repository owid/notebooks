import pandas as pd
import matplotlib.pyplot as plt

# Read data
data_folder = ""
# Data comes from the Human Mortality Database (pre-1950) and the UN World Population Projections (1950 onwards)
le_hmd = pd.read_csv(data_folder + "life-expectancy-males-vs-females.csv")
le_unwpp = pd.read_csv(data_folder + "female-and-male-life-expectancy-at-birth-in-years.csv")

hmd_countries = ["Australia", "Austria", "Belarus", "Belgium", "Canada", "Chile", "Croatia", "Czechia", "Denmark", "Estonia", "Finland", "France", "Germany", "Greece", "Hong Kong", "Hungary", "Iceland", "Ireland", "Israel", "Italy", "Japan", "Latvia", "Lithuania", "Luxembourg", "Netherlands", "New Zealand", "Norway", "Poland", "Portugal", "South Korea", "Russia", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland", "Taiwan", "United Kingdom", "United States", "Ukraine"]

# Rename cols
le_hmd.columns = ["Entity", "Code", "Year", "LE_Female", "LE_Male"]
le_unwpp.columns = ["Entity", "Code", "Year", "LE_Male", "LE_Female"]

# Use HMD dataset for life expectancy before 1950
# Use UN WPP dataset for life expectancy 1950 onwards
# Note that HMD dataset is missing some countries for very recent years because of delays - maybe because the website isnt fully updated or lifetables arent calculated yet, but we can use the UN WPP data for the same HMD countries anyway
# Otherwise it would wrongly look like the record life expectancy is always falling in the most recent years, due to delays.
le_hmd = le_hmd[le_hmd["Year"] < 1950]
le_unwpp = le_unwpp[le_unwpp["Year"] >= 1950]

le_joined = pd.concat([le_hmd, le_unwpp])

# Filter and process data
# Only include female life expectancy
# Only include HMD countries
# Only include data from after 1840
# Sort by Year, Life expectancy females, and retain only the country with the highest life expectancy.
le_record = (le_joined.drop(columns=["LE_Male"])
              .loc[le["Entity"].isin(hmd_countries) & (le["Year"] > 1840)]
              .sort_values(by=["Year", "LE_Female"])
              .groupby("Year").tail(1))

# Save dataset
le_record.to_csv(data_folder + "life-expectancy-record.csv", index=False)

### Horizontal lines
# Create dataframe of predictions of life expectancy: it contains the source of the prediction, their predicted limit of life expectancy, the year the prediction was made
predictions = pd.DataFrame({
    "Prediction_maker": ["UN", 
                                               "Frejka",
                                                  "Bourgeois-Pichat",
                                                  "Siegel",
                                                  "UN",
                                                  "Bourgeois-Pichat",
                                                  "World Bank", 
                                                  "UN",
                                                  "Coale & Guo",
                                                  "Coale",
                                                  "UN",
                                                  "Olshansky et al.",
                                                  "World Bank",
                                                  "UN"],
    "Prediction_limit": [77.5,
                                                  77.5,
                                                  78.2,
                                                  79.4,
                                                  80,
                                                  80.3,
                                                  82.5,
                                                  82.5,
                                                  84.9,
                                                  84.2,
                                                  87.5,
                                                  88,
                                                  90,
                                                  92.5],
    "Prediction_year_made": [1973,
                                                     1981,
                                                     1952,
                                                     1980,
                                                     1979,
                                                     1978,
                                                     1984,
                                                     1985,
                                                     1955,
                                                     1955,
                                                     1989,
                                                     2001,
                                                     1989,
                                                     1998]
})

# Add new columns 
# - year when prediction was broken
predictions["Year_Broken"] = predictions["Prediction_limit"].apply(
    lambda limit: le_record["Year"][le_record["LE_Female"] > limit].iloc[0] if len(le_record["LE_Female"][le_record["LE_Female"] > limit]) > 0 else None)

# - the current life expectancy record when the prediction was made
predictions["LE_Record_YearMade"] = predictions["Prediction_year_made"].apply(
    lambda year_made: le_record["LE_Female"][le_record["Year"] == year_made].iloc[0] if len(le_record["LE_Female"][le_record["Year"] == year_made]) > 0 else None)

# Set country colors
country_colors = {
    "Hong Kong": "#00894b",
    "Iceland": "#ec7333",
    "Japan": "#be2856",
    "Netherlands": "#ffca30",
    "Norway": "#e43638",
    "Sweden": "#00a5cc",
    "Denmark": "#ffe086",
    "Switzerland": "#c15065",
    "Belarus": "#58ac8c",
    "Australia": "#578145"
}

# Plot
fig, ax = plt.subplots(figsize=(10, 6))

# Plot records
ax.scatter(le_record["Year"], le_record["LE_Female"], c=le_record["Entity"].map(country_colors), edgecolors="black", linewidths=0.3)
# Plot predictions
ax.scatter(predictions["Prediction_year_made"], predictions["Prediction_limit"], marker="x", color="black")

ax.set_xlim([1950, 2025])
ax.set_ylim([70, 95])
ax.set_title("Record female life expectancy")
ax.set_ylabel("Life expectancy")

plt.legend(handles=[plt.Line2D([0], [0], marker='o', color='w', label=key, markersize=10, markerfacecolor=value) for key, value in country_colors.items()])

plt.savefig(data_folder + "record_female_life_expectancy-v1.svg")
plt.show()

# When was LE_x exceeded?
le_x = 88
print(le_record[le_record["LE_Female"] >= le_x].sort_values(by="Year").head(1))
