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

ab_drugs <- read_excel(paste0(file_path, "Antibiotic drug development.xlsx"),
                       sheet=1,
                       col_types=c("text", "numeric", "numeric", 
                                   "text", "text", 
                                   "text"))

# Arrange by year
ab_drugs <- ab_drugs %>%
  arrange(Year_introduced) 

# Give drugs an ID number to put them in order
setDT(ab_drugs)[, id := .GRP, by = Antibiotic_class]

ab_drugs <- as_tibble(ab_drugs)

# Select colors
group.colors <- c("Actinomycetes" = "#38AABA", 
                   "Other bacteria" = "#0C4767", 
                   "Fungi" ="#970046",
                  "Synthetic" = "white")

ggplot(data=ab_drugs, aes(x=Year_introduced, 
                          y=id, 
                          label=Antibiotic_class)) +
  geom_point(aes(fill=Source_of_antibiotic), color="black", size=2.5, pch=21, stroke=0.8) +
  # Show names
  geom_text(hjust=1, nudge_x=-2.5, size=3.5, family="Lato") + 
  geom_text(aes(label=Example_drug), hjust=0, nudge_x=2.5, size=3.5, family="Lato", color="#999999", fontface="italic") + 
  theme_classic() +
  scale_fill_manual(values=group.colors) +
  theme(text = element_text(family = "Lato"), # Set Lato for all text elements
        axis.text.y=element_blank(),
        axis.ticks.y=element_blank(),
        plot.title = element_text(size = 20),
        axis.title.x.top = element_text(vjust = 1.5), # Adjust x-axis title position at the top
        axis.text.x.top = element_text(vjust = 1.5),  # Adjust x-axis text position at the top
        axis.ticks.x.top = element_line(),           # Add ticks to the top x-axis
        plot.margin = margin(t = 10, r = 10, b = 10, l = 10)) +
  labs(title="Timeline of the development of antibiotic drugs",
       subtitle="The year when each antibiotic drug class was first introduced for medical use.",
       x="",
       y="",
       fill="Source of drug",
       caption="Sources: Hutchings, Truman, Wilkinson (2019) Antibiotics: Past, present and future.") +
  coord_cartesian(xlim=c(1900,2024)) +
  scale_y_reverse() + # Flip y-axis
  scale_x_continuous(breaks= seq(1900,2020,by=10), 
                     labels = seq(1900,2020,by=10),
                     position = "bottom") # Position x-axis at the bottom


ggsave(paste0(file_path, "antibiotics_timeline.svg"),height=8,width=10)




