library(jsonlite)
library(dplyr)
library(ggplot2)
library(janitor)

download.file('https://stats.oecd.org/sdmx-json/data/DP_LIVE/.HEALTHEXP.../OECD?contentType=csv&detail=code&separator=comma&csv-lang=en', 'data/oecd_stat.csv' )
download.file('https://ghoapi.azureedge.net/api/GHED_GGHE-DGDP_SHA2011', 'data/GHED_GGHE-DGDP_SHA2011.json')


owid <- clean_names(read.csv("data/public-health-expenditure-share-GDP-OWID.csv")) %>% filter(between(year, 1959,1971)) %>% select(entity, code, year, value =public_expenditure_on_health_gdp_owid_extrapolated_series)

oecd_93 <- read.csv("data/OECD 1993.csv") %>% pivot_longer(starts_with('X')) %>% mutate(entity = year, year = as.numeric(gsub("X","",name)), source = 'oecd_93') %>% select(entity,year, value, source )

oecd_93_roc <- oecd_93 %>% 
  select(entity, year, value) %>% 
  filter(between(year, 1960, 1970)) %>% 
  group_by(entity) %>% 
  mutate(time_m1 = lag(value, n = 1L), br_roc = time_m1/value) %>% 
  select(entity, year, br_roc) %>% 
  ungroup() %>% 
  filter(complete.cases(.))

oecd <- read.csv("data/oecd_stat.csv") %>% filter(SUBJECT == 'TOT' & MEASURE == 'PC_GDP') %>% select(entity = LOCATION, year = TIME,value = Value ) %>% mutate(source = 'oecd_stat')

who <- fromJSON('data/GHED_GGHE-DGDP_SHA2011.json') 
who <- who$value

who <- who %>% filter(SpatialDimType == 'COUNTRY') %>% select(entity = SpatialDim, year = TimeDim,value =  NumericValue) %>% mutate(source = 'who_gho')

who_oecd <- rbind(who, oecd)

who_oecd_plot <- who_oecd %>% 
  group_by(year,entity ) %>% 
  add_count() %>% 
  filter(n >1) %>% 
  group_by(entity) 




ggplot(who_oecd_plot)+
  geom_line(aes(x = year, y= value, group = interaction(entity,source), colour = source), alpha = 0.5)+
  facet_wrap(.~ entity)+
  labs(y = 'Health Expenditure (% of GDP)', x = "Year", colour = "Source")+
  theme_bw()
  


ggplot()+
  geom_line(data = who_oecd_plot %>% filter(source == 'who_gho'), aes(x = year, y= value, group = interaction(entity,source), colour = source), alpha = 0.5, size = 2.5)+
  geom_line(data = who_oecd_plot %>% filter(source == 'oecd_stat'), aes(x = year, y= value, group = interaction(entity,source), colour = source))+
  facet_wrap(.~ entity)+
  labs(y = 'Health Expenditure (% of GDP)', x = "Year", colour = "Source")+
  theme_bw()+
  theme(text = element_text(size=12))


oecd_roc <- oecd %>% 
  select(entity, year, value) %>% 
  group_by(entity) %>% 
  mutate(time_m1 = lag(value, n = 1L), br_roc = time_m1/value) %>% 
  select(entity, year = year, br_roc) %>% 
  ungroup() %>% 
  filter(complete.cases(.))


roc_df <- rbind(owid_roc, oecd_roc)


years <- 2000:1960 
who_out <- who%>% 
  select(entity, year, value)
for (year_sel in years){
  
  roc_yr <- roc_df %>% filter(year == year_sel)
  
  who_new <- who_out %>% filter(year == year_sel) %>% 
    left_join(., roc_yr, by = 'entity') %>% 
    mutate(value= value*br_roc, year = year_sel-1) %>% 
    select(entity, year, value)
  
  who_out <- rbind(who_out, who_new)
  
}

lindert <- read.csv("data/lindert_1880_1930.csv") %>% select(entity,year, value = public_expenditure_on_health)

full_owid <- rbind(who_out, lindert)

full_lines = who_out$entity[which(who_out$year == 1970 & !is.na(who_out$value))]


ggplot()+
  geom_line(data = who_out %>% filter(entity%in% full_lines), aes(x = year, y = value, group = entity, colour = entity))+
  geom_line(data = who %>% filter(entity %in% full_lines), aes(x = year, y = value, group = entity, colour = entity, size = 2, alpha = 0.4) )









#### standardise country names - should do iso and countries separately

countries <- full_owid['SpatialDim']
colnames(countries)<- "Country"
write.csv(countries, "data/country_names.csv", row.names = FALSE)

countries <- read.csv("data/country_names_country_standardized.csv") %>% distinct()
####

full_owid <- full_owid %>% 
  left_join(., countries, by = c('entity'= 'Country')) %>% 
  select(entity = Our.World.In.Data.Name, year = year, public_health_expenditure_pc_gdp = value) %>% 
  filter(complete.cases(.))
  
full_lines = full_owid$entity[which(full_owid$year == 1970 & !is.na(full_owid$public_health_expenditure_pc_gdp))]


ggplot()+
  geom_line(data = full_owid %>% filter(entity %in% full_lines), aes(x = year, y = public_health_expenditure_pc_gdp, group = entity, colour = entity))
  

write.csv(full_owid, "data/OMM_public_health_expenditure_pc_gdp_new.csv", row.names = FALSE)

