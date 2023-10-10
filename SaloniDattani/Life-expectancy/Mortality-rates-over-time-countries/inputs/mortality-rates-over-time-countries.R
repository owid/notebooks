# Open libraries
library(tidyverse)
library(scales)
library(viridis)

# Data source:
# https://www.mortality.org/
# Choose countries, then go to Cohort data > Death Rates > 1x10
# Download and replace this with path to folder
data_folder <- ""
# set filename to cMx_1x10_(name of country).txt

countries <- c("USA", "Italy", "UK", "Sweden")
mortality <- list()

# Import data
for (country in countries) {
  
  # Import and rename cols
  mortality[[country]] <- read_table(paste0(data_folder, "cMx_1x10_", country, ".txt"), skip=2)
  colnames(mortality[[country]]) <- c("Year", "Age", "Female", "Male", "Total")
  
  mortality[[country]] <- mortality[[country]] %>%
    mutate(Country = country)
  
}

# Join into single df
mortality <- do.call(rbind.data.frame, mortality)

# Reformat
mortality$Age <- as.integer(mortality$Age)
mortality$Female <- as.numeric(mortality$Female)
mortality$Male <- as.numeric(mortality$Male)
mortality$Total <- as.numeric(mortality$Total)
mortality$Country <- as.factor(mortality$Country)

# Gather to make it long format and get only values for total
mortality_g <- gather(mortality, "Demographic", "Rate", 3:5)
mortality_g_total <- filter(mortality_g, Demographic == "Total")

# Select decades to show
decades <- seq(1800, 2000, by=10)

mortality_g_total <- mortality_g_total %>%
                      filter(Year %in% paste0(decades, "-", decades + 9))

# Get number of time periods shown for colour scale
n_colours <- length(decades)
colors <- rev(turbo(n_colours))

# Plot
ggplot(data=mortality_g_total, aes(color=Year, x=Age, y=Rate)) +
  # Choose line or smoothed line or points
  geom_line(aes(color=Year),size=1,alpha=1) +
  geom_point(data=filter(mortality_g_total, Age==0), aes(color=Year,x=Age,y=Rate), size=1, show.legend=FALSE)+
  # Limit to 95 because ages above 100 are noisy and go above 100%
  coord_cartesian(xlim=c(0,95)) +
  facet_grid(cols=vars(Country)) +
  theme_classic() +
  theme(strip.background = element_blank()) +
  scale_x_continuous(breaks = seq(0, 100, by=10)) +
  scale_y_continuous(labels = scales::percent, trans='log2', breaks = c(0.0001, 0.001, 0.01, 0.1, 1)) +
  scale_color_manual(name = "Birth cohort", values = colors) +
  labs(title = "Annual death rate by age", 
       y = "Death rate", 
       x = "Age",
       color = "Birth cohort",
       caption = "Cohort death rates.\nSource: Human Mortality Database.\nUniversity of California, Berkeley (USA)\n(data downloaded on [12 Sep 2023])") 

ggsave(paste0(data_folder, "annual-mortality-time-countries.svg"), width = 12, height = 6)
