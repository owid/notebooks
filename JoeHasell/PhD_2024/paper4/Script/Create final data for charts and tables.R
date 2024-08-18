

library(tidyverse)

source("Script/Functions/Averaging function.R") 
source("Script/Functions/series_link function.R") 


# Set of 20 countries

countries_20<- c("Australia",
                 "Austria",
                 "Belgium",
                 "Canada",
                 "Denmark",
                 "Finland",
                 "France",
                 "Germany",
                 "Greece",
                 "Ireland",
                 "Italy",
                 "Japan",
                 "Luxembourg",
                 "Netherlands",
                 "Norway",
                 "Portugal",
                 "Spain",
                 "Sweden",
                 "United Kingdom",
                 "United States")


# THREE SERIES FOR HOUSING AND NON-HOUSING SHARES (NEW) -----

# prep OECD industry data ----
load("Manipulated data/OECD industry data - aggregate factor shares.Rda") 

OECD_industry_shares<- aggregate_factor_shares %>%
  select(-net_share) %>%
  filter(transaction %in% c("housing_gross_CAP","non_housing_gross_CAP_2")) %>%
  spread(transaction, gross_share) %>%
  rename(housing_cap_share = housing_gross_CAP,
         non_housing_cap_share = non_housing_gross_CAP_2) %>%
  mutate(series = "OECD_industry_data") %>%
  drop_na() # only include rows where both housing and non-housing share is available

# prep KLEMS industry data ----
load("Manipulated data/KLEMS - aggregate factor shares.Rda") 

KLEMS_industry_shares<- aggregate_factor_shares %>%
  filter(transaction %in% c("housing_gross_CAP","non_housing_gross_CAP_2")) %>%
  spread(transaction, gross_share) %>%
  rename(housing_cap_share = housing_gross_CAP,
         non_housing_cap_share = non_housing_gross_CAP_2) %>%
  mutate(series = "KLEMS_industry_data") %>%
  drop_na() # only include rows where both housing and non-housing share is available

# prep OECD sector data -----
  # Here I use the overall sector capital shares (GOS + imputed capital
  # component of mixed income) and rent consumption data to split
  # housing and non-housing capital shares

# Load OECD consumption of housing share
load("Manipulated data/consump_housing_share.Rda") 


# Load OECD sector data capital shares

load("Manipulated data/sector_accounts_capital_share.Rda")

  # discard HH GOS figures in favour of rent consumption data 
    # (NB the same denominator has been used to calculate rent consumption share) 
sector_accounts_capital_share<- sector_accounts_capital_share %>%
  select(-hh_GOS_share_of_factor_cost_VA)

# Merge in consumption share

OECD_sector_shares_with_rent_consumption<- merge(sector_accounts_capital_share,
                                                 consump_housing_share) 

# calculate non-housing cap share as total cap share less rent consumption share
OECD_sector_shares_with_rent_consumption<- OECD_sector_shares_with_rent_consumption %>%
  mutate(housing_cap_share = rent_consumption_share_of_factor_cost_VA,
         non_housing_cap_share = cap_share_of_factor_cost_VA - housing_cap_share) %>%
  select(country, year, housing_cap_share, non_housing_cap_share) %>%
  mutate(series = "OECD_sector_and_rent_consumption_data")  %>%
  drop_na() # only include rows where both housing and non-housing share is available 
  

# Append the three different datasets ------

H_and_nonH_cap_shares_all<- rbind(OECD_industry_shares,
                                           KLEMS_industry_shares)


H_and_nonH_cap_shares_all<- rbind(H_and_nonH_cap_shares_all,
                                           OECD_sector_shares_with_rent_consumption)


# Gather to long format, and filter for country and year-----

H_and_nonH_cap_shares_all<- H_and_nonH_cap_shares_all %>%
  gather(share, value, -c(country, year, series)) %>%
  filter(country %in% countries_20,
         year >= 1970 & year <= 2017)


# Select series-years to be used in average under different specs ----


# switch_1995 spec: switch at earliest year of latest series
# Select the relevant series to form the average

# Drop sector data except for US and Spain
H_and_nonH_cap_shares_switch1995<- H_and_nonH_cap_shares_all %>%
  filter((series != "OECD_sector_and_rent_consumption_data" | 
            country %in% c("United States", "Spain")))

# Drop any KLEMS data falling after earliest OECD industry data 
  # (or sector data in the case of US and Spain)

non_KLEMS_earliest_years<- H_and_nonH_cap_shares_switch1995 %>%
  group_by(country) %>%
  filter(series != "KLEMS_industry_data") %>%
  summarise(max_KLEMS_year = min(year))

H_and_nonH_cap_shares_switch1995<- merge(
  H_and_nonH_cap_shares_switch1995,
  non_KLEMS_earliest_years, all = TRUE)

H_and_nonH_cap_shares_switch1995<- H_and_nonH_cap_shares_switch1995 %>%
  filter( series != "KLEMS_industry_data" | 
          year < max_KLEMS_year | 
          country == "Japan" )

# Switch2000 spec - if earliest year is 1995, switch at 2000 instead ----

# Drop sector data except for US and Spain
H_and_nonH_cap_shares_switch2000<- H_and_nonH_cap_shares_all %>%
  filter((series != "OECD_sector_and_rent_consumption_data" | 
            country %in% c("United States", "Spain")))


non_KLEMS_earliest_years<- H_and_nonH_cap_shares_all %>%
  group_by(country) %>%
  filter(series != "KLEMS_industry_data") %>%
  summarise(max_KLEMS_year = min(year))


cut_off_years_alt_spec<- non_KLEMS_earliest_years %>%
  mutate(max_KLEMS_year = replace(max_KLEMS_year,
                                  max_KLEMS_year==1995,
                                  2005))

H_and_nonH_cap_shares_switch2000<- merge(
  H_and_nonH_cap_shares_switch2000,
  cut_off_years_alt_spec, all = TRUE)

# drop KLEMS data after the break
H_and_nonH_cap_shares_switch2000<- H_and_nonH_cap_shares_switch2000 %>%
  filter( series != "KLEMS_industry_data" |
            year < max_KLEMS_year |
            country == "Japan" )

# Drop OECD industry data before the break
H_and_nonH_cap_shares_switch2000<- H_and_nonH_cap_shares_switch2000 %>%
  filter( series != "OECD_industry_data" |
            year >= max_KLEMS_year |
            country %in% c("Norway", "Netherlands"))

# Drop OECD sector data before the break in the case of Spain
H_and_nonH_cap_shares_switch2000<- H_and_nonH_cap_shares_switch2000 %>%
  filter(country != "Spain" |
           series != "OECD_sector_and_rent_consumption_data" |
           year >= max_KLEMS_year)

# KLEMSplus (plus OECD industry for Norway and Denmark) -----

H_and_nonH_cap_shares_KLEMSplus<- H_and_nonH_cap_shares_all %>%
  filter(series == "KLEMS_industry_data" |
           (country %in% c("Norway", "Denmark") & 
            series == "OECD_industry_data")) %>%
  filter(!(country == "Denmark" & series == "KLEMS_industry_data")) %>%
  filter(year<=2007)


# OECDindustPlus from 1995 (OECD industry plus OECD sector for US and Spain, from 1995 onwards) -----

H_and_nonH_cap_shares_OECDindustPlus<- H_and_nonH_cap_shares_all %>%
  filter(series == "OECD_industry_data" |
            (country %in% c("United States", "Spain") & 
            series == "OECD_sector_and_rent_consumption_data")) %>%
  filter(year>=1995)

# As per OECDindustPlus, but adding in post-1995 KLEMS for Canada, Japan 
# and Belgium

H_and_nonH_cap_shares_OECDindustPlus2<- H_and_nonH_cap_shares_all %>%
  filter(series == "OECD_industry_data" |
           (country %in% c("United States", "Spain") & 
              series == "OECD_sector_and_rent_consumption_data") |
           (country %in% c("Canada", "Japan") &
              series == "KLEMS_industry_data") |
           (country == "Belgium" &
              series == "KLEMS_industry_data" &
              year<1999) ) %>%
  filter(year>=1995)

# no Ireland or Portgual (but otherwise as KLEMS/OECD industry separate data)
H_and_nonH_cap_shares_KLEMSplus_no_IRL_PRT<- H_and_nonH_cap_shares_KLEMSplus %>%
  filter(!country %in% c("Ireland", "Portugal"))

H_and_nonH_cap_shares_OECDindustPlus_no_IRL_PRT<- H_and_nonH_cap_shares_OECDindustPlus %>%
  filter(!country %in% c("Ireland", "Portugal"))

H_and_nonH_cap_shares_OECDindustPlus2_no_IRL_PRT<- H_and_nonH_cap_shares_OECDindustPlus2 %>%
  filter(!country %in% c("Ireland", "Portugal"))



# Save as list ----

H_and_nonH_cap_shares<- list()

H_and_nonH_cap_shares[["all"]]<- H_and_nonH_cap_shares_all
H_and_nonH_cap_shares[["switch1995"]]<- H_and_nonH_cap_shares_switch1995
H_and_nonH_cap_shares[["switch2000"]]<- H_and_nonH_cap_shares_switch2000
H_and_nonH_cap_shares[["KLEMSplus"]]<- H_and_nonH_cap_shares_KLEMSplus
H_and_nonH_cap_shares[["OECDindustPlus"]]<- H_and_nonH_cap_shares_OECDindustPlus
H_and_nonH_cap_shares[["OECDindustPlus2"]]<- H_and_nonH_cap_shares_OECDindustPlus2
H_and_nonH_cap_shares[["KLEMSplus_no_IRL_PRT"]]<- H_and_nonH_cap_shares_KLEMSplus_no_IRL_PRT
H_and_nonH_cap_shares[["OECDindustPlus_no_IRL_PRT"]]<- H_and_nonH_cap_shares_OECDindustPlus_no_IRL_PRT
H_and_nonH_cap_shares[["OECDindustPlus2_no_IRL_PRT"]]<- H_and_nonH_cap_shares_OECDindustPlus2_no_IRL_PRT


save(H_and_nonH_cap_shares,
     file="Manipulated data/H_and_nonH_cap_shares")

# CALCULATE AVERAGE HOUSING AND NONHOUSING CAP SHARE -----

# load different data selections
load("Manipulated data/H_and_nonH_cap_shares")

# load GDP at PPPs data for weights
load("Manipulated data/GDP_PPP.Rda")

# make a list to store the averages from the three selections
avg_H_and_nonH_cap_shares<- list()

for(spec in c("all", "switch1995", "switch2000", "KLEMSplus", "OECDindustPlus",
              "OECDindustPlus2", "KLEMSplus_no_IRL_PRT", 
              "OECDindustPlus_no_IRL_PRT", "OECDindustPlus2_no_IRL_PRT")){

# grab data for this spec 
df<- H_and_nonH_cap_shares[[spec]]

# Add in GDP at PPPs
df<- merge(df,GDP_PPP)

# Make each country-series it's own entity
df<- df %>%
  mutate(country_series = paste0(country, " - ", series))

# Calculate 'average' housing cap shares - normalised year fixed effects
avg_housing_cap_shares<- df %>%
  filter(share == "housing_cap_share")

avg_housing_cap_shares<- get_normalised_trend(avg_housing_cap_shares,
                                              "country_series",
                                              "value",
                                              "year",
                                              "GDP_at_2015_PPPs")

avg_housing_cap_shares<- avg_housing_cap_shares %>%
  mutate(share = "housing_cap_share")

# Calculate 'average' non-housing cap shares - normalised year fixed effects

avg_non_housing_cap_shares<- df %>%
  filter(share == "non_housing_cap_share")

avg_non_housing_cap_shares<- get_normalised_trend(avg_non_housing_cap_shares,
                                              "country_series",
                                              "value",
                                              "year",
                                              "GDP_at_2015_PPPs")

avg_non_housing_cap_shares<- avg_non_housing_cap_shares %>%
  mutate(share = "non_housing_cap_share")

# append housing and nonhousing average cap shares
avg_housing_and_non_housing_cap_shares<- rbind(avg_housing_cap_shares,
                                               avg_non_housing_cap_shares)

# gather weighted and unweighted averages in long format
avg_housing_and_non_housing_cap_shares<- avg_housing_and_non_housing_cap_shares %>%
  rename(weighted_average = weighted_trend_in_value,
         unweighted_average = trend_in_value) %>%
  gather(weights, value, -c(year, share))

# store output in list
avg_H_and_nonH_cap_shares[[spec]]<- avg_housing_and_non_housing_cap_shares

}


# Save -----

save(avg_H_and_nonH_cap_shares,
     file="Manipulated data/avg_H_and_nonH_cap_shares.Rda")

# Make a table of changes across three periods -----

early_series<- avg_H_and_nonH_cap_shares[["KLEMSplus_no_IRL_PRT"]] %>%
  filter(year %in% c(1970, 1995, 2007)) %>%
  mutate(str_year = paste0("yr", year)) %>%
  select(-year) %>%
  spread(str_year, value) %>%
  mutate(change_1970_1995 = yr1995-yr1970,
         change_1995_2007 = yr2007-yr1995)


late_series<- avg_H_and_nonH_cap_shares[["OECDindustPlus2_no_IRL_PRT"]] %>%
  filter(year %in% c(1995, 2007, 2017)) %>%
  mutate(str_year = paste0("yr", year)) %>%
  select(-year) %>%
  spread(str_year, value) %>%
  mutate(change_1995_2007 = yr2007-yr1995,
         change_2007_2017 = yr2017-yr2007)

# LOG CHANGES IN RELATIVE PRICE VS SYNTHETIC HOUSING SHARE -----

load("Manipulated data/linked_series_all_countries.Rda")
load("Manipulated data/relative_rent_price_CPI.Rda")

housing_shares_and_prices<- merge(linked_series_all_countries,
                                  relative_rent_price_CPI) 

housing_shares_and_prices<- housing_shares_and_prices %>%
  mutate(log_relative_rent_price = log(relative_rent_price),
         log_housing_share = log(linked_series)) %>%
  group_by(country) %>%
  mutate(diff_log_relative_rent_price = log_relative_rent_price - 
           lag(log_relative_rent_price),
         diff_log_housing_share = (log_housing_share - 
                                     lag(log_housing_share))) %>%
  drop_na() %>%
  mutate(diff_log_relative_rent_price = cumsum(diff_log_relative_rent_price),
         diff_log_housing_share = cumsum(diff_log_housing_share)) %>%
  
  select(country, year, diff_log_relative_rent_price, diff_log_housing_share) %>%
  drop_na()

# Save
save(housing_shares_and_prices,
     file="Manipulated data/housing_shares_and_prices.Rda")



# BELOW HERE 'M NOT SURE IF WE NEED ANYMORE ---------


# LINKED SINGLE HOUSING SHARE SERIES ------


# Combine KLEMS and OECD data

# Load OECD housing share data
load("Manipulated data/housing_share_three_approaches.Rda") 

# Load KLEMS aggregate share data (to get the housing cap share)
load("Manipulated data/KLEMS - aggregate factor shares.Rda") 


# Combine the housing cap share from the KLEMS data with the
# OECD derived shares

KLEMS_housing_share<- aggregate_factor_shares %>%
  filter(transaction == "housing_gross_CAP") %>%
  rename(KLEMS_RE_industry_CAP_share = gross_share) %>%
  select(country, year, KLEMS_RE_industry_CAP_share)

housing_share_three_approaches<- merge(
  housing_share_three_approaches,
  KLEMS_housing_share, all = TRUE)

# filter for start and end year
housing_share_three_approaches<- housing_share_three_approaches %>%
  filter(year>=1970 & year<=2017)

# Four 'exception' groups of countries:

just_OECD_industry<- c("Denmark",
                       "Norway")

just_KLEMS_industry<- c("Japan")

just_OECD_consumption<- c("United States")

OECD_consumption_KLEMS_industry<- c("Canada",
                                    "Spain")


for(co in countries_20){
  # co<- "Denmark"
  input_data<- housing_share_three_approaches %>%
    filter(country == co)
  
  # select a single series or run the linking function on the right 
    # pair of series, according to the country groupings above (see main paper
    # for explanation)
  
  if(co %in% just_OECD_industry){
    linked_series<- input_data %>%
      select(year, OECD_RE_industry_CAP_share) %>%
      rename(proportional_linked_series = OECD_RE_industry_CAP_share) %>%
      mutate(additional_linked_series = proportional_linked_series)
      
  } else if(co %in% just_KLEMS_industry){
    linked_series<- input_data %>%
      select(year, KLEMS_RE_industry_CAP_share) %>%
      rename(proportional_linked_series = KLEMS_RE_industry_CAP_share)  %>%
      mutate(additional_linked_series = proportional_linked_series)
    
  } else if(co %in% just_OECD_consumption){
    linked_series<- input_data %>%
      select(year, OECD_consumption_share) %>%
      rename(proportional_linked_series = OECD_consumption_share) %>%
      mutate(additional_linked_series = proportional_linked_series)
    
  } else if(co %in% OECD_consumption_KLEMS_industry){
    
    proportional_linked_series<- series_link(input_data, "year", 
                                  "KLEMS_RE_industry_CAP_share", #earlier series
                                  "OECD_consumption_share", # later series
                                "proportional") #link type
    
    proportional_linked_series<-  proportional_linked_series %>%
      rename(proportional_linked_series = linked_series)
    
    additional_linked_series<- series_link(input_data, "year", 
                                "KLEMS_RE_industry_CAP_share", #earlier series
                                "OECD_consumption_share", # later series
                                "additional") #link type
    
    additional_linked_series<-  additional_linked_series %>%
      rename(additional_linked_series = linked_series)
    
    linked_series<- merge(proportional_linked_series,
                          additional_linked_series,
                          all = TRUE)
    
  } else {
    
  proportional_linked_series<- series_link(input_data, "year", 
                                           "KLEMS_RE_industry_CAP_share", #earlier series
                                           "OECD_RE_industry_CAP_share", # later series
                                           "proportional") #link type
  
  proportional_linked_series<-  proportional_linked_series %>%
    rename(proportional_linked_series = linked_series)
  
  additional_linked_series<- series_link(input_data, "year", 
                                         "KLEMS_RE_industry_CAP_share", #earlier series
                                         "OECD_RE_industry_CAP_share", # later series
                                         "additional") #link type
  
  additional_linked_series<-  additional_linked_series %>%
    rename(additional_linked_series = linked_series)
  
  linked_series<- merge(proportional_linked_series,
                        additional_linked_series,
                        all = TRUE)
  
  }
  
  
  # add country var back in
  linked_series<-  linked_series %>%
    mutate(country = co)
  
  # If it's the first country store as new dataframe
  if(co == countries_20[1]){
    linked_series_all_countries<- linked_series
  } else { # else append to the existing data frame
    linked_series_all_countries<- rbind(linked_series_all_countries, 
                                                linked_series)
  }
  
}


save(linked_series_all_countries,
     file="Manipulated data/linked_series_all_countries.Rda")

# AVERAGE HOUSING SHARE (of the linked series) ----

# load the linked series data (calculated above)
load("Manipulated data/linked_series_all_countries.Rda")

# load GDP at PPPs data for weights
load("Manipulated data/GDP_PPP.Rda")

# Add in GDP at PPPs
linked_series_all_countries<- merge(
  linked_series_all_countries,
  GDP_PPP)

# calculate average across countries

average_housing_share_proportional_links<- get_normalised_trend(linked_series_all_countries,
                                             "country",
                                             "proportional_linked_series",
                                             "year",
                                             "GDP_at_2015_PPPs")


average_housing_share_additional_links<- get_normalised_trend(linked_series_all_countries,
                                                                "country",
                                                                "additional_linked_series",
                                                                "year",
                                                                "GDP_at_2015_PPPs")


average_housing_share<- merge(average_housing_share_proportional_links, 
                              average_housing_share_additional_links,
                              all = TRUE)

average_housing_share<- average_housing_share %>%
  gather(series, value, -year)

# Store weighted/unweighted and link type as separate vars
average_housing_share[grepl("weighted", average_housing_share$series, fixed = TRUE),
                       "weights"] <- "Weighted"

average_housing_share[!grepl("weighted", average_housing_share$series, fixed = TRUE),
                      "weights"] <- "Unweighted"

average_housing_share[grepl("additional", average_housing_share$series, fixed = TRUE),
                      "link_type"] <- "additional"

average_housing_share[grepl("proportional", average_housing_share$series, fixed = TRUE),
                      "link_type"] <- "proportional"


# Save
average_housing_share<- average_housing_share %>%
  select(-series)

save(average_housing_share,
     file="Manipulated data/average_housing_share.Rda")


# THREE SERIES FOR NON-HOUSING CAPITAL SHARES  ----

# load and prepare the three series -----

# OECD industry data
load("Manipulated data/OECD industry data - aggregate factor shares.Rda") 

OECD_industry_non_housing_cap_shares<- aggregate_factor_shares %>%
  filter(transaction %in% c("non_housing_gross_CAP_2")) %>%
  select(country, year, gross_share) %>%
  rename(OECD_industry_non_housing_cap_shares = gross_share)


# KLEMS industry data
load("Manipulated data/KLEMS - aggregate factor shares.Rda") 

KLEMS_industry_non_housing_cap_shares<- aggregate_factor_shares %>%
  filter(transaction %in% c("non_housing_gross_CAP_2")) %>%
  select(country, year, gross_share) %>%
  rename(KLEMS_industry_non_housing_cap_shares = gross_share)

# OECD institutional sector data
# this is calculated as total capital income less the linked housing
# share series calculated above
load("Manipulated data/sector_accounts_capital_share.Rda")
load("Manipulated data/linked_series_all_countries.Rda")

OECD_sector_non_housing_cap_shares<- merge(sector_accounts_capital_share,
                                           linked_series_all_countries)

OECD_sector_non_housing_cap_shares<- OECD_sector_non_housing_cap_shares %>%
  mutate(OECD_sector_non_housing_cap_shares_proportional_linked = cap_share_of_factor_cost_VA -
           proportional_linked_series,
         OECD_sector_non_housing_cap_shares_additional_linked = cap_share_of_factor_cost_VA -
           additional_linked_series) %>%
  select(country, year, OECD_sector_non_housing_cap_shares_proportional_linked,
         OECD_sector_non_housing_cap_shares_additional_linked)

# Merge the series together ----

non_housing_cap_shares<- merge(OECD_industry_non_housing_cap_shares,
                               KLEMS_industry_non_housing_cap_shares,
                               all = TRUE) 

non_housing_cap_shares<- merge(non_housing_cap_shares,
                               OECD_sector_non_housing_cap_shares,
                               all = TRUE) 

# gather to long format and filter for country and year
non_housing_cap_shares<- non_housing_cap_shares %>%
  gather(series, value, -c(country, year)) %>%
  filter(country %in% countries_20,
         year>=1970 & year<=2017) %>%
  drop_na()

# Save
save(non_housing_cap_shares,
     file="Manipulated data/non_housing_cap_shares.Rda")

# AVERAGE NON-HOUSING CAPITAL SHARE -----




# THREE SERIES FOR OVERALL CAPITAL SHARES  ----

# load the data and prepare the three cap shares series -----

load("Manipulated data/KLEMS - aggregate factor shares.Rda")

KLEMS_cap_shares<- aggregate_factor_shares %>%
  filter(transaction == "gross_CAP_2") %>%
  rename(KLEMS_industry_gross_cap_share = gross_share) %>%
  select(country, year, KLEMS_industry_gross_cap_share)

load("Manipulated data/OECD industry data - aggregate factor shares.Rda")

OECD_industry_cap_shares<- aggregate_factor_shares %>%
  filter(transaction == "gross_CAP_2") %>%
  rename(OECD_industry_gross_cap_share = gross_share) %>%
  select(country, year, OECD_industry_gross_cap_share)

load("Manipulated data/sector_accounts_capital_share.Rda")

sector_accounts_capital_share<- sector_accounts_capital_share %>%
  rename(OECD_sector_gross_cap_share = cap_share_of_factor_cost_VA)


# merge the three series -----

gross_cap_shares<- merge(KLEMS_cap_shares, OECD_industry_cap_shares, all=TRUE)
gross_cap_shares<- merge(gross_cap_shares, sector_accounts_capital_share, all=TRUE)

# convert to long format to make charts easier
gross_cap_shares<- gross_cap_shares %>%
  gather(series, value, -c(country, year)) %>%
  drop_na()

# filter for 20 countries in our series and for 1970 onwards
gross_cap_shares<- gross_cap_shares %>%
  filter(country %in% countries_20,
         year>= 1970)


# Save
save(gross_cap_shares,
     file="Manipulated data/gross_cap_shares.Rda")



# LINKED SERIES FOR OVERALL CAPITAL SHARE ------

load("Manipulated data/gross_cap_shares.Rda")

test<- spread(gross_cap_shares, series, value)

# Four 'exception' groups of countries:

just_OECD_industry<- c("Denmark",
                       "Norway")

just_KLEMS_industry<- c("Japan")

just_OECD_consumption<- c("United States")

OECD_consumption_KLEMS_industry<- c("Canada",
                                    "Spain")



# Note that for these countries, the series and link year are as per the housing
# share: Australia, Austria, Belgium, 

for(co in countries_20){
  # co<- "Denmark"
  input_data<- housing_share_three_approaches %>%
    filter(country == co)
  
  # select a single series or run the linking function on the right 
  # pair of series, according to the country groupings above (see main paper
  # for explanation)
  
  if(co %in% just_OECD_industry){
    linked_series<- input_data %>%
      select(year, OECD_RE_industry_CAP_share) %>%
      rename(linked_series = OECD_RE_industry_CAP_share)
    
  } else if(co %in% just_KLEMS_industry){
    linked_series<- input_data %>%
      select(year, KLEMS_RE_industry_CAP_share) %>%
      rename(linked_series = KLEMS_RE_industry_CAP_share)
    
  } else if(co %in% just_OECD_consumption){
    linked_series<- input_data %>%
      select(year, OECD_consumption_share) %>%
      rename(linked_series = OECD_consumption_share)
    
  } else if(co %in% OECD_consumption_KLEMS_industry){
    
    linked_series<- series_link(input_data, "year", 
                                "KLEMS_RE_industry_CAP_share", #earlier series
                                "OECD_consumption_share", # later series
                                "proportional") #link type
  } else {
    
    linked_series<- series_link(input_data, "year", 
                                "KLEMS_RE_industry_CAP_share", #earlier series
                                "OECD_RE_industry_CAP_share", # later series
                                "proportional") #link type
  }
  
  
  # add country var back in
  linked_series<-  linked_series %>%
    mutate(country = co)
  
  # If it's the first country store as new dataframe
  if(co == countries_20[1]){
    linked_series_all_countries<- linked_series
  } else { # else append to the existing data frame
    linked_series_all_countries<- rbind(linked_series_all_countries, 
                                        linked_series)
  }
  
}





# LOG CHANGES IN RELATIVE PRICE VS SYNTHETIC HOUSING SHARE -----

load("Manipulated data/linked_series_all_countries.Rda")
load("Manipulated data/relative_rent_price_CPI.Rda")

housing_shares_and_prices<- merge(linked_series_all_countries,
                                  relative_rent_price_CPI) 

housing_shares_and_prices<- housing_shares_and_prices %>%
  mutate(log_relative_rent_price = log(relative_rent_price),
         log_housing_share = log(linked_series)) %>%
  group_by(country) %>%
  mutate(diff_log_relative_rent_price = log_relative_rent_price - 
           lag(log_relative_rent_price),
         diff_log_housing_share = (log_housing_share - 
                                     lag(log_housing_share))) %>%
  drop_na() %>%
  mutate(diff_log_relative_rent_price = cumsum(diff_log_relative_rent_price),
         diff_log_housing_share = cumsum(diff_log_housing_share)) %>%
  
  select(country, year, diff_log_relative_rent_price, diff_log_housing_share) %>%
  drop_na()

# Save
save(housing_shares_and_prices,
     file="Manipulated data/housing_shares_and_prices.Rda")










