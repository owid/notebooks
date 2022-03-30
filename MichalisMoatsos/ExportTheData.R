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

setwd(dirname(rstudioapi::getSourceEditorContext()$path))

OldExport <- read.csv('/home/michalis/PhD/Sources/OWID/Poverty_and_inequality_measures_from_PovCal_2021.csv',
                      stringsAsFactors = F,
                      check.names = F)

##### Creating the dataframe ####
FirstRows <- c('Entity','Year')
AbsPLs <- c(1.90, 3.20, 5.50, 10, 15, 20, 30, 40)
AbsPLColsSuffixes <- c(' per day - share of population below poverty line',
                    ' per day - poverty gap index',
                    ' per day - total number of people below poverty line',
                    ' per day - absolute poverty gap',
                    ' per day - income gap ratio',
                    ' per day - watts index')
RelPLs <- c(40,50,60)
RelPLColsSuffixes <- c('% of median income - share of population below poverty line',
                       '% of median income - poverty gap index',
                       '% of median income - total number of people below poverty line',
                       '% of median income - absolute poverty gap',
                       '% of median income - income gap ratio',
                       '% of median income - watts index')
DecileSharesColumns <- c("Decile 1 – share of income or consumption",
                   "Decile 2 – share of income or consumption", "Decile 3 – share of income or consumption",
                   "Decile 4 – share of income or consumption", "Decile 5 – share of income or consumption",
                   "Decile 6 – share of income or consumption", "Decile 7 – share of income or consumption",
                   "Decile 8 – share of income or consumption", "Decile 9 – share of income or consumption",
                   "Decile 10 – share of income or consumption")
DecileThresholdsColumns <- c("Decile 1 – threshold of income or consumption",
                   "Decile 2 – threshold of income or consumption", "Decile 3 – threshold of income or consumption",
                   "Decile 4 – threshold of income or consumption", "Decile 5 – threshold of income or consumption",
                   "Decile 6 – threshold of income or consumption", "Decile 7 – threshold of income or consumption",
                   "Decile 8 – threshold of income or consumption", "Decile 9 – threshold of income or consumption")
DecileAveragesColumns <- c("Decile 1 – average income or consumption", "Decile 2 – average income or consumption",
                           "Decile 3 – average income or consumption", "Decile 4 – average income or consumption",
                           "Decile 5 – average income or consumption", "Decile 6 – average income or consumption",
                           "Decile 7 – average income or consumption", "Decile 8 – average income or consumption",
                           "Decile 9 – average income or consumption", "Decile 10 – average income or consumption")
IneqIndices <- c('Gini index',"Gini_estimated", "Polarization","Polarization_estimated", "MLD","MLD_estimated","Palma","P90:P10 ratio", "P90:50 ratio",
                 "Entropy_0_5","Entropy_1_0","Entropy_1_5","Entropy_2_0",
                 "Atkinson_0_5","Atkinson_1_0","Atkinson_1_5","Atkinson_2_0",
                 "Theil_0_0","Theil_0_5","Theil_1_0","Theil_1_5","Theil_2_0","Var.Coeff")

# 'OriginalMedian','OriginalMean','OriginalDecileShares' means: where there 
# median or mean or decile share values available from Povcalnet? When not
# I am estimating them from gpinter

MetaColumns <- c("isinterpolated","usemicrodata",'coveragetype','datatype','IsSurveyYear',
                 'OriginalMedian','OriginalMean','OriginalDecileShares','MonotonicityBreaks')
GenStatsAndInfo <- c('Mean','Mean_estimated','Median','Median_estimated','PPP','Population')

AbsCols <- expand.grid(AbsPLs,AbsPLColsSuffixes)
AbsCols$Title <- paste0("$",AbsCols$Var1,AbsCols$Var2)
AbsCols <- AbsCols[order(AbsCols[,1]),]
RelCols <- expand.grid(RelPLs,RelPLColsSuffixes)
RelCols$Title <- paste0("$",RelCols$Var1,RelCols$Var2)
RelCols <- RelCols[order(RelCols[,1]),]

AllCols <- c(FirstRows,AbsCols$Title,RelCols$Title,GenStatsAndInfo,DecileSharesColumns,
             DecileThresholdsColumns,DecileAveragesColumns,IneqIndices,MetaColumns)

MyEmptyRow <- cbind(AllCols)
MyEmptyRow <- t(MyEmptyRow)
MyEmptyRow <- as.data.frame(MyEmptyRow)
names(MyEmptyRow) <- AllCols
MyEmptyRow[,c(1:ncol(MyEmptyRow))] <- NA

ExportDataFrame <- subset(MyEmptyRow,MyEmptyRow$Entity=='sfjskdjfsdj0988')

#load('/media/michalis/1984/PovcalNet/MasterData/MasterDistroWithFills.RData')
load('/mnt/sdb3/PovcalNet/MasterData/MasterDistroWithFills.RData')
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
MasterDistro$ISO3DataYearCovTypePL <- NULL
gc()

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

NewMonotonicityAlerts <- cbind('ID','NumOfBreaks')
NewMonotonicityAlerts <- as.data.frame(NewMonotonicityAlerts)
names(NewMonotonicityAlerts) <- c('ID','NumOfBreaks')
NewMonotonicityAlerts[,c(1:ncol(NewMonotonicityAlerts))] <- NA
MonotonicityAlerts <- subset(NewMonotonicityAlerts,NewMonotonicityAlerts$ID=='234u29wejfio')

HHS2$ISO3DataYearCovType <- paste0(HHS2$countrycode,":",HHS2$year,":",HHS2$datayear,
                                   ":",HHS2$coveragetype,":",ifelse(HHS2$datatype=="consumption",'c','i'))

UniqueHHS <- sort(unique(MasterDistro$ISO3DataYearCovType))

IdealPLs <- c(seq(0.001,5,0.001),seq(5.01,60,0.01),seq(60.1,150,0.1),
              seq(150.5,1400,0.5), seq(1405,3000,5), seq(3010,10000,10),
              seq(11000,35000,100),99999)

##### Running the loop ####

total <- length(UniqueHHS)
pb <- tkProgressBar(title = "progress bar", min = 0,max = total, width = 300)

for (i in UniqueHHS[c(1:length(UniqueHHS))]){
  setTkProgressBar(pb, which(UniqueHHS==i), 
                   label=paste( round(which(UniqueHHS==i)/total*100, 3),"% done"))
  #print(i)
  Temp <- subset(MasterDistro,MasterDistro$ISO3DataYearCovType==i)
  if (!all(is.na(Temp$headcount))){
    NewEmptyRow <- MyEmptyRow
    
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
    
    Temp <- Temp[ order(Temp[,'povertyline']), ]
    TempNew <- Temp
    TempNew$Diffs <- c(1,diff(TempNew$headcount))
    y <- nrow(TempNew)
    while (any(TempNew$Diffs<0)){
      TempNew <- subset(TempNew,TempNew$Diffs>0)
      TempNew$Diffs <- c(1,diff(TempNew$headcount))
    }
    if (y>nrow(TempNew)){
      print(paste0('monotonicity alert at: ',i,' involving ',y-nrow(TempNew),' rows.'))
      TempAlert <- NewMonotonicityAlerts
      TempAlert$ID <- i
      TempAlert$NumOfBreaks <- y-nrow(TempNew)
      MonotonicityAlerts <- rbind(MonotonicityAlerts,TempAlert)
      rm(TempAlert)
    }
    NewEmptyRow$MonotonicityBreaks <- y-nrow(TempNew)
    TempNew <- TempNew[ order(TempNew[,'povertyline']), ]
    TempNew$Diffs <- c(1,diff(TempNew$headcount))
    TempShort <- subset(TempNew,(TempNew$headcount<0.8 & TempNew$Diffs>0.001) | (TempNew$headcount>=0.8 & TempNew$Diffs>0.0005))
    # if the above gives an error (as in "AUS:1988:NA:N:i") try the following:
    testDistro <- tryCatch(thresholds_fit(TempShort$headcount[c(1:nrow(TempShort)-1)], 
                                          365*TempShort$povertyline[c(1:nrow(TempShort)-1)],
                                          average = 12*unique(Temp$mean)),error=function(cond) {
                                            # Choose a return value in case of error
                                            return(T)
                                          })
    if (is.logical(testDistro)){
      TempShort <- subset(TempNew,(TempNew$headcount<0.8 & TempNew$Diffs>0.001) | (TempNew$headcount>=0.8 & TempNew$Diffs>0.001))
    }
    # if the above gives an error (as in "AUS:1993:NA:N:i") try the following:
    testDistro <- tryCatch(thresholds_fit(TempShort$headcount[c(1:nrow(TempShort)-1)], 
                                          365*TempShort$povertyline[c(1:nrow(TempShort)-1)],
                                          average = 12*unique(Temp$mean)),error=function(cond) {
                                            # Choose a return value in case of error
                                            return(T)
                                          })
    if (is.logical(testDistro)){
      TempShort <- subset(TempNew,(TempNew$headcount<0.8 & TempNew$Diffs>0.0012) | (TempNew$headcount>=0.8 & TempNew$Diffs>0.001))
    }
    # if the above gives an error (as in "AUT:1981:1987:N:i") try the following:
    testDistro <- tryCatch(thresholds_fit(TempShort$headcount[c(1:nrow(TempShort)-1)], 
                                          365*TempShort$povertyline[c(1:nrow(TempShort)-1)],
                                          average = 12*unique(Temp$mean)),error=function(cond) {
                                            # Choose a return value in case of error
                                            return(T)
                                          })
    if (is.logical(testDistro)){
      TempShort <- subset(TempNew,(TempNew$headcount<0.8 & TempNew$Diffs>0.0025) | (TempNew$headcount>=0.8 & TempNew$Diffs>0.001))
    }
    # if the above gives an error (as in "BEL:1981:1985:N:i") try the following:
    testDistro <- tryCatch(thresholds_fit(TempShort$headcount[c(1:nrow(TempShort)-1)], 
                                          365*TempShort$povertyline[c(1:nrow(TempShort)-1)],
                                          average = 12*unique(Temp$mean)),error=function(cond) {
                                            # Choose a return value in case of error
                                            return(T)
                                          })
    if (is.logical(testDistro)){
      TempShort <- subset(TempNew,(TempNew$headcount<0.8 & TempNew$Diffs>0.0025) | (TempNew$headcount>=0.8 & TempNew$Diffs>0.0025))
    }
    
    if (nrow(TempShort)<100){
      TempShort <- subset(TempNew,(TempNew$headcount<0.8 & TempNew$Diffs>0.0009) | (TempNew$headcount>=0.8 & TempNew$Diffs>0.0002))
    }
    # the command bellow did not work very well, big difference with the given PCN values when used 
    # to estimate MLD or Gini
    #TheDistroInProportions <- rep(TempShort$povertyline,round(10000*TempShort$headcount))
    # so I reverted to gpinter entirely
    
    # following the example from the gpinter-vignette.pdf on page 2:
    # TempShort <- subset(TempShort,!round(TempShort$headcount,4)==0.0544)
    #TempShort$PopulationInBracket <- diff(c(0,round(1000000*NewEmptyRow$Population*TempShort$headcount,0)))
    #TempShort$CumulativePopInBracket <- c(cumsum(TempShort$PopulationInBracket)[c(1:(nrow(TempShort)))])
    
    if (!is.na(unique(Temp$mean))){
      distribution <- thresholds_fit(TempShort$headcount[c(1:nrow(TempShort)-1)], 
                                     365*TempShort$povertyline[c(1:nrow(TempShort)-1)],
                                     average = 12*unique(Temp$mean))
    } else {
      distribution <- thresholds_fit(TempShort$headcount[c(1:nrow(TempShort)-1)], 
                                     365*TempShort$povertyline[c(1:nrow(TempShort)-1)])
    }
    
    
    GPinterDistro <- generate_tabulation(distribution,
                                         fractiles = c(seq(0.1, 0.9, 0.1)))
    
    GPinterDistroDetailed <- generate_tabulation(distribution,
                                         fractiles = c(seq(0.001, 0.999, 0.001)))
    
    # copy readily available info or easy (one-liners) to calculate
    # FirstRows
    NewEmptyRow$Entity <- unique(Temp$countrycode)
    NewEmptyRow$Year <-  unique(Temp$year)
    # GenStatsAndInfo
    NewEmptyRow$Mean <- unique(Temp$mean)
    NewEmptyRow$Mean_estimated <- bracket_average(distribution, 0, 1)/12
    NewEmptyRow$Median <- unique(Temp$median)
    NewEmptyRow$Median_estimated <- GPinterDistro$threshold[which(round(GPinterDistro$fractile,1)==0.5)]/12
    NewEmptyRow$PPP <- unique(Temp$ppp)
    NewEmptyRow$Population <- unique(Temp$population)
    # MetaColumns
    NewEmptyRow$isinterpolated <- unique(Temp$isinterpolated)
    NewEmptyRow$usemicrodata <- unique(Temp$usemicrodata)
    NewEmptyRow$coveragetype <- unique(Temp$coveragetype)
    NewEmptyRow$datatype <- unique(Temp$datatype)
    NewEmptyRow$usemicrodata <- unique(Temp$usemicrodata)
    NewEmptyRow$IsSurveyYear <- F
    NewEmptyRow$OriginalMedian <- ifelse(is.na(NewEmptyRow$Median),F,T)
    NewEmptyRow$OriginalMean <- ifelse(is.na(NewEmptyRow$Mean),F,T)
    NewEmptyRow$OriginalDecileShares <- 
    # IneqIndices
    NewEmptyRow$`Gini index` <- unique(Temp$gini)
    NewEmptyRow$Gini_estimated <- gini(distribution)
    NewEmptyRow$Polarization <- unique(Temp$polarization)
    # which polarization index definition?
    # https://www.sciencedirect.com/science/article/pii/S0165176518301046
    NewEmptyRow$Polarization_estimated <- NA
    NewEmptyRow$MLD <- unique(Temp$mld)
    NewEmptyRow$MLD_estimated <- entropy(GPinterDistroDetailed$threshold, parameter = 0)
    # The Palma ratio is the share of all income received by the 10% people with 
    # highest disposable income divided by the share of all income received by the 40%
    # https://data.oecd.org/inequality/income-inequality.htm
    NewEmptyRow$Palma <- bracket_share(distribution, 0.90, 1)/bracket_share(distribution, 0, 0.4)
    # The P90/P10 ratio is the ratio of the upper bound value of the ninth decile 
    # (i.e. the 10% of people with highest income) to that of the first. The P50/P10 
    # ratio is the ratio of median income to the upper bound value of the first decile.
    # (ibid)
    NewEmptyRow$`P90:P10 ratio` <- GPinterDistro$threshold[which(round(GPinterDistro$fractile,1)==0.9)]/
      GPinterDistro$threshold[which(round(GPinterDistro$fractile,1)==0.1)]
    NewEmptyRow$`P90:50 ratio` <- GPinterDistro$threshold[which(round(GPinterDistro$fractile,1)==0.9)]/
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
    # DecileSharesColumns
    NewEmptyRow$`Decile 1 – share of income or consumption` <- HHS2$decile1[which(HHS2$ISO3DataYearCovType==i)]
    NewEmptyRow$`Decile 2 – share of income or consumption` <- HHS2$decile2[which(HHS2$ISO3DataYearCovType==i)]
    NewEmptyRow$`Decile 3 – share of income or consumption` <- HHS2$decile3[which(HHS2$ISO3DataYearCovType==i)]
    NewEmptyRow$`Decile 4 – share of income or consumption` <- HHS2$decile4[which(HHS2$ISO3DataYearCovType==i)]
    NewEmptyRow$`Decile 5 – share of income or consumption` <- HHS2$decile5[which(HHS2$ISO3DataYearCovType==i)]
    NewEmptyRow$`Decile 6 – share of income or consumption` <- HHS2$decile6[which(HHS2$ISO3DataYearCovType==i)]
    NewEmptyRow$`Decile 7 – share of income or consumption` <- HHS2$decile7[which(HHS2$ISO3DataYearCovType==i)]
    NewEmptyRow$`Decile 8 – share of income or consumption` <- HHS2$decile8[which(HHS2$ISO3DataYearCovType==i)]
    NewEmptyRow$`Decile 9 – share of income or consumption` <- HHS2$decile9[which(HHS2$ISO3DataYearCovType==i)]
    NewEmptyRow$`Decile 10 – share of income or consumption` <- HHS2$decile10[which(HHS2$ISO3DataYearCovType==i)]
    # DecileThresholdsColumns
    NewEmptyRow$`Decile 1 – threshold of income or consumption` <- 
      GPinterDistro$threshold[which(round(GPinterDistro$fractile,1)==0.1)]
    NewEmptyRow$`Decile 2 – threshold of income or consumption` <- 
      GPinterDistro$threshold[which(round(GPinterDistro$fractile,1)==0.2)]
    NewEmptyRow$`Decile 3 – threshold of income or consumption` <- 
      GPinterDistro$threshold[which(round(GPinterDistro$fractile,1)==0.3)]
    NewEmptyRow$`Decile 4 – threshold of income or consumption` <- 
      GPinterDistro$threshold[which(round(GPinterDistro$fractile,1)==0.4)]
    NewEmptyRow$`Decile 5 – threshold of income or consumption` <- 
      GPinterDistro$threshold[which(round(GPinterDistro$fractile,1)==0.5)]
    NewEmptyRow$`Decile 6 – threshold of income or consumption` <- 
      GPinterDistro$threshold[which(round(GPinterDistro$fractile,1)==0.6)]
    NewEmptyRow$`Decile 7 – threshold of income or consumption` <- 
      GPinterDistro$threshold[which(round(GPinterDistro$fractile,1)==0.7)]
    NewEmptyRow$`Decile 8 – threshold of income or consumption` <- 
      GPinterDistro$threshold[which(round(GPinterDistro$fractile,1)==0.8)]
    NewEmptyRow$`Decile 9 – threshold of income or consumption` <- 
      GPinterDistro$threshold[which(round(GPinterDistro$fractile,1)==0.9)]
    
    # DecileAveragesColumns
    NewEmptyRow$`Decile 1 – average income or consumption` <- bracket_average(distribution, 0, 0.1)
    NewEmptyRow$`Decile 2 – average income or consumption` <- bracket_average(distribution, 0.1, 0.2)
    NewEmptyRow$`Decile 3 – average income or consumption` <- bracket_average(distribution, 0.2, 0.3)
    NewEmptyRow$`Decile 4 – average income or consumption` <- bracket_average(distribution, 0.3, 0.4)
    NewEmptyRow$`Decile 5 – average income or consumption` <- bracket_average(distribution, 0.4, 0.5)
    NewEmptyRow$`Decile 6 – average income or consumption` <- bracket_average(distribution, 0.5, 0.6)
    NewEmptyRow$`Decile 7 – average income or consumption` <- bracket_average(distribution, 0.6, 0.7)
    NewEmptyRow$`Decile 8 – average income or consumption` <- bracket_average(distribution, 0.7, 0.8)
    NewEmptyRow$`Decile 9 – average income or consumption` <- bracket_average(distribution, 0.8, 0.9)
    NewEmptyRow$`Decile 10 – average income or consumption` <- bracket_average(distribution, 0.9, 1)
    
    # now get the information that is at some row within the Temp dataframe:
    NewEmptyRow$`$1.9 per day - share of population below poverty line` <- 
      Temp$headcount[which(round(Temp$povertyline,3)==1.900)]
    NewEmptyRow$`$3.2 per day - share of population below poverty line` <- 
      Temp$headcount[which(round(Temp$povertyline,3)==3.200)]
    NewEmptyRow$`$5.5 per day - share of population below poverty line` <- 
      Temp$headcount[which(round(Temp$povertyline,3)==5.500)]
    NewEmptyRow$`$10 per day - share of population below poverty line` <- 
      Temp$headcount[which(round(Temp$povertyline,3)==10.000)]
    NewEmptyRow$`$15 per day - share of population below poverty line` <- 
      Temp$headcount[which(round(Temp$povertyline,3)==15.000)]
    NewEmptyRow$`$20 per day - share of population below poverty line` <- 
      Temp$headcount[which(round(Temp$povertyline,3)==20.000)]
    NewEmptyRow$`$30 per day - share of population below poverty line` <- 
      Temp$headcount[which(round(Temp$povertyline,3)==30.000)]
    NewEmptyRow$`$40 per day - share of population below poverty line` <- 
      Temp$headcount[which(round(Temp$povertyline,3)==40.000)]
    
    NewEmptyRow$`$1.9 per day - total number of people below poverty line` <- 
      round(Temp$headcount[which(round(Temp$povertyline,3)==1.900)]*1000000*unique(Temp$population))
    NewEmptyRow$`$3.2 per day - total number of people below poverty line` <- 
      round(Temp$headcount[which(round(Temp$povertyline,3)==3.200)]*1000000*unique(Temp$population))
    NewEmptyRow$`$5.5 per day - total number of people below poverty line` <- 
      round(Temp$headcount[which(round(Temp$povertyline,3)==5.500)]*1000000*unique(Temp$population))
    NewEmptyRow$`$10 per day - total number of people below poverty line` <- 
      round(Temp$headcount[which(round(Temp$povertyline,3)==10.000)]*1000000*unique(Temp$population))
    NewEmptyRow$`$15 per day - total number of people below poverty line` <- 
      round(Temp$headcount[which(round(Temp$povertyline,3)==15.000)]*1000000*unique(Temp$population))
    NewEmptyRow$`$20 per day - total number of people below poverty line` <- 
      round(Temp$headcount[which(round(Temp$povertyline,3)==20.000)]*1000000*unique(Temp$population))
    NewEmptyRow$`$30 per day - total number of people below poverty line` <- 
      round(Temp$headcount[which(round(Temp$povertyline,3)==30.000)]*1000000*unique(Temp$population))
    NewEmptyRow$`$40 per day - total number of people below poverty line` <- 
      round(Temp$headcount[which(round(Temp$povertyline,3)==40.000)]*1000000*unique(Temp$population))
    
    #Absolute poverty gap (expressed in annual terms)
    #[FYI, this is the amount of money (theoretically) needed to bring everyone up to the poverty line, expressed in annual terms]
    #Derived as:
    #  = poverty_gap_index x poverty_line x population x 365
    NewEmptyRow$`$1.9 per day - absolute poverty gap` <- Temp$povertygap[which(round(Temp$povertyline,3)==1.900)]*1.9*365
    #Poverty gap index (as per WB/Ravallion terminology)
    NewEmptyRow$`$1.9 per day - poverty gap index` <- Temp$povertygap[which(round(Temp$povertyline,3)==1.900)]
    #‘Income gap ratio’ (According to Ravallion)
    IGPdata <- GPinterDistroDetailed$threshold[which(GPinterDistroDetailed$threshold<=365*1.9)]/365
    NewEmptyRow$`$1.9 per day - income gap ratio` <- mean((1.9-IGPdata)/1.9)
    rm(IGPdata)
    NewEmptyRow$`$1.9 per day - watts index` <- Temp$watts[which(round(Temp$povertyline,3)==1.900)]
    #Watts(GPinterDistroDetailed$threshold,365*1.9)
    
    NewEmptyRow$`$3.2 per day - absolute poverty gap` <- Temp$povertygap[which(round(Temp$povertyline,3)==3.200)]*3.2*365
    NewEmptyRow$`$3.2 per day - poverty gap index` <- Temp$povertygap[which(round(Temp$povertyline,3)==3.200)]
    IGPdata <- GPinterDistroDetailed$threshold[which(GPinterDistroDetailed$threshold<=365*3.2)]/365
    NewEmptyRow$`$3.2 per day - income gap ratio` <- mean((3.2-IGPdata)/3.2)
    rm(IGPdata)
    NewEmptyRow$`$3.2 per day - watts index` <- Temp$watts[which(round(Temp$povertyline,3)==3.200)]
    
    NewEmptyRow$`$5.5 per day - absolute poverty gap` <- Temp$povertygap[which(round(Temp$povertyline,3)==5.500)]*5.5*365
    NewEmptyRow$`$5.5 per day - poverty gap index` <- Temp$povertygap[which(round(Temp$povertyline,3)==5.500)]
    IGPdata <- GPinterDistroDetailed$threshold[which(GPinterDistroDetailed$threshold<=365*5.5)]/365
    NewEmptyRow$`$5.5 per day - income gap ratio` <- mean((5.5-IGPdata)/5.5)
    rm(IGPdata)
    NewEmptyRow$`$5.5 per day - watts index` <- Temp$watts[which(round(Temp$povertyline,3)==5.500)]
    
    NewEmptyRow$`$10 per day - absolute poverty gap` <- Temp$povertygap[which(round(Temp$povertyline,3)==10.000)]*10*365
    NewEmptyRow$`$10 per day - poverty gap index` <- Temp$povertygap[which(round(Temp$povertyline,3)==10.000)]
    IGPdata <- GPinterDistroDetailed$threshold[which(GPinterDistroDetailed$threshold<=365*10)]/365
    NewEmptyRow$`$10 per day - income gap ratio` <- mean((10-IGPdata)/10)
    rm(IGPdata)
    NewEmptyRow$`$10 per day - watts index` <- Temp$watts[which(round(Temp$povertyline,3)==10.000)]
    
    NewEmptyRow$`$15 per day - absolute poverty gap` <- Temp$povertygap[which(round(Temp$povertyline,3)==15.000)]*15*365
    NewEmptyRow$`$15 per day - poverty gap index` <- Temp$povertygap[which(round(Temp$povertyline,3)==15.000)]
    IGPdata <- GPinterDistroDetailed$threshold[which(GPinterDistroDetailed$threshold<=365*15)]/365
    NewEmptyRow$`$15 per day - income gap ratio` <- mean((15-IGPdata)/15)
    rm(IGPdata)
    NewEmptyRow$`$15 per day - watts index` <- Temp$watts[which(round(Temp$povertyline,3)==15.000)]
    
    NewEmptyRow$`$20 per day - absolute poverty gap` <- Temp$povertygap[which(round(Temp$povertyline,3)==20.000)]*20*365
    NewEmptyRow$`$20 per day - poverty gap index` <- Temp$povertygap[which(round(Temp$povertyline,3)==20.000)]
    IGPdata <- GPinterDistroDetailed$threshold[which(GPinterDistroDetailed$threshold<=365*20)]/365
    NewEmptyRow$`$20 per day - income gap ratio` <- mean((20-IGPdata)/20)
    rm(IGPdata)
    NewEmptyRow$`$20 per day - watts index` <- Temp$watts[which(round(Temp$povertyline,3)==20.000)]
    
    NewEmptyRow$`$30 per day - absolute poverty gap` <- Temp$povertygap[which(round(Temp$povertyline,3)==30.000)]*30*365
    NewEmptyRow$`$30 per day - poverty gap index` <- Temp$povertygap[which(round(Temp$povertyline,3)==30.000)]
    IGPdata <- GPinterDistroDetailed$threshold[which(GPinterDistroDetailed$threshold<=365*30)]/365
    NewEmptyRow$`$30 per day - income gap ratio` <- mean((30-IGPdata)/30)
    rm(IGPdata)
    NewEmptyRow$`$30 per day - watts index` <- Temp$watts[which(round(Temp$povertyline,3)==30.000)]
    
    NewEmptyRow$`$40 per day - absolute poverty gap` <- Temp$povertygap[which(round(Temp$povertyline,3)==40.000)]*40*365
    NewEmptyRow$`$40 per day - poverty gap index` <- Temp$povertygap[which(round(Temp$povertyline,3)==40.000)]
    IGPdata <- GPinterDistroDetailed$threshold[which(GPinterDistroDetailed$threshold<=365*40)]/365
    NewEmptyRow$`$40 per day - income gap ratio` <- mean((40-IGPdata)/40)
    rm(IGPdata)
    NewEmptyRow$`$40 per day - watts index` <- Temp$watts[which(round(Temp$povertyline,3)==40.000)]
    
    if (NewEmptyRow$OriginalMedian){
      PL40 <- IdealPLs[which.min(abs(IdealPLs-round(.4*12*NewEmptyRow$Median/365,3)))][1]
      NewEmptyRow$`$40% of median income - share of population below poverty line` <- 
        Temp$headcount[which(round(Temp$povertyline,3)==round(PL40,3))]
      NewEmptyRow$`$40% of median income - poverty gap index` <-  
        Temp$povertygap[which(round(Temp$povertyline,3)==round(PL40,3))]
      NewEmptyRow$`$40% of median income - total number of people below poverty line` <- 
        round(Temp$headcount[which(round(Temp$povertyline,3)==round(PL40,3))]*
        1000000*NewEmptyRow$Population)
      NewEmptyRow$`$40% of median income - absolute poverty gap` <-  
        Temp$povertygap[which(round(Temp$povertyline,3)==round(PL40,3))]*
        round(PL40,3)*365
      IGPdata <- GPinterDistroDetailed$threshold[which(GPinterDistroDetailed$threshold<=365*PL40)]/365
      NewEmptyRow$`$40% of median income - income gap ratio` <- mean((PL40-IGPdata)/PL40)
      rm(IGPdata)
      NewEmptyRow$`$40% of median income - watts index` <- 
        Temp$watts[which(round(Temp$povertyline,3)==round(PL40,3))]
      rm(PL40)
      
      PL50 <- IdealPLs[which.min(abs(IdealPLs-round(.5*12*NewEmptyRow$Median/365,3)))][1]
      NewEmptyRow$`$50% of median income - share of population below poverty line` <- 
        Temp$headcount[which(round(Temp$povertyline,3)==round(PL50,3))]
      NewEmptyRow$`$50% of median income - poverty gap index` <-  
        Temp$povertygap[which(round(Temp$povertyline,3)==round(PL50,3))]
      NewEmptyRow$`$50% of median income - total number of people below poverty line` <- 
        round(Temp$headcount[which(round(Temp$povertyline,3)==round(PL50,3))]*
                1000000*NewEmptyRow$Population)
      NewEmptyRow$`$50% of median income - absolute poverty gap` <- 
        Temp$povertygap[which(round(Temp$povertyline,3)==round(PL50,3))]*
        round(PL50,3)*365
      IGPdata <- GPinterDistroDetailed$threshold[which(GPinterDistroDetailed$threshold<=365*PL50)]/365
      NewEmptyRow$`$50% of median income - income gap ratio` <- mean((PL50-IGPdata)/PL50)
      rm(IGPdata)
      NewEmptyRow$`$50% of median income - watts index` <- 
        Temp$watts[which(round(Temp$povertyline,3)==round(PL50,3))]
      rm(PL50)
      
      PL60 <- IdealPLs[which.min(abs(IdealPLs-round(.6*12*NewEmptyRow$Median/365,3)))][1]
      NewEmptyRow$`$60% of median income - share of population below poverty line` <- 
        Temp$headcount[which(round(Temp$povertyline,3)==round(PL60,3))]
      NewEmptyRow$`$60% of median income - poverty gap index` <-  
        Temp$povertygap[which(round(Temp$povertyline,3)==round(PL60,3))]
      NewEmptyRow$`$60% of median income - total number of people below poverty line` <- 
        round(Temp$headcount[which(round(Temp$povertyline,3)==round(PL60,3))]*
                1000000*NewEmptyRow$Population)
      NewEmptyRow$`$60% of median income - absolute poverty gap` <- 
        Temp$povertygap[which(round(Temp$povertyline,3)==round(PL60,3))]*
        round(PL60,3)*365
      IGPdata <- GPinterDistroDetailed$threshold[which(GPinterDistroDetailed$threshold<=365*PL60)]/365
      NewEmptyRow$`$60% of median income - income gap ratio` <- mean((PL60-IGPdata)/PL60)
      rm(IGPdata)
      NewEmptyRow$`$60% of median income - watts index` <- 
        Temp$watts[which(round(Temp$povertyline,3)==round(PL60,3))]
      rm(PL60)
    } else {
      PL40 <- IdealPLs[which.min(abs(IdealPLs-round(.4*12*NewEmptyRow$Median_estimated/365,3)))][1]
      NewEmptyRow$`$40% of median income - share of population below poverty line` <- 
        Temp$headcount[which(round(Temp$povertyline,3)==round(PL40,3))]
      NewEmptyRow$`$40% of median income - poverty gap index` <-  
        Temp$povertygap[which(round(Temp$povertyline,3)==round(PL40,3))]
      NewEmptyRow$`$40% of median income - total number of people below poverty line` <- 
        round(Temp$headcount[which(round(Temp$povertyline,3)==round(PL40,3))]*
                1000000*NewEmptyRow$Population)
      NewEmptyRow$`$40% of median income - absolute poverty gap` <-  
        Temp$povertygap[which(round(Temp$povertyline,3)==round(PL40,3))]*
        round(PL40,3)*365
      IGPdata <- GPinterDistroDetailed$threshold[which(GPinterDistroDetailed$threshold<=365*PL40)]/365
      NewEmptyRow$`$40% of median income - income gap ratio` <- mean((PL40-IGPdata)/PL40)
      rm(IGPdata)
      NewEmptyRow$`$40% of median income - watts index` <- 
        Temp$watts[which(round(Temp$povertyline,3)==round(PL40,3))]
      rm(PL40)
      
      PL50 <- IdealPLs[which.min(abs(IdealPLs-round(.5*12*NewEmptyRow$Median_estimated/365,3)))][1]
      NewEmptyRow$`$50% of median income - share of population below poverty line` <- 
        Temp$headcount[which(round(Temp$povertyline,3)==round(PL50,3))]
      NewEmptyRow$`$50% of median income - poverty gap index` <-  
        Temp$povertygap[which(round(Temp$povertyline,3)==round(PL50,3))]
      NewEmptyRow$`$50% of median income - total number of people below poverty line` <- 
        round(Temp$headcount[which(round(Temp$povertyline,3)==round(PL50,3))]*
                1000000*NewEmptyRow$Population)
      NewEmptyRow$`$50% of median income - absolute poverty gap` <- 
        Temp$povertygap[which(round(Temp$povertyline,3)==round(PL50,3))]*
        round(PL50,3)*365
      IGPdata <- GPinterDistroDetailed$threshold[which(GPinterDistroDetailed$threshold<=365*PL50)]/365
      NewEmptyRow$`$50% of median income - income gap ratio` <- mean((PL50-IGPdata)/PL50)
      rm(IGPdata)
      NewEmptyRow$`$50% of median income - watts index` <- 
        Temp$watts[which(round(Temp$povertyline,3)==round(PL50,3))]
      rm(PL50)
      
      PL60 <- IdealPLs[which.min(abs(IdealPLs-round(.6*12*NewEmptyRow$Median_estimated/365,3)))][1]
      NewEmptyRow$`$60% of median income - share of population below poverty line` <- 
        Temp$headcount[which(round(Temp$povertyline,3)==round(PL60,3))]
      NewEmptyRow$`$60% of median income - poverty gap index` <-  
        Temp$povertygap[which(round(Temp$povertyline,3)==round(PL60,3))]
      NewEmptyRow$`$60% of median income - total number of people below poverty line` <- 
        round(Temp$headcount[which(round(Temp$povertyline,3)==round(PL60,3))]*
                1000000*NewEmptyRow$Population)
      NewEmptyRow$`$60% of median income - absolute poverty gap` <- 
        Temp$povertygap[which(round(Temp$povertyline,3)==round(PL60,3))]*
        round(PL60,3)*365
      IGPdata <- GPinterDistroDetailed$threshold[which(GPinterDistroDetailed$threshold<=365*PL60)]/365
      NewEmptyRow$`$60% of median income - income gap ratio` <- mean((PL60-IGPdata)/PL60)
      rm(IGPdata)
      NewEmptyRow$`$60% of median income - watts index` <- 
        Temp$watts[which(round(Temp$povertyline,3)==round(PL60,3))]
      rm(PL60)
    }
    
    # NewEmptyRow[,which(is.na(NewEmptyRow[1,]))]
    ExportDataFrame <- rbind(ExportDataFrame,NewEmptyRow)
    rm(NewEmptyRow,distribution)
  }
}
close(pb)

save(list = 'ExportDataFrame',file = '~/PhD/Sources/OWID/ExportDataFrame.RData')
# Now check which is original and which not
