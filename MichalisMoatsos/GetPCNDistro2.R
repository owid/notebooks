# this is a script for fetching all distributions from PCN
# for all countries and regions/global
# Better run this during Weekends, because it seems to take less time 
# and returns less errors/missing obs

library(povcalnetR)
library(tictoc)
library(doParallel)
library(beepr)
library(tcltk)

#### OWID ####
# https://github.com/owid/importers
# https://github.com/owid/notebooks
# https://github.com/owid/notebooks/tree/main/MichalisMoatsos

# meet with Boby for the data structure
# https://github.com/owid/importers/tree/master/vdem/output
# actual data https://github.com/owid/importers/tree/master/vdem/output/datapoints
# for variable 10 https://github.com/owid/importers/blob/master/vdem/output/datapoints/datapoints_10.csv

#### Questions ####

# Why some distros do not go all the way to 100%, 
# Is it possible to request the full distro only instead of requesting all the PLs?
# Sometimes PCN library returns datayear as NA
# SUR <- povcalnet(country = "SUR") is empty, but there is an entry in POVCALNET!!!

#### Definitions ####
# http://iresearch.worldbank.org/PovcalNet/Docs/dictionary.html
# but those DO NOT cover all the columns returned by pocvalnetR functions

# Headcount (H):	% of population living in households with consumption or income per person below the poverty line.
# Survey year 	The "Survey year" is the year for which the income or consumption data were collected.
# Reference year	is year we choose to line up the data. The reference years currently available are 1981, 1984, 1987, 1990, 1993, 1996, 1999, 2002, 2005, 2008, 2010, 2011, 2012, 2013 and 2015.
# Mean$	The "Mean$" is $ the average monthly household per capita income or consumption expenditure from the survey in 2011 PPP.
# Median$	is the median of monthly household per capita income or consumption expenditure from the survey in 2011 PPP.
# PL	Poverty line in 2011 PPP per day. The default poverty line is $1.9 per day.
# PPP	refers to Purchasing Power Parity. The default option is the PPP exchange rates for household final consumption expenditure in 2011 in the World Development Indicators.
# Poverty Gap (PG): 	The mean shortfall of income from the poverty line. The mean is based on the entire population treating the nonpoor as having a shortfall of zero, and the shortfall is expressed as a proportion of the poverty line.
# Squared poverty gap (SPG): 	The mean squared shortfall of income from the poverty line. The mean is based on the entire population treating the nonpoor as having a shortfall of zero, and the shortfall is expressed as a proportion of the poverty line (and then squared).
# Watts' poverty index:	This is the mean across the population of the proportionate poverty gaps, as measured by the log of the ratio of the poverty line to income, where the mean is formed over the whole population, counting the nonpoor as having a zero poverty gap.
#	Gini index:	a measure of inequality between 0 (everyone has the same income) and 100 (richest person has all the income)
#	MLD index:	stands for the mean log deviation. This is an index of inequality, given by the mean across the population of the log of the overall mean divided by individual income.
#	Spatial CPI: 	A price index that reflects differences in prices faced in different locations at the same date.
#	Weighted national mean: 	The mean for the economy as a whole incorporating the statistical weights implied by the sample design to as to get an unbiased estimate of the population mean.
# Data Type: 	Type of welfare variable. Could either be income or consumption
#    C: grouped consumption
#    I: grouped income
#    i: unit-record income data with non-parametric analysis
#    c: unit-record consumption data with non-parametric analysis

#### Missing Definitions ####
# see which columns from what the API returns don't have definitions in the above

#### OWID Python parameters ####
# https://github.com/owid/importers/blob/master/povcal/main.py
# MIN_POV_LINE = 0
# MAX_POV_LINE = 1400
#def generate_poverty_lines_between(minimum_dollar, maximum_dollar):
#  lines = all_cents_between_dollars(minimum_dollar, min(60, maximum_dollar), 0.01)
#  lines.extend(
#    all_cents_between_dollars(
#      max(60.10, minimum_dollar), min(150, maximum_dollar), 0.10
#    )
#  )
#  lines.extend(
#    all_cents_between_dollars(
#      max(150.50, minimum_dollar), min(1400, maximum_dollar), 0.50
#    )
#  )

#def all_cents_between_dollars(minimum_dollar, maximum_dollar, increment=0.01):
#  return [
#    round(cent, 2)
#    for cent in np.arange(minimum_dollar, maximum_dollar + increment, increment)
#  ]

OWID_PLs <- c(seq(0.01,60,0.01),seq(60.1,150,0.1),seq(150.5,1400,0.5))

#### Investigation ####
# investigating the limitations of the API

# let's get the data from World Bank's PovcalNet API:
PCN <- povcalnet_info()
# PCN df is required to request all countries' info from PovcalNet:
HHS <- povcalnet(country = PCN$country_code)
CurrentISO3 <- 'CHN'

PLs <- seq(0.001,5,0.001)
IdealPLs <- c(seq(0.001,5,0.001),seq(5.01,45,0.01),seq(45.1,155,0.1))
TestPLs <- c(0.01, seq(1,20,1))

# using the country level function povcalnet_cl()
CurYear <- 2010
Distro <- povcalnet_cl(CurrentISO3,1,CurYear)
Distro <- subset(Distro,Distro$countrycode=='2398y9wfhehfsdih') # just maintain 
# the structure of the data as they are return by PCN API

tic()
for (i in 1:length(PLs)){
  Distro <- rbind(Distro,povcalnet_cl(rep(CurrentISO3,length(PLs[i])),PLs[i],rep(CurYear,length(PLs[i]))))
}
toc()
# therefore: with single line requests speed is at 0.39/sec
# total time for that would be
length(IdealPLs)*nrow(HHS)*0.39/3600
# 2238.47 hours
# way too high a number...
rm(Distro)

# Now, using the aggregate level function povcalnet:
# The time it takes to execute this simple request that returns all HHS for a 
# single PL takes is about 12.2 seconds to complete

tic()
Temp <- povcalnet(
  country = "all",
  povline = jjj,
  year = "all",
  aggregate = FALSE,
  fill_gaps = T,
  coverage = "all",
  ppp = NULL,
  url = "http://iresearch.worldbank.org",
  format = "csv"
)
toc()

# variables:
# country	
# character: list of country iso3 code (accepts multiple) or 'all'. Use povcalnet_info for full list of countries.
# povline	
# numeric: poverty line (in 2011 PPP-adjusted USD) to calculate poverty measures
# year	
# numeric: list of years, or 'all'.
# aggregate	
# logical: 'TRUE' will return aggregate results, 'FALSE' country-level results.
# fill_gaps	
# logical: 'TRUE' will interpolate / extrapolate values when surveys are not available for a specific year.
# coverage	
# character: Can take one of three values: 'national', 'urban', 'rural'
# ppp	
# numeric: Optional - Allows the selection of custom PPP (Purchasing Power Parity) exchange rates
# url	
# character: API root URL. For testing purposes only, should not be changed for 99 percent of users.
# format	
# character: Response format to be requested from the API: 'csv' or 'json'

# using this approach I will need:
length(IdealPLs)*12.2/3600
# 34 hours to complete, much better than the country level approach
# and it also gives you the option to request the in between gaps (interpolated)

# now I am trying to see if parallelism will make things even faster:

tic()
no_cores <- 20
cl <- makeCluster(no_cores, type="FORK")
registerDoParallel(cl)
Distro <- foreach(jjj=TestPLs, .combine='rbind', .errorhandling = "pass") %dopar% { 
  Temp <- povcalnet(
    country = "all",
    povline = jjj,
    year = "all",
    aggregate = FALSE,
    fill_gaps = T,
    coverage = "all",
    ppp = NULL,
    url = "http://iresearch.worldbank.org",
    format = "csv"
  )
  return(Temp)
}

stopCluster(cl)
registerDoSEQ()

beep(6)
toc()

# with 4 cores it takes 197.607 in total, and since this run for 20 TestPLs 
# this means 9.85 per request
length(IdealPLs)*9.85/3600
# 27.5 hours to complete, but no idea how stable this is

# with 10 cores 118.284, or 5.91 per request
length(IdealPLs)*5.91/3600
# 16.5 hours to complete, but no idea how stable this is

# with 20 cores 127.214, or 6.36 per request
length(IdealPLs)*6.36/3600
# 17.76 hours to complete, but no idea how stable this is
# actually a couple of other times it got stuck with 20 cores
# so I will opt for 10 cores

# but there will be an R bottleneck with the 
# many expansions of the data structure

#### Part A: Original Data, no imputed ####

##### Fetch All HHS WITHOUT interpolations ####

library(povcalnetR)
library(doParallel)

# my own take for Ideal PLs:
# IdealPLs <- c(seq(0.001,5,0.001),seq(5.01,45,0.01),seq(45.1,155,0.1))
# expanding it according to OWID_PLs, and according to the findings from 
# the limits of PCN script

IdealPLs <- c(seq(0.001,5,0.001),seq(5.01,60,0.01),seq(60.1,150,0.1),
              seq(150.5,1400,0.5), seq(1405,3000,5), seq(3010,10000,10),
              seq(11000,35000,100),99999)

for (i in c(seq(100,length(IdealPLs)-1,100),length(IdealPLs))){
  no_cores <- 10
  cl <- makeCluster(no_cores, type="FORK")
  registerDoParallel(cl)
  if (i>15100){
    low_i <- i-61
  } else {
    low_i <- i-99
  }
  Distro <- foreach(jjj=IdealPLs[c(low_i:i)], 
                    #.combine='rbind', 
                    .errorhandling = "pass") %dopar% { 
                      
                      ttt <- 8
                      while (ttt>0){
                        Temp <- povcalnet(
                          country = "all",
                          povline = jjj,
                          year = "all",
                          aggregate = FALSE,
                          fill_gaps = F,
                          coverage = "all",
                          ppp = NULL,
                          url = "http://iresearch.worldbank.org",
                          format = "csv"
                        )
                        
                        WrongEntries <- which(!trimws(format(Temp$povertyline,nsmall = 3))==
                                                trimws(format(jjj, nsmall = 3)))
                        
                        if (length(WrongEntries)>0){
                          ttt <- ttt - 1
                        } else {
                          ttt <- 0
                        }
                      }
                      
                      # I added this extra column because in several instances
                      # the poverty line returned from a particular country
                      # is much different from the poverty line requested
                      # e.g. when asking PL of 1.009 I got a 0.2264779
                      # PL for Burundi in 1981
                      # in the same df I got year 19892Y and datayear 0.0163
                      # for Belarus see 
                      # "/media/michalis/1984/PovcalNet/Examples/Distro1100.RData" oh I just deleted it...
                      Temp$RequestedLine <- jjj
                      return(Temp)
                    }
  stopCluster(cl)
  registerDoSEQ()
  # next time it must be width = 5 because it goes up to ~16000 and it does not 
  # sort properly in R:
  save(list = 'Distro',file = paste0('/media/michalis/1984/PovcalNet/NoFillGaps/Distro',formatC(i,width = 5, format = "d", flag = "0"),'.RData'))
  print(paste0('Saved file... ',paste0('/media/michalis/1984/PovcalNet/NoFillGaps/Distro',formatC(i,width = 5, format = "d", flag = "0"),'.RData')))
  rm(Distro)
}
rm(low_i)

###### Integrity Check and Combine saved data ####

# let's get the data from World Bank's PovcalNet API:
PCN <- povcalnet_info()
# PCN df is required to request all countries' info from PovcalNet:
HHS <- povcalnet(country = PCN$country_code)
TempDistro <- povcalnetR::povcalnet_cl('USA',1,2010)
TempDistro$RequestedLine <- as.numeric(NA)
MasterDistro <- subset(TempDistro,TempDistro$countrycode=='2398y9wfhehfsdih') # just maintain 
TempMasterDistro <- subset(TempDistro,TempDistro$countrycode=='2398y9wfhehfsdih') # just maintain 
# the data structure
FaultyEntries <- subset(TempDistro,TempDistro$countrycode=='2398y9wfhehfsdih') # just maintain 
# the data structure and add a comment column
FaultyEntries$Comments <- as.character(NA)
SavedDistrosFolder <- '/media/michalis/1984/PovcalNet/NoFillGaps'
TheFiles <- list.files(SavedDistrosFolder,pattern = 'Distro')
#TheFiles <- TheFiles[c(34:42,44:53)]
TheWrongList <- rep(as.numeric(NA),length(IdealPLs))
names(TheWrongList) <- trimws(format(IdealPLs, nsmall = 3))

options(warn=2) # turn warnings to errors, for better debugging
tictoc::tic()
for (i in c(1:length(TheFiles))){
#for (i in c(1)){
  # Load the saved data from the disk
  CurrentFile <- paste0(SavedDistrosFolder, '/',TheFiles[i])
  load(CurrentFile)
  print(CurrentFile)
  
  # First check: all list elements must have a fixed length of 32
  # equal to the number of columns returned by the PovcalNet API (31)
  # plus one extra column I add for control ("RequestedLine")
  # that stores the PL requested to the API.
  # Elements not complying are removed, and at the end of this process
  # we will have a reporting variable with all the PL values that
  # need to be requested again from the API
  
  if (!all(sapply(Distro, length)==32)){
    while (!all(sapply(Distro, length)==32)){
      # remove those that did not:
      Distro[[which(!(sapply(Distro, length)==32))[1]]] <- NULL
    }
    print(paste0('Current number of fetched PLs', length(Distro),". Normally this must be 100."))
  } else {
    print('No entries with less than 32 columns to remove...')
  }
  
  # Second check: all entries from a particular list element (so within each list
  # element) must have Distro$RequestedLine == Distro$povertyline
  # those that do not are kept in a separate dataframe
  # plus other integrity checks in the loop below:
  
  for (j in c(1:length(Distro))){
    
    Temp <- Distro[[j]]
    NewFaultyEntries <- subset(FaultyEntries,FaultyEntries$countrycode=='498heo98h')
    
    # Rule 0: no line with all NA, and no line with 
    # countrycode == "CountryCode"
    # and no line with countryname=="DELETE"
    Temp <- subset(Temp,!Temp$countrycode=="CountryCode")
    Temp <- subset(Temp,!Temp$countryname=="DELETE")
    
    # Rule 0.5: all PLs must be identical to the one requested
    WrongEntries <- which(!trimws(format(Temp$povertyline,nsmall = 3))==
                            trimws(format(Temp$RequestedLine, nsmall = 3)))
    NonIdenticalLines <- length(WrongEntries)
    
    FaultyTemp <- Temp[WrongEntries,]
    FaultyTemp$Comments <- 'PL not identical to the one requested'
    Temp <- suppressMessages(dplyr::anti_join(x = Temp, y = FaultyTemp))
    NewFaultyEntries <- rbind(NewFaultyEntries,FaultyTemp)
    
    # Rule 1: all PPPs from one ISO3 must be the same
    # and matching the value from HHS
    for (k in sort(unique(Temp$countrycode))){
      WrongEntries <- which(!Temp$ppp[which(Temp$countrycode==k)]==unique(HHS$ppp[which(HHS$countrycode==k)]))
      if (length(WrongEntries)>0){
        FaultyTemp <- Temp[which(Temp$countrycode==k)[WrongEntries],]
        # remove that entry from the Temp dataframe
        Temp <- suppressMessages(dplyr::anti_join(x = Temp, y = FaultyTemp))
        FaultyTemp$Comments <- 'Wrong PPP value'
        NewFaultyEntries <- rbind(NewFaultyEntries,FaultyTemp)
        rm(FaultyTemp)
      }
      rm(WrongEntries)
    }
    
    # Rule 2: columns "year" "datayear" and from isinterpolated until 
    # "decile10" must be numeric or convertible to numeric without warnings
    # define which columns must be numeric:
    NumericColumns <- c("year","datayear", names(Temp)[c(8:31)])
    # get the columns that actually are numeric:
    nums <- unlist(lapply(Temp, is.numeric)) 
    # and extract those that are not, although they should:
    WronglyNonNumericColumns <- NumericColumns[which(!NumericColumns %in% names(Temp)[nums])]
    # across those find the non-numeric entries:
    for (wrongcols in c(WronglyNonNumericColumns)){
      WrongEntries <- suppressWarnings(which(is.na(as.numeric(unlist(Temp[,wrongcols])))))
      NA_entries <- which(is.na((unlist(Temp[,wrongcols]))))
      WrongEntries <- WrongEntries[which(!WrongEntries %in% NA_entries)]
      if (length(WrongEntries)>0){
        FaultyTemp <- Temp[WrongEntries,]
        # remove that entry from the Temp dataframe
        Temp <- suppressMessages(dplyr::anti_join(x = Temp, y = FaultyTemp))
        FaultyTemp$Comments <- paste0('Non-numeric value in column ', wrongcols)
        NewFaultyEntries <- rbind(NewFaultyEntries,FaultyTemp)
        rm(FaultyTemp)
      }
      rm(WrongEntries)
    }
    
    # Rule 3: in non-interpolated entries "year", "datayear" must be identical 
    # with their corresponding HHS entry
    #WrongEntries <- which(!(Temp$coveragetype %in% HHS$coveragetype))
    #if (length(WrongEntries)>0){
    #  stop('build the code for Rule 3')
    #}
    #rm(WrongEntries)
    
    # Rule 4: interpolated values must be between the benchmark values used 
    # in the interpolation
    #WrongEntries <- which(!(Temp$coveragetype %in% HHS$coveragetype))
    #if (length(WrongEntries)>0){
    #  stop('build the code for Rule 4')
    #}
    #rm(WrongEntries)
    
    # Rule 5: coverage type must be from the range included in HHS
    WrongEntries <- which(!(Temp$coveragetype %in% HHS$coveragetype))
    if (length(WrongEntries)>0){
      stop('build the code for Rule 5')
    }
    rm(WrongEntries)
    
    # Rule 6: apply the allowed values limits to the data using
    # https://rdrr.io/cran/userfriendlyscience/man/checkDataIntegrity.html
    # to be developed...
    
    # keeping a log over the distros with different PLs than requested:
    TheWrongList[which(names(TheWrongList)==
                         as.character(unique(trimws(format(NewFaultyEntries$RequestedLine, 
                                                           nsmall = 3)))))] <- NonIdenticalLines
    
    rm(NonIdenticalLines)
    FaultyEntries <- rbind(FaultyEntries,NewFaultyEntries)
    rm(NewFaultyEntries)
    
    TempMasterDistro <- rbind(TempMasterDistro,Temp)
    rm(Temp)
  }
  MasterDistro <- rbind(MasterDistro,TempMasterDistro)
  TempMasterDistro <- subset(TempDistro,TempDistro$countrycode=='2398y9wfhehfsdih') 
  rm(Distro)
  print('-------------------------------------')
}
options(warn=0) # restore to default from warn=2
tictoc::toc()

#[1] "/media/michalis/1984/PovcalNet/NoFillGaps/Distro0500.RData"
#[1] "Current number of fetched PLs99. Normally this must be 100."
#[1] "/media/michalis/1984/PovcalNet/NoFillGaps/Distro1300.RData"
#[1] "Current number of fetched PLs99. Normally this must be 100."
#[1] "/media/michalis/1984/PovcalNet/NoFillGaps/Distro1700.RData"
#[1] "Current number of fetched PLs99. Normally this must be 100."
#[1] "/media/michalis/1984/PovcalNet/NoFillGaps/Distro2900.RData"
#[1] "Current number of fetched PLs99. Normally this must be 100."
#[1] "/media/michalis/1984/PovcalNet/NoFillGaps/Distro8900.RData"
#[1] "Current number of fetched PLs99. Normally this must be 100."
#[1] "/media/michalis/1984/PovcalNet/NoFillGaps/FDistro11200.RData"
#[1] "Current number of fetched PLs99. Normally this must be 100."
#[1] "/media/michalis/1984/PovcalNet/NoFillGaps/FDistro12600.RData"
#[1] "Current number of fetched PLs99. Normally this must be 100."
#[1] "/media/michalis/1984/PovcalNet/NoFillGaps/FDistro14700.RData"
#[1] "Current number of fetched PLs99. Normally this must be 100."
#[1] "/media/michalis/1984/PovcalNet/NoFillGaps/FDistro14900.RData"
#[1] "Current number of fetched PLs98. Normally this must be 100."

DistroRange <- paste0(readr::parse_number(TheFiles[1]),'-',readr::parse_number(TheFiles[length(TheFiles)]))
save(list = 'MasterDistro',file = paste0('/media/michalis/1984/PovcalNet/NoFillGaps/MasterData/MasterDistro',DistroRange,'.RData'))
save(list = 'FaultyEntries',file = paste0('/media/michalis/1984/PovcalNet/NoFillGaps/MasterData/FaultyEntries',DistroRange,'.RData'))

table(FaultyEntries$Comments)
# PL not identical to the one requested 
# 149985 
length(table(FaultyEntries$RequestedLine))
# [1] 9408

# PCN returns 2056 unique HHS, and I have a PL vector with length 15162
nrow(HHS)*length(IdealPLs)
# 31173072
nrow(FaultyEntries)+nrow(MasterDistro)
# 31152512
nrow(HHS)*length(IdealPLs) - (nrow(FaultyEntries)+nrow(MasterDistro))
# 20560
nrow(HHS)*length(IdealPLs) ==
  nrow(FaultyEntries)+nrow(MasterDistro) + 10*nrow(HHS) # 10 are the missing RequestedLines
# some of them in a single DistroXXXXX.RData file;
# so all good, I just need to fetch what is missing and also bring in the 
# correct entries from the second take of all HHS w/o interpolations
# that correspond to the FaultyEntries from the first take

##### Take 2 Fetch All HHS WITHOUT interpolations ####

library(povcalnetR)
library(doParallel)

# my own take for Ideal PLs:
# IdealPLs <- c(seq(0.001,5,0.001),seq(5.01,45,0.01),seq(45.1,155,0.1))
# expanding it according to OWID_PLs, and according to the findings from 
# the limits of PCN script

IdealPLs <- c(seq(0.001,5,0.001),seq(5.01,60,0.01),seq(60.1,150,0.1),
              seq(150.5,1400,0.5), seq(1405,3000,5), seq(3010,10000,10),
              seq(11000,35000,100),99999)

for (i in c(seq(14200,length(IdealPLs)-1,100),length(IdealPLs))){
  no_cores <- 10
  cl <- makeCluster(no_cores, type="FORK")
  registerDoParallel(cl)
  if (i>15100){
    low_i <- i-61
  } else {
    low_i <- i-99
  }
  Distro <- foreach(jjj=IdealPLs[c(low_i:i)], 
                    #.combine='rbind', 
                    .errorhandling = "pass") %dopar% { 
                      
                      ttt <- 8
                      while (ttt>0){
                        Temp <- povcalnet(
                          country = "all",
                          povline = jjj,
                          year = "all",
                          aggregate = FALSE,
                          fill_gaps = F,
                          coverage = "all",
                          ppp = NULL,
                          url = "http://iresearch.worldbank.org",
                          format = "csv"
                        )
                        
                        WrongEntries <- which(!trimws(format(Temp$povertyline,nsmall = 3))==
                                                trimws(format(jjj, nsmall = 3)))
                        
                        if (length(WrongEntries)>0){
                          ttt <- ttt - 1
                        } else {
                          ttt <- 0
                        }
                      }
                      
                      # I added this extra column because in several instances
                      # the poverty line returned from a particular country
                      # is much different from the poverty line requested
                      # e.g. when asking PL of 1.009 I got a 0.2264779
                      # PL for Burundi in 1981
                      # in the same df I got year 19892Y and datayear 0.0163
                      # for Belarus see 
                      # "/media/michalis/1984/PovcalNet/Examples/Distro1100.RData" oh I just deleted it...
                      Temp$RequestedLine <- jjj
                      return(Temp)
                    }
  stopCluster(cl)
  registerDoSEQ()
  # next time it must be width = 5 because it goes up to ~16000 and it does not 
  # sort properly in R:
  save(list = 'Distro',file = paste0('/media/michalis/1984/PovcalNet/NoFillGaps2/Distro',formatC(i,width = 5, format = "d", flag = "0"),'.RData'))
  print(paste0('Saved file... ',paste0('/media/michalis/1984/PovcalNet/NoFillGaps2/Distro',formatC(i,width = 5, format = "d", flag = "0"),'.RData')))
  rm(Distro)
}

###### Integrity Check and Combine saved data ####
# do I need the integrity check on take 2>???

# let's get the data from World Bank's PovcalNet API:
PCN <- povcalnet_info()
# PCN df is required to request all countries' info from PovcalNet:
HHS <- povcalnet(country = PCN$country_code)
TempDistro <- povcalnetR::povcalnet_cl('USA',1,2010)
TempDistro$RequestedLine <- as.numeric(NA)
MasterDistro <- subset(TempDistro,TempDistro$countrycode=='2398y9wfhehfsdih') # just maintain 
TempMasterDistro <- subset(TempDistro,TempDistro$countrycode=='2398y9wfhehfsdih') # just maintain 
# the data structure
FaultyEntries <- subset(TempDistro,TempDistro$countrycode=='2398y9wfhehfsdih') # just maintain 
# the data structure and add a comment column
FaultyEntries$Comments <- as.character(NA)
SavedDistrosFolder <- '/media/michalis/1984/PovcalNet/NoFillGaps2'
TheFiles <- list.files(SavedDistrosFolder,pattern = 'Distro')
#TheFiles <- TheFiles[c(34:42,44:53)]
TheWrongList <- rep(as.numeric(NA),length(IdealPLs))
names(TheWrongList) <- trimws(format(IdealPLs, nsmall = 3))

options(warn=2) # turn warnings to errors, for better debugging
tictoc::tic()
for (i in c(1:length(TheFiles))){
  #for (i in c(1)){
  # Load the saved data from the disk
  CurrentFile <- paste0(SavedDistrosFolder, '/',TheFiles[i])
  load(CurrentFile)
  print(CurrentFile)
  
  # First check: all list elements must have a fixed length of 32
  # equal to the number of columns returned by the PovcalNet API (31)
  # plus one extra column I add for control ("RequestedLine")
  # that stores the PL requested to the API.
  # Elements not complying are removed, and at the end of this process
  # we will have a reporting variable with all the PL values that
  # need to be requested again from the API
  
  if (!all(sapply(Distro, length)==32)){
    while (!all(sapply(Distro, length)==32)){
      # remove those that did not:
      Distro[[which(!(sapply(Distro, length)==32))[1]]] <- NULL
    }
    print(paste0('Current number of fetched PLs', length(Distro),". Normally this must be 100."))
  } else {
    print('No entries with less than 32 columns to remove...')
  }
  
  # Second check: all entries from a particular list element (so within each list
  # element) must have Distro$RequestedLine == Distro$povertyline
  # those that do not are kept in a separate dataframe
  # plus other integrity checks in the loop below:
  
  for (j in c(1:length(Distro))){
    
    Temp <- Distro[[j]]
    NewFaultyEntries <- subset(FaultyEntries,FaultyEntries$countrycode=='498heo98h')
    
    # Rule 0: no line with all NA, and no line with 
    # countrycode == "CountryCode"
    # and no line with countryname=="DELETE"
    Temp <- subset(Temp,!Temp$countrycode=="CountryCode")
    Temp <- subset(Temp,!Temp$countryname=="DELETE")
    
    # Rule 0.5: all PLs must be identical to the one requested
    WrongEntries <- which(!trimws(format(Temp$povertyline,nsmall = 3))==
                            trimws(format(Temp$RequestedLine, nsmall = 3)))
    NonIdenticalLines <- length(WrongEntries)
    
    FaultyTemp <- Temp[WrongEntries,]
    FaultyTemp$Comments <- 'PL not identical to the one requested'
    Temp <- suppressMessages(dplyr::anti_join(x = Temp, y = FaultyTemp))
    NewFaultyEntries <- rbind(NewFaultyEntries,FaultyTemp)
    
    # Rule 1: all PPPs from one ISO3 must be the same
    # and matching the value from HHS
    for (k in sort(unique(Temp$countrycode))){
      WrongEntries <- which(!Temp$ppp[which(Temp$countrycode==k)]==unique(HHS$ppp[which(HHS$countrycode==k)]))
      if (length(WrongEntries)>0){
        FaultyTemp <- Temp[which(Temp$countrycode==k)[WrongEntries],]
        # remove that entry from the Temp dataframe
        Temp <- suppressMessages(dplyr::anti_join(x = Temp, y = FaultyTemp))
        FaultyTemp$Comments <- 'Wrong PPP value'
        NewFaultyEntries <- rbind(NewFaultyEntries,FaultyTemp)
        rm(FaultyTemp)
      }
      rm(WrongEntries)
    }
    
    # Rule 2: columns "year" "datayear" and from isinterpolated until 
    # "decile10" must be numeric or convertible to numeric without warnings
    # define which columns must be numeric:
    NumericColumns <- c("year","datayear", names(Temp)[c(8:31)])
    # get the columns that actually are numeric:
    nums <- unlist(lapply(Temp, is.numeric)) 
    # and extract those that are not, although they should:
    WronglyNonNumericColumns <- NumericColumns[which(!NumericColumns %in% names(Temp)[nums])]
    # across those find the non-numeric entries:
    for (wrongcols in c(WronglyNonNumericColumns)){
      WrongEntries <- suppressWarnings(which(is.na(as.numeric(unlist(Temp[,wrongcols])))))
      NA_entries <- which(is.na((unlist(Temp[,wrongcols]))))
      WrongEntries <- WrongEntries[which(!WrongEntries %in% NA_entries)]
      if (length(WrongEntries)>0){
        FaultyTemp <- Temp[WrongEntries,]
        # remove that entry from the Temp dataframe
        Temp <- suppressMessages(dplyr::anti_join(x = Temp, y = FaultyTemp))
        FaultyTemp$Comments <- paste0('Non-numeric value in column ', wrongcols)
        NewFaultyEntries <- rbind(NewFaultyEntries,FaultyTemp)
        rm(FaultyTemp)
      }
      rm(WrongEntries)
    }
    
    # Rule 3: in non-interpolated entries "year", "datayear" must be identical 
    # with their corresponding HHS entry
    #WrongEntries <- which(!(Temp$coveragetype %in% HHS$coveragetype))
    #if (length(WrongEntries)>0){
    #  stop('build the code for Rule 3')
    #}
    #rm(WrongEntries)
    
    # Rule 4: interpolated values must be between the benchmark values used 
    # in the interpolation
    #WrongEntries <- which(!(Temp$coveragetype %in% HHS$coveragetype))
    #if (length(WrongEntries)>0){
    #  stop('build the code for Rule 4')
    #}
    #rm(WrongEntries)
    
    # Rule 5: coverage type must be from the range included in HHS
    WrongEntries <- which(!(Temp$coveragetype %in% HHS$coveragetype))
    if (length(WrongEntries)>0){
      stop('build the code for Rule 5')
    }
    rm(WrongEntries)
    
    # Rule 6: apply the allowed values limits to the data using
    # https://rdrr.io/cran/userfriendlyscience/man/checkDataIntegrity.html
    # to be developed...
    
    # keeping a log over the distros with different PLs than requested:
    TheWrongList[which(names(TheWrongList)==
                         as.character(unique(trimws(format(NewFaultyEntries$RequestedLine, 
                                                           nsmall = 3)))))] <- NonIdenticalLines
    
    rm(NonIdenticalLines)
    FaultyEntries <- rbind(FaultyEntries,NewFaultyEntries)
    rm(NewFaultyEntries)
    
    TempMasterDistro <- rbind(TempMasterDistro,Temp)
    rm(Temp)
  }
  MasterDistro <- rbind(MasterDistro,TempMasterDistro)
  TempMasterDistro <- subset(TempDistro,TempDistro$countrycode=='2398y9wfhehfsdih') 
  rm(Distro)
  print('-------------------------------------')
}
options(warn=0) # restore to default from warn=2
tictoc::toc()

#[1] "/media/michalis/1984/PovcalNet/NoFillGaps2/Distro6400.RData"
#[1] "Current number of fetched PLs99. Normally this must be 100."
#[1] "/media/michalis/1984/PovcalNet/NoFillGaps2/Distro7000.RData"
#[1] "Current number of fetched PLs99. Normally this must be 100."
#[1] "/media/michalis/1984/PovcalNet/NoFillGaps2/Distro8200.RData"
#[1] "Current number of fetched PLs99. Normally this must be 100."
#[1] "/media/michalis/1984/PovcalNet/NoFillGaps2/Distro9000.RData"
#[1] "Current number of fetched PLs99. Normally this must be 100."
#[1] "/media/michalis/1984/PovcalNet/NoFillGaps2/Distro9200.RData"
#[1] "Current number of fetched PLs99. Normally this must be 100."
#[1] "/media/michalis/1984/PovcalNet/NoFillGaps2/FDistro10000.RData"
#[1] "Current number of fetched PLs98. Normally this must be 100."
#[1] "/media/michalis/1984/PovcalNet/NoFillGaps2/FDistro10900.RData"
#[1] "Current number of fetched PLs97. Normally this must be 100."
#[1] "/media/michalis/1984/PovcalNet/NoFillGaps2/FDistro11600.RData"
#[1] "Current number of fetched PLs99. Normally this must be 100."
#[1] "/media/michalis/1984/PovcalNet/NoFillGaps2/FDistro11800.RData"
#[1] "Current number of fetched PLs99. Normally this must be 100."
#[1] "/media/michalis/1984/PovcalNet/NoFillGaps2/FDistro14100.RData"
#[1] "Current number of fetched PLs99. Normally this must be 100."

DistroRange <- paste0(readr::parse_number(TheFiles[1]),'-',readr::parse_number(TheFiles[length(TheFiles)]))
save(list = 'MasterDistro',file = paste0('/media/michalis/1984/PovcalNet/NoFillGaps/MasterData/MasterDistroB',DistroRange,'.RData'))
save(list = 'FaultyEntries',file = paste0('/media/michalis/1984/PovcalNet/NoFillGaps/MasterData/FaultyEntriesB',DistroRange,'.RData'))

table(FaultyEntries$Comments)
# PL not identical to the one requested 
# 13639 
length(table(FaultyEntries$RequestedLine))
# [1] 1213

###### Merge Take 2 with Take 1 on FaultyEntries ####
# merge on faulty entries and missing years the two takes on HHS without interpolations
# to minimize the faulty entries and missing years to be reFetched

# PCN returns 2056 unique HHS, and I have a PL vector with length 15162
nrow(HHS)*length(IdealPLs)
# 31173072
nrow(FaultyEntries)+nrow(MasterDistro)
# 31146344
nrow(HHS)*length(IdealPLs) - (nrow(FaultyEntries)+nrow(MasterDistro))
# 26728
nrow(HHS)*length(IdealPLs) ==
nrow(FaultyEntries)+nrow(MasterDistro) + 13*nrow(HHS) # 13 are the missing RequestedLines
# some of them in a single DistroXXXXX.RData file;
# so all good, I just need to fetch what is missing and also bring in the 
# correct entries from the second take of all HHS w/o interpolations
# that correspond to the FaultyEntries from the first take

# OK but the above were just  test for the consistency of take 2, I need to load
# the FaultyEntries and MasterDistro from Take 1:

load("/media/michalis/1984/PovcalNet/NoFillGaps/MasterData/FaultyEntries100-15162.RData")
load("/media/michalis/1984/PovcalNet/NoFillGaps/MasterData/MasterDistro100-15162.RData")

# this contains the Faulty lines of which a proper entry is found:
CorrectedLines <- subset(FaultyEntries,FaultyEntries$countrycode=='sdfkjsdkjfshdk')
# this contains the Faulty lines of which a proper entry is NOT found:
NotFound <- subset(FaultyEntries,FaultyEntries$countrycode=='sdfkjsdkjfshdk')
# this contains the new data lines that are found (to be used instead of the faulty lines):
NewData <- CorrectedLines # empty template to be populated in the loop
NewData$Comments <- NULL # to be of the same width as the MasterDistro dataframe
AllNewLinesTemplate <- NewData # reference empty template
Take2HHSMissingPLs <- c() # which PLs are missing from the Take2 PCN HHS fetch

total <- length(unique(FaultyEntries$RequestedLine))
pb <- tkProgressBar(title = "progress bar", min = 0,max = total, width = 300)

for (i in c(1:total)){
  
  setTkProgressBar(pb, i, label=paste( round(i/total*100, 3),"% done"))
  
  NewNotFound <- subset(FaultyEntries,FaultyEntries$countrycode=='sdfkjsdkjfshdk')
  
  FaultyLine <- as.numeric(sort(unique(FaultyEntries$RequestedLine))[i])
  FetchDistroNum <- ceiling(which(IdealPLs==FaultyLine)/100)*100
  if (FetchDistroNum==15200){
    FetchDistroNum <- length(IdealPLs)
  }
  if (FetchDistroNum<10000){
    load(paste0('/media/michalis/1984/PovcalNet/NoFillGaps2/Distro',formatC(FetchDistroNum,width = 4, format = "d", flag = "0"),'.RData'))
  } else {
    load(paste0('/media/michalis/1984/PovcalNet/NoFillGaps2/FDistro',formatC(FetchDistroNum,width = 5, format = "d", flag = "0"),'.RData'))
  }
  if (which(IdealPLs==FaultyLine) %% 100>0){
    Take2HHS <- Distro[[which(IdealPLs==FaultyLine) %% 100]]
  } else {
    Take2HHS <- Distro[[100]]
  }
  
  if (is.null(nrow(Take2HHS))){
    Take2HHSMissingPLs <- c(Take2HHSMissingPLs,FaultyLine)
  } else {
  
    # locate the FaultyLine in the new HHS set:
    TempFaultyEntries <- subset(FaultyEntries,FaultyEntries$RequestedLine==FaultyLine)
    AllNewLines <- AllNewLinesTemplate
    
    for (j in 1:nrow(TempFaultyEntries)){
      
      NewLine <- subset(Take2HHS,Take2HHS$countrycode==TempFaultyEntries$countrycode[j] &
                          Take2HHS$year==TempFaultyEntries$year[j] &
                          Take2HHS$datayear==TempFaultyEntries$datayear[j] &
                          Take2HHS$coveragetype==TempFaultyEntries$coveragetype[j] &
                          Take2HHS$datatype==TempFaultyEntries$datatype[j] &
                          round(Take2HHS$povertyline,3)==round(TempFaultyEntries$RequestedLine[j],3))
      
      AllNewLines <- rbind(AllNewLines,NewLine)
      if (nrow(NewLine)==0){
        NewNotFound <- rbind(NewNotFound,TempFaultyEntries[j,])
      }
      rm(NewLine)
    }
    
    NotFound <- rbind(NotFound,NewNotFound)
    
    if (nrow(AllNewLines)+nrow(NewNotFound)==nrow(TempFaultyEntries)){
      if (all(round(AllNewLines$povertyline,3)==round(FaultyLine,3))){
        CorrectedLines <- rbind(CorrectedLines,TempFaultyEntries)
        NewData <- rbind(NewData,AllNewLines)
      } else {
        stop('!all(AllNewLines$povertyline)==FaultyLine')
      }
    } else {
      stop("!nrow(AllNewLines)+nrow(NewNotFound)==nrow(TempFaultyEntries)")
    }
  }
}
close(pb)
rm(Distro,pb,i,j,no_cores,total)

# save.image("/media/michalis/1984/PovcalNetTemp2.RData")
# load("/media/michalis/1984/PovcalNetTemp2.RData")
#length(which(table(MasterDistro$RequestedLine)<nrow(HHS)))

# check if there are more than we would expect:
ttt <- table(MasterDistro$RequestedLine)
ttt[ttt>nrow(HHS)]
# integer(0)

###### Merge New and MasterDistro ####
MasterDistro <- rbind(MasterDistro,NewData)
ttt[ttt>nrow(HHS)]
# integer(0)
rm(NewData)
WrongEntries <- which(!trimws(format(MasterDistro$povertyline,nsmall = 3))==
                        trimws(format(MasterDistro$RequestedLine, nsmall = 3)))
# this test goes OK but that was expected
UniqueReqPLs <- as.numeric(trimws(sort(unique(MasterDistro$RequestedLine))))
UniqueReqPLs <- as.numeric(format(UniqueReqPLs,nsmall = 3))
MissingPLs <- IdealPLs[which(!(round(IdealPLs,3) %in% round(UniqueReqPLs,3)))]
# So I should be missing 
length(MissingPLs)*nrow(HHS)
# 20560, from the theoretical number of data points:
# PCN returns 2056 unique HHS, and I have a PL vector with length 15162
nrow(HHS)*length(IdealPLs)
# 31173072
nrow(HHS)*length(IdealPLs) ==
  nrow(MasterDistro) + length(MissingPLs)*nrow(HHS) # 10 are the missing RequestedLines
# and 10 are the MissingPLs found; FALSE!
nrow(HHS)*length(IdealPLs) -
  (nrow(MasterDistro) + length(MissingPLs)*nrow(HHS))
# I am missing 376 extra entries, so I will first get the missing PLs and then check
# what is wrong

#rm(AllNewLines,AllNewLinesTemplate,CorrectedLines,FaultyEntries,NewNotFound,
#   NotFound,TempFaultyEntries,Take2HHS)
#rm(WrongEntries,Take2HHSMissingPLs,FetchDistroNum,FaultyLine)
# save.image("/media/michalis/1984/PovcalNetTemp3.RData")
# load("/media/michalis/1984/PovcalNetTemp3.RData")

###### Process the missing PLs ####
# from the above I am still missing the PLs that are entirely missing from the Take 1!
# so I need to fetch them

library(povcalnetR)
library(doParallel)

no_cores <- 2
cl <- makeCluster(no_cores, type="FORK")
registerDoParallel(cl)
Distro <- foreach(jjj=MissingPLs, 
                  #.combine='rbind', 
                  .errorhandling = "pass") %dopar% { 
                    
                    ttt <- 8
                    while (ttt>0){
                      Temp <- povcalnet(
                        country = "all",
                        povline = jjj,
                        year = "all",
                        aggregate = FALSE,
                        fill_gaps = F,
                        coverage = "all",
                        ppp = NULL,
                        url = "http://iresearch.worldbank.org",
                        format = "csv"
                      )
                      
                      WrongEntries <- which(!trimws(format(Temp$povertyline,nsmall = 3))==
                                              trimws(format(jjj, nsmall = 3)))
                      
                      if (length(WrongEntries)>0){
                        ttt <- ttt - 1
                      } else {
                        ttt <- 0
                      }
                    }
                    
                    # I added this extra column because in several instances
                    # the poverty line returned from a particular country
                    # is much different from the poverty line requested
                    # e.g. when asking PL of 1.009 I got a 0.2264779
                    # PL for Burundi in 1981
                    # in the same df I got year 19892Y and datayear 0.0163
                    # for Belarus see 
                    # "/media/michalis/1984/PovcalNet/Examples/Distro1100.RData" oh I just deleted it...
                    Temp$RequestedLine <- jjj
                    return(Temp)
                  }
stopCluster(cl)
registerDoSEQ()
# next time it must be width = 5 because it goes up to ~16000 and it does not 
# sort properly in R:
save(list = 'Distro',file = paste0('/media/michalis/1984/PovcalNet/NoFillGaps3/DistroMissingPLs.RData'))
print(paste0('Saved file... ',paste0('/media/michalis/1984/PovcalNet/NoFillGaps3/DistroMissingPLs.RData')))

###### Integrity Check ####

load('/media/michalis/1984/PovcalNet/NoFillGaps3/DistroMissingPLs.RData')
# let's get the data from World Bank's PovcalNet API:
PCN <- povcalnet_info()
# PCN df is required to request all countries' info from PovcalNet:
HHS <- povcalnet(country = PCN$country_code)
TempDistro <- povcalnetR::povcalnet_cl('USA',1,2010)
TempDistro$RequestedLine <- as.numeric(NA)
TempMasterDistro <- subset(TempDistro,TempDistro$countrycode=='2398y9wfhehfsdih') # just maintain 
# the data structure
FaultyEntries <- subset(TempDistro,TempDistro$countrycode=='2398y9wfhehfsdih') # just maintain 
# the data structure and add a comment column
FaultyEntries$Comments <- as.character(NA)
TheWrongList <- rep(as.numeric(NA),length(MissingPLs))
names(TheWrongList) <- trimws(format(MissingPLs, nsmall = 3))

# check if the new distribution have the right width
if (!all(sapply(Distro, length)==32)){
  while (!all(sapply(Distro, length)==32)){
    # remove those that did not:
    Distro[[which(!(sapply(Distro, length)==32))[1]]] <- NULL
  }
  print(paste0('Current number of fetched PLs', length(Distro),". Normally this must be 100."))
} else {
  print('No entries with less than 32 columns to remove...')
}

# Second check: all entries from a particular list element (so within each list
# element) must have Distro$RequestedLine == Distro$povertyline
# those that do not are kept in a separate dataframe
# plus other integrity checks in the loop below:
# here I also integrate them in a new dataframe ready to be binded with MasterDistro
# I am doing this using TempMasterDistro

for (j in c(1:length(Distro))){
  
  Temp <- Distro[[j]]
  NewFaultyEntries <- subset(FaultyEntries,FaultyEntries$countrycode=='498heo98h')
  
  # Rule 0: no line with all NA, and no line with 
  # countrycode == "CountryCode"
  # and no line with countryname=="DELETE"
  Temp <- subset(Temp,!Temp$countrycode=="CountryCode")
  Temp <- subset(Temp,!Temp$countryname=="DELETE")
  
  # Rule 0.5: all PLs must be identical to the one requested
  WrongEntries <- which(!trimws(format(Temp$povertyline,nsmall = 3))==
                          trimws(format(Temp$RequestedLine, nsmall = 3)))
  NonIdenticalLines <- length(WrongEntries)
  
  FaultyTemp <- Temp[WrongEntries,]
  FaultyTemp$Comments <- 'PL not identical to the one requested'
  Temp <- suppressMessages(dplyr::anti_join(x = Temp, y = FaultyTemp))
  NewFaultyEntries <- rbind(NewFaultyEntries,FaultyTemp)
  
  # Rule 1: all PPPs from one ISO3 must be the same
  # and matching the value from HHS
  for (k in sort(unique(Temp$countrycode))){
    WrongEntries <- which(!Temp$ppp[which(Temp$countrycode==k)]==unique(HHS$ppp[which(HHS$countrycode==k)]))
    if (length(WrongEntries)>0){
      FaultyTemp <- Temp[which(Temp$countrycode==k)[WrongEntries],]
      # remove that entry from the Temp dataframe
      Temp <- suppressMessages(dplyr::anti_join(x = Temp, y = FaultyTemp))
      FaultyTemp$Comments <- 'Wrong PPP value'
      NewFaultyEntries <- rbind(NewFaultyEntries,FaultyTemp)
      rm(FaultyTemp)
    }
    rm(WrongEntries)
  }
  
  # Rule 2: columns "year" "datayear" and from isinterpolated until 
  # "decile10" must be numeric or convertible to numeric without warnings
  # define which columns must be numeric:
  NumericColumns <- c("year","datayear", names(Temp)[c(8:31)])
  # get the columns that actually are numeric:
  nums <- unlist(lapply(Temp, is.numeric)) 
  # and extract those that are not, although they should:
  WronglyNonNumericColumns <- NumericColumns[which(!NumericColumns %in% names(Temp)[nums])]
  # across those find the non-numeric entries:
  for (wrongcols in c(WronglyNonNumericColumns)){
    WrongEntries <- suppressWarnings(which(is.na(as.numeric(unlist(Temp[,wrongcols])))))
    NA_entries <- which(is.na((unlist(Temp[,wrongcols]))))
    WrongEntries <- WrongEntries[which(!WrongEntries %in% NA_entries)]
    if (length(WrongEntries)>0){
      FaultyTemp <- Temp[WrongEntries,]
      # remove that entry from the Temp dataframe
      Temp <- suppressMessages(dplyr::anti_join(x = Temp, y = FaultyTemp))
      FaultyTemp$Comments <- paste0('Non-numeric value in column ', wrongcols)
      NewFaultyEntries <- rbind(NewFaultyEntries,FaultyTemp)
      rm(FaultyTemp)
    }
    rm(WrongEntries)
  }
  
  # Rule 3: in non-interpolated entries "year", "datayear" must be identical 
  # with their corresponding HHS entry
  #WrongEntries <- which(!(Temp$coveragetype %in% HHS$coveragetype))
  #if (length(WrongEntries)>0){
  #  stop('build the code for Rule 3')
  #}
  #rm(WrongEntries)
  
  # Rule 4: interpolated values must be between the benchmark values used 
  # in the interpolation
  #WrongEntries <- which(!(Temp$coveragetype %in% HHS$coveragetype))
  #if (length(WrongEntries)>0){
  #  stop('build the code for Rule 4')
  #}
  #rm(WrongEntries)
  
  # Rule 5: coverage type must be from the range included in HHS
  WrongEntries <- which(!(Temp$coveragetype %in% HHS$coveragetype))
  if (length(WrongEntries)>0){
    stop('build the code for Rule 5')
  }
  rm(WrongEntries)
  
  # Rule 6: apply the allowed values limits to the data using
  # https://rdrr.io/cran/userfriendlyscience/man/checkDataIntegrity.html
  # to be developed...
  
  # keeping a log over the distros with different PLs than requested:
  TheWrongList[which(names(TheWrongList)==
                       as.character(unique(trimws(format(NewFaultyEntries$RequestedLine, 
                                                         nsmall = 3)))))] <- NonIdenticalLines
  
  rm(NonIdenticalLines)
  FaultyEntries <- rbind(FaultyEntries,NewFaultyEntries)
  rm(NewFaultyEntries)
  
  TempMasterDistro <- rbind(TempMasterDistro,Temp)
  rm(Temp)
}

which(table(MasterDistro$RequestedLine)>nrow(HHS))
which(!table(MasterDistro$RequestedLine)==nrow(HHS))
which(table(TempMasterDistro$RequestedLine)>nrow(HHS))

length(MissingPLs)*nrow(HHS)==nrow(TempMasterDistro)
# Bingo! let's just add these to the MasterDistro and we are done!
MasterDistro <- rbind(MasterDistro,TempMasterDistro)
rm(TempMasterDistro)
# check if there are any wrong PLs still:
WrongEntries <- which(!trimws(format(MasterDistro$povertyline,nsmall = 3))==
                        trimws(format(MasterDistro$RequestedLine, nsmall = 3)))
# this test goes OK!
UniqueReqPLs <- as.numeric(trimws(sort(unique(MasterDistro$RequestedLine))))
UniqueReqPLs <- as.numeric(format(UniqueReqPLs,nsmall = 3))
MissingPLs <- IdealPLs[which(!(round(IdealPLs,3) %in% round(UniqueReqPLs,3)))]
# so all lines appear in the data (but not sure yet if they appear for the correct
# number of times, which is nrow(HHS))
# PCN returns 2056 unique HHS, and I have a PL vector with length 15162
nrow(HHS)*length(IdealPLs)
# 31173072
nrow(HHS)*length(IdealPLs) == nrow(MasterDistro)
nrow(HHS)*length(IdealPLs) - nrow(MasterDistro)
# 376
# I am missing 376 entries, now lets see which line is not complete:
ttt <- table(MasterDistro$RequestedLine)
ttt[ttt>nrow(HHS)]
# integer(0)
sum(nrow(HHS)-ttt)
# so I know exactly what is missing by comparing the HHS with each PL from
MissingPLs <- as.numeric(names(ttt[ttt<nrow(HHS)]))
# save.image("/media/michalis/1984/PovcalNetTemp4.RData")
# load("/media/michalis/1984/PovcalNetTemp4.RData")

##### Fetch entries missing from both Takes ####

ttt[ttt<nrow(HHS)]
#3.806  4.438   5.76   5.82   6.08   8.53   9.03  11.35  11.44  11.91  13.07  13.82   17.4  17.48   20.1  22.09  23.03  24.29  24.42  24.79  25.13  25.26  25.68  26.08  26.72   30.1  31.84 
#2055   2055   2055   2040   2055   2054   2055   2055   2055   2055   2053   2055   2050   2052   2055   2055   2054   2055   2055   2052   2055   2055   2055   2055   2055   2054   2055 
#32.04  33.08   36.7  37.29  38.34  38.52  38.63  39.03  39.71  40.02  41.06  41.15  42.01  42.02  44.57   45.1  45.66  45.68  45.83  46.36  46.58  46.59  47.24  47.25  48.09  48.71   48.8 
#2055   2055   2055   2055   2055   2055   2054   2054   2055   2053   2051   2052   2054   2055   1907   2055   2053   2055   2055   2053   2050   2055   2055   2055   2055   2055   2055 
#49.38  49.41  49.58  49.63  50.69  51.85  54.46  56.07  56.73  57.35  59.07   60.3   80.7   87.6   95.2  111.4  112.6  125.6  138.8  140.2    201  204.5    211    262    281  315.5    390 
#2052   2055   2054   2055   2055   2055   2055   2055   2055   2054   2054   2053   2055   2055   2055   2055   2055   2055   2055   2055   2054   2055   2031   2055   2055   2050   2055 
#401  404.5    489    504  531.5  552.5  640.5  702.5    716  717.5    760  777.5    781  800.5  801.5  818.5    820  834.5    937  955.5    975  977.5   1001   1002   1006 1026.5   1032 
#2055   2054   2054   2055   2055   2055   2054   2052   2055   2055   2055   2055   2055   2053   2055   2055   2055   2054   2054   2055   2054   2055   2054   2055   2055   2054   2054 
#1039.5 1100.5   1202 1202.5 1208.5   1319   1344   6160 
#2053   2054   2055   2054   2054   2054   2055   2053 

sort(ttt[ttt<nrow(HHS)])
#44.57    211   5.82   17.4  46.58  315.5  41.06  17.48  24.79  41.15  49.38  702.5  13.07  40.02  45.66  46.36   60.3  800.5 1039.5   6160   8.53  23.03   30.1  38.63  39.03  42.01  49.58 
#1907   2031   2040   2050   2050   2050   2051   2052   2052   2052   2052   2052   2053   2053   2053   2053   2053   2053   2053   2053   2054   2054   2054   2054   2054   2054   2054 
#57.35  59.07    201  404.5    489  640.5  834.5    937    975   1001 1026.5   1032 1100.5 1202.5 1208.5   1319  3.806  4.438   5.76   6.08   9.03  11.35  11.44  11.91  13.82   20.1  22.09 
#2054   2054   2054   2054   2054   2054   2054   2054   2054   2054   2054   2054   2054   2054   2054   2054   2055   2055   2055   2055   2055   2055   2055   2055   2055   2055   2055 
#24.29  24.42  25.13  25.26  25.68  26.08  26.72  31.84  32.04  33.08   36.7  37.29  38.34  38.52  39.71  42.02   45.1  45.68  45.83  46.59  47.24  47.25  48.09  48.71   48.8  49.41  49.63 
#2055   2055   2055   2055   2055   2055   2055   2055   2055   2055   2055   2055   2055   2055   2055   2055   2055   2055   2055   2055   2055   2055   2055   2055   2055   2055   2055 
#50.69  51.85  54.46  56.07  56.73   80.7   87.6   95.2  111.4  112.6  125.6  138.8  140.2  204.5    262    281    390    401    504  531.5  552.5    716  717.5    760  777.5    781  801.5 
#2055   2055   2055   2055   2055   2055   2055   2055   2055   2055   2055   2055   2055   2055   2055   2055   2055   2055   2055   2055   2055   2055   2055   2055   2055   2055   2055 
#818.5    820  955.5  977.5   1002   1006   1202   1344 
#2055   2055   2055   2055   2055   2055   2055   2055 

HHS$ISO3DataYearCovType <- paste0(HHS$countrycode,":",HHS$year,":",HHS$datayear,
                                  ":",HHS$coveragetype,":",ifelse(HHS$datatype=="consumption",'c','i'))
rm(MissingEntries)
for (i in MissingPLs){
  print(paste0('-----',i,'------'))
  tempdf <- subset(MasterDistro,round(MasterDistro$RequestedLine,3)==round(i,3))
  tempdf$ISO3DataYearCovType <- paste0(tempdf$countrycode,":",tempdf$year,":",
                                       tempdf$datayear,":",tempdf$coveragetype,":",
                                       ifelse(tempdf$datatype=="consumption",'c','i'))
  tempID <- HHS$ISO3DataYearCovType[which(!HHS$ISO3DataYearCovType %in% tempdf$ISO3DataYearCovType)]
  print(length(tempID))
  if (!exists('MissingEntries')){
    MissingEntries <- data.frame(ID=tempID,PL=i,stringsAsFactors = F)
    print(length(tempID))
  } else {
    print(length(tempID)+nrow(MissingEntries))
    MissingEntries <- rbind(MissingEntries,data.frame(ID=tempID,PL=i,stringsAsFactors = F))
  }
  print(nrow(MissingEntries))
  rm(tempdf)
}

nrow(MissingEntries)==nrow(HHS)*length(IdealPLs) - nrow(MasterDistro)
# perfect!

# let's fetch them from PCN
no_cores <- 2
cl <- makeCluster(no_cores, type="FORK")
registerDoParallel(cl)
Distro <- foreach(jjj=c(1:nrow(MissingEntries)), 
                  #.combine='rbind', 
                  .errorhandling = "pass") %dopar% { 
                    
                    countrycode1 <- strsplit(MissingEntries$ID[jjj],":",fixed = T)[[1]][1]
                    year1 <- as.numeric(strsplit(MissingEntries$ID[jjj],":",fixed = T)[[1]][2])
                    datayear1 <- as.numeric(strsplit(MissingEntries$ID[jjj],":",fixed = T)[[1]][3])
                    coveragetype1 <- strsplit(MissingEntries$ID[jjj],":",fixed = T)[[1]][4]
                    datatype1 <- strsplit(MissingEntries$ID[jjj],":",fixed = T)[[1]][5]
                    datatype1 <- ifelse(datatype1=="c","consumption","income")
                    
                    ttt <- 20
                    while (ttt>0){
                      Temp <- povcalnet(
                        country = countrycode1,
                        povline = MissingEntries$PL[jjj],
                        year = year1,
                        aggregate = FALSE,
                        fill_gaps = T,
                        coverage = "all",
                        ppp = NULL,
                        url = "http://iresearch.worldbank.org",
                        format = "csv"
                      )
                      
                      if (!all(is.na(Temp$datayear))){
                        Temp <- subset(Temp, round(Temp$datayear,2)==round(datayear1,2))
                      }
                      
                      Temp <- subset(Temp, Temp$coveragetype==coveragetype1)
                      
                      WrongEntries <- which(!trimws(format(Temp$povertyline,nsmall = 3))==
                                              trimws(format(MissingEntries$PL[jjj], nsmall = 3)))
                      
                      if (length(WrongEntries)>0){
                        ttt <- ttt - 1
                      } else {
                        ttt <- 0
                      }
                    }
                    
                    # I added this extra column because in several instances
                    # the poverty line returned from a particular country
                    # is much different from the poverty line requested
                    # e.g. when asking PL of 1.009 I got a 0.2264779
                    # PL for Burundi in 1981
                    # in the same df I got year 19892Y and datayear 0.0163
                    # for Belarus see 
                    # "/media/michalis/1984/PovcalNet/Examples/Distro1100.RData" oh I just deleted it...
                    Temp$RequestedLine <- MissingEntries$PL[jjj]
                    return(Temp)
                  }
stopCluster(cl)
registerDoSEQ()

# next time it must be width = 5 because it goes up to ~16000 and it does not 
# sort properly in R:
save(list = 'Distro',file = paste0('/media/michalis/1984/PovcalNet/NoFillGaps3/DistroLastMissingPLs.RData'))
print(paste0('Saved file... ',paste0('/media/michalis/1984/PovcalNet/NoFillGaps3/DistroLastMissingPLs.RData')))

# check that those are the entries I actually wanted!
load('/media/michalis/1984/PovcalNet/NoFillGaps3/DistroLastMissingPLs.RData')
# lets see now if we have enough new entries:
length(Distro)==sum(nrow(HHS)-ttt)
# Bingo! let's just add these to the MasterDistro and we are done!

# let's get the data from World Bank's PovcalNet API:
TempDistro <- povcalnetR::povcalnet_cl('USA',1,2010)
TempDistro$RequestedLine <- as.numeric(NA)
TempMasterDistro <- subset(TempDistro,TempDistro$countrycode=='2398y9wfhehfsdih') # just maintain 
# the data structure
FaultyEntries <- subset(TempDistro,TempDistro$countrycode=='2398y9wfhehfsdih') # just maintain 
# the data structure and add a comment column
FaultyEntries$Comments <- as.character(NA)
TheWrongList <- rep(as.numeric(NA),length(MissingPLs))
names(TheWrongList) <- trimws(format(MissingPLs, nsmall = 3))

# check if the new distribution have the right width
if (!all(sapply(Distro, length)==32)){
  while (!all(sapply(Distro, length)==32)){
    # remove those that did not:
    Distro[[which(!(sapply(Distro, length)==32))[1]]] <- NULL
  }
  print(paste0('Current number of fetched PLs', length(Distro),". Normally this must be 100."))
} else {
  print('No entries with less than 32 columns to remove...')
}

# Second check: all entries from a particular list element (so within each list
# element) must have Distro$RequestedLine == Distro$povertyline
# those that do not are kept in a separate dataframe
# plus other integrity checks in the loop below:
# here I also integrate them in a new dataframe ready to be binded with MasterDistro
# I am doing this using TempMasterDistro

for (j in c(1:length(Distro))){
  
  Temp <- Distro[[j]]
  NewFaultyEntries <- subset(FaultyEntries,FaultyEntries$countrycode=='498heo98h')
  
  # Rule 0: no line with all NA, and no line with 
  # countrycode == "CountryCode"
  # and no line with countryname=="DELETE"
  Temp <- subset(Temp,!Temp$countrycode=="CountryCode")
  Temp <- subset(Temp,!Temp$countryname=="DELETE")
  
  # Rule 0.5: all PLs must be identical to the one requested
  WrongEntries <- which(!trimws(format(Temp$povertyline,nsmall = 3))==
                          trimws(format(Temp$RequestedLine, nsmall = 3)))
  NonIdenticalLines <- length(WrongEntries)
  
  FaultyTemp <- Temp[WrongEntries,]
  FaultyTemp$Comments <- 'PL not identical to the one requested'
  Temp <- suppressMessages(dplyr::anti_join(x = Temp, y = FaultyTemp))
  NewFaultyEntries <- rbind(NewFaultyEntries,FaultyTemp)
  
  # Rule 1: all PPPs from one ISO3 must be the same
  # and matching the value from HHS
  for (k in sort(unique(Temp$countrycode))){
    WrongEntries <- which(!Temp$ppp[which(Temp$countrycode==k)]==unique(HHS$ppp[which(HHS$countrycode==k)]))
    if (length(WrongEntries)>0){
      FaultyTemp <- Temp[which(Temp$countrycode==k)[WrongEntries],]
      # remove that entry from the Temp dataframe
      Temp <- suppressMessages(dplyr::anti_join(x = Temp, y = FaultyTemp))
      FaultyTemp$Comments <- 'Wrong PPP value'
      NewFaultyEntries <- rbind(NewFaultyEntries,FaultyTemp)
      rm(FaultyTemp)
    }
    rm(WrongEntries)
  }
  
  # Rule 2: columns "year" "datayear" and from isinterpolated until 
  # "decile10" must be numeric or convertible to numeric without warnings
  # define which columns must be numeric:
  NumericColumns <- c("year","datayear", names(Temp)[c(8:31)])
  # get the columns that actually are numeric:
  nums <- unlist(lapply(Temp, is.numeric)) 
  # and extract those that are not, although they should:
  WronglyNonNumericColumns <- NumericColumns[which(!NumericColumns %in% names(Temp)[nums])]
  # across those find the non-numeric entries:
  for (wrongcols in c(WronglyNonNumericColumns)){
    WrongEntries <- suppressWarnings(which(is.na(as.numeric(unlist(Temp[,wrongcols])))))
    NA_entries <- which(is.na((unlist(Temp[,wrongcols]))))
    WrongEntries <- WrongEntries[which(!WrongEntries %in% NA_entries)]
    if (length(WrongEntries)>0){
      FaultyTemp <- Temp[WrongEntries,]
      # remove that entry from the Temp dataframe
      Temp <- suppressMessages(dplyr::anti_join(x = Temp, y = FaultyTemp))
      FaultyTemp$Comments <- paste0('Non-numeric value in column ', wrongcols)
      NewFaultyEntries <- rbind(NewFaultyEntries,FaultyTemp)
      rm(FaultyTemp)
    }
    rm(WrongEntries)
  }
  
  # Rule 3: in non-interpolated entries "year", "datayear" must be identical 
  # with their corresponding HHS entry
  #WrongEntries <- which(!(Temp$coveragetype %in% HHS$coveragetype))
  #if (length(WrongEntries)>0){
  #  stop('build the code for Rule 3')
  #}
  #rm(WrongEntries)
  
  # Rule 4: interpolated values must be between the benchmark values used 
  # in the interpolation
  #WrongEntries <- which(!(Temp$coveragetype %in% HHS$coveragetype))
  #if (length(WrongEntries)>0){
  #  stop('build the code for Rule 4')
  #}
  #rm(WrongEntries)
  
  # Rule 5: coverage type must be from the range included in HHS
  WrongEntries <- which(!(Temp$coveragetype %in% HHS$coveragetype))
  if (length(WrongEntries)>0){
    stop('build the code for Rule 5')
  }
  rm(WrongEntries)
  
  # Rule 6: apply the allowed values limits to the data using
  # https://rdrr.io/cran/userfriendlyscience/man/checkDataIntegrity.html
  # to be developed...
  
  # keeping a log over the distros with different PLs than requested:
  TheWrongList[which(names(TheWrongList)==
                       as.character(unique(trimws(format(NewFaultyEntries$RequestedLine, 
                                                         nsmall = 3)))))] <- NonIdenticalLines
  
  rm(NonIdenticalLines)
  FaultyEntries <- rbind(FaultyEntries,NewFaultyEntries)
  rm(NewFaultyEntries)
  
  # only keep the entries that were identified in MissingEntries:
  if (nrow(Temp)>1){
     
    jjj <- j
    countrycode1 <- strsplit(MissingEntries$ID[jjj],":",fixed = T)[[1]][1]
    year1 <- as.numeric(strsplit(MissingEntries$ID[jjj],":",fixed = T)[[1]][2])
    datayear1 <- as.numeric(strsplit(MissingEntries$ID[jjj],":",fixed = T)[[1]][3])
    coveragetype1 <- strsplit(MissingEntries$ID[jjj],":",fixed = T)[[1]][4]
    datatype1 <- strsplit(MissingEntries$ID[jjj],":",fixed = T)[[1]][5]
    datatype1 <- ifelse(datatype1=="c","consumption","income")
    
    Temp <- subset(Temp,Temp$countrycode==countrycode1 &
                   Temp$year==year1 &
                   Temp$datayear==datayear1 &
                   Temp$coveragetype==coveragetype1 &
                   Temp$datatype==datatype1)
  
  }
  
  TempMasterDistro <- rbind(TempMasterDistro,Temp)
  rm(Temp)
}

# test before merge:
ttt <- table(MasterDistro$RequestedLine)
ttt[ttt>nrow(HHS)]
#named integer(0)

MasterDistro <- rbind(MasterDistro,TempMasterDistro)
rm(TempMasterDistro)

ttt <- table(MasterDistro$RequestedLine)
ttt[ttt>nrow(HHS)]
#named integer(0)
sort(ttt[ttt<nrow(HHS)])
# 44.57 
# 2055
sum(nrow(HHS)-ttt)
# 1

# check if there are any wrong PLs still:
WrongEntries <- which(!trimws(format(MasterDistro$povertyline,nsmall = 3))==
                        trimws(format(MasterDistro$RequestedLine, nsmall = 3)))
# this test goes OK!
UniqueReqPLs <- as.numeric(trimws(sort(unique(MasterDistro$RequestedLine))))
UniqueReqPLs <- as.numeric(format(UniqueReqPLs,nsmall = 3))
MissingPLs <- IdealPLs[which(!(round(IdealPLs,3) %in% round(UniqueReqPLs,3)))]
# so all lines appear in the data (but not sure yet if they appear for the correct
# number of times, which is nrow(HHS))
# PCN returns 2056 unique HHS, and I have a PL vector with length 15162
nrow(HHS)*length(IdealPLs)
# 31173072
nrow(HHS)*length(IdealPLs) == nrow(MasterDistro)
nrow(HHS)*length(IdealPLs) - nrow(MasterDistro)
# 1
# I am missing at 1 entry, now lets see which line is not complete:
ttt <- table(MasterDistro$RequestedLine)
ttt[ttt>nrow(HHS)]
#named integer(0)
sum(ttt[ttt>nrow(HHS)]-nrow(HHS))
# 0
sum(nrow(HHS)-ttt)
# 1
# so I know exactly what is missing by comparing the HHS with each PL from
MissingPLs <- as.numeric(names(ttt[ttt<nrow(HHS)]))

##### Fetch Again entries missing from both Takes ####

rm(MissingEntries)
for (i in MissingPLs){
  print(paste0('-----',i,'------'))
  tempdf <- subset(MasterDistro,round(MasterDistro$RequestedLine,3)==round(i,3))
  tempdf$ISO3DataYearCovType <- paste0(tempdf$countrycode,":",tempdf$year,":",
                                       tempdf$datayear,":",tempdf$coveragetype,":",
                                       ifelse(tempdf$datatype=="consumption",'c','i'))
  tempID <- HHS$ISO3DataYearCovType[which(!HHS$ISO3DataYearCovType %in% tempdf$ISO3DataYearCovType)]
  print(length(tempID))
  if (!exists('MissingEntries')){
    MissingEntries <- data.frame(ID=tempID,PL=i,stringsAsFactors = F)
    print(length(tempID))
  } else {
    print(length(tempID)+nrow(MissingEntries))
    MissingEntries <- rbind(MissingEntries,data.frame(ID=tempID,PL=i,stringsAsFactors = F))
  }
  print(nrow(MissingEntries))
  rm(tempdf)
}
MissingEntries <- subset(MissingEntries,MissingEntries$ID=='BOL:1990:1990.5:U:i')
# the above is necessary because the API has returned the other entries without
# datayear, so matching is not possible:
# "BGD:1985:1985.5:N:c"  "BGD:1988:1988.5:N:c"  "BGD:1991:1991.5:N:c"  
# "BGD:1995:1995.5:N:c" "BEN:2011:2011.33:N:c" "BWA:1993:1993.33:N:c" 
# "BWA:2002:2002.53:N:c" "BWA:2009:2009.25:N:c" "BWA:2015:2015.85:N:c"
nrow(MissingEntries)==nrow(HHS)*length(IdealPLs) - nrow(MasterDistro)

table(MissingEntries$PL)
#44.57 
#    1

# let's fetch them from PCN
countrycode1 <- strsplit(MissingEntries$ID[1],":",fixed = T)[[1]][1]
year1 <- as.numeric(strsplit(MissingEntries$ID[1],":",fixed = T)[[1]][2])
datayear1 <- as.numeric(strsplit(MissingEntries$ID[1],":",fixed = T)[[1]][3])
coveragetype1 <- strsplit(MissingEntries$ID[1],":",fixed = T)[[1]][4]
datatype1 <- strsplit(MissingEntries$ID[1],":",fixed = T)[[1]][5]
datatype1 <- ifelse(datatype1=="c","consumption","income")

Temp <- povcalnet(
  country = 'BOL',
  povline = 44.57,
  year = 1990,
  aggregate = FALSE,
  fill_gaps = F,
  coverage = "all",
  ppp = NULL,
  url = "http://iresearch.worldbank.org",
  format = "csv"
)

Temp$RequestedLine <- MissingEntries$PL[1]

# next time it must be width = 5 because it goes up to ~16000 and it does not 
# sort properly in R:
save(list = 'Temp',file = paste0('/media/michalis/1984/PovcalNet/NoFillGaps3/DistroLastMissingPLs2.RData'))
print(paste0('Saved file... ',paste0('/media/michalis/1984/PovcalNet/NoFillGaps3/DistroLastMissingPLs2.RData')))

MasterDistro <- rbind(MasterDistro,Temp)
rm(Temp)

ttt <- table(MasterDistro$RequestedLine)
ttt[ttt>nrow(HHS)]
#named integer(0)
sort(ttt[ttt<nrow(HHS)])
#named integer(0)
sum(nrow(HHS)-ttt)
# 0

rm(wrongcols,WrongEntries,TheWrongList,nums,j,k,MissingPLs,no_cores,
   NumericColumns,WronglyNonNumericColumns)
rm(UniqueReqPLs,Distro,cl,FaultyEntries,FaultyTemp,TempDistro)
rm(AllNewLines,AllNewLinesTemplate,Take2HHS,tempdf,TempFaultyEntries)
rm(NotFound,NewNotFound,countrycode,countrycode1,coveragetype,coveragetype1)
rm(datatype,datatype1,datayear,datayear1,FaultyLine,DistroRange,FetchDistroNum)
rm(jjj,i,CurrentFile,tempID,TheFiles)
rm(ttt,year,year1,Take2HHSMissingPLs,NA_entries)
rm(CorrectedLines)
rm(MissingEntries)
# save.image("/media/michalis/1984/PovcalNetTemp5.RData")
# load("/media/michalis/1984/PovcalNetTemp5.RData")
tempID <- HHS$ISO3DataYearCovType[which(!HHS$ISO3DataYearCovType %in% tempdf$ISO3DataYearCovType)]

MissingEntries <- data.frame(ID=tempID,PL=i,stringsAsFactors = F)

##### Last check(s) ####
# do all RequestedPLs have a unique set of entries of length equal to HHS?

total <- length(IdealPLs)
pb <- tkProgressBar(title = "progress bar", min = 0,max = total, width = 300)

for (i in c(1:total)){
  
  setTkProgressBar(pb, i, label=paste( round(i/total*100, 3),"% done"))
  tempdf <- subset(MasterDistro,round(MasterDistro$RequestedLine,3)==round(IdealPLs[i],3))
  
  tempdf$ISO3DataYearCovType <- paste0(tempdf$countrycode,":",tempdf$year,":",
                                       tempdf$datayear,":",tempdf$coveragetype,":",
                                       ifelse(tempdf$datatype=="consumption",'c','i'))
  if (!length(unique(tempdf$ISO3DataYearCovType))==nrow(HHS)){
    print(paste0(i,':',length(unique(tempdf$ISO3DataYearCovType))))
  }
}
close(pb)

# "11522:2055"
# but how can this be that it is only one? while the sum is correct?
# what more is wrong?
i <- 11522
tempdf <- subset(MasterDistro,round(MasterDistro$RequestedLine,3)==round(IdealPLs[i],3))
tempdf$ISO3DataYearCovType <- paste0(tempdf$countrycode,":",tempdf$year,":",
                                     tempdf$datayear,":",tempdf$coveragetype,":",
                                     ifelse(tempdf$datatype=="consumption",'c','i'))
which(duplicated(tempdf$ISO3DataYearCovType))

RowToRemove <- tempdf[which(duplicated(tempdf$ISO3DataYearCovType)),]
RowToRemove$ISO3DataYearCovType <- NULL
paste0(RowToRemove$countrycode,":",RowToRemove$year,":",
       RowToRemove$datayear,":",RowToRemove$coveragetype,":",
       ifelse(RowToRemove$datatype=="consumption",'c','i'))
# "PHL:2006:2006:N:c"
tempdf <- suppressMessages(dplyr::anti_join(x = tempdf, y = RowToRemove))
MasterDistro <- suppressMessages(dplyr::anti_join(x = MasterDistro, y = RowToRemove))

# save.image("/media/michalis/1984/PovcalNetTemp6.RData")
# load("/media/michalis/1984/PovcalNetTemp6.RData")

# Now lets locate which one is missing:
tempID <- HHS$ISO3DataYearCovType[which(!HHS$ISO3DataYearCovType %in% tempdf$ISO3DataYearCovType)]
# "PHL:2006:2006:N:i"
MissingEntries <- data.frame(ID=tempID,PL=IdealPLs[11522],stringsAsFactors = F)

# let's fetch them from PCN
countrycode1 <- strsplit(MissingEntries$ID[1],":",fixed = T)[[1]][1]
year1 <- as.numeric(strsplit(MissingEntries$ID[1],":",fixed = T)[[1]][2])
datayear1 <- as.numeric(strsplit(MissingEntries$ID[1],":",fixed = T)[[1]][3])
coveragetype1 <- strsplit(MissingEntries$ID[1],":",fixed = T)[[1]][4]
datatype1 <- strsplit(MissingEntries$ID[1],":",fixed = T)[[1]][5]
datatype1 <- ifelse(datatype1=="c","consumption","income")

Temp <- povcalnet(
  country = countrycode1,
  povline = IdealPLs[11522],
  year = year1,
  aggregate = FALSE,
  fill_gaps = F,
  coverage = "all",
  ppp = NULL,
  url = "http://iresearch.worldbank.org",
  format = "csv"
)

Temp$RequestedLine <- MissingEntries$PL[1]
Temp <- subset(Temp,Temp$datatype==datatype1)

# next time it must be width = 5 because it goes up to ~16000 and it does not 
# sort properly in R:
save(list = 'Temp',file = 
       paste0('/media/michalis/1984/PovcalNet/NoFillGaps3/DistroLastMissingPLs3.RData'))
print(paste0('Saved file... ',
             paste0('/media/michalis/1984/PovcalNet/NoFillGaps3/DistroLastMissingPLs3.RData')))

MasterDistro <- rbind(MasterDistro,Temp)
rm(Temp)

ttt <- table(MasterDistro$RequestedLine)
ttt[ttt>nrow(HHS)]
#named integer(0)
sort(ttt[ttt<nrow(HHS)])
#named integer(0)
sum(nrow(HHS)-ttt)
# 0

MasterDistro$ISO3DataYearCovType <- paste0(MasterDistro$countrycode,":",
                                           MasterDistro$year,":",
                                           MasterDistro$datayear,":",MasterDistro$coveragetype,":",
                                           ifelse(MasterDistro$datatype=="consumption",'c','i'))

ttt <- table(MasterDistro$ISO3DataYearCovType)

all(ttt==length(IdealPLs))
ttt[ttt>length(IdealPLs)]
ttt[ttt<length(IdealPLs)]

# so there are some entries that are with a missing datayear

# before continuing just a quick check if those are all entries with a missing datayear:
temp <- subset(MasterDistro,is.na(MasterDistro$datayear))
sum(ttt[grepl(":NA:",names(ttt),fixed = T)])==nrow(temp)
# YES!!!!!

# I will replace those NAs with the appropriate ones as captured in ttt
ttt <- ttt[ttt<length(IdealPLs)]
IDs <- ttt[ttt<3]
TargetValues <- ttt[ttt>3]

for (i in c(1:length(IDs))){
  MasterDistro$datayear[which(MasterDistro$ISO3DataYearCovType==names(IDs[i]))] <- as.numeric(strsplit(names(TargetValues)[i],":",fixed = T)[[1]][3])
}

MasterDistro$ISO3DataYearCovType <- paste0(MasterDistro$countrycode,":",
                                           MasterDistro$year,":",
                                           MasterDistro$datayear,":",MasterDistro$coveragetype,":",
                                           ifelse(MasterDistro$datatype=="consumption",'c','i'))

ttt <- table(MasterDistro$ISO3DataYearCovType)

all(ttt==length(IdealPLs))
# TRUE
ttt[ttt>length(IdealPLs)]
# named integer(0)
ttt[ttt<length(IdealPLs)]
# named integer(0)

# This nails it, so we are (almost) done! As a very last test I will slice the 
# dataset per unique HHS then I will check if indeed those 2056 entries are of 
# the same length in terms of unique entries (which must be equal to the length 
# of IdealPLs) although with the above test demonstrates that this must already 
# be the case, but it is good practice to split per unique SSH anyway

##### Split per unique HHS ####

for (i in sort(unique(MasterDistro$ISO3DataYearCovType))){
  DistroPerHHS <- subset(MasterDistro,MasterDistro$ISO3DataYearCovType==i)

  j <- gsub(":","_",i)
  write.csv2(DistroPerHHS,paste0('/media/michalis/1984/PovcalNet/NoFillGaps/SplitPerHHS/',j,'.csv'))
  rm(DistroPerHHS)
}
rm(i)

##### ReSlice per unique HHS ####
### only keep observations up to 100% only
### test monotonicity

PartialDistributions <- c()
SurvivingPLs <- c()

for (i in sort(unique(MasterDistro$ISO3DataYearCovType))){
  DistroPerHHS <- subset(MasterDistro,MasterDistro$ISO3DataYearCovType==i)
  
  # and my last test for completeness:
  # it should have been placed in the previous loop, 
  # but here should do fine as well
  if (!length(unique(DistroPerHHS$RequestedLine))==length(IdealPLs)){
    print(paste0("Fail at ",DistroPerHHS$ISO3DataYearCovType))
  }
  
  # I need to go through each and only keep the poverty lines
  # that bring about a change in the headcount
  
  DistroPerHHS <- DistroPerHHS[ order(DistroPerHHS[,'povertyline']), ]
  DistroPerHHS$Diffs <- c(1,diff(DistroPerHHS$headcount))
  
  # and test monotonicity of the headcount values
  if (any(DistroPerHHS$Diffs<0)){
    stop('monotonicity alert')
  }
  
  # this was misplaced above the monotonicity test
  # so the test was irrelevant at that point...
  DistroPerHHS <- subset(DistroPerHHS,DistroPerHHS$Diffs>0)
  
  if (max(DistroPerHHS$headcount)[1]<1){
    print(paste0(i,':partial distribution up to:',max(DistroPerHHS$headcount)[1]))
    PartialDistributions <- c(PartialDistributions,paste0(i,j))
  }
  
  DistroPerHHS$Diffs <- NULL
  
  SurvivingPLs <- c(SurvivingPLs,DistroPerHHS$RequestedLine)
  SurvivingPLs <- unique(SurvivingPLs)

  j <- gsub(":","_",i)
  write.csv2(DistroPerHHS,paste0('/media/michalis/1984/PovcalNet/NoFillGaps2/SplitPerHHS/',j,'.csv'))
  rm(DistroPerHHS)
  
}

# based on the density of the surviving observations I can update the IdealPLs list to:

# save.image("/media/michalis/1984/PovcalNetTemp7.RData") I haven't saved this...
# load("/media/michalis/1984/PovcalNetTemp7.RData")

#### Part B: Fetch original and imputed ####

library(povcalnetR)
library(tictoc)
library(doParallel)
library(beepr)
library(tcltk)

rm(list= ls())

##### Fetch All HHS with interpolations ####
# because after experimenting with various lengths of requests
# it appears that processing large chunks of the IdealPLs is
# unstable (curl errors and non terminating foreach)
# I use a for loop that walks through the IdealPLs at 100
# elements in each foreach

# my own take for Ideal PLs:
# IdealPLs <- c(seq(0.001,5,0.001),seq(5.01,45,0.01),seq(45.1,155,0.1))
# expanding it according to OWID_PLs

IdealPLs <- c(seq(0.001,5,0.001),seq(5.01,60,0.01),seq(60.1,150,0.1),
              seq(150.5,1400,0.5), seq(1405,3000,5), seq(3010,10000,10),
              seq(11000,35000,100),99999)

for (i in c(seq(100,length(IdealPLs),15162)){
  no_cores <- 5
  cl <- makeCluster(no_cores, type="FORK")
  registerDoParallel(cl)
  if (i>15100){
    low_i <- i-61
  } else {
    low_i <- i-99
  }
  Distro <- foreach(jjj=IdealPLs[c(low_i:i)], 
                    #.combine='rbind', 
                    .errorhandling = "pass") %dopar% { 
                      
                      ttt <- 8
                      while (ttt>0){
                        Temp <- povcalnet(
                          country = "all",
                          povline = jjj,
                          year = "all",
                          aggregate = FALSE,
                          fill_gaps = T,
                          coverage = "all",
                          ppp = NULL,
                          url = "http://iresearch.worldbank.org",
                          format = "csv"
                        )
                        
                        WrongEntries <- which(!trimws(format(Temp$povertyline,nsmall = 3))==
                                                trimws(format(jjj, nsmall = 3)))
                        
                        if (length(WrongEntries)>0){
                          ttt <- ttt - 1
                        } else {
                          ttt <- 0
                        }
                      }
                      
                      # I added this extra column because in several instances
                      # the poverty line returned from a particular country
                      # is much different from the poverty line requested
                      # e.g. when asking PL of 1.009 I got a 0.2264779
                      # PL for Burundi in 1981
                      # in the same df I got year 19892Y and datayear 0.0163
                      # for Belarus see 
                      # "/media/michalis/1984/PovcalNet/Examples/Distro1100.RData" oh I just deleted it...
                      Temp$RequestedLine <- jjj
                      return(Temp)
                    }
  stopCluster(cl)
  registerDoSEQ()
  # next time it must be width = 5 because it goes up to ~16000 and it does not 
  # sort properly in R:
  save(list = 'Distro',file = paste0('/media/michalis/1984/PovcalNet/Distro',formatC(i,width = 5, format = "d", flag = "0"),'.RData'))
  print(paste0('Saved file... ',paste0('/media/michalis/1984/PovcalNet/Distro',formatC(i,width = 5, format = "d", flag = "0"),'.RData')))
  rm(Distro)
}

###### Integrity Check and Combine saved data ####

# let's get the data from World Bank's PovcalNet API:
PCN <- povcalnet_info()
# PCN df is required to request all countries' info from PovcalNet:
HHS <- povcalnet(country = PCN$country_code)
TempDistro <- povcalnetR::povcalnet_cl('USA',1,2010)
TempDistro$RequestedLine <- as.numeric(NA)
MasterDistro <- subset(TempDistro,TempDistro$countrycode=='2398y9wfhehfsdih') # just maintain 
TempMasterDistro <- subset(TempDistro,TempDistro$countrycode=='2398y9wfhehfsdih') # just maintain 
# the data structure
FaultyEntries <- subset(TempDistro,TempDistro$countrycode=='2398y9wfhehfsdih') # just maintain 
# the data structure and add a comment column
FaultyEntries$Comments <- as.character(NA)
SavedDistrosFolder <- '/media/michalis/1984/PovcalNet'
TheFiles <- list.files(SavedDistrosFolder,pattern = 'Distro')
#TheFiles <- TheFiles[c(34:42,44:53)]
TheWrongList <- rep(as.numeric(NA),length(IdealPLs))
names(TheWrongList) <- trimws(format(IdealPLs, nsmall = 3))

options(warn=2) # turn warnings to errors, for better debugging
tictoc::tic()
for (i in c(1:length(TheFiles))){
  #for (i in c(1)){
  # Load the saved data from the disk
  CurrentFile <- paste0(SavedDistrosFolder, '/',TheFiles[i])
  load(CurrentFile)
  print(CurrentFile)
  
  # First check: all list elements must have a fixed length of 32
  # equal to the number of columns returned by the PovcalNet API (31)
  # plus one extra column I add for control ("RequestedLine")
  # that stores the PL requested to the API.
  # Elements not complying are removed, and at the end of this process
  # we will have a reporting variable with all the PL values that
  # need to be requested again from the API
  
  if (!all(sapply(Distro, length)==32)){
    while (!all(sapply(Distro, length)==32)){
      # remove those that did not:
      Distro[[which(!(sapply(Distro, length)==32))[1]]] <- NULL
    }
    print(paste0('Current number of fetched PLs', length(Distro),". Normally this must be 100."))
  } else {
    print('No entries with less than 32 columns to remove...')
  }
  
  # Second check: all entries from a particular list element (so within each list
  # element) must have Distro$RequestedLine == Distro$povertyline
  # those that do not are kept in a separate dataframe
  # plus other integrity checks in the loop below:
  
  for (j in c(1:length(Distro))){
    
    Temp <- Distro[[j]]
    NewFaultyEntries <- subset(FaultyEntries,FaultyEntries$countrycode=='498heo98h')
    
    # Rule 0: no line with all NA, and no line with 
    # countrycode == "CountryCode"
    # and no line with countryname=="DELETE"
    Temp <- subset(Temp,!Temp$countrycode=="CountryCode")
    Temp <- subset(Temp,!Temp$countryname=="DELETE")
    
    # Rule 0.5: all PLs must be identical to the one requested
    WrongEntries <- which(!trimws(format(Temp$povertyline,nsmall = 3))==
                            trimws(format(Temp$RequestedLine, nsmall = 3)))
    NonIdenticalLines <- length(WrongEntries)
    
    FaultyTemp <- Temp[WrongEntries,]
    FaultyTemp$Comments <- 'PL not identical to the one requested'
    Temp <- suppressMessages(dplyr::anti_join(x = Temp, y = FaultyTemp))
    NewFaultyEntries <- rbind(NewFaultyEntries,FaultyTemp)
    
    # Rule 1: all PPPs from one ISO3 must be the same
    # and matching the value from HHS
    for (k in sort(unique(Temp$countrycode))){
      WrongEntries <- which(!Temp$ppp[which(Temp$countrycode==k)]==unique(HHS$ppp[which(HHS$countrycode==k)]))
      if (length(WrongEntries)>0){
        FaultyTemp <- Temp[which(Temp$countrycode==k)[WrongEntries],]
        # remove that entry from the Temp dataframe
        Temp <- suppressMessages(dplyr::anti_join(x = Temp, y = FaultyTemp))
        FaultyTemp$Comments <- 'Wrong PPP value'
        NewFaultyEntries <- rbind(NewFaultyEntries,FaultyTemp)
        rm(FaultyTemp)
      }
      rm(WrongEntries)
    }
    
    # Rule 2: columns "year" "datayear" and from isinterpolated until 
    # "decile10" must be numeric or convertible to numeric without warnings
    # define which columns must be numeric:
    NumericColumns <- c("year","datayear", names(Temp)[c(8:31)])
    # get the columns that actually are numeric:
    nums <- unlist(lapply(Temp, is.numeric)) 
    # and extract those that are not, although they should:
    WronglyNonNumericColumns <- NumericColumns[which(!NumericColumns %in% names(Temp)[nums])]
    # across those find the non-numeric entries:
    for (wrongcols in c(WronglyNonNumericColumns)){
      WrongEntries <- suppressWarnings(which(is.na(as.numeric(unlist(Temp[,wrongcols])))))
      NA_entries <- which(is.na((unlist(Temp[,wrongcols]))))
      WrongEntries <- WrongEntries[which(!WrongEntries %in% NA_entries)]
      if (length(WrongEntries)>0){
        FaultyTemp <- Temp[WrongEntries,]
        # remove that entry from the Temp dataframe
        Temp <- suppressMessages(dplyr::anti_join(x = Temp, y = FaultyTemp))
        FaultyTemp$Comments <- paste0('Non-numeric value in column ', wrongcols)
        NewFaultyEntries <- rbind(NewFaultyEntries,FaultyTemp)
        rm(FaultyTemp)
      }
      rm(WrongEntries)
    }
    
    # Rule 3: in non-interpolated entries "year", "datayear" must be identical 
    # with their corresponding HHS entry
    #WrongEntries <- which(!(Temp$coveragetype %in% HHS$coveragetype))
    #if (length(WrongEntries)>0){
    #  stop('build the code for Rule 3')
    #}
    #rm(WrongEntries)
    
    # Rule 4: interpolated values must be between the benchmark values used 
    # in the interpolation
    #WrongEntries <- which(!(Temp$coveragetype %in% HHS$coveragetype))
    #if (length(WrongEntries)>0){
    #  stop('build the code for Rule 4')
    #}
    #rm(WrongEntries)
    
    # Rule 5: coverage type must be from the range included in HHS
    WrongEntries <- which(!(Temp$coveragetype %in% HHS$coveragetype))
    if (length(WrongEntries)>0){
      stop('build the code for Rule 5')
    }
    rm(WrongEntries)
    
    # Rule 6: apply the allowed values limits to the data using
    # https://rdrr.io/cran/userfriendlyscience/man/checkDataIntegrity.html
    # to be developed...
    
    # keeping a log over the distros with different PLs than requested:
    TheWrongList[which(names(TheWrongList)==
                         as.character(unique(trimws(format(NewFaultyEntries$RequestedLine, 
                                                           nsmall = 3)))))] <- NonIdenticalLines
    
    rm(NonIdenticalLines)
    FaultyEntries <- rbind(FaultyEntries,NewFaultyEntries)
    rm(NewFaultyEntries)
    
    TempMasterDistro <- rbind(TempMasterDistro,Temp)
    rm(Temp)
  }
  MasterDistro <- rbind(MasterDistro,TempMasterDistro)
  TempMasterDistro <- subset(TempDistro,TempDistro$countrycode=='2398y9wfhehfsdih') 
  rm(Distro)
  print('-------------------------------------')
}
options(warn=0) # restore to default from warn=2
tictoc::toc()

#[1] "/media/michalis/1984/PovcalNet/FDistro11900.RData"
#[1] "Current number of fetched PLs99. Normally this must be 100."
#[1] "/media/michalis/1984/PovcalNet/FDistro14900.RData"
#[1] "Current number of fetched PLs99. Normally this must be 100."

DistroRange <- paste0(readr::parse_number(TheFiles[1]),'-',readr::parse_number(TheFiles[length(TheFiles)]))
save(list = 'MasterDistro',file = paste0('/media/michalis/1984/PovcalNet/MasterData/MasterDistro',DistroRange,'.RData'))
save(list = 'FaultyEntries',file = paste0('/media/michalis/1984/PovcalNet/MasterData/FaultyEntries',DistroRange,'.RData'))

table(FaultyEntries$Comments)
# PL not identical to the one requested 
# 1264494 
length(table(FaultyEntries$RequestedLine))
# [1] 8324

HHS2 <- povcalnet(
  country = "all",
  povline = 1.9,
  year = "all",
  aggregate = FALSE,
  fill_gaps = T,
  coverage = "all",
  ppp = NULL,
  url = "http://iresearch.worldbank.org",
  format = "csv"
)

# PCN returns 6503 unique HHS, and I have a PL vector with length 15162
nrow(HHS2)*length(IdealPLs)
# 98598486
nrow(FaultyEntries)+nrow(MasterDistro)
# 98585480
nrow(HHS2)*length(IdealPLs) - (nrow(FaultyEntries)+nrow(MasterDistro))
# 13006
nrow(HHS2)*length(IdealPLs) ==
  nrow(FaultyEntries)+nrow(MasterDistro) + 2*nrow(HHS2) # 2 are the missing RequestedLines
# TRUE

##### Fetch Take 2 All HHS with interpolations ####

rm(list= ls()[!(ls() %in% c('IdealPLs'))])

for (i in c(seq(100,length(IdealPLs),100),15162)){
  no_cores <- 5
  cl <- makeCluster(no_cores, type="FORK")
  registerDoParallel(cl)
  if (i>15100){
    low_i <- i-61
  } else {
    low_i <- i-99
  }
  Distro <- foreach(jjj=IdealPLs[c(low_i:i)], 
                    #.combine='rbind', 
                    .errorhandling = "pass") %dopar% { 
                      
                      ttt <- 8
                      while (ttt>0){
                        Temp <- povcalnet(
                          country = "all",
                          povline = jjj,
                          year = "all",
                          aggregate = FALSE,
                          fill_gaps = T,
                          coverage = "all",
                          ppp = NULL,
                          url = "http://iresearch.worldbank.org",
                          format = "csv"
                        )
                        
                        WrongEntries <- which(!trimws(format(Temp$povertyline,nsmall = 3))==
                                                trimws(format(jjj, nsmall = 3)))
                        
                        if (length(WrongEntries)>0){
                          ttt <- ttt - 1
                        } else {
                          ttt <- 0
                        }
                      }
                      
                      # I added this extra column because in several instances
                      # the poverty line returned from a particular country
                      # is much different from the poverty line requested
                      # e.g. when asking PL of 1.009 I got a 0.2264779
                      # PL for Burundi in 1981
                      # in the same df I got year 19892Y and datayear 0.0163
                      # for Belarus see 
                      # "/media/michalis/1984/PovcalNet/Examples/Distro1100.RData" oh I just deleted it...
                      Temp$RequestedLine <- jjj
                      return(Temp)
                    }
  stopCluster(cl)
  registerDoSEQ()
  # next time it must be width = 5 because it goes up to ~16000 and it does not 
  # sort properly in R:
  save(list = 'Distro',file = paste0('/media/michalis/1984/PovcalNet/WithFills/Distro',formatC(i,width = 5, format = "d", flag = "0"),'.RData'))
  print(paste0('Saved file... ',paste0('/media/michalis/1984/PovcalNet/WithFills/Distro',formatC(i,width = 5, format = "d", flag = "0"),'.RData')))
  rm(Distro)
}

###### Integrity Check and Combine saved data ####
# do I need the integrity check on take 2>???

# let's get the data from World Bank's PovcalNet API:
PCN <- povcalnet_info()
# PCN df is required to request all countries' info from PovcalNet:
HHS <- povcalnet(country = PCN$country_code)
TempDistro <- povcalnetR::povcalnet_cl('USA',1,2010)
TempDistro$RequestedLine <- as.numeric(NA)
MasterDistro <- subset(TempDistro,TempDistro$countrycode=='2398y9wfhehfsdih') # just maintain 
TempMasterDistro <- subset(TempDistro,TempDistro$countrycode=='2398y9wfhehfsdih') # just maintain 
# the data structure
FaultyEntries <- subset(TempDistro,TempDistro$countrycode=='2398y9wfhehfsdih') # just maintain 
# the data structure and add a comment column
FaultyEntries$Comments <- as.character(NA)
SavedDistrosFolder <- '/media/michalis/1984/PovcalNet/WithFills'
TheFiles <- list.files(SavedDistrosFolder,pattern = 'Distro')
#TheFiles <- TheFiles[c(34:42,44:53)]
TheWrongList <- rep(as.numeric(NA),length(IdealPLs))
names(TheWrongList) <- trimws(format(IdealPLs, nsmall = 3))

options(warn=2) # turn warnings to errors, for better debugging
tictoc::tic()
for (i in c(1:length(TheFiles))){
  #for (i in c(1)){
  # Load the saved data from the disk
  CurrentFile <- paste0(SavedDistrosFolder, '/',TheFiles[i])
  load(CurrentFile)
  print(CurrentFile)
  
  # First check: all list elements must have a fixed length of 32
  # equal to the number of columns returned by the PovcalNet API (31)
  # plus one extra column I add for control ("RequestedLine")
  # that stores the PL requested to the API.
  # Elements not complying are removed, and at the end of this process
  # we will have a reporting variable with all the PL values that
  # need to be requested again from the API
  
  if (!all(sapply(Distro, length)==32)){
    while (!all(sapply(Distro, length)==32)){
      # remove those that did not:
      Distro[[which(!(sapply(Distro, length)==32))[1]]] <- NULL
    }
    print(paste0('Current number of fetched PLs', length(Distro),". Normally this must be 100."))
  } else {
    print('No entries with less than 32 columns to remove...')
  }
  
  # Second check: all entries from a particular list element (so within each list
  # element) must have Distro$RequestedLine == Distro$povertyline
  # those that do not are kept in a separate dataframe
  # plus other integrity checks in the loop below:
  
  for (j in c(1:length(Distro))){
    
    Temp <- Distro[[j]]
    NewFaultyEntries <- subset(FaultyEntries,FaultyEntries$countrycode=='498heo98h')
    
    # Rule 0: no line with all NA, and no line with 
    # countrycode == "CountryCode"
    # and no line with countryname=="DELETE"
    Temp <- subset(Temp,!Temp$countrycode=="CountryCode")
    Temp <- subset(Temp,!Temp$countryname=="DELETE")
    
    # Rule 0.5: all PLs must be identical to the one requested
    WrongEntries <- which(!trimws(format(Temp$povertyline,nsmall = 3))==
                          trimws(format(Temp$RequestedLine, nsmall = 3)))
    NonIdenticalLines <- length(WrongEntries)
    
    FaultyTemp <- Temp[WrongEntries,]
    FaultyTemp$Comments <- 'PL not identical to the one requested'
    Temp <- suppressMessages(dplyr::anti_join(x = Temp, y = FaultyTemp))
    NewFaultyEntries <- rbind(NewFaultyEntries,FaultyTemp)
    
    # Rule 1: all PPPs from one ISO3 must be the same
    # and matching the value from HHS
    for (k in sort(unique(Temp$countrycode))){
      WrongEntries <- which(!Temp$ppp[which(Temp$countrycode==k)]==unique(HHS$ppp[which(HHS$countrycode==k)]))
      if (length(WrongEntries)>0){
        FaultyTemp <- Temp[which(Temp$countrycode==k)[WrongEntries],]
        # remove that entry from the Temp dataframe
        Temp <- suppressMessages(dplyr::anti_join(x = Temp, y = FaultyTemp))
        FaultyTemp$Comments <- 'Wrong PPP value'
        NewFaultyEntries <- rbind(NewFaultyEntries,FaultyTemp)
        rm(FaultyTemp)
      }
      rm(WrongEntries)
    }
    
    # Rule 2: columns "year" "datayear" and from isinterpolated until 
    # "decile10" must be numeric or convertible to numeric without warnings
    # define which columns must be numeric:
    NumericColumns <- c("year","datayear", names(Temp)[c(8:31)])
    # get the columns that actually are numeric:
    nums <- unlist(lapply(Temp, is.numeric)) 
    # and extract those that are not, although they should:
    WronglyNonNumericColumns <- NumericColumns[which(!NumericColumns %in% names(Temp)[nums])]
    # across those find the non-numeric entries:
    for (wrongcols in c(WronglyNonNumericColumns)){
      WrongEntries <- suppressWarnings(which(is.na(as.numeric(unlist(Temp[,wrongcols])))))
      NA_entries <- which(is.na((unlist(Temp[,wrongcols]))))
      WrongEntries <- WrongEntries[which(!WrongEntries %in% NA_entries)]
      if (length(WrongEntries)>0){
        FaultyTemp <- Temp[WrongEntries,]
        # remove that entry from the Temp dataframe
        Temp <- suppressMessages(dplyr::anti_join(x = Temp, y = FaultyTemp))
        FaultyTemp$Comments <- paste0('Non-numeric value in column ', wrongcols)
        NewFaultyEntries <- rbind(NewFaultyEntries,FaultyTemp)
        rm(FaultyTemp)
      }
      rm(WrongEntries)
    }
    
    # Rule 3: in non-interpolated entries "year", "datayear" must be identical 
    # with their corresponding HHS entry
    #WrongEntries <- which(!(Temp$coveragetype %in% HHS$coveragetype))
    #if (length(WrongEntries)>0){
    #  stop('build the code for Rule 3')
    #}
    #rm(WrongEntries)
    
    # Rule 4: interpolated values must be between the benchmark values used 
    # in the interpolation
    #WrongEntries <- which(!(Temp$coveragetype %in% HHS$coveragetype))
    #if (length(WrongEntries)>0){
    #  stop('build the code for Rule 4')
    #}
    #rm(WrongEntries)
    
    # Rule 5: coverage type must be from the range included in HHS
    WrongEntries <- which(!(Temp$coveragetype %in% HHS$coveragetype))
    if (length(WrongEntries)>0){
      stop('build the code for Rule 5')
    }
    rm(WrongEntries)
    
    # Rule 6: apply the allowed values limits to the data using
    # https://rdrr.io/cran/userfriendlyscience/man/checkDataIntegrity.html
    # to be developed...
    
    # keeping a log over the distros with different PLs than requested:
    TheWrongList[which(names(TheWrongList)==
                       as.character(unique(trimws(format(NewFaultyEntries$RequestedLine, 
                                                         nsmall = 3)))))] <- NonIdenticalLines
    
    rm(NonIdenticalLines)
    FaultyEntries <- rbind(FaultyEntries,NewFaultyEntries)
    rm(NewFaultyEntries)
    
    TempMasterDistro <- rbind(TempMasterDistro,Temp)
    rm(Temp)
  }
  MasterDistro <- rbind(MasterDistro,TempMasterDistro)
  TempMasterDistro <- subset(TempDistro,TempDistro$countrycode=='2398y9wfhehfsdih') 
  rm(Distro)
  print('-------------------------------------')
}
options(warn=0) # restore to default from warn=2
tictoc::toc()
# 14126.986
DistroRange <- paste0(readr::parse_number(TheFiles[1]),'-',readr::parse_number(TheFiles[length(TheFiles)]))
save(list = 'MasterDistro',file = paste0('/media/michalis/1984/PovcalNet/WithFills/MasterData/MasterDistroB',DistroRange,'.RData'))
save(list = 'FaultyEntries',file = paste0('/media/michalis/1984/PovcalNet/WithFills/MasterData/FaultyEntriesB',DistroRange,'.RData'))

table(FaultyEntries$Comments)
# PL not identical to the one requested 
# 13639 
length(table(FaultyEntries$RequestedLine))
# [1] 1213

# https://stackoverflow.com/questions/2851327/combine-a-list-of-data-frames-into-one-data-frame-by-row

###### Merge Take 2 with Take 1 on FaultyEntries ####
# merge on faulty entries and missing years the two takes on HHS without interpolations
# to minimize the faulty entries and missing years to be reFetched

load("/media/michalis/1984/PovcalNet/MasterData/FaultyEntries100-15162.RData")
load("/media/michalis/1984/PovcalNet/MasterData/MasterDistro100-15162.RData")

# this contains the Faulty lines of which a proper entry is found:
CorrectedLines <- subset(FaultyEntries,FaultyEntries$countrycode=='sdfkjsdkjfshdk')
# this contains the Faulty lines of which a proper entry is NOT found:
NotFound <- subset(FaultyEntries,FaultyEntries$countrycode=='sdfkjsdkjfshdk')
# this contains the new data lines that are found (to be used instead of the faulty lines):
NewData <- CorrectedLines # empty template to be populated in the loop
NewData$Comments <- NULL # to be of the same width as the MasterDistro dataframe
AllNewLinesTemplate <- NewData # reference empty template
Take2HHSMissingPLs <- c() # which PLs are missing from the Take2 PCN HHS fetch

total <- length(unique(FaultyEntries$RequestedLine))
pb <- tkProgressBar(title = "progress bar", min = 0,max = total, width = 300)

for (i in c(1:total)){
  
  setTkProgressBar(pb, i, label=paste( round(i/total*100, 3),"% done"))
  
  NewNotFound <- subset(FaultyEntries,FaultyEntries$countrycode=='sdfkjsdkjfshdk')
  
  FaultyLine <- as.numeric(sort(unique(FaultyEntries$RequestedLine))[i])
  FetchDistroNum <- ceiling(which(IdealPLs==FaultyLine)/100)*100
  if (FetchDistroNum==15200){
    FetchDistroNum <- length(IdealPLs)
  }
  #if (FetchDistroNum<10000){
    load(paste0('/media/michalis/1984/PovcalNet/WithFills/Distro',formatC(FetchDistroNum,width = 5, format = "d", flag = "0"),'.RData'))
  #} else {
  #  load(paste0('/media/michalis/1984/PovcalNet/WithFills/FDistro',formatC(FetchDistroNum,width = 5, format = "d", flag = "0"),'.RData'))
  #}
  if (which(IdealPLs==FaultyLine) %% 100>0){
    Take2HHS <- Distro[[which(IdealPLs==FaultyLine) %% 100]]
  } else {
    Take2HHS <- Distro[[100]]
  }
  
  if (is.null(nrow(Take2HHS))){
    Take2HHSMissingPLs <- c(Take2HHSMissingPLs,FaultyLine)
  } else {
    
    # locate the FaultyLine in the new HHS set:
    TempFaultyEntries <- subset(FaultyEntries,FaultyEntries$RequestedLine==FaultyLine)
    AllNewLines <- AllNewLinesTemplate
    
    for (j in 1:nrow(TempFaultyEntries)){
      
      NewLine <- subset(Take2HHS,Take2HHS$countrycode==TempFaultyEntries$countrycode[j] &
                        Take2HHS$year==TempFaultyEntries$year[j] &
                        Take2HHS$datayear==TempFaultyEntries$datayear[j] &
                        Take2HHS$coveragetype==TempFaultyEntries$coveragetype[j] &
                        Take2HHS$datatype==TempFaultyEntries$datatype[j] &
                        round(Take2HHS$povertyline,3)==round(TempFaultyEntries$RequestedLine[j],3))
      
      AllNewLines <- rbind(AllNewLines,NewLine)
      if (nrow(NewLine)==0){
        NewNotFound <- rbind(NewNotFound,TempFaultyEntries[j,])
      }
      rm(NewLine)
    }
    
    NotFound <- rbind(NotFound,NewNotFound)
    
    if (nrow(AllNewLines)+nrow(NewNotFound)==nrow(TempFaultyEntries)){
      if (all(round(AllNewLines$povertyline,3)==round(FaultyLine,3))){
        CorrectedLines <- rbind(CorrectedLines,TempFaultyEntries)
        NewData <- rbind(NewData,AllNewLines)
      } else {
        stop('!all(AllNewLines$povertyline)==FaultyLine')
      }
    } else {
      stop("!nrow(AllNewLines)+nrow(NewNotFound)==nrow(TempFaultyEntries)")
    }
  }
}
close(pb)
rm(Distro,pb,i,j,no_cores,total)

save.image("/media/michalis/1984/PovcalNetTemp2BB.RData")
# load("/media/michalis/1984/PovcalNetTemp2BB.RData")
#length(which(table(MasterDistro$RequestedLine)<nrow(HHS)))

# check if there are more than we would expect:
ttt <- table(MasterDistro$RequestedLine)
ttt[ttt>nrow(HHS2)]
# integer(0)

###### Merge New and MasterDistro ####
MasterDistro <- rbind(MasterDistro,NewData)
ttt <- table(MasterDistro$RequestedLine)
ttt[ttt>nrow(HHS2)]
# integer(0)

rm(NewData)
WrongEntries <- which(!trimws(format(MasterDistro$povertyline,nsmall = 3))==
                      trimws(format(MasterDistro$RequestedLine, nsmall = 3)))
# this test goes OK but that was expected
UniqueReqPLs <- as.numeric(trimws(sort(unique(MasterDistro$RequestedLine))))
UniqueReqPLs <- as.numeric(format(UniqueReqPLs,nsmall = 3))
MissingPLs <- IdealPLs[which(!(round(IdealPLs,3) %in% round(UniqueReqPLs,3)))]
# So I should be missing 
length(MissingPLs)*nrow(HHS2)
# 13006, from the theoretical number of data points:
# PCN returns 6503 unique HHS2, and I have a PL vector with length 15162
nrow(HHS2)*length(IdealPLs)
# 98598486
nrow(HHS2)*length(IdealPLs) ==
  nrow(MasterDistro) + length(MissingPLs)*nrow(HHS2) # 2 are the missing RequestedLines
# and 2 are the MissingPLs found; FALSE!
nrow(HHS2)*length(IdealPLs) -
  (nrow(MasterDistro) + length(MissingPLs)*nrow(HHS2))
# I am missing 416809 extra entries, so I will first get the missing PLs and then check
# what is wrong

#rm(AllNewLines,AllNewLinesTemplate,CorrectedLines,FaultyEntries,NewNotFound,
#   NotFound,TempFaultyEntries,Take2HHS)
#rm(WrongEntries,Take2HHSMissingPLs,FetchDistroNum,FaultyLine)
# save.image("/media/michalis/1984/PovcalNetTemp3.RData")
# load("/media/michalis/1984/PovcalNetTemp3.RData")

###### Process the missing PLs ####
# from the above I am still missing the PLs that are entirely missing from the Take 1!
# so I need to fetch them

library(povcalnetR)
library(doParallel)

no_cores <- 2
cl <- makeCluster(no_cores, type="FORK")
registerDoParallel(cl)
Distro <- foreach(jjj=MissingPLs, 
                  #.combine='rbind', 
                  .errorhandling = "pass") %dopar% { 
                    
                    ttt <- 8
                    while (ttt>0){
                      Temp <- povcalnet(
                        country = "all",
                        povline = jjj,
                        year = "all",
                        aggregate = FALSE,
                        fill_gaps = F,
                        coverage = "all",
                        ppp = NULL,
                        url = "http://iresearch.worldbank.org",
                        format = "csv"
                      )
                      
                      WrongEntries <- which(!trimws(format(Temp$povertyline,nsmall = 3))==
                                            trimws(format(jjj, nsmall = 3)))
                      
                      if (length(WrongEntries)>0){
                        ttt <- ttt - 1
                      } else {
                        ttt <- 0
                      }
                    }
                    
                    # I added this extra column because in several instances
                    # the poverty line returned from a particular country
                    # is much different from the poverty line requested
                    # e.g. when asking PL of 1.009 I got a 0.2264779
                    # PL for Burundi in 1981
                    # in the same df I got year 19892Y and datayear 0.0163
                    # for Belarus see 
                    # "/media/michalis/1984/PovcalNet/Examples/Distro1100.RData" oh I just deleted it...
                    Temp$RequestedLine <- jjj
                    return(Temp)
                  }
stopCluster(cl)
registerDoSEQ()
# next time it must be width = 5 because it goes up to ~16000 and it does not 
# sort properly in R:
save(list = 'Distro',file = paste0('/media/michalis/1984/PovcalNet/WithFills/MasterData/DistroMissingPLs.RData'))
print(paste0('Saved file... ',paste0('/media/michalis/1984/PovcalNet/WithFills/MasterData/DistroMissingPLs.RData')))

###### Integrity Check ####

load('/media/michalis/1984/PovcalNet/NoFillGaps3/DistroMissingPLs.RData')
# let's get the data from World Bank's PovcalNet API:
PCN <- povcalnet_info()
# PCN df is required to request all countries' info from PovcalNet:

TempDistro <- povcalnetR::povcalnet_cl('USA',1,2010)
TempDistro$RequestedLine <- as.numeric(NA)
TempMasterDistro <- subset(TempDistro,TempDistro$countrycode=='2398y9wfhehfsdih') # just maintain 
# the data structure
FaultyEntries <- subset(TempDistro,TempDistro$countrycode=='2398y9wfhehfsdih') # just maintain 
# the data structure and add a comment column
FaultyEntries$Comments <- as.character(NA)
TheWrongList <- rep(as.numeric(NA),length(MissingPLs))
names(TheWrongList) <- trimws(format(MissingPLs, nsmall = 3))

# check if the new distribution have the right width
if (!all(sapply(Distro, length)==32)){
  while (!all(sapply(Distro, length)==32)){
    # remove those that did not:
    Distro[[which(!(sapply(Distro, length)==32))[1]]] <- NULL
  }
  print(paste0('Current number of fetched PLs', length(Distro),". Normally this must be 100."))
} else {
  print('No entries with less than 32 columns to remove...')
}

# Second check: all entries from a particular list element (so within each list
# element) must have Distro$RequestedLine == Distro$povertyline
# those that do not are kept in a separate dataframe
# plus other integrity checks in the loop below:
# here I also integrate them in a new dataframe ready to be binded with MasterDistro
# I am doing this using TempMasterDistro

for (j in c(1:length(Distro))){
  
  Temp <- Distro[[j]]
  NewFaultyEntries <- subset(FaultyEntries,FaultyEntries$countrycode=='498heo98h')
  
  # Rule 0: no line with all NA, and no line with 
  # countrycode == "CountryCode"
  # and no line with countryname=="DELETE"
  Temp <- subset(Temp,!Temp$countrycode=="CountryCode")
  Temp <- subset(Temp,!Temp$countryname=="DELETE")
  
  # Rule 0.5: all PLs must be identical to the one requested
  WrongEntries <- which(!trimws(format(Temp$povertyline,nsmall = 3))==
                        trimws(format(Temp$RequestedLine, nsmall = 3)))
  NonIdenticalLines <- length(WrongEntries)
  
  FaultyTemp <- Temp[WrongEntries,]
  FaultyTemp$Comments <- 'PL not identical to the one requested'
  Temp <- suppressMessages(dplyr::anti_join(x = Temp, y = FaultyTemp))
  NewFaultyEntries <- rbind(NewFaultyEntries,FaultyTemp)
  
  # Rule 1: all PPPs from one ISO3 must be the same
  # and matching the value from HHS
  for (k in sort(unique(Temp$countrycode))){
    WrongEntries <- which(!Temp$ppp[which(Temp$countrycode==k)]==unique(HHS2$ppp[which(HHS2$countrycode==k)]))
    if (length(WrongEntries)>0){
      FaultyTemp <- Temp[which(Temp$countrycode==k)[WrongEntries],]
      # remove that entry from the Temp dataframe
      Temp <- suppressMessages(dplyr::anti_join(x = Temp, y = FaultyTemp))
      FaultyTemp$Comments <- 'Wrong PPP value'
      NewFaultyEntries <- rbind(NewFaultyEntries,FaultyTemp)
      rm(FaultyTemp)
    }
    rm(WrongEntries)
  }
  
  # Rule 2: columns "year" "datayear" and from isinterpolated until 
  # "decile10" must be numeric or convertible to numeric without warnings
  # define which columns must be numeric:
  NumericColumns <- c("year","datayear", names(Temp)[c(8:31)])
  # get the columns that actually are numeric:
  nums <- unlist(lapply(Temp, is.numeric)) 
  # and extract those that are not, although they should:
  WronglyNonNumericColumns <- NumericColumns[which(!NumericColumns %in% names(Temp)[nums])]
  # across those find the non-numeric entries:
  for (wrongcols in c(WronglyNonNumericColumns)){
    WrongEntries <- suppressWarnings(which(is.na(as.numeric(unlist(Temp[,wrongcols])))))
    NA_entries <- which(is.na((unlist(Temp[,wrongcols]))))
    WrongEntries <- WrongEntries[which(!WrongEntries %in% NA_entries)]
    if (length(WrongEntries)>0){
      FaultyTemp <- Temp[WrongEntries,]
      # remove that entry from the Temp dataframe
      Temp <- suppressMessages(dplyr::anti_join(x = Temp, y = FaultyTemp))
      FaultyTemp$Comments <- paste0('Non-numeric value in column ', wrongcols)
      NewFaultyEntries <- rbind(NewFaultyEntries,FaultyTemp)
      rm(FaultyTemp)
    }
    rm(WrongEntries)
  }
  
  # Rule 3: in non-interpolated entries "year", "datayear" must be identical 
  # with their corresponding HHS entry
  #WrongEntries <- which(!(Temp$coveragetype %in% HHS$coveragetype))
  #if (length(WrongEntries)>0){
  #  stop('build the code for Rule 3')
  #}
  #rm(WrongEntries)
  
  # Rule 4: interpolated values must be between the benchmark values used 
  # in the interpolation
  #WrongEntries <- which(!(Temp$coveragetype %in% HHS$coveragetype))
  #if (length(WrongEntries)>0){
  #  stop('build the code for Rule 4')
  #}
  #rm(WrongEntries)
  
  # Rule 5: coverage type must be from the range included in HHS
  WrongEntries <- which(!(Temp$coveragetype %in% HHS2$coveragetype))
  if (length(WrongEntries)>0){
    stop('build the code for Rule 5')
  }
  rm(WrongEntries)
  
  # Rule 6: apply the allowed values limits to the data using
  # https://rdrr.io/cran/userfriendlyscience/man/checkDataIntegrity.html
  # to be developed...
  
  # keeping a log over the distros with different PLs than requested:
  TheWrongList[which(names(TheWrongList)==
                     as.character(unique(trimws(format(NewFaultyEntries$RequestedLine, 
                                                       nsmall = 3)))))] <- NonIdenticalLines
  
  rm(NonIdenticalLines)
  FaultyEntries <- rbind(FaultyEntries,NewFaultyEntries)
  rm(NewFaultyEntries)
  
  TempMasterDistro <- rbind(TempMasterDistro,Temp)
  rm(Temp)
}
# have we got more than nrow(HHS2) entries for any particular RequestedLine?
which(table(MasterDistro$RequestedLine)>nrow(HHS2))
# named integer(0)
which(!table(MasterDistro$RequestedLine)==nrow(HHS2))
# length is 7102
which(table(TempMasterDistro$RequestedLine)<nrow(HHS2))
#  388 9680 
#    1    2 
length(MissingPLs)*nrow(HHS2)==nrow(TempMasterDistro)
# False! let's just add these to the MasterDistro and we investigate further:
MasterDistro <- rbind(MasterDistro,TempMasterDistro)
rm(TempMasterDistro)
# check if there are any wrong PLs still:
WrongEntries <- which(!trimws(format(MasterDistro$povertyline,nsmall = 3))==
                      trimws(format(MasterDistro$RequestedLine, nsmall = 3)))
# this test goes OK!
UniqueReqPLs <- as.numeric(trimws(sort(unique(MasterDistro$RequestedLine))))
UniqueReqPLs <- as.numeric(format(UniqueReqPLs,nsmall = 3))
MissingPLs <- IdealPLs[which(!(round(IdealPLs,3) %in% round(UniqueReqPLs,3)))]
# so all lines appear in the data (but not sure yet if they appear for the correct
# number of times, which is nrow(HHS2))
# PCN returns 6503 unique HHS2, and I have a PL vector with length 15162
nrow(HHS2)*length(IdealPLs)
# 98598486
nrow(HHS2)*length(IdealPLs) == nrow(MasterDistro)
nrow(HHS2)*length(IdealPLs) - nrow(MasterDistro)
# 425703
# I am missing 425703 entries, now lets see which line is not complete:
ttt <- table(MasterDistro$RequestedLine)
ttt[ttt>nrow(HHS2)]
# integer(0)
ttt[ttt<nrow(HHS2)]
sum(nrow(HHS2)-ttt)
# 425703 # something went very wrong here... 

# so I know exactly what is missing by comparing the HHS2 with each PL from
MissingPLs <- as.numeric(names(ttt[ttt<nrow(HHS2)]))
# save.image("/media/michalis/1984/PovcalNetTemp4BB.RData")
# load("/media/michalis/1984/PovcalNetTemp4BB.RData")
rm(AllNewLines,AllNewLinesTemplate,cl,CorrectedLines,FaultyEntries,Distro,
   FaultyTemp,NewNotFound,NotFound,TempDistro,TempFaultyEntries)

##### Fetch entries missing from both Takes ####

ttt[ttt<nrow(HHS2)]
sort(ttt[ttt<nrow(HHS2)])
# too many to paste here; see above

HHS2$ISO3DataYearCovType <- paste0(HHS2$countrycode,":",HHS2$year,":",HHS2$datayear,
                                  ":",HHS2$coveragetype,":",ifelse(HHS2$datatype=="consumption",'c','i'))

for (i in MissingPLs[c(1:length(MissingPLs))]){
  print(paste0('-----',i,'------'))
  tempdf <- subset(MasterDistro,round(MasterDistro$RequestedLine,3)==round(i,3))
  tempdf$ISO3DataYearCovType <- paste0(tempdf$countrycode,":",tempdf$year,":",
                                       tempdf$datayear,":",tempdf$coveragetype,":",
                                       ifelse(tempdf$datatype=="consumption",'c','i'))
  tempID <- HHS2$ISO3DataYearCovType[which(!HHS2$ISO3DataYearCovType %in% tempdf$ISO3DataYearCovType)]
  print(length(tempID))
  if (!exists('MissingEntries')){
    MissingEntries <- data.frame(ID=tempID,PL=i,stringsAsFactors = F)
    print(length(tempID))
  } else {
    print(length(tempID)+nrow(MissingEntries))
    MissingEntries <- rbind(MissingEntries,data.frame(ID=tempID,PL=i,stringsAsFactors = F))
  }
  print(nrow(MissingEntries))
  rm(tempdf)
}

nrow(MissingEntries)==nrow(HHS2)*length(IdealPLs) - nrow(MasterDistro)
# not good but that's for later!
save(list = 'MissingEntries',file = paste0('/media/michalis/1984/PovcalNet/WithFills/MasterData/MissingEntries.RData'))
# save(list = 'MasterDistro',file = paste0('/media/michalis/1984/MasterDistro.RData'))
# rm(MasterDistro)

# let's fetch them from PCN
for (i in c(seq(100,length(MissingPLs)-100,100),length(MissingPLs))){
  no_cores <- 5
  cl <- makeCluster(no_cores, type="FORK")
  registerDoParallel(cl)
  if (i>7000){
    low_i <- i-103
  } else {
    low_i <- i-99
  }
  no_cores <- 6
  cl <- makeCluster(no_cores, type="FORK")
  registerDoParallel(cl)
  Distro <- foreach(jjj=MissingPLs[c(low_i:i)], 
                    #.combine='rbind', 
                    .errorhandling = "pass") %dopar% { 
                      
                      ttt <- 8
                      while (ttt>0){
                        Temp <- povcalnet(
                          country = "all",
                          povline = jjj,
                          year = "all",
                          aggregate = FALSE,
                          fill_gaps = T,
                          coverage = "all",
                          ppp = NULL,
                          url = "http://iresearch.worldbank.org",
                          format = "csv"
                        )
                        
                        WrongEntries <- which(!trimws(format(Temp$povertyline,nsmall = 3))==
                                              trimws(format(jjj, nsmall = 3)))
                        
                        if (length(WrongEntries)>0){
                          ttt <- ttt - 1
                        } else {
                          ttt <- 0
                        }
                      }
                      
                      # I added this extra column because in several instances
                      # the poverty line returned from a particular country
                      # is much different from the poverty line requested
                      # e.g. when asking PL of 1.009 I got a 0.2264779
                      # PL for Burundi in 1981
                      # in the same df I got year 19892Y and datayear 0.0163
                      # for Belarus see 
                      # "/media/michalis/1984/PovcalNet/Examples/Distro1100.RData" oh I just deleted it...
                      
                      Temp$RequestedLine <- jjj
                      
                      Temp$ISO3DataYearCovType <- paste0(Temp$countrycode,":",Temp$year,":",Temp$datayear,
                                                         ":",Temp$coveragetype,":",ifelse(Temp$datatype=="consumption",'c','i'))
                      
                      RequiredEntries <- unique(MissingEntries$ID[which(MissingEntries$PL==jjj)])
                      
                      Temp <- subset(Temp,Temp$ISO3DataYearCovType %in% RequiredEntries)
                      
                      return(Temp)
                    }
  stopCluster(cl)
  registerDoSEQ()
  save(list = 'Distro',file = paste0('/media/michalis/1984/PovcalNet/WithFillsMissing/Distro',formatC(i,width = 5, format = "d", flag = "0"),'.RData'))
  print(paste0('Saved file... ',paste0('/media/michalis/1984/PovcalNet/WithFillsMissing/Distro',formatC(i,width = 5, format = "d", flag = "0"),'.RData')))
  rm(Distro)
}

###### Integrity Check and Combine saved data ####

# let's get the data from World Bank's PovcalNet API:
#PCN <- povcalnet_info()
# PCN df is required to request all countries' info from PovcalNet:
#HHS <- povcalnet(country = PCN$country_code)
TempDistro <- povcalnetR::povcalnet_cl('USA',1,2010)
TempDistro$RequestedLine <- as.numeric(NA)
MasterDistroExtra <- subset(TempDistro,TempDistro$countrycode=='2398y9wfhehfsdih') # just maintain 
TempMasterDistro <- subset(TempDistro,TempDistro$countrycode=='2398y9wfhehfsdih') # just maintain 
# the data structure
FaultyEntries <- subset(TempDistro,TempDistro$countrycode=='2398y9wfhehfsdih') # just maintain 
# the data structure and add a comment column
FaultyEntries$Comments <- as.character(NA)
SavedDistrosFolder <- '/media/michalis/1984/PovcalNet/WithFillsMissing'
TheFiles <- list.files(SavedDistrosFolder,pattern = 'Distro')
#TheFiles <- TheFiles[c(34:42,44:53)]
TheWrongList <- rep(as.numeric(NA),length(IdealPLs))
names(TheWrongList) <- trimws(format(IdealPLs, nsmall = 3))

options(warn=2) # turn warnings to errors, for better debugging
tictoc::tic()

for (i in c(1:length(TheFiles))){
  #for (i in c(1)){
  # Load the saved data from the disk
  CurrentFile <- paste0(SavedDistrosFolder, '/',TheFiles[i])
  load(CurrentFile)
  print(CurrentFile)
  
  # First check: all list elements must have a fixed length of 33
  # equal to the number of columns returned by the PovcalNet API (31)
  # plus one extra column I add for control ("RequestedLine")
  # and one more ...
  # that stores the PL requested to the API.
  # Elements not complying are removed, and at the end of this process
  # we will have a reporting variable with all the PL values that
  # need to be requested again from the API
  
  if (!all(sapply(Distro, length)==33)){
    while (!all(sapply(Distro, length)==33)){
      # remove those that did not:
      Distro[[which(!(sapply(Distro, length)==33))[1]]] <- NULL
    }
    #print(paste0('Current number of fetched PLs', length(Distro),". Normally this must be 100."))
  } else {
    print('No entries with less than 33 columns to remove...')
  }
  
  # Second check: all entries from a particular list element (so within each list
  # element) must have Distro$RequestedLine == Distro$povertyline
  # those that do not are kept in a separate dataframe
  # plus other integrity checks in the loop below:
  
  for (j in c(1:length(Distro))){
    
    Temp <- Distro[[j]]
    Temp$ISO3DataYearCovType <- NULL
    NewFaultyEntries <- subset(FaultyEntries,FaultyEntries$countrycode=='498heo98h')
    
    # Rule 0: no line with all NA, and no line with 
    # countrycode == "CountryCode"
    # and no line with countryname=="DELETE"
    Temp <- subset(Temp,!Temp$countrycode=="CountryCode")
    Temp <- subset(Temp,!Temp$countryname=="DELETE")
    
    # Rule 0.5: all PLs must be identical to the one requested
    WrongEntries <- which(!trimws(format(Temp$povertyline,nsmall = 3))==
                          trimws(format(Temp$RequestedLine, nsmall = 3)))
    NonIdenticalLines <- length(WrongEntries)
    
    FaultyTemp <- Temp[WrongEntries,]
    FaultyTemp$Comments <- 'PL not identical to the one requested'
    Temp <- suppressMessages(dplyr::anti_join(x = Temp, y = FaultyTemp))
    NewFaultyEntries <- rbind(NewFaultyEntries,FaultyTemp)
    
    # Rule 1: all PPPs from one ISO3 must be the same
    # and matching the value from HHS
    for (k in sort(unique(Temp$countrycode))){
      WrongEntries <- which(!Temp$ppp[which(Temp$countrycode==k)]==unique(HHS2$ppp[which(HHS2$countrycode==k)]))
      if (length(WrongEntries)>0){
        FaultyTemp <- Temp[which(Temp$countrycode==k)[WrongEntries],]
        # remove that entry from the Temp dataframe
        Temp <- suppressMessages(dplyr::anti_join(x = Temp, y = FaultyTemp))
        FaultyTemp$Comments <- 'Wrong PPP value'
        NewFaultyEntries <- rbind(NewFaultyEntries,FaultyTemp)
        rm(FaultyTemp)
      }
      rm(WrongEntries)
    }
    
    # Rule 2: columns "year" "datayear" and from isinterpolated until 
    # "decile10" must be numeric or convertible to numeric without warnings
    # define which columns must be numeric:
    NumericColumns <- c("year","datayear", names(Temp)[c(8:31)])
    # get the columns that actually are numeric:
    nums <- unlist(lapply(Temp, is.numeric)) 
    # and extract those that are not, although they should:
    WronglyNonNumericColumns <- NumericColumns[which(!NumericColumns %in% names(Temp)[nums])]
    # across those find the non-numeric entries:
    for (wrongcols in c(WronglyNonNumericColumns)){
      WrongEntries <- suppressWarnings(which(is.na(as.numeric(unlist(Temp[,wrongcols])))))
      NA_entries <- which(is.na((unlist(Temp[,wrongcols]))))
      WrongEntries <- WrongEntries[which(!WrongEntries %in% NA_entries)]
      if (length(WrongEntries)>0){
        FaultyTemp <- Temp[WrongEntries,]
        # remove that entry from the Temp dataframe
        Temp <- suppressMessages(dplyr::anti_join(x = Temp, y = FaultyTemp))
        FaultyTemp$Comments <- paste0('Non-numeric value in column ', wrongcols)
        NewFaultyEntries <- rbind(NewFaultyEntries,FaultyTemp)
        rm(FaultyTemp)
      }
      rm(WrongEntries)
    }
    
    # Rule 3: in non-interpolated entries "year", "datayear" must be identical 
    # with their corresponding HHS entry
    #WrongEntries <- which(!(Temp$coveragetype %in% HHS$coveragetype))
    #if (length(WrongEntries)>0){
    #  stop('build the code for Rule 3')
    #}
    #rm(WrongEntries)
    
    # Rule 4: interpolated values must be between the benchmark values used 
    # in the interpolation
    #WrongEntries <- which(!(Temp$coveragetype %in% HHS$coveragetype))
    #if (length(WrongEntries)>0){
    #  stop('build the code for Rule 4')
    #}
    #rm(WrongEntries)
    
    # Rule 5: coverage type must be from the range included in HHS
    WrongEntries <- which(!(Temp$coveragetype %in% HHS$coveragetype))
    if (length(WrongEntries)>0){
      stop('build the code for Rule 5')
    }
    rm(WrongEntries)
    
    # Rule 6: apply the allowed values limits to the data using
    # https://rdrr.io/cran/userfriendlyscience/man/checkDataIntegrity.html
    # to be developed...
    
    # keeping a log over the distros with different PLs than requested:
    TheWrongList[which(names(TheWrongList)==
                       as.character(unique(trimws(format(NewFaultyEntries$RequestedLine, 
                                                         nsmall = 3)))))] <- NonIdenticalLines
    
    rm(NonIdenticalLines)
    FaultyEntries <- rbind(FaultyEntries,NewFaultyEntries)
    rm(NewFaultyEntries)
    
    TempMasterDistro <- rbind(TempMasterDistro,Temp)
    rm(Temp)
  }
  MasterDistroExtra <- rbind(MasterDistroExtra,TempMasterDistro)
  TempMasterDistro <- subset(TempDistro,TempDistro$countrycode=='2398y9wfhehfsdih') 
  rm(Distro)
  print('-------------------------------------')
}
options(warn=0) # restore to default from warn=2
tictoc::toc()

save(list = 'MasterDistroExtra',file = paste0('/media/michalis/1984/PovcalNet/WithFills/MasterData/DistroLastMissingPLs.RData'))
print(paste0('Saved file... ',paste0('/media/michalis/1984/PovcalNet/WithFills/MasterData/DistroLastMissingPLs.RData')))

# check that those are the entries I actually wanted!
load('/media/michalis/1984/PovcalNet/WithFills/MasterData/DistroLastMissingPLs.RData')
load('/media/michalis/1984/PovcalNet/WithFills/MasterData/MasterDistroB100-15162.RData')

# test before merge:
ttt <- table(MasterDistro$RequestedLine)
ttt[ttt>nrow(HHS2)]
#named integer(0)
nrow(HHS2)*length(IdealPLs)
# 98598486
nrow(MasterDistro)
# 98570675
nrow(HHS2)*length(IdealPLs)-nrow(MasterDistro)
# 27811
#lets see now if we have enough new entries:
nrow(MasterDistroExtra)==sum(ttt-nrow(HHS2))
# FALSE

#MasterDistro <- rbind(MasterDistro,MasterDistroExtra)
#rm(MasterDistroExtra)

ttt <- table(MasterDistro$RequestedLine)
ttt[ttt>nrow(HHS2)]
#named integer(0)
sum(nrow(HHS2)-sort(ttt[ttt<nrow(HHS2)]))
# 1799
TheMissingPLs <- sort(ttt[ttt<nrow(HHS2)])
# 1190.5  598.5  597.5    598  42.25  4.303 1205.5   1101   1393   6070   1460   6490   6980  55.02   6000   1051  14.23   6380   6480   44.7   9.83  14.24  14.82  107.7 
#      7     14    165    191   5942   6039   6180   6428   6428   6458   6479   6488   6491   6495   6495   6496   6499   6499   6499   6500   6501   6501   6501   6501 
# 1040   5880   6820   6910   90.1   1440   7080 
# 6501   6501   6501   6501   6502   6502   6502

# PLs that are totally missing:
TotallyMissingPLs <- IdealPLs[which(!IdealPLs %in% names(ttt))]
# 597.5  598.0  598.5 1190.5

# let's see if they are in the MasterDistroExtra
TotallyMissingPLs[which(TotallyMissingPLs %in% unique(MasterDistroExtra$RequestedLine))]
# 597.5  598.0  598.5 1190.5
# fantastic

NewEntries <- subset(MasterDistroExtra, round(MasterDistroExtra$RequestedLine,3) %in% round(TotallyMissingPLs,3))
# but not all of them are here...
# I need to fetch them again
rm(NewEntries)

##### Fetch the few lines ####
no_cores <- 4
cl <- makeCluster(no_cores, type="FORK")
registerDoParallel(cl)

Distro <- foreach(jjj=TotallyMissingPLs, 
                  #.combine='rbind', 
                  .errorhandling = "pass") %dopar% { 
                    
                    ttt <- 8
                    while (ttt>0){
                      Temp <- povcalnet(
                        country = "all",
                        povline = jjj,
                        year = "all",
                        aggregate = FALSE,
                        fill_gaps = T,
                        coverage = "all",
                        ppp = NULL,
                        url = "http://iresearch.worldbank.org",
                        format = "csv"
                      )
                      
                      WrongEntries <- which(!trimws(format(Temp$povertyline,nsmall = 3))==
                                            trimws(format(jjj, nsmall = 3)))
                      
                      if (length(WrongEntries)>0){
                        ttt <- ttt - 1
                      } else {
                        ttt <- 0
                      }
                    }
                    
                    # I added this extra column because in several instances
                    # the poverty line returned from a particular country
                    # is much different from the poverty line requested
                    # e.g. when asking PL of 1.009 I got a 0.2264779
                    # PL for Burundi in 1981
                    # in the same df I got year 19892Y and datayear 0.0163
                    # for Belarus see 
                    # "/media/michalis/1984/PovcalNet/Examples/Distro1100.RData" oh I just deleted it...
                    Temp$RequestedLine <- jjj
                    return(Temp)
                  }
stopCluster(cl)
registerDoSEQ()

TempDistro <- povcalnetR::povcalnet_cl('USA',1,2010)
TempDistro$RequestedLine <- as.numeric(NA)
TempMasterDistro <- subset(TempDistro,TempDistro$countrycode=='2398y9wfhehfsdih') # just maintain 
# the data structure
FaultyEntries <- subset(TempDistro,TempDistro$countrycode=='2398y9wfhehfsdih') # just maintain 
# the data structure and add a comment column
FaultyEntries$Comments <- as.character(NA)
#TheFiles <- TheFiles[c(34:42,44:53)]
TheWrongList <- rep(as.numeric(NA),length(IdealPLs))
names(TheWrongList) <- trimws(format(IdealPLs, nsmall = 3))

if (!all(sapply(Distro, length)==32)){
  while (!all(sapply(Distro, length)==32)){
    # remove those that did not:
    Distro[[which(!(sapply(Distro, length)==32))[1]]] <- NULL
  }
  print(paste0('Current number of fetched PLs', length(Distro),". Normally this must be 100."))
} else {
  print('No entries with less than 32 columns to remove...')
}

# Second check: all entries from a particular list element (so within each list
# element) must have Distro$RequestedLine == Distro$povertyline
# those that do not are kept in a separate dataframe
# plus other integrity checks in the loop below:

for (j in c(1:length(Distro))){
  
  Temp <- Distro[[j]]
  NewFaultyEntries <- subset(FaultyEntries,FaultyEntries$countrycode=='498heo98h')
  
  # Rule 0: no line with all NA, and no line with 
  # countrycode == "CountryCode"
  # and no line with countryname=="DELETE"
  Temp <- subset(Temp,!Temp$countrycode=="CountryCode")
  Temp <- subset(Temp,!Temp$countryname=="DELETE")
  
  # Rule 0.5: all PLs must be identical to the one requested
  WrongEntries <- which(!trimws(format(Temp$povertyline,nsmall = 3))==
                        trimws(format(Temp$RequestedLine, nsmall = 3)))
  NonIdenticalLines <- length(WrongEntries)
  
  FaultyTemp <- Temp[WrongEntries,]
  FaultyTemp$Comments <- 'PL not identical to the one requested'
  Temp <- suppressMessages(dplyr::anti_join(x = Temp, y = FaultyTemp))
  NewFaultyEntries <- rbind(NewFaultyEntries,FaultyTemp)
  
  # Rule 1: all PPPs from one ISO3 must be the same
  # and matching the value from HHS2
  for (k in sort(unique(Temp$countrycode))){
    WrongEntries <- which(!Temp$ppp[which(Temp$countrycode==k)]==unique(HHS2$ppp[which(HHS2$countrycode==k)]))
    if (length(WrongEntries)>0){
      FaultyTemp <- Temp[which(Temp$countrycode==k)[WrongEntries],]
      # remove that entry from the Temp dataframe
      Temp <- suppressMessages(dplyr::anti_join(x = Temp, y = FaultyTemp))
      FaultyTemp$Comments <- 'Wrong PPP value'
      NewFaultyEntries <- rbind(NewFaultyEntries,FaultyTemp)
      rm(FaultyTemp)
    }
    rm(WrongEntries)
  }
  
  # Rule 2: columns "year" "datayear" and from isinterpolated until 
  # "decile10" must be numeric or convertible to numeric without warnings
  # define which columns must be numeric:
  NumericColumns <- c("year","datayear", names(Temp)[c(8:31)])
  # get the columns that actually are numeric:
  nums <- unlist(lapply(Temp, is.numeric)) 
  # and extract those that are not, although they should:
  WronglyNonNumericColumns <- NumericColumns[which(!NumericColumns %in% names(Temp)[nums])]
  # across those find the non-numeric entries:
  for (wrongcols in c(WronglyNonNumericColumns)){
    WrongEntries <- suppressWarnings(which(is.na(as.numeric(unlist(Temp[,wrongcols])))))
    NA_entries <- which(is.na((unlist(Temp[,wrongcols]))))
    WrongEntries <- WrongEntries[which(!WrongEntries %in% NA_entries)]
    if (length(WrongEntries)>0){
      FaultyTemp <- Temp[WrongEntries,]
      # remove that entry from the Temp dataframe
      Temp <- suppressMessages(dplyr::anti_join(x = Temp, y = FaultyTemp))
      FaultyTemp$Comments <- paste0('Non-numeric value in column ', wrongcols)
      NewFaultyEntries <- rbind(NewFaultyEntries,FaultyTemp)
      rm(FaultyTemp)
    }
    rm(WrongEntries)
  }
  
  # Rule 3: in non-interpolated entries "year", "datayear" must be identical 
  # with their corresponding HHS2 entry
  #WrongEntries <- which(!(Temp$coveragetype %in% HHS2$coveragetype))
  #if (length(WrongEntries)>0){
  #  stop('build the code for Rule 3')
  #}
  #rm(WrongEntries)
  
  # Rule 4: interpolated values must be between the benchmark values used 
  # in the interpolation
  #WrongEntries <- which(!(Temp$coveragetype %in% HHS2$coveragetype))
  #if (length(WrongEntries)>0){
  #  stop('build the code for Rule 4')
  #}
  #rm(WrongEntries)
  
  # Rule 5: coverage type must be from the range included in HHS2
  WrongEntries <- which(!(Temp$coveragetype %in% HHS2$coveragetype))
  if (length(WrongEntries)>0){
    stop('build the code for Rule 5')
  }
  rm(WrongEntries)
  
  # Rule 6: apply the allowed values limits to the data using
  # https://rdrr.io/cran/userfriendlyscience/man/checkDataIntegrity.html
  # to be developed...
  
  # keeping a log over the distros with different PLs than requested:
  TheWrongList[which(names(TheWrongList)==
                     as.character(unique(trimws(format(NewFaultyEntries$RequestedLine, 
                                                       nsmall = 3)))))] <- NonIdenticalLines
  
  rm(NonIdenticalLines)
  FaultyEntries <- rbind(FaultyEntries,NewFaultyEntries)
  rm(NewFaultyEntries)
  
  TempMasterDistro <- rbind(TempMasterDistro,Temp)
  rm(Temp)
}

# Now I need to check which are the duplicates and which are actually missing
# from the MasterDistro

nrow(HHS2)*length(IdealPLs)-nrow(MasterDistro)
# 27811
sum(nrow(HHS2)-sort(ttt[ttt<nrow(HHS2)]))
# 1799
nrow(TempMasterDistro)
# 26012
nrow(HHS2)*length(IdealPLs)-nrow(MasterDistro) ==
  sum(nrow(HHS2)-sort(ttt[ttt<nrow(HHS2)])) + nrow(TempMasterDistro)
# TRUE!!!!

MasterDistro <- rbind(MasterDistro,TempMasterDistro)

ttt <- table(MasterDistro$RequestedLine)
ttt[ttt>nrow(HHS2)]
#named integer(0)
sum(nrow(HHS2)-sort(ttt[ttt<nrow(HHS2)]))
# 1799
TheMissingPLs <- sort(ttt[ttt<nrow(HHS2)])

##### Fetch another few lines ####
no_cores <- 8
cl <- makeCluster(no_cores, type="FORK")
registerDoParallel(cl)

Distro <- foreach(jjj=round(as.numeric(names(TheMissingPLs)),3), 
                  #.combine='rbind', 
                  .errorhandling = "pass") %dopar% { 
                    
                    ttt <- 8
                    while (ttt>0){
                      Temp <- povcalnet(
                        country = "all",
                        povline = jjj,
                        year = "all",
                        aggregate = FALSE,
                        fill_gaps = T,
                        coverage = "all",
                        ppp = NULL,
                        url = "http://iresearch.worldbank.org",
                        format = "csv"
                      )
                      
                      WrongEntries <- which(!trimws(format(Temp$povertyline,nsmall = 3))==
                                            trimws(format(jjj, nsmall = 3)))
                      
                      if (length(WrongEntries)>0){
                        ttt <- ttt - 1
                      } else {
                        ttt <- 0
                      }
                    }
                    
                    # I added this extra column because in several instances
                    # the poverty line returned from a particular country
                    # is much different from the poverty line requested
                    # e.g. when asking PL of 1.009 I got a 0.2264779
                    # PL for Burundi in 1981
                    # in the same df I got year 19892Y and datayear 0.0163
                    # for Belarus see 
                    # "/media/michalis/1984/PovcalNet/Examples/Distro1100.RData" oh I just deleted it...
                    Temp$RequestedLine <- jjj
                    return(Temp)
                  }
stopCluster(cl)
registerDoSEQ()

TempDistro <- povcalnetR::povcalnet_cl('USA',1,2010)
TempDistro$RequestedLine <- as.numeric(NA)
TempMasterDistro <- subset(TempDistro,TempDistro$countrycode=='2398y9wfhehfsdih') # just maintain 
# the data structure
FaultyEntries <- subset(TempDistro,TempDistro$countrycode=='2398y9wfhehfsdih') # just maintain 
# the data structure and add a comment column
FaultyEntries$Comments <- as.character(NA)
#TheFiles <- TheFiles[c(34:42,44:53)]
TheWrongList <- rep(as.numeric(NA),length(IdealPLs))
names(TheWrongList) <- trimws(format(IdealPLs, nsmall = 3))

if (!all(sapply(Distro, length)==32)){
  while (!all(sapply(Distro, length)==32)){
    # remove those that did not:
    Distro[[which(!(sapply(Distro, length)==32))[1]]] <- NULL
  }
  print(paste0('Current number of fetched PLs', length(Distro),". Normally this must be 100."))
} else {
  print('No entries with less than 32 columns to remove...')
}

# Second check: all entries from a particular list element (so within each list
# element) must have Distro$RequestedLine == Distro$povertyline
# those that do not are kept in a separate dataframe
# plus other integrity checks in the loop below:

for (j in c(1:length(Distro))){
  
  Temp <- Distro[[j]]
  NewFaultyEntries <- subset(FaultyEntries,FaultyEntries$countrycode=='498heo98h')
  
  # Rule 0: no line with all NA, and no line with 
  # countrycode == "CountryCode"
  # and no line with countryname=="DELETE"
  Temp <- subset(Temp,!Temp$countrycode=="CountryCode")
  Temp <- subset(Temp,!Temp$countryname=="DELETE")
  
  # Rule 0.5: all PLs must be identical to the one requested
  WrongEntries <- which(!trimws(format(Temp$povertyline,nsmall = 3))==
                        trimws(format(Temp$RequestedLine, nsmall = 3)))
  NonIdenticalLines <- length(WrongEntries)
  
  FaultyTemp <- Temp[WrongEntries,]
  FaultyTemp$Comments <- 'PL not identical to the one requested'
  Temp <- suppressMessages(dplyr::anti_join(x = Temp, y = FaultyTemp))
  NewFaultyEntries <- rbind(NewFaultyEntries,FaultyTemp)
  
  # Rule 1: all PPPs from one ISO3 must be the same
  # and matching the value from HHS2
  for (k in sort(unique(Temp$countrycode))){
    WrongEntries <- which(!Temp$ppp[which(Temp$countrycode==k)]==unique(HHS2$ppp[which(HHS2$countrycode==k)]))
    if (length(WrongEntries)>0){
      FaultyTemp <- Temp[which(Temp$countrycode==k)[WrongEntries],]
      # remove that entry from the Temp dataframe
      Temp <- suppressMessages(dplyr::anti_join(x = Temp, y = FaultyTemp))
      FaultyTemp$Comments <- 'Wrong PPP value'
      NewFaultyEntries <- rbind(NewFaultyEntries,FaultyTemp)
      rm(FaultyTemp)
    }
    rm(WrongEntries)
  }
  
  # Rule 2: columns "year" "datayear" and from isinterpolated until 
  # "decile10" must be numeric or convertible to numeric without warnings
  # define which columns must be numeric:
  NumericColumns <- c("year","datayear", names(Temp)[c(8:31)])
  # get the columns that actually are numeric:
  nums <- unlist(lapply(Temp, is.numeric)) 
  # and extract those that are not, although they should:
  WronglyNonNumericColumns <- NumericColumns[which(!NumericColumns %in% names(Temp)[nums])]
  # across those find the non-numeric entries:
  for (wrongcols in c(WronglyNonNumericColumns)){
    WrongEntries <- suppressWarnings(which(is.na(as.numeric(unlist(Temp[,wrongcols])))))
    NA_entries <- which(is.na((unlist(Temp[,wrongcols]))))
    WrongEntries <- WrongEntries[which(!WrongEntries %in% NA_entries)]
    if (length(WrongEntries)>0){
      FaultyTemp <- Temp[WrongEntries,]
      # remove that entry from the Temp dataframe
      Temp <- suppressMessages(dplyr::anti_join(x = Temp, y = FaultyTemp))
      FaultyTemp$Comments <- paste0('Non-numeric value in column ', wrongcols)
      NewFaultyEntries <- rbind(NewFaultyEntries,FaultyTemp)
      rm(FaultyTemp)
    }
    rm(WrongEntries)
  }
  
  # Rule 3: in non-interpolated entries "year", "datayear" must be identical 
  # with their corresponding HHS2 entry
  #WrongEntries <- which(!(Temp$coveragetype %in% HHS2$coveragetype))
  #if (length(WrongEntries)>0){
  #  stop('build the code for Rule 3')
  #}
  #rm(WrongEntries)
  
  # Rule 4: interpolated values must be between the benchmark values used 
  # in the interpolation
  #WrongEntries <- which(!(Temp$coveragetype %in% HHS2$coveragetype))
  #if (length(WrongEntries)>0){
  #  stop('build the code for Rule 4')
  #}
  #rm(WrongEntries)
  
  # Rule 5: coverage type must be from the range included in HHS2
  WrongEntries <- which(!(Temp$coveragetype %in% HHS2$coveragetype))
  if (length(WrongEntries)>0){
    stop('build the code for Rule 5')
  }
  rm(WrongEntries)
  
  # Rule 6: apply the allowed values limits to the data using
  # https://rdrr.io/cran/userfriendlyscience/man/checkDataIntegrity.html
  # to be developed...
  
  # keeping a log over the distros with different PLs than requested:
  TheWrongList[which(names(TheWrongList)==
                     as.character(unique(trimws(format(NewFaultyEntries$RequestedLine, 
                                                       nsmall = 3)))))] <- NonIdenticalLines
  
  rm(NonIdenticalLines)
  FaultyEntries <- rbind(FaultyEntries,NewFaultyEntries)
  rm(NewFaultyEntries)
  
  TempMasterDistro <- rbind(TempMasterDistro,Temp)
  rm(Temp)
}

# Now I need to check which are the duplicates and which are actually missing
# from the MasterDistro
nrow(TempMasterDistro)==nrow(HHS2)*length(TheMissingPLs)
# not exactly, but almost 260082 =/= 260120
MasterDistro <- subset(MasterDistro,!round(MasterDistro$RequestedLine,3) %in% 
                       unique(round(TempMasterDistro$RequestedLine,3)))
nrow(MasterDistro)
# 98338366
MasterDistro <- rbind(MasterDistro,TempMasterDistro)
nrow(MasterDistro)
# 98598448
nrow(HHS2)*length(IdealPLs)
# 98598486
nrow(HHS2)*length(IdealPLs)-nrow(MasterDistro)

ttt <- table(MasterDistro$RequestedLine)
ttt[ttt>nrow(HHS2)]
#named integer(0)
sum(nrow(HHS2)-sort(ttt[ttt<nrow(HHS2)]))
# 38
TheMissingPLs <- sort(ttt[ttt<nrow(HHS2)])
TotallyMissingPLs <- round(as.numeric(names(TheMissingPLs)),3)

##### Fetch more lines ####

no_cores <- 2
cl <- makeCluster(no_cores, type="FORK")
registerDoParallel(cl)

Distro <- foreach(jjj=TotallyMissingPLs, 
                  #.combine='rbind', 
                  .errorhandling = "pass") %dopar% { 
                    
                    ttt <- 8
                    while (ttt>0){
                      Temp <- povcalnet(
                        country = "all",
                        povline = jjj,
                        year = "all",
                        aggregate = FALSE,
                        fill_gaps = T,
                        coverage = "all",
                        ppp = NULL,
                        url = "http://iresearch.worldbank.org",
                        format = "csv"
                      )
                      
                      WrongEntries <- which(!trimws(format(Temp$povertyline,nsmall = 3))==
                                            trimws(format(jjj, nsmall = 3)))
                      
                      if (length(WrongEntries)>0){
                        ttt <- ttt - 1
                      } else {
                        ttt <- 0
                      }
                    }
                    
                    # I added this extra column because in several instances
                    # the poverty line returned from a particular country
                    # is much different from the poverty line requested
                    # e.g. when asking PL of 1.009 I got a 0.2264779
                    # PL for Burundi in 1981
                    # in the same df I got year 19892Y and datayear 0.0163
                    # for Belarus see 
                    # "/media/michalis/1984/PovcalNet/Examples/Distro1100.RData" oh I just deleted it...
                    Temp$RequestedLine <- jjj
                    return(Temp)
                  }
stopCluster(cl)
registerDoSEQ()

TempDistro <- povcalnetR::povcalnet_cl('USA',1,2010)
TempDistro$RequestedLine <- as.numeric(NA)
TempMasterDistro <- subset(TempDistro,TempDistro$countrycode=='2398y9wfhehfsdih') # just maintain 
# the data structure
FaultyEntries <- subset(TempDistro,TempDistro$countrycode=='2398y9wfhehfsdih') # just maintain 
# the data structure and add a comment column
FaultyEntries$Comments <- as.character(NA)
#TheFiles <- TheFiles[c(34:42,44:53)]
TheWrongList <- rep(as.numeric(NA),length(IdealPLs))
names(TheWrongList) <- trimws(format(IdealPLs, nsmall = 3))

if (!all(sapply(Distro, length)==32)){
  while (!all(sapply(Distro, length)==32)){
    # remove those that did not:
    Distro[[which(!(sapply(Distro, length)==32))[1]]] <- NULL
  }
  print(paste0('Current number of fetched PLs', length(Distro),". Normally this must be 100."))
} else {
  print('No entries with less than 32 columns to remove...')
}

# Second check: all entries from a particular list element (so within each list
# element) must have Distro$RequestedLine == Distro$povertyline
# those that do not are kept in a separate dataframe
# plus other integrity checks in the loop below:

for (j in c(1:length(Distro))){
  
  Temp <- Distro[[j]]
  NewFaultyEntries <- subset(FaultyEntries,FaultyEntries$countrycode=='498heo98h')
  
  # Rule 0: no line with all NA, and no line with 
  # countrycode == "CountryCode"
  # and no line with countryname=="DELETE"
  Temp <- subset(Temp,!Temp$countrycode=="CountryCode")
  Temp <- subset(Temp,!Temp$countryname=="DELETE")
  
  # Rule 0.5: all PLs must be identical to the one requested
  WrongEntries <- which(!trimws(format(Temp$povertyline,nsmall = 3))==
                        trimws(format(Temp$RequestedLine, nsmall = 3)))
  NonIdenticalLines <- length(WrongEntries)
  
  FaultyTemp <- Temp[WrongEntries,]
  FaultyTemp$Comments <- 'PL not identical to the one requested'
  Temp <- suppressMessages(dplyr::anti_join(x = Temp, y = FaultyTemp))
  NewFaultyEntries <- rbind(NewFaultyEntries,FaultyTemp)
  
  # Rule 1: all PPPs from one ISO3 must be the same
  # and matching the value from HHS2
  for (k in sort(unique(Temp$countrycode))){
    WrongEntries <- which(!Temp$ppp[which(Temp$countrycode==k)]==unique(HHS2$ppp[which(HHS2$countrycode==k)]))
    if (length(WrongEntries)>0){
      FaultyTemp <- Temp[which(Temp$countrycode==k)[WrongEntries],]
      # remove that entry from the Temp dataframe
      Temp <- suppressMessages(dplyr::anti_join(x = Temp, y = FaultyTemp))
      FaultyTemp$Comments <- 'Wrong PPP value'
      NewFaultyEntries <- rbind(NewFaultyEntries,FaultyTemp)
      rm(FaultyTemp)
    }
    rm(WrongEntries)
  }
  
  # Rule 2: columns "year" "datayear" and from isinterpolated until 
  # "decile10" must be numeric or convertible to numeric without warnings
  # define which columns must be numeric:
  NumericColumns <- c("year","datayear", names(Temp)[c(8:31)])
  # get the columns that actually are numeric:
  nums <- unlist(lapply(Temp, is.numeric)) 
  # and extract those that are not, although they should:
  WronglyNonNumericColumns <- NumericColumns[which(!NumericColumns %in% names(Temp)[nums])]
  # across those find the non-numeric entries:
  for (wrongcols in c(WronglyNonNumericColumns)){
    WrongEntries <- suppressWarnings(which(is.na(as.numeric(unlist(Temp[,wrongcols])))))
    NA_entries <- which(is.na((unlist(Temp[,wrongcols]))))
    WrongEntries <- WrongEntries[which(!WrongEntries %in% NA_entries)]
    if (length(WrongEntries)>0){
      FaultyTemp <- Temp[WrongEntries,]
      # remove that entry from the Temp dataframe
      Temp <- suppressMessages(dplyr::anti_join(x = Temp, y = FaultyTemp))
      FaultyTemp$Comments <- paste0('Non-numeric value in column ', wrongcols)
      NewFaultyEntries <- rbind(NewFaultyEntries,FaultyTemp)
      rm(FaultyTemp)
    }
    rm(WrongEntries)
  }
  
  # Rule 3: in non-interpolated entries "year", "datayear" must be identical 
  # with their corresponding HHS2 entry
  #WrongEntries <- which(!(Temp$coveragetype %in% HHS2$coveragetype))
  #if (length(WrongEntries)>0){
  #  stop('build the code for Rule 3')
  #}
  #rm(WrongEntries)
  
  # Rule 4: interpolated values must be between the benchmark values used 
  # in the interpolation
  #WrongEntries <- which(!(Temp$coveragetype %in% HHS2$coveragetype))
  #if (length(WrongEntries)>0){
  #  stop('build the code for Rule 4')
  #}
  #rm(WrongEntries)
  
  # Rule 5: coverage type must be from the range included in HHS2
  WrongEntries <- which(!(Temp$coveragetype %in% HHS2$coveragetype))
  if (length(WrongEntries)>0){
    stop('build the code for Rule 5')
  }
  rm(WrongEntries)
  
  # Rule 6: apply the allowed values limits to the data using
  # https://rdrr.io/cran/userfriendlyscience/man/checkDataIntegrity.html
  # to be developed...
  
  # keeping a log over the distros with different PLs than requested:
  TheWrongList[which(names(TheWrongList)==
                     as.character(unique(trimws(format(NewFaultyEntries$RequestedLine, 
                                                       nsmall = 3)))))] <- NonIdenticalLines
  
  rm(NonIdenticalLines)
  FaultyEntries <- rbind(FaultyEntries,NewFaultyEntries)
  rm(NewFaultyEntries)
  
  TempMasterDistro <- rbind(TempMasterDistro,Temp)
  rm(Temp)
}

# Now I need to check which are the duplicates and which are actually missing
# from the MasterDistro

nrow(TempMasterDistro)==nrow(HHS2)*length(TheMissingPLs)
# YES!!!
MasterDistro <- subset(MasterDistro,!round(MasterDistro$RequestedLine,3) %in% 
                       unique(round(TempMasterDistro$RequestedLine,3)))
nrow(MasterDistro)
# 98585480
MasterDistro <- rbind(MasterDistro,TempMasterDistro)
nrow(MasterDistro)
# 98598486
nrow(HHS2)*length(IdealPLs)
# 98598486
nrow(HHS2)*length(IdealPLs)-nrow(MasterDistro)
# 0 YES!!!
rm(MasterDistroExtra,cl,FaultyEntries,FaultyTemp,TempDistro,pb,TempMasterDistro,Distro)
rm(tempdf)

#save.image("/media/michalis/1984/PovcalNetTempLast.RData")

##### Last check(s) ####
# do all RequestedPLs have a unique set of entries of length equal to HHS?

MasterDistro$ISO3DataYearCovType <- paste0(MasterDistro$countrycode,":",MasterDistro$year,":",
                                           MasterDistro$datayear,":",MasterDistro$coveragetype,":",
                                           ifelse(MasterDistro$datatype=="consumption",'c','i'))
DistroPerUniqueHHS2 <- table(MasterDistro$ISO3DataYearCovType)

MasterDistro$ISO3DataYearCovTypePL <- paste0(MasterDistro$countrycode,":",MasterDistro$year,":",
                                           MasterDistro$datayear,":",MasterDistro$coveragetype,":",
                                           ifelse(MasterDistro$datatype=="consumption",'c','i'),
                                           MasterDistro$povertyline)
UniqueISO3DataYearCovTypePL <- length(unique(MasterDistro$ISO3DataYearCovTypePL))
# are all rows unique?
UniqueISO3DataYearCovTypePL==nrow(MasterDistro)
# YES!!!
# do all requested lines have resulted to an equal poverty line?
all(round(MasterDistro$povertyline,3)==round(MasterDistro$RequestedLine,3))
# YES!!!
# do all PLs have proper length?
DistrosPerPL <- table(MasterDistro$povertyline)
all(DistrosPerPL==nrow(HHS2))
# DONE!!! DONE!!! DONE!!! DONE!!! DONE!!!

#### EXPORT WithFills ####

# save(list = 'MasterDistro',file = paste0('/media/michalis/1984/PovcalNet/MasterData/MasterDistroWithFills.RData'))
# save.image("/media/michalis/1984/PovcalNetWithFillsFinal.RData") 
# load("/media/michalis/1984/PovcalNetWithFillsFinal.RData")
# load('/media/michalis/1984/PovcalNet/MasterData/MasterDistroWithFills.RData')

##### Split and ReSlice per unique HHS ####
### ReSlice means only keep observations up to 100% only
### and also test for monotonicity

# in order to do this faster I will do that in two takes
# one first half of the ISO3s
# and then the other half

AllISO3s <- sort(unique(MasterDistro$countrycode))
PartA <- AllISO3s[c(1:82)]
PartB <- AllISO3s[c(83:length(AllISO3s))]

MasterDistro <- subset(MasterDistro,MasterDistro$countrycode %in% PartA)
gc()

PartialDistributions <- c()
SurvivingPLs <- c()
ContainsNAs <- c()

# after this one there is an error
which(sort(unique(MasterDistro$ISO3DataYearCovType))=='IND:2018:2011.5:A:c')
# 2759
# all its headcount entries are NA

for (i in sort(unique(MasterDistro$ISO3DataYearCovType))){
  DistroPerHHS <- subset(MasterDistro,MasterDistro$ISO3DataYearCovType==i)
  
  ContainsNAs <- c(ContainsNAs,sum(is.na(DistroPerHHS$headcount)))
  names(ContainsNAs)[length(ContainsNAs)] <- i
  
  j <- gsub(":","_",i)
  write.csv2(DistroPerHHS,paste0('/media/michalis/1984/PovcalNet/WithFills/SplitPerHHS/',j,'.csv'))
  
  # and my last (redundant) test for completeness:
  if (!length(unique(DistroPerHHS$RequestedLine))==length(IdealPLs)){
    print(paste0("Fail at ",DistroPerHHS$ISO3DataYearCovType))
  }
  
  # I need to go through each and only keep the poverty lines
  # that bring about a change in the headcount
  
  DistroPerHHS <- DistroPerHHS[ order(DistroPerHHS[,'povertyline']), ]
  DistroPerHHS$Diffs <- c(1,diff(DistroPerHHS$headcount))
  
  # and test monotonicity of the headcount values
  if (any(DistroPerHHS$Diffs<0)){
    stop('monotonicity alert')
  }
  
  # this was misplaced above the monotonicity test
  # so the test was irrelevant at that point...
  DistroPerHHS <- subset(DistroPerHHS,DistroPerHHS$Diffs>0)
  
  if (sum(is.na(DistroPerHHS$headcount))==nrow(DistroPerHHS)){
    # do nothing 
  } else if (max(DistroPerHHS$headcount)[1]<1){
    print(paste0(i,':partial distribution up to:',max(DistroPerHHS$headcount)[1]))
    PartialDistributions <- c(PartialDistributions,paste0(i,j))
  }
  
  DistroPerHHS$Diffs <- NULL
  
  SurvivingPLs <- c(SurvivingPLs,DistroPerHHS$RequestedLine)
  SurvivingPLs <- unique(SurvivingPLs)
  
  j <- gsub(":","_",i)
  write.csv2(DistroPerHHS,paste0('/media/michalis/1984/PovcalNet/WithFills/SplitPerHHSMinimal/',j,'.csv'))
  rm(DistroPerHHS)
  #gc()
}
#rm(i)

load('/media/michalis/1984/PovcalNet/MasterData/MasterDistroWithFills.RData')
MasterDistro <- subset(MasterDistro,MasterDistro$countrycode %in% PartB)
gc()

for (i in sort(unique(MasterDistro$ISO3DataYearCovType))){
  DistroPerHHS <- subset(MasterDistro,MasterDistro$ISO3DataYearCovType==i)
  
  ContainsNAs <- c(ContainsNAs,sum(is.na(DistroPerHHS$headcount)))
  names(ContainsNAs)[length(ContainsNAs)] <- i
  
  j <- gsub(":","_",i)
  write.csv2(DistroPerHHS,paste0('/media/michalis/1984/PovcalNet/WithFills/SplitPerHHS/',j,'.csv'))
  
  # and my last (redundant) test for completeness:
  if (!length(unique(DistroPerHHS$RequestedLine))==length(IdealPLs)){
    print(paste0("Fail at ",DistroPerHHS$ISO3DataYearCovType))
  }
  
  # I need to go through each and only keep the poverty lines
  # that bring about a change in the headcount
  
  DistroPerHHS <- DistroPerHHS[ order(DistroPerHHS[,'povertyline']), ]
  DistroPerHHS$Diffs <- c(1,diff(DistroPerHHS$headcount))
  
  # and test monotonicity of the headcount values
  if (any(DistroPerHHS$Diffs<0)){
    stop('monotonicity alert')
  }
  
  # this was misplaced above the monotonicity test
  # so the test was irrelevant at that point...
  DistroPerHHS <- subset(DistroPerHHS,DistroPerHHS$Diffs>0)
  
  if (sum(is.na(DistroPerHHS$headcount))==nrow(DistroPerHHS)){
    # do nothing
  } else if (max(DistroPerHHS$headcount)[1]<1){
    print(paste0(i,':partial distribution up to:',max(DistroPerHHS$headcount)[1]))
    PartialDistributions <- c(PartialDistributions,paste0(i,j))
  }
  
  DistroPerHHS$Diffs <- NULL
  
  SurvivingPLs <- c(SurvivingPLs,DistroPerHHS$RequestedLine)
  SurvivingPLs <- unique(SurvivingPLs)
  
  j <- gsub(":","_",i)
  write.csv2(DistroPerHHS,paste0('/media/michalis/1984/PovcalNet/WithFills/SplitPerHHSMinimal/',j,'.csv'))
  rm(DistroPerHHS)
  #gc()
}
#rm(i)

#AllPartialDistributions <- PartialDistributions
#AllSurvivingPLs <- SurvivingPLs
# load('/media/michalis/1984/PovcalNet/MasterData/MasterDistroWithFills.RData')
# save.image("/media/michalis/1984/PovcalNetWithFillsFinal.RData") 

# based on the density of the surviving observations I can update the IdealPLs list to:

# save.image("/media/michalis/1984/PovcalNetTemp7.RData") I haven't saved this...
# load("/media/michalis/1984/PovcalNetTemp7.RData")

#### Missing Statistics ####
# Many data points – for Gini, Mean, decile shares – are missing (i.e. even 
# where the platform will return a result for any given headcount ratio, 
# certain summary statistics are withheld).

#### Summary Statistics ####
# Some key summary variables of interest are not provided 
# (e.g. the threshold income marking the top or bottom decile etc.)

#### Global/Regional Data ####
# need to fetch the global and regional data from all those years as well

#### Data structure ####
# poverty data 
# Entity,Year,$1.90 per day - share of population below poverty line,
# $1.90 per day - poverty gap index,$1.90 per day - total number of people below poverty line,
# $1.90 per day - absolute poverty gap,$3.20 per day - share of population below poverty line,
# $3.20 per day - poverty gap index,$3.20 per day - total number of people below poverty line,
# $3.20 per day - absolute poverty gap,$5.50 per day - share of population below poverty line,
# $5.50 per day - poverty gap index,$5.50 per day - total number of people below poverty line,$5.50 per day - absolute poverty gap,$10.00 per day - share of population below poverty line,$10.00 per day - poverty gap index,$10.00 per day - total number of people below poverty line,$10.00 per day - absolute poverty gap,$15.00 per day - share of population below poverty line,$15.00 per day - poverty gap index,$15.00 per day - total number of people below poverty line,$15.00 per day - absolute poverty gap,$20.00 per day - share of population below poverty line,$20.00 per day - poverty gap index,$20.00 per day - total number of people below poverty line,$20.00 per day - absolute poverty gap,$30.00 per day - share of population below poverty line,$30.00 per day - poverty gap index,$30.00 per day - total number of people below poverty line,$30.00 per day - absolute poverty gap,40% of median income - share of population below poverty line,40% of median income - poverty gap index,40% of median income - total number of people below poverty line,40% of median income - absolute poverty gap,50% of median income - share of population below poverty line,50% of median income - poverty gap index,50% of median income - total number of people below poverty line,50% of median income - absolute poverty gap,60% of median income - share of population below poverty line,60% of median income - poverty gap index,60% of median income - total number of people below poverty line,60% of median income - absolute poverty gap,10th percentile – level of income or consumption per day,20th percentile – level of income or consumption per day,30th percentile – level of income or consumption per day,40th percentile – level of income or consumption per day,50th percentile (median) – level of income or consumption per day,60th percentile – level of income or consumption per day,70th percentile – level of income or consumption per day,80th percentile – level of income or consumption per day,90th percentile – level of income or consumption per day,Decile 1 – share of income or consumption,Decile 2 – share of income or consumption,Decile 3 – share of income or consumption,Decile 4 – share of income or consumption,Decile 5 – share of income or consumption,Decile 6 – share of income or consumption,Decile 7 – share of income or consumption,Decile 8 – share of income or consumption,Decile 9 – share of income or consumption,Decile 10 – share of income or consumption,Mean income or consumption per day,Gini index,P90:P10,P90:P50,Welfare measure,Survey year,Population,Decile 1 – average income or consumption,Decile 2 – average income or consumption,Decile 3 – average income or consumption,Decile 4 – average income or consumption,Decile 5 – average income or consumption,Decile 6 – average income or consumption,Decile 7 – average income or consumption,Decile 8 – average income or consumption,Decile 9 – average income or consumption,Decile 10 – average income or consumption,$1.00 per day - share of population below poverty line,$1.00 per day - poverty gap index,$1.00 per day - total number of people below poverty line,$1.00 per day - absolute poverty gap


# distribution:
# CountryName,RequestYear,P0.0,P0.1,P0.2,P0.3,P0.4,P0.5,P0.6,P0.7,P0.8,P0.9,P1.0,P1.1,P1.2,P1.3,P1.4,P1.5,P1.6,P1.7,P1.8,P1.9,P2.0,P2.1,P2.2,P2.3,P2.4,P2.5,P2.6,P2.7,P2.8,P2.9,P3.0,P3.1,P3.2,P3.3,P3.4,P3.5,P3.6,P3.7,P3.8,P3.9,P4.0,P4.1,P4.2,P4.3,P4.4,P4.5,P4.6,P4.7,P4.8,P4.9,P5.0,P5.1,P5.2,P5.3,P5.4,P5.5,P5.6,P5.7,P5.8,P5.9,P6.0,P6.1,P6.2,P6.3,P6.4,P6.5,P6.6,P6.7,P6.8,P6.9,P7.0,P7.1,P7.2,P7.3,P7.4,P7.5,P7.6,P7.7,P7.8,P7.9,P8.0,P8.1,P8.2,P8.3,P8.4,P8.5,P8.6,P8.7,P8.8,P8.9,P9.0,P9.1,P9.2,P9.3,P9.4,P9.5,P9.6,P9.7,P9.8,P9.9,P10.0,P10.1,P10.2,P10.3,P10.4,P10.5,P10.6,P10.7,P10.8,P10.9,P11.0,P11.1,P11.2,P11.3,P11.4,P11.5,P11.6,P11.7,P11.8,P11.9,P12.0,P12.1,P12.2,P12.3,P12.4,P12.5,P12.6,P12.7,P12.8,P12.9,P13.0,P13.1,P13.2,P13.3,P13.4,P13.5,P13.6,P13.7,P13.8,P13.9,P14.0,P14.1,P14.2,P14.3,P14.4,P14.5,P14.6,P14.7,P14.8,P14.9,P15.0,P15.1,P15.2,P15.3,P15.4,P15.5,P15.6,P15.7,P15.8,P15.9,P16.0,P16.1,P16.2,P16.3,P16.4,P16.5,P16.6,P16.7,P16.8,P16.9,P17.0,P17.1,P17.2,P17.3,P17.4,P17.5,P17.6,P17.7,P17.8,P17.9,P18.0,P18.1,P18.2,P18.3,P18.4,P18.5,P18.6,P18.7,P18.8,P18.9,P19.0,P19.1,P19.2,P19.3,P19.4,P19.5,P19.6,P19.7,P19.8,P19.9,P20.0,P20.1,P20.2,P20.3,P20.4,P20.5,P20.6,P20.7,P20.8,P20.9,P21.0,P21.1,P21.2,P21.3,P21.4,P21.5,P21.6,P21.7,P21.8,P21.9,P22.0,P22.1,P22.2,P22.3,P22.4,P22.5,P22.6,P22.7,P22.8,P22.9,P23.0,P23.1,P23.2,P23.3,P23.4,P23.5,P23.6,P23.7,P23.8,P23.9,P24.0,P24.1,P24.2,P24.3,P24.4,P24.5,P24.6,P24.7,P24.8,P24.9,P25.0,P25.1,P25.2,P25.3,P25.4,P25.5,P25.6,P25.7,P25.8,P25.9,P26.0,P26.1,P26.2,P26.3,P26.4,P26.5,P26.6,P26.7,P26.8,P26.9,P27.0,P27.1,P27.2,P27.3,P27.4,P27.5,P27.6,P27.7,P27.8,P27.9,P28.0,P28.1,P28.2,P28.3,P28.4,P28.5,P28.6,P28.7,P28.8,P28.9,P29.0,P29.1,P29.2,P29.3,P29.4,P29.5,P29.6,P29.7,P29.8,P29.9,P30.0,P30.1,P30.2,P30.3,P30.4,P30.5,P30.6,P30.7,P30.8,P30.9,P31.0,P31.1,P31.2,P31.3,P31.4,P31.5,P31.6,P31.7,P31.8,P31.9,P32.0,P32.1,P32.2,P32.3,P32.4,P32.5,P32.6,P32.7,P32.8,P32.9,P33.0,P33.1,P33.2,P33.3,P33.4,P33.5,P33.6,P33.7,P33.8,P33.9,P34.0,P34.1,P34.2,P34.3,P34.4,P34.5,P34.6,P34.7,P34.8,P34.9,P35.0,P35.1,P35.2,P35.3,P35.4,P35.5,P35.6,P35.7,P35.8,P35.9,P36.0,P36.1,P36.2,P36.3,P36.4,P36.5,P36.6,P36.7,P36.8,P36.9,P37.0,P37.1,P37.2,P37.3,P37.4,P37.5,P37.6,P37.7,P37.8,P37.9,P38.0,P38.1,P38.2,P38.3,P38.4,P38.5,P38.6,P38.7,P38.8,P38.9,P39.0,P39.1,P39.2,P39.3,P39.4,P39.5,P39.6,P39.7,P39.8,P39.9,P40.0,P40.1,P40.2,P40.3,P40.4,P40.5,P40.6,P40.7,P40.8,P40.9,P41.0,P41.1,P41.2,P41.3,P41.4,P41.5,P41.6,P41.7,P41.8,P41.9,P42.0,P42.1,P42.2,P42.3,P42.4,P42.5,P42.6,P42.7,P42.8,P42.9,P43.0,P43.1,P43.2,P43.3,P43.4,P43.5,P43.6,P43.7,P43.8,P43.9,P44.0,P44.1,P44.2,P44.3,P44.4,P44.5,P44.6,P44.7,P44.8,P44.9,P45.0,P45.1,P45.2,P45.3,P45.4,P45.5,P45.6,P45.7,P45.8,P45.9,P46.0,P46.1,P46.2,P46.3,P46.4,P46.5,P46.6,P46.7,P46.8,P46.9,P47.0,P47.1,P47.2,P47.3,P47.4,P47.5,P47.6,P47.7,P47.8,P47.9,P48.0,P48.1,P48.2,P48.3,P48.4,P48.5,P48.6,P48.7,P48.8,P48.9,P49.0,P49.1,P49.2,P49.3,P49.4,P49.5,P49.6,P49.7,P49.8,P49.9,P50.0,P50.1,P50.2,P50.3,P50.4,P50.5,P50.6,P50.7,P50.8,P50.9,P51.0,P51.1,P51.2,P51.3,P51.4,P51.5,P51.6,P51.7,P51.8,P51.9,P52.0,P52.1,P52.2,P52.3,P52.4,P52.5,P52.6,P52.7,P52.8,P52.9,P53.0,P53.1,P53.2,P53.3,P53.4,P53.5,P53.6,P53.7,P53.8,P53.9,P54.0,P54.1,P54.2,P54.3,P54.4,P54.5,P54.6,P54.7,P54.8,P54.9,P55.0,P55.1,P55.2,P55.3,P55.4,P55.5,P55.6,P55.7,P55.8,P55.9,P56.0,P56.1,P56.2,P56.3,P56.4,P56.5,P56.6,P56.7,P56.8,P56.9,P57.0,P57.1,P57.2,P57.3,P57.4,P57.5,P57.6,P57.7,P57.8,P57.9,P58.0,P58.1,P58.2,P58.3,P58.4,P58.5,P58.6,P58.7,P58.8,P58.9,P59.0,P59.1,P59.2,P59.3,P59.4,P59.5,P59.6,P59.7,P59.8,P59.9,P60.0,P60.1,P60.2,P60.3,P60.4,P60.5,P60.6,P60.7,P60.8,P60.9,P61.0,P61.1,P61.2,P61.3,P61.4,P61.5,P61.6,P61.7,P61.8,P61.9,P62.0,P62.1,P62.2,P62.3,P62.4,P62.5,P62.6,P62.7,P62.8,P62.9,P63.0,P63.1,P63.2,P63.3,P63.4,P63.5,P63.6,P63.7,P63.8,P63.9,P64.0,P64.1,P64.2,P64.3,P64.4,P64.5,P64.6,P64.7,P64.8,P64.9,P65.0,P65.1,P65.2,P65.3,P65.4,P65.5,P65.6,P65.7,P65.8,P65.9,P66.0,P66.1,P66.2,P66.3,P66.4,P66.5,P66.6,P66.7,P66.8,P66.9,P67.0,P67.1,P67.2,P67.3,P67.4,P67.5,P67.6,P67.7,P67.8,P67.9,P68.0,P68.1,P68.2,P68.3,P68.4,P68.5,P68.6,P68.7,P68.8,P68.9,P69.0,P69.1,P69.2,P69.3,P69.4,P69.5,P69.6,P69.7,P69.8,P69.9,P70.0,P70.1,P70.2,P70.3,P70.4,P70.5,P70.6,P70.7,P70.8,P70.9,P71.0,P71.1,P71.2,P71.3,P71.4,P71.5,P71.6,P71.7,P71.8,P71.9,P72.0,P72.1,P72.2,P72.3,P72.4,P72.5,P72.6,P72.7,P72.8,P72.9,P73.0,P73.1,P73.2,P73.3,P73.4,P73.5,P73.6,P73.7,P73.8,P73.9,P74.0,P74.1,P74.2,P74.3,P74.4,P74.5,P74.6,P74.7,P74.8,P74.9,P75.0,P75.1,P75.2,P75.3,P75.4,P75.5,P75.6,P75.7,P75.8,P75.9,P76.0,P76.1,P76.2,P76.3,P76.4,P76.5,P76.6,P76.7,P76.8,P76.9,P77.0,P77.1,P77.2,P77.3,P77.4,P77.5,P77.6,P77.7,P77.8,P77.9,P78.0,P78.1,P78.2,P78.3,P78.4,P78.5,P78.6,P78.7,P78.8,P78.9,P79.0,P79.1,P79.2,P79.3,P79.4,P79.5,P79.6,P79.7,P79.8,P79.9,P80.0,P80.1,P80.2,P80.3,P80.4,P80.5,P80.6,P80.7,P80.8,P80.9,P81.0,P81.1,P81.2,P81.3,P81.4,P81.5,P81.6,P81.7,P81.8,P81.9,P82.0,P82.1,P82.2,P82.3,P82.4,P82.5,P82.6,P82.7,P82.8,P82.9,P83.0,P83.1,P83.2,P83.3,P83.4,P83.5,P83.6,P83.7,P83.8,P83.9,P84.0,P84.1,P84.2,P84.3,P84.4,P84.5,P84.6,P84.7,P84.8,P84.9,P85.0,P85.1,P85.2,P85.3,P85.4,P85.5,P85.6,P85.7,P85.8,P85.9,P86.0,P86.1,P86.2,P86.3,P86.4,P86.5,P86.6,P86.7,P86.8,P86.9,P87.0,P87.1,P87.2,P87.3,P87.4,P87.5,P87.6,P87.7,P87.8,P87.9,P88.0,P88.1,P88.2,P88.3,P88.4,P88.5,P88.6,P88.7,P88.8,P88.9,P89.0,P89.1,P89.2,P89.3,P89.4,P89.5,P89.6,P89.7,P89.8,P89.9,P90.0,P90.1,P90.2,P90.3,P90.4,P90.5,P90.6,P90.7,P90.8,P90.9,P91.0,P91.1,P91.2,P91.3,P91.4,P91.5,P91.6,P91.7,P91.8,P91.9,P92.0,P92.1,P92.2,P92.3,P92.4,P92.5,P92.6,P92.7,P92.8,P92.9,P93.0,P93.1,P93.2,P93.3,P93.4,P93.5,P93.6,P93.7,P93.8,P93.9,P94.0,P94.1,P94.2,P94.3,P94.4,P94.5,P94.6,P94.7,P94.8,P94.9,P95.0,P95.1,P95.2,P95.3,P95.4,P95.5,P95.6,P95.7,P95.8,P95.9,P96.0,P96.1,P96.2,P96.3,P96.4,P96.5,P96.6,P96.7,P96.8,P96.9,P97.0,P97.1,P97.2,P97.3,P97.4,P97.5,P97.6,P97.7,P97.8,P97.9,P98.0,P98.1,P98.2,P98.3,P98.4,P98.5,P98.6,P98.7,P98.8,P98.9,P99.0,P99.1,P99.2,P99.3,P99.4,P99.5,P99.6,P99.7,P99.8,P99.9

#### Fetch all additional info ####
# http://iresearch.worldbank.org/PovcalNet/data.aspx
# and all these pages: iresearch.worldbank.org/PovcalNet/Docs/CountryDocs/KHM.htm
# http://iresearch.worldbank.org/PovcalNet/Archive.aspx
# clickable region names here http://iresearch.worldbank.org/PovcalNet/povDuplicateWB.aspx >>> javascript:dispSmry(emptyVisible,"MNA",1981)
# http://iresearch.worldbank.org/PovcalNet/FAQs.aspx
# http://iresearch.worldbank.org/PovcalNet/methodology.aspx
# http://iresearch.worldbank.org/PovcalNet/introduction.aspx
# http://iresearch.worldbank.org/PovcalNet/publications.aspx
# http://iresearch.worldbank.org/PovcalNet/home.aspx

#### Fetch Regional Aggregates ####

rm(list= ls()[!(ls() %in% c('IdealPLs'))])

for (i in c(seq(9800,length(IdealPLs),100),15162)){
  no_cores <- 5
  cl <- makeCluster(no_cores, type="FORK")
  registerDoParallel(cl)
  if (i>15100){
    low_i <- i-61
  } else {
    low_i <- i-99
  }
  Distro <- foreach(jjj=IdealPLs[c(low_i:i)], 
                    #.combine='rbind', 
                    .errorhandling = "pass") %dopar% { 
                      
                      ttt <- 8
                      while (ttt>0){
                        Temp <- povcalnet_wb(
                          povline = jjj,
                          year = "all",
                          url = "http://iresearch.worldbank.org",
                          format = "csv"
                        )
                        
                        WrongEntries <- which(!trimws(format(Temp$povertyline,nsmall = 3))==
                                              trimws(format(jjj, nsmall = 3)))
                        
                        if (length(WrongEntries)>0){
                          ttt <- ttt - 1
                        } else {
                          ttt <- 0
                        }
                      }
                      
                      # I added this extra column because in several instances
                      # the poverty line returned from a particular country
                      # is much different from the poverty line requested
                      # e.g. when asking PL of 1.009 I got a 0.2264779
                      # PL for Burundi in 1981
                      # in the same df I got year 19892Y and datayear 0.0163
                      # for Belarus see 
                      # "/media/michalis/1984/PovcalNet/Examples/Distro1100.RData" oh I just deleted it...
                      Temp$RequestedLine <- jjj
                      return(Temp)
                    }
  stopCluster(cl)
  registerDoSEQ()
  # next time it must be width = 5 because it goes up to ~16000 and it does not 
  # sort properly in R:
  save(list = 'Distro',file = paste0('/media/michalis/1984/PovcalNet/Regional/Distro',formatC(i,width = 5, format = "d", flag = "0"),'.RData'))
  print(paste0('Saved file... ',paste0('/media/michalis/1984/PovcalNet/Regional/Distro',formatC(i,width = 5, format = "d", flag = "0"),'.RData')))
  rm(Distro)
}

redo 5600 5700

#### Visualization Platforms ####
# http://worrydream.com/ExplorableExplanations/
# https://explorabl.es/