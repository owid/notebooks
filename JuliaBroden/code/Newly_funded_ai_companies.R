rm(list = ls())
library(stringr)
library(googlesheets4)
library(dplyr)
library(readr)

# Newly funded ai companies
sheet_url <- "https://docs.google.com/spreadsheets/d/1HsBaNYXv4QR8DlIDqkMJaUx4fBy2N4bVX_Isfp7jUp8/edit#gid=2097439470"
df <- read_sheet(sheet_url, sheet = 'Newly Funded AI Companies')
df2 <- read_sheet(sheet_url, sheet = 'Newly Funded AI Companies by Geo (2021)')
df3 <- read_sheet(sheet_url, sheet = 'Newly Funded AI Companies by US/China/EU (2013-21)')

df$Entity <- "World"
df2$Year <- 2021
df2 <-df2 %>% 
  rename(Entity = 'Geographic Area')
df3 <-df3 %>% 
  rename(Entity = 'Geographic Area')

# Merge and save
df4 <- Reduce(function(x, y) merge(x, y, all=TRUE), 
              list(df, df2, df3))
df4 <- df4 %>% relocate(Entity, Year) %>% 
  rename(newly_funded_ai_companies = 'Number of Newly Funded AI Companies')
write_csv(df4, "transformed/Newly_funded_ai_companies.csv")
