library(gpinter)
library(tidyverse)
library(dineq)






df<- read.csv('https://joeh.fra1.digitaloceanspaces.com/phd_global_dist/percentiles_from_PIP.csv')

head(df)


head(df %>% filter(p==0.99), n=20)

# Merge in standard variables from any API response

df_standard<- read.csv('https://joeh.fra1.digitaloceanspaces.com/PIP/example_response_filled.csv')

df_standard<- df_standard %>%
select(entity, reporting_year, welfare_type, reporting_level, reporting_pop, reporting_gdp, mean) %>%
rename(year = reporting_year)

df<- left_join(df, df_standard)

head(df)

# ### Select only national entities, unless only sub-national available

# Check if only subnational estimates are available for some countries

# Count how many reporting levels there are for each estimate
count_reporting_levels<- df %>%
 count(entity, year, p) %>%
 rename(number_of_reporting_levels = n)

# Merge the counts back into dataframe
df<- left_join(df, count_reporting_levels)

# Filter to see if there are any cases where only non-national estimates are available
df %>%
filter(number_of_reporting_levels<3 & reporting_level!='national') %>%
select(entity) %>%
unique()

# Keep only national estimates except for these cases

df<- df %>%
filter(reporting_level=='national' | number_of_reporting_levels<3)

# Check again if there is more than one reporting level
df %>%
 count(entity, year, p) %>%
 rename(number_of_reporting_levels = n) %>%
    filter(number_of_reporting_levels>1)




# ### Check coverage

# Select year range
year_list<- seq(1981, 2019)

# Filter for these years and count number of years per entity 
df %>% filter(year %in% year_list) %>%
    select(entity, year) %>%
    unique() %>%
    count(entity) %>%
    filter(n<length(year_list))




# ### MLD decomposition

# Calculate population in each percentile

df<- df %>%
 mutate(pop_in_perc = share_of_pop * reporting_pop)

year_list = as.numeric(unique(df$year))

# +
#
run_mld_decomp<- function(df_input){
    
mld_decomp<- data.frame(
              year = numeric(),
              mld_total = numeric(),
              mld_within = numeric(),
              mld_between = numeric()
                                   )

# run mld decomposition, year by year
for(y in year_list){
  
  df_this_year<- df_input %>%
    filter(year == y)
  
 mld_results<- mld_decomp(df_this_year$average_in_bracket,
                   df_this_year$entity, 
                   weights = df_this_year$pop_in_perc)

 mld_decomp_this_year<- data.frame(
              year = y,
              mld_total = mld_results[["mld_decomp"]][["mld_total"]],
              mld_within = mld_results[["mld_decomp"]][["mld_within"]],
              mld_between = mld_results[["mld_decomp"]][["mld_between"]]
                                   )
  
 mld_decomp<- rbind(mld_decomp, mld_decomp_this_year)
    
}

# Within between shares

mld_decomp<- mld_decomp %>%
  mutate(within_share = mld_within/mld_total,
         between_share = mld_between/mld_total,
         )
    
return(mld_decomp)
    
}
# -

mld_decomp_baseline<- run_mld_decomp(df)
mld_decomp_baseline

# ### Alternative scenarios

# #### Set top 1% share to 20% universally

# +
# Function to replace average income above a threshold with the average that would yield a given (higher) top income share.

# Arguments:
  # Thr: percentile above which to adjust the distribution
  # A_t_1: original average above percentile
  # S_t_1: original share above percentile
  # S_adj_t_1: target adjusted share above percentile
  # A_0_1: original overall average

# For the derivation see here: https://imgur.com/a/O1Ko5jT

adjusted_averages<- function(Thr, A_t_1, S_t_1, S_adj_t_1, A_0_1){


# Ratio of adjusted to unadjusted top share
K = S_adj_t_1/S_t_1

# Calculate original average below percentile (reverse the weighted average)
A_0_t <- (A_0_1 - (1-Thr) * A_t_1) / Thr


# Calculate adjusted average above percentile
A_adj_t_1 = (Thr * A_0_t)/(A_0_1/(K * A_t_1)-(1-Thr)) 

# Calculate adjusted overall average (weighted average)
A_adj_0_1 = Thr * A_0_t + (1-Thr) * A_adj_t_1

# outputs<- list()
# outputs[["Adjusted top average"]]<- A_adj_t_1
# outputs[["Adjusted overall average"]]<- A_adj_0_1

return(A_adj_t_1)

}


check<- adjusted_averages(0.9, 30, 10, 20, 10)

check
# -

adjusted_averages(0.99, 24.50341, 0.03376764, 0.2, 7.256477)

head(df)

df_alt_20<- df %>%
  mutate(average_in_bracket = if_else(p==0.99,
                                         adjusted_averages(0.99,average_above,share_above, .20, mean),
                                         average_in_bracket))

head(df_alt_20 %>% filter(p ==0.99))

mld_decomp_alt_20<- run_mld_decomp(df_alt_20)
mld_decomp_alt_20

# ### Scale all incomes to GDP per cap

# +
# Ratio of GDP per cap to mean

df_alt_avg_to_gdp<- df %>%
  mutate(ratio_gdp_mean = (reporting_gdp/365)/mean) %>%
  mutate(average_in_bracket = average_in_bracket * ratio_gdp_mean)
# -

mld_decomp_alt_avg_to_gdp<- run_mld_decomp(df_alt_avg_to_gdp)
mld_decomp_alt_avg_to_gdp

# ### Merge in WID data for pre tax national income

df_wid<- read.csv('data/clean_wid_percentiles.csv')

head(df_wid)

summary(df_wid %>% filter(p==0.99))

df_wid<- df_wid %>%
  select(entity, year, p, average, share) %>%
 rename(wid_average = average,
       wid_share_above = share)

#Merge in to PIP data
df_pip_wid<- left_join(df, df_wid)

head(df_pip_wid)

# A model to predict WID top 1% share where missing

# +
lm_top_1_pretax<- lm(wid_share_above ~ share_above + welfare_type + as.factor(year), data = df_pip_wid %>% filter(p==0.99))

modelSummary <- summary(lm_top_1_pretax)

modelCoeffs <- modelSummary$coefficients  # model coefficients

intercept<- modelCoeffs["(Intercept)", "Estimate"] 
b_share_above<- modelCoeffs["share_above", "Estimate"] 


# +
df_predicted_shares<- df_pip_wid %>%
        filter(p==0.99) 

df_predicted_shares<- df_predicted_shares %>%
        mutate(predicted_shares = predict(lm_top_1_pretax, newdata = df_predicted_shares))

# Merge predictions into main data
df_predicted_shares<- df_predicted_shares %>%
    select(entity, year, p, predicted_shares)

df_pip_wid<- left_join(df_pip_wid, df_predicted_shares)

df_pip_wid<- df_pip_wid %>%
    mutate(wid_shares_inc_predicted = if_else(is.na(wid_share_above),
                                              predicted_shares,
                                              wid_share_above))

# +
# Predict
df_pip_wid<- df_pip_wid %>%
    mutate(lm_predicted_wid_topshare = as.numeric(NA))  %>%
    mutate(lm_predicted_wid_topshare = if_else(p==0.99,
                                               (intercept + b_share_above * share_above),
                                               as.numeric(NA)))

df_pip_wid <- df_pip_wid %>%
    mutate(wid_topshare_plus_predict = if_else(is.na(wid_share_above),
                                               lm_predicted_wid_topshare,
                                               wid_share_above))
# -

df_pip_wid %>% filter(p==0.99)

# +
# Adjust top average

df_pip_wid<- df_pip_wid %>%
  mutate(average_in_bracket = if_else(p==0.99,
                                         adjusted_averages(0.99,average_above,share_above, wid_topshare_plus_predict, mean),
                                         average_in_bracket))
# -

# MLD decomp results
mld_decomp_alt_wid_topshares<- run_mld_decomp(df_pip_wid)
mld_decomp_alt_wid_topshares

mld_decomp_baseline



# ## Plots

# +
# compare mld decomp of different scenarios
mld_decomp_baseline<- mld_decomp_baseline %>%
mutate(scenario = "Survey data")

mld_decomp_alt_wid_topshares<- mld_decomp_alt_wid_topshares %>%
mutate(scenario = "Top 1% scaled up to \n WID pretax shares")

mld_decomp_alt_avg_to_gdp<- mld_decomp_alt_avg_to_gdp %>%
mutate(scenario = "All incomes scaled to GDP")

compare_mld<- bind_rows(mld_decomp_baseline, mld_decomp_alt_wid_topshares, mld_decomp_alt_avg_to_gdp)

compare_mld$scenario <- factor(compare_mld$scenario,      # Reordering group factor levels
                         levels = c("Survey data", 
                                    "Top 1% scaled up to \n WID pretax shares",
                                   "All incomes scaled to GDP"))




# +
compare_mld_area<- compare_mld %>%
    select(year, mld_within, mld_between, scenario) %>%
    pivot_longer(cols = c('mld_within', 'mld_between'),
                 names_to = "measure",
                 values_to = "value")

plot<- ggplot(compare_mld_area, aes(x = year, y=value, fill = measure)) +
        geom_area() +
facet_wrap(~scenario) +
        ggtitle("Decomposition of global inequality (MLD) within and between countries")

plot

ggsave('graphics/total_mld_breakdown.png')


# +
# compare mld decomp of different scenarios
compare_mld_area<- compare_mld %>%
    select(year, within_share, between_share, scenario) %>%
    pivot_longer(cols = c('within_share', 'between_share'),
                 names_to = "measure",
                 values_to = "value")

plot<- ggplot(compare_mld_area, aes(x = year, y=value, fill = measure)) +
        geom_area() +
facet_wrap(~scenario) +
        ggtitle("Share of global inequality (MLD) found within and between countries")

plot

ggsave('graphics/within_between_shares_of_total.png')

# -


