library(tidyverse)
library(ggridges)

data_folder <- ""

cohort_df <- read_table(paste0(data_folder, "us-cohort-age-specific-fertility.txt"))
completed_df <- read_table(paste0(data_folder, "us-completed-cohort-fertility.txt")) ## Only needed if you want to colour the ridges by the completed CFR

# Data cleaning and transformation
cohort_df <- cohort_df %>%
  mutate(
    Age = as.numeric(gsub("[^0-9]", "", Age)), # Convert Age to numeric
    ASFR = as.numeric(ASFR),                  # Convert ASFR to numeric, coercing non-numeric values to NA
    Year = Cohort + Age                       # Calculate the year
  ) 

# Join completed_df to cohort_df
cohort_df <- cohort_df %>%
  left_join(completed_df %>% mutate(CCF = as.numeric(CCF)), by = "Cohort") # Ensure CCF is numeric


# Filter data to include cohorts between 1920 and 1980
cohort_df <- cohort_df %>%
  filter(Cohort >= 1918 & Cohort <= 1970) 

# Get the max ASFR for scaling
max_asfr <- max(cohort_df$ASFR, na.rm = TRUE)


### X axis: Age
# Ridgeline plot with gradient fill
ggplot(cohort_df, aes(
  x = Age, 
  y = reorder(factor(Cohort), -Cohort), 
  height = ASFR / max_asfr, 
  group = Cohort, 
  fill = ASFR  # Map the ASFR values to the fill aesthetic
)) +
  geom_ridgeline_gradient(scale = 7, color = "white", na.rm = TRUE) + # Gradient ridgelines
  scale_fill_gradient(name = "ASFR", low = "#88ABBF", high = "#8D687F", na.value = "grey80") + # Gradient fill based on ASFR
  scale_y_discrete(breaks = seq(1915, 1970, by = 5)) +
  labs(
    title = "Visualizing the US Baby Boom",
    subtitle = "Age-specific fertility rate with ASFR gradient fill",
    x = "Age",
    y = "Birth cohort",
    caption = "Source: Human Fertility Database (2024)"
  ) +
  theme_minimal(base_family = "sans") +
  theme(
    panel.background = element_rect(fill = "white", color = "white"), # Set panel background to white
    plot.background = element_rect(fill = "white", color = "white"), # Set plot background to white
    panel.grid.major = element_line(color = "white", size = 0.5), # Ensure gridlines are white
    panel.grid.minor = element_blank(), # Remove minor gridlines
    plot.title = element_text(color = "black", face = "bold", size = 16),
    plot.subtitle = element_text(color = "black", size = 12),
    plot.caption = element_text(color = "black", size = 10),
    axis.ticks = element_line(color = "white"), # Ensure axis ticks are white
    legend.position = "right", # Legend to the right of the plot
    legend.title = element_text(color = "black", size = 10, face = "bold"),
    legend.text = element_text(color = "black", size = 9)
  )

ggsave(paste0(data_folder, "ridgeline_cohort_ASFR_by_age.svg"), height=10, width=7)

## DARK MODE VERSION

# Ridgeline plot with correctly positioned vertical lines
ggplot(cohort_df, aes(x = Age, 
                      y = reorder(factor(Cohort), -Cohort), 
                      height = ASFR / max_asfr, 
                      group = Cohort,
                      fill = ASFR)) +
  geom_ridgeline_gradient(scale = 7, color = "#171831", na.rm = TRUE) + # Gradient ridgelines
  scale_fill_gradient(name = "ASFR", low = "#23395B", high = "#88ABBF", na.value = "grey80") + # Gradient fill based on ASFR
  scale_y_discrete(breaks = seq(1915, 1970, by = 5)) +
  labs(
    title = "Visualizing the US Baby Boom",
    subtitle = "Age-specific fertility rate",
    x = "Age",
    y = "Birth cohort",
    caption = "Source: Human Fertility Database (2024)"
  ) +
  theme_minimal(base_family = "sans") +
  theme(
    panel.background = element_rect(fill = "#171831", color = "#171831"),
    plot.background = element_rect(fill = "#171831", color = "#171831"),
    panel.grid.major = element_blank(), # Remove gridlines
    panel.grid.minor = element_blank(),   # Remove minor gridlines
    panel.grid.major.x = element_blank(), # Remove major vertical gridlines
    plot.title = element_text(color = "#f3d167", face = "bold", size = 16),
    plot.subtitle = element_text(color = "#f3d167", size = 12),
    plot.caption = element_text(color = "#f3d167", size = 10),
    axis.ticks = element_line(color = "white"),
    axis.title = element_text(color = "#f3d167"),
    axis.text = element_text(color = "#f3d167"), 
    legend.position = "right", # Place legend to the right of the plot
    legend.title = element_text(color = "#f3d167", size = 10, face = "bold"),
    legend.text = element_text(color = "#f3d167", size = 9)
  )
ggsave(paste0(data_folder, "ridgeline_cohort_ASFR_by_age-darkmode.svg"), height=10, width=7)



### Alternative chart where X axis is year

# Data frame with vertical line positions for specific ages within each curve, if needed
age_lines <- cohort_df %>%
  filter(Age %in% c(20, 25, 30, 35, 40)) %>%
  mutate(
    year = Cohort + Age,    # Calculate the corresponding year
    scaled_height = ASFR / max_asfr * 5  # Calculate scaled height for ASFR
  )

# Ridgeline plot with correctly positioned vertical lines
ggplot(cohort_df, aes(x = Year, 
                      y = reorder(factor(Cohort), -Cohort), 
                      height = ASFR / max_asfr, 
                      group = Cohort,
                      fill = ASFR)) +
  geom_ridgeline_gradient(scale = 7, color = "#171831", na.rm = TRUE) + # Gradient ridgelines
  scale_fill_gradient(name = "ASFR", low = "#88ABBF", high = "#8D687F", na.value = "grey80") + # Gradient fill based on ASFR
  scale_x_continuous(
    limits = c(1930, 2020),
    breaks = seq(1930, 2020, by = 10) # Add more x-axis labels every 10 years
  ) +
  scale_y_discrete(breaks = seq(1920, 1970, by = 5)) +
  labs(
    title = "Visualizing the US Baby Boom",
    subtitle = "Age-specific fertility rate",
    x = "Year",
    y = "Birth cohort",
    caption = "Source: Human Fertility Database (2024)"
  ) +
  theme_minimal(base_family = "sans") +
  theme(
    panel.background = element_rect(fill = "black", color = "black"),
    plot.background = element_rect(fill = "black", color = "black"),
    panel.grid.major = element_line(color = "#292E24", size = 0.5), # Set gridlines to dark grey
    panel.grid.minor = element_blank(),                              # Remove minor gridlines
    panel.grid.major.x = element_line(color = "#292E24", size = 0.5), # Add dark grey vertical gridlines
    axis.text = element_text(color = "white"),
    axis.title = element_text(color = "white"),
    plot.title = element_text(color = "white", face = "bold", size = 16),
    plot.subtitle = element_text(color = "white", size = 12),
    plot.caption = element_text(color = "white", size = 10),
    axis.ticks = element_line(color = "white"),
    legend.position = "none"
  )
ggsave(paste0(data_folder, "ridgeline_cohort_ASFR_by_year.svg"), height=10, width=7)

## HEATMAP VERSION

# Convert data to long format for visualization
cohort_df_long <- cohort_df %>%
  complete(Cohort, Age) %>% # Ensure all combinations are included
  replace_na(list(ASFR = 0)) # Replace missing ASFR with 0 for visualization

# Heatmap-like plot mimicking ridgelines
ggplot(cohort_df_long, aes(
  x = Age, 
  y = reorder(factor(Cohort), -Cohort), 
  fill = ASFR
)) +
  geom_tile(height = 0.8) + # Tiles for each combination of Age and Cohort
  scale_fill_gradient(name = "ASFR", low = "#88ABBF", high = "#8D687F", na.value = "grey80") + # Gradient fill for ASFR
  scale_y_discrete(breaks = seq(1915, 1970, by = 5)) +
  labs(
    title = "Visualizing the US Baby Boom",
    subtitle = "Age-specific fertility rate",
    x = "Age",
    y = "Birth cohort",
    caption = "Source: Human Fertility Database (2024)"
  ) +
  theme_minimal(base_family = "sans") +
  theme(
    panel.background = element_rect(fill = "white", color = "white"), # Set panel background to white
    plot.background = element_rect(fill = "white", color = "white"), # Set plot background to white
    panel.grid.major = element_line(color = "white", size = 0.5), # Ensure gridlines are white
    panel.grid.minor = element_blank(), # Remove minor gridlines
    plot.title = element_text(color = "black", face = "bold", size = 16),
    plot.subtitle = element_text(color = "black", size = 12),
    plot.caption = element_text(color = "black", size = 10),
    axis.ticks = element_line(color = "white"), # Ensure axis ticks are white
    legend.position = "right", # Legend to the right of the plot
    legend.title = element_text(color = "black", size = 10, face = "bold"),
    legend.text = element_text(color = "black", size = 9)
  )
ggsave(paste0(data_folder, "heatmap_cohort_ASFR_by_year.svg"), height=10, width=7)



