rm(list = ls())
library(stringr)
library(googlesheets4)
library(dplyr)
library(readr)
library(tidyr)
# library(janitor) # adorn_totals("row")

sheet_url <- "https://docs.google.com/spreadsheets/d/1rfIoVslO0vJjtZBYL8qMmUZLgbaNXS76sQaJZkn9Nx4/edit#gid=0"

# New CS PhDs by specialty Fig 4.4.2

# wide format
# df <- df %>%
#   rename(Speciality = ...1) %>%
#   gather(Year, New_CS_PhDs, -Speciality) %>%
#   mutate(Entity = "United States", Year = as.numeric(Year)) %>%
#   relocate(Entity, Year) %>% 
#   pivot_wider(names_from = "Speciality", values_from = "New_CS_PhDs") %>% 
#   select_all(~gsub("\\s+|\\.", "_", .)) %>% 
#   select_all(~gsub("/", "_", .)) %>% 
#   #select_all(tolower) %>% 
#   rename_with(~paste0("New_CS_PhDs_", .), -c(Entity, Year))

df <- read_sheet(sheet_url, sheet = 2, range = "B4:M24") #share

df <- df %>% 
  rename(Entity = ...1) %>%
  gather(Year, share_new_cs_phds_by_specialty, -Entity) %>%
  relocate(Entity, Year)

df_number <- read_sheet(sheet_url, sheet = 2, range = "B33:M54") #number
df_number[21,1] <- 'Total'

df_number <- df_number %>% 
  rename(Entity = ...1) %>% 
  gather(Year, number_new_cs_phds_by_specialty, -Entity) %>%
  relocate(Entity, Year)

join <- full_join(df, df_number)

write_csv(join, "transformed/PhDs_speciality.csv")

# Female new AI and CS PhDs Fig 4.4.6
df2 <- read_sheet(sheet_url) #"A35:R35", "A67:R67"
df_cs <- df2[34, 2:18]
df_ai <- df2[66, 2:18]

df_cs <- df_cs %>%
  gather(Year, share_new_female_cs_phds) %>%
  mutate(Entity = "North America", Year = as.numeric(Year), share_new_female_cs_phds = share_new_female_cs_phds / 100) %>%
  relocate(Entity, Year)

df_ai <- df_ai %>%
  gather(Year, share_new_female_ai_phds) %>%
  mutate(Entity = "North America", Year = as.numeric(Year), share_new_female_ai_phds = share_new_female_ai_phds / 100) %>%
  relocate(Entity, Year)

df_female <- merge(df_cs, df_ai, by = c('Entity', 'Year'), all = T)

# New international AI PhDs Fig 4.4.9
df_inter <- df2[67, 2:18]

df_inter <- df_inter %>%
  gather(Year, share_new_international_ai_phds) %>%
  mutate(Entity = "North America", Year = as.numeric(Year), share_new_international_ai_phds = share_new_international_ai_phds / 100) %>%
  relocate(Entity, Year)

df_fem_int <- merge(df_female, df_inter, by = c('Entity', 'Year'), all = T)

write_csv(df_fem_int, "transformed/PhDs_female_international.csv")
