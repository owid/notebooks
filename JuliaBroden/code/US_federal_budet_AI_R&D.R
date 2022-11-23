rm(list = ls())
library(stringr)
library(googlesheets4)
library(dplyr)
library(readr)
library(tidyr)

# US federal budget for nondefense AI R&D Fig 5.2.1 missing

# US DOD budget for AI-specific RDT&E Fig 5.2.2
sheet_url <- "https://docs.google.com/spreadsheets/d/1v3Rit642csazCeNsj8MjRIaPN2Q2JRXsvJU5kdRQ2MY/edit#gid=1247288154"
df <- read_sheet(sheet_url, sheet = 3)

df <- df[-18,]

df <- df %>%
  rename(Department = 'Row Labels', '2020' = 'Sum of FY2020 Funding', 
         '2021' = 'Sum of FY2021 Funding', '2022' = 'Sum of FY2022 Funding') %>%
  gather(Year, Sum_of_FY_funding_dollar, -Department) %>%
  mutate(Year = as.numeric(Year), Entity = "United States", Sum_of_FY_funding_dollar = 10^6 * Sum_of_FY_funding_dollar) %>% 
  relocate(Entity, Year) %>% 
  pivot_wider(names_from = "Department", values_from = "Sum_of_FY_funding_dollar") %>% 
  select_all(~gsub("\\s+|\\.", "_", .)) %>% 
  #select_all(tolower) %>% 
  rename_with(~paste0("Sum_of_FY_funding_dollar_", .), -c(Entity, Year))

write_csv(df, "transformed/US_DOD_budget_AI_specific_RDTE.csv")
