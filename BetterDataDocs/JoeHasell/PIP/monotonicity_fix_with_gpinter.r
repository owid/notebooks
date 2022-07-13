
library(gpinter)
library(tidyverse)


df<- read.csv('API_output/percentiles/all_percentiles.csv')

head(df)

# Another cell

df<- df %>%
     group_by(entity, year) %>% 
     arrange(headcount)

head(df)

df <- 
    df %>%
    group_by(entity, year) %>%
    mutate(lag.headcount = dplyr::lag(headcount, n = 1, default = NA))

head(df)


