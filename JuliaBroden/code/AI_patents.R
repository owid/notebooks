rm(list = ls())
library(stringr)
library(googlesheets4)
library(dplyr)
library(readr)

sheet_url <- "https://docs.google.com/spreadsheets/d/1D_7XVaE4BK0DrEFRg0aLaQSYdGQ4YugA1OD3UPd4LMY/edit#gid=872675196"

df <- read_sheet(sheet_url, sheet = 3)

df <- df %>% 
  rename(Entity = `Number of AI Patent Filings`) %>%
  mutate(Entity = str_to_sentence(Entity)) %>%
  relocate(Entity, Year)

write_csv(df, "Patent_Filings.csv")
