rm(list = ls())
library(stringr)
library(googlesheets4)
library(dplyr)
library(readr)

sheet_url <- "https://docs.google.com/spreadsheets/d/1D_7XVaE4BK0DrEFRg0aLaQSYdGQ4YugA1OD3UPd4LMY/edit#gid=1620293967"

df <- read_sheet(sheet_url, sheet = 2)

df <- df %>%
  rename(c(Entity = `Field of Study`, number_ai_publications_by_field = `Number of AI Publications`)) %>%
  mutate(Entity = ifelse(Entity == "Human‚Äìcomputer interaction", "Human-computer interaction", Entity)) %>% 
  mutate(Entity = ifelse(Entity == "Other AI", "All other fields", Entity)) %>% 
  relocate(Entity, Year)

# Add Total entity
df2 <- df %>%
  group_by(Year) %>% 
  summarise(number_ai_publications_by_field = sum(number_ai_publications_by_field)) %>% 
  bind_rows(df, .)

df2$Entity[is.na(df2$Entity)] <- 'Total'

write_csv(df2, "transformed/AI_publications_by_field.csv")
