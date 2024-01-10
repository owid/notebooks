library(tidyverse)
library(gpinter)

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






align_distr<- function(distr, id){

    #choose the lower bracket thresholds, begin from 0
    p <- c(seq(0,99,1))/100

    q<- fitted_quantile(distr, p)

    shares<- top_share(distr, p)

    output <- data.frame(p, q, shares)
    
    output$distr_id<- id

    return(output)
}


# id<- 'Zambia 1993 national consumption'

# selected_df<- df_percentiles %>%
#   filter(distr_id == id)

# p<- selected_df$headcount
# q<- selected_df$percentile_value

# print(q)


# # Original distribution
# gpinter_obj <- thresholds_fit(p, q)

# aligned_distr<- align_distr(gpinter_obj)



# list to store aligned distributions
aligned_distr_list<- list()

for (id in distr_id_list){
    print(paste0('Processing: ',id))

    result <- try({
    

        selected_df<- df_percentiles %>%
        filter(distr_id == id)

        p<- selected_df$headcount
        q<- selected_df$percentile_value

        # Create Gpinter distribution object using the percentile values in percentiles.csv
        gpinter_obj <- thresholds_fit(p, q)

        # Output alined percentiles
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

