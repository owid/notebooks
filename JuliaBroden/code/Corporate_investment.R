rm(list = ls())
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

### Adjust for inflation

# We adjust for inflation based on the US CPI for 2021
# For full explanation see https://github.com/owid/owid-issues/issues/621#issuecomment-1291179760
cpi <- read_csv("https://owid.cloud/api/variables/446013.csv") %>%
  filter(Entity == "United States") %>%
  rename(cpi = `Consumer price index (2010 = 100)`) %>%
  select(Year, cpi)

# Adjust CPI values so that 2021 is the reference year (2021 = 100)
cpi_2021 <- cpi %>% filter(Year == 2021) %>% pull(cpi)
cpi <- cpi %>% mutate(cpi = 100 * cpi / cpi_2021)

# Merge df with CPI data
df <- left_join(df, cpi, by = "Year")

# Adjust total_corporate_investment_by_activity for inflation
df <- df %>%
  mutate(total_corporate_investment_by_activity_inflation_adjusted = round(100 * total_corporate_investment_by_activity / cpi)) %>%
  select(-cpi)

write_csv(df, "transformed/Corporate_investment_ai.csv")

# Total corporate investment 
df_total <- df %>% 
  group_by(Year) %>% 
  summarise(total_corporate_investment = sum(total_corporate_investment_by_activity), 
                                             total_corporate_investment_inflation_adjusted = 
                                               sum(total_corporate_investment_by_activity_inflation_adjusted))

df_total$Entity <- "World"

df_total <- df_total %>% relocate(Entity, Year)

write_csv(df_total, "transformed/total_corporate_investment_ai.csv")
