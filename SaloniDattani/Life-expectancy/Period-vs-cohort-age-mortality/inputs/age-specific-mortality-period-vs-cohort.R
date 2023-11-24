# Open libraries
library(tidyverse)
library(scales)
library(viridis)

# !!! Download and replace this with path to folder
data_folder <- ""

# Data source:
# https://www.mortality.org/
# Choose countries, then go to Cohort data > Death Rates > 1x1
# set filename to cMx_1x10_(name of country).txt
# Choose countries, then go to Period data > Death Rates > 1x1
# set filename to Mx_1x10_(name of country).txt

countries <- c("FRA")
cohort_mortality <- list()
period_mortality <- list()

# Import cohort data
for (country in countries) {
  
  # Import and rename cols
  cohort_mortality[[country]] <- read_table(paste0(data_folder, "cMx_1x1_", country, ".txt"), skip=2, na = ".")
  colnames(cohort_mortality[[country]]) <- c("Year", "Age", "Female", "Male", "Total")
  
  cohort_mortality[[country]] <- cohort_mortality[[country]] %>%
    mutate(Country = country) %>%
    mutate(Type = "Cohort")
  
}

# Import period data
for (country in countries) {
  
  # Import and rename cols
  period_mortality[[country]] <- read_table(paste0(data_folder, "Mx_1x1_", country, ".txt"), skip=2, na = ".")
  colnames(period_mortality[[country]]) <- c("Year", "Age", "Female", "Male", "Total")
  
  period_mortality[[country]] <- period_mortality[[country]] %>%
    mutate(Country = country) %>%
    mutate(Type = "Period")
  
}

# Join into single df
cohort_mortality <- do.call(rbind.data.frame, cohort_mortality)
period_mortality <- do.call(rbind.data.frame, period_mortality)

# Gather to make it long format and get only values for total
cohort_mortality <- gather(cohort_mortality, "Sex", "Rate", Female:Total)
period_mortality <- gather(period_mortality, "Sex", "Rate", Female:Total)

mortality <- bind_rows(cohort_mortality, period_mortality)

# Reformat
mortality$Age <- as.integer(mortality$Age)
mortality$Rate <- as.numeric(mortality$Rate)
mortality$Country <- as.factor(mortality$Country)
mortality$Sex <- as.factor(mortality$Sex)
mortality$Type <- as.factor(mortality$Type)

# Select years to show, retain only Total
years <- c(1910,1918,1920,1930,1940)
mortality_y <- mortality %>%
                  filter(Year %in% years) %>%
                  filter(Sex == 'Total')

mortality_y$Year <- as.factor(mortality_y$Year)

# Get number of time periods shown for colour scale
n_colours <- nrow(count(mortality_y, Year))
colors <- colorRampPalette(brewer.pal(8, "Spectral"))(n_colours)

# Plot comparison between cohort and period mortality rates
ggplot(data=mortality_y, aes(color=Year, x=Age, y=Rate)) +
    geom_line(aes(color=Year),size=1, alpha=1) +
    geom_point(data=filter(mortality, Age==0), aes(color=Year,x=Age,y=Rate), size=1, show.legend=FALSE) +
    facet_grid(cols=vars(Type)) +
    coord_cartesian(xlim=c(0,95)) +
    theme_classic() +
    labs(title = "Annual death rate by age",
       y = "Death rate",
       x = "Age",
       color = "Year or birth cohort", 
       caption = "Period vs cohort age-specific death rates. Source: Source: Max Planck Institute for Demographic Research (Germany), University of California, Berkeley (USA), and French Institute for Demographic Studies (France).\n(data downloaded on 24 Sep 2023)") +
    scale_color_manual(values = colors) +
    scale_x_continuous(breaks = seq(0, 100, by=10)) +
    scale_y_continuous(labels = scales::percent, trans='log2', breaks = c(0.0001, 0.001, 0.01, 0.1, 1)) 

ggsave(paste0(data_folder, "period-cohort-age-specific-mortality.svg"), width = 12, height = 6)
