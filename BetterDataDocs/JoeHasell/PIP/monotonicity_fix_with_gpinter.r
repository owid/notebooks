# -*- coding: utf-8 -*-

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

# Check for empty rows

df %>%
filter(is.na(poverty_line))

# +
## GPinter to produce complete set of percentiles (given that the returned percentile is sometimes quite different to the requested percentile)

# +
gpinter_align_percentiles<- function(distribution){
# This includes some outputs that are helpful to Joe for other work, but are not relevant to OWID's immediate needs.
    # Later I drop the less relevant columns.
#choose the lower bracket thresholds, begin from 0 
p <- c(seq(0,99,1))/100

# This calculates the upper brakect thresholds (up to 1)
p_1<- c(tail(p, length(p)-1),1)

average_in_bracket<- bracket_average(distribution, p, p_1)

q<- fitted_quantile(distribution, p)

average_above<- top_average(distribution, p)

share_above<- top_share(distribution, p)

# size of bracket (share of population)
share_of_pop<- p_1 - p

output <- data.frame(p, q, average_in_bracket, average_above, share_above, share_of_pop)

return(output)

}
# -



# Combine entity name and reporting level to get unique rows

df<- df %>%
    mutate(entity_level = paste0(entity, "*", reporting_level))

# Make an empty dataframe to append the Gpinter results for each country

gpinter_results_all<- data.frame(entity = character(),
                         year = numeric(),
                         p = numeric(),
                         q = numeric(),
                         average_in_bracket = numeric(),
                         average_above = numeric(), 
                         share_above = numeric(), 
                         share_of_pop = numeric())

#Select year
year_list = unique(df$year)

# +
# For testing – since it takes a while to run on all years
#year_list = c(1981,2015)

# +

for(yr in year_list){
  print(paste0("Aligning percentiles for year: ", yr))

    selected_year_df<- df %>%
      filter(year == yr)

    entity_list<- unique(selected_year_df$entity_level)



    # loop on each country
    for(ent in entity_list){
      #print(paste0("Country is: ", ent))

        selected_year_country_df<- selected_year_df %>%
          filter(entity_level == ent)
    
        p<- selected_year_country_df$headcount
        q<- selected_year_country_df$poverty_line

        # Original distribution
        #original_distribution <- thresholds_fit(p, q, average = average_inc)
        original_distribution <- thresholds_fit(p, q)
    
        # Make a dataframe with the aligned percentiles for this country
        gpinter_results_entity<- gpinter_align_percentiles(original_distribution) %>%
              mutate(entity_level = ent,
              year = yr)
    
    
        # Add to running lists
        gpinter_results_all<- rbind(gpinter_results_all,
                                gpinter_results_entity)
    }
    
    
}

# Split entity and reporting level
gpinter_results_all<- gpinter_results_all %>%
    separate(entity_level, c("entity", "reporting_level"), sep = '\\*')
# +
# Inspect result
#gpinter_results_all
# -


write.csv(gpinter_results_all, "clean_data/percentile_data_for_joes_phd.csv")

gpinter_results_all_just_percentiles<- gpinter_results_all %>%
 select(entity, year, reporting_level, p, q) %>%
 filter(p>0)

write.csv(gpinter_results_all_just_percentiles, "clean_data/percentiles_filled.csv")
