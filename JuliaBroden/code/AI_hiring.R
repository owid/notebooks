rm(list = ls())
library(stringr)
library(googlesheets4)
library(dplyr)
library(readr)

# Fig 4.1.2 Relative AI hiring index by geographic area
sheet_url <- "https://docs.google.com/spreadsheets/d/1gB9NAYtob2ZZci0oazqU0CeIh5syaJRPm_bok8ksLLM/edit#gid=1645662213"

df <- read_sheet(sheet_url, sheet = 2)

df <- df %>% rename(Year = 'Month-Year')

reference_date <- as.Date("2020/01/01")
df$Year <- as.Date(df$Year) # make sure it's a date type
df$Year <- difftime(df$Year, reference_date, units = "days")

df <- df %>%
  gather(Entity,Relative_ai_hiring_index, -Year) %>% 
  relocate(Entity, Year)

write_csv(df, "AI_hiring.csv")
