library(tidyverse)


get_normalised_trend<- function(reg_data, entity_varname, value_varname, 
                                time_varname, weight_varname){
  
  # Set boolean according to whether a null weight var has been specified
  if(weight_varname %in% c("NA", "na", "N/A", "n/a", 
                            "N", "n", "None", "none",
                           "no", "No")){
    use_weights<- FALSE
  } else {
    use_weights<- TRUE
  }
  
# Rename variables to make evaluation easier
  reg_data<- reg_data %>%
    rename(value_var = !!as.symbol(value_varname),
           time_var = as.symbol(time_varname),
           entity_var = as.symbol(entity_varname))
  
  if(use_weights){
  reg_data<- reg_data %>%
    rename(weight_var = as.symbol(weight_varname))
  }
  
  # filter for periods where in which value is not missing
  reg_data<- reg_data %>%
    filter(!is.na(value_var))
  
  # grab first and last year
  first_year<- reg_data %>%
    select(time_var) %>%
    min() 
  
  last_year<- reg_data %>%
    select(time_var) %>%
    max() 
  

  # Calculate normalised trend as initial average + year fixed effects
  
  # Run regression
   
  year_fe_reg<- lm(value_var ~ as.factor(time_var) + as.factor(entity_var), 
                   data = reg_data)
  
  # extract year fixed effects
  year_fe<- summary(year_fe_reg)$coefficients[
                            2:(last_year - first_year + 1), 1]
  
  # calculate initial average (unweighted and weighted)
  start_avg<- reg_data %>%
    filter(time_var == first_year) %>%
    summarise(avg = mean(value_var, na.rm = TRUE))
  
  initial_avg<- unique(start_avg$avg)
  
  # calculate normalised trend (from 2nd year onwards) as year f.e. plus
  # initial average
  
  normalised_trend<- data.frame("time_var" = (first_year+1):last_year,
                                "fe" = year_fe)
  
  normalised_trend<- normalised_trend %>%
    mutate(trend = fe + initial_avg) %>%
    select(-c(fe))
  
  # append initial year
  initial_year<- data.frame("time_var" = first_year,
                            "trend" = initial_avg)
  
  normalised_trend<- rbind(normalised_trend, initial_year)
  
  
  # Same for weighted regression, if using
  if(use_weights){
    weighted_year_fe_reg<- lm(value_var ~ as.factor(time_var) + as.factor(entity_var), 
                              data = reg_data,
                              weights = weight_var)
    weighted_year_fe<- summary(weighted_year_fe_reg)$coefficients[
      2:(last_year - first_year + 1), 1]
    
    # calculate initial average (unweighted and weighted)
    start_avg_w<- reg_data %>%
      filter(time_var == first_year) %>%
      summarise(weighted_avg = weighted.mean(value_var,
                                             weight_var,
                                             na.rm = TRUE))
    
    initial_weighted_avg<- unique(start_avg_w$weighted_avg)
    
    # calculate normalised trend (from 2nd year onwards) as year f.e. plus
    # initial average
    
    normalised_trend_w<- data.frame("time_var" = (first_year+1):last_year,
                                  "weighted_fe" = weighted_year_fe)
    
    normalised_trend_w<- normalised_trend_w %>%
      mutate(weighted_trend = weighted_fe + initial_weighted_avg) %>%
      select(-c(weighted_fe))
    
    # append initial year
    initial_year_w<- data.frame("time_var" = first_year,
                              "weighted_trend" = initial_weighted_avg)
  
    normalised_trend_w<- rbind(normalised_trend_w, initial_year_w)

    # Merge weighted trend into unweighted trend
    
    normalised_trend<- merge(normalised_trend, normalised_trend_w, all = TRUE)

    }
 
  # sort by the time var
  normalised_trend<- normalised_trend %>%
    arrange(time_var)
  
  # Rename the variables according to the original names passed as input.
  
  trend_varname<- paste0("trend_in_", value_varname)
  weighted_trend_varname<- paste0("weighted_trend_in_", value_varname)
  
  normalised_trend<- normalised_trend %>%
    rename(!!as.symbol(time_varname) := time_var,
           !!as.symbol(trend_varname) := trend)
  
  if(use_weights){
  normalised_trend<- normalised_trend %>%
    rename(!!as.symbol(weighted_trend_varname) := weighted_trend)
}

  return(normalised_trend)
  
}  

# # Test it out:
# df<- data.frame("country" = c("CAN", "CAN", "USA", "USA", "USA", "AUS", "AUS"),
#                 "year" = c(1990, 1991, 1990, 1991, 1992, 1991,1992),
#                 "value" = c(1, 2 , 5,6,7, 3,3),
#                 "weight_var" = c(1,1,1,1,1,1,1))
# 
# 
# check<- get_normalised_trend(df, "country", "value", "year", "weight_var")