library(dplyr) 


percPop <- function(data,inc_concept_varname,weight="wt",povline) {
  
  # rename to handle dynamic varname more easily
  data_alt<- data %>% 
    rename(inc_concept := !!inc_concept_varname)
  
  res <- 100 * (sum((data_alt$inc_concept< povline) * data_alt[,paste(weight)]) / sum(data_alt[,paste(weight)]))
  return(res)
}

setups <- function(df) {
  hfile    <- paste(df,'h',sep='')
  dsh      <- read.LIS(hfile, vars=c("did","hid","nhhmem","dhi","hwgt"), subset="!is.na(dhi) & dhi !=0 & !is.na(hwgt)",labels=FALSE)
  dsh$ey   <- dsh$dhi  / sqrt(dsh$nhhmem) # sq root equivalised household income
  dsh$pcy   <- dsh$dhi  / dsh$nhhmem # per capita household income
  dsh$wt   <- dsh$hwgt * dsh$nhhmem
  # dsh      <- lisTopBottom(dsh,'dhi','ey','wt')	
  return(dsh)
}


PPP_conversion<- function(data, var_to_convert_name, new_varname, PPP_year){
  
  # rename to handle dynamic varname more easily
  data<- data %>%
    rename(var_to_convert := !!var_to_convert_name)
  
  if(PPP_year == 2011){
    
    data<- left_join(data, LIS_PPPs_2011) %>%
      mutate(!!new_varname := var_to_convert/lisppp_2011) 
      
  }
  
  if(PPP_year == 2017){
    
    data<- left_join(data, LIS_PPPs_2017) %>%
      mutate(!!new_varname := var_to_convert/lisppp_2017)

  }
  
  # rename var back to original
  data<- data %>%
    rename(!!var_to_convert_name := var_to_convert)
  
  return(data)
  
}



# Grab LIS PPPs (which adjust for CPI up to reference year and then PPPs 
# across countries in the reference year) 

LIS_PPPs_2011<- read.dta13(paste(INC_DIR, "ppp_2011.dta", sep=""),convert.factors=FALSE) %>% 
  mutate(survey_code = paste0(toupper(iso2), substr(year, start = 3, stop = 4))) %>% 
  rename(lisppp_2011 = lisppp) %>% 
  select(survey_code, lisppp_2011) 

LIS_PPPs_2017<- read.dta13(paste(INC_DIR, "ppp_2017.dta", sep=""),convert.factors=FALSE) %>% 
  mutate(survey_code = paste0(toupper(iso2), substr(year, start = 3, stop = 4))) %>% 
  rename(lisppp_2017 = lisppp) %>% 
  select(survey_code, lisppp_2017) 



#--------------------------#
#  Share under int$ threshold   #
#--------------------------#


# A data frame to store results 
output<- data.frame("survey_code" = character(), 
                    "poverty_line" = numeric(), 
                    "income_concept" = character())



surveys   <- c('AU14', 'AU10', 'AU08', 'AU04', 'AU03', 'AU01', 'AU95', 'AU89', 'AU85', 'AU81', 'AT16', 'AT13', 'AT10', 'AT07', 'AT04', 'AT00', 'AT97', 'AT95', 'AT94', 'AT87', 'BE17', 'BE16', 'BE15', 'BE14', 'BE13', 'BE12', 'BE11', 'BE10', 'BE09', 'BE08', 'BE07', 'BE06', 'BE05', 'BE04', 'BE03', 'BE00', 'BE97', 'BE95', 'BE92', 'BE88', 'BE85', 'BR16', 'BR13', 'BR11', 'BR09', 'BR06', 'CA17', 'CA16', 'CA15', 'CA14', 'CA13', 'CA12', 'CA10', 'CA07', 'CA04', 'CA00', 'CA98', 'CA97', 'CA94', 'CA91', 'CA87', 'CA81', 'CA75', 'CA71', 'CL17', 'CL15', 'CL13', 'CL11', 'CL09', 'CL06', 'CL03', 'CL00', 'CL98', 'CL96', 'CL94', 'CL92', 'CL90', 'CN13', 'CN02', 'CO16', 'CO13', 'CO10', 'CO07', 'CO04', 'CI15', 'CI08', 'CI02', 'CZ16', 'CZ13', 'CZ10', 'CZ07', 'CZ04', 'CZ02', 'CZ96', 'CZ92', 'DK16', 'DK13', 'DK10', 'DK07', 'DK04', 'DK00', 'DK95', 'DK92', 'DK87', 'DO07', 'EG12', 'EE16', 'EE13', 'EE10', 'EE07', 'EE04', 'EE00', 'FI16', 'FI13', 'FI10', 'FI07', 'FI04', 'FI00', 'FI95', 'FI91', 'FI87', 'FR10', 'FR05', 'FR00', 'FR94', 'FR89', 'FR84', 'FR78', 'GE19', 'GE18', 'GE17', 'GE16', 'GE15', 'GE14', 'GE13', 'GE12', 'GE11', 'GE10', 'GE09', 'DE18', 'DE17', 'DE16', 'DE15', 'DE14', 'DE13', 'DE12', 'DE11', 'DE10', 'DE09', 'DE08', 'DE07', 'DE06', 'DE05', 'DE04', 'DE03', 'DE02', 'DE01', 'DE00', 'DE99', 'DE98', 'DE97', 'DE96', 'DE95', 'DE94', 'DE93', 'DE92', 'DE91', 'DE90', 'DE89', 'DE88', 'DE87', 'DE86', 'DE85', 'DE84', 'DE83', 'DE81', 'DE78', 'DE73', 'GR16', 'GR13', 'GR10', 'GR07', 'GR04', 'GR00', 'GR95', 'GT14', 'GT11', 'GT06', 'HU15', 'HU12', 'HU09', 'HU07', 'HU05', 'HU99', 'HU94', 'HU91', 'IS10', 'IS07', 'IS04', 'IN11', 'IN04', 'IE17', 'IE16', 'IE15', 'IE14', 'IE13', 'IE12', 'IE11', 'IE10', 'IE09', 'IE08', 'IE07', 'IE06', 'IE05', 'IE04', 'IE03', 'IE02', 'IE00', 'IE96', 'IE95', 'IE94', 'IE87', 'IL18', 'IL17', 'IL16', 'IL15', 'IL14', 'IL13', 'IL12', 'IL11', 'IL10', 'IL09', 'IL08', 'IL07', 'IL06', 'IL05', 'IL04', 'IL03', 'IL02', 'IL01', 'IL97', 'IL92', 'IL86', 'IL79', 'IT16', 'IT14', 'IT10', 'IT08', 'IT04', 'IT00', 'IT98', 'IT95', 'IT93', 'IT91', 'IT89', 'IT87', 'IT86', 'JP13', 'JP10', 'JP08', 'LT18', 'LT17', 'LT16', 'LT15', 'LT14', 'LT13', 'LT12', 'LT11', 'LT10', 'LT09', 'LU13', 'LU10', 'LU07', 'LU04', 'LU00', 'LU97', 'LU94', 'LU91', 'LU85', 'MX18', 'MX16', 'MX14', 'MX12', 'MX10', 'MX08', 'MX06', 'MX05', 'MX04', 'MX02', 'MX00', 'MX98', 'MX96', 'MX94', 'MX92', 'MX89', 'MX84', 'NL18', 'NL17', 'NL16', 'NL15', 'NL13', 'NL10', 'NL07', 'NL04', 'NL99', 'NL93', 'NL90', 'NL87', 'NL83', 'NO16', 'NO13', 'NO10', 'NO07', 'NO04', 'NO00', 'NO95', 'NO91', 'NO86', 'NO79', 'PS17', 'PA16', 'PA13', 'PA10', 'PA07', 'PY16', 'PY13', 'PY10', 'PY07', 'PY04', 'PY00', 'PE16', 'PE13', 'PE10', 'PE07', 'PE04', 'PL16', 'PL13', 'PL10', 'PL07', 'PL04', 'PL99', 'PL95', 'PL92', 'PL86', 'RO97', 'RO95', 'RU18', 'RU17', 'RU16', 'RU15', 'RU14', 'RU13', 'RU11', 'RU10', 'RU07', 'RU04', 'RU00', 'RS16', 'RS13', 'RS10', 'RS06', 'SK18', 'SK17', 'SK16', 'SK15', 'SK14', 'SK13', 'SK10', 'SK07', 'SK04', 'SK96', 'SK92', 'SI15', 'SI12', 'SI10', 'SI07', 'SI04', 'SI99', 'SI97', 'ZA17', 'ZA15', 'ZA12', 'ZA10', 'ZA08', 'KR16', 'KR14', 'KR12', 'KR10', 'KR08', 'KR06', 'ES16', 'ES13', 'ES10', 'ES07', 'ES04', 'ES00', 'ES95', 'ES90', 'ES85', 'ES80', 'SE05', 'SE00', 'SE95', 'SE92', 'SE87', 'SE81', 'SE75', 'SE67', 'CH18', 'CH17', 'CH16', 'CH15', 'CH14', 'CH13', 'CH12', 'CH11', 'CH10', 'CH09', 'CH08', 'CH07', 'CH06', 'CH04', 'CH02', 'CH00', 'CH92', 'CH82', 'TW16', 'TW13', 'TW10', 'TW07', 'TW05', 'TW00', 'TW97', 'TW95', 'TW91', 'TW86', 'TW81', 'UK18', 'UK17', 'UK16', 'UK15', 'UK14', 'UK13', 'UK12', 'UK11', 'UK10', 'UK09', 'UK08', 'UK07', 'UK06', 'UK05', 'UK04', 'UK03', 'UK02', 'UK01', 'UK00', 'UK99', 'UK98', 'UK97', 'UK96', 'UK95', 'UK94', 'UK91', 'UK86', 'UK79', 'UK74', 'UK69', 'US19', 'US18', 'US17', 'US16', 'US15', 'US14', 'US13', 'US12', 'US11', 'US10', 'US09', 'US08', 'US07', 'US06', 'US05', 'US04', 'US03', 'US02', 'US01', 'US00', 'US99', 'US98', 'US97', 'US96', 'US95', 'US94', 'US93', 'US92', 'US91', 'US86', 'US79', 'US74', 'UY16', 'UY13', 'UY10', 'UY07', 'UY04', 'VN13', 'VN11')


for (survey in surveys) {
  
  # Grab micro data and set up using LIS' standard code
  df <- setups(survey) %>%
    mutate(survey_code = survey) # add a 'survey code' var
  
  # run the PPP conversion on equivalised and per cap income vars
  df <- PPP_conversion(df, "ey", "ey_PPP_2011", 2011)
  df <- PPP_conversion(df, "pcy", "pcy_PPP_2011", 2011)
  
  

  
  # for each poverty line
  for (pov_line in c(10,30,50)) {
    
    # for each income concept
    for (y_var in c("ey_PPP_2011","pcy_PPP_2011")){
      
      # calculate the share under the line
      pov_estimate<- round(percPop(data=df, 
                                   inc_concept = y_var, 
                                   povline = pov_line*365),
                           digits=3)
      
      # Make a one-row dataframe to store this result
      this_estimate<- data.frame("survey_code" = survey, 
                                 "poverty_line" = pov_line, 
                                 "income_concept" = y_var)
      
      # append the data for this result to the running data frame of all results
      output<- rbind(output, this_estimate) 
      
    }
      
  }
  
  
}



# Print the output data frame (as sort of comma separated for copying and pasting) 
print(write.csv(output, row.names = FALSE))

