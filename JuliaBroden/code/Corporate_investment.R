rm(list = ls())
library(stringr)
library(googlesheets4)
library(dplyr)
library(readr)

# Global corporate investment Figure 4.2.1

sheet_url <- "https://docs.google.com/spreadsheets/d/1HsBaNYXv4QR8DlIDqkMJaUx4fBy2N4bVX_Isfp7jUp8/edit#gid=1022620627"

df <- read_sheet(sheet_url)

df <- df %>%
  rename(Entity = 'Investment Activity', total_corporate_investment_by_activity = `Total Investment (in billions of U.S. Dollars)`) %>%
  mutate(total_corporate_investment_by_activity = 10^9 * total_corporate_investment_by_activity) %>%
  relocate(Entity, Year)

write_csv(df, "transformed/Corporate_investment_ai.csv")

# Total corporate investment 
df2 <- df %>% 
  group_by(Year) %>% 
  summarise(total_corporate_investment = sum(total_corporate_investment_by_activity))

df2$Entity <- "World"

df2 <- df2 %>% relocate(Entity, Year)
write_csv(df2, "transformed/total_corporate_investment_ai.csv")
