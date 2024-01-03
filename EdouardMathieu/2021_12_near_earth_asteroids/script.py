import pandas as pd
from datetime import datetime

# Source URL: https://cneos.jpl.nasa.gov/stats/totals.html
# Tab: Cumulative Totals
# Scroll down and click "CSV" under the table

# Load the CSV file
df = pd.read_csv(
    "Discovery StatisticsPrintDownload.csv",
    usecols=["Date", "NEA-km", "NEA-140m", "NEA"],
)

# Sort by Date in descending order
df["Date"] = pd.to_datetime(df["Date"])
df.sort_values(by="Date", ascending=False, inplace=True)

# Extract Year from Date
df["Year"] = df["Date"].dt.year

# Filter out data from the current year
current_year = datetime.now().year
df = df[df["Year"] < current_year]

# Keep only the latest record for each year
df = df.drop_duplicates(subset="Year")

# Calculate additional columns
df["larger_than_1km"] = df["NEA-km"]
df["between_140m_and_1km"] = df["NEA-140m"] - df["larger_than_1km"]
df["smaller_than_140m"] = df["NEA"] - df["larger_than_1km"] - df["between_140m_and_1km"]

# Add the 'Entity' column
df["Entity"] = "World"

# Select the final columns
df = df[
    ["Entity", "Year", "larger_than_1km", "between_140m_and_1km", "smaller_than_140m"]
]

# Write the final dataframe to CSV
output_file = "Near-Earth asteroids discovered over time.csv"
df.to_csv(output_file, index=False)
