library(tidyverse)
library(extrafont)
library(scales)



# Import Lato font

library(showtext)
showtext_auto()

# Add Google Fonts
font_add_google("Lato")
font_add_google("Playfair Display", "Playfair Display SemiBold")



# Fetch the data
gdp_intdollars <- read.csv("data/gdp-per-capita-worldbank.csv")
gdp_constant2015 <- read.csv("data/gdp-per-capita-world-bank-constant-usd.csv")

colnames(gdp_intdollars)[4]<- "GDP per capita (int-$)"
colnames(gdp_constant2015)[4]<- "GDP per capita (2015 US$)"

#Filtering for latest year
filtered_gdp_intdollars_2022 <- gdp_intdollars %>%
  filter(Year == 2022, Code != "", Code != "OWID_WRL")

filtered_gdp_constant2015_2022 <- gdp_constant2015 %>%
  filter(Year == 2022, Code != "", Code != "OWID_WRL")

gdp_combined <-filtered_gdp_intdollars_2022 %>%
  inner_join(filtered_gdp_constant2015_2022, by = c("Entity", "Code", "Year"))


gdp_long <- gdp_combined %>%
  pivot_longer(
    cols = c(`GDP per capita (int-$)`, `GDP per capita (2015 US$)`),
    names_to = "Type",
    values_to = "GDP_Value"
  )

countries_to_highlight <- c("USA","IND","BRA", "BFA")  

gdp_long <- gdp_long %>%
  mutate(highlight = ifelse(Code %in% countries_to_highlight, "Highlighted", "Other"),
         color = ifelse(highlight == "Highlighted", "Highlighted", Type)
  )

# Swarmplot

swarm_plot <- ggplot(gdp_long, aes(x = Type, y = GDP_Value, color = color)) +
  geom_jitter(width = 0.08, alpha = 0.5, size = 6) +
  scale_color_manual(
    values = c(
      "Highlighted" = "red",   
      "GDP per capita (int-$)" = "lightblue",       
      "GDP per capita (2015 US$)" = "lightgreen"         
    ),
    name = "Group"
  ) +
  scale_y_log10() +
  # Labels and style
  labs(
    title = "GDP per capita in international and market dollars, 2022",
    subtitle = "Both series are adjusted for inflation. Market dollar data converts local currencies using the exchange rates observed in
currency markets. International dollar data adjusts for differences in the cost of living between countries.",
    y = "GDP per capita (log scale)",
    x = "",
    caption = "Source: Multiple sources compiled by World Bank (2024); World Bank (2023)" 
  ) +
  coord_flip() +  
  theme(
    # Background
    panel.background = element_rect(fill = "white", color = "grey70"), # White panel background
    plot.background = element_rect(fill = "white", color = "grey70"),  # White overall background
    
    # Text styling
    strip.text = element_text(size = 12, face = "bold", color = "grey30"), 
    text = element_text(family = "Lato", color = "grey50"),
    axis.text = element_text(size = 10, color = "grey50"),
    axis.title = element_text(size = 12, color = "grey50"),
    plot.title = element_text(size = 25, family = "Playfair Display SemiBold", color = "grey10"),
    plot.subtitle = element_text(size = 14, face = "plain", family = "Lato", color = "grey30"),
    plot.caption = element_text(size = 10, color = "grey50", hjust = 0), # Left-align caption
    plot.caption.position = "plot",                                   # Position caption below the plot
    
    # Lines in grey
    panel.grid = element_blank(),                        # Remove grid lines
    axis.ticks = element_line(color = "grey70"),         # Axis ticks in grey
    axis.ticks.length = unit(0.2, "cm"),                 # Customize tick length
    panel.border = element_blank()  # Removed conflicting panel border
  ) +
  theme(legend.position = "none")  


print(swarm_plot)


