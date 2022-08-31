Updating the World Bank Income Groups Chart
================

We would like to update the historical World Bank income groupings
chart. First, we load the required dependencies.

``` r
#Dependencies
require(tidyverse) #For data wrangling
require(readxl) #For reading in Excel files
```

Then download the new data directly from the World Bank Databank
website.

``` r
download.file("http://databank.worldbank.org/data/download/site-content/OGHIST.xlsx",
"OGHIST.xlsx")
```

Read in and clean the new data.

``` r
groups_2021 <- read_excel("OGHIST.xlsx", 
                          sheet = "Country Analytical History", 
                          skip = 5) %>%
  dplyr::rename(ccode = "...1", #Country codes
                Entity = "Data for calendar year :")
```

    ## New names:
    ## * `` -> ...1

There will be spaces in this file to mark the start and end of the
current list of countries, as well as the start and end of the
historical country groupings. Finding the NA values will allow us to
subset the data at the correct point.

``` r
#Finding the rows that mark this
spaces <- which(is.na(groups_2021$ccode))

#We can view which rows have spaces (un-comment to view)
#as.data.frame(groups_2021)[spaces, ]

#Current country list
spaces_current_begin <- spaces[which(spaces<20)]
spaces_current_begin <- spaces_current_begin[length(spaces_current_begin)]
spaces_current_end <- spaces[which(spaces>20)][1]

#Separating out the current list of countries
groups_current <- groups_2021[(spaces_current_begin+1):(spaces_current_end-1),]

#Finding the historical country names and groupings
groups_hist <- groups_2021[spaces_current_end:length(groups_2021$ccode),] %>%
  filter(!is.na(ccode))
```

Cleaning the current and past country groupings.

``` r
#Cleaning the current country groupings data
groups_current_clean <- groups_current %>%
  mutate(ccode = NULL) %>% #Removing the country code column
  pivot_longer(cols = !Entity, #All other columns are named based on years
               names_to = "Year", 
               values_to = "group2021") %>%
  mutate(Year = as.numeric(Year), #Converting years from character to numeric
         group2021 = gsub("[/*]", "", group2021),
         group2021 = if_else(group2021 == "L", "Low income", #Renaming groups
                 if_else(group2021 == "LM", "Lower-middle income",
                  if_else(group2021 == "UM", "Upper-middle income",
                   if_else(group2021 == "H", "High income",
                  if_else(group2021 == "..", "Not categorized", 
                          NA_character_)))))) %>%
  dplyr::select(Entity, Year, group2021) #Selecting variables of interest
```

``` r
#Cleaning the historical country groupings data
groups_hist_clean <- groups_hist %>%
  mutate(ccode = NULL) %>% #Removing the country code column
  pivot_longer(cols = !Entity, #All other columns are named based on years
               names_to = "Year", 
               values_to = "group2021") %>%
  mutate(Year = as.numeric(Year), #Converting years from character to numeric
         group2021 = gsub("[/*]", "", group2021),
         group2021 = if_else(group2021 == "L", "Low income", #Renaming groups
                 if_else(group2021 == "LM", "Lower-middle income",
                  if_else(group2021 == "UM", "Upper-middle income",
                   if_else(group2021 == "H", "High income",
                  if_else(group2021 == "..", "Not categorized", 
                          NA_character_)))))) %>%
  #Selecting variables of interest
  dplyr::select(Entity_hist = Entity, Year, group2021) 
```

Now let’s create a table to map historical groupings onto current ones.

``` r
#View these historical groupings
groups_hist
```

    ## # A tibble: 6 x 37
    ##   ccode Entity `1987` `1988` `1989` `1990` `1991` `1992` `1993` `1994` `1995`
    ##   <chr> <chr>  <chr>  <chr>  <chr>  <chr>  <chr>  <chr>  <chr>  <chr>  <chr> 
    ## 1 CSK   Czech… ..     ..     ..     UM     UM     <NA>   <NA>   <NA>   <NA>  
    ## 2 MYT   Mayot… ..     ..     ..     H      UM     UM     UM     UM     UM    
    ## 3 ANT   Nethe… UM     UM     UM     UM     UM     UM     UM     H      H     
    ## 4 YUG   Serbi… ..     ..     ..     ..     ..     LM     LM     LM     LM    
    ## 5 SUN   USSR … ..     ..     ..     UM     <NA>   <NA>   <NA>   <NA>   <NA>  
    ## 6 YUGf  Yugos… UM     UM     UM     UM     UM     <NA>   <NA>   <NA>   <NA>  
    ## # … with 26 more variables: `1996` <chr>, `1997` <chr>, `1998` <chr>,
    ## #   `1999` <chr>, `2000` <chr>, `2001` <chr>, `2002` <chr>, `2003` <chr>,
    ## #   `2004` <chr>, `2005` <chr>, `2006` <chr>, `2007` <chr>, `2008` <chr>,
    ## #   `2009` <chr>, `2010` <chr>, `2011` <chr>, `2012` <chr>, `2013` <chr>,
    ## #   `2014` <chr>, `2015` <chr>, `2016` <chr>, `2017` <chr>, `2018` <chr>,
    ## #   `2019` <chr>, `2020` <chr>, `2021` <chr>

``` r
#CZECHOSLOVAKIA (former)
#https://en.wikipedia.org/wiki/Czechoslovakia
#Czechoslovakia became Czechia and Slovakia in 1992
#There is no data prior to 1990, but we can incorporate 1990-1991
cz_countries <- c("Czech Republic", "Slovak Republic")
cz_hist <- "Czechoslovakia (former)"

#MAYOTTE
#https://en.wikipedia.org/wiki/Mayotte
#An overseas département of France
#Given its own World Bank Income group up to 2011
#We do not include this in the data, as it would fall under France

#NETHERLANDS ANTILLES (former)
#https://en.wikipedia.org/wiki/Netherlands_Antilles
#Broke up into different states, including Sint Maarten and Curaçao
na_countries <- c("Curaçao", "Sint Maarten (Dutch part)")
na_hist <- "Netherlands Antilles (former)"

#SERBIA AND MONTENEGRO
#https://en.wikipedia.org/wiki/Serbia_and_Montenegro
sm_countries <- c("Serbia", "Montenegro")
sm_hist <- "Serbia and Montenegro (former)"

#USSR
#https://en.wikipedia.org/wiki/Republics_of_the_Soviet_Union
ussr_countries <- c("Armenia", "Azerbaijan", "Belarus", "Estonia", 
                    "Georgia", "Kazakhstan", "Kyrgyz Republic", 
                    "Latvia", "Lithuania", "Moldova", "Russian Federation",
                    "Tajikistan", 
                    "Turkmenistan", "Ukraine", "Uzbekistan")
ussr_hist <- "USSR (former)"

#YUGOSLAVIA (former)
#https://en.wikipedia.org/wiki/Yugoslavia#New_states
yg_countries <- c("Serbia", "Montenegro", "Croatia", "Slovenia", 
                  "North Macedonia", "Bosnia and Herzegovina")
yg_hist <- "Yugoslavia (former)"
```

``` r
#Construct a lookup table using these entries
lookup_table <- tibble(Entity = c(cz_countries, 
            na_countries, sm_countries, ussr_countries, yg_countries), 
                       Entity_hist = c(rep(cz_hist, length(cz_countries)), 
            rep(na_hist, length(na_countries)), 
            rep(sm_hist, length(sm_countries)), 
            rep(ussr_hist, length(ussr_countries)), 
            rep(yg_hist, length(yg_countries))))
```

``` r
#Filter the historical groupings data to non-NA values
hist_data <- groups_hist_clean %>%
  filter(!is.na(group2021), Entity_hist != "Mayotte", 
         group2021 != "Not categorized")
```

``` r
#Merge historical data with lookup table
hist_data <- merge(hist_data, lookup_table) %>%
  rename(group2021_extra = group2021)
```

``` r
#Join the historical data with the current groupings, then replace observations
full_data_2021 <- full_join(groups_current_clean, hist_data) %>%
  #Replacing new groupings with historical ones
  mutate(group2021 = if_else(group2021 == "Not categorized" & 
                               group2021_extra != "Not categorized", 
                             group2021_extra, group2021),
         #Venezuela is uncategorized
         group2021 = if_else(is.na(group2021), 
                             "Not categorized", group2021))%>%
  dplyr::select(-c(Entity_hist, group2021_extra))
```

    ## Joining, by = c("Entity", "Year")

``` r
#Write this data as a CSV
write_csv(full_data_2021 %>% 
            rename(`Income classifications (World Bank (2021))` = group2021,
                   Country = "Entity"), 
          "Income Classification - World Bank (2021).csv")
```

Let’s make sure this data matches what was previously included in the
OWID dataset. Reading in the previous OWID data downloaded from the
Github page:

``` r
groups_2017 <- read_csv("https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/Income%20Classification%20-%20World%20Bank%20(2017)/Income%20Classification%20-%20World%20Bank%20(2017).csv") %>%
    rename(group2017 = `Income classifications (World Bank (2017))`)
```

Now compare the two datasets. As we can see here, the only
non-overlapping entries are from countries whose entries have been
altered to reflect their historical designations.

``` r
#New dataset
#Previous OWID dataset
#Merging the two datasets
compare_both <- full_join(full_data_2021, groups_2017)
```

    ## Joining, by = c("Entity", "Year")

``` r
#Finding observations that don't match
compare_both %>% 
  filter(group2021 != group2017) %>%
  arrange(Entity, Year)
```

    ## # A tibble: 50 x 4
    ##    Entity                  Year group2021           group2017      
    ##    <chr>                  <dbl> <chr>               <chr>          
    ##  1 Bosnia and Herzegovina  1987 Upper-middle income Not categorized
    ##  2 Bosnia and Herzegovina  1988 Upper-middle income Not categorized
    ##  3 Bosnia and Herzegovina  1989 Upper-middle income Not categorized
    ##  4 Bosnia and Herzegovina  1990 Upper-middle income Not categorized
    ##  5 Bosnia and Herzegovina  1991 Upper-middle income Not categorized
    ##  6 Croatia                 1987 Upper-middle income Not categorized
    ##  7 Croatia                 1988 Upper-middle income Not categorized
    ##  8 Croatia                 1989 Upper-middle income Not categorized
    ##  9 Croatia                 1990 Upper-middle income Not categorized
    ## 10 Croatia                 1991 Upper-middle income Not categorized
    ## # … with 40 more rows

To confirm that the rest are just name mismatches addressed by the
Grapher, let’s read in the name-standardized data we get from the
Grapher and compare that against the 2017 data.

``` r
#Read in the standardized dataset
groups_2021_standardized <- read_csv("Income Classification - World Bank (2021)_country_standardized.csv") %>%
  rename(Entity = `Our World In Data Name`,
         group2021_final = `Income classifications (World Bank (2021))`)
```

``` r
compare_final <- full_join(groups_2017, groups_2021_standardized)
```

    ## Joining, by = c("Entity", "Year")

``` r
#Finding observations that don't match
compare_final %>% 
  filter(group2021_final != group2017) %>%
  arrange(Entity, Year)
```

    ## # A tibble: 73 x 5
    ##    Entity               Year group2017     Country            group2021_final   
    ##    <chr>               <dbl> <chr>         <chr>              <chr>             
    ##  1 Bosnia and Herzego…  1987 Not categori… Bosnia and Herzeg… Upper-middle inco…
    ##  2 Bosnia and Herzego…  1988 Not categori… Bosnia and Herzeg… Upper-middle inco…
    ##  3 Bosnia and Herzego…  1989 Not categori… Bosnia and Herzeg… Upper-middle inco…
    ##  4 Bosnia and Herzego…  1990 Not categori… Bosnia and Herzeg… Upper-middle inco…
    ##  5 Bosnia and Herzego…  1991 Not categori… Bosnia and Herzeg… Upper-middle inco…
    ##  6 Croatia              1987 Not categori… Croatia            Upper-middle inco…
    ##  7 Croatia              1988 Not categori… Croatia            Upper-middle inco…
    ##  8 Croatia              1989 Not categori… Croatia            Upper-middle inco…
    ##  9 Croatia              1990 Not categori… Croatia            Upper-middle inco…
    ## 10 Croatia              1991 Not categori… Croatia            Upper-middle inco…
    ## # … with 63 more rows

``` r
#The rest are countries that have been removed (Czechoslovakia, Mayotte, Netherlands Antilles) or renamed (Micronesia)
paste("Name not found in 2021 data:", paste(unique(compare_final %>% 
  filter(is.na(group2021_final)) %>%
  arrange(Entity) %>%
  pull(Entity)), collapse = ", "))
```

    ## [1] "Name not found in 2021 data: Czech Republic, Czechoslovakia, Macedonia, Mayotte, Micronesia, Netherlands Antilles, Swaziland"

``` r
paste("Name not found in 2017 data:", paste(unique(compare_final %>% 
  filter(is.na(group2017), Year < 2017) %>%
  arrange(Entity) %>%
  pull(Entity)), collapse = ", "))
```

    ## [1] "Name not found in 2017 data: Czechia, Eswatini, Micronesia (country), North Macedonia"

Now we can make the final edits to the dataset and save it in the format
we will want:

``` r
write_csv(read_csv("Income Classification - World Bank (2021)_country_standardized.csv") %>% 
        rename(Entity = `Our World In Data Name`) %>%
          dplyr::select(-c(Country)),
        "Income Classification - World Bank (2021).csv")
```

    ## Parsed with column specification:
    ## cols(
    ##   Country = col_character(),
    ##   `Our World In Data Name` = col_character(),
    ##   Year = col_double(),
    ##   `Income classifications (World Bank (2021))` = col_character()
    ## )
