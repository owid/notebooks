library(tidyverse)
library(scales)
library(viridis)
library(ggrepel)
library(data.table)
library(readxl)
library(extrafont)

# Import Lato font
font_import(pattern = "Lato")
loadfonts(device = "mac") # use "win" for Windows, "mac" for macOS

# !!! Download spreadsheet and replace this with path to file
file_path <- ""

# Import spreadsheet
ab_drugs <- read_excel(paste0(file_path, "Antibiotic drug development.xlsx"),
                       sheet=1,
                       col_types=c("text", "numeric", "numeric", 
                                   "text", "text", 
                                   "text"))

# Arrange by year
ab_drugs <- ab_drugs %>%
  arrange(Year_discovery_reported) %>% 
  mutate(Antibiotic_class = factor(Antibiotic_class, levels = rev(Antibiotic_class)),
         # Add a small offset if the discovery and introduction years are the same
         Year_introduced = ifelse(Year_discovery_reported == Year_introduced, 
                                  Year_introduced + 0.1, Year_introduced)) 

ab_drugs <- as_tibble(ab_drugs)

ggplot(ab_drugs, aes(y = Antibiotic_class, 
                     label=Antibiotic_class)) +
  geom_segment(aes(x = Year_discovery_reported, 
                   xend = Year_introduced, 
                   yend = Antibiotic_class,
                   color = Year_discovery_reported), 
               size = 2) +  # Adjust `size` for line thickness
  geom_text(aes(x = Year_discovery_reported), hjust=1, nudge_x=-2, size=3.5, family="Lato") + 
  scale_color_gradient(low = "lightblue", high = "darkblue", guide = "none") +  # Gradient from light to dark blue
  labs(
    x = "Year",
    y = "",
    title = "Antibiotics: time from discovery to development",
    caption="Sources: Hutchings, Truman, Wilkinson (2019) Antibiotics: Past, present and future.") +
  theme_minimal(base_family = "Lato") +  # Set base font to Lato
  theme(
    panel.grid = element_blank(),
    axis.text.y = element_blank(),  # Adjust for better readability
    axis.text.x = element_text(size = 10),
    axis.ticks.x = element_line(color = "black"),
    axis.line.x = element_line(color = "black", size = 0.5),  # Add x-axis line
    plot.title = element_text(hjust = 0.5)  # Center the title
  ) +
  coord_cartesian(xlim=c(1890,2024)) +
  scale_x_continuous(breaks= seq(1900,2020,by=10), 
                     labels = seq(1900,2020,by=10),
                     position = "bottom") # Position x-axis at the bottom

ggsave(paste0(file_path, "antibiotics_time_to_development.svg"),height=8,width=10)


