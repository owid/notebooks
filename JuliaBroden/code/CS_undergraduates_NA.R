rm(list = ls())
library(stringr)
library(googlesheets4)
library(dplyr)
library(readr)
library(tidyr)

sheet_url <- "https://docs.google.com/spreadsheets/d/1rfIoVslO0vJjtZBYL8qMmUZLgbaNXS76sQaJZkn9Nx4/edit#gid=407251975"

# New CS undergraduate graduates in NA Fig 4.4.1
df <- read_sheet(sheet_url) 

df <- df[14, 2:18]

df <- df %>%
  gather(Year, new_cs_undergraduate_graduates_at_doctoral_institutions) %>%
  mutate(Entity = "North America", Year = as.numeric(Year)) %>%
  relocate(Entity, Year)

write_csv(df, "transformed/CS_undergraduates_NA.csv")
