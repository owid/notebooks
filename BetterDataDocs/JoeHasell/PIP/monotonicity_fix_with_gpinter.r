
library(gpinter)
library(tidyverse)


df<- read.csv('API_output/percentiles/all_percentiles.csv')

head(df)

# Another cell

df<- df %>%
     group_by(entity, year, reporting_level, welfare_type) %>% 
     arrange(headcount)



df <- 
    df %>%
    group_by(entity, year, reporting_level, welfare_type) %>%
    mutate(lag.poverty_line = dplyr::lag(poverty_line, n = 1, default = NA))

head(df)

# Reorder to inspect the lag

df<- df %>%
     arrange(entity, year, reporting_level, welfare_type, headcount)

head(df)

# Browse rows where monotonicity is broken (Only Ghana and Guyana)

df %>%
filter(lag.poverty_line>=poverty_line)

#

# Drop non monotonic rows

df<- df %>%
     filter(lag.poverty_line<poverty_line)


