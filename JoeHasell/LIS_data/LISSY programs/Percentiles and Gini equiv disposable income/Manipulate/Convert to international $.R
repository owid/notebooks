library(tidyverse)


fp<- "Manipulate/Output – percentiles and Gini equiv disp hh income (current LCUs).csv"

output_LCUs<- read.csv(fp) %>%
  mutate(country_iso2 = substr(survey_code, start = 1, stop = 2),
         year_code = substr(survey_code, start = 3, stop = 4))


# convert 2-digit year_code to year (year < 50 -> 20xx; else 19xx)
output_LCUs<- output_LCUs %>%
  mutate(year = if_else(as.numeric(year_code)<50, 
                        paste0("20", year_code),
                        paste0("19", year_code)))


# Use OWID country names

country_names<- read.csv("Manipulate/country_names_country_standardized.csv")

output_LCUs<- left_join(output_LCUs, country_names) %>%
  rename(country = OWID_country_name)

# Convert to int-$ (at 2011 and 2017 prices)

output_int_dollars_2011<- output_LCUs %>%
  mutate_at(vars(matches("percentile_")), list(~. / lisppp_2011)) %>%
  select(country, year,gini_coef, starts_with("percentile_"))


output_int_dollars_2017<- output_LCUs %>%
  mutate_at(vars(matches("percentile_")), list(~. / lisppp_2017)) %>%
  select(country, year,gini_coef, starts_with("percentile_"))


# Export as csv

write.csv(output_int_dollars_2011, 
          "Output/Gini and percentile thresholds, equivalised disposable household income 2011 int-$ (LIS 2021).csv", 
          row.names = FALSE,
          na = "")

write.csv(output_int_dollars_2017, 
          "Output/Gini and percentile thresholds, equivalised disposable household income 2017 int-$ (LIS 2021).csv", 
          row.names = FALSE,
          na = "")


