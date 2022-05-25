rm(list = ls())
library(plyr)
library(data.table)
library(purrr)
library(dplyr)
library(lubridate)

aggregate <- function(df, case_type, date_type) {
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
  date <- seq(min(df$date), max(df$date), by = 1)
  location <- unique(df$location)
  df_range <- data.table(crossing(date, location))
  df <- merge(df, df_range, by = c("location", "date"), all = T)
  df[, N := nafill(N, fill = 0)]

  # Add 7-day average
  setorder(df, date)
  df[, rolling_avg := round(frollmean(N, 7), 2), location]
    
  # Add cumulative version
  df[, cumulative := cumsum(N), location]
  
  setnames(
    df,
    c("N", "cumulative", "rolling_avg"),
    c(
      sprintf("daily_%s_by_%s", case_type, date_type),
      sprintf("total_%s_by_%s", case_type, date_type),
      sprintf("7day_%s_by_%s", case_type, date_type)
    )
  )
  
  return(df)
}

df <- fread("https://github.com/globaldothealth/monkeypox/raw/main/latest.csv")
stopifnot(length(unique(df$Status)) == 3)

df <- df[!is.na(Status) & !is.na(Country) & Status != "excluded"]
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

dataframes <- list(
  aggregate(df, "confirmed", "confirmation"),
  aggregate(df, "confirmed", "entry"),
  aggregate(df, "all", "entry")
)

df <- reduce(dataframes, full_join, by = c("location", "date"))

df[, date := date(date)]
df <- df[date < today()]
setorder(df, location, date)
fwrite(df, "owid-monkeypox-data.csv")

# Twitter update
max <- df[location != "World" & !is.na(total_confirmed_by_confirmation), max(total_confirmed_by_confirmation, na.rm = T), location]
setorder(max, -V1)
update <- sprintf(
  "Monkeypox update:\n%s total confirmed cases\n+%s per day in the last week\n\nCountries with the most confirmed cases:\n%s\n\nData by @globaldothealth",
  max(df$total_confirmed_by_confirmation, na.rm = T),
  round(tail(df$`7day_confirmed_by_confirmation`, 1)),
  paste0(sprintf("%s: %s", head(max$location, 5), head(max$V1, 5)), collapse = "\n")
)
clipr::write_clip(update)
browseURL("https://ourworldindata.org/explorers/monkeypox?facet=none&hideControls=false&Metric=Confirmed+cases&Frequency=7-day+average&Shown+by=Date+of+confirmation&country=~OWID_WRL")
browseURL("https://twitter.com/compose/tweet")
