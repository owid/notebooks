# -*- coding: utf-8 -*-
library(tidyverse)


# ## Filled data

# Read in data after Gpinter
df_after <- read.csv('data/intermediate/key_vars/filled_true/key_vars_after_Gpinter.csv')

df_after <- df_after %>% 
    rename(gini_est = gini) %>% 
    rename(welf_tru = reporting_level) %>% 
    rename(reporting_level = welfare_type)%>% 
    rename(welfare_type = welf_tru)

nrow(df_after)

head(df_after)

# Read in data before Gpinter
df_before <- read.csv('data/API_output/example_response_filled.csv')

nrow(df_before)

# merge
merged <- left_join(df_before, df_after)

head(merged)


names(merged)

ggplot(data = merged, aes(x=decile5, y=sh_decile_5)) +
    geom_point()

ggplot(data = merged, aes(x=decile10, y=sh_decile_10)) +
    geom_point()

# Note that PIP does something very strage with median – they keep it fixed across the interpolation (whereas all the other variables are interpoloated)
ggplot(data = merged, aes(x=median, y=thresh_decile_5)) +
    geom_point()

ggplot(data = merged, aes(x=gini, y=gini_est)) +
    geom_point()

# ## Survey-year only data



# Read in data after Gpinter
df_after <- read.csv('data/intermediate/key_vars/filled_false/key_vars_after_Gpinter.csv')

df_after <- df_after %>% 
    rename(gini_est = gini) %>% 
    rename(welf_tru = reporting_level) %>% 
    rename(reporting_level = welfare_type)%>% 
    rename(welfare_type = welf_tru)

nrow(df_after)

head(df_after)

# Read in data before Gpinter
df_before <- read.csv('data/API_output/example_response_survey.csv')

nrow(df_before)

# merge
merged <- left_join(df_before, df_after)

head(merged)




ggplot(data = merged, aes(x=decile5, y=sh_decile_4)) +
    geom_point()

ggplot(data = merged, aes(x=decile10, y=sh_decile_9)) +
    geom_point()

# Note that PIP does something very strage with median – they keep it fixed across the interpolation (whereas all the other variables are interpoloated)
ggplot(data = merged, aes(x=median, y=thresh_decile_5)) +
    geom_point()

ggplot(data = merged, aes(x=gini, y=gini_est)) +
    geom_point()

# It seems to be China's national data that yields very different figures to those after Gpinter
merged %>%
filter(gini_est > gini + 0.1) 

# ## Check empty values

merged %>% nrow()

merged %>% drop_na() %>% nrow()


merged %>% filter(is.na(sh_decile_5))


summary(merged)


