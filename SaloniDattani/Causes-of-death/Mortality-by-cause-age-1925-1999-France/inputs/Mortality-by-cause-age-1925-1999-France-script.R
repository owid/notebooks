# This script is adapted from the paper:
# Visualizing compositional data on the Lexis surface
# BY Jonas Schöley, Frans Willekens (2017)
# Data and code can be downloaded from: https://www.demographic-research.org/Volumes/Vol36/21/
# While the original paper plotted the % of deaths from each cause, this script plots the mortality rate from each cause instead.

# Cause of death data comes from the Institut National d'Études Démographiques
# Vallin, J. and Mesle, F. (2014). Database on causes of death in France from 1925 to 1999 ´
# [electronic resource]. http://www.ined.fr/en/
# Death codes and further information can also be found on the Cause of Death database here: https://www.causesofdeath.org/docs/formats.pdf


###############################
# Prepare Cause of Death Data #
###############################

# This script loads the French cause of death data set which contains death
# counts by period, age, sex and cause of death. Within each period-age-sex
# combination the cause of death proportions and mortality rates are calculated.

# Init --------------------------------------------------------------------

library(tidyverse)
library(scales)

# INED COD ----------------------------------------------------------------

path <- "" # fill this in with the path to the folder containing the data files called cod_names.csv and ined-cod-fra-1925-1999-rates.csv

# import icd-9 codes and labels
cbook_cod <- read_csv(paste0(path, "cod_names.csv"), skip = 13)

# select age levels in correct order
lev_age <- c("<1","1-4","5-9","10-14","15-19","20-24","25-29",
             "30-34","35-39","40-44","45-49","50-54","55-59",
             "60-64","65-69","70-74","75-79","80-84","85-89",
             "90-94","95-99","100+")

# import data on deaths by year, sex, age & cause of death
read_csv(paste0(path, "ined-cod-fra-1925-1999-rates.csv"), skip  = 19) %>%
  filter(age != "total") %>%
  # apply factors
  mutate(
    age = factor(age, levels = lev_age, ordered = TRUE),
    cod = factor(cod, labels = cbook_cod$short)
  ) %>%
  # add numerical starting age and age group width
  arrange(age) %>%
  group_by(year, sex, cod) %>%
  mutate(
    age_start = c(0, 1, seq(5, 100, 5)),
    age_width = c(diff(age_start), 5)
  ) %>% ungroup() %>%
  # convert counts to cause specific shares on total deaths
  group_by(year, age, sex) %>%
  dplyr::select(year, age, age_start, age_width, sex, cod, mx) %>%
  mutate(px = mx / mx[cod == "Total"]) %>% ungroup() -> cod_prop #%>%
# filter to relevant data:
# a dataset of death proportions by cause of death over period, sex & age
#filter(cod != "Total") %>% droplevels() -> cod_prop

# The deaths by cause don't sum up to the number of deaths in the
# "Total" category. Therefore the proportions don't add up to unity.
# The "leftover" proportion gets assigned the cause of death "Other".
cod_prop %>%
  group_by(year, age, age_start, age_width, sex) %>%
  summarise(cod = "Other", px = 1 - sum(px)) %>%
  bind_rows(dplyr::select(cod_prop, -px), .) %>%
  ungroup() %>%
  arrange(year, age, sex) -> cod_prop

# 10 Causes of Death ------------------------------------------------------

# Calculate the death proportions of the 9 most common causes of death on all
# deaths. Aggregate the "leftovers" in category "Other".

# a vector of cods we are interested in
lab_cod_10 <- cbook_cod$short[c(2, # Infectious and parasitic diseases - Codes 001*-139*
                                3, # Neoplasms - Codes 140*-239*
                                1, # Total causes - Codes 000*-999*
                                10, # Diseases of the respiratory system - Codes 460*-519*
                                18, # Symptoms, signs and ill-defined conditions - Codes 780*-799*
                                19)] # Injury and poisoning - Codes 800*-999*
cod_prop %>%
  # filter to the cods we are interested in
  filter(cod %in% lab_cod_10) %>%
  # convert to long format to make facilitate calculations
  spread(key = cod, value = mx) %>%
  # calculate the proportion of deaths not due to our cods of interest
  mutate(Other = 1-rowSums(.[lab_cod_10])) %>%
  # convert back to long format
  gather_(key_col = "cod", value_col = "mx",
          gather_cols = c(lab_cod_10)) %>%
  arrange(sex, year, age, cod) -> cod_prop10

write_csv(mutate(cod_prop10, mx = sprintf("%1.5f", mx)), path = paste0(path,"cod10.csv"))


# Total Mortality Rates ---------------------------------------------------

# Calculate a Lexis surface of overall mortality rates.

read_csv(paste0(path,"ined-cod-fra-1925-1999-rates.csv"), skip = 19) %>%
  filter(age != "total", cod == "000*-999*") %>%
  dplyr::select(-cod) %>%
  # apply factors
  mutate(
    age = factor(age, levels = lev_age, ordered = TRUE)
  ) %>%
  # add numerical starting age and age group width
  arrange(age) %>%
  group_by(year, sex) %>%
  mutate(
    age_start = c(0, 1, seq(5, 100, 5)),
    age_width = c(diff(age_start), 5)
  ) %>% ungroup()  %>%
  mutate(mx = mx/1E5) -> mx

write_csv(mutate(mx, mx = sprintf("%1.5f", mx)), path = paste0(path,"mx.csv"))


#########################################################################
# Plot mortality rates by cause of death and age group over time #
#########################################################################

# Init --------------------------------------------------------------------

library(readr)
library(rgeos)
library(raster)
library(dplyr)
library(ggplot2)
library(RColorBrewer)

# Data --------------------------------------------------------------------

# proportions of 10 selected causes of death on
# all causes of death by year, age and sex
cod10 <- read_csv(paste0(path,"cod10.csv"))


# Plot Mortality rates ----------------------------------------------------

# Add color palette for 15 intervals
colourCount = 15
getPalette = colorRampPalette(brewer.pal(8, "PuBuGn"))
# Change Total to say All causes
# Neoplasms to say Cancers
# External to say External causes
cod10$cod[cod10$cod == "Total"] <- "All causes"
cod10$cod[cod10$cod == "Neoplasms"] <- "Cancers"
cod10$cod[cod10$cod == "External"] <- "External causes"

# Reorder cause categories for the plot
cod10 <- cod10 %>%
            mutate(cod = factor(cod)) %>%
            mutate(cod = fct_relevel(cod,
                                     c("All causes",
                                       "External causes",
                                       "Cancers",
                                       "Infections",
                                       "Respiratory diseases",
                                       "Ill-defined")))

# PLOT
plot_mortality_rates <-
  ggplot() +
  # Lexis surface - heatmap with custom breaks
  geom_tile(aes(x = year+0.5, y = age_start+age_width/2,
                width = 1, height = age_width,
                fill = cut(mx, breaks=c(1,2,5,
                                        10,20,50,
                                        100,200,500,
                                        1000,2000,5000,
                                        10000,20000,50000,
                                        100000))),
            data = filter(cod10, sex == "total")) +
  # Lexis surface outline
  #  geom_contour(aes(x = year+0.5, y = age_start+age_width/2,
  #                   z = mx),
  #                   linetype="dashed", color="#016450", size=0.2,
  #                   breaks = c(1,10,100,1000,10000,100000),
  #               data = filter(cod10, sex == "total")) +

  #  geom_textcontour((aes(x = year+0.5,
  #                        y = age_start+age_width/2,
  #                        z = mx)),
  #    data = filter(cod10, sex == "total"),
#    breaks = 10^(1:10),
#    size = 2.5, straight = TRUE, text_only = T) +

# Fill in the heatmap with the colour palette and add a legend with labels
scale_fill_manual(values = getPalette(colourCount),
                  guide = guide_legend(reverse = TRUE),
                  na.value = "#FFFFFF",
                  labels = c("1-2",
                             "2-5",
                             "5-10",
                             "10-20",
                             "20-50",
                             "50-100",
                             "100-200",
                             "200-500",
                             "500-1,000",
                             "1,000-2,000",
                             "2,000-5,000",
                             "5,000-10,000",
                             "10,000-20,000",
                             "20,000-50,000",
                             "50,000-100,000")) +
  scale_x_continuous("Year", expand = c(0.02, 0),
                     breaks = seq(1940, 2000, 20)) +
  scale_y_continuous("Age", expand = c(0, 0),
                     breaks = seq(0, 100, 20)) +
  # Facet - arrange them in three columns
  facet_wrap(~ cod, ncol = 3, as.table = TRUE) +
  # Lexis grid - diagonal, horizontal and vertical lines
  geom_hline(yintercept = seq(20, 100, 20),
             alpha = 0.2, lty = "dotted") +
  geom_vline(xintercept = seq(1940, 1980, 20),
             alpha = 0.2, lty = "dotted") +
  geom_abline(intercept = seq(-100, 100, 20)-1940,
              alpha = 0.2, lty = "dotted") +
  # Select yaxis limits
  coord_equal(ylim=c(0,100)) +
  # Theme minimal and select font sizes
  theme_minimal() +
  theme(
    axis.text   = element_text(colour = "black"),
    #axis.text.y = element_text(),
    #axis.text.x = element_text(),
    strip.text.x = element_text(size = 12),
    panel.margin = unit(0.3, "cm"),
    plot.title = element_text(size = 20)
  ) +
# Add titles
  labs(title = "Causes of death have changed over time and vary by age",
       subtitle = "Shown are the annual number of deaths per 100,000 people in each age group in France.",
       caption = "Source: Institut National d'Études Démographiques.\nAdapted from Jonas Schoëley and Frans Willekens (2017)",
       fill = "Mortality rate",
       x="",
       y="Age")

# Save to svg format
ggsave(paste0(path,"mortality_bycause.svg"), plot_mortality_rates,
       width = 13, height = 8)
