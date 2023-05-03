library(stringr)
library(data.table)
library(rvest)
library(lubridate)
rm(list = ls())

page <- read_html("https://en.wikipedia.org/wiki/List_of_quantum_processors")
tables <- page %>% html_table()
df <- tables[[2]]
setDT(df)

df[, year := as.integer(str_extract(`Release date`, "20\\d{2}"))]

df[, qubits := str_extract(`Qubits (Logical)`, "^\\d+ qb")]
df[, qubits := as.integer(str_extract(qubits, "\\d+"))]

df <- df[!is.na(year) & year < year(today()), .(qubits = max(qubits)), year]
setorder(df, year)
df[, qubits := cummax(qubits)]

df[, entity := "World"]
setcolorder(df, "entity")

fwrite(df, "Quantum processors over time.csv")