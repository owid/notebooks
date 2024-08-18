
library(tidyverse)
library(readxl) # For handling xls source data files


country_names<- read.csv("Original data/Kohl country names_country_standardized.csv")

# load raw data
fp<- "Original data/Kohl Homeownership rates/Homeownership rates 1.1.xlsx"
HO_rates<- as.data.frame(read_excel(fp, sheet = "data"))

# standardize country names 
HO_rates<- left_join(HO_rates, country_names) 

HO_rates<- HO_rates %>%
  select(-c(Country, iso)) %>%
  rename(country = Our.World.In.Data.Name)

# Gather to long format
HO_rates<- HO_rates %>%
  gather(year, HO_rate, -country) %>%
  mutate(year = as.numeric(year)) %>%
  drop_na()

# Save
save(HO_rates, file = "Manipulated data/HO_rates.Rda")

# export as csv
write.csv(HO_rates, "Manipulated data/HO_rates.csv",
          row.names = FALSE)


