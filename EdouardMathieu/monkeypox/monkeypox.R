rm(list = ls())
library(googlesheets4)
library(plyr)
library(readr)
library(purrr)
library(dplyr)
library(tidyr)
library(lubridate)
library(data.table)

aggregate <- function(df, date_type, pop) {
  stopifnot(date_type %in% c("confirmation"))
  
  col_name <- sprintf("Date_%s", date_type)
  df <- df %>%
    rename(date := {{col_name}}) %>%
    filter(!is.na(date)) %>%
    select(location, date)

  world <- df %>%
    group_by(date) %>%
    count() %>%
    mutate(location = "World")
  df <- df %>%
    group_by(location, date) %>%
    count()
  df <- rbind(df, world)
  
  # Fill missing dates with 0 for all countries
  date <- seq(min(df$date), max(df$date), by = "1 day")
  location <- unique(df$location)
  df_range <- data.frame(crossing(date, location))
  df <- full_join(df, df_range, by = c("location", "date")) %>%
    mutate(n = replace_na(n, 0))
  
  # Add 7-day average
  df <- df %>%
    arrange(date) %>%
    group_by(location) %>%
    mutate(rolling_avg = round(frollmean(n, 7), 2))
  
  # Add cumulative version
  df <- df %>%
    group_by(location) %>%
    mutate(cumulative = cumsum(n))

  # Add per-capita metrics
  df <- left_join(df, pop, by = "location")
  stopifnot(all(!is.na(df$population)))
  df <- df %>%
    mutate(
      n_pm = round(n * 1000000 / population, 3),
      cumulative_pm = round(cumulative * 1000000 / population, 3),
      rolling_avg_pm = round(rolling_avg * 1000000 / population, 3)
    ) %>%
    select(-population)

  # Rename columns
  metric <- mapvalues(date_type, c("confirmation"), c("cases"))
  col_names <- sprintf(c("new_%s", "total_%s", "new_%s_smoothed"), metric)
  col_names_pm <- col_names %>% paste0("_per_million")
  setnames(
    df,
    c("n", "cumulative", "rolling_avg", "n_pm", "cumulative_pm", "rolling_avg_pm"),
    c(col_names, col_names_pm)
  )
  
  return(df)
}

cols <- c("Country", "Status", "Date_confirmation")

# Import main data from Google Sheets
gs4_deauth()
df_gs <- read_sheet("https://docs.google.com/spreadsheets/d/1CEBhao3rMe-qtCbAgJTn5ZKQMRFWeAeaiXFpBY3gbHE/edit#gid=0") %>% 
  select(cols)

### Get the endemic countries data from github - for cases after 6th May 2022
df_gh <- read_csv("https://raw.githubusercontent.com/globaldothealth/monkeypox/main/latest.csv")
# Select data that isn't US has either date entry or date confirmed after may 6th 2022.
df_gh <- df_gh %>%
  filter(Date_confirmation >= "2022-05-06") %>% 
  filter(!Country %in% df_gs$Country) %>% 
  select(cols)

# Bind spreadsheet and GitHub files
df <- rbind(df_gs, df_gh) %>%
  filter(!is.na(Status), !is.na(Country))

# Keep confirmed cases only
stopifnot(all(sort(unique(df$Status)) == c("confirmed", "discarded", "omit_error", "suspected")))
df <- df %>%
  filter(Status == "confirmed") %>%
  select(Status, Country, Date_confirmation) %>%
  rename(status = Status, location = Country)

# Entity cleaning
country_mapping <- read_csv("country_mapping.csv")
df <- left_join(df, country_mapping, by = "location")
if (any(is.na(df$new))) {
  stop("Missing location mapping", cat(df[is.na(new), unique(location)], sep = "\n"))
}
df <- df %>%
  select(-location) %>%
  rename(location = new) %>%
  relocate(location)

# Population data
pop <- read_csv(
  "https://github.com/owid/covid-19-data/raw/master/scripts/input/un/population_latest.csv",
  col_select = c("entity", "population")
) %>%
  rename(location = entity)

dataframes <- list(
  aggregate(df, "confirmation", pop)
)

df <- reduce(dataframes, full_join, by = c("location", "date")) %>%
  mutate(date = date(date)) %>%
  filter(date < today()) %>%
  relocate(location, date) %>%
  arrange(location, date)

write_csv(df, "owid-monkeypox-data.csv", na = "")
