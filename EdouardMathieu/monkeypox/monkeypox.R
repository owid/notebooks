rm(list = ls())
library(googlesheets4)
library(plyr)
library(data.table)
library(purrr)
library(dplyr)
library(tidyr)
library(lubridate)
setwd("~/git/notebooks/EdouardMathieu/monkeypox")

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
  
  setnames(
    df,
    c("N", "cumulative", "rolling_avg"),
    sprintf("%s_%s_by_%s", c("daily", "total", "7day"), case_type, date_type)
  )
  
  return(df)
}

df <- read_sheet("https://docs.google.com/spreadsheets/d/1CEBhao3rMe-qtCbAgJTn5ZKQMRFWeAeaiXFpBY3gbHE/edit#gid=0")
setDT(df)
df <- df[!is.na(Status) & !is.na(Country)]
stopifnot(all(sort(unique(df$Status)) == c("confirmed", "discarded", "suspected")))

df <- df[Status != "discarded"]
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
# source("tweet.R")
