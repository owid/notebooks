rm(list = ls())
library(stringr)
library(googlesheets4)
library(dplyr)
library(readr)

# Fig 4.1.3 share of ai jobs among all job postings
sheet_url <- "https://docs.google.com/spreadsheets/d/19UGjvQW-PcnWoHEPe9Wd1Eib5z6S5II7lu1tE92fK3M/edit#gid=114714324"

df <- read_sheet(sheet_url, sheet = 3)

df <- df %>%
  gather(Entity, AI_job_postings, -Year) %>%
  relocate(Entity, Year)

# percent or decimal?
write_csv(df, "AI_jobs.csv")
