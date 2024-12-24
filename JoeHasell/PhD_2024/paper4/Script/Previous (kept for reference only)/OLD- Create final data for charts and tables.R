

library(tidyverse)

source("Script/Functions/Averaging function.R") 
source("Script/Functions/proportional_link function.R") 


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

# THREE APPROACHES TO HOUSING SHARE DATA ------


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



# gather to long format 
housing_share_three_approaches<- housing_share_three_approaches %>%
  gather(series_name, value, -c(country, year))

# Filter for period, country and series -----

# only data 1970-2018
housing_share_three_approaches<- housing_share_three_approaches %>%
  filter(year>=1970 & year<= 2018)

# filter for a specific set of countries
housing_share_three_approaches<- housing_share_three_approaches %>%
  filter(country %in% countries_20)

# Drop the series based on GOS in Household sector, as explained in the paper
housing_share_three_approaches<- housing_share_three_approaches %>%
  filter(country == "Japan" |
           series_name != "OECD_hh_GOS_share") 

#  Create single synthetic series by 'averaging' (see paper for details) -----
print("Creating average for:")  

for(co in unique(housing_share_three_approaches$country)){

print(co)
  
  single_country<- housing_share_three_approaches %>%
  filter(country == co)

  new_country_averages<- get_normalised_trend(single_country,
                              "series_name",
                              "value",
                              "year",
                              "none")
  
  new_country_averages<- new_country_averages %>%
    mutate(country = co)
  
  if(co == housing_share_three_approaches$country[1]){

    country_averages<- new_country_averages
    
  } else {
    
    country_averages<- rbind(country_averages, new_country_averages)
    
  }
}

synthetic_housing_shares<- country_averages

synthetic_housing_shares<- synthetic_housing_shares %>%
  rename(value = trend_in_value)

save(synthetic_housing_shares,
     file="Manipulated data/synthetic_housing_shares.Rda")


# Average across countries (of the synthetic series) ----

# load the synthetic series data (calculated above)
load("Manipulated data/synthetic_housing_shares.Rda")

# load GDP at PPPs data for weights
load("Manipulated data/GDP_PPP.Rda")

# Add in GDP at PPPs
synthetic_housing_shares<- merge(
  synthetic_housing_shares,
  GDP_PPP)

# calculate average across countries

average_housing_share<- get_normalised_trend(synthetic_housing_shares,
                                             "country",
                                             "value",
                                             "year",
                                             "GDP_at_2015_PPPs")

average_housing_share<- average_housing_share %>%
  rename(unweighted_average_housing_share = trend_in_value,
         weighted_average_housing_share = weighted_trend_in_value)

save(average_housing_share,
     file="Manipulated data/average_housing_share.Rda")


# LOG CHANGES IN RELATIVE PRICE VS SYNTHETIC HOUSING SHARE -----

load("Manipulated data/synthetic_housing_shares.Rda")
load("Manipulated data/relative_rent_price_CPI.Rda")

housing_shares_and_prices<- merge(synthetic_housing_shares,
                                      relative_rent_price_CPI) 

housing_shares_and_prices<- housing_shares_and_prices %>%
  mutate(log_relative_rent_price = log(relative_rent_price),
         log_housing_share = log(value)) %>%
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

# SYNTHETIC SERIES FOR OVERALL CAPITAL SHARES ----

# load the data and format to bring the three cap shares series together

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


# merge the three series

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




