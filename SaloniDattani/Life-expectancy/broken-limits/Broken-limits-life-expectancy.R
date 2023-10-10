# Open libraries
library(tidyverse)

data_folder <- ""

le <- read_csv(paste0(data_folder, "female-and-male-life-expectancy-at-birth-in-years.csv"))

hmd_countries <- c("Australia", "Austria", "Belarus", "Belgium", "Canada", "Chile", "Croatia", "Czechia", "Denmark", "Estonia", "Finland", "France", "Germany", "Greece", "Hong Kong", "Hungary", "Iceland", "Ireland", "Israel", "Italy", "Japan", "Latvia", "Lithuania", "Luxembourg", "Netherlands", "New Zealand", "Norway", "Poland", "Portugal", "South Korea", "Russia", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland", "Taiwan", "United Kingdom", "United States", "Ukraine")

colnames(le) <- c("Entity", "Code", "Year", "LE_Male", "LE_Female")

le_record <- le %>%
              dplyr::select(-LE_Male) %>%
              filter(Entity %in% hmd_countries) %>%
              filter(Year > 1840) %>%
              group_by(Year) %>%
              dplyr::arrange(Year, LE_Female) %>%
              top_n(1)

write_csv(le_record, paste0(data_folder, "life-expectancy-record.csv"))

# Set country colours
country.colors <- c("Hong Kong" = "#00894b", 
                  "Iceland" = "#ec7333", 
                  "Japan" ="#be2856",
                  "Netherlands" = "#ffca30",
                  "Norway" = "#e43638",
                  "Sweden" = "#00a5cc")

predictions <- data.frame(Prediction_maker = c("UN", 
                                               "Frejka",
                                                  "Bourgeois-Pichat",
                                                  "Siegel",
                                                  "UN",
                                                  "Bourgeois-Pichat",
                                                  "World Bank", 
                                                  "UN",
                                                  "Coale & Guo",
                                                  "Coale",
                                                  "UN",
                                                  "Olshansky et al.",
                                                  "World Bank",
                                                  "UN"),
                             Prediction_limit = c(77.5,
                                                  77.5,
                                                  78.2,
                                                  79.4,
                                                  80,
                                                  80.3,
                                                  82.5,
                                                  82.5,
                                                  84.9,
                                                  84.2,
                                                  87.5,
                                                  88,
                                                  90,
                                                  92.5),
                            Prediction_year_made = c(1973,
                                                     1981,
                                                     1952,
                                                     1980,
                                                     1979,
                                                     1978,
                                                     1984,
                                                     1985,
                                                     1955,
                                                     1955,
                                                     1989,
                                                     2001,
                                                     1989,
                                                     1998))

# Make new column saying which year the prediction was broken
predictions$Year_Broken <- sapply(predictions$Prediction_limit, function(limit) {
  year_broken <- which(le_record$LE_Female > limit)[1]
  if (!is.na(year_broken)) {
    return(le_record$Year[year_broken])
  } else {
    return(NA)
  }
})

# Make new column saying what the LE record was on the year when the prediction was made
predictions$LE_Record_YearMade <- sapply(predictions$Prediction_year_made, function(year_made) {
  le_record <- le_record$LE_Female[le_record$Year == year_made]
  if (length(le_record) > 0) {
    return(le_record[1])
  } else {
    return(NA)
  }
})



# Plot
ggplot() +
  # Plot records
  geom_point(data=le_record, aes(x=Year, y=LE_Female, fill=Entity),
             shape=21, color="black", stroke=0.3) +
  # Plot prediction limit and year when prediction was made
  geom_point(data=predictions, aes(x=Prediction_year_made,y=Prediction_limit), shape=3, color="black", stroke=1) +
  theme_classic() +
  scale_fill_manual(values=country.colors) +
  coord_cartesian(xlim=c(1950,2025),ylim=c(70,95)) +
  labs(title = "Record female life expectancy", y="Life expectancy", fill="Country")

ggsave(paste0(data_folder, "record_female_life_expectancy_since_1950.svg"))

# When was LE_x exceeded?
le_record %>% 
  filter(LE_Female >= 88) %>%  #replace with life expectancy of interest
  arrange(Year) %>% 
  head(n=1)



