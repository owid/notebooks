library(tidyverse)
library(rsdmx)


# GDP AT PPPs ----

GDP_PPP<- readSDMX(providerId = "OECD",
                       resource = "data",
                      flowRef = "SNA_TABLE1",
                      key = ".B1_GE.VPVOB",
                       start = 1950,
                      end = 2020,
                      dsd = TRUE)


GDP_PPP<- as.data.frame(GDP_PPP)

# Save
save(GDP_PPP, file="Original data/OECD API outputs/GDP_PPP_raw.Rda")

# HOUSING CONSUMPTION ------
rental_consumption <- readSDMX(providerId = "OECD",
                            resource = "data",
                            flowRef = "SNA_TABLE5",
                            key = ".P31CP041+P31CP042.C+VOB",
                            start = 1950,
                            end = 2020,
                            dsd = TRUE)

rental_consumption<- as.data.frame(rental_consumption)

# Save
save(rental_consumption, file="Original data/OECD API outputs/rental_consumption.Rda")


# RENT PRICE -----
# This is the CPI component for actual rentals or else the aggrgeate
  # of actual and imputed rentals and maintenance. See paper for details.

rent_price_index <- readSDMX(providerId = "OECD",
                               resource = "data",
                               flowRef = "HOUSE_PRICES",
                               key = ".RPI",
                               start = 1950,
                               end = 2020,
                               dsd = TRUE)

rent_price_index<- as.data.frame(rent_price_index)


# Save
save(rent_price_index, file="Original data/OECD API outputs/rent_price_index.Rda")

# CPI ------

CPI <- readSDMX(providerId = "OECD",
                             resource = "data",
                             flowRef = "PRICES_CPI",
                             key = ".CPALTT01.IXOB.A",
                             start = 1950,
                             end = 2020,
                             dsd = TRUE)

CPI<- as.data.frame(CPI)

  # the single subject-measure CPALTT01 - IXOB refers to all items
    # CPI index. 2015=100

# Save
save(CPI, file="Original data/OECD API outputs/CPI.Rda")

# GDP deflator ------

GDP_deflator <- readSDMX(providerId = "OECD",
                resource = "data",
                flowRef = "EO",
                key = ".PGDP.A",
                start = 1950,
                end = 2020,
                dsd = TRUE)

GDP_deflator<- as.data.frame(GDP_deflator)

# the single subject-measure CPALTT01 - IXOB refers to all items
# CPI index. 2015=100

# Save
save(GDP_deflator, file="Original data/OECD API outputs/GDP_deflator.Rda")





# SECTOR ACCOUNTS ------


# Grab full dataset

sector_accounts <- readSDMX(providerId = "OECD",
                        resource = "data",
                        flowRef = "SNA_TABLE14A",
                        key = "..S1+S2+S11+S12+S13+S14_S15+S14+S15.C",
                        start = 1950,
                        end = 2020,
                        dsd = TRUE)

sector_accounts<- as.data.frame(sector_accounts)

# Save
save(sector_accounts, file="Original data/OECD API outputs/sector_accounts.Rda")


# INDUSTRY VALUE ADDED DATA ----------

# set paramaters for API query

select_table<- "SNA_TABLE6A_ARCHIVE" # Value added and its components by activity, ISIC rev4

start_year<- 1950
end_year<- 2020

countries<- "" # leave blank for all entities
transactions<- "" # i.e. output/GOS/CoE etc. leave blank for all
activities<- "" # ISIC rev 4 industries. leave blank for all industries and sub-industries
measures<- "C+VOB" # Prices. C = constant; VOB = indexed to OECD base year

key_query<- paste(countries,transactions,activities,measures, sep = ".")

industry_accounts <- readSDMX(providerId = "OECD",
                              resource = "data",
                              flowRef = select_table,
                              key = key_query,
                              start = start_year,
                              end = end_year,
                              dsd = TRUE)

industry_accounts<- as.data.frame(industry_accounts)

# Save
save(industry_accounts, file="Original data/OECD API outputs/industry_accounts.Rda")


# INDUSTRY LABOUR INPUTS DATA ----

# set paramaters for API query

select_table<- "SNA_TABLE7A_ARCHIVE" # Labour intput by activity, ISIC rev4

start_year<- 1950
end_year<- 2020


countries<- "" # leave blank for all entities
transactions<- "" # i.e. total employment/employed/self-employed. leave blank for all
activities<- "" # ISIC rev 4 industries. leave blank for all industries and sub-industries
measures<- "HRS" # i.e. hours/jobs/fte. HRS = hours in millions

key_query<- paste(countries,transactions,activities,measures, sep = ".")

employment_by_industry <- readSDMX(providerId = "OECD",
                              resource = "data",
                              flowRef = select_table,
                              key = key_query,
                              start = start_year,
                              end = end_year,
                              dsd = TRUE)

employment_by_industry<- as.data.frame(employment_by_industry)


# Save
save(employment_by_industry, file="Original data/OECD API outputs/employment_by_industry.Rda")


