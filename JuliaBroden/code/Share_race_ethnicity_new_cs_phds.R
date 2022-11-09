rm(list = ls())
library(stringr)
library(googlesheets4)
library(dplyr)
library(readr)
library(tidyr)

sheet_url <- "https://docs.google.com/spreadsheets/d/1rfIoVslO0vJjtZBYL8qMmUZLgbaNXS76sQaJZkn9Nx4/edit#gid=2124443447"

df <- read_sheet(sheet_url, sheet = 'New Computing PhD by Race/Ethnicity')

#total <- df[9,]
#dft <- mutate_each(funs(./.[9], setdiff(names(.), "share")))

df <- df %>% pivot_longer(cols = '2010':'2020', names_to = 'Year', values_to = 'share_race_ethnicity_new_cs_phds') %>% 
  rename(Entity = ...1)

write_csv(df, "transformed/share_race_ethnicity_new_cs_phds.csv") 
