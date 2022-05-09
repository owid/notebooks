library(rio)
library(stringr)
library(data.table)
library(lubridate)

url <- "https://yougov.co.uk/_pubapis/v5/uk/trackers/dietery-choices-of-brits-eg-vegeterian-flexitarian-meat-eater-etc/download/"

df <- rio::import(url, format = "xlsx")
setDT(df)

setnames(df, "Which of these best describes your diet?", "Entity")
df <- df[!Entity %in% c("Base", "Unweighted base")]
df[, Entity := str_replace(Entity, " \\(.*", "")]

df <- transpose(df, make.names = TRUE, keep.names = "Year")
df[, Entity := "United Kingdom"]

setcolorder(df, c("Entity", "Year"))

df[, Year := as.integer(ymd(Year) - ymd("20190101"))]
fwrite(df, "YouGov - Dietary choices of Brits.csv")
