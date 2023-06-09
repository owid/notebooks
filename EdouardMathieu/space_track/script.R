rm(list = ls())
library(data.table)
library(lubridate)

# Go to https://www.space-track.org and log in
# Go to Query Builder
# Use the following parameters: Class = gp, Order by = OBJECT_ID, Format = CSV
# Click on BUILD QUERY then RUN QUERY to download the CSV
# Move the CSV file to the script's folder
data <- fread("https __www.space-track.org_basicspacedata_query_class_gp_orderby_object_id asc_format_csv_emptyresult_show.csv")


# Orbit definitions

data[PERIAPSIS <= 2000, ORBIT := "Low Earth orbit"]
data[PERIAPSIS >= 2000 & PERIAPSIS <= 35586, ORBIT := "Medium Earth orbit"]
data[PERIAPSIS >= 35586 & PERIAPSIS <= 35986, ORBIT := "Geostationary orbit"]
data[PERIAPSIS >= 35986, ORBIT := "High Earth orbit"]


# Objects in Lower Earth orbit over time, broken down by object type

df <- data[OBJECT_TYPE %in% c("PAYLOAD", "ROCKET BODY", "DEBRIS")]
df <- df[ORBIT == "Low Earth orbit"]

years <- year(min(df$LAUNCH_DATE, na.rm = T)):year(max(df$LAUNCH_DATE, na.rm = T))
years <- years[years < year(today())]

count_objects <- function(year) {
  subset <- df[year(LAUNCH_DATE) <= year & (is.na(DECAY_DATE) | year(DECAY_DATE) > year)]
  subset <- subset[, .N, OBJECT_TYPE]
  subset[, YEAR := year]
  return(subset)
}

df <- rbindlist(lapply(years, FUN = count_objects))

leo_objects <- copy(df)
setnames(leo_objects, "OBJECT_TYPE", "ENTITY")


# Non-debris objects in space over time, broken down by orbit

df <- data[OBJECT_TYPE %in% c("PAYLOAD", "ROCKET BODY")]

years <- year(min(df$LAUNCH_DATE, na.rm = T)):year(max(df$LAUNCH_DATE, na.rm = T))
years <- years[years < year(today())]

count_objects <- function(year) {
  subset <- df[year(LAUNCH_DATE) <= year & (is.na(DECAY_DATE) | year(DECAY_DATE) > year)]
  subset <- subset[, .N, ORBIT]
  subset[, YEAR := year]
  return(subset)
}

df <- rbindlist(lapply(years, FUN = count_objects))
setnames(df, "ORBIT", "ENTITY")


# Merge into a single dataset

df <- rbindlist(list(leo_objects, df))
df[, ENTITY := plyr::mapvalues(
  ENTITY,
  c("ROCKET BODY", "PAYLOAD", "DEBRIS"),
  c("Rocket bodies", "Payloads", "Debris")
)]
setnames(df, "N", "Number of objects")
setcolorder(df, c("ENTITY", "YEAR"))
setorder(df, ENTITY, YEAR)
fwrite(df, "Space-Track - Number of objects in space.csv")
