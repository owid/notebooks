rm(list = ls())
library(stringr)
library(googlesheets4)
library(dplyr)
library(readr)

# Private investment global Fig 4.2.2
sheet_url <- "https://docs.google.com/spreadsheets/d/1HsBaNYXv4QR8DlIDqkMJaUx4fBy2N4bVX_Isfp7jUp8/edit#gid=1022620627"

df <- read_sheet(sheet_url, sheet = 2)

df <- df %>%
  mutate(Entity = "World") %>%
  rename(Total_investment_billions_US_dollars = `Total Investment (in billions of U.S. Dollars)`) %>%
  relocate(Entity, Year)

# Private investment by geographic area Fig 4.2.4
df2 <- read_sheet(sheet_url, sheet = 4)

df2 <- df2 %>%
  rename(Entity = `Geographic Area`,
         Total_investment_billions_US_dollars = `Total Investment (in billions of U.S. Dollars)`)

# Private investment by focus area Fig 4.2.10
df3 <- read_sheet(sheet_url, sheet = 12)

df3 <-df3 %>% 
  mutate(Entity = "World") %>%
  rename(Total_investment_billions_US_dollars = `Total Investment (in billions of U.S. Dollars)`,
         Focus_area = `Focus Area`)

# Merge and save
df4 <- Reduce(function(x, y) merge(x, y, all=TRUE), 
                 list(df, df2, df3))
df4 <- df4 %>% relocate(Entity, Year)

write_csv(df4, "transformed/Private_investment_ai.csv")
