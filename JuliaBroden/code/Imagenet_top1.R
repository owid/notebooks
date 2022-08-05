rm(list = ls())
library(stringr)
library(googlesheets4)
library(dplyr)
library(readr)

sheet_url <- "https://docs.google.com/spreadsheets/d/1C1aJ9TVVCYDvRHsf3i8fhFCm7UhjqO1J7AWoSXyM--U/edit#gid=480995261"

### Version 1: With or without extra training data as entity

# df <- read_sheet(sheet_url)
# 
# df <- df %>% 
#   rename(c(Entity = `Type`, Top5_accuracy = `Top-5 Accuracy`)) %>%
#   mutate(Entity = str_to_sentence(Entity)) %>%
#   relocate(Entity, Year, Top5_accuracy, Method)
# 
# write_csv(df, "Imagenet_top1_V1.csv")

### Version 2: Method as entity

df2 <- read_sheet(sheet_url, sheet = "ImageNet: Top-1 Accuracy")

df2 <- df2 %>% 
  select(-Source) %>%
  rename(Entity = Method, Top1_accuracy = `Top-1 Accuracy`, Imagenet_extra_training_data = Type) %>%
  mutate(Entity = str_to_sentence(Entity)) %>%
  relocate(Entity, Year, Top1_accuracy, Imagenet_extra_training_data)

write_csv(df2, "transformed/Imagenet_top1_V2.csv")
