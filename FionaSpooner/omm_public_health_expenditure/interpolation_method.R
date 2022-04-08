years <- 1990:1996

phe_pcnt <- c(5.380,5.330,rep(NA,3),5.067,4.782)

df_phe <- data.frame(year = years, phe_pcnt = phe_pcnt)

# Estimate annual rate of change going backwards in time - 1996-1990 annual

df_phe <- df_phe %>% 
  mutate(time_m1 = lag(phe_pcnt, n = 1L), roc = phe_pcnt/time_m1) %>% select(year, phe_pcnt, roc)
df_phe

# method 1 - linearly interpolate

df_phe <- df_phe %>% 
  mutate(roc_app = na.approx(roc, na.rm = FALSE))

df_phe


# method 2 - log 

multiplier <- df_phe %>% 
  filter(!is.na(roc)) %>% 
  mutate(missing_years = max(year) - min(year), roc_diff =roc[which.min(year)]/roc[which.max(year)],
         multiplier = 10^(log10(roc_diff)/missing_years)) %>% 
  select(multiplier) %>% distinct() %>% pull()

df_phe
df_phe$roc_log<- df_phe$roc
for (row in nrow(df_phe):2){
  print(row)
  
  df_phe$roc_log[row-1] <- df_phe$roc_log[row] * multiplier
  
}
df_phe

##### which makes more sense

df_phe$phe_log<- df_phe$phe_pcnt
df_phe$phe_app<- df_phe$phe_pcnt

for (row in 5:1){
  print(row)
  
  df_phe$phe_log[row] <- df_phe$roc_log[row+1] *  df_phe$phe_log[row+ 1 ]
  df_phe$phe_app[row] <- df_phe$roc_app[row+1] *  df_phe$phe_app[row+ 1 ]
}
df_phe









