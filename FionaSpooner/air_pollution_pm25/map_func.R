library(terra)
library(tmap)
library(raster)
library(RColorBrewer)

data(World)
world <- World

pal <- c("#8CB78A","#DDD10B","#DA970A", "#DE4F0B","#C20A08",
          "#940B27",brewer.pal(11, "RdBu")[1],"#000000")

make_pm_25 <- function(year, save_file = FALSE){
  
  file <- gsub("2020", year, "data/V5GL02.HybridPM25.Global.202001-202012.nc")
  r <- raster::raster(file) 
  names(r)<- 'pm25'
  p <- tm_shape(r) +
    tm_raster('pm25',
              title = expression('PM'[2.5]), 
              breaks=c(0, 5, 10, 15, 25, 35, 50, 100, 300),
              palette = pal3)+
    tm_shape(world, is.master = TRUE, bbox = c(-180,180, -56, 75))+#, c(-18000000, -7150000, 20000000,8400000)) +
    tm_borders(lwd = 0.4,alpha = 0.5) +
    tm_layout(main.title= paste0('Annual Mean Concentration of Fine Particulate Matter - ', year), 
              main.title.position = c('center'))
  if (save_file){
    tmap_save(p, paste0("output/",year,"_global_pm25.png"))
  }
  
  return(p)
}




