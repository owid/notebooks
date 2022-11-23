rm(list = ls())
library(stringr)
library(googlesheets4)
library(dplyr)
library(readr)

# Fig 2.6.1 Atari-57
sheet_url <- "https://docs.google.com/spreadsheets/d/1C1aJ9TVVCYDvRHsf3i8fhFCm7UhjqO1J7AWoSXyM--U/edit#gid=573863021"

df <- read_sheet(sheet_url, sheet = 35)

df <- df %>% 
  select(-Source) %>%
  rename(Entity = 'Model', mean_normalized_human_score = 'Mean-Normalized Human Score') %>%
  relocate(Entity, Year)

write_csv(df, "transformed/Atari.csv")
