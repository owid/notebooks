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
  return(df)
}

age_groups <- c("All adults", "18-24", "25-49", "50-64", "65+")

df <- rbindlist(lapply(age_groups, get_sheet_data))

setcolorder(df, c("Entity", "Year"))
df[, Year := as.integer(ymd(Year) - ymd("20190101"))]
fwrite(df, "YouGov - Dietary choices of Brits.csv")

pivoted <- df %>% gather(diet, share, 3:8) %>% spread(Entity, share) %>% data.table
setnames(pivoted, "diet", "Entity")
setcolorder(pivoted, c("Entity", "Year"))
pivoted[, `All adults` := NULL]
setnames(
  pivoted,
  c("18-24y", "25-49y", "50-64y", "65y+"),
  c("18-24 years old", "25-49 years old", "50-64 years old", "Over 65s")
)
fwrite(pivoted, "YouGov - Dietary choices of Brits - Pivoted version.csv")
