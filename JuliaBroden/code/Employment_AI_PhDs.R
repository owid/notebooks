rm(list = ls())
library(stringr)
library(googlesheets4)
library(dplyr)
library(readr)
library(tidyr)

# Employment AI PhDs Fig 4.4.5
sheet_url <- "https://docs.google.com/spreadsheets/d/1rfIoVslO0vJjtZBYL8qMmUZLgbaNXS76sQaJZkn9Nx4/edit#gid=0"

df <- read_sheet(sheet_url)
df <- df[c(59:60, 62, 64), ]

# To Do: Create variables for the share of total of each of these; name as: share_ai_phds_employed_academia (etc.)

df <- df %>% 
  pivot_longer(!"...1", names_to = "Year") %>% pivot_wider(names_from = "...1") %>% 
  rename(number_ai_phds_employed_academia = 'Total AI to Academia', number_ai_phds_employed_government = 'AI to Government', 
         number_ai_phds_employed_industry = 'AI to Industry', total_number_ai_phds_employed = 'Total AI With Employment Data') %>% 
  mutate(Entity = "North America",
         share_ai_phds_employed_academia = number_ai_phds_employed_academia/total_number_ai_phds_employed, 
         share_ai_phds_employed_government = number_ai_phds_employed_government/total_number_ai_phds_employed,
         share_ai_phds_employed_industry = number_ai_phds_employed_industry/total_number_ai_phds_employed) %>% 
  relocate(Entity, Year)

write_csv(df, "transformed/Employment_AI_PhDs.csv")
