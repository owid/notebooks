library(tidyverse)
library(scales)

# https://wonder.cdc.gov/
# Infant deaths - Linked records
# Group  by: Age of Infant at Death in days

# !!! Download and replace this with path to folder
data_folder <- ""

# Import
infant_2020 <- read_tsv(paste0(data_folder, "Linked Birth  Infant Death Records, 2017-2020 Expanded.txt"))

# Rename columns
names(infant_2020) <- c("Notes", "Age_days", "Age_code", "Deaths", "Births", "Death_rate")

# Remove string that says unreliable from Death_rate column
infant_2020$Death_rate <- gsub(" \\(Unreliable\\)", "", infant_2020$Death_rate)

# Convert Death_rate to numeric
infant_2020$Death_rate <- as.numeric(infant_2020$Death_rate)

infant_2020 <- infant_2020 %>% filter(Age_code != 999)

# PLOT 1: Daily mortality rates across the first year, per 1,000 births
ggplot(infant_2020, aes(x = Age_code, y = Death_rate)) +
  geom_point(size = 1) +
  scale_y_log10(limits = c(0.001, 10), breaks = c(0.001, 0.01, 0.1, 1, 10), labels=comma) +
  #scale_x_log10() +
  scale_x_continuous(breaks = seq(0, 360, by = 60)) +
  labs(title = "Infant mortality rates across the first year of life",
       subtitle = "The chances of dying are highest during the first few days of an infant's life.\nOver the following days, weeks, and months, their chances of dying decrease sharply.\n\nMortality rate per day, per 1,000 live births",
       x = "Age (days)",
       y = "",
       caption = "Source: US Centers for Disease Control and Prevention.") +
  theme_bw() 
  #theme(plot.title = element_text(hjust = 0.5, face = "bold", size = 16),
  #      plot.subtitle = element_text(hjust = 0.5, size = 12),
  #      plot.caption = element_text(hjust = 0, size = 10))


# Cumulative deaths calculation
infant_2020 <- infant_2020 %>%
  mutate(Cumulative_deaths = cumsum(Deaths))

# PLOT 2: Cumulative share of infants who have died by a given age
ggplot(infant_2020, aes(x = Age_code, y = Cumulative_deaths / Births)) +
  #geom_point() +
  geom_line(size = 1.5) +
  #scale_y_log10() +
  scale_y_continuous(labels = scales::percent, 
                     breaks = seq(0, 0.006, by = 0.001), limits = c(0, 0.006)) +
  scale_x_continuous(breaks = seq(0, 360, by = 60)) +
  labs(x = "Age (days)", y = "", 
       title = "Share of infants who have died over the first year",
       subtitle = "The cumulative share of infants who have died by a given age.",
       caption = "Based on US infant mortality rates between 2017-2020, using death certificates.\nSource: US Centers for Disease Control and Prevention.") +
  theme_bw()# +
 # theme(plot.title = element_text(hjust = 0.5, face = "bold"),
 #       plot.caption = element_text(hjust = 0, size = 9))

