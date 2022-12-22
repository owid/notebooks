library(tidyr)
library(stringr)
library(data.table)
rm(list = ls())

# Download data from https://www.airlines.org/dataset/world-airlines-traffic-and-capacity/
df <- fread("Traffic and Operations 1929-Present_data.csv")
setnames(df, c("Year", "Var", "Value"))

df[, Value := as.double(str_replace(Value, ",", "."))]

# Conversion factor: "(mils)"
df[str_detect(Var, "\\(mils\\)"), Value := Value * 1000000]
df[str_detect(Var, "\\(mils\\)"), Var := str_replace(Var, " \\(mils\\)", "")]

# Conversion factor: "(000)"
df[str_detect(Var, "\\(000\\)"), Value := Value * 1000]
df[str_detect(Var, "\\(000\\)"), Var := str_replace(Var, " \\(000\\)", "")]

# Reshape
df <- spread(df, Var, Value) %>% data.table

df[, Entity := "World"]
setcolorder(df, c("Entity", "Year"))

fwrite(df, "Global airline traffic and capacity (ICAO).csv")
