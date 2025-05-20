library(ggplot2)
library(dplyr)
library(ggthemes)
library(scales) 
library(extrafont)
font_import(prompt = FALSE)  # Automatically import fonts without asking
source('themes.R')

df <- read.csv('https://catalog.ourworldindata.org/external/health/latest/measles_state_level/measles.csv')
colnames(df) <- c("country", "year", "cases", "source", "case_rate")
df<- df %>% 
  filter(country != "American Samoa") %>%
  filter(country!= "District of Columbia") %>%
  filter(country!= "Guam") %>% 
  filter(country != "Northern Mariana Islands") %>% 
  filter(country != "Puerto Rico") %>%
  filter(country != "Virgin Islands, U.S.") %>%
  filter(year > 1929) 

df$case_rate <- as.numeric(df$case_rate)

df$case_rate_log <- log10(df$case_rate + 1)  # +1 to avoid log(0)

# Define breaks and colors
scale_breaks <- c(0, 1, 3, 10, 30, 100, 300, 1000)
scale_colors <- c("#FFFFCC", "#C7E9B4", "#7FCDBB", "#41B6C4", "#1D91C0", "#225EA8", "#0C2C84", "#081D58")

# Transformed breaks for legend positions
log_breaks <- log10(scale_breaks + 1)  # same +1 offset

p <- ggplot(df, aes(x = year, y = country, fill = case_rate_log)) +
  geom_tile(color = "white", size = 0.2) +
  scale_fill_gradientn(
    colors = scale_colors,
    values = rescale(log_breaks),  # now evenly spaced in log space
    breaks = log_breaks,
    labels = scale_breaks,
    name = "Case rate"
  ) +
  theme_owid_combined() +
  labs(
    title = "Measles cases per 100,000 people",
    x = "Year",
    y = "Country"
  ) +
  theme(axis.text.x = element_text(hjust = 1)) +
  scale_y_discrete(limits = rev) +
  geom_vline(xintercept = 1963, lwd = 1.2, color = "#cf0a66")+
  geom_vline(xintercept = 1971, lwd = 1.2, color = "#cf0a66")+
  geom_vline(xintercept = 1980, lwd = 1.2, color = "#cf0a66")
p
# Save as a PDF then convert to an SVG in Inkscape - direct saving to SVG in R doesn't appear to work correctly (the chart is just a black rectangle when opened in Figma)
ggsave("output/measles_plot_logged_test.pdf", plot = p, width = 18, height = 12, units = "in", dpi = 1200)
