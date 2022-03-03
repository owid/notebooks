library(data.table)
library(rvest)
rm(list = ls())

page <- read_html("https://www.pewresearch.org/politics/2021/05/17/public-trust-in-government-1958-2021/")
df <- page %>% html_node("table") %>% html_table()
setDT(df)

df <- df[, c("Date", "Moving average")]
df[, year := year(mdy(Date))]
df <- df[, .(public_trust_government = round(mean(`Moving average`))), year]
df[, entity := "United States"]
setcolorder(df, c("entity", "year", "public_trust_government"))

fwrite(df, "US - Public Trust in Government - Pew Research Center.csv")
