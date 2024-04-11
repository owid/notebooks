# Open libraries
library(tidyverse)
library(scales)
library(viridis)

# Data source:
# CDC Wonder https://wonder.cdc.gov/

# 1. Underlying cause of death - group by single age - group by ICD chapter (By cause)
# Saved link: https://wonder.cdc.gov/controller/saved/D158/D386F982 --> save as "underlying-cod-2018-2021-all-causes.txt"

# 2. Underlying cause of death - group by single age (All causes)
# Saved link: https://wonder.cdc.gov/controller/saved/D158/D386F982 --> save as "underlying-cod-2018-2021-by-cause-by-cause.txt"

# Download and replace this with path to folder
data_folder <- ""


#----- DATA IMPORT

### Import all cause age-specific mortality
all_causes <- read_tsv(paste0(data_folder, "underlying-cod-2018-2021-all-causes.txt"))

# Remove quotation marks
all_causes <- all_causes %>% 
  mutate(across(
    everything(),
    ~ map_chr(.x, ~ gsub("\"", "", .x))
  ))

# Rename col names & add dummy variables for all causes to join later
all_causes <- all_causes %>%
  rename(Age = `Single-Year Ages Code`) %>%
  rename(Crude_rate = `Crude Rate`) %>%
  mutate(ICD_chapter = "All causes") %>%
  mutate(ICD_chapter_code = "ALL")

# Change to numeric
all_causes$Age <- as.numeric(all_causes$Age)
all_causes$Deaths <- as.numeric(all_causes$Deaths)
all_causes$Population <- as.numeric(all_causes$Population)
all_causes$Crude_rate <- as.numeric(all_causes$Crude_rate)
all_causes$ICD_chapter <- as.factor(all_causes$ICD_chapter)

# Keep ages 0-100
all_causes <- all_causes %>%
  filter(Age >= 0) %>%
  filter(Age <= 100)

# Rearrange columns
all_causes <- all_causes %>%
  select(Notes, `Single-Year Ages`, Age, ICD_chapter, ICD_chapter_code, Deaths, Population, Crude_rate)

### Import age-specific mortality by ICD chapter
by_cause <- read_tsv(paste0(data_folder, "underlying-cod-2018-2021-by-cause-by-cause.txt"))

# Remove quotation marks
by_cause <- by_cause %>% 
  mutate(across(
    everything(),
    ~ map_chr(.x, ~ gsub("\"", "", .x))
  ))

# Rename col names
by_cause <- by_cause %>%
  rename(Age = `Single-Year Ages Code`) %>%
  rename(Crude_rate = `Crude Rate`) %>%
  rename(ICD_chapter = `ICD Chapter`) %>%
  rename(ICD_chapter_code = `ICD Chapter Code`)

# Change to numeric
by_cause$Age <- as.numeric(by_cause$Age)
by_cause$Deaths <- as.numeric(by_cause$Deaths)
by_cause$Population <- as.numeric(by_cause$Population)
by_cause$Crude_rate <- as.numeric(by_cause$Crude_rate)
by_cause$ICD_chapter <- as.factor(by_cause$ICD_chapter)

# Keep ages 0-100
by_cause <- by_cause %>%
  filter(Age >= 0) %>%
  filter(Age <= 100)

# Create category for disease-related
disease_related <- by_cause %>%
  filter(ICD_chapter != "External causes of morbidity and mortality") %>%
  filter(ICD_chapter != "Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified") %>%
  group_by(Age) %>%
  summarise(Deaths = sum(Deaths), Population = min(Population)) %>%
  mutate(ICD_chapter = "Disease related", Crude_rate = (Deaths / Population) * 100000)

#--- JOIN
mx_age <- bind_rows(all_causes, by_cause)
mx_age <- bind_rows(mx_age, disease_related)


# Select cause categories to retain from plot
mx_age <- mx_age %>%
  filter(ICD_chapter %in% c("All causes",
                            "Disease related",
                            "External causes of morbidity and mortality")) 

# Rename ICD chapters to human-readable names
mx_age$ICD_chapter <- recode(mx_age$ICD_chapter, 
                             "External causes of morbidity and mortality" = "External causes")

#--- PLOT 1: all together
group.colors <- c("All causes" = "black", 
                  "Disease related" = "#4C6A9C", 
                  "External causes" ="#B16214")

plot_together <- ggplot(mx_age, 
                        aes(x=Age, y=Crude_rate, color=ICD_chapter, linetype=ICD_chapter)) +
  geom_line(linewidth=1) +
  theme_classic() +
  labs(title = "Annual mortality rate, per 100,000 people",
       subtitle = "Disease related causes includes all cause categories apart from external causes and signs and symptoms.",
       caption = "Source: United States Centers for Disease Control and Prevention") +
  ylab("") +
  facet_wrap(vars(Gender)) +
  theme(strip.background = element_blank()) +
  scale_color_manual(values=group.colors) +
  scale_x_continuous(breaks = seq(0, 100, by=20)) +
  scale_linetype_manual(values = c("All causes" = "solid", 
                                   "Disease related" = "dashed", 
                                   "External causes" = "dashed")) +
  scale_y_continuous(labels = comma, trans='log2', breaks = c(0.1,1,10,100,1000,10000,100000)) 

plot_together

ggsave(paste0(data_folder, "together_plot.svg"), plot = plot_together, 
       width = 10, height = 6)
