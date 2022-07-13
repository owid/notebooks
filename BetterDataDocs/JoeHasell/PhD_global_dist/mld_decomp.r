library(gpinter)
library(tidyverse)


url = "https://joeh.fra1.digitaloceanspaces.com/phd_global_dist/percentiles_from_PIP.csv"


df<- read.csv(url)

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

# MLD decomposition

# +
#
mld_decomp<- data.frame(
              year = numeric(),
              mld_total = numeric(),
              mld_within = numeric(),
              mld_between = numeric()
                                   )

# run mld decomposition, year by year
for(y in year_list){
  
  df_this_year<- df %>%
    filter(year == y)
  
 mld_results<- mld_decomp(df_this_year$average_in_bracket,
                   df_this_year$country, 
                   weights = brackets_avgs_this_year$share_of_pop)

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
