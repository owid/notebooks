rm(list = ls())
library(stringr)
library(googlesheets4)
library(dplyr)
library(readr)

sheet_url <- "https://docs.google.com/spreadsheets/d/1D_7XVaE4BK0DrEFRg0aLaQSYdGQ4YugA1OD3UPd4LMY/edit#gid=1620293967"

df <- read_sheet(sheet_url, sheet = 2)

df <- df %>%
  rename(c(Entity = `Field of Study`, Number_ai_publications = `Number of AI Publications`)) %>%
  relocate(Entity, Year)

df$Entity[df$Entity == "Human‚Äìcomputer interaction"] <- "Human-computer interaction"
  
write_csv(df, "AI_publications_by_field.csv")
