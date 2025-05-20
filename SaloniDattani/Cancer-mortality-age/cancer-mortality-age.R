
# Open libraries
library(tidyverse)
library(scales)
library(extrafont)

# Import Lato font
font_import(pattern = "Lato")
loadfonts(device = "all") # use "win" for Windows, "mac" for macOS


# Data source:
# CDC Wonder https://wonder.cdc.gov/
# Underlying cause of death -> group by: single-year age group, ICD-10 113 Cause List
# In section 6, click ICD-10 113 Cause list
# Highlight #Malignant neoplasms until #In situ neoplasms
# Download and save to data_folder
# https://wonder.cdc.gov/controller/saved/D158/D406F321

# !!! Download and replace this with path to folder
data_folder <- ""


# Import
raw_df <- read_tsv(paste0(data_folder, "Underlying Cause of Death, 2018-2022, Single Race-Cancer-ICD-10-113.txt"))
colnames(raw_df) <- c("Notes", "Age_long", "Age",  "ICD_long", "ICD", "Deaths_n", "Population", "Death_crude_rate")

# Data source:
# CDC Wonder https://wonder.cdc.gov/
# Underlying cause of death -> group by: single-year age group, ICD-10 113 Cause List, Gender
# In section 6, click ICD-10 113 Cause list
# Highlight #Malignant neoplasms until #In situ neoplasms
# Download and save to data_folder
# https://wonder.cdc.gov/controller/saved/D158/D406F645
raw_gender_df <- read_tsv(paste0(data_folder, "Underlying Cause of Death, 2018-2022, Single Race-Cancer-ICD-10-113, by sex.txt"))
colnames(raw_gender_df) <- c("Notes", "Age_long", "Age",  "ICD_long", "ICD", "Gender_long", "Gender", "Deaths_n", "Population", "Death_crude_rate")

# Recode vars
coded_df <- raw_df

coded_df$Age <- as.numeric(coded_df$Age)
#coded_df$Gender <- as.factor(coded_df$Gender)
coded_df$ICD_long <- as.factor(coded_df$ICD_long)
coded_df$Death_crude_rate <- as.numeric(coded_df$Death_crude_rate)
coded_df$Population <- as.numeric(coded_df$Population)

# Rename ICD_long to be more human-readable
rename_vector <- c(
  "#In situ neoplasms, benign neoplasms and neoplasms of uncertain or unknown behavior (D00-D48)" = "In situ, uncertain and benign cancers",
  "#Malignant neoplasms (C00-C97)" = "Cat_Malignant cancers",
  "All other and unspecified malignant neoplasms (C17,C23-C24,C26-C31,C37-C41,C44-C49,C51-C52,C57-C60,C62-C63,C66,C68-C69,C73-C80,C97)" = "Other unspecified cancers",
  "Hodgkin disease (C81)" = "Hodgkin disease",
  "Leukemia (C91-C95)" = "Leukemia",
  "Malignant melanoma of skin (C43)" = "Melanoma skin cancer",
  "Malignant neoplasm of bladder (C67)" = "Bladder cancer",
  "Malignant neoplasm of breast (C50)" = "Breast cancer",
  "Malignant neoplasm of cervix uteri (C53)" = "Cervical cancer",
  "Malignant neoplasm of esophagus (C15)" = "Esophageal cancer",
  "Malignant neoplasm of larynx (C32)" = "Laryngeal cancer",
  "Malignant neoplasm of ovary (C56)" = "Ovarian cancer",
  "Malignant neoplasm of pancreas (C25)" = "Pancreatic cancer",
  "Malignant neoplasm of prostate (C61)" = "Prostate cancer",
  "Malignant neoplasm of stomach (C16)" = "Stomach cancer",
  "Malignant neoplasms of colon, rectum and anus (C18-C21)" = "Colorectal cancer",
  "Malignant neoplasms of corpus uteri and uterus, part unspecified (C54-C55)" = "Uterine cancer",
  "Malignant neoplasms of kidney and renal pelvis (C64-C65)" = "Kidney cancer",
  "Malignant neoplasms of lip, oral cavity and pharynx (C00-C14)" = "Oral and pharyngeal cancer",
  "Malignant neoplasms of liver and intrahepatic bile ducts (C22)" = "Liver cancer",
  "Malignant neoplasms of lymphoid, hematopoietic and related tissue (C81-C96)" = "Cat_Lymphoid and blood cancers",
  "Malignant neoplasms of meninges, brain and other parts of central nervous system (C70-C72)" = "Brain and CNS cancers",
  "Malignant neoplasms of trachea, bronchus and lung (C33-C34)" = "Lung cancer",
  "Multiple myeloma and immunoproliferative neoplasms (C88,C90)" = "Multiple myeloma",
  "Non-Hodgkin lymphoma (C82-C85)" = "Non-Hodgkin lymphoma",
  "Other and unspecified malignant neoplasms of lymphoid, hematopoietic and related tissue (C96)" = "Other lymphoid and blood cancers"
)

# Note that Malignant neoplasms of lymphoid, hematopoietic and related tissue (C81-C96) includes several other categories; it will be removed later.

# Apply the renaming
coded_df <- coded_df %>%
  mutate(ICD_long = recode(ICD_long, !!!rename_vector))

# Remove NAs
coded_df <- coded_df %>% 
  filter(#!is.na(Gender), 
    !is.na(Age_long), 
    !is.na(ICD), 
    !is.na(Deaths_n), 
    !is.na(Population))


# Calculate the % of deaths in each age and gender group that are in each ICD code
coded_df <- coded_df %>%
  group_by(Age) %>% #, Gender) %>%
  mutate(Total_Deaths_Group = sum(Deaths_n)) %>%
  ungroup() %>%
  mutate(Percentage_Deaths_ICD = (Deaths_n / Total_Deaths_Group) * 100)

# Order the ICD categories in alphabetical order
coded_df$ICD_long <- factor(coded_df$ICD_long, 
                            levels = sort(levels(coded_df$ICD_long)))

# Remove the category from the main df
coded_df <- coded_df %>% 
  filter(!ICD_long %in% c(
    "Cat_Malignant cancers",
    "Cat_Lymphoid and blood cancers"
  ))

# Specify OWID colors
owid_colors <- c("#6D3E91", "#00847E", "#58AC8C", "#286BBB",
                 "#883039", "#BC8E5A", "#00295B", "#C15065",
                 "#18470F", "#9A5129", "#E56E5A", "#A2559C",
                 "#38AABA", "#578145", "#970046", "#C05917",
                 "#B13507", "#4C6A9C", "#CF0A66", "#00875E",
                 "#B16214", "#8C4569", "#3B8E1D", "#D73C50")

# Remove these cancers from the panels of the line chart
coded_df_line <- coded_df %>%
  filter(!ICD_long %in% c(
    "Other unspecified lymphoid cancers", 
    "Laryngeal cancer", 
    "Hodgkin disease",
    "Other lymphoid and blood cancers"
  ))

# In the line chart, replace Cervical, Breast, Uterine, and Ovarian cancer death rates with female only death rates. Replace Prostate cancer with male only death rates.
coded_gender_df <- raw_gender_df

coded_gender_df$Age <- as.numeric(coded_gender_df$Age)
coded_gender_df$Gender <- as.factor(coded_gender_df$Gender)
coded_gender_df$ICD_long <- as.factor(coded_gender_df$ICD_long)
coded_gender_df$Death_crude_rate <- as.numeric(coded_gender_df$Death_crude_rate)
coded_gender_df$Population <- as.numeric(coded_gender_df$Population)

# Apply the renaming
coded_gender_df <- coded_gender_df %>%
  mutate(ICD_long = recode(ICD_long, !!!rename_vector))

# Remove NAs
coded_gender_df <- coded_gender_df %>% 
  filter(!is.na(Gender), 
         !is.na(Age_long), 
         !is.na(ICD), 
         !is.na(Deaths_n), 
         !is.na(Population))


# Order the ICD categories in alphabetical order
coded_gender_df$ICD_long <- factor(coded_gender_df$ICD_long, 
                                   levels = sort(levels(coded_gender_df$ICD_long)))

# Remove prostate, breast, cervical, uterine, ovarian cancers from the original line chart
coded_df_line <- coded_df_line %>%
  filter(!ICD_long %in% c("Prostate cancer", "Breast cancer", "Ovarian cancer", "Uterine cancer", "Cervical cancer"))
# Keep only these cancers in the coded gender_df and add this to the df
# Retain the rows where Gender is F where ICD_long is one of Breast cancer, Uterine cancer or Ovarian cancer; and also retain rows where Gender is M where ICD_long is Prostate cancer
coded_gender_df <- coded_gender_df %>%
  filter(ICD_long %in% c("Prostate cancer", "Breast cancer", "Ovarian cancer", "Uterine cancer", "Cervical cancer"))  %>%
  filter((Gender == "F" & ICD_long %in% c("Breast cancer", "Uterine cancer", "Ovarian cancer", "Cervical cancer")) | (Gender == "M" & ICD_long == "Prostate cancer")) %>%
  select(-c(Gender_long, Gender))

joined_line_df <- bind_rows(coded_df_line, coded_gender_df)

# Rename the categories to make this clear
rename_vector_gender <- c(
  "Cervical cancer" = "Cervical cancer (women)",
  "Breast cancer" = "Breast cancer (women)",
  "Uterine cancer" = "Uterine cancer (women)",
  "Ovarian cancer" = "Ovarian cancer (women)",
  "Prostate cancer" = "Prostate cancer (men)")

# Join dataset so it contains death rates across both sexes for most cancers, but single sex death rates for the selected cancers
joined_line_df <- joined_line_df %>%
  mutate(ICD_long = recode(ICD_long, !!!rename_vector_gender))

# 1. Create line charts showing death rate from each cause
ggplot(joined_line_df, aes(x = Age, y = Death_crude_rate, color = ICD_long)) +
  geom_line() + # Death rate
  facet_wrap(~ ICD_long, ncol = 4, scales = "free_y") + 
  scale_color_manual(values = owid_colors) + 
  scale_x_continuous(breaks = seq(0, 100, by = 20)) + # X-axis breaks at multiples of 20
  # scale_y_log10() + # Remove hash to apply log scale to y-axis
  labs(
    title = "How do cancer mortality risks vary with age?",
    subtitle = "The crude death rate per 100,000 from each ICD-10 113 cancer category, between 2018-2022 in the United States",
    x = "Age",
    y = "",
    color = "ICD-10 113 category",
    caption = "Data source: CDC Wonder database, using data on the underlying cause of death from 2018–2022\nChart by Saloni Dattani\nFemale death rates are shown for breast, uterine, ovarian and cervical cancers\nMale death rates are shown for prostate cancer."
  ) +
  theme_minimal() + 
  guides(fill = guide_legend(title.position = "top")) +
  theme(text = element_text(family = "Lato"),
        strip.text.x = element_text(size = 12),
        axis.text = element_text(size = 10),
        axis.title = element_text(size = 12),
        legend.position = "none", # Remove legend
        plot.title = element_text(face = "bold", size = 16))
ggsave(paste0(data_folder, "cancer-death-rates-by-age-usa.svg"), height=8, width=12)

# Remove these cancers from the panels of the share chart, since its a broader group 
coded_df <- coded_df %>%
  filter(!ICD_long %in% c(
    "Cat_Lymphoid and blood cancers"
  ))

# Combine some of the cancers for the share chart

# Define the groups to be merged
merge_groups <- list(
  list(
    new_category = "Non-leukemia lymphatic and blood cancers",
    old_categories = c("Hodgkin disease", "Non-Hodgkin lymphoma", "Multiple myeloma", "Other lymphoid and blood cancers")
  ),
  # list(
  #   new_category = "Digestive system cancers",
  #   old_categories = c("Colorectal cancer", "Esophageal cancer", "Liver cancer", "Pancreatic cancer", "Stomach cancer")
  # ),
  list(
    new_category = "Cervical, uterine, and ovarian cancers",
    old_categories = c("Cervical cancer", "Uterine cancer", "Ovarian cancer")
  ),
  list(
    new_category = "Head, neck, and oral cancers",
    old_categories = c("Oral and pharyngeal cancer", "Laryngeal cancer")
  ),
  list(
    new_category = "Bladder and kidney cancers",
    old_categories = c("Bladder cancer", "Kidney cancer")
  ),
  list(
    new_category = "Skin cancers",
    old_categories = c("Melanoma skin cancer")
  ),
  list(
    new_category = "Other/unspecified cancers",
    old_categories = c("Other unspecified cancers", "In situ, uncertain and benign cancers")
  )
)


# Function to merge categories based on the list
merge_cancer_categories <- function(df, group) {
  merged_rows <- df %>%
    filter(ICD_long %in% group$old_categories) %>%
    group_by(Age) %>%
    summarise(
      ICD_long = group$new_category,
      Deaths_n = sum(Deaths_n, na.rm = TRUE),
      Population = first(Population),
      Death_crude_rate = sum(Death_crude_rate, na.rm = TRUE),
      Percentage_Deaths_ICD = sum(Percentage_Deaths_ICD, na.rm = TRUE)
    )
  
  # Filter out the old categories and append the new merged rows
  df %>%
    filter(!ICD_long %in% group$old_categories) %>%
    bind_rows(merged_rows)
}

# Apply the function to all merge groups using purrr::reduce to handle multiple merges
final_df <- reduce(merge_groups, merge_cancer_categories, .init = coded_df) %>%
  arrange(Age)

# 2. Create chart showing share of deaths from each cause
ggplot(final_df, aes(x = Age, y = Percentage_Deaths_ICD, fill = ICD_long)) +
  #geom_bar(stat = "identity", position = "fill", alpha = 0.7) +
  geom_area(position = "fill", alpha = 0.7) + 
  #facet_wrap(~ Gender_long, scales = "free_y", nrow = 2) + 
  scale_fill_manual(values = owid_colors) + 
  scale_x_continuous(breaks = seq(0, 100, by = 20)) + # X-axis breaks at multiples of 20
  scale_y_continuous(breaks = seq(0, 1, by=0.2)) + # Y-axis breaks for geom_area version (in decimal share)
  #scale_y_continuous(breaks = seq(0, 1, by=0.2), labels = scales::label_percent()) + # Y-axis breaks for geom_bar version (in percentages)
  labs(
    title = "Which cancers are people dying from at different ages?",
    subtitle = "The share of cancer deaths from each cancer, between 2018-2022 in the United States, using ICD-10 113 category codes",
    x = "Age",
    y = "",
    fill = "ICD-10 113 category",
    caption = "Data source: CDC Wonder database, using data on the underlying cause of death from 2018–2022\nChart by Saloni Dattani\nFor clarity, several cancer categories have been merged. 'Non-leukemia lymphatic and blood cancers' includes Hodgkin disease, Non-Hodgkin lymphoma, multiple myeloma, and other lymphoid and blood cancers.\n'Head, neck, and oral cancers' includes oral, pharyngeal, and laryngeal cancers. 'Other/unspecified cancers' combines in situ, uncertain, benign, and other unspecified cancers."
  ) +
  theme_minimal() + 
  guides(fill = guide_legend(title.position = "top")) +
  theme(text = element_text(family = "Lato"),
        strip.text.x = element_text(size = 12, face = "bold"),
        axis.text = element_text(size = 10),
        axis.title = element_text(size = 12),
        legend.position = "right", # Place legend at the right
        legend.box = "vertical", # Arrange legend items horizontally
        plot.title = element_text(face = "bold", size = 16),
        panel.grid.major.y = element_blank(), # Remove y-axis major grid lines
        panel.grid.minor.y = element_blank() # Remove y-axis minor grid lines 
        #axis.text.y = element_text(margin = margin(r = -20)) # Move y-axis text closer to the axis
  )  
ggsave(paste0(data_folder, "cancer-deaths-relative-share-by-age-usa.svg"), height=8, width=10)

# 3. Create chart showing number of deaths from each cause
ggplot(final_df, aes(x = Age, y = Deaths_n, fill = ICD_long)) +
  geom_bar(stat = "identity", alpha = 0.7) + # Number of deaths
  scale_fill_manual(values = owid_colors) + 
  scale_x_continuous(breaks = seq(0, 100, by = 20)) + # X-axis breaks at multiples of 20
  scale_y_continuous(labels = comma) + #y-axis labels with commas for thousand separator
  labs(
    title = "How many people die from each cancer at different ages?",
    subtitle = "The number of deaths from each cancer cause of death category, between 2018-2021 in the United States",
    x = "Age",
    y = "",
    fill = "ICD cause of death category",
    caption = "Data source: CDC Wonder database (2018–2022)\nChart by Saloni Dattani\nFor clarity, several cancer categories have been merged. 'Non-leukemia lymphatic and blood cancers' includes Hodgkin disease, Non-Hodgkin lymphoma, multiple myeloma, and other lymphoid and blood cancers.\n'Head, neck, and oral cancers' includes oral, pharyngeal, and laryngeal cancers. 'Other/unspecified cancers' combines in situ, uncertain, benign, and other unspecified cancers."
  ) +
  theme_minimal() + 
  guides(fill = guide_legend(title.position = "top")) +
  theme(text = element_text(family = "Lato"),
        strip.text.x = element_text(size = 12, face = "bold"),
        axis.text = element_text(size = 10),
        axis.title = element_text(size = 12),
        legend.position = "right", # Place legend at the right
        legend.box = "vertical", # Arrange legend items horizontally
        plot.title = element_text(face = "bold", size = 16),
        panel.grid.major.y = element_blank(), # Remove y-axis major grid lines
        panel.grid.minor.y = element_blank(), # Remove y-axis minor grid lines 
        axis.text.y = element_text(margin = margin(r = -20)) # Move y-axis text closer to the axis
  )  
ggsave(paste0(data_folder, "cancer-number-deaths-by-age-usa.svg"), height=8, width=10)
