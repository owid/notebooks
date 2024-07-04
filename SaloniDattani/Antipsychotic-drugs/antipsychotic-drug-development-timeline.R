library(tidyverse)
library(scales)
library(viridis)
library(ggrepel)
library(data.table)
library(readxl)

# Import spreadsheet
file_path <- "owid/notebooks/SaloniDattani/Antipsychotic-drugs/"

ap_drugs <- read_excel(paste0(file_path, "Psychosis treatments.xlsx"),
                       sheet=1,
                       col_types=c("text", "text", "text", "text", 
                                   "numeric", "numeric", 
                                   "text", "text", "text", "text"))

# Remove drugs not approved in the US
ap_drugs <- ap_drugs %>% 
              filter(!is.na(Year_first_used_approved_US)) %>%
  # Shorten names            
              mutate(Treatment_class = str_replace_all(Treatment_class, 
                                           c("First-generation antipsychotic" = "First-generation",
                                             "Second-generation antipsychotic" = "Second-generation",
                                             "Third-generation antipsychotic" = "Third-generation")))

# Arrange by year
ap_drugs <- ap_drugs %>%
  arrange(Year_first_used_approved_US) 

# Give drugs an ID number to put them in order
setDT(ap_drugs)[, id := .GRP, by = Treatment_name]

ap_drugs <- as_tibble(ap_drugs)

# Select colors
group.colors <- c("First-generation" = "#38AABA", 
                   "Second-generation" = "#BC8E5A", 
                   "Third-generation" ="#970046")


ggplot(data=ap_drugs, aes(x=Year_first_used_approved_US, 
                          y=id, 
                          label=Treatment_name)) +
  geom_point(aes(fill=Treatment_class), color="black", size=2.5, pch=21, stroke=0.8) +
  # Show names
  geom_text(hjust=1, nudge_x=-3, size=3) + 
  theme_classic() +
  scale_fill_manual(values=group.colors) +
  scale_x_continuous(breaks= seq(1940,2020,by=10), 
                     labels = seq(1940,2020,by=10)) +
  theme(axis.text.y=element_blank(),
        axis.ticks.y=element_blank(),
        plot.title = element_text(size = 20)) +
  labs(title="The development of antipsychotic drugs",
       subtitle="The year when each antipsychotic drug was licensed in the United States.",
       x="",
       y="",
       fill="Generation of antipsychotic drug",
       caption="Sources: Pharmaceutical Manufacturing Encyclopedia (2013)\nand multiple sources compiled by Dattani (2024)") +
  coord_cartesian(xlim=c(1940,2024))

ggsave(paste0(file_path, "antipsychotics_timeline.svg"),height=8,width=10)


