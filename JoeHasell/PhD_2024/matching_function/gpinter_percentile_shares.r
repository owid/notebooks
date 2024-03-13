library(tidyverse)
library(gpinter)

# load OWID main PIP pov file, to obtain mean 
df_main<- read.csv("poverty_inc_or_cons.csv")

df_main<- df_main %>%
  select(Entity, Year, reporting_level, welfare_type, mean)

# add a country-year-reporting-level-welfare col
df_main$distr_id <- paste(
    df_main$Entity,
    df_main$Year,
    df_main$reporting_level,
    df_main$welfare_type,
    sep = ' - ')

# print(head(df_main))

# Load scraped percentile data
df_percentiles<- read.csv("percentiles.csv")

# Filter out regional aggregates – which do not have reporting_level
df_percentiles<- df_percentiles %>%
  filter(reporting_level != '')

# drop duplicated rows (i.e. where the same pair of percentile and headcou values are matched to multiple target_percentile)
df_percentiles<- df_percentiles %>%
  group_by(Entity, Year, reporting_level, welfare_type, percentile_value, headcount,) %>%
  summarize(target_percentile = first(target_percentile), .groups = 'drop')

# add a country-year-reporting-level-welfare col
df_percentiles$distr_id <- paste(
    df_percentiles$Entity,
    df_percentiles$Year,
    df_percentiles$reporting_level,
    df_percentiles$welfare_type,
    sep = ' - ')



distr_id_list<- unique(df_percentiles$distr_id)



#### Test Gpinter flow on one country year
# id<- 'Zambia - 1993 - national - consumption'

# selected_perc_df<- df_percentiles %>%
#   filter(distr_id == id)

# selected_main_df<- df_main %>%
#   filter(distr_id == id)

# p<- selected_perc_df$headcount
# q<- selected_perc_df$percentile_value
# avg<- selected_main_df$mean
# print(p)

# gpinter_obj <- thresholds_fit(p, q, average=avg)

#     p <- c(seq(0,99,1))/100

#     q<- fitted_quantile(gpinter_obj, p)

#     shares<- top_share(gpinter_obj, p)

#     output <- data.frame(p, q, shares)

# print(output)

######


#### Make a function to run over all country years
align_distr<- function(distr, id){

    #choose the lower bracket thresholds, begin from 0
    p <- c(seq(0,99,1))/100

    q<- fitted_quantile(distr, p)

    shares<- top_share(distr, p)

    output <- data.frame(p, q, shares)
    
    output$distr_id<- id

    return(output)
}



# list to store aligned distributions
aligned_distr_list<- list()

# For each country year (+ reporting level + welfare)
for (id in distr_id_list){
    print(paste0('Processing: ',id))

    result <- try({
    
        #  Grab the percentiles/quantiles
        selected_df<- df_percentiles %>%
        filter(distr_id == id)

        p<- selected_df$headcount
        q<- selected_df$percentile_value

        #Grab the mean income
        selected_main_df<- df_main %>%
          filter(distr_id == id)

        avg<- selected_main_df$mean

        # Create Gpinter distribution object using the percentiles and avg
        gpinter_obj <- thresholds_fit(p, q, average = avg)

        # Output alined percentiles and income shares
        aligned_distr_list[[id]]<- align_distr(gpinter_obj, id)
    }, silent = TRUE)

    if (inherits(result, "try-error")) {
        print(paste("Error in iteration", id))
    next
  }
}

aligned_distr_combined_df <- bind_rows(aligned_distr_list)

aligned_distr_combined_df<- aligned_distr_combined_df %>%
    separate(distr_id, into = c('country', 'year', 'reporting_level', 'welfare_type'),
    sep = ' - ')

write.csv(aligned_distr_combined_df, "gpinter_aligned_percentiles_and_shares.csv", row.names = FALSE)

