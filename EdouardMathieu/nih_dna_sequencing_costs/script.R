rm(list = ls())
library(data.table)
library(rio)

URL <- "https://www.genome.gov/sites/default/files/media/files/2021-11/Sequencing_Cost_Data_Table_Aug2021.xls"

df <- data.table(import(URL))

setnames(df, c("year", "cost_per_mb", "cost_per_genome"))

df[, year := year(year)]

setorder(df, cost_per_genome)
df <- df[, .SD[1], year]

setorder(df, year)

df[, base_pairs_per_dollar := (1 / cost_per_mb) * 1000000]

df[, entity := "World"]
setcolorder(df, c("entity", "year"))

fwrite(df, "NIH - DNA Sequencing Costs.csv")
