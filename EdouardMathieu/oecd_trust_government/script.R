library(lubridate)
library(data.table)
rm(list = ls())

df <- fread(
  sprintf("https://stats.oecd.org/sdmx-json/data/DP_LIVE/AUS+AUT+BEL+CAN+CHE+CHL+COL+CRI+CZE+DEU+DNK+ESP+EST+FIN+FRA+GBR+GRC+HUN+IRL+ISL+ISR+ITA+JPN+KOR+LTU+LUX+LVA+MEX+NLD+NOR+NZL+POL+PRT+SVK+SVN+SWE+TUR+USA.TRUSTGOV.TOT.PC.A/OECD?contentType=csv&detail=code&separator=comma&csv-lang=en&startPeriod=2010&endPeriod=%s", year(today())),
  select = c("TIME", "LOCATION", "Value")
)
setnames(df, "TIME", "Year")

pop <- fread("https://github.com/owid/owid-datasets/raw/master/datasets/Population%20(Gapminder%2C%20HYDE%20%26%20UN)/Population%20(Gapminder%2C%20HYDE%20%26%20UN).csv", select = c("Entity", "Year", "Population (historical estimates)"))
setnames(pop, "Population (historical estimates)", "population")

mapping <- fread("oecd_country_standardized.csv")

df <- merge(mapping, df, by = "LOCATION")
df <- merge(df, pop, by = c("Entity", "Year"))
df[, weighted_value := Value * population]

df <- df[, .(trust_government = sum(weighted_value) / sum(population)), Year]
df[, entity := "OECD"]

setcolorder(df, c("entity", "Year"))
fwrite(df, "OECD - Trust in government.csv")
