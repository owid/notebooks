rm(list = ls())
library(stringr)
library(googlesheets4)
library(dplyr)
library(readr)
library(lubridate)
library(tidyr)

# Fig 4.1.2 Relative AI hiring index by geographic area
sheet_url <- "https://docs.google.com/spreadsheets/d/1gB9NAYtob2ZZci0oazqU0CeIh5syaJRPm_bok8ksLLM/edit#gid=1645662213"

df <- read_sheet(sheet_url, sheet = 2)

reference_date <- ymd("2020/01/01")

df <- df %>%
  rename(Year = 'Month-Year') %>%
  mutate(Year = difftime(ymd(Year), reference_date, units = "days")) %>%
  gather(Entity, growth_ai_hiring_smoothed, -Year) %>% 
  relocate(Entity, Year)

write_csv(df, "transformed/AI_hiring.csv")

# Fig 4.1.1
sheet_url <- "https://docs.google.com/spreadsheets/d/1gB9NAYtob2ZZci0oazqU0CeIh5syaJRPm_bok8ksLLM/edit#gid=0"

df2 <- read_sheet(sheet_url, sheet = 'Relative AI Hiring Index')

df2$Year <- 2021

df2 <- df2 %>%
  rename(Entity = `Country Geo`, growth_ai_hiring = `Relative AI Hiring Index (Dec 2021)`) %>%
  relocate(Entity, Year)

df2[2,1] <- 'Hong Kong'

write_csv(df2, "transformed/AI_hiring_rate.csv")
