
library(tidyverse)
library(gt)

load("Manipulated data/H_and_nonH_cap_shares")

# specify if you want to see all data, or the selected data for average under 
# baseline or alt speca ("all", "switch1995", "switch2000", "KLEMSplus", 
# "OECDindustPlus", "OECDindustPlus2", "KLEMSplus_no_IRL_PRT", 
# "OECDindustPlus_no_IRL_PRT", "OECDindustPlus2_no_IRL_PRT")
spec<- "all"

df<- H_and_nonH_cap_shares[[spec]]

# Prepare table 1 -----

# drop Ireland and Portugal
df <- df %>%
  filter(!country %in% c("Ireland", "Portugal"))

# Column 1
Column1_series<- df %>% 
  select(country) %>%
  unique() %>%
  mutate(series = "KLEMS_industry_data") %>%
  mutate(series = replace(series,
                          country %in% c("Norway"),
                          "OECD_industry_data"))
  
Column1_min_year<- merge(Column1_series, df) %>%
  group_by(country, share) %>%
  slice_min(year) %>%
  rename(early_year = year,
         early_value = value)

Column1_max_year<- merge(Column1_series, df) %>%
  filter(year<=2007) %>%
  group_by(country, share) %>%
  slice_max(year)  %>%
  rename(late_year = year,
         late_value = value)

Column1<- merge(Column1_min_year,Column1_max_year) %>%
  mutate(value_diff = late_value-early_value,
         year_diff = late_year-early_year) %>%
  mutate(decade_change = value_diff/year_diff * 10) %>%
  select(country, series, share, early_year, late_year,decade_change) %>%
  spread(share, decade_change) %>%
  mutate()

# Column 2
Column2_series<- df %>% 
  select(country) %>%
  unique() %>%
  mutate(series = "OECD_industry_data")

Column2_min_year<- merge(Column2_series, df) %>%
  filter(year>=1995) %>%
  group_by(country, share) %>%
  slice_min(year) %>%
  rename(early_year = year,
         early_value = value)

Column2_max_year<- merge(Column2_series, df) %>%
  group_by(country, share) %>%
  slice_max(year)  %>%
  rename(late_year = year,
         late_value = value)

Column2<- merge(Column2_min_year,Column2_max_year) %>%
  mutate(value_diff = late_value-early_value,
         year_diff = late_year-early_year) %>%
  mutate(decade_change = value_diff/year_diff * 10) %>%
  select(country, series, share, early_year, late_year,decade_change) %>%
  spread(share, decade_change) %>%
  mutate()

country_list<- select(Column1, country)

Column2<- left_join(country_list, Column2)


# Column 3
Column3_series<- df %>% 
  select(country) %>%
  unique() %>%
  mutate(series = "OECD_sector_and_rent_consumption_data")

Column3_min_year<- merge(Column3_series, df) %>%
  filter(year>=1995) %>%
  group_by(country, share) %>%
  slice_min(year) %>%
  rename(early_year = year,
         early_value = value)

Column3_max_year<- merge(Column3_series, df) %>%
  group_by(country, share) %>%
  slice_max(year)  %>%
  rename(late_year = year,
         late_value = value)

Column3<- merge(Column3_min_year,Column3_max_year) %>%
  mutate(value_diff = late_value-early_value,
         year_diff = late_year-early_year) %>%
  mutate(decade_change = value_diff/year_diff * 10) %>%
  select(country, series, share, early_year, late_year,decade_change) %>%
  spread(share, decade_change) %>%
  mutate()

country_list<- select(Column1, country)

Column3<- left_join(country_list, Column3)


# example of how gt table works ----


test<- df[1:8,]

gt_table<- gt(data = test) %>%
  tab_header(
    title = "Test title",
    subtitle = "Test subtitle") %>%
  tab_footnote(
    footnote = "Footnote 1.",
    locations = cells_body(columns = country, rows = 3)
  ) %>%
  tab_footnote(
    footnote = "Footnote 2.",
    locations = cells_body(columns = country, rows = 4)
  ) %>%
  tab_spanner(
    label = "EU-KLEMS* - 1970-2007",
    columns = c(share, value)
  ) %>%
  tab_spanner(
    label = "1995-2017 (OECD, by industry)",
    columns = c(year, series)
  )
  
gt_table

