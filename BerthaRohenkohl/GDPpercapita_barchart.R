library(tidyverse)
library(extrafont)
library(scales)
library(ggplot2)



# Import Lato font

library(showtext)
showtext_auto()

# Add Google Fonts
font_add_google("Lato")
font_add_google("Playfair Display", "Playfair Display SemiBold")


gdp_data <- read.csv("Data/gdp-per-capita-vs-gdp-per-capita-adjusted-for-inflation-from-current-us.csv") 

gdp_data <- rename(gdp_data, Country = Entity)
colnames(gdp_data)
colnames(gdp_data)[3]<- "GDP per capita (2021 int-$)"
colnames(gdp_data)[4]<- "GDP per capita (2021 US$)"

selected_countries <- c("Burkina Faso", "India", "Brazil", "Spain", "United States")
gdp_data <- gdp_data[gdp_data$Country %in% selected_countries & gdp_data$Year == 2023, ]

gdp_data$Country <- factor(gdp_data$Country, levels = selected_countries)

# Reshape 
gdp_data_long <- pivot_longer(gdp_data, 
                                     cols = c("GDP per capita (2021 US$)", "GDP per capita (2021 int-$)"),
                                     names_to = "Variant", 
                                     values_to = "Value")

gdp_data_long$Variant <- factor(gdp_data_long$Variant, levels = c("GDP per capita (2021 US$)", "GDP per capita (2021 int-$)"), 
                                labels = c("2021 US$", "2021 Int-$"))

# Plot vertical bars
chart_v1 <-  ggplot(gdp_data_long, aes(x = Country, y = Value, fill = Variant)) +
  geom_bar(stat = "identity", position = position_dodge(width = 0.7), width = 0.6) +
  scale_fill_manual(values = c("2021 US$" = "#1f78b4", "2021 Int-$" = "darkgreen")) +
  labs(x = NULL,y = "GDP per capita", fill = NULL, title = "GDP per capita (2023)", subtitle = "something here") +
  theme_minimal() +
  theme(
    legend.position = "top",
    panel.grid.major.x = element_blank(),
    panel.grid.major.y = element_line(linetype = "dashed", color = "grey"),
    panel.grid.minor = element_blank(),
    strip.text = element_text(size = 12, face = "bold", color = "grey30"), 
    axis.text = element_text(size = 10, color = "grey50"),
    axis.title = element_text(size = 12, color = "grey50")
  ) +
  scale_y_continuous(breaks = seq(0, 80000, by = 10000))

print(chart_v1)
