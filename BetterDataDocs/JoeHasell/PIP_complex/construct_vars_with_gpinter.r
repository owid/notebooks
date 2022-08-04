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
id_vars<- c('country_name', 'reporting_year', 'reporting_level', 'welfare_type')




# ### Read in data

is_filled<- 'true'
df_filled<- read.csv(paste0('data/intermediate/percentiles/filled_',is_filled ,'/percentiles_before_Gpinter.csv'))

is_filled<- 'false'
df_survey<- read.csv(paste0('data/intermediate/percentiles/filled_',is_filled ,'/percentiles_before_Gpinter.csv'))

# Read in averages and merge in

df_main_filled<- read.csv('data/API_output/example_response_filled.csv')

df_main_filled<- df_main_filled %>% select(all_of(c(id_vars, "mean")))

df_filled<- left_join(df_filled, df_main_filled)

df_main_survey<- read.csv('data/API_output/example_response_survey.csv')

df_main_survey<- df_main_survey %>% select(all_of(c(id_vars, "mean")))

df_survey<- left_join(df_survey, df_main_survey)

# ### Cleaning

# #### Drop Sierra Leone from filled data

# See `PIP_issues` for further discussion.

df_filled<- df_filled %>% filter(country_name!="Sierra Leone")


# #### Drop duplicate columns

# Because the API sometimes returns the same headcount share for different requested percentiles (see `PIP_issues` notebook), we get duplicate headcount/poverty line observations. Here we drop these...



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



# ### Skip list

# These are country (reporting_level-welfare_type)-year observations that break GPinter (even though there are no monotonicty issues. It's unclear why these are breaking GPinter.

# +

skip_list<- c(
    "1989*Sierra Leone*national*consumption*filled=false",
    "1995*Ecuador*urban*income*filled=false",
    "1989*El Salvador*national*income*filled=false"
    )


# -

# ## Use GPinter to produce aligned set of percentiles (given that the returned percentile is sometimes quite different to the requested percentile)

# +
gpinter_align_percentiles<- function(distribution){
# This includes some outputs that are helpful to Joe for other work, but are not relevant to OWID's immediate needs.
    # Later I drop the less relevant columns.
#choose the lower bracket thresholds, begin from 0 
p <- c(seq(0,99,1))/100

# This calculates the upper brakect thresholds (up to 1)
p_1<- c(tail(p, length(p)-1),1)

average_in_bracket<- bracket_average(distribution, p, p_1)

share_in_bracket<- bracket_share(distribution, p, p_1)

q<- fitted_quantile(distribution, p)

average_above<- top_average(distribution, p)

share_above<- top_share(distribution, p)

# size of bracket (share of population)
share_of_pop<- p_1 - p
    

percentiles <- data.frame(p, q, share_in_bracket, average_in_bracket, average_above, share_above, share_of_pop)
    

    
# Create 1 row dataframe of key vars

# Decile shares and averages 
deciles_sh_avg<- percentiles %>%
    mutate(decile = paste0("decile_", ceiling(p*10))) %>% # create a decile categorical var
    group_by(decile) %>% # income share and average by decile
    summarize(sh = sum(share_in_bracket), 
              avg = mean(average_in_bracket)) %>%
    pivot_wider(names_from=decile, values_from = c(sh, avg)) # pivot to one row
    

# Decile thresholds
deciles_threshold<- percentiles %>% 
    mutate(p = p*10) %>%
    filter(p %in% c(1:9)) %>%
    select(p,q) %>%
    pivot_wider(names_from = p, values_from = q, names_prefix = "thresh_decile_")

# Join the decile shares, avgs and thresholds
key_vars<- cbind(deciles_sh_avg, deciles_threshold)

# Add the Gini to the one row dataframe
gini_scalar<-  gini(distribution) # Gini using Gpinter function (one value for all percentiles)

key_vars<- key_vars %>%
     mutate(gini = gini_scalar) 
    

# Gather two outputs in a list
outputs<- list()
outputs[["percentiles"]]<- percentiles
outputs[["key_vars"]]<- key_vars
        
return(outputs)

}


# +
# Test the function
selected_year_id_df<- df_filled %>%
 filter(reporting_year == 2000,
        country_name == "United Kingdom")

 p<- selected_year_id_df$headcount
                    q<- selected_year_id_df$poverty_line
                    average_inc<- as.numeric(unique(selected_year_id_df$mean))

original_distribution <- thresholds_fit(p, q, average = average_inc)

test<- gpinter_align_percentiles(original_distribution)

test[["key_vars"]]
# -




# +
for(is_filled in c('true', 'false')){
   
    
    if(is_filled == 'true'){
    
        df<- df_filled
    
    } else if(is_filled == 'false'){
    
        df<- df_survey

    }

    # Combine country_name, reporting_level and welfare_type to get unique rows within a year
    df<- df %>%
        mutate(id = paste(country_name, reporting_level, welfare_type, sep="*"))
    
    # Same but with year – this is needed to check against the skip list, defined above
    df<- df %>%
        mutate(year_id = paste(reporting_year, country_name, reporting_level, welfare_type, sep="*"))

    


    #Make empty dataframes to append the Gpinter results for each country
    # ... for the percentiles
    gpinter_percentiles_all<- data.frame(id = character(),
                         reporting_year = numeric(),
                         p = numeric(),
                         q = numeric(),
                         average_in_bracket = numeric(),
                         average_above = numeric(), 
                         share_above = numeric(), 
                         share_of_pop = numeric())
    
    # ... and for the key vars
    gpinter_key_vars_all<- data.frame(
                                id = character(),
                                reporting_year = numeric(),
                                sh_decile_1 = numeric(),
                                sh_decile_2 = numeric(),
                                sh_decile_3 = numeric(),
                                sh_decile_4 = numeric(),
                                sh_decile_5 = numeric(),
                                sh_decile_6 = numeric(),
                                sh_decile_7 = numeric(),
                                sh_decile_8 = numeric(),
                                sh_decile_9 = numeric(),
                                sh_decile_10 = numeric(),
                                avg_decile_1 = numeric(),
                                avg_decile_2 = numeric(),
                                avg_decile_3 = numeric(),
                                avg_decile_4 = numeric(),
                                avg_decile_5 = numeric(),
                                avg_decile_6 = numeric(),
                                avg_decile_7 = numeric(),
                                avg_decile_8 = numeric(),
                                avg_decile_9 = numeric(),
                                avg_decile_10 = numeric(),
                                thresh_decile_1 = numeric(),
                                thresh_decile_2 = numeric(),
                                thresh_decile_3 = numeric(),
                                thresh_decile_4 = numeric(),
                                thresh_decile_5 = numeric(),
                                thresh_decile_6 = numeric(),
                                thresh_decile_7 = numeric(),
                                thresh_decile_8 = numeric(),
                                thresh_decile_9 = numeric(),
                                gini = numeric()
                                )
    
    
    #Select reporting_year
    year_list = sort(unique(df$reporting_year))
    
    # For testing – since it takes a while to run on all reporting_years
    #year_list = c(1981)    
    
    for(yr in year_list){
        print(paste0("Aligning percentiles for reporting_year: ", yr))

        selected_year_df<- df %>%
          filter(reporting_year == yr)

            id_list<- unique(selected_year_df$id)



        # loop on each id
            for(ent in id_list){
                
                                    
                selected_year_id_df<- selected_year_df %>%
                      filter(id == ent)

                year_and_id<- as.character(unique(selected_year_id_df$year_id))
                year_and_id<- paste0(year_and_id, "*filled=", is_filled)

                print(paste0("Preparing: ",year_and_id))

                if(!year_and_id %in% skip_list){
                    
    
                    p<- selected_year_id_df$headcount
                    q<- selected_year_id_df$poverty_line
                    average_inc<- as.numeric(unique(selected_year_id_df$mean))

                    # Create a GPinter distribution object by passing the p and q values and average from PIP
                    original_distribution <- thresholds_fit(p, q, average = average_inc)
    
                    # Grab the outputs (two dataframes) from my function built on Gpinter
                    gpinter_func_outputs<- gpinter_align_percentiles(original_distribution)

                    # store as dataframes, adding the year and observation id
                    gpinter_percentiles<- gpinter_func_outputs[["percentiles"]] %>%
                        mutate(id = ent,
                        reporting_year = yr)

                    gpinter_key_vars<- gpinter_func_outputs[["key_vars"]] %>%
                        mutate(id = ent,
                        reporting_year = yr)
    
    
                    # Add to running lists
                    gpinter_percentiles_all<- rbind(gpinter_percentiles_all,
                                gpinter_percentiles)

                    gpinter_key_vars_all<- rbind(gpinter_key_vars_all,
                                gpinter_key_vars)
                    
                    }
                    
              }
      }
    

    

    # Split country_name and reporting level
    gpinter_percentiles_all<- gpinter_percentiles_all %>%
        separate(id, c("country_name", "reporting_level", "welfare_type"), sep = '\\*')
    
    gpinter_key_vars_all<- gpinter_key_vars_all %>%
        separate(id, c("country_name", "reporting_level", "welfare_type"), sep = '\\*')

    # write as csv
    write.csv(gpinter_percentiles_all, paste0('data/intermediate/percentiles/filled_', is_filled, '/percentiles_after_Gpinter.csv'), row.names = FALSE)
    write.csv(gpinter_key_vars_all, paste0('data/intermediate/key_vars/filled_', is_filled, '/key_vars_after_Gpinter.csv'), row.names = FALSE)
}


# -


