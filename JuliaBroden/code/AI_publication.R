rm(list = ls())
library(stringr)
library(googlesheets4)
library(dplyr)
library(readr)

sheet_url <- "https://docs.google.com/spreadsheets/d/1D_7XVaE4BK0DrEFRg0aLaQSYdGQ4YugA1OD3UPd4LMY/edit#gid=1620293967"

df <- read_sheet(sheet_url)

df$Entity <- "World"

df <- df %>%
  rename(number_ai_publications_by_country = `Number of AI Publications`) %>%
  mutate(Entity = str_to_sentence(Entity)) %>%
  relocate(Entity, Year)

write_csv(df, "transformed/AI_publications.csv")
