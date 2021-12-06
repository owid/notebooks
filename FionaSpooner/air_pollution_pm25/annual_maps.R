library(terra)
library(tmap)
library(raster)
library(RColorBrewer)

source('map_func.R')

#Download data from https://wustl.app.box.com/v/ACAG-V5GL02-GWRPM25/folder/148054977849

years <- 1998:2020

for (year in years){
  make_pm_25(year, save_file = TRUE)
}



