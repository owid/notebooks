rm(list = ls())
library(stringr)
library(googlesheets4)
library(dplyr)
library(readr)

### Top1 accuracy
sheet_url <- "https://docs.google.com/spreadsheets/d/1C1aJ9TVVCYDvRHsf3i8fhFCm7UhjqO1J7AWoSXyM--U/edit#gid=480995261"

df <- read_sheet(sheet_url, sheet = "ImageNet: Top-1 Accuracy")

df <- df %>% 
  select(-Source) %>%
  rename(Entity = Method, top1_accuracy = `Top-1 Accuracy`, imagenet_extra_training_data = Type) %>%
  mutate(Entity = str_to_sentence(Entity)) %>%
  relocate(Entity, Year, top1_accuracy, imagenet_extra_training_data)

df[12,1] <- "Vgg-19*"
df[13,1] <- "Inception v3*"

### Top5 accuracy
sheet_url <- "https://docs.google.com/spreadsheets/d/1C1aJ9TVVCYDvRHsf3i8fhFCm7UhjqO1J7AWoSXyM--U/edit#gid=586400223"

df2 <- read_sheet(sheet_url, sheet = 2)

df2 <- df2 %>% 
  select(-Source) %>%
  rename(Entity = Method, top5_accuracy = `Top-5 Accuracy`, imagenet_extra_training_data = Type) %>%
  mutate(Entity = str_to_sentence(Entity)) %>%
  relocate(Entity, Year, top5_accuracy, imagenet_extra_training_data)

### Merge
df3 <- merge(df, df2, by = c('Entity', 'Year', 'imagenet_extra_training_data'), all = T)
write_csv(df3, "transformed/Imagenet.csv")







