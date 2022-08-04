rm(list = ls())
library(stringr)
library(googlesheets4)
library(dplyr)
library(readr)
library(tidyr)

sheet_url <- "https://docs.google.com/spreadsheets/d/19XGeINgrM0_q5wVblicx-vrj2iXrZmHEYCw1HHzpTUY/edit#gid=0"

df <- read_sheet(sheet_url)

df <- df %>%
  rename(Entity = `Name`) %>%
  gather(Year,Conference_attendance, -Entity)

df$Year <- as.numeric(df$Year)

write_csv(df, "Attendance_ai_conference.csv")
