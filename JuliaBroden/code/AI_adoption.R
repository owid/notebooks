rm(list = ls())
library(stringr)
library(googlesheets4)
library(dplyr)
library(readr)
library(tidyr)

sheet_url <- "https://docs.google.com/spreadsheets/d/1yaC2mzS-d5dekLrTen0NGm-0zvuPcMfFLwRRml0tyJ4/edit#gid=0"

# AI adoption by organizations Fig 4.3.1
df <- read_sheet(sheet_url)

#df <- df[-1,]

df <- df %>%
  rename(Entity = ...1) %>%
  gather(Year, share_companies_using_ai, -Entity) %>%
  mutate(Year = as.numeric(Year), share_companies_using_ai = share_companies_using_ai / 100)

write_csv(df, "transformed/adoption_organization.csv")

# AI adoption by industry Fig 4.3.2
df2 <- read_sheet(sheet_url, sheet = 3)

df2 <- df2 %>%
  rename(Entity = ...1) %>%
  mutate(Year = 2021) %>% 
  select_all(~gsub("\\s+|\\.", "_", .)) %>% 
  select_all(~gsub("/", "_", .)) %>% 
  rename_with(~paste0("Industry_", .), -c(Entity, Year)) %>% 
  relocate(Entity, Year)

write_csv(df2, "transformed/adoption_industry.csv")

# AI capabilities Fig 4.3.3
df3 <- read_sheet(sheet_url, sheet = 5)

df3 <- df3 %>%
  rename(Entity = "Industry") %>%
  mutate(Year = 2021) %>% 
  select_all(~gsub("\\s+|\\.", "_", .)) %>% 
  rename_with(~paste0("Industry_", .), -c(Entity, Year)) %>% 
  relocate(Entity, Year)

write_csv(df3, "transformed/adoption_capabilities.csv")
