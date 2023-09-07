
library(tidyverse)

#Knitr purely for printing tables
library(knitr)

# Gpinter is the interpolation tool used by WID
library(gpinter)

#Pipr is a way of retriving stats from the PIP API
library(pipr)



# Use R's pipr package to grab the latest World Bank PIP data
# df_main_stats <- get_stats()

# fp<- "data/original/pip_main_data.csv"

# write.csv(df_main_stats, fp)


fp<- '/Users/joehasell/Documents/GitHub/personal_site/PhD_pages/Paper_1/data_appendix/data/original/PIP_OWID_percentiles_8_May.csv'
# fp<- 'PhD_pages/Paper_1/data_appendix/data/original/PIP_OWID_percentiles_8_May.csv'

df_owid_percentiles<- read.csv(fp)



# select_country<-  "China"
# select_year <- 1981
# select_reporting_level <- "national"
# df_thresholds <- df_owid_percentiles


prep_dist_from_thresholds <- function(select_country,
                      select_year,
                      select_reporting_level,
                      df_thresholds) {


  filtered_df<- df_thresholds %>%
    filter(
      Entity == select_country &
      Year == select_year &
      reporting_level == select_reporting_level
    )

  p<- filtered_df$headcount
  q<- filtered_df$percentile_value

  dist <- try(thresholds_fit(p , q))

  return(dist)
}


co<-  "VVV"
yr <- 1981
rpt_level <- "national"
df_thresholds <- df_owid_percentiles




# An empty dataframe to append the calculated top shares
gpinter_top1_shares<- data.frame(
  country = as.character(),
  year = as.integer(),
  reporting_level = as.character(),
  top1_share_gpinter = as.numeric()
)



countries_to_check<- unique(df_owid_percentiles$Entity)

for (co in countries_to_check){
  # co<- 'India'

  # Make a list of years to calculate merged distributions for -
    # all years for which the country is present in the data
  country_data<- df_owid_percentiles %>%
      filter(Entity == co)

  years_to_check<- unique(country_data$Year)

  for (yr in years_to_check){
  # yr <- 1977
    yr_data<- country_data %>%
      filter(Year == yr)

    rpt_levels_to_check<- unique(yr_data$reporting_level)

    for (rpt_level in rpt_levels_to_check){
      # rpt_level<- "national"


      prepped_dist<- try(prep_dist_from_thresholds(select_country = co,
                                                   select_year = yr,
                                                   select_reporting_level = rpt_level,
                                                   df_thresholds = df_owid_percentiles))
      
      
      if(class(prepped_dist)=="try-error"){
        
        print(paste0(co, " ", yr, " ", rpt_level, " - An error occurred"))
        
      } else{
        
        top1_share<- top_share(prepped_dist, 0.99)
        print(paste0(co, " ", yr, " ", rpt_level, " - Top 1% share = ", top1_share))
        
        
        gpinter_top1_shares<- gpinter_top1_shares %>%
          add_row(country = co, year=yr, reporting_level = rpt_level, top1_share_gpinter = top1_share)
        
        
      }
    

    


    }
  }
}


# Write the estiamted top 1% shares to csv
fp<- "/Users/joehasell/Documents/GitHub/personal_site/PhD_pages/Paper_1/data_appendix/data/manipulation/pip_estimated_top1_shares.csv"

write.csv(gpinter_top1_shares, fp)



# # Load PIP percentile data and adjust structure for gpinter
# 
# fp<- "PhD_pages/Paper_1/data_appendix/data/original/pip_percentiles.csv"
# 
# df_pip_percentiles<- read.csv(fp)
# 
# 
# df_alt_percentiles <- df_pip_percentiles %>%
#   group_by(country_code, year, reporting_level) %>%
#   mutate(
#     avg_welfare = lead(avg_welfare),
#     welfare_share = lead(welfare_share),
#     percentile = (percentile)/100
#   )
# 
# df_alt_percentiles <- df_alt_percentiles %>%
#   filter(
#     percentile != 1
#   )
# 
# 
# # Load PIP main data and prep decile shares to pass to Gpinter
# 
# 
# fp<- "PhD_pages/Paper_1/data_appendix/data/original/pip_main_data.csv"
# 
# df_main_data<- read.csv(fp)
# 
# decile_shares<- df_main_data %>%
#     select(
#       country_code, 
#       year, 
#       reporting_level,
#       decile1,
#       decile2,
#       decile3,
#       decile4,
#       decile5,
#       decile6,
#       decile7,
#       decile8,
#       decile9,
#       decile10)
# 
# decile_shares<- decile_shares %>%
#     pivot_longer(cols = starts_with("decile"), names_to = 'decile', names_prefix = 'decile', values_to = "shares")
# 
# decile_shares<- decile_shares %>%
#   mutate(decile = (as.numeric(decile)-1)/10)
# 
# decile_shares<- decile_shares %>%
#   filter(decile!=0)
# 
# #   Estimate top 1% shares from PIP decile shares
# 
# 
# run = TRUE
# 
# if (run){
# 
# prep_dist <- function(select_country, 
#                       select_year, 
#                       select_reporting_level,
#                       specify_average,
#                       df_shares) {
# 
#   
#   filtered_df<- df_shares %>%
#     filter(
#       country_code == select_country & 
#       year == select_year &
#       reporting_level == select_reporting_level
#     )
#   
#   p<- filtered_df$decile
#   shares<- filtered_df$shares
#   
#   dist <- shares_fit(p = p, bracketshare = shares, average = specify_average)
#   
#   return(dist)
# }
# 
# 
# handle_Gpinter_error <- function(expr){
#   tryCatch(expr,
#          error = function(e){
#            message("An error occurred:\n", e)
#            print(paste0("An error occurred:\n", e))
#          },
#          warning = function(w){
#            message("A warning occured:\n", w)
#            print(paste0("A warning occurred:\n", w))
#          },
#          finally = {
#            message("Estimated top 1% share successfully!")
#            print("Estimated top 1% share successfully!")
#          })
# }
# 
# # An empty dataframe to append the calculated top shares
# gpinter_top1_shares<- data.frame(
#   country_code = as.character(),
#   year = as.integer(),
#   reporting_level = as.character(),
#   top1_share_gpinter = as.numeric()
# )
# 
# countries_to_check<- unique(df_main_data$country_code)
# 
# for (co in countries_to_check){
#   # co<- 'IND'
# 
#   # Make a list of years to calculate merged distributions for - 
#     # all years for which the country is present in the data
#   country_data<- df_main_data %>%
#       filter(country_code == co) 
# 
#   years_to_check<- unique(country_data$year)
# 
#   for (yr in years_to_check){
#     
#     yr_data<- country_data %>%
#       filter(year == yr) 
# 
#     rpt_levels_to_check<- unique(yr_data$reporting_level)
# 
#     for (rpt_level in rpt_levels_to_check){
# 
#   # rpt_level<- 'rural'
# 
# 
#     # Get  mean from PIP main stats file
#     df_filtered<- df_main_data %>%
#       filter(
#         reporting_level == rpt_level,
#         country_code == co,
#         year == yr)
# 
# 
#     avg<- df_filtered$mean[1]  
# 
#     # I have to round up the mean to the nearest cent for the GPinter to work (there has to be a bit of headroom for the interpolation to work)
#     avg<- ceiling(avg *100)/100
# 
#     print(paste0(co, " ", yr, " ", rpt_level))
# 
# 
#     handle_Gpinter_error({
#     dist = prep_dist(
# 
#       select_country = co, 
#       select_year = yr, 
#       select_reporting_level = rpt_level,
#       specify_average = avg,
#       df_shares = decile_shares
# 
#     )
# 
#     top1_share<- top_share(dist, 0.99)
# 
#     gpinter_top1_shares<- gpinter_top1_shares %>%
#       add_row(country_code = co, year=yr, reporting_level = rpt_level, top1_share_gpinter = top1_share)
# 
#     })
# 
#     }
#   }
# }
# 
# kable(head(gpinter_top1_shares))
# 
# # Write the estiamted top 1% shares to csv
# fp<- "PhD_pages/Paper_1/data_appendix/data/manipulation/pip_estimated_top1_shares.csv"
# 
# write.csv(gpinter_top1_shares, fp)
# 
# }

