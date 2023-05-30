library(rio)
library(stringr)
library(data.table)
library(lubridate)
library(plyr)

URL <- "https://yougov.co.uk/_pubapis/v5/uk/trackers/dietery-choices-of-brits-eg-vegeterian-flexitarian-meat-eater-etc/download/"

get_sheet_data <- function(age_group) {
  message(age_group)
  df <- rio::import(URL, format = "xlsx", sheet = age_group)
  setDT(df)
  setnames(df, "Which of these best describes your diet?", "Entity")
  df <- df[!Entity %in% c("Base", "Unweighted base")]
  df[, Entity := str_replace(Entity, " \\(.*", "")]
  df <- transpose(df, make.names = TRUE, keep.names = "Year")
  df[, Entity := mapvalues(
    age_group,
    c("All adults", "18-24", "25-49", "50-64", "65+"),
    c("All adults", "18-24y", "25-49y", "50-64y", "65y+"),
    warn_missing = FALSE
  )]
  
  df[, total := `Plant-based / Vegan` + Vegetarian + Flexitarian + Pescetarian + `Meat eater` + `None of these`]
  df[, `Plant-based / Vegan` := round(`Plant-based / Vegan` / total, 2)]
  df[, Vegetarian := round(Vegetarian / total, 2)]
  df[, Flexitarian := round(Flexitarian / total, 2)]
  df[, Pescetarian := round(Pescetarian / total, 2)]
  df[, `Meat eater` := round(`Meat eater` / total, 2)]
  df[, `None of these` := round(`None of these` / total, 2)]
  df[, total := NULL]
  
  return(df)
}

age_groups <- c("All adults", "18-24", "25-49", "50-64", "65+")

df <- rbindlist(lapply(age_groups, get_sheet_data))

setcolorder(df, c("Entity", "Year"))
df[, Year := as.integer(ymd(Year) - ymd("20190101"))]
fwrite(df, "YouGov - Dietary choices of Brits.csv")
