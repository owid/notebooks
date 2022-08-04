rm(list = ls())
library(stringr)
library(googlesheets4)
library(dplyr)
library(readr)

sheet_url <- "https://docs.google.com/spreadsheets/d/1HsBaNYXv4QR8DlIDqkMJaUx4fBy2N4bVX_Isfp7jUp8/edit#gid=0"

df <- read_sheet(sheet_url)

df <- df %>%
  rename(Entity = `Investment Activity`,
         `Total investment` = `Total Investment (in billions of U.S. Dollars)`) %>%
  mutate(`Total investment` = round(`Total investment` * 1e9),
         Entity = str_to_sentence(Entity)) %>%
  relocate(Entity, Year)

write_csv(df, "AI Index Report 2022 - Global corporate AI investment.csv")
