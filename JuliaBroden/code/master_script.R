rm(list = ls())
library(stringr)
library(dplyr)
library(readr)
library(purrr)

join <- list.files(path = "/Users/Julia/Documents/OWID/R/transformed",
                   pattern = "*.csv", full.names = T) %>% 
  lapply(read_csv) %>% 
  reduce(full_join, by = c('Entity', 'Year')) %>% 
  rename(entity = Entity, year = Year)

path <- "/Users/Julia/Documents/OWID/R"
write_csv(join, file.path(path, 'output/AI_index_22_11_12.csv'), na = "")

#setwd("~/Documents/OWID/R")