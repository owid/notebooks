rm(list = ls())
library(stringr)
library(googlesheets4)
library(dplyr)
library(readr)

sheet_url <- "https://docs.google.com/spreadsheets/d/1C1aJ9TVVCYDvRHsf3i8fhFCm7UhjqO1J7AWoSXyM--U/edit#gid=1172956859"

df <- read_sheet(sheet_url, sheet = 'ImageNet: Training Cost')

df <- df %>%
  rename(imagenet_training_cost_usd = `Cost (USD)`) %>%
  mutate(Entity = "AI system") %>%
  select(-Cost) %>% 
  relocate(Entity, Year)

write_csv(df, "transformed/Imagenet_training_cost.csv")
