# -*- coding: utf-8 -*-
library(tidyverse)

# Pull in PIP data

df_pip<- read.csv("https://joeh.fra1.digitaloceanspaces.com/PIP/main_data.csv")

nrow(df_pip)

# Select only one reporting_level and welfare_type per entity-year (so that entity-years become unique)

# +
#If there are multiple reporting_levels for an entity-year, keep only national
df_pip<- df_pip %>% 
  group_by(entity, reporting_year, welfare_type) %>% 
  mutate(flag = +(n() > 1)) %>% 
  ungroup() %>%
  filter(flag==0 | reporting_level == "national") %>%
    select(-flag)



# -

nrow(df_pip)

#If there are multiple welfare_types for an entity-year, keep only consumption
    #...In fact there are none
df_pip<- df_pip %>% 
  group_by(entity, reporting_year, reporting_level) %>% 
  mutate(flag = +(n() > 1)) %>% 
  ungroup() %>%
  filter(flag==0 | welfare_type == "consumption") %>%
    select(-flag)

nrow(df_pip)

# Pull in WID data

df_wid<- read.csv("https://joeh.fra1.digitaloceanspaces.com/wid/gini_and_topshares_standardized.csv")

head(df_wid)

# Merge the two data frames

df<- full_join(df_wid, df_pip,  by = c("entity" = "entity", "year" = "reporting_year"))

head(df)

summary(df)

df %>% filter(year %in% c(1990, 2019)) %>% select(entity, year, wid_gini, gini) %>% drop_na() %>% count(entity)

# Calculate change in Gini 1990 – 2019

# +
gini_change<- df %>% filter(year %in% c(1990, 2019)) %>% 
                select(entity, year, wid_gini, gini) %>%
                pivot_wider(id_Cols = entity, names_from = year, values_from = c(wid_gini, gini), names_sep = "_")

gini_change
# -

df %>% filter(entity=="")


