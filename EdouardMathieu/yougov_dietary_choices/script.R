library(rio)
library(stringr)
library(data.table)
library(lubridate)

URL <- "https://yougov.co.uk/_pubapis/v5/uk/trackers/dietery-choices-of-brits-eg-vegeterian-flexitarian-meat-eater-etc/download/"

get_sheet_data <- function(age_group) {
  message(age_group)
  df <- rio::import(URL, format = "xlsx", sheet = age_group)
  setDT(df)
  setnames(df, "Which of these best describes your diet?", "Entity")
  df <- df[!Entity %in% c("Base", "Unweighted base")]
  df[, Entity := str_replace(Entity, " \\(.*", "")]
  df <- transpose(df, make.names = TRUE, keep.names = "Year")
  df[, Entity := age_group]
  return(df)
}

age_groups <- c("All adults", "18-24", "25-49", "50-64", "65+")

df <- rbindlist(lapply(age_groups, get_sheet_data))

setcolorder(df, c("Entity", "Year"))
df[, Year := as.integer(ymd(Year) - ymd("20190101"))]
fwrite(df, "YouGov - Dietary choices of Brits.csv")
