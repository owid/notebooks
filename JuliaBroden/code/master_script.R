rm(list = ls())
library(stringr)
library(dplyr)
library(readr)
library(purrr)

## Merge AI publications and patent  ------------------------------------------
ai_publ <- read.csv(file = '/Users/Julia/Documents/OWID/R/transformed/AI_publications.csv')
patent <- read.csv(file = '/Users/Julia/Documents/OWID/R/transformed/Patent_Filings.csv')

df <- merge(ai_publ, patent, by = c('Entity', 'Year'), all = T)
write_csv(df, "AI_publications_Patent_filings_merged.csv")

## Reusable code -------------------------------------------------------------
# Set working directory to folder which contains transformed csv files
setwd("~/Documents/OWID/R/transformed")

mf <- list.files(pattern="*.csv") %>%
  map_df(~read_csv(.))

path <- "/Users/Julia/Documents/OWID/R/output"
write_csv(mf, file.path(path, 'master.csv'), na = "")




