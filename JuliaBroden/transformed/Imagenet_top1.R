rm(list = ls())
library(stringr)
library(googlesheets4)
library(dplyr)
library(readr)

sheet_url <- "https://docs.google.com/spreadsheets/d/1C1aJ9TVVCYDvRHsf3i8fhFCm7UhjqO1J7AWoSXyM--U/edit#gid=480995261"

df <- read_sheet(sheet_url)

df <- df %>% 
  select(-c(Method,Source)) %>%
  rename(Entity = `Type`) %>%
  mutate(Entity = str_to_sentence(Entity)) %>%
  relocate(Entity, Year)

write_csv(df, "Imagenet_top1.csv")

             