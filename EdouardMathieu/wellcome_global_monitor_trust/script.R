library(zoo)
library(tidyr)
library(rio)
library(data.table)
rm(list = ls())

FILE_URL = "https://cms.wellcome.org/sites/default/files/2021-11/wgm-public-file-covid-crosstabs.xlsx"
REPORT_YEAR = 2020

df <- import(FILE_URL, sheet = "Country Tabs", skip = 1)
setDT(df)
setnames(df, "...1", "metric")

df[, metric := zoo::na.locf(metric, na.rm = F)]
df <- df[str_detect(metric, "Trust")]
df[, metric := str_to_sentence(str_replace(metric, "^[A-Z0-9]+ ", ""))]

df <- df[...2 %in% c("A lot", "Some")]
df[, ...2 := NULL]

df <- pivot_longer(df, 2:ncol(df), names_to = "entity")
setDT(df)
df <- df[!str_detect(entity, "\\.{3}\\d+")]

df <- df[, .(value = 100 * round(sum(as.double(value)), 3)), c("metric", "entity")]
df <- df[value > 0] # Countries with 0% trust are in fact ones with no respondent
df <- df[entity != "Global Total"]

df[, year := REPORT_YEAR]
df <- pivot_wider(df, id_cols = c("entity", "year"), names_from = "metric", values_from = "value")
setDT(df)

country_mapping <- fread("wellcome_country_standardized.csv")
df <- merge(country_mapping, df, by = "entity")
df[, entity := NULL]
setnames(df, "owid_entity", "entity")
fwrite(df, "Wellcome Global Monitor 2020: Covid-19 - Trust questions.csv")
