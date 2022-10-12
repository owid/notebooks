rm(list = ls())
library(rvest)
library(stringr)
library(data.table)

page <- read_html("https://en.wikipedia.org/wiki/List_of_United_Nations_peacekeeping_missions")

tables <- page %>%
  html_nodes(".wikitable") %>%
  html_table()

for (i in 1:length(tables)) {
  if (any(nchar(tables[[i]]$`Dates of operation`) == 9)) {
    tables[[i]]$completed <- TRUE
  } else {
    tables[[i]]$completed <- FALSE
  }
}

df <- rbindlist(tables, fill = TRUE)

df[, code := str_extract(`Name of operation`, "\\([^)]+\\)$")]
df <- df[, c("Dates of operation", "code", "completed")] %>% unique

df[, start := as.integer(str_extract(`Dates of operation`, "^\\d{4}"))]
df[, end := as.integer(str_extract(`Dates of operation`, "\\d{4}$"))]
df[completed == FALSE, end := NA]

calculate_operations <- function(df, year) {
  subset <- df[start <= year & (end >= year | is.na(end))]
  return(data.table(Year = year, `Number of peacekeeping missions (United Nations Peacekeeping)` = nrow(subset)))
}

years <- min(df$start):year(today())
ops <- rbindlist(lapply(years, df = df, FUN = calculate_operations))

old <- fread("https://github.com/owid/owid-datasets/raw/master/datasets/United%20Nations%20Peacekeeping/United%20Nations%20Peacekeeping.csv")
old[, `Number of peacekeeping missions (United Nations Peacekeeping)` := NULL]

new <- merge(ops, old, on = "Year", all = T)
setcolorder(new, c("Entity", "Year"))
new[, Entity := "World"]
fwrite(new, "United Nations Peacekeeping.csv")
