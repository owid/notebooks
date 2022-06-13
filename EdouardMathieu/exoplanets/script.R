library(lubridate)
library(data.table)
rm(list = ls())

df <- fread("https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+distinct+pl_name,disc_year,discoverymethod+from+ps&format=csv")

df <- df[disc_year < year(today())]

top_methods <- table(df$discoverymethod) %>% sort %>% tail(3) %>% names
df[!discoverymethod %in% top_methods, discoverymethod := "Other methods"]
df[, discoverymethod := str_to_sentence(discoverymethod)]

df <- df[, .N, c("disc_year", "discoverymethod")]
df <- df %>% spread(disc_year, N)
df <- df %>% gather(disc_year, N, 2:ncol(df))
setDT(df)

setorder(df, disc_year)
df[, cumulative_exoplanets := cumsum(nafill(N, fill = 0)), discoverymethod]
df[, N := NULL]

setnames(df, c("discoverymethod", "disc_year"), c("entity", "year"))

fwrite(df, "output/NASA - Exoplanets.csv")
