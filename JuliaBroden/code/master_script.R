rm(list = ls())
library(stringr)
library(dplyr)
library(readr)
library(purrr)

join <- list.files(path = "/Users/Julia/Documents/OWID/Clone/JuliaBroden/transformed",
                   pattern = "*.csv", full.names = T) %>% 
  lapply(read_csv) %>% 
  reduce(full_join, by = c('Entity', 'Year')) %>% 
  rename(entity = Entity, year = Year)

path <- "/Users/Julia/Documents/OWID/Clone/JuliaBroden"
write_csv(join, file.path(path, 'output/AI_index_22_11_29.csv'), na = "") 

# for the variables total_corporate_investment and total_corporate_investment_inflation_adjusted we get a rounding error in the staging server