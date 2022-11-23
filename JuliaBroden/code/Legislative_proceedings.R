rm(list = ls())
library(stringr)
library(googlesheets4)
library(dplyr)
library(readr)

# Legislative proceedings Fig 5.1.9
sheet_url <- "https://docs.google.com/spreadsheets/d/1oZPYsTA83zZYapwDKvrs39A8CRoNv6YamNPJJZtOKzE/edit#gid=614387978"
df <- read_sheet(sheet_url, sheet = 2)

df <- df[-26,]

df <- df %>%
  rename(Entity = Country) %>%
  select(-Total) %>%
  gather(Year, number_mentions_AI_legislative_proceedings, -Entity) %>%
  mutate(Year = as.numeric(Year)) %>% 
  relocate(Entity, Year)

write_csv(df, "transformed/legislative_proceedings.csv")
