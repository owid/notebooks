rm(list = ls())
library(stringr)
library(googlesheets4)
library(dplyr)
library(readr)
library(tidyr)

# Number AI bills Fig 5.1.1 - 5.1.2b)
sheet_url <- "https://docs.google.com/spreadsheets/d/1oZPYsTA83zZYapwDKvrs39A8CRoNv6YamNPJJZtOKzE/edit#gid=0"
df <- read_sheet(sheet_url)

df <- df %>%
  rename(Entity = Country) %>%
  select(-Total) %>%
  gather(Year, number_ai_bills, -Entity) %>%
  mutate(Year = as.numeric(Year)) %>% 
  relocate(Entity, Year) %>% 
  group_by(Entity) %>% 
  mutate(number_ai_bills_cumulative = cumsum(number_ai_bills)) %>% 
  select(-number_ai_bills)
  
write_csv(df, "transformed/AI_bills.csv")

# Fig 5.1.3 missing data