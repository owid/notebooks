rm(list = ls())
library(stringr)
library(dplyr)
library(readr)

df <- read.csv(file = 'OpenAI/efficiency_sota_open_ai.csv')

reference_date <- mdy("01/01/2020")

df <- df %>% 
  filter(Metric == 'AlexNet') %>% 
  select(-Metric, -Publication.link, -Analysis, -Analysis.link) %>% 
  rename(Entity = 'Publication', training_computation_teraflop_s_days = 'Compute..teraflops.s.days.', 
         reduction_factor = 'Reduction.Factor',
         Year = 'Publication.Date') %>% 
  mutate(Year = difftime(mdy(Year), reference_date, units = "days")) %>%
  relocate(Entity, Year)

write_csv(df, "OpenAI/efficiency_sota.csv")
