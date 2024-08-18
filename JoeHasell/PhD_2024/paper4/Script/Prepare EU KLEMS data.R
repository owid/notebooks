# For documentation of data see:
# chrome-extension://bomfdkbfpdhijjbeoicnfhjbdhncfhig/view.html?mp=xmskWMiI

# Issues:
# Why no fall in US labour share??
# What's going on with Portugal in the 70s? Note that the description of the 
  # sources in EU KLEMS 2009 documentation is incomplete.



# LOAD LIBRARIES --------------
library(tidyverse)
library(readxl) # For handling xls source data files


# I first grab the data for four 'transactions':value added, employee comp, 
  # labour comp and capital comp data. These are arranged differently across
  # three different data files: one for USA (SIC data), one for Canada, and
  # one for a much larger dataset covering European countries.


# lists to store the data from the different workbooks
ind_data_list<- list()
sector_descriptions_list<- list()

# IMPORT CANADA 2008 DATA ----


orginal_data<- list()
industry_data<- list()

file_name<- "can_output_08I.xls"
fp<- paste0("Original data/KLEMS/", file_name)

for(transaction in c("VA", "COMP", "LAB", "CAP")){

      orginal_data[[transaction]]<- as.data.frame(read_excel(fp,
                                             sheet = transaction))

  # Organise industry as a long format dataframe
  industry_data[[transaction]]<- orginal_data[[transaction]] %>%
    gather(year, !!transaction, -c(desc, code)) %>% # convert to long format
    mutate(year = as.numeric(gsub( "_", "",year))) %>% # make year var numeric
    select(-desc) # drop industry description var (we will just use 'code')
  
  # Spread to wide (each industry is a column)
  industry_data[[transaction]]<- industry_data[[transaction]] %>%
    mutate(code = paste0("code_", code)) %>%
    spread(code, !!transaction)

  # Calculate total across all industries
  industry_data[[transaction]]<- industry_data[[transaction]] %>%
    mutate(TOT = rowSums(across(!year)))
    
  # calculate aggregate industries (in order to be comparable with 
    # other countries).
  industry_data[[transaction]]<- industry_data[[transaction]] %>%
    mutate(D = code_15t16 +
             code_17t19 +
             code_20 +
             code_21t22 +
             code_23 +
             code_24 +
             code_25 +
             code_26 +
             code_27t28 +
             code_29 +
             code_30t33 +
             code_34t35 +
             code_36t37,
           G = code_50 +
             code_51 +
             code_52,
           I = code_60t63 +
             code_64,
           K = code_70 +
             code_71t74
    )
          
  # gather data back to long format again and add country var
  industry_data[[transaction]]<- industry_data[[transaction]] %>% 
    gather(code, !!transaction, -year) %>%
    mutate(code = gsub("code_", "", code)) %>%
    mutate(country = "CAN")
  
}

# Store all data from this data source in a list
ind_data_list[["CAN"]]<- industry_data


# Store sector descriptions to merge back in later if needed
sector_descriptions_list[["CAN"]]<- orginal_data[["VA"]] %>%
  select(desc, code) %>%
  unique()


  
# USA-SIC 2008 DATA ----
  
# Similar to Canada, except in the data for US, a total line is given. 
  # We use this for the aggregate, and drop it from the industry-level data

orginal_data<- list()
industry_data<- list()

file_name<- "usa_sic_output_08I.xls"
fp<- paste0("Original data/KLEMS/", file_name)
  
for(transaction in c("VA", "COMP", "LAB", "CAP")){
    
  orginal_data[[transaction]]<- as.data.frame(read_excel(fp,
                                          sheet = transaction))
   
  orginal_data[[transaction]]<- orginal_data[[transaction]] %>%
   filter(rowSums(is.na(.)) != (ncol(.)-2)) # Drop sub industries with
                                              # no data in any year
  
  # Organise industry as a long format dataframe (this dataset already 
    # includes the aggregate as a row)
  industry_data[[transaction]]<- orginal_data[[transaction]] %>%
    gather(year, !!transaction, -c(desc, code)) %>% # convert to long format
    mutate(year = as.numeric(gsub( "_", "",year))) %>% # make year var numeric
    select(-desc) # drop industry description var (we will just use 'code')
    
  # add a country var
  industry_data[[transaction]]<- industry_data[[transaction]] %>%
    mutate(country = "USA-SIC")
}
  
# Store all data from this data source in a list
ind_data_list[["USA-SIC"]]<- industry_data
  
  
# Store sector descriptions to merge back in later if needed
sector_descriptions_list[["USA-SIC"]]<- orginal_data[["VA"]] %>%
  select(desc, code) %>%
  unique()
  


# MAIN DATA (2011) ----

# Import
df_09 <- read.csv("Original data/KLEMS/all_countries_09I 2.csv")

# convert to long format
klems<- df_09 %>%
  gather(year, value, -c(country, var, code)) %>%
  mutate(year = as.numeric(gsub( "X_", "",year)))

industry_data<- list()

for(transaction in c("VA", "COMP", "LAB", "CAP")){
  
  industry_data[[transaction]]<- klems %>%
    filter(var == transaction) %>%
    select(country, code, year, value) %>%
    rename(!!transaction := value)
  
}

ind_data_list[["KLEMS-Main"]]<- industry_data

# APPEND DATA FROM DIFFERENT WORKBOOKS INTO SINGLE DATAFRAMES ----

for(transaction in c("VA", "COMP", "LAB", "CAP")){
 
  industry_data[[transaction]]<- rbind(ind_data_list[["CAN"]][[transaction]],
                                       ind_data_list[["USA-SIC"]][[transaction]]) 

  industry_data[[transaction]]<- rbind(industry_data[[transaction]],
                                       ind_data_list[["KLEMS-Main"]][[transaction]])   
  
}

# MERGE TRANSACTIONS INTO SINGLE DATAFRAME ----

# Merge all the aggregate transactions together 
all_data<- merge(industry_data[["VA"]], industry_data[["COMP"]], all=TRUE)
all_data<- merge(all_data, industry_data[["LAB"]], all=TRUE)
all_data<- merge(all_data, industry_data[["CAP"]], all=TRUE)

# Some details with the distinction between 0 and missing data:

# Any industry where VA = CAP but LAB is missing, set LAB = 0
all_data<- all_data %>%
  mutate(LAB = replace(LAB,
                       VA==CAP & is.na(LAB),
                       0))

# Any industry where VA = LAB but CAP is missing, set CAP = 0

all_data<- all_data %>%
  mutate(CAP = replace(CAP,
                       VA==LAB & is.na(CAP),
                       0))

# Drop Belgium for 2005-7 since VA != CAP + LAB in 2005/6 (neither individual industries 
  # nor the reported total across all industries) and no LAB or CAP data in 2007
all_data<- all_data %>%
  filter(!(country == "BEL" & year >= 2005))


# Drop any country-year-industry obs that do not have data for all 4 transactions
all_data<- all_data %>%
  drop_na() 

# Adjust labour and cap income to reflect two scenarios
  # Method 1:  just as KLEMS have calculated
all_data<- all_data %>%
  rename(gross_CAP_1 = CAP,
         LAB_1 = LAB)

  # Method 2: set minimum CAP as 0 and recalculate LAB
all_data<- all_data %>%
  mutate(gross_CAP_2 = pmax(0, gross_CAP_1),
         LAB_2 = pmin(LAB_1 + gross_CAP_1, LAB_1))

# Calculate imputed income of self employed as labour comp 
# less employeee comp (under the two methods)
all_data<- all_data %>%
  mutate(CoSE_1 = LAB_1 - COMP,
         CoSE_2 = LAB_2 - COMP)

# AGGREGATE OVER INDUSTRIES -----

# Aggregate over industries (excluding sub-industries) and check totals

# This list gives the main industry headings
main_industry_codes<- c("AtB",
                        "C",
                        "D",
                        "E",
                        "F",
                        "G",
                        "H",
                        "I",
                        "J",
                        "K",
                        "L",
                        "M",
                        "N",
                        "O",
                        "P",
                        "Q")

# filter out sub-industries
main_industry_accounts<- all_data %>%
  filter(code %in% main_industry_codes)

# sum across main industries
agg_industry_accounts<- main_industry_accounts %>%
  group_by(country, year) %>%
  summarise(VA = sum(VA, na.rm=TRUE),
            gross_CAP_1 = sum(gross_CAP_1, na.rm=TRUE),
            gross_CAP_2 = sum(gross_CAP_2, na.rm=TRUE),
            COMP = sum(COMP, na.rm=TRUE),
            CoSE_1 = sum(CoSE_1, na.rm=TRUE),
            CoSE_2 = sum(CoSE_2, na.rm=TRUE),
            LAB_1 = sum(LAB_1, na.rm=TRUE),
            LAB_2 = sum(LAB_2, na.rm=TRUE)) %>%
  gather(transaction, obsValue, -c(country, year))


# check against reported totals ----

reported_totals<- all_data %>%
  filter(code == "TOT") %>%
  select(country, year, VA, COMP, LAB_1, gross_CAP_1) %>%
  gather(transaction, reported_total, -c(country, year))


bad_totals<- left_join(agg_industry_accounts, reported_totals)

bad_totals<- bad_totals %>%
  mutate(total_check = obsValue/reported_total)

tolerance<- 0.0005 # one twentieth of a percent tolerance

bad_totals<- bad_totals %>%
  filter((total_check<(1-tolerance) | total_check>(1+tolerance))) %>%
  mutate(bad_total = 1)

br<- bad_totals %>%
  filter(bad_total == 1)
# For Poland the total VA and CAP is slightly different (0.1-0.5 %) to the
  # reported total. But the gap is roughly consistent over time so we keep
  # Poland in the sample.


# Spread aggregate data back to wide format
agg_industry_accounts<- agg_industry_accounts %>%
  spread(transaction, obsValue)




# SEPARATE HOUSING CAP INCOME -----

# Note that within real estate activity there is no issue around labour share
  # being >100%. So the figrues from each of the two methods are the same.

br<- all_data %>%
  filter(code == "70", #'70' = Real estate activities
        gross_CAP_1 != gross_CAP_2)

# find housing cap and store it as if it relates to the total across industries
housing_cap<- all_data %>%
  filter(code == "70") %>% #'70' = Real estate activities
  rename(housing_gross_CAP = gross_CAP_1) %>%
  select(year, country, housing_gross_CAP)

# merge housing cap back into main dataframe
agg_industry_accounts<- left_join(agg_industry_accounts, housing_cap)

# calculate (aggregate) non-housing cap as total cap less housing cap

agg_industry_accounts<- agg_industry_accounts %>%
  mutate(non_housing_gross_CAP_1 = gross_CAP_1 - housing_gross_CAP,
         non_housing_gross_CAP_2 = gross_CAP_2 - housing_gross_CAP)



# CALCULATE AGGREGATE SHARES -----------

# Calc factor price VA = CAP + LAB
agg_industry_accounts<- agg_industry_accounts %>%
  mutate(CAP_plus_LAB = gross_CAP_1 + LAB_1)

# Question: does VA = CAP + LAB?
  # -> Answer: always (except for Belgium 2005-6 which was dropped earlier)

tolerance<- 0.001
br<- agg_industry_accounts %>%
  filter((VA > CAP_plus_LAB * (1 + tolerance)) |
           (VA < CAP_plus_LAB * (1 - tolerance)))


# calculate shares out of CAP + LAB
agg_industry_accounts<- agg_industry_accounts %>%
  gather(transaction, value, # convert to long format to make the calc easier
         -c(country, year, CAP_plus_LAB)) %>%
  mutate(share_of_CAP_plus_LAB = value/CAP_plus_LAB)

# check sum to 1
sum_check_method1<- agg_industry_accounts %>%
  filter(transaction %in% c("non_housing_gross_CAP_1",
                            "housing_gross_CAP",
                            "CoSE_1",
                            "COMP")) %>%
  group_by(country, year) %>%
  summarise(sum_CAP_plus_LAB = sum(share_of_CAP_plus_LAB))

sum_check_method2<- agg_industry_accounts %>%
  filter(transaction %in% c("non_housing_gross_CAP_2",
                            "housing_gross_CAP",
                            "CoSE_2",
                            "COMP")) %>%
  group_by(country, year) %>%
  summarise(sum_CAP_plus_LAB = sum(share_of_CAP_plus_LAB))


# CALCULATE INDUSTRY SHARES -----------

# Calc factor price VA = CAP + LAB
all_data<- all_data %>%
  mutate(CAP_plus_LAB = gross_CAP_1 + LAB_1)

# Question: does VA = CAP + LAB?
# -> Answer: always (except for Belgium 2005-6 which was dropped earlier)

tolerance<- 0.001
br<- all_data %>%
  filter((VA > CAP_plus_LAB * (1 + tolerance)) |
           (VA < CAP_plus_LAB * (1 - tolerance)))


# calculate shares out of CAP + LAB
all_data<- all_data %>%
  gather(transaction, value, # convert to long format to make the calc easier
         -c(country, code, year, CAP_plus_LAB)) %>%
  mutate(share_of_CAP_plus_LAB = value/CAP_plus_LAB)

# check sum to 1
sum_check_method1<- all_data %>%
  filter(transaction %in% c("gross_CAP_1",
                            "CoSE_1",
                            "COMP")) %>%
  group_by(country, year, code) %>%
  summarise(sum_CAP_plus_LAB = sum(share_of_CAP_plus_LAB))

sum_check_method2<- all_data %>%
  filter(transaction %in% c("gross_CAP_2",
                            "CoSE_2",
                            "COMP")) %>%
  group_by(country, year, code) %>%
  summarise(sum_CAP_plus_LAB = sum(share_of_CAP_plus_LAB))

# FINAL TIDYING AND COUNTRY NAME STANDARDIZATION ----

# select variables

aggregate_factor_shares<- agg_industry_accounts %>%
  select(country, year,  transaction, share_of_CAP_plus_LAB) %>%
  rename(gross_share = share_of_CAP_plus_LAB)

industry_factor_shares<- all_data %>%
  select(country, year, code, transaction, share_of_CAP_plus_LAB) %>%
  rename(gross_share = share_of_CAP_plus_LAB)


# select which US series to be used


aggregate_factor_shares<- aggregate_factor_shares %>%
  filter(!country == "USA-NAICS")

industry_factor_shares<- industry_factor_shares %>%
  filter(!country == "USA-NAICS")


# merge-in industry descriptions (from the US data, which is comprehensive)
industry_factor_shares<- left_join(industry_factor_shares,
                                    sector_descriptions_list[["USA-SIC"]])

# Standardize country names

KLEMS_country_names<- read.csv(
    "Original data/EU_KLEMS_countries_country_standardized.csv")

KLEMS_country_names<- KLEMS_country_names %>%
  rename(country = Country)

# aggregate shares
aggregate_factor_shares<- merge(aggregate_factor_shares, KLEMS_country_names)

aggregate_factor_shares <- aggregate_factor_shares %>%
  select(-country) %>%
  rename(country = Our.World.In.Data.Name)


# industry-level shares
industry_factor_shares<- merge(industry_factor_shares, KLEMS_country_names)

industry_factor_shares <- industry_factor_shares %>%
  select(-country) %>%
  rename(country = Our.World.In.Data.Name)


# Save share data -----

# aggregate shares
fp<- "Manipulated data/KLEMS - aggregate factor shares.Rda"
save(aggregate_factor_shares, file=fp)

# industry-level shares
fp<- "Manipulated data/KLEMS - industry-level factor shares.Rda"
save(industry_factor_shares, file=fp)

