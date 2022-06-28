library(plyr)
library(tidyverse)
library(readxl)
rm(list = ls())
setwd("~/git/notebooks/EdouardMathieu/global_terrorism_database/")

df <- read_excel("input/globalterrorismdb_0221dist.xlsx")

country_mapping <- read_csv("config/gtd_country_standardized.csv")

by_country <- df %>%
  mutate(country_txt = mapvalues(
    country_txt,
    from = country_mapping$Country,
    to = country_mapping$`Our World In Data Name`)
  ) %>%
  group_by(country_txt, iyear) %>%
  summarize(
    terrorist_incidents = n(),
    terrorism_fatalities = sum(nkill, na.rm = TRUE),
    terrorism_injuries = sum(nwound, na.rm = TRUE)
  ) %>%
  rename(entity = country_txt)

# by_country %>% select(entity) %>% distinct %>% rename(Country = entity) %>%
#   write_csv("config/countries_to_standardize.csv")

by_region <- df %>%
  group_by(region_txt, iyear) %>%
  summarize(
    terrorist_incidents = n(),
    terrorism_fatalities = sum(nkill, na.rm = TRUE),
    terrorism_injuries = sum(nwound, na.rm = TRUE)
  ) %>%
  rename(entity = region_txt)

world <- df %>%
  group_by(iyear) %>%
  summarize(
    terrorist_incidents = n(),
    terrorism_fatalities = sum(nkill, na.rm = TRUE),
    terrorism_injuries = sum(nwound, na.rm = TRUE)
  ) %>%
  mutate(entity = "World")

output <- bind_rows(by_country, by_region, world) %>%
  rename(year = iyear)

write_csv(output, "output/Global Terrorism Database.csv")
