# Install and load necessary packages
library(sf)
library(readxl)
library(tidyverse)
library(rnaturalearth)
library(rnaturalearthdata)

file_path <- ""

# Get the world map outline
world <- ne_countries(scale = "medium", returnclass = "sf")
africa <- world %>% filter(continent == "Africa")

# Read the shapefiles
shapefile <- st_read(paste0(file_path, "IUs_9May2024.shp"))

#import data
survey_data <- read_excel(paste0(file_path, "surveys_for_Our_World_in_Data_2024_05_30.xlsx"), sheet = "surveys") 
# Inspect the shapefile and survey data
head(shapefile)
head(survey_data)

# Merge the shapefile with the survey data on the common column (e.g., geoconnect in shapefile and geo_id in survey_data)
# Assuming 'geoconnect' in shapefile corresponds to 'geo_id' in survey_data
merged_data <- shapefile %>%
  left_join(survey_data, by = c("geoconnect" = "geo_id"))

### BASELINE DATA

# Ensure tf_category_string is a factor with levels ordered as desired
merged_data$tf_category_string <- factor(merged_data$tf_category_string, levels = c("< 5", "5-9.9", "10-29.9", "30-49.9", ">= 50"))

# Filter the data to include only baseline surveys
baseline_data <- merged_data %>%
  filter(survey_type == "BL")

# Define color palette - color brewer orange reds
color_palette <- c("#d4b9da", "#c994c7", "#df65b0", "#dd1c77", "#980043")

# Use a smaller subset of the data for testing
subset_data <- baseline_data %>% slice(1:4000) # adjust the number to match your testing needs - currently set to full dataset

# Create the choropleth map with the specified customizations
baseline_gg <- ggplot(data = subset_data) +
  geom_sf(data = africa, fill = "gray90", color = "gray50") + # Base world map
  geom_sf(data = subset_data, aes(fill = tf_category_string), color = NA) + # Overlay district data without outlines
  coord_sf(xlim = c(-20, 60), ylim = c(-35, 40)) + # Set the limits for Africa
  scale_fill_manual(values = color_palette) + # Apply the color palette
  theme_minimal() +
  theme(
    axis.text = element_blank(),  # Remove axis text
    axis.title = element_blank(), # Remove axis titles
    panel.grid = element_blank()  # Remove grid
  ) +
  labs(title = "Decline in trachoma prevalence over time",
       fill = "Prevalence of follicular trachoma\nin children aged 1-9 years old",
       subtitle = "Baseline surveys")

ggsave(plot = baseline_gg, filename = paste0(file_path, "baseline_map.svg"))


#### MOST RECENT DATA

# Filter the survey data to keep only the most recent year for each geo_id
survey_data_filtered <- survey_data %>%
  group_by(geo_id) %>%
  filter(survey_year == max(survey_year)) %>%
  ungroup()

merged_data1 <- shapefile %>%
  right_join(survey_data_filtered, by = c("geoconnect" = "geo_id"))

merged_data1$tf_category_string <- factor(merged_data1$tf_category_string, levels = c("< 5", "5-9.9", "10-29.9", "30-49.9", ">= 50"))

# Use a smaller subset of the data for testing
subset_data1 <- merged_data1 %>% slice(1:5000) # adjust the number to match your testing needs - currently set to full dataset


# Create the choropleth map with the specified customizations
final_gg <- ggplot() +
  geom_sf(data = africa, fill = "gray90", color = "gray50") + # Base world map
  geom_sf(data = subset_data1, aes(fill = tf_category_string), color = NA) + # Overlay district data without outlines
  scale_fill_manual(values = color_palette) + # Apply the reversed color palette
  coord_sf(xlim = c(-20, 60), ylim = c(-35, 40)) + # Set the limits for Africa
  theme_minimal() +
  theme(
    axis.text = element_blank(),  # Remove axis text
    axis.title = element_blank(), # Remove axis titles
    panel.grid = element_blank()  # Remove grid
  ) +
  labs(title = "Decline in trachoma prevalence over time",
       fill = "Prevalence of follicular trachoma\nin children aged 1-9 years old",
       subtitle = "Final surveys")

ggsave(plot = final_gg, filename = paste0(file_path, "final_map.svg"))

