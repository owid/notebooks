library(terra)
library(tmap)
library(raster)

data(World)
world <- World

pmf <- list.files('data', pattern = 'nc', full.names = TRUE)

pms<- terra::rast(pmf)
ext(pms)<- c(-180, 180, -55, 68)
terra::crs(pms) <- "+proj=longlat +datum=WGS84 +no_defs"
names(pms)<- 1998:2020

test <- pms

# Running a linear model through each cell and extracting the slope
X <- cbind(1, 1:nlyr(test))
## pre-computing constant part of least squares
invXtX <- solve(t(X) %*% X) %*% t(X)
## [2] is to just get the slope
quickfun <- function(y) (invXtX %*% y)[2]
#slope <- terra::app(test, quickfun) 

roc <- terra::app(test, fun=quickfun, cores = 8)
names(roc) <- "roc"
pal = c("#1A9850","#66BD63","#A6D96A", "#D9EF8B", "#FEE08B" ,"#FDAE61" ,"#F46D43" ,"#D73027")

#writeRaster(roc, "output/rate_of_change_1998_2020.tif")
#roc <- raster::raster("output/rate_of_change_1998_2020.tif")

names(roc) <- "roc"

tm <- tm_shape(test2) +
  tm_raster('roc',
           # title = expression(atop('Average annual','change in PM'[2.5])), 
           title = expression('Average annual change in PM'[2.5]),
             breaks=c(-5, -2.5, -1,-0.5, 0,0.5, 1, 2.5, 5),
            palette = pal)+
  tm_shape(world, is.master = TRUE, bbox = c(-180,180, -56, 75))+#, c(-18000000, -7150000, 20000000,8400000)) +
  tm_borders(lwd = 0.4,alpha = 0.5) +
  tm_layout(main.title= paste0('Rate of change in concentration of fine particulate matter (1998-2020)'), 
            main.title.position = c('center'), legend.title.size = 0.9, legend.text.size = 0.7)

tmap_save(tm, paste0("output/rate_of_change.png"), dpi = 600)


############### Difference between 2019 and 1998
r98 <- raster::raster('data/V5GL02.HybridPM25.Global.199801-199812.nc') #%>% project(., "+proj=wintri")
r19 <- raster::raster('data/V5GL02.HybridPM25.Global.201901-201912.nc')

change <- r19 - r98 

names(change) <- 'pm25'

pal = c("#1A9850","#66BD63","#A6D96A", "#D9EF8B", "#FEE08B" ,"#FDAE61" ,"#F46D43" ,"#D73027")

pm <- tm_shape(change) +
  tm_raster('pm25',
            title = expression('Change in PM'[2.5]), 
            breaks=c(-125,-50, -25, 0,5, 10,20, 40, 80),
            palette = pal)+
  tm_shape(world, is.master = TRUE, bbox = c(-180,180, -56, 75))+#, c(-18000000, -7150000, 20000000,8400000)) +
  tm_borders(lwd = 0.4,alpha = 0.5) +
  tm_layout(main.title= paste0('Change in Annual Mean Concentration of Fine Particulate Matter\n 2019 vs 1998'), 
            main.title.position = c('center'))

tmap_save(pm, "Comparison_1998_2019.png")


################ Difference between 3 yr averages around 1999 and 2019

pmf <- list.files('data', pattern = 'nc', full.names = TRUE)
early <- terra::rast(pmf[1:3])
ext(early)<- c(-180, 180, -55, 68)
terra::crs(early) <- "+proj=longlat +datum=WGS84 +no_defs"
names(early)<- 1998:2000

early_mean <- terra::app(early, fun=mean, cores = 8)

late <- terra::rast(pmf[21:23])
ext(late)<- c(-180, 180, -55, 68)
terra::crs(late) <- "+proj=longlat +datum=WGS84 +no_defs"
names(late)<- 2018:2020

late_mean <- terra::app(late, fun=mean, cores = 8)

difference <- late_mean - early_mean

pm <- tm_shape(difference) +
  tm_raster('mean',
            title = expression('Change in PM'[2.5]), 
            breaks=c(-80,-40, -20,-10,-5,0,5, 10,20, 40, 80, 100),
            palette = pal)+
  tm_shape(world, is.master = TRUE, bbox = c(-180,180, -56, 75))+#, c(-18000000, -7150000, 20000000,8400000)) +
  tm_borders(lwd = 0.4,alpha = 0.5) +
  tm_layout(main.title= paste0('Change in Annual Mean Concentration of Fine Particulate Matter\n 2019 vs 1999'), 
            main.title.position = c('center'))

pm



