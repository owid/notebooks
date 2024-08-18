# Open libraries
library(readxl)
library(tidyverse)
library(scales)
library(viridis)
library(ggrepel)
library(openxlsx)

print(sessionInfo())

# Data source: https://cy.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/childmortalitystatisticschildhoodinfantandperinatalchildhoodinfantandperinatalmortalityinenglandandwales/2013

# Filepath where you saved the files
file_path <- ""

###########
# 2021 data
infant_2021 <- read.xlsx(xlsxFile = paste0(file_path, "cim2021deathcohortworkbook.xlsx"), sheet = 5, startRow=10)

infant_2021 <- data.frame(lapply(infant_2021, as.numeric))

# Create variables for daily mortality -- divide by number of days in the period
infant_2021 <- infant_2021 %>%
  mutate("Day 1" = Early.neonatal.under.1.day.mortality.rate) %>%
  mutate("Day 7" = Early.neonatal.1.day.and.under.1.week.mortality.rate / 6) %>%
  mutate("Day 28" = Late.neonatal.1.week.and.under.4.weeks.mortality.rate / 21) %>%
  mutate("Day 91" = Postneonatal.4.weeks.and.under.3.months.mortality.rate / 63) %>%
  mutate("Day 182" = Postneonatal.3.months.and.under.6.months.mortality.rate / 91) %>%
  mutate("Day 365" = Postneonatal.6.months.and.under.1.year.mortality.rate / 182)

infant_g_2021 <- infant_2021 %>%
  dplyr::select(Year, "Day 1":"Day 365") %>%
  gather("Age", "Mortality", 2:7)


##############3
# 1921 to 2013 data
# Data source: https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/childmortalitystatisticschildhoodinfantandperinatalchildhoodinfantandperinatalmortalityinenglandandwales
infant_m <- read_excel(path = paste0(file_path, "cmstables2013correction.xls"), sheet = "Table 17", skip=19, col_names=F)

# Rename cols
colnames(infant_m) <- c("Year",
                        "Under.1.year",
                        "Under.4.weeks",
                        "Under.1.week",
                        "Under.1.day",
                        "One.day.and.under.1.week",
                        "One.week.and.under.4.weeks",
                        "Four.weeks.and.under.1.year",
                        "Four.weeks.and.under.3.months",
                        "Three.months.and.under.6.months",
                        "Six.months.and.under.1.year",
                        "Stillbirths",
                        "Stillbirths.plus.deaths.under.1.week",
                        "Stillbirths.plus.deaths.under.4.weeks",
                        "Stillbirths.plus.deaths.under.1.year")

# Reformat numeric               
infant_m <- data.frame(lapply(infant_m, as.numeric))

# Create variables for daily mortality -- divide by number of days in the period
infant_n <- infant_m %>%
            mutate("Day 1" = Under.1.day) %>%
            mutate("Day 7" = One.day.and.under.1.week / 6) %>%
            mutate("Day 28" = One.week.and.under.4.weeks / 21) %>%
            mutate("Day 91" = Four.weeks.and.under.3.months / 63) %>%
            mutate("Day 182" = Three.months.and.under.6.months / 91) %>%
            mutate("Day 365" = Six.months.and.under.1.year / 182)

# Gather into long format
infant_g <- infant_n %>%
              dplyr::select(Year, "Day 1":"Day 365") %>%
              gather("Age", "Mortality", 2:7)


# Prefer 2021 data for data past 1980, so delete them here
infant_g <- infant_g %>%
  filter(Year < 1980)


#############
# Join datasets
infant_g_2021 <- bind_rows(infant_g, infant_g_2021)


# Replace with numerics for plotting       
infant_g_2021[infant_g_2021 == "Day 1"] <- 1
infant_g_2021[infant_g_2021 == "Day 7"] <- 7
infant_g_2021[infant_g_2021 == "Day 28"] <- 28
infant_g_2021[infant_g_2021 == "Day 91"] <- 91
infant_g_2021[infant_g_2021 == "Day 182"] <- 182
infant_g_2021[infant_g_2021 == "Day 365"] <- 365

infant_g_2021$Age <- as.numeric(infant_g_2021$Age)

# Select years to show
infant_g_2021 <- infant_g_2021 %>%
            filter(Year %in% c(1921, 1931, 1941, 1951, 1961, 1971, 1981, 1991, 2001, 2011, 2021))

# Change to factor so the legend shows them separately
infant_g_2021$Year <- as.factor(infant_g_2021$Year)

# Define colors
unique_years <- infant_g_2021 %>% 
                    pull(Year) %>% 
                    unique() 
unique_years <- sort(unique_years)

sunset <- c("#fcde9c","#faa476","#f0746e","#e34f6f","#dc3977","#b9257a","#7c1d6f")

colourCount <- length(unique_years)
getPalette <- colorRampPalette(sunset)
colors <- getPalette(colourCount)

# Function to interpolate mortality rate for days not given
interp_fun_by_year <- function(Year) {
  subset_df <- infant_g_2021[infant_g_2021$Year == Year,]
  log_x <- log(subset_df$Age)
  log_y <- log(subset_df$Mortality)
  log_interp_fun <- stats::approxfun(log_x, log_y)
  return(function(x) exp(log_interp_fun(log(x))))
}

# GGPLOT
# Daily infant mortality by age
plot <- ggplot(data=infant_g_2021, aes(x=Age, y=Mortality, color=Year)) +
geom_point(aes(color=Year), size=1.4) +
      scale_y_continuous(trans='log10', breaks = c(0,
                                                   0.001,0.002,0.005,
                                                   0.01,0.02,0.05,
                                                   0.1,0.2,0.5,
                                                   1,2,5,
                                                   10,20,50,
                                                   100,200,500),
                         labels = label_comma()) +
      #scale_x_continuous(trans='log10') +
  theme_classic() +
  theme(strip.background = element_blank()) +
  scale_color_manual(name = "Year", values = colors) +
  theme(plot.title = element_text(face = "bold")) +
  labs(title = "Infant mortality rates decline sharply after birth", 
       subtitle = "The chances of dying are highest during the first few days of an infant's life.\nOver the following days, weeks and months, their chances of dying decrease sharply. \nOver time, the mortality rate has declined across the entire first year of an infant's life.", 
       y = "Daily mortality rate (per 1,000 live births)", 
       x = "Age (days)",
       caption = "Source: Office for National Statistics, UK") 
# Add interpolated lines connecting points
  for(i in seq_along(unique_years)) {
    year <- unique_years[i]
    plot <- plot + stat_function(fun = interp_fun_by_year(year), 
                                 color = colors[i],
                                 size=1.1)
  }

plot

ggsave(paste0(file_path,"infant_mortality-over-time.svg"), plot,
       width = 15, height = 12)
