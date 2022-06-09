#### Notes to mention ####

# for the relative pov I am using the closest PL to the rel PL
# I can also use the actual rel PL with the gpinter distribution
# but I think it is closer to the data to keep it as I have it
# although I don't have a strong preference, the difference must be minuscule

# the HHS with monotonicity issues are identified and reported here

#### Actual Code ####

# Variables we want:
#Variables based around poverty lines
#The variables below should be prepared for:
#  these absolute poverty lines: {$1.90, $3.20, $5.50, $10, $15, $20, $30, $40}
#These relative lines: {40% of median, 50% of median, 60% of median}
#Share of population below poverty line
#Number of people below poverty line
#Poverty gap index (as per WB/Ravallion terminology)
#Absolute poverty gap (expressed in annual terms)
#[FYI, this is the amount of money (theoretically) needed to bring everyone up to the poverty line, expressed in annual terms]

#Derived as:
  
#  = poverty_gap_index x poverty_line x population x 365

#‘Income gap ratio’ (According to Ravallion)

#Other variables
#Mean income/consumption per day
#Decile thresholds, 1 through 9 (AKA P10, P20… P90 – Including Median)
#Decile shares, 1 through 10
#Per day average within decile, 1 through 10

#Inequality indices
#Gini
#P90:P10 ratio
#P90:50 ratio
#The list of inequality measures is potentially very large… MLD, Palma Ratio, absolute measures etc.
#Metadata variables
#Welfare measure
#[i.e. whether consumption or income]

#Is survey year (or not)?
#  [Dichotomous variable indicating if the data is interpolated/extrapolated or not]

library(povcalnetR)
library(ineq)
library(gpinter)
library(tcltk)
library(doParallel)
library(readr)
library(tidyverse)
library(RCurl)
library(knitr)
library(Hmisc)
library(httr)
library(jsonlite)

setwd(dirname(rstudioapi::getSourceEditorContext()$path))
rm(list= ls())

##### Creating the dataframe ####

FirstRows <- c('Entity','Year')

AbsPLs <- c('1_00', "1_90", "3_20", "5_50", "10_00", 
            "15_00", "20_00", "30_00", "40_00")

AbsPLColsPrefixes <- c('headcount_ratio_',
                    'poverty_gap_index_',
                    'headcount_',
                    'total_shortfall_annual_',
                    'income_gap_ratio_',
                    'watts_index_')

RelPLs <- c("40_median","50_median","60_median")
RelPLsEst <- c("40_median_est","50_median_est","60_median_est")

RelPLColsPrefixes <- c('headcount_ratio_',
                       'poverty_gap_index_',
                       'headcount_',
                       'total_shortfall_annual_',
                       'income_gap_ratio_',
                       'watts_index_')

DecileSharesColumns <- c("share_decile_1",
                         "share_decile_2",
                         "share_decile_3",
                         "share_decile_4",
                         "share_decile_5",
                         "share_decile_6",
                         "share_decile_7",
                         "share_decile_8",
                         "share_decile_9",
                         "share_decile_10")

DecileSharesColumnsEst <- c("share_decile_1_est",
                         "share_decile_2_est",
                         "share_decile_3_est",
                         "share_decile_4_est",
                         "share_decile_5_est",
                         "share_decile_6_est",
                         "share_decile_7_est",
                         "share_decile_8_est",
                         "share_decile_9_est",
                         "share_decile_10_est")

DecileThresholdsColumns <- c("threshold_decile_1_est",
                             "threshold_decile_2_est",
                             "threshold_decile_3_est",
                             "threshold_decile_4_est",
                             "threshold_decile_5_est",
                             "threshold_decile_6_est",
                             "threshold_decile_7_est",
                             "threshold_decile_8_est",
                             "threshold_decile_9_est")

DecileAveragesColumns <- c("average_decile_1_est",
                           "average_decile_2_est",
                           "average_decile_3_est",
                           "average_decile_4_est",
                           "average_decile_5_est",
                           "average_decile_6_est",
                           "average_decile_7_est",
                           "average_decile_8_est",
                           "average_decile_9_est",
                           "average_decile_10_est")

IneqIndices <- c('Gini',"Gini_est", "Polarization","Polarization_est", "MLD","MLD_est",
                 "Palma","P90_P10_ratio", "P90_P50_ratio",
                 "Entropy_0_5","Entropy_1_0","Entropy_1_5","Entropy_2_0",
                 "Atkinson_0_5","Atkinson_1_0","Atkinson_1_5","Atkinson_2_0",
                 "Theil_0_0","Theil_0_5","Theil_1_0","Theil_1_5","Theil_2_0","Var.Coeff")

MetaColumns <- c('survey_year',"is_interpolated","distribution_type",'reporting_level',
                 'estimation_type','welfare_type','comparable_spell','survey_comparability',
                 'survey_acronym','IsSurveyYear','MaxHeadcountRatio',
                 'MonotonicityBreaks','MonotonicityBreaksDistinct','RowsWithIncreasingHeadcount',
                 'DataframeRowsForGpinter', "reporting_gdp", "reporting_pce")

GenStatsAndInfo <- c('MeanPerDay','MeanPerDay_est','MedianPerDay',
                     'MedianPerDay_est','MedianPerDay_gp_est','PPP','Population')

AbsCols <- expand.grid(AbsPLColsPrefixes,AbsPLs)
AbsCols$Title <- paste0(AbsCols$Var1,AbsCols$Var2)
AbsCols <- AbsCols[order(AbsCols[,1]),]
RelCols <- expand.grid(RelPLColsPrefixes,RelPLs)
RelCols$Title <- paste0(RelCols$Var1,RelCols$Var2)
RelCols <- RelCols[order(RelCols[,1]),]
RelColsEst <- expand.grid(RelPLColsPrefixes,RelPLsEst)
RelColsEst$Title <- paste0(RelColsEst$Var1,RelColsEst$Var2)
RelColsEst <- RelColsEst[order(RelColsEst[,1]),]

AllCols <- c(FirstRows,AbsCols$Title,RelCols$Title,RelColsEst$Title,
             GenStatsAndInfo,DecileSharesColumns,DecileSharesColumnsEst,
             DecileThresholdsColumns,DecileAveragesColumns,IneqIndices,
             MetaColumns)

MyEmptyRow <- cbind(AllCols)
MyEmptyRow <- t(MyEmptyRow)
MyEmptyRow <- as.data.frame(MyEmptyRow)
names(MyEmptyRow) <- AllCols
MyEmptyRow[,c(1:ncol(MyEmptyRow))] <- NA

ExportDataFrame <- subset(MyEmptyRow,MyEmptyRow$Entity=='sfjskdjfsdj0988')

label(ExportDataFrame[,grepl('_est',names(ExportDataFrame))]) <- 'Estimated using gpinter'
label(MyEmptyRow[,grepl('_est',names(ExportDataFrame))]) <- 'Estimated using gpinter'
label(ExportDataFrame$MedianPerDay_gp_est) <- 'Median value per day estimated with gpinter'
label(MyEmptyRow$MedianPerDay_gp_est) <- 'Median value per day estimated with gpinter'
label(ExportDataFrame$MedianPerDay_est) <- 'Median value per day estimated from the data by finding the poverty line where headcount is equal to 0.5'
label(MyEmptyRow$MedianPerDay_est) <- 'Median value per day estimated from the data by finding the poverty line where headcount is equal to 0.5'

load('/media/michalis/DataBox/PIP/MasterData/MasterDistroWithFills.RData')

MasterDistro$countryname <- NULL
MasterDistro$regioncode <- NULL
MasterDistro$decile1 <- NULL
MasterDistro$decile2 <- NULL
MasterDistro$decile3 <- NULL
MasterDistro$decile4 <- NULL
MasterDistro$decile5 <- NULL
MasterDistro$decile6 <- NULL
MasterDistro$decile8 <- NULL
MasterDistro$decile9 <- NULL
MasterDistro$decile10 <- NULL
gc()

# this is the unique identifier:
MasterDistro$iso3typeyearwelfare <- paste0(MasterDistro$country_code,
                                           MasterDistro$reporting_level,
                                           MasterDistro$reporting_year,
                                           MasterDistro$welfare_type)

res = GET("https://api.worldbank.org/pip/v1/pip?country=all&year=all&povline=1.9&fill_gaps=true")
HHS2 <- fromJSON(rawToChar(res$content))
#load('HHS2.RData')

# this is the unique identifier:
HHS2$iso3typeyearwelfare <- paste0(HHS2$country_code,
                                   HHS2$reporting_level,
                                   HHS2$reporting_year,
                                   HHS2$welfare_type)

# I will remove the median values from entries that are not
# part of the original HHS data

#load('HHS.RData')
res = GET("https://api.worldbank.org/pip/v1/pip?country=all&year=all&povline=1.9")
HHS <- fromJSON(rawToChar(res$content))

HHS$iso3typeyearwelfare <- paste0(HHS$country_code,
                                   HHS$reporting_level,
                                   HHS$reporting_year,
                                   HHS$welfare_type)

HHS2$median[which(!HHS2$iso3typeyearwelfare %in% HHS$iso3typeyearwelfare)] <- as.numeric(NA)

sum(!is.na(HHS2$median))
# 1772

MasterDistro$median[which(!MasterDistro$iso3typeyearwelfare %in% HHS$iso3typeyearwelfare)] <- as.numeric(NA)
sum(!is.na(MasterDistro$median))/14920
# 1772 perfect!

# remove the entries that in the meantime have also been removed from PIP
ttt <- unique(MasterDistro$iso3typeyearwelfare)
ttt[which(!ttt %in% HHS2$iso3typeyearwelfare)]
# [1] "WSMnational1981consumption" "SOMnational2011consumption"
rm(ttt)
MasterDistro <- subset(MasterDistro, !MasterDistro$iso3typeyearwelfare %in% c("WSMnational1981consumption","SOMnational2011consumption"))

UniqueHHS <- sort(unique(MasterDistro$iso3typeyearwelfare))

IdealPLs <- c(seq(0.001,5,0.001),seq(5.01,60,0.01),seq(60.1,150,0.1),
              seq(150.5,1400,0.5), seq(1405,3000,5), seq(3010,10000,10))

##### Running countries' loop ####

total <- length(UniqueHHS)

# ca.X hrs down? from ca.36 hrs with the old fitting approach to gpinter

pb <- tkProgressBar(title = "progress bar", min = 0,max = total, width = 300)

which(UniqueHHS=='SYRnational2013consumption')

for (i in UniqueHHS[c(1:length(UniqueHHS))]){

  setTkProgressBar(pb, which(UniqueHHS==i), 
                   label=paste( round(which(UniqueHHS==i)/total*100, 3),"% done"))

  Temp <- subset(MasterDistro,MasterDistro$iso3typeyearwelfare==i)
  
  if (!all(is.na(Temp$headcount))){
    NewEmptyRow <- MyEmptyRow
    
    if (length(unique(Temp$mean))==1){
      if (unique(Temp$mean)==HHS2$mean[which(HHS2$iso3typeyearwelfare==i)]){
        NewEmptyRow$MeanPerDay <- unique(Temp$mean)
      } else {
        print(paste0('Mean not equal to HHS mean at ',i))
        NewEmptyRow$MeanPerDay <- HHS2$mean[which(HHS2$iso3typeyearwelfare==i)]
      }
    } else if (length(unique(Temp$mean))>1){
      print(paste0('More than 1 mean values at ', i))
      NewEmptyRow$MeanPerDay <- HHS2$mean[which(HHS2$iso3typeyearwelfare==i)]
    } else {
      print(paste0('Probably mean is NA at ', i))
      NewEmptyRow$MeanPerDay <- HHS2$mean[which(HHS2$iso3typeyearwelfare==i)]
    }
    
    if (!all(is.na(unique(Temp$reporting_gdp)))){
      if (length(unique(Temp$reporting_gdp))==1){
        if (unique(Temp$reporting_gdp)==HHS2$reporting_gdp[which(HHS2$iso3typeyearwelfare==i)]){
          NewEmptyRow$reporting_gdp <- unique(Temp$reporting_gdp)
        } else {
          print(paste0('Fetched reporting_gdp value not equal to HHS reporting_gdp at ',i))
          NewEmptyRow$reporting_gdp <- HHS2$reporting_gdp[which(HHS2$iso3typeyearwelfare==i)]
        }
      } else if (length(unique(Temp$reporting_gdp))>1){
        print(paste0('More than 1 reporting_gdp at ', i))
        NewEmptyRow$reporting_gdp <- HHS2$reporting_gdp[which(HHS2$iso3typeyearwelfare==i)]
      }
    } else if (!is.na(HHS2$reporting_gdp[which(HHS2$iso3typeyearwelfare==i)])){
      print(paste0('Fetched reporting_gdp is NA at ', i))
      NewEmptyRow$reporting_gdp <- HHS2$reporting_gdp[which(HHS2$iso3typeyearwelfare==i)]
    }
    
    if (!all(is.na(unique(Temp$reporting_pce)))){
      if (length(unique(Temp$reporting_pce))==1){
        if (unique(Temp$reporting_pce)==HHS2$reporting_pce[which(HHS2$iso3typeyearwelfare==i)]){
          NewEmptyRow$reporting_pce <- unique(Temp$reporting_pce)
        } else {
          print(paste0('Fetched reporting_pce value not equal to HHS reporting_pce at ',i))
          NewEmptyRow$reporting_pce <- HHS2$reporting_pce[which(HHS2$iso3typeyearwelfare==i)]
        }
      } else if (length(unique(Temp$reporting_pce))>1){
        print(paste0('More than 1 reporting_pce at ', i))
        NewEmptyRow$reporting_pce <- HHS2$reporting_pce[which(HHS2$iso3typeyearwelfare==i)]
      }
    } else if (!is.na(HHS2$reporting_pce[which(HHS2$iso3typeyearwelfare==i)])){
      print(paste0('Fetched reporting_pce is NA at ', i))
      NewEmptyRow$reporting_pce <- HHS2$reporting_pce[which(HHS2$iso3typeyearwelfare==i)]
    }
    
    # because some distributions are way too detailed to be matched by gpinter
    # and they produce errors like:
    # "Error in clean_input_tabulation(p, threshold, average, bracketshare, topshare,  : 
    # input data is inconsistent between p=0.0539 and p=0.0544. The bracket average 
    # (217.52) is not strictly within the bracket thresholds (217.91 and 218.27)"
    # which is meaningless, I will sample the distribution at a higher
    # step between samples in the headcount (via Diff>0.001 below)
    # I am using a different step size at parts levels of the distro
    # so that the density does not become too low
    
    # moreover monotonicity issues like in:
    # ARM:1997:1996:N:i 
    # Error in clean_input_thresholds(p, threshold, average, last_bracketavg,  : 
    # thresholds must be strictly increasing: at rows 37 and 38, you have threshold=1967.35 followed by threshold=1952.75
    # Error in clean_input_thresholds(p, threshold, average, last_bracketavg,  : 
    # thresholds must be strictly increasing: at rows 38 and 39, you have threshold=1971 followed by threshold=1956.4
    # I will remove those before subsetting to the short version
    
    Temp <- Temp[ order(Temp[,'poverty_line']), ]
    TempNew <- Temp
    TempNew <- subset(TempNew,!is.na(TempNew$headcount))
    TempNew$Diffs <- c(1,diff(TempNew$headcount))
    y <- nrow(TempNew)
    
    NewEmptyRow$MonotonicityBreaksDistinct <- sum(TempNew$Diffs<0)
    
    while (any(TempNew$Diffs<0)){
      TempNew <- subset(TempNew,!TempNew$Diffs<0)
      TempNew$Diffs <- c(1,diff(TempNew$headcount))
    }
    
    NewEmptyRow$RowsWithIncreasingHeadcount <- nrow(subset(TempNew,TempNew$Diffs>0))
    
    NewEmptyRow$MonotonicityBreaks <- y-nrow(TempNew)
    TempNew <- TempNew[ order(TempNew[,'poverty_line']), ]
    TempNew$Diffs <- c(0,diff(TempNew$headcount))
    TempNew$CumDiffs <- cumsum(TempNew$Diffs)
    
    # I am using the code below
    # to take samples only at specific (wider) intervals
    # so that gpinter can perform without errors
    
    TempNew$headcount <- round(TempNew$headcount,3)
    TempShort <- subset(TempNew,!duplicated(TempNew$headcount))
    
    # the above gives a testDistro error (below) at "ARG:1992:1992:U:i"
    
    # let's catch the error and use the message to get the point where the error
    # of fitting takes place. A typical error message is like:
    # "Error in clean_input_tabulation(p, threshold, average, bracketshare, topshare,  : 
    # input data is inconsistent between p=0.8357 and p=0.8374. The bracket average 
    # (9094.33) is not strictly within the bracket thresholds (9095.80 and 9099.45)
    
    testDistro <- tryCatch(thresholds_fit(TempShort$headcount[c(1:nrow(TempShort)-1)], 
                                          365*TempShort$poverty_line[c(1:nrow(TempShort)-1)],
                                          average = 365*NewEmptyRow$MeanPerDay),error=function(e) {
                                            # Choose a return value in case of error
                                            return(parse_number(unlist(e)$message))
                                          })
    
    if (is.numeric(testDistro) & !is.na(testDistro)){
      # if the above produces and error of inconsistency above a threshold (captured by testDistro)
      # then lower the sample from slightly below that threshold and above
      TempShort$headcount[TempShort$headcount>0.98*testDistro] <- 
        round(TempShort$headcount[TempShort$headcount>0.98*testDistro],2)
      TempShort <- subset(TempShort,!duplicated(TempShort$headcount))
      
      testDistro <- tryCatch(thresholds_fit(TempShort$headcount[c(1:nrow(TempShort)-1)], 
                                            365*TempShort$poverty_line[c(1:nrow(TempShort)-1)],
                                            average = 365*NewEmptyRow$MeanPerDay),error=function(e) {
                                              # Choose a return value in case of error
                                              return(parse_number(unlist(e)$message))
                                            })
      
    }
    
    if (is.numeric(testDistro)){
      # if the above attempt does not work, then lower the sample throughout the
      # distribution
      
      TempShort <- subset(TempNew,!duplicated(TempNew$headcount))
      TempShort$headcount <- round(TempShort$headcount,2)
      TempShort <- subset(TempShort,!duplicated(TempShort$headcount))
      
      testDistro <- tryCatch(thresholds_fit(TempShort$headcount[c(1:nrow(TempShort)-1)], 
                                            365*TempShort$poverty_line[c(1:nrow(TempShort)-1)],
                                            average = 365*NewEmptyRow$MeanPerDay),error=function(e) {
                                              # Choose a return value in case of error
                                              return(parse_number(unlist(e)$message))
                                            })
      
    }
    
    if (is.numeric(testDistro)){
      # if the above attempt does not work, then lower the sample throughout the
      # distribution
      
      TempShort <- TempShort[seq(1,nrow(TempShort),2),]
      
      testDistro <- tryCatch(thresholds_fit(TempShort$headcount[c(1:nrow(TempShort)-1)], 
                                            365*TempShort$poverty_line[c(1:nrow(TempShort)-1)],
                                            average = 365*NewEmptyRow$MeanPerDay),error=function(e) {
                                              # Choose a return value in case of error
                                              return(parse_number(unlist(e)$message))
                                            })
      
    }
    
    if (is.numeric(testDistro)){
      stop(paste0('error at ',i))
    }
    
    NewEmptyRow$DataframeRowsForGpinter <- nrow(TempShort)
    
    # the command bellow did not work very well, big difference with the given PCN values when used 
    # to estimate MLD or Gini
    # TheDistroInProportions <- rep(TempShort$poverty_line,round(10000*TempShort$headcount))
    # so I reverted to gpinter entirely
    
    # following the example from the gpinter-vignette.pdf on page 2:
    # TempShort <- subset(TempShort,!round(TempShort$headcount,4)==0.0544)
    #TempShort$PopulationInBracket <- diff(c(0,round(1000000*NewEmptyRow$Population*TempShort$headcount,0)))
    #TempShort$CumulativePopInBracket <- c(cumsum(TempShort$PopulationInBracket)[c(1:(nrow(TempShort)))])
    
    if (!is.na(unique(NewEmptyRow$MeanPerDay))){
      distribution <- thresholds_fit(TempShort$headcount[c(1:nrow(TempShort)-1)], 
                                     365*TempShort$poverty_line[c(1:nrow(TempShort)-1)],
                                     average = 365*unique(NewEmptyRow$MeanPerDay))
    } else {
      distribution <- thresholds_fit(TempShort$headcount[c(1:nrow(TempShort)-1)], 
                                     365*TempShort$poverty_line[c(1:nrow(TempShort)-1)])
    }
    
    
    GPinterDistro <- generate_tabulation(distribution,
                                         fractiles = c(seq(0.1, 0.9, 0.1)))
    
    GPinterDistroDetailed <- generate_tabulation(distribution,
                                         fractiles = c(seq(0.001, 0.999, 0.001)))
    
    # copy readily available info or easy (one-liners) to calculate
    
    # FirstRows
    NewEmptyRow$Entity <- unique(Temp$country_code)
    NewEmptyRow$Year <-  unique(Temp$reporting_year)
    NewEmptyRow$MaxHeadcountRatio <- max(TempNew$headcount)
    
    # GenStatsAndInfo
    NewEmptyRow$MeanPerDay_est <- bracket_average(distribution, 0, 1)/365
    NewEmptyRow$MedianPerDay <- unique(Temp$median)
    
    # now the median should be estimated not only based on the GPinter, but also 
    # on the value that gives a headcount equal to .5
    
    if (length(Temp$poverty_line[which(round(Temp$headcount,3)==0.500)])>0){
      NewEmptyRow$MedianPerDay_est <- mean(Temp$poverty_line[which(round(Temp$headcount,3)==0.500)], na.rm = T)
    } else if (length(Temp$poverty_line[which(round(Temp$headcount,3)==0.501)]) | 
               length(Temp$poverty_line[which(round(Temp$headcount,3)==0.499)])){ 
      NewEmptyRow$MedianPerDay_est <- mean(c(Temp$poverty_line[which(round(Temp$headcount,3)==0.501)],
                                             Temp$poverty_line[which(round(Temp$headcount,3)==0.499)]), na.rm = T)
    } else if (length(Temp$poverty_line[which(round(Temp$headcount,3)==0.502)]) | 
               length(Temp$poverty_line[which(round(Temp$headcount,3)==0.498)])){ 
      NewEmptyRow$MedianPerDay_est <- mean(c(Temp$poverty_line[which(round(Temp$headcount,3)==0.502)],
                                             Temp$poverty_line[which(round(Temp$headcount,3)==0.498)]), na.rm = T)
    } else if (length(Temp$poverty_line[which(round(Temp$headcount,3)==0.503)]) | 
               length(Temp$poverty_line[which(round(Temp$headcount,3)==0.497)])){ 
      NewEmptyRow$MedianPerDay_est <- mean(c(Temp$poverty_line[which(round(Temp$headcount,3)==0.503)],
                                             Temp$poverty_line[which(round(Temp$headcount,3)==0.497)]), na.rm = T)
    } else if (length(Temp$poverty_line[which(round(Temp$headcount,3)==0.504)]) | 
               length(Temp$poverty_line[which(round(Temp$headcount,3)==0.496)])){ 
      NewEmptyRow$MedianPerDay_est <- mean(c(Temp$poverty_line[which(round(Temp$headcount,3)==0.504)],
                                             Temp$poverty_line[which(round(Temp$headcount,3)==0.496)]), na.rm = T)
    } else if (length(Temp$poverty_line[which(round(Temp$headcount,3)==0.505)]) | 
               length(Temp$poverty_line[which(round(Temp$headcount,3)==0.495)])){ 
      NewEmptyRow$MedianPerDay_est <- mean(c(Temp$poverty_line[which(round(Temp$headcount,3)==0.505)],
                                             Temp$poverty_line[which(round(Temp$headcount,3)==0.495)]), na.rm = T)
    } else {
      #stop('median not estimated')
      NewEmptyRow$MedianPerDay_est <- as.numeric(NA)
    }
    
    NewEmptyRow$PPP <- unique(Temp$ppp)
    NewEmptyRow$Population <- unique(Temp$reporting_pop)
    
    # MetaColumns
    NewEmptyRow$is_interpolated <- unique(Temp$is_interpolated)
    NewEmptyRow$survey_year <- unique(Temp$survey_year)
    NewEmptyRow$distribution_type <- unique(Temp$distribution_type)
    NewEmptyRow$survey_coverage <- unique(Temp$survey_coverage)
    NewEmptyRow$survey_comparability <- unique(Temp$survey_comparability)
    NewEmptyRow$comparable_spell <- unique(Temp$comparable_spell)
    NewEmptyRow$reporting_level <- unique(Temp$reporting_level)
    NewEmptyRow$welfare_type <- unique(Temp$welfare_type)
    NewEmptyRow$Population <- unique(Temp$reporting_pop)
    
    NewEmptyRow$IsSurveyYear <- F
    
    # DecileSharesColumns
    NewEmptyRow$share_decile_1 <- HHS2$decile1[which(HHS2$iso3typeyearwelfare==i)]
    NewEmptyRow$share_decile_2 <- HHS2$decile2[which(HHS2$iso3typeyearwelfare==i)]
    NewEmptyRow$share_decile_3 <- HHS2$decile3[which(HHS2$iso3typeyearwelfare==i)]
    NewEmptyRow$share_decile_4 <- HHS2$decile4[which(HHS2$iso3typeyearwelfare==i)]
    NewEmptyRow$share_decile_5 <- HHS2$decile5[which(HHS2$iso3typeyearwelfare==i)]
    NewEmptyRow$share_decile_6 <- HHS2$decile6[which(HHS2$iso3typeyearwelfare==i)]
    NewEmptyRow$share_decile_7 <- HHS2$decile7[which(HHS2$iso3typeyearwelfare==i)]
    NewEmptyRow$share_decile_8 <- HHS2$decile8[which(HHS2$iso3typeyearwelfare==i)]
    NewEmptyRow$share_decile_9 <- HHS2$decile9[which(HHS2$iso3typeyearwelfare==i)]
    NewEmptyRow$share_decile_10 <- HHS2$decile10[which(HHS2$iso3typeyearwelfare==i)]
    
    # IneqIndices
    
    NewEmptyRow$Polarization <- unique(Temp$polarization)
    NewEmptyRow$MLD <- unique(Temp$mld)
    NewEmptyRow$Gini <- unique(Temp$gini)
    
    if (max(TempNew$headcount)>0.98){
      
      NewEmptyRow$MedianPerDay_gp_est <- 
        GPinterDistro$threshold[which(round(GPinterDistro$fractile,1)==0.5)]/365 # GPinterDistroDetailed$threshold[which(round(GPinterDistroDetailed$fractile,3)==0.500)]/365
      
      # which polarization index definition?
      # https://www.sciencedirect.com/science/article/pii/S0165176518301046
      NewEmptyRow$Polarization_est <- NA
      
      NewEmptyRow$Gini_est <- gini(distribution)
      
      NewEmptyRow$MLD_est <- entropy(GPinterDistroDetailed$threshold, parameter = 0)
      # The Palma ratio is the share of all income received by the 10% people with 
      # highest disposable income divided by the share of all income received by the 40%
      # https://data.oecd.org/inequality/income-inequality.htm
      NewEmptyRow$Palma <- bracket_share(distribution, 0.90, 1)/bracket_share(distribution, 0, 0.4)
      # The P90/P10 ratio is the ratio of the upper bound value of the ninth decile 
      # (i.e. the 10% of people with highest income) to that of the first. The P50/P10 
      # ratio is the ratio of median income to the upper bound value of the first decile.
      # (ibid)
      NewEmptyRow$P90_P10_ratio <- GPinterDistro$threshold[which(round(GPinterDistro$fractile,1)==0.9)]/
        GPinterDistro$threshold[which(round(GPinterDistro$fractile,1)==0.1)]
      NewEmptyRow$P90_P50_ratio <- GPinterDistro$threshold[which(round(GPinterDistro$fractile,1)==0.9)]/
        GPinterDistro$threshold[which(round(GPinterDistro$fractile,1)==0.5)]
      NewEmptyRow$Entropy_0_5 <- entropy(GPinterDistroDetailed$threshold, parameter = 0.5)
      NewEmptyRow$Entropy_1_0 <- entropy(GPinterDistroDetailed$threshold, parameter = 1.0)
      NewEmptyRow$Entropy_1_5 <- entropy(GPinterDistroDetailed$threshold, parameter = 1.5)
      NewEmptyRow$Entropy_2_0 <- entropy(GPinterDistroDetailed$threshold, parameter = 2.0)
      NewEmptyRow$Atkinson_0_5 <- Atkinson(GPinterDistroDetailed$threshold, parameter = 0.5)
      NewEmptyRow$Atkinson_1_0 <- Atkinson(GPinterDistroDetailed$threshold, parameter = 1.0)
      NewEmptyRow$Atkinson_1_5 <- Atkinson(GPinterDistroDetailed$threshold, parameter = 1.5)
      NewEmptyRow$Atkinson_2_0 <- Atkinson(GPinterDistroDetailed$threshold, parameter = 2.0)
      NewEmptyRow$Theil_0_0 <- Theil(GPinterDistroDetailed$threshold, parameter = 0)
      NewEmptyRow$Theil_0_5 <- Theil(GPinterDistroDetailed$threshold, parameter = 0.5)
      NewEmptyRow$Theil_1_0 <- Theil(GPinterDistroDetailed$threshold, parameter = 1.0)
      NewEmptyRow$Theil_1_5 <- Theil(GPinterDistroDetailed$threshold, parameter = 1.5)
      NewEmptyRow$Theil_2_0 <- Theil(GPinterDistroDetailed$threshold, parameter = 2.0)
      NewEmptyRow$Var.Coeff <- var.coeff(GPinterDistroDetailed$threshold)
    
      # also use the gpinter
      NewEmptyRow$share_decile_1_est <- bracket_share(distribution, 0, 0.1)
      NewEmptyRow$share_decile_2_est <- bracket_share(distribution, 0.1, 0.2)
      NewEmptyRow$share_decile_3_est <- bracket_share(distribution, 0.2, 0.3)
      NewEmptyRow$share_decile_4_est <- bracket_share(distribution, 0.3, 0.4)
      NewEmptyRow$share_decile_5_est <- bracket_share(distribution, 0.4, 0.5)
      NewEmptyRow$share_decile_6_est <- bracket_share(distribution, 0.5, 0.6)
      NewEmptyRow$share_decile_7_est <- bracket_share(distribution, 0.6, 0.7)
      NewEmptyRow$share_decile_8_est <- bracket_share(distribution, 0.7, 0.8)
      NewEmptyRow$share_decile_9_est <- bracket_share(distribution, 0.8, 0.9)
      NewEmptyRow$share_decile_10_est <- bracket_share(distribution, 0.9, 1)
    
      # DecileThresholdsColumns
      NewEmptyRow$threshold_decile_1_est <- 
        GPinterDistro$threshold[which(round(GPinterDistro$fractile,1)==0.1)]
      NewEmptyRow$threshold_decile_2_est <- 
        GPinterDistro$threshold[which(round(GPinterDistro$fractile,1)==0.2)]
      NewEmptyRow$threshold_decile_3_est <- 
        GPinterDistro$threshold[which(round(GPinterDistro$fractile,1)==0.3)]
      NewEmptyRow$threshold_decile_4_est <- 
        GPinterDistro$threshold[which(round(GPinterDistro$fractile,1)==0.4)]
      NewEmptyRow$threshold_decile_5_est <- 
        GPinterDistro$threshold[which(round(GPinterDistro$fractile,1)==0.5)]
      NewEmptyRow$threshold_decile_6_est <- 
        GPinterDistro$threshold[which(round(GPinterDistro$fractile,1)==0.6)]
      NewEmptyRow$threshold_decile_7_est <- 
        GPinterDistro$threshold[which(round(GPinterDistro$fractile,1)==0.7)]
      NewEmptyRow$threshold_decile_8_est <- 
        GPinterDistro$threshold[which(round(GPinterDistro$fractile,1)==0.8)]
      NewEmptyRow$threshold_decile_9_est <- 
        GPinterDistro$threshold[which(round(GPinterDistro$fractile,1)==0.9)]
      
      # DecileAveragesColumns
      NewEmptyRow$average_decile_1_est <- bracket_average(distribution, 0, 0.1)
      NewEmptyRow$average_decile_2_est <- bracket_average(distribution, 0.1, 0.2)
      NewEmptyRow$average_decile_3_est <- bracket_average(distribution, 0.2, 0.3)
      NewEmptyRow$average_decile_4_est <- bracket_average(distribution, 0.3, 0.4)
      NewEmptyRow$average_decile_5_est <- bracket_average(distribution, 0.4, 0.5)
      NewEmptyRow$average_decile_6_est <- bracket_average(distribution, 0.5, 0.6)
      NewEmptyRow$average_decile_7_est <- bracket_average(distribution, 0.6, 0.7)
      NewEmptyRow$average_decile_8_est <- bracket_average(distribution, 0.7, 0.8)
      NewEmptyRow$average_decile_9_est <- bracket_average(distribution, 0.8, 0.9)
      NewEmptyRow$average_decile_10_est <- bracket_average(distribution, 0.9, 1)
    }
    
    # now get the information that is at some row within the Temp data frame:
    if (length(which(round(Temp$poverty_line,3)==1.000))>0){
      NewEmptyRow$headcount_ratio_1_00 <- 
        Temp$headcount[which(round(Temp$poverty_line,3)==1.000)]
    }
    if (length(which(round(Temp$poverty_line,3)==1.900))>0){
      NewEmptyRow$headcount_ratio_1_90 <- 
        Temp$headcount[which(round(Temp$poverty_line,3)==1.900)]
    }
    if (length(which(round(Temp$poverty_line,3)==3.200))>0){
      NewEmptyRow$headcount_ratio_3_20 <- 
        Temp$headcount[which(round(Temp$poverty_line,3)==3.200)]
    }
    if (length(which(round(Temp$poverty_line,3)==5.500))>0){
      NewEmptyRow$headcount_ratio_5_50 <- 
        Temp$headcount[which(round(Temp$poverty_line,3)==5.500)]
    }
    if (length(which(round(Temp$poverty_line,3)==10.000))>0){
      NewEmptyRow$headcount_ratio_10_00 <- 
        Temp$headcount[which(round(Temp$poverty_line,3)==10.000)]
    }
    if (length(which(round(Temp$poverty_line,3)==15.000))>0){
      NewEmptyRow$headcount_ratio_15_00 <- 
        Temp$headcount[which(round(Temp$poverty_line,3)==15.000)]
    }
    if (length(which(round(Temp$poverty_line,3)==20.000))>0){
      NewEmptyRow$headcount_ratio_20_00 <- 
        Temp$headcount[which(round(Temp$poverty_line,3)==20.000)]
    }
    if (length(which(round(Temp$poverty_line,3)==30.000))>0){
      NewEmptyRow$headcount_ratio_30_00 <- 
        Temp$headcount[which(round(Temp$poverty_line,3)==30.000)]
    }
    if (length(which(round(Temp$poverty_line,3)==40.000))>0){
      NewEmptyRow$headcount_ratio_40_00 <- 
        Temp$headcount[which(round(Temp$poverty_line,3)==40.000)]
    }
    if (length(which(round(Temp$poverty_line,3)==1.000))>0){
      NewEmptyRow$headcount_1_00 <- 
        round(Temp$headcount[which(round(Temp$poverty_line,3)==1.000)]*unique(Temp$reporting_pop))
    }
    if (length(which(round(Temp$poverty_line,3)==1.900))>0){
      NewEmptyRow$headcount_1_90 <- 
        round(Temp$headcount[which(round(Temp$poverty_line,3)==1.900)]*unique(Temp$reporting_pop))
    }
    if (length(which(round(Temp$poverty_line,3)==3.200))>0){
      NewEmptyRow$headcount_3_20 <- 
        round(Temp$headcount[which(round(Temp$poverty_line,3)==3.200)]*unique(Temp$reporting_pop))
    }
    if (length(which(round(Temp$poverty_line,3)==5.500))>0){
      NewEmptyRow$headcount_5_50 <- 
        round(Temp$headcount[which(round(Temp$poverty_line,3)==5.500)]*unique(Temp$reporting_pop))
    }
    if (length(which(round(Temp$poverty_line,3)==10.000))>0){
      NewEmptyRow$headcount_10_00 <- 
        round(Temp$headcount[which(round(Temp$poverty_line,3)==10.000)]*unique(Temp$reporting_pop))
    }
    if (length(which(round(Temp$poverty_line,3)==15.000))>0){
      NewEmptyRow$headcount_15_00 <- 
        round(Temp$headcount[which(round(Temp$poverty_line,3)==15.000)]*unique(Temp$reporting_pop))
    }
    if (length(which(round(Temp$poverty_line,3)==20.000))>0){
      NewEmptyRow$headcount_20_00 <- 
        round(Temp$headcount[which(round(Temp$poverty_line,3)==20.000)]*unique(Temp$reporting_pop))
    }
    if (length(which(round(Temp$poverty_line,3)==30.000))>0){
      NewEmptyRow$headcount_30_00 <- 
        round(Temp$headcount[which(round(Temp$poverty_line,3)==30.000)]*unique(Temp$reporting_pop))
    }
    if (length(which(round(Temp$poverty_line,3)==40.000))>0){
      NewEmptyRow$headcount_40_00 <- 
        round(Temp$headcount[which(round(Temp$poverty_line,3)==40.000)]*unique(Temp$reporting_pop))
    }
    
    #Absolute poverty gap (expressed in annual terms)
    #[FYI, this is the amount of money (theoretically) needed to bring everyone up to the poverty line, expressed in annual terms]
    #Derived as:
    #  = poverty_gap_index x poverty_line x population x 365
    if (length(which(round(Temp$poverty_line,3)==1.000))>0){
      NewEmptyRow$total_shortfall_annual_1_00 <- Temp$poverty_gap[which(round(Temp$poverty_line,3)==1.000)]*1*365
      #Poverty gap index (as per WB/Ravallion terminology)
      NewEmptyRow$poverty_gap_index_1_00 <- Temp$poverty_gap[which(round(Temp$poverty_line,3)==1.000)]
      #‘Income gap ratio’ (According to Ravallion)
      IGPdata <- GPinterDistroDetailed$threshold[which(GPinterDistroDetailed$threshold<=365*1)]/365
      NewEmptyRow$income_gap_ratio_1_00 <- mean((1-IGPdata)/1)
      rm(IGPdata)
      NewEmptyRow$watts_index_1_00 <- Temp$watts[which(round(Temp$poverty_line,3)==1.000)]
      #Watts(GPinterDistroDetailed$threshold,365*1.9)
    }
    
    if (length(which(round(Temp$poverty_line,3)==1.900))>0){
      NewEmptyRow$total_shortfall_annual_1_90 <- Temp$poverty_gap[which(round(Temp$poverty_line,3)==1.900)]*1.9*365
      #Poverty gap index (as per WB/Ravallion terminology)
      NewEmptyRow$poverty_gap_index_1_90 <- Temp$poverty_gap[which(round(Temp$poverty_line,3)==1.900)]
      #‘Income gap ratio’ (According to Ravallion)
      IGPdata <- GPinterDistroDetailed$threshold[which(GPinterDistroDetailed$threshold<=365*1.9)]/365
      NewEmptyRow$income_gap_ratio_1_90 <- mean((1.9-IGPdata)/1.9)
      rm(IGPdata)
      NewEmptyRow$watts_index_1_90 <- Temp$watts[which(round(Temp$poverty_line,3)==1.900)]
      #Watts(GPinterDistroDetailed$threshold,365*1.9)
    }
    
    if (length(which(round(Temp$poverty_line,3)==3.200))>0){
      NewEmptyRow$total_shortfall_annual_3_20 <- Temp$poverty_gap[which(round(Temp$poverty_line,3)==3.200)]*3.2*365
      NewEmptyRow$poverty_gap_index_3_20 <- Temp$poverty_gap[which(round(Temp$poverty_line,3)==3.200)]
      IGPdata <- GPinterDistroDetailed$threshold[which(GPinterDistroDetailed$threshold<=365*3.2)]/365
      NewEmptyRow$income_gap_ratio_3_20 <- mean((3.2-IGPdata)/3.2)
      rm(IGPdata)
      NewEmptyRow$watts_index_3_20 <- Temp$watts[which(round(Temp$poverty_line,3)==3.200)]
    }
    
    if (length(which(round(Temp$poverty_line,3)==5.500))>0){
      NewEmptyRow$total_shortfall_annual_5_50 <- Temp$poverty_gap[which(round(Temp$poverty_line,3)==5.500)]*5.5*365
      NewEmptyRow$poverty_gap_index_5_50 <- Temp$poverty_gap[which(round(Temp$poverty_line,3)==5.500)]
      IGPdata <- GPinterDistroDetailed$threshold[which(GPinterDistroDetailed$threshold<=365*5.5)]/365
      NewEmptyRow$income_gap_ratio_5_50 <- mean((5.5-IGPdata)/5.5)
      rm(IGPdata)
      NewEmptyRow$watts_index_5_50 <- Temp$watts[which(round(Temp$poverty_line,3)==5.500)]
    }
    
    if (length(which(round(Temp$poverty_line,3)==10.000))>0){
      NewEmptyRow$total_shortfall_annual_10_00 <- Temp$poverty_gap[which(round(Temp$poverty_line,3)==10.000)]*10*365
      NewEmptyRow$poverty_gap_index_10_00 <- Temp$poverty_gap[which(round(Temp$poverty_line,3)==10.000)]
      IGPdata <- GPinterDistroDetailed$threshold[which(GPinterDistroDetailed$threshold<=365*10)]/365
      NewEmptyRow$income_gap_ratio_10_00 <- mean((10-IGPdata)/10)
      rm(IGPdata)
      NewEmptyRow$watts_index_10_00 <- Temp$watts[which(round(Temp$poverty_line,3)==10.000)]
    }
    
    if (length(which(round(Temp$poverty_line,3)==15.000))>0){
      NewEmptyRow$total_shortfall_annual_15_00 <- Temp$poverty_gap[which(round(Temp$poverty_line,3)==15.000)]*15*365
      NewEmptyRow$poverty_gap_index_15_00 <- Temp$poverty_gap[which(round(Temp$poverty_line,3)==15.000)]
      IGPdata <- GPinterDistroDetailed$threshold[which(GPinterDistroDetailed$threshold<=365*15)]/365
      NewEmptyRow$income_gap_ratio_15_00 <- mean((15-IGPdata)/15)
      rm(IGPdata)
      NewEmptyRow$watts_index_15_00 <- Temp$watts[which(round(Temp$poverty_line,3)==15.000)]
    }
    
    if (length(which(round(Temp$poverty_line,3)==20.000))>0){
      NewEmptyRow$total_shortfall_annual_20_00 <- Temp$poverty_gap[which(round(Temp$poverty_line,3)==20.000)]*20*365
      NewEmptyRow$poverty_gap_index_20_00 <- Temp$poverty_gap[which(round(Temp$poverty_line,3)==20.000)]
      IGPdata <- GPinterDistroDetailed$threshold[which(GPinterDistroDetailed$threshold<=365*20)]/365
      NewEmptyRow$income_gap_ratio_20_00 <- mean((20-IGPdata)/20)
      rm(IGPdata)
      NewEmptyRow$watts_index_20_00 <- Temp$watts[which(round(Temp$poverty_line,3)==20.000)]
    }
    
    if (length(which(round(Temp$poverty_line,3)==30.000))>0){
      NewEmptyRow$total_shortfall_annual_30_00 <- Temp$poverty_gap[which(round(Temp$poverty_line,3)==30.000)]*30*365
      NewEmptyRow$poverty_gap_index_30_00 <- Temp$poverty_gap[which(round(Temp$poverty_line,3)==30.000)]
      IGPdata <- GPinterDistroDetailed$threshold[which(GPinterDistroDetailed$threshold<=365*30)]/365
      NewEmptyRow$income_gap_ratio_30_00 <- mean((30-IGPdata)/30)
      rm(IGPdata)
      NewEmptyRow$watts_index_30_00 <- Temp$watts[which(round(Temp$poverty_line,3)==30.000)]
    }
    
    if (length(which(round(Temp$poverty_line,3)==40.000))>0){
      NewEmptyRow$total_shortfall_annual_40_00 <- Temp$poverty_gap[which(round(Temp$poverty_line,3)==40.000)]*40*365
      NewEmptyRow$poverty_gap_index_40_00 <- Temp$poverty_gap[which(round(Temp$poverty_line,3)==40.000)]
      IGPdata <- GPinterDistroDetailed$threshold[which(GPinterDistroDetailed$threshold<=365*40)]/365
      NewEmptyRow$income_gap_ratio_40_00 <- mean((40-IGPdata)/40)
      rm(IGPdata)
      NewEmptyRow$watts_index_40_00 <- Temp$watts[which(round(Temp$poverty_line,3)==40.000)]
    }
    
    # Relative poverty estimates:
    
    PL40 <- IdealPLs[which.min(abs(IdealPLs-round(.4*NewEmptyRow$MedianPerDay,3)))][1]
    
    if (!is.na(PL40)){
      if (length(which(round(Temp$poverty_line,3)==round(PL40,3)))>0){
        NewEmptyRow$headcount_ratio_40_median <- 
          Temp$headcount[which(round(Temp$poverty_line,3)==round(PL40,3))]
        NewEmptyRow$poverty_gap_index_40_median <-  
          Temp$poverty_gap[which(round(Temp$poverty_line,3)==round(PL40,3))]
        NewEmptyRow$headcount_40_median <- 
          round(Temp$headcount[which(round(Temp$poverty_line,3)==round(PL40,3))]*
          NewEmptyRow$Population)
        NewEmptyRow$total_shortfall_annual_40_median <-  
          Temp$poverty_gap[which(round(Temp$poverty_line,3)==round(PL40,3))]*
          round(PL40,3)*365
        IGPdata <- GPinterDistroDetailed$threshold[which(GPinterDistroDetailed$threshold<=365*PL40)]/365
        NewEmptyRow$income_gap_ratio_40_median <- mean((PL40-IGPdata)/PL40)
        rm(IGPdata)
        NewEmptyRow$watts_index_40_median <- 
          Temp$watts[which(round(Temp$poverty_line,3)==round(PL40,3))]
      }
    }
    rm(PL40)
    
    PL50 <- IdealPLs[which.min(abs(IdealPLs-round(.5*NewEmptyRow$MedianPerDay,3)))][1]
    
    if (!is.na(PL50)){
      if (length(which(round(Temp$poverty_line,3)==round(PL50,3)))>0){
        NewEmptyRow$headcount_ratio_50_median <- 
          Temp$headcount[which(round(Temp$poverty_line,3)==round(PL50,3))]
        NewEmptyRow$poverty_gap_index_50_median <-  
          Temp$poverty_gap[which(round(Temp$poverty_line,3)==round(PL50,3))]
        NewEmptyRow$headcount_50_median <- 
          round(Temp$headcount[which(round(Temp$poverty_line,3)==round(PL50,3))]*
                  NewEmptyRow$Population)
        NewEmptyRow$total_shortfall_annual_50_median <- 
          Temp$poverty_gap[which(round(Temp$poverty_line,3)==round(PL50,3))]*
          round(PL50,3)*365
        IGPdata <- GPinterDistroDetailed$threshold[which(GPinterDistroDetailed$threshold<=365*PL50)]/365
        NewEmptyRow$income_gap_ratio_50_median <- mean((PL50-IGPdata)/PL50)
        rm(IGPdata)
        NewEmptyRow$watts_index_50_median <- 
          Temp$watts[which(round(Temp$poverty_line,3)==round(PL50,3))]
      }
    }
    rm(PL50)
    
    PL60 <- IdealPLs[which.min(abs(IdealPLs-round(.6*NewEmptyRow$MedianPerDay,3)))][1]
    
    if (!is.na(PL60)){
      if (length(which(round(Temp$poverty_line,3)==round(PL60,3)))>0){
        NewEmptyRow$headcount_ratio_60_median <- 
          Temp$headcount[which(round(Temp$poverty_line,3)==round(PL60,3))]
        NewEmptyRow$poverty_gap_index_60_median <-  
          Temp$poverty_gap[which(round(Temp$poverty_line,3)==round(PL60,3))]
        NewEmptyRow$headcount_60_median <- 
          round(Temp$headcount[which(round(Temp$poverty_line,3)==round(PL60,3))]*
                  NewEmptyRow$Population)
        NewEmptyRow$total_shortfall_annual_60_median <- 
          Temp$poverty_gap[which(round(Temp$poverty_line,3)==round(PL60,3))]*
          round(PL60,3)*365
        IGPdata <- GPinterDistroDetailed$threshold[which(GPinterDistroDetailed$threshold<=365*PL60)]/365
        NewEmptyRow$income_gap_ratio_60_median <- mean((PL60-IGPdata)/PL60)
        rm(IGPdata)
        NewEmptyRow$watts_index_60_median <- 
          Temp$watts[which(round(Temp$poverty_line,3)==round(PL60,3))]
      }
    }
    rm(PL60)
    
    # XXX
    
    PL40 <- IdealPLs[which.min(abs(IdealPLs-round(.4*NewEmptyRow$MedianPerDay_est,3)))][1]
    if (is.na(PL40)){
      PL40 <- IdealPLs[which.min(abs(IdealPLs-round(.4*NewEmptyRow$MedianPerDay_gp_est,3)))][1]
      if (is.na(PL40)){
        stop('is.na(PL40)')
      }
    }
    
    if (length(which(round(Temp$poverty_line,3)==round(PL40,3)))>0){
      NewEmptyRow$headcount_ratio_40_median_est <- 
        Temp$headcount[which(round(Temp$poverty_line,3)==round(PL40,3))]
      NewEmptyRow$poverty_gap_index_40_median_est <-  
        Temp$poverty_gap[which(round(Temp$poverty_line,3)==round(PL40,3))]
      NewEmptyRow$headcount_40_median_est <- 
        round(Temp$headcount[which(round(Temp$poverty_line,3)==round(PL40,3))]*
                NewEmptyRow$Population)
      NewEmptyRow$total_shortfall_annual_40_median_est <-  
        Temp$poverty_gap[which(round(Temp$poverty_line,3)==round(PL40,3))]*
        round(PL40,3)*365
      IGPdata <- GPinterDistroDetailed$threshold[which(GPinterDistroDetailed$threshold<=365*PL40)]/365
      NewEmptyRow$income_gap_ratio_40_median_est <- mean((PL40-IGPdata)/PL40)
      rm(IGPdata)
      NewEmptyRow$watts_index_40_median_est <- 
        Temp$watts[which(round(Temp$poverty_line,3)==round(PL40,3))]
    }
    rm(PL40)
    
    PL50 <- IdealPLs[which.min(abs(IdealPLs-round(.5*NewEmptyRow$MedianPerDay_est,3)))][1]
    if (is.na(PL50)){
      PL50 <- IdealPLs[which.min(abs(IdealPLs-round(.5*NewEmptyRow$MedianPerDay_gp_est,3)))][1]
      if (is.na(PL50)){
        stop('is.na(PL50)')
      }
    }
    
    if (length(which(round(Temp$poverty_line,3)==round(PL50,3)))>0){
      NewEmptyRow$headcount_ratio_50_median_est <- 
        Temp$headcount[which(round(Temp$poverty_line,3)==round(PL50,3))]
      NewEmptyRow$poverty_gap_index_50_median_est <-  
        Temp$poverty_gap[which(round(Temp$poverty_line,3)==round(PL50,3))]
      NewEmptyRow$headcount_50_median_est <- 
        round(Temp$headcount[which(round(Temp$poverty_line,3)==round(PL50,3))]*
                NewEmptyRow$Population)
      NewEmptyRow$total_shortfall_annual_50_median_est <- 
        Temp$poverty_gap[which(round(Temp$poverty_line,3)==round(PL50,3))]*
        round(PL50,3)*365
      IGPdata <- GPinterDistroDetailed$threshold[which(GPinterDistroDetailed$threshold<=365*PL50)]/365
      NewEmptyRow$income_gap_ratio_50_median_est <- mean((PL50-IGPdata)/PL50)
      rm(IGPdata)
      NewEmptyRow$watts_index_50_median_est <- 
        Temp$watts[which(round(Temp$poverty_line,3)==round(PL50,3))]
    }
    rm(PL50)
    
    PL60 <- IdealPLs[which.min(abs(IdealPLs-round(.6*NewEmptyRow$MedianPerDay_est,3)))][1]
    if (is.na(PL60)){
      PL60 <- IdealPLs[which.min(abs(IdealPLs-round(.6*NewEmptyRow$MedianPerDay_gp_est,3)))][1]
      if (is.na(PL60)){
        stop('is.na(PL60)')
      }
    }
    
    if (length(which(round(Temp$poverty_line,3)==round(PL60,3)))>0){
      NewEmptyRow$headcount_ratio_60_median_est <- 
        Temp$headcount[which(round(Temp$poverty_line,3)==round(PL60,3))]
      NewEmptyRow$poverty_gap_index_60_median_est <-  
        Temp$poverty_gap[which(round(Temp$poverty_line,3)==round(PL60,3))]
      NewEmptyRow$headcount_60_median_est <- 
        round(Temp$headcount[which(round(Temp$poverty_line,3)==round(PL60,3))]*
                NewEmptyRow$Population)
      NewEmptyRow$total_shortfall_annual_60_median_est <- 
        Temp$poverty_gap[which(round(Temp$poverty_line,3)==round(PL60,3))]*
        round(PL60,3)*365
      IGPdata <- GPinterDistroDetailed$threshold[which(GPinterDistroDetailed$threshold<=365*PL60)]/365
      NewEmptyRow$income_gap_ratio_60_median_est <- mean((PL60-IGPdata)/PL60)
      rm(IGPdata)
      NewEmptyRow$watts_index_60_median_est <- 
        Temp$watts[which(round(Temp$poverty_line,3)==round(PL60,3))]
    }
    rm(PL60)
    
    # NewEmptyRow[,which(is.na(NewEmptyRow[1,]))]
    ExportDataFrame <- rbind(ExportDataFrame,NewEmptyRow)
    rm(NewEmptyRow,distribution)
  
  } else {
      print(paste0('All headcounts are NA at ',i))
    }
}
close(pb)

ExportDataFrame$ISO3Year <- paste0(ExportDataFrame$Entity,ExportDataFrame$Year)

#[1] "All headcounts are NA at IND:2018:2011.5:A:c"
#[1] "All headcounts are NA at IND:2018:2011.5:R:c"
#[1] "All headcounts are NA at IND:2018:2011.5:U:c"
#[1] "All headcounts are NA at IND:2019:2011.5:A:c"
#[1] "All headcounts are NA at IND:2019:2011.5:R:c"
#[1] "All headcounts are NA at IND:2019:2011.5:U:c"

# survey_year was not in the df when I run the script, so it may not be in the save as well
# when I run this script for PIP I will use that column

if (!file.exists('~/PhD/Sources/OWID/ExportDataFramePIP.RData')){
  save(list = 'ExportDataFrame',file = '~/PhD/Sources/OWID/ExportDataFramePIP.RData')
}

# load('~/PhD/Sources/OWID/ExportDataFramePIP.RData')
# Now check which is original and which not
# by comparing with the original set of HHS:
# write.csv2(ExportDataFrame,'~/PhD/Sources/OWID/MainDataCountriesOnlyNew.csv')

#### Original/Imputation Flag ####

table(ExportDataFrame$IsSurveyYear)
# FALSE 
#  6682 
ExportDataFrame$iso3typeyearwelfare <- paste0(ExportDataFrame$Entity,
                                              ExportDataFrame$reporting_level,
                                              ExportDataFrame$Year,
                                              ExportDataFrame$welfare_type)

length(ExportDataFrame$iso3typeyearwelfare)==nrow(ExportDataFrame)

length(unique(HHS$iso3typeyearwelfare))==nrow(HHS)

# perfect, so we do have unique identifiers for both dataframes
sum(unique(HHS$iso3typeyearwelfare) %in% ExportDataFrame$iso3typeyearwelfare)
# 2049, where are the other 96?
# let's find the missing ones:
unique(HHS$iso3typeyearwelfare)[which(!unique(HHS$iso3typeyearwelfare) %in% ExportDataFrame$iso3typeyearwelfare)]
#[1] "FSMurban2000income"         "IDNrural2020consumption"    "IDNurban2020consumption"    "IDNrural2021consumption"    "IDNurban2021consumption"    "PHLnational2000income"     
#[7] "PHLnational2003income"      "PHLnational2006income"      "PHLnational2009income"      "PHLnational2012income"      "PHLnational2015income"      "PHLnational2018income"     
#[13] "THAnational2020consumption" "ALBnational2016income"      "ALBnational2017income"      "ALBnational2018income"      "ARMnational2020consumption" "BGRnational2007income"     
#[19] "BLRnational2020consumption" "ESTnational2003income"      "ESTnational2004income"      "GEOnational2020consumption" "HRVnational2009income"      "HRVnational2010income"     
#[25] "HUNnational1999income"      "HUNnational2004income"      "HUNnational2005income"      "HUNnational2006income"      "HUNnational2007income"      "KGZnational2020consumption"
#[31] "LTUnational2004income"      "LTUnational2008income"      "LVAnational2004income"      "LVAnational2007income"      "LVAnational2008income"      "LVAnational2009income"     
#[37] "MNEnational2012income"      "MNEnational2013income"      "MNEnational2014income"      "POLnational1999income"      "POLnational2004income"      "POLnational2005income"     
#[43] "POLnational2006income"      "POLnational2007income"      "POLnational2008income"      "POLnational2009income"      "POLnational2010income"      "POLnational2011income"     
#[49] "POLnational2012income"      "POLnational2013income"      "POLnational2014income"      "POLnational2015income"      "POLnational2016income"      "POLnational2017income"     
#[55] "POLnational2018income"      "ROUnational2006income"      "ROUnational2007income"      "ROUnational2008income"      "ROUnational2009income"      "ROUnational2010income"     
#[61] "ROUnational2011income"      "ROUnational2012income"      "ROUnational2013income"      "ROUnational2016income"      "ROUnational2018income"      "RUSnational2014income"     
#[67] "RUSnational2015income"      "RUSnational2016income"      "RUSnational2017income"      "RUSnational2018income"      "RUSnational2020consumption" "SRBnational2013income"     
#[73] "SRBnational2015income"      "SRBnational2018income"      "SRBnational2019income"      "SVKnational2004income"      "SVKnational2005income"      "SVKnational2006income"     
#[79] "SVKnational2007income"      "SVKnational2008income"      "SVKnational2009income"      "UKRnational2020consumption" "ARGurban1980income"         "ARGurban2020income"        
#[85] "BOLurban1990income"         "BOLurban1992income"         "BOLnational2020income"      "BRAnational2020income"      "CHLnational2020income"      "COLurban1980income"        
#[91] "COLurban1988income"         "COLurban1989income"         "COLurban1991income"         "COLnational2020income"      "CRInational2020income"      "DOMnational2020income"     
#[97] "ECUurban1987income"         "ECUurban1995income"         "ECUurban1998income"         "ECUnational2020income"      "HNDurban1986income"         "HTInational2012income"     
#[103] "MEXnational2020income"      "NICnational1993income"      "NICnational1998income"      "NICnational2001income"      "NICnational2005income"      "PANnational1979income"     
#[109] "PERnational2020income"      "PRYnational2020income"      "URYurban1981income"         "URYurban1989income"         "URYurban1992income"         "URYurban1995income"        
#[115] "URYurban1996income"         "URYurban1997income"         "URYurban1998income"         "URYurban2000income"         "URYurban2001income"         "URYurban2002income"        
#[121] "URYurban2003income"         "URYurban2004income"         "URYurban2005income"         "URYnational2020income"      "CANnational1971income"      "CANnational1975income"     
#[127] "ESPnational1980income"      "FRAnational1978income"      "GBRnational1969income"      "GBRnational1974income"      "GBRnational1979income"      "ISRnational1979income"     
#[133] "NORnational1979income"      "SWEnational1967income"      "SWEnational1975income"      "USAnational1974income"      "USAnational1979income"      "INDrural1977consumption"   
#[139] "INDurban1977consumption"    "ETHrural1981consumption"    "MDGnational1980consumption" "RWArural1984consumption"    "INDnational1977consumption" "IDNnational2020consumption"
#[145] "IDNnational2021consumption"

# They are either out of the period of imputation (1981-2019) 45 cases
unique(HHS$iso3typeyearwelfare)[which(!unique(HHS$iso3typeyearwelfare) %in% ExportDataFrame$iso3typeyearwelfare & (HHS$reporting_year<1981 | HHS$reporting_year>2019))]
# or there is the other welfare type selected for the imputation:
# manually checked for several cases

# lets see if those are also part of the imputed set:
HHS2$iso3typeyearwelfare
unique(HHS$iso3typeyearwelfare)[which(!unique(HHS$iso3typeyearwelfare) %in% HHS2$iso3typeyearwelfare)]

# no they are not, so we are OK I think.
ExportDataFrame$IsSurveyYear[which(ExportDataFrame$iso3typeyearwelfare %in% unique(HHS$iso3typeyearwelfare))] <- T
table(ExportDataFrame$IsSurveyYear)
# FALSE  TRUE 
#  4633  2049 

#### Corrections ####

##### Relative poverty = 0 in some observations ##### 

ExportDataFrame$ISO3Year[which(ExportDataFrame$headcount_ratio_40_median==0)]
#[1] "NPL1984"
ExportDataFrame$ISO3Year[which(ExportDataFrame$headcount_ratio_40_median_est==0)]
"NPL1981" "NPL1982" "NPL1983" "NPL1984" "NPL1985" "NPL1986" "NPL1987" "NPL1988" "NPL1989"

CurYear <- 1984
NPL <- subset(MasterDistro,MasterDistro$country_code=='NPL' & MasterDistro$reporting_year==CurYear)
RelPL <- ExportDataFrame$MedianPerDay[which(ExportDataFrame$Entity=='NPL' & ExportDataFrame$Year==CurYear)]*.4
max(NPL$headcount[which(NPL$poverty_line<RelPL)])
# so it is like this... headcount starts to rise after a PL of 0.525
# amd RelPL40 is 0.50988

##### Missing values ####

kable(data.frame(colSums(is.na(ExportDataFrame))) %>%
        filter(colSums.is.na.ExportDataFrame.. > 0))

ExportDataFrame$ISO3Year[is.na(ExportDataFrame$headcount_ratio_5_50)]
# "GNB1981" "GNB1982" "GNB1983" "GNB1984" "GNB1985" "GNB1986" "GNB1987" "GNB1988" "GNB1989" "GNB1990" "GNB1991" "GNB1992"
ExportDataFrame$ISO3Year[is.na(ExportDataFrame$average_decile_10_est)]
# "GNB1981" "GNB1982" "GNB1983" "GNB1984" "GNB1985" "GNB1986" "GNB1987" "GNB1988" "GNB1989" "GNB1990" "GNB1991" "GNB1992"
ExportDataFrame$ISO3Year[is.na(ExportDataFrame$Theil_2_0)]
# "GNB1981" "GNB1982" "GNB1983" "GNB1984" "GNB1985" "GNB1986" "GNB1987" "GNB1988" "GNB1989" "GNB1990" "GNB1991" "GNB1992"
ExportDataFrame$ISO3Year[is.na(ExportDataFrame$MedianPerDay_est)]
# "AUT1989"
ExportDataFrame$ISO3Year[is.na(ExportDataFrame$headcount_ratio_40_00)]
# "GNB1981" "GNB1982" "GNB1983" "GNB1984" "GNB1985" "GNB1986" "GNB1987" "GNB1988" "GNB1989" "GNB1990" "GNB1991" "GNB1992" "SLE1999" "SLE2001"
ExportDataFrame$ISO3Year[is.na(ExportDataFrame$income_gap_ratio_40_median_est)]
#  "NPL1981" "NPL1982" "NPL1983" "NPL1984" "NPL1985" "NPL1986" "NPL1987" "NPL1988" "NPL1989"
ExportDataFrame$ISO3Year[is.na(ExportDataFrame$watts_index_40_median_est)]
# "SLE1981" "SLE1982" "SLE1983" "SLE1984" "SLE1985" "SLE1986" "SLE1987" "SLE1988" "SLE1989" "SLE1990" "SLE1991" "SLE1992" "SLE1993" "SLE1994" "SLE1995" "SLE1996" "SLE1997" "SLE1998"
# "SLE1999" "SLE2000" "SLE2001" "SLE2002" "SLE2003"

#### To report ####

# summary of the length of monotonicity breaks in HHS with at least one monotonicity break
summary(ExportDataFrame$MonotonicityBreaks[which(ExportDataFrame$MonotonicityBreaks>0)])
#    Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
#    1.00    6.00   15.00   64.38   63.00 1533.00

ExportDataFrame$ISO3Year[which(ExportDataFrame$MonotonicityBreaks>1000)]
#  "ARE2018" "ARE2019" "SYR2013"
ExportDataFrame$ISO3Year[which(ExportDataFrame$MonotonicityBreaks>1)]
ExportDataFrame$ISO3Year[which(ExportDataFrame$MonotonicityBreaks>1)]

length(ExportDataFrame$ISO3Year[which(ExportDataFrame$MonotonicityBreaksDistinct>0)])
#[1] 973

length(ExportDataFrame$ISO3Year[which(ExportDataFrame$MonotonicityBreaks>0)])
#[1] 973

ExportDataFrame$MaxHeadcountRatio[which(ExportDataFrame$MaxHeadcountRatio<1)]
ExportDataFrame$ISO3Year[which(ExportDataFrame$MaxHeadcountRatio<1)]
# "GNB1981" "GNB1982" "GNB1983" "GNB1984" "GNB1985" "GNB1986" "GNB1987" "GNB1988" "GNB1989" "GNB1990" "GNB1991" "GNB1992"
