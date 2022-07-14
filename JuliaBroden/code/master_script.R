rm(list = ls())
library(stringr)
library(dplyr)
library(readr)

top1 <- read.csv(file = '/Users/Julia/Documents/OWID/R/transformed/Imagenet_top1_V2.csv')
top5 <- read.csv(file = '/Users/Julia/Documents/OWID/R/transformed/Imagenet_top5_V2.csv')
patent <- read.csv(file = '/Users/Julia/Documents/OWID/R/transformed/Patent_Filings.csv')

master <- merge(top1, top5, by = c('Entity', 'Year', 'Type', 'Source'), all = T)

master <- merge(master, patent, by = c('Entity', 'Year'), all = T)


write_csv(master, 'master.csv')
