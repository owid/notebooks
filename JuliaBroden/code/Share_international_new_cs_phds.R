rm(list = ls())
library(stringr)
library(googlesheets4)
library(dplyr)
library(readr)
library(tidyr)

sheet_url <- "https://docs.google.com/spreadsheets/d/1rfIoVslO0vJjtZBYL8qMmUZLgbaNXS76sQaJZkn9Nx4/edit#gid=407251975"

df1 <- read_sheet(sheet_url, range = "B1:R1", col_names = F)
df2 <- read_sheet(sheet_url, range = "B36:R36", col_names = F)
df <- as.data.frame(t(rbind(df1, df2)))
df$Entity <- "World"

df <- df %>% 
  rename(Year = V1, share_international_new_cs_phds = V2) %>% 
  relocate(Entity, Year)

write_csv(df, "transformed/share_international_new_cs_phds.csv")
