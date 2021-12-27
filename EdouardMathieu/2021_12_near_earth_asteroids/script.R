library(stringr)
library(data.table)
library(lubridate)
rm(list = ls())

df <- fread("Discovery StatisticsPrintDownload.csv", select = c("Date", "NEA-km", "NEA-140m", "NEA"))
df[, Year := str_sub(Date, 1, 4)]
df[, larger_than_1km := `NEA-km`]
df[, between_140m_and_1km := `NEA-140m` - larger_than_1km]
df[, smaller_than_140m := NEA - larger_than_1km - between_140m_and_1km]
setorder(df, -Date)
df[, Entity := "World"]
df <- df[, .SD[1], Year][, c("Entity", "Year", "larger_than_1km", "between_140m_and_1km", "smaller_than_140m")]

fwrite(df, "Near-Earth asteroids discovered over time.csv")
