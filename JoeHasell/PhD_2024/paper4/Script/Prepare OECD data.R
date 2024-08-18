
library(tidyverse)




# GDP at PPPs output -----

# load country mapping
load("Manipulated data/OECD country mapping.Rda")

# load API data
load("Original data/OECD API outputs/GDP_PPP_raw.Rda") # GDP at PPPs (OECD data)

# Standardize country names 

GDP_PPP<- merge(GDP_PPP, country_names)

GDP_PPP <- GDP_PPP %>%
  rename(country = Our.World.In.Data.Name,
         GDP_at_2015_PPPs = obsValue) %>%
  mutate(year = as.numeric(obsTime)) %>%
  select(country, year,GDP_at_2015_PPPs) 


# Save
save(GDP_PPP, file="Manipulated data/GDP_PPP.Rda")



# TIDY INDUSTRY GENERATION OF INCOME DATA ----

# load country mapping
load("Manipulated data/OECD country mapping.Rda")

# load API data
load("Original data/OECD API outputs/industry_accounts.Rda")

# Standardize country names
industry_accounts_raw<- merge(industry_accounts, country_names)

industry_accounts_raw <- industry_accounts_raw %>%
  rename(country = Our.World.In.Data.Name) %>%
  mutate(year = as.numeric(obsTime))

# Filter for only current price data and the needed transactions
industry_accounts_raw<- industry_accounts_raw %>%
  filter(MEASURE == "C" & 
           TRANSACT %in% c("B1GA", "D1A","B2G_B3GA", "B2N_B3NA"))

# label transaction codes
industry_accounts_raw[industry_accounts_raw$TRANSACT %in% "B1GA", "transaction"]<- "value_added" 
industry_accounts_raw[industry_accounts_raw$TRANSACT %in% "D1A", "transaction"]<- "CoE" 
industry_accounts_raw[industry_accounts_raw$TRANSACT %in% "B2G_B3GA", "transaction"]<- "GOS" 
industry_accounts_raw[industry_accounts_raw$TRANSACT %in% "B2N_B3NA", "transaction"]<- "NOS"  

# Select needed vars
industry_accounts_raw<- industry_accounts_raw %>%
  select(country,transaction,ACTIVITY,year,obsValue)


# TIDY INDUSTRY LABOUR INPUTS DATA ----

# load country mapping
load("Manipulated data/OECD country mapping.Rda")

# load API data
load("Original data/OECD API outputs/employment_by_industry.Rda")

# standardize country names and rename vars
employment_by_industry_raw<- merge(employment_by_industry, country_names)

employment_by_industry_raw <- employment_by_industry_raw %>%
  rename(country = Our.World.In.Data.Name) %>%
  mutate(year = as.numeric(obsTime))

employment_by_industry_raw<- employment_by_industry_raw %>%
  select(country,TRANSACT,ACTIVITY,year,obsValue)

# Grab self-employed and employed hours as wide format
employment_by_industry_raw<- employment_by_industry_raw %>%
  filter(TRANSACT %in% c("ESEA", "EEMA"),  # codes for self-employed and employed
         !is.na(obsValue)) %>% # drop NAs
  spread(TRANSACT, obsValue) %>% #spread to wide format
  rename(self_employed_hrs = ESEA, 
         employed_hrs = EEMA)


# PREPARE FACTOR SHARES FOR INDUSTRY DATA ----

industry_accounts<- industry_accounts_raw
employment_by_industry <- employment_by_industry_raw
  

# Impute self employed labour income ------

# convert industry data to wide format
industry_accounts<- industry_accounts %>%
  spread(transaction, obsValue)

# merge-in hours data
industry_accounts<- merge(industry_accounts, employment_by_industry)

# Drop a handful of rows where employed hours = 0 but CoE > 0 
  # (i.e. an infinite wage)
industry_accounts<- industry_accounts %>%
  filter(!(CoE>0 & employed_hrs == 0))

# Impute labour income
  # TWO scenarios:
    # CoSE_1 = imputed self employed labour income assuming per-hour 
      # compensation is same as employees 
    # CoSE_2 = Minimum of either the above or GOS (i.e. labour income cannot
      # be higher than factor price value added)

industry_accounts<- industry_accounts %>%
  mutate(per_hour_CoE = CoE/employed_hrs,
         CoSE_1 = per_hour_CoE * self_employed_hrs,
         CoSE_2 = pmin(CoSE_1, GOS))

# Then subtract this from GOS/NOS to derive capital income.
industry_accounts<- industry_accounts %>%
  mutate(gross_CAP_1 = GOS - CoSE_1,
         gross_CAP_2= GOS - CoSE_2,
         net_CAP_1 = NOS - CoSE_1,
         net_CAP_2 = NOS - CoSE_2) 

# Aggregate over industries -----

# Drop if value added = 0
industry_accounts<- industry_accounts %>%
  filter(!value_added == 0)

# set of all the aggregate industries (data also includes sub-industries)
main_industry_codes<- c("VA0", "VB", "VC", "VD", "VE", "VF", "VG", "VH", "VI",
                        "VJ", "VK", "VL", "VM", "VN", "VO", "VP", "VQ", "VR",
                        "VS", "VT", "VU")

main_industry_accounts<- industry_accounts %>%
  filter(ACTIVITY %in% main_industry_codes)

# Aggregate over industries (excluding sub-industries)

agg_industry_accounts<- main_industry_accounts %>%
  group_by(country, year) %>%
  summarise(value_added = sum(value_added, na.rm=TRUE),
            gross_CAP_1 = sum(gross_CAP_1, na.rm=TRUE),
            gross_CAP_2 = sum(gross_CAP_2, na.rm=TRUE),
            net_CAP_1 = sum(net_CAP_1, na.rm=TRUE),
            net_CAP_2 = sum(net_CAP_2, na.rm=TRUE),
            CoE = sum(CoE, na.rm=TRUE),
            CoSE_1 = sum(CoSE_1, na.rm=TRUE),
            CoSE_2 = sum(CoSE_2, na.rm=TRUE),
            GOS = sum(GOS, na.rm=TRUE),
            NOS = sum(NOS, na.rm=TRUE)) %>%
  na_if(0) %>%
  gather(transaction, obsValue, -c(country, year))


reported_totals<- industry_accounts %>%
  filter(ACTIVITY == "VTOT") %>%
  select(country, year, CoE, GOS, NOS, value_added) %>%
  gather(transaction, reported_total, -c(country, year))


# Check totals. Keep observations where sum across industries equal
  # (or are very very close to) the reported all-industry total.

bad_totals<- left_join(agg_industry_accounts, reported_totals)

bad_totals<- bad_totals %>%
  mutate(total_check = obsValue/reported_total)

tolerance<- 0.005 # half a percent tolerance

bad_totals<- bad_totals %>%
  filter((total_check<(1-tolerance) | total_check>(1+tolerance))) %>%
  mutate(bad_total = 1) %>%
  select(country, year, transaction, bad_total)


# Merge back in to sums and drop any bad totals

agg_industry_accounts<- left_join(agg_industry_accounts, bad_totals)

agg_industry_accounts<- agg_industry_accounts %>%
  filter(is.na(bad_total)) %>%
  select(-bad_total)

# Spread back to wide format and keep only country-years with all vars
agg_industry_accounts<- agg_industry_accounts %>%
  spread(transaction, obsValue)


# Separate housing capital income ------

# Note that CoSE does not exceed GOS in the housing industry ever
  # so we can use either CoSE scenario in this case
br<- main_industry_accounts %>%
  filter(ACTIVITY == "VL" & CoSE_1!=CoSE_2)

# Filter for housing cap income and merge it in as an 
# aggregate activity
housing_cap<- industry_accounts %>%
  filter(ACTIVITY == "VL") %>% # code for Real Estate industry
  rename(housing_gross_CAP = gross_CAP_1,
         housing_net_CAP = net_CAP_1) %>%
  select(country, year, housing_gross_CAP, housing_net_CAP)

agg_industry_accounts<- left_join(agg_industry_accounts, housing_cap)

# Calculate non-housing cap income (at the aggregate level)
  # under the two scenarios
agg_industry_accounts<- agg_industry_accounts %>%
  mutate(non_housing_gross_CAP_1 = gross_CAP_1 - housing_gross_CAP,
         non_housing_gross_CAP_2 = gross_CAP_2 - housing_gross_CAP,
         non_housing_net_CAP_1 = net_CAP_1 - housing_net_CAP,
         non_housing_net_CAP_2 = net_CAP_2 - housing_net_CAP)


# Calc aggregate shares in factor-price income ----

# Calc factor-price value added (i.e. CoE + GOS)

agg_industry_accounts<- agg_industry_accounts %>%
  mutate(gross_cap_plus_lab = GOS + CoE,
         net_cap_plus_lab = NOS + CoE)

# gather to long format to make calculation of shares easier
# Calc gross and net shares separately
# gross
gross_shares<- agg_industry_accounts %>%
  select(country, year, CoE, GOS,
         CoSE_1, CoSE_2,
         non_housing_gross_CAP_1, non_housing_gross_CAP_2, 
         housing_gross_CAP, 
         gross_cap_plus_lab,
         gross_CAP_1,
         gross_CAP_2) %>%
  drop_na() # drops any rows that do not have all these vars

gross_shares<- gross_shares %>%
  gather(transaction, obsValue, -c(country, year,
                                   gross_cap_plus_lab)) %>%
  mutate(gross_share = obsValue/gross_cap_plus_lab) %>%
  select(country, year, transaction, gross_share)

# net
net_shares<- agg_industry_accounts %>%
  select(country, year, CoE, NOS,
         CoSE_1, CoSE_2,
         non_housing_net_CAP_1, non_housing_net_CAP_2,
         housing_net_CAP, 
         net_cap_plus_lab) %>%
  drop_na() # drops any rows that do not have all these vars

net_shares<- net_shares %>%
  gather(transaction, obsValue, -c(country, year,
                                   net_cap_plus_lab)) %>%
  mutate(net_share = obsValue/net_cap_plus_lab) %>%
  select(country, year, transaction, net_share)

# combine the gross and net share data
aggregate_factor_shares<- merge(gross_shares, net_shares, all = TRUE)


# Save aggregate shares -----

fp<- "Manipulated data/OECD industry data - aggregate factor shares.Rda"
save(aggregate_factor_shares, file=fp)




# Below here is a bit of a mess. The only thing remaining is:
  # - to work out shares for industry data
  #  - to check what is going on with Iceland and Sweden -INF share data?

# Calculate shares in industry-level data ------

# main_industry_accounts<- bind_rows(main_industry_accounts, agg_industry_accounts)
# 
# # Calc factor-price value added (i.e. CoE + GOS)
# 
# main_industry_accounts<- main_industry_accounts %>%
#   mutate(gross_cap_plus_lab = GOS + CoE,
#          net_cap_plus_lab = NOS + CoE)
# 
# 
# # gather to long format to make calculation of shares easier
#   # Calc gross and net shares separately
#   # gross
# gross_shares<- main_industry_accounts %>%
#   select(country, year, ACTIVITY, CoE, CoSE, GOS,
#          non_housing_gross_CAP, housing_gross_CAP, gross_cap_plus_lab)
# 
# gross_shares<- gross_shares %>%
#   gather(transaction, obsValue, -c(country, year, ACTIVITY,
#                                    gross_cap_plus_lab)) %>%
#   mutate(gross_share = obsValue/gross_cap_plus_lab) %>%
#   select(country, year, ACTIVITY, transaction, gross_share)
#   
#   # net
# net_shares<- main_industry_accounts %>%
#   select(country, year, ACTIVITY, CoE, CoSE, NOS,
#          non_housing_net_CAP, housing_net_CAP, net_cap_plus_lab)
# 
# net_shares<- net_shares %>%
#   gather(transaction, obsValue, -c(country, year, ACTIVITY,
#                                    net_cap_plus_lab)) %>%
#   mutate(net_share = obsValue/net_cap_plus_lab) %>%
#   select(country, year, ACTIVITY, transaction, net_share)
# 
# 
# 
# 
# # calculate shares in gross and net value added (at factor price)
# industry_accounts<- industry_accounts %>%
#   mutate(gross_share = obsValue/gross_cap_plus_lab,
#          net_share = obsValue/net_cap_plus_lab)
# 
# 
# # WHAT IS GOING WITH ICELAND AND SWEDEN -INF data?
# 
# 
# gross_shares<- agg_industry_accounts %>%
#   select(country, year,CoE, CoSE, GOS,
#          non_housing_cap_gross, housing_cap_gross, gross_cap_plus_lab) %>%
#   drop_na()
# 
# gross_shares<- gross_shares %>%
#   gather(transaction, value, 
#          -c(country, year, gross_cap_plus_lab)) %>%
#   mutate(share_of_cap_plus_lab = value/gross_cap_plus_lab)
# 
# net_shares<- agg_industry_accounts %>%
#   select(country, year, CoE, CoSE, GOS,
#          non_housing_cap_net, housing_cap_net, net_cap_plus_lab) %>%
#   drop_na()
# 
# net_shares<- net_shares %>%
#   gather(transaction, value, 
#          -c(country, year, net_cap_plus_lab)) %>%
#   mutate(share_of_cap_plus_lab = value/net_cap_plus_lab)
# 
# 
# 
# # # check sum equals total ----
# # # calculate sum across industries
# # sum_activities<- industry_accounts %>%
# #   filter(ACTIVITY %in% main_activity_names) %>%
# #   group_by(country, year, transaction) %>%
# #   summarise(sum_of_activities = sum(obsValue, na.rm=TRUE)) 
# # 
# # 
# # 
# # # grab total
# # total_activity<- industry_accounts %>%
# #   filter(ACTIVITY == "VTOT") %>%
# #   select(-ACTIVITY) %>%
# #   rename(VTOT = obsValue)
# # 
# # # Merge in with sum and calculate share
# # sum_activities<- merge(sum_activities, total_activity)
# # sum_activities<- sum_activities %>%
# #   mutate(sum_share_in_VTOT = sum_of_activities/VTOT,
# #          sum_share_in_VTOT = replace(sum_share_in_VTOT, # overide if correctly zero
# #                                  (sum_of_activities==0 & VTOT ==0),
# #                                  1))
# # 
# # 
# # # Browse country-year-transactions whose total lies within a tolerance
# # 
# # tolerance<- 0.005 # half a percent tolerance 
# # 
# # br<- sum_activities %>%
# #   filter((sum_share_in_VTOT<(1-tolerance) | sum_share_in_VTOT>(1+tolerance)))
# # 
# # 
# # # merge with the disaggregated industry data
# # industry_accounts<- merge(industry_accounts, sum_activities)
# # 
# # 
# # # convert to wide format
# # 
# # transactions<- transactions %>%
# #   select(-c(sum_of_activities, VTOT, share_in_VTOT)) %>%
# #   spread(TRANSACT, obsValue)
# 
# # Drop observations where the total does not sum close to 1
# 
# tolerance<- 0.005 # half a percent tolerance 
# 
# # Gross shares 
# # NB For some reason Finland does not sum to 1 
# # (GOS not breaking down exactly)
# gross_shares<- gross_shares %>%
#   select(-value) %>%
#   spread(transaction,share_of_cap_plus_lab) %>%
#   mutate(test_sum = CoE + CoSE + non_housing_cap_gross + housing_cap_gross) %>%
#   filter(!(test_sum<(1-tolerance) | test_sum>(1+tolerance))) %>%
#   select(-c(test_sum, gross_cap_plus_lab)) %>%
#   gather(transaction,share_of_cap_plus_lab, -c(country, year))
# 
# 
# # Net shares 
# net_shares<- net_shares %>%
#   select(-value) %>%
#   spread(transaction,share_of_cap_plus_lab) %>%
#   mutate(test_sum = CoE + CoSE + non_housing_cap_net + housing_cap_net) %>%
#   filter(!(test_sum<(1-tolerance) | test_sum>(1+tolerance))) %>%
#   select(-c(test_sum, net_cap_plus_lab)) %>%
#   gather(transaction,share_of_cap_plus_lab, -c(country, year))
# 
# 
# 
# # SAVE -----
# 
# OECD_gross_shares<- gross_shares
# fp<- paste0(manip_dir, "OECD_gross_shares.Rda")
# save(OECD_gross_shares, file=fp)
# 
# OECD_net_shares<- net_shares
# fp<- paste0(manip_dir, "OECD_net_shares.Rda")
# save(OECD_net_shares, file=fp)
# 

# TIDY FINAL CONSUMPTION DATA ------

# load country mapping
load("Manipulated data/OECD country mapping.Rda")

# load API data
load("Original data/OECD API outputs/rental_consumption.Rda")

# Keep current price data only
rental_consumption<- rental_consumption %>%
  filter(MEASURE == "C")

# Sum actual and imputed rent
rental_consumption<- rental_consumption %>%
  group_by(LOCATION, obsTime) %>%
  summarise(total_rent = sum(obsValue))


# Standardize country names
rental_consumption<- merge(rental_consumption, country_names)

rental_consumption <- rental_consumption %>%
  rename(country = Our.World.In.Data.Name) %>%
  mutate(year = as.numeric(obsTime)) %>%
  select(year, country, total_rent)


# Save
save(rental_consumption, 
     file="Manipulated data/final_consumption_of_rent.Rda")



# TIDY SECTOR DATA ----

# load country mapping
load("Manipulated data/OECD country mapping.Rda")

# load API data
load("Original data/OECD API outputs/sector_accounts.Rda")

# Standardize country names
sector_accounts<- merge(sector_accounts, country_names)

sector_accounts <- sector_accounts %>%
  rename(country = Our.World.In.Data.Name) %>%
  mutate(year = as.numeric(obsTime)) 

sector_accounts<- sector_accounts %>%
  select(country, TRANSACT, SECTOR, year, obsValue)

# Select needed transactions ------

sector_share_data<- sector_accounts %>%
  mutate(transaction = as.character(NA)) %>%
  mutate(transaction = replace(transaction,
                               SECTOR == "S1" & TRANSACT =="NFB1GP",
                               "GDP_output"),
         transaction = replace(transaction,
                               SECTOR == "S1" & TRANSACT =="B1_GE",
                               "GDP_expenditure"),
         transaction = replace(transaction,
                               SECTOR == "S1" & TRANSACT =="NFD1P",
                               "total_CoE"),
         transaction = replace(transaction,
                               SECTOR == "S1" & TRANSACT =="NFB2GP",
                               "total_GOS"),
         transaction = replace(transaction,
                               SECTOR == "S12" & TRANSACT =="NFD1P",
                               "finCorp_CoE"),
         transaction = replace(transaction,
                               SECTOR == "S12" & TRANSACT =="NFB2GP",
                               "finCorp_GOS"),
         transaction = replace(transaction,
                               SECTOR == "S11" & TRANSACT =="NFD1P",
                               "nonfinCorp_CoE"),
         transaction = replace(transaction,
                               SECTOR == "S11" & TRANSACT =="NFB2GP",
                               "nonfinCorp_GOS"),
         transaction = replace(transaction,
                               SECTOR == "S1" & TRANSACT =="NFB3GP",
                               "mixed_inc"),
         transaction = replace(transaction,
                               SECTOR == "S14" & TRANSACT =="NFB2GP",
                               "household_GOS"),
         transaction = replace(transaction,
                               SECTOR == "S1" & TRANSACT =="NFD2P",
                               "taxes_on_prod"),
         transaction = replace(transaction,
                               SECTOR == "S1" & TRANSACT =="NFD3R",
                               "subsidies_on_prod"),
         
  ) %>%
  filter(!is.na(transaction)) %>%
  select(country, year, transaction, obsValue)


# spread to wide format

sector_share_data<- sector_share_data %>%
  spread(transaction, obsValue)

# note that expenditure side data for GDP has additional coverage
br<- sector_share_data %>%
  filter(is.na(GDP_expenditure) & !is.na(GDP_output))

br2<- sector_share_data %>%
  filter(is.na(GDP_output) & !is.na(GDP_expenditure))

# calculate factor cost value added 
# as GDP_expenditure - (taxes_on_prod - subsidies_on_prod)

sector_share_data<- sector_share_data %>%
  mutate(factor_cost_VA = GDP_expenditure - 
           (taxes_on_prod - subsidies_on_prod))


# Check components sum correctly

sector_share_data<- sector_share_data %>%
  mutate(sum_check = (total_CoE + total_GOS + mixed_inc)/factor_cost_VA)


# Mixed income: impute cap and labour income components --------

  # calculate combined corp sector CoE and GOS and factor cost VA (as the sum)
sector_share_data<- sector_share_data %>%
  mutate(corp_CoE = finCorp_CoE + nonfinCorp_CoE,
         corp_GOS = finCorp_GOS + nonfinCorp_GOS,
         corp_factor_cost_VA = corp_CoE + corp_GOS)


  # Calculate cap share in corp sector:
sector_share_data<- sector_share_data %>%
  mutate(corp_cap_share_of_corp_factor_cost_VA = corp_GOS/corp_factor_cost_VA)

  # Impute mixed income based on corp cap share
sector_share_data<- sector_share_data %>%
  mutate(mixed_inc_cap = (mixed_inc * corp_cap_share_of_corp_factor_cost_VA))


# Calculate overall and 'housing' capital share -----
  # NB. For the reasons discussed in the paper, household GOS does not delineate 
    # housing income particularly well.
sector_share_data<- sector_share_data %>%
  mutate(cap_share_of_factor_cost_VA = (mixed_inc_cap + total_GOS)/
                                                        factor_cost_VA)

sector_share_data<- sector_share_data %>%
  mutate(hh_GOS_share_of_factor_cost_VA = household_GOS/factor_cost_VA)

sector_accounts_capital_share<- sector_share_data %>%
  select(country, year, 
    cap_share_of_factor_cost_VA, 
    hh_GOS_share_of_factor_cost_VA)

# Save capital shares
save(sector_accounts_capital_share, 
     file="Manipulated data/sector_accounts_capital_share.Rda")


# Save factor cost VA for use with the rent consumption series

factor_cost_VA_data<- sector_share_data %>%
  select(country, year, factor_cost_VA) %>%
  drop_na()

save(factor_cost_VA_data, 
     file="Manipulated data/OECD_factor_cost_VA_data.Rda")


# CALCULATE CONSUMPTION HOUSING SHARES ----

load("Manipulated data/final_consumption_of_rent.Rda")
load("Manipulated data/OECD_factor_cost_VA_data.Rda")


# Merge rent consumption data with factor cost VA derived from sector data
consump_housing_share<- merge(factor_cost_VA_data, rental_consumption)

# calculate share of factor cost VA
consump_housing_share<- consump_housing_share %>%
  mutate(rent_consumption_share_of_factor_cost_VA = total_rent/factor_cost_VA) %>%
  select(country, year, rent_consumption_share_of_factor_cost_VA)


# Save
save(consump_housing_share, 
     file="Manipulated data/consump_housing_share.Rda")



# COMBINE CONSUMPTION, SECTOR AND INDUSTRY HOUSING SHARES -----


# load and prepare the OECD consumption, sector and industry share data
  # (all calculated above)

# consumption:
load("Manipulated data/consump_housing_share.Rda") 

consump_housing_share<- consump_housing_share %>%
  rename(OECD_consumption_share = rent_consumption_share_of_factor_cost_VA)

# sector:
load("Manipulated data/sector_accounts_capital_share.Rda") 

sector_housing_share<- sector_accounts_capital_share %>%
  select(country, year, hh_GOS_share_of_factor_cost_VA) %>%
  rename(OECD_hh_GOS_share = hh_GOS_share_of_factor_cost_VA)

# industry 
load("Manipulated data/OECD industry data - aggregate factor shares.Rda") 

# take the housing capital income share of VA from the
  # industry data factor shares (prepared above)
industry_housing_share<- aggregate_factor_shares %>%
  filter(transaction == "housing_gross_CAP") %>%
  rename(OECD_RE_industry_CAP_share = gross_share) %>%
  select(country, year, OECD_RE_industry_CAP_share)

# merge three datasets together
housing_share_three_approaches<- merge(
  consump_housing_share, sector_housing_share, all = TRUE)

housing_share_three_approaches<- merge(
  housing_share_three_approaches,
  industry_housing_share, all = TRUE)

# Save
save(housing_share_three_approaches, 
     file="Manipulated data/housing_share_three_approaches.Rda")




# RELATIVE PRICE OF RENT ----

# load country mapping
load("Manipulated data/OECD country mapping.Rda")

# Rent price index -----

# load API data
load("Original data/OECD API outputs/rent_price_index.Rda")


# Standardize country names
country_names_alt<- country_names %>%
  rename(COU = LOCATION)

rent_price_index<- merge(rent_price_index, country_names_alt)

rent_price_index <- rent_price_index %>%
  rename(country = Our.World.In.Data.Name,
         housing_CPI = obsValue) %>%
  mutate(year = as.numeric(obsTime)) %>%
  filter(!is.na(year)) #drop quarterly data

rent_price_index<- rent_price_index %>%
  select(country, year, housing_CPI)


# Overall price index -----


# load API data
load("Original data/OECD API outputs/CPI.Rda")


# Standardize country names
CPI<- merge(CPI, country_names)

CPI <- CPI %>%
  rename(country = Our.World.In.Data.Name,
         overall_CPI = obsValue) %>%
  mutate(year = as.numeric(obsTime))

CPI <- CPI %>%
  select(country, year, overall_CPI)

# Calculate relative price index ----

relative_rent_price_CPI<- merge(rent_price_index, CPI)

relative_rent_price_CPI<- relative_rent_price_CPI %>%
  mutate(relative_rent_price = housing_CPI/overall_CPI) %>%
  select(country, year, relative_rent_price)

# Save
save(relative_rent_price_CPI, file="Manipulated data/relative_rent_price_CPI.Rda")


