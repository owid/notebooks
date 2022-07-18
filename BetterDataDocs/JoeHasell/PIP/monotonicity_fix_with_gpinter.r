# -*- coding: utf-8 -*-

library(gpinter)
library(tidyverse)


# +
# A function to drop duplicates. Because the API sometimes returns the same headcount share for different requested percentiles
# (see `PIP_issues` notebook), we get duplicate headcount/poverty line observations. Later we use this function to drop these... 

drop_dupes<- function(df, id_vars, duplicate_data_var){
    
    dedupe_vars<- c(id_vars, duplicate_data_var)

    df<- df %>%
        distinct(across(all_of(dedupe_vars)), .keep_all = TRUE)
    
return(df)
    
}

# -



# +

drop_non_mono<- function(df, id_vars, order_var, data_var, browse){

# Group, order and lag
lag_data_var<- paste0("lag_", data_var)

data_var <- sym(data_var)

  # df<- df %>%
  #    group_by_at(id_vars) %>% 
  #    arrange_at(order_var, .by_group = TRUE) %>%
  #    mutate({{lag_data_var}} := dplyr::lag(!!data_var, n = 1, default = NA)) %>%
  #    arrange_at(c(id_vars,order_var))

  df<- df %>%
     group_by_at(id_vars) %>% 
     arrange_at(order_var, .by_group = TRUE) %>%
     mutate({{lag_data_var}} := dplyr::lag(!!data_var, n = 1, default = NA)) %>%
     arrange_at(c(id_vars,order_var))

lag_data_var <- sym(lag_data_var)


  if(browse){
        df<- df %>% filter(!!lag_data_var>=!!data_var)
      } else{
        df<- df %>% filter(!!lag_data_var<!!data_var)  
      }

return(df)
    
}

# -





# ### Read in data

df_filled<- read.csv('API_output/percentiles/all_percentiles_filled.csv')

head(df_filled)

df_survey<- read.csv('API_output/percentiles/all_percentiles_survey.csv')

head(df_survey)

# ### Cleaning

# #### Drop Sierra Leone from filled data

# See `PIP_issues` for further discussion.

df_filled<- df_filled %>% filter(country_name!="Sierra Leone")


# #### Drop duplicate columns

# Because the API sometimes returns the same headcount share for different requested percentiles (see `PIP_issues` notebook), we get duplicate headcount/poverty line observations. Here we drop these...

id_vars<- c('country_name', 'reporting_year', 'reporting_level', 'welfare_type')

df_filled<- drop_dupes(df_filled,
                       id_vars = id_vars,
                        duplicate_data_var = 'headcount')

df_survey<- drop_dupes(df_survey,
                       id_vars = id_vars,
                        duplicate_data_var = 'headcount')

# #### Drop negative incomes

# In the filled data, we see that there are lots of observations with a negative poverty line.

df_filled %>% filter(poverty_line<0)

# All these observations relate to two countries: Sierra Leone and El Salvador

# +
neg_inc_list<- df_filled %>%
    group_by_at(id_vars) %>%
    summarize(min_poverty_line = min(poverty_line))

neg_inc_list %>% filter(min_poverty_line<0)
# -

# We merge this list back into the data and drop any (country-reporting_level-welfare_type-)years that include negative incomes

df_filled<- left_join(df_filled, neg_inc_list) %>%
    filter(min_poverty_line>0)

# Note that the survey-year only data does not contain negative incomes.

df_survey %>% filter(df_survey<0)



# #### Drop non-monotonically increasing data

# In a few cases, the API returns non-monotonically increasing data – i.e. an income level that is not strictly greater for a higher percentile.
#
# We browse these rows and then drop them.

# Browse non-monotonic rows in the filled data
drop_non_mono(df=df_filled,
              id_vars = c('country_name', 'reporting_year', 'reporting_level', 'welfare_type'),
              order_var = 'headcount',
              data_var = 'poverty_line',
              browse=TRUE)

# Drop non-monotonic rows in the filled data
df_filled<- drop_non_mono(df=df_filled,
              id_vars = c('country_name', 'reporting_year', 'reporting_level', 'welfare_type'),
              order_var = 'headcount',
              data_var = 'poverty_line',
              browse=FALSE)

# Browse non-monotonic rows in the survey-year only data
drop_non_mono(df=df_survey,
              id_vars = c('country_name', 'reporting_year', 'reporting_level', 'welfare_type'),
              order_var = 'headcount',
              data_var = 'poverty_line',
              browse=TRUE)

# Drop non-monotonic rows in the survey-year only data
df_survey<- drop_non_mono(df=df_survey,
              id_vars = c('country_name', 'reporting_year', 'reporting_level', 'welfare_type'),
              order_var = 'headcount',
              data_var = 'poverty_line',
              browse=FALSE)



#

# +
## Use GPinter to produce aligned set of percentiles (given that the returned percentile is sometimes quite different to the requested percentile)

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
# +
for(is_filled in c('true', 'false')){
    
    
    if(is_filled == 'true'){
    
        df<- df_filled
    
    } else if(is_filled == 'false'){
    
        df<- df_survey

    }

    # Combine country_name, reporting_level and welfare_type to get unique rows within a year
    df<- df %>%
        mutate(id = paste0(country_name, welfare_type, reporting_level, sep="*"))

    


    #Make an empty dataframe to append the Gpinter results for each country
    gpinter_results_all<- data.frame(id = character(),
                         reporting_year = numeric(),
                         p = numeric(),
                         q = numeric(),
                         average_in_bracket = numeric(),
                         average_above = numeric(), 
                         share_above = numeric(), 
                         share_of_pop = numeric())
    
    
    #Select reporting_year
    year_list = unique(df$reporting_year)
    
    # For testing – since it takes a while to run on all reporting_years
    #year_list = c(1981,2015)    
    
    for(yr in year_list){
        print(paste0("Aligning percentiles for reporting_year: ", yr))

        selected_year_df<- df %>%
          filter(reporting_year == yr)

            id_list<- unique(selected_year_df$id)



        # loop on each id (~=country)
            for(ent in id_list){
                #print(paste0("Country is: ", ent))

                selected_year_id_df<- selected_year_df %>%
                  filter(id == ent)
    
                p<- selected_year_id_df$headcount
                q<- selected_year_id_df$poverty_line

                # Original distribution
                #original_distribution <- thresholds_fit(p, q, average = average_inc)
                original_distribution <- thresholds_fit(p, q)
    
                # Make a dataframe with the aligned percentiles for this country
                gpinter_results_id<- gpinter_align_percentiles(original_distribution) %>%
                    mutate(id = ent,
                    reporting_year = yr)
    
    
                # Add to running lists
                gpinter_results_all<- rbind(gpinter_results_all,
                                gpinter_results_id)
              }
      }
    

    

    # Split country_name and reporting level
    gpinter_results_all<- gpinter_results_all %>%
        separate(id, c("country_name", "reporting_level", "welfare_type"), sep = '\\*')

    # write as csv – fill set of vars for Joe's PhD
    
    write.csv(gpinter_results_all, paste0('clean_data/percentiles/filled_', is_filled, '/percentile_data_for_joes_phd.csv'))
              
    # write as csv – smaller set of vars for OWID  
    gpinter_results_all_just_percentiles<- gpinter_results_all %>%
        select(country_name, reporting_year, reporting_level, welfare_type, p, q) %>%
        filter(p>0)
    
    write.csv(gpinter_results_all_just_percentiles, paste0('clean_data/percentiles/filled_', is_filled, "/percentiles_filled.csv"))
    
}
# -


# +
df_test<- df_survey

yr<- 1981

selected_year_df<- df %>%
          filter(reporting_year == yr)

            id_list<- unique(selected_year_df$id)



        # loop on each id (~=country)
            for(ent in id_list){
                #print(paste0("Country is: ", ent))

                selected_year_id_df<- selected_year_df %>%
                  filter(id == ent)
    
                p<- selected_year_id_df$headcount
                q<- selected_year_id_df$poverty_line

                # Original distribution
                #original_distribution <- thresholds_fit(p, q, average = average_inc)
                original_distribution <- thresholds_fit(p, q)
    
                # Make a dataframe with the aligned percentiles for this country
                gpinter_results_id<- gpinter_align_percentiles(original_distribution) %>%
                    mutate(id = ent,
                    reporting_year = yr)
    
    
                # Add to running lists
                gpinter_results_all<- rbind(gpinter_results_all,
                                gpinter_results_id)
              }



# -


