library(tidyverse)

series_link<- function(input_data, time_varname, 
                             earlier_series_varname, later_series_varname,
                         link_type){
  
  
  if(link_type %in% c("additional", "add",
                     "Additional", "Add")){
    link<- "additional"
  }
  
  if(link_type %in% c("proportional", "Proportional")){
    link<- "proportional"
  } 
  
  # Rename variables to make evaluation easier
  input_data<- input_data %>%
    rename(time_var = as.symbol(time_varname),
           earlier_series = as.symbol(earlier_series_varname),
           later_series = as.symbol(later_series_varname))  
  
  # select only the two series and the time variable
  input_data<- input_data %>%
    select(time_var, earlier_series, later_series)
  
  # Find overlap year for ratio
  
  earliest_overlap<- input_data %>%
    drop_na() %>%
    filter(time_var == min(time_var))
  
  # if there is no overlap year...
  if (nrow(earliest_overlap)==0){
    
    # ... print a warning
    print(paste0("No overlapping observations for ", earlier_series_varname, 
                 " and ", later_series_varname)) 
    
    # return a blank data frame in the same format
    final_series<- data.frame("time_var" = as.numeric(NA),
                              "linked_series" = as.numeric(NA))
  } else {

    if(link == "proportional"){    
    # calculate multiplier (ratio of later to earlier series for the overlap year)
    earliest_overlap<- earliest_overlap %>%
      mutate(multiplier = later_series/earlier_series)
    
    multiplier<- as.numeric(earliest_overlap$multiplier)
    } else if(link == "additional"){
    
    # calculate arithmetic difference
    earliest_overlap<- earliest_overlap %>%
      mutate(arith_diff = later_series-earlier_series)
    
    arith_diff<- as.numeric(earliest_overlap$arith_diff)    
    
    }
    
    # construct final series as the later series from the overlap year onwards,
    # and the earlier series prior to the overlap year times by the multiplier
    overlap_year<- as.numeric(earliest_overlap$time_var)
    
    final_series_part_1<- input_data %>%
      filter(time_var>= overlap_year) %>%
      mutate(linked_series = later_series) %>%
      select(time_var, linked_series)
    
    
    final_series_part_2<- input_data %>%
      filter(time_var< overlap_year) 
    
    if(link == "proportional"){ 
      final_series_part_2<- final_series_part_2 %>%
      mutate(linked_series = earlier_series * multiplier) 
      
    } else if(link == "additional"){
      
      final_series_part_2<- final_series_part_2 %>%
        mutate(linked_series = earlier_series + arith_diff) 
    }
      
      
    final_series_part_2<- final_series_part_2 %>%
      select(time_var, linked_series)
    
    final_series<- rbind(final_series_part_1, final_series_part_2)
    
  }
  
  # Return the final linked series, with the time varname as oer input data
  
  final_series<- final_series %>%
    arrange(time_var) %>% # sort by time period
    rename(!!as.symbol(time_varname) := time_var)
  
  return(final_series)
}

# # Testing of function
# test_data<- data.frame("year" = c(1990, 1991, 1992, 1993),
#                        "S1" = c(5, 5.1, 5.3, NA),
#                        "S2" = c(NA, 5.5, 5.6, 5.7))
# 
# test_data2<- data.frame("year" = c(1990, 1991, 1992, 1993),
#                         "S1" = c(5, 5.1, NA, NA),
#                         "S2" = c(NA, NA, 5.6, 5.7))
# 
# check2<- series_link(test_data, "year", "S1", "S2", "proportional")
