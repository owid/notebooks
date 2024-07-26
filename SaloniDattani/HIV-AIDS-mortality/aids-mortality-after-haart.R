library(tidyverse)

file_path <- "" # Update

icd9_df <- read_tsv(paste0(file_path, "Compressed Mortality, 1979-1998.txt"))
icd10_df <- read_tsv(paste0(file_path, "Compressed Mortality, 1999-2016.txt"))

icd9_df$`Crude Rate` <- as.numeric(icd9_df$`Crude Rate`)
icd9_df$Population <- as.numeric(icd9_df$Population)

icd10_df$`Crude Rate` <- as.numeric(icd10_df$`Crude Rate`)
icd10_df$Population <- as.numeric(icd10_df$Population)

# Add the new column to each dataframe
icd9_df <- icd9_df %>%
  mutate(ICD_version = "ICD-9")

icd10_df <- icd10_df %>%
  mutate(ICD_version = "ICD-10")

# Use bind_rows to merge them
combined_df <- bind_rows(icd9_df, icd10_df)

filtered_df <- combined_df %>% 
  filter(`Age Group Code` %in% c("15-19", "20-24", "25-34", "35-44", "45-54", "55-64", "65-74", "75-84"))

# Specify the factor levels of ICD_version
filtered_df$ICD_version <- factor(filtered_df$ICD_version, levels = c("ICD-9", "ICD-10"))

ggplot(data=filtered_df, aes(x=Year, y=`Crude Rate`, color=`Age Group Code`)) +
  geom_line() +
  geom_vline(xintercept = 1995, linetype = "dashed", color = "red") +
  annotate("text", x = 1995, y = max(combined_df$`Crude Rate`, na.rm = TRUE), 
           label = "HAART introduced", vjust = -0.5, hjust = -0.1) +
  scale_x_continuous(breaks = seq(1985, 2015, by = 5)) +
  coord_cartesian(xlim = c(1986, 2016)) +
  theme_classic() +
  labs(title="HIV/AIDS death rates shrank after HAART was introduced", 
       subtitle="Crude HIV/AIDS death rate per 100,000 people", 
       y="",
       color="Age group",
       size="ICD version",
       caption="Source: NCHS, via Compressed Mortality File Archives") +
  theme(legend.position = "bottom",
        plot.title = element_text(face = "bold", size = 16))                           
                          
                          