rm(list = ls())
library(stringr)
library(googlesheets4)
library(dplyr)
library(readr)
library(tidyr)
library(janitor)

sheet_url <- "https://docs.google.com/spreadsheets/d/19XGeINgrM0_q5wVblicx-vrj2iXrZmHEYCw1HHzpTUY/edit#gid=0"

df <- read_sheet(sheet_url)

df <- df %>%
  adorn_totals("row") %>%
  rename(Entity = Name) %>%
  gather(Year, conference_attendance, -Entity) %>%
  mutate(Year = as.numeric(Year))

write_csv(df, "transformed/Attendance_ai_conference.csv", na = "")
