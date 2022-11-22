rm(list = ls())
library(googlesheets4)
library(dplyr)
library(readr)

# Private investment global Fig 4.2.2
sheet_url <- "https://docs.google.com/spreadsheets/d/1HsBaNYXv4QR8DlIDqkMJaUx4fBy2N4bVX_Isfp7jUp8/edit#gid=1022620627"

df <- read_sheet(sheet_url, sheet = 2)

df <- df %>%
  rename(total_private_investment_by_country = `Total Investment (in billions of U.S. Dollars)`) %>%
  mutate(Entity = "World", total_private_investment_by_country = 10^9 * total_private_investment_by_country) %>%
  relocate(Entity, Year)

# Private investment by geographic area Fig 4.2.4
df2 <- read_sheet(sheet_url, sheet = 4)

df2 <- df2 %>%
  rename(Entity = `Geographic Area`,
         total_private_investment_by_country = `Total Investment (in billions of U.S. Dollars)`) %>%
  mutate(total_private_investment_by_country = 10^9 * total_private_investment_by_country, Year = 2021) %>%
  relocate(Entity, Year)

# Private investment by focus area Fig 4.2.10
df3 <- read_sheet(sheet_url, sheet = 12)

df3 <-df3 %>% 
  rename(Entity = "Focus Area", total_private_investment_by_focus_area = `Total Investment (in billions of U.S. Dollars)`) %>%
  mutate(total_private_investment_by_focus_area = 10^9 * total_private_investment_by_focus_area) %>%
  relocate(Entity, Year)

df3 <- df3 %>%  
  group_by(Year) %>% 
  summarise(total_private_investment_by_focus_area = sum(total_private_investment_by_focus_area)) %>% 
  bind_rows(df3, .)

df3$Entity[is.na(df3$Entity)] <- "Total"

# Change entity names
df3 <- df3 %>% 
  mutate(Entity=recode(Entity, 'AR/VR' = 'Augmented Reality/Virtual Reality', 
                       'AV' = 'Audiovisual',
                       'Agritech' = 'Agricultural Tech',
                       'Ed Tech' = 'Educational Tech',
                       'Fintech' = 'Financial Tech',
                       'HR Tech' = 'Human Resources Tech',
                       'Insurtech' = 'Insurance Tech',
                       'NLP, Customer Support' = 'Natural Language, Customer Support',
                       'VC' = 'Venture Capital'))

# Private investment by geographic area Fig 4.2.6
df4 <- read_sheet(sheet_url, sheet = 'Private AI Investment by US/China/EU (2013-21)')
df4 <- df4 %>%
  rename(Entity = `Geographic Area`,
         total_private_investment_by_country = `Total Investment (in billions of U.S. Dollars)`) %>%
  mutate(total_private_investment_by_country = 10^9 * total_private_investment_by_country) %>%
  relocate(Entity, Year)

# Merge and save
df5 <- Reduce(function(x, y) merge(x, y, all=TRUE), 
              list(df, df2, df3, df4))
df5 <- df5 %>% relocate(Entity, Year)

# Take care of inconsistency in numbers for US 2021 (in df2: 52878619257 vs df4: 52872119257)
df5[165, 3] <- round((52878619257 + 52872119257) / 2)
df5 <- df5[-166, ]

write_csv(df5, "transformed/Private_investment_ai.csv")
