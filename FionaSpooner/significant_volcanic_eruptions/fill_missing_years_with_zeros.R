library(dplyr)
library(janitor)

df <- clean_names(read.csv('data/owid_download_significant_volcanic_eruptions.csv'))

min_year <- min(df$year)
max_year <- max(df$year)

years <- seq(min_year, max_year, 1)
entities <- unique(df$entity)

all_entities_years <- expand.grid(entity = entities, year = years)

filled_df <- all_entities_years %>% 
  left_join(., df, by = c("entity", "year"))


filled_df$number_of_significant_volcanic_eruptions_ngdc_wds[is.na(filled_df$number_of_significant_volcanic_eruptions_ngdc_wds)] <- 0

write.csv(filled_df, "data/update_owid_download_significant_volcanic_eruptions.csv", row.names = FALSE)
