library(rio)
library(stringr)
library(data.table)
library(lubridate)
library(plyr)

URL <- "https://yougov.co.uk/_pubapis/v5/uk/trackers/dietery-choices-of-brits-eg-vegeterian-flexitarian-meat-eater-etc/download/"

# Function to process sheet data for a given age group, including data cleaning and normalization
get_sheet_data <- function(age_group) {
  message(age_group)

  # Import the specific sheet for the age group
  df <- rio::import(URL, format = "xlsx", sheet = age_group)
  setDT(df)

  # Clean and process the data
  setnames(df, "Which of these best describes your diet?", "Entity")
  df <- df[!Entity %in% c("Base", "Unweighted base")]

  # Clean up Entity names by removing text in parentheses
  df[, Entity := str_replace(Entity, " \\(.*", "")]

  # Transpose the data for better structure
  df <- transpose(df, make.names = TRUE, keep.names = "Year")

  # Normalize age group names
  df[, Entity := mapvalues(
    age_group,
    c("All adults", "18-24", "25-49", "50-64", "65+"),
    c("All adults", "18-24y", "25-49y", "50-64y", "65y+"),
    warn_missing = FALSE
  )]
  
  # Calculate the proportion of each dietary choice by dividing by the total and rounding
  df[, total := `Plant-based / Vegan` + Vegetarian + Flexitarian + Pescetarian + `Meat eater` + `None of these`]
  df[, `Plant-based / Vegan` := round(`Plant-based / Vegan` / total, 2)]
  df[, Vegetarian := round(Vegetarian / total, 2)]
  df[, Flexitarian := round(Flexitarian / total, 2)]
  df[, Pescetarian := round(Pescetarian / total, 2)]
  df[, `Meat eater` := round(`Meat eater` / total, 2)]
  df[, `None of these` := round(`None of these` / total, 2)]
  df[, total := NULL]
  
  return(df)
}

# Define the age groups to be processed
age_groups <- c("All adults", "18-24", "25-49", "50-64", "65+")

# Combine data from all age groups into a single data frame
df <- rbindlist(lapply(age_groups, get_sheet_data))

# Order columns for readability and consistency, and convert Year to an integer representing days since a baseline date
setcolorder(df, c("Entity", "Year"))
df[, Year := as.integer(ymd(Year) - ymd("20190101"))]

fwrite(df, "YouGov - Dietary choices of Brits.csv")
