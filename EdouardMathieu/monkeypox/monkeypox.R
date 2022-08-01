rm(list = ls())
library(googlesheets4)
library(plyr)
library(data.table)
library(purrr)
library(dplyr)
library(tidyr)
library(lubridate)
setwd('Documents/OWID/repos/notebooks/EdouardMathieu/monkeypox/')
aggregate <- function(df, case_type, date_type, pop) {
  stopifnot(date_type %in% c("confirmation", "entry"))
  stopifnot(case_type %in% c("all", "confirmed"))
  
  if (case_type == "confirmed") df <- df[status == "confirmed"]
  
  setnames(df, sprintf("Date_%s", date_type), "date")
  df <- df[!is.na(date), c("location", "date")]
  
  world <- df[, .N, "date"]
  world[, location := "World"]
  df <- df[, .N, c("location", "date")]
  df <- rbindlist(list(df, world), use.names = T)
  
  # Fill missing dates with 0 for all countries
  date <- seq(min(df$date), max(df$date), by = "1 day")
  location <- unique(df$location)
  df_range <- data.table(crossing(date, location))
  df <- merge(df, df_range, by = c("location", "date"), all = T)
  df[, N := nafill(N, fill = 0)]
  
  # Add 7-day average
  setorder(df, date)
  df[, rolling_avg := round(frollmean(N, 7), 2), location]
  
  # Add cumulative version
  df[, cumulative := cumsum(N), location]
  
  # Add per-capita metrics
  df <- merge(df, pop, by = "location", all.x = TRUE)
  stopifnot(all(!is.na(df$population)))
  df[, N_pm := round(N * 1000000 / population, 3)]
  df[, cumulative_pm := round(cumulative * 1000000 / population, 3)]
  df[, rolling_avg_pm := round(rolling_avg * 1000000 / population, 3)]
  df[, population := NULL]
  
  setnames(
    df,
    c("N", "cumulative", "rolling_avg", "N_pm", "cumulative_pm", "rolling_avg_pm"),
    c(sprintf("%s_%s_by_%s", c("daily", "total", "7day"), case_type, date_type),
      sprintf("%s_%s_by_%s_per_million", c("daily", "total", "7day"), case_type, date_type))
  )
  
  return(df)
}

cols <- c("Country", "Status", "Date_entry", "Date_confirmation")

gs4_deauth()
df_gs <- read_sheet("https://docs.google.com/spreadsheets/d/1CEBhao3rMe-qtCbAgJTn5ZKQMRFWeAeaiXFpBY3gbHE/edit#gid=0") %>% 
  select(cols)

### Get the endemic countries data from github - for cases after 6th May 2022
df_gh <- read.csv('https://raw.githubusercontent.com/globaldothealth/monkeypox/main/latest.csv')
# Select data that isn't US has either date entry or date confirmed after may 6th 2022.
df_gh <- df_gh %>%
  mutate(Date_entry = as.Date(Date_entry), Date_confirmation = as.Date(Date_confirmation)) %>% 
  filter(Date_entry >= as.Date("2022-05-06") & Date_confirmation >= as.Date("2022-05-06")) %>% 
  filter(!Country %in% df_gs$Country) %>% 
  select(cols)

df <- rbind(df_gs, df_gh)



setDT(df)

df <- df[!is.na(Status) & !is.na(Country)]

stopifnot(all(sort(unique(df$Status)) == c("confirmed", "discarded", "omit_error", "suspected")))
df <- df[!Status %in% c("discarded", "omit_error")]

df <- df[, c("Status", "Country", "Date_entry", "Date_confirmation")]
setnames(df, c("Status", "Country"), c("status", "location"))

# Entity cleaning
country_mapping <- fread("country_mapping.csv")
df <- merge(df, country_mapping, all.x = TRUE, on = "location")
if (any(is.na(df$new))) {
  stop("Missing location mapping", cat(df[is.na(new), unique(location)], sep = "\n"))
}
df[, location := NULL]
setnames(df, "new", "location")
setcolorder(df, "location")

# Population data
pop <- fread(
  "https://github.com/owid/covid-19-data/raw/master/scripts/input/un/population_latest.csv",
  select = c("entity", "population"),
  col.names = c("location", "population"),
  showProgress = FALSE
)

pop_missing <- data.frame(location = c("Martinique", "Guadeloupe"), population = c(374743,400013))
pop <- rbind(pop, pop_missing)

dataframes <- list(
  aggregate(df, "confirmed", "confirmation", pop),
  aggregate(df, "confirmed", "entry", pop),
  aggregate(df, "all", "entry", pop)
)

df <- reduce(dataframes, full_join, by = c("location", "date"))

df[, date := date(date)]
df <- df[date < today()]
setorder(df, location, date)

fwrite(df, "owid-monkeypox-data.csv")
