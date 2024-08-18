
library(tidyverse)

# Housing and non-housing cap share various series, facet ------

load("Manipulated data/H_and_nonH_cap_shares")

# specify if you want to see all data, or the selected data for average under 
  # baseline or alt spec ("all", "switch1995", "switch2000", "KLEMSplus", 
    # "OECDindustPlus", "OECDindustPlus2", "KLEMSplus_no_IRL_PRT", 
    # "OECDindustPlus_no_IRL_PRT", "OECDindustPlus2_no_IRL_PRT")
spec<- "all"

df<- H_and_nonH_cap_shares[[spec]]

# All 20 countries together -----

housing_and_non_housing_cap_small_multiple <- ggplot(df, 
                                         aes(x=year, y=value)) +
  geom_line(alpha = 0.8, aes(linetype = share, colour=series)) +
  ggtitle("Housing and non-housing capital share of total value added (at factor prices)") + 
  facet_wrap(~country, ncol=4) +
  theme(text = element_text(size=7),
        axis.title.x = element_blank(),
        axis.title.y = element_blank(),
        axis.text.x = element_text(angle=90,vjust=0.5),
        legend.title=element_blank()) +
  theme_light()

housing_and_non_housing_cap_small_multiple

# Split 18 countries into blocks, 6 countries in each block -----

# drop Ireland and Portugal
df <- df %>%
  filter(!country %in% c("Ireland", "Portugal"))

# unique(df$country)

# set order of legend
df$share <- factor(df$share, 
                               levels=c("non_housing_cap_share",
                                        "housing_cap_share"))
# Block 1 (6 countires)
block1<- df %>%
  filter(country <= "Finland")

block1_chart <- ggplot(block1, 
                                                     aes(x=year, y=value)) +
  geom_line(alpha = 0.8, aes(linetype = share, colour=series)) +
  ggtitle("Housing and non-housing capital share of total value added (at factor prices)") + 
  scale_linetype_manual(values=c("solid", "dashed")) +
  facet_wrap(~country, ncol=2) +
  theme(text = element_text(size=7),
        axis.title.x = element_blank(),
        axis.title.y = element_blank(),
        axis.text.x = element_text(angle=90,vjust=0.5),
        legend.title=element_blank()) +
  theme_light()

block1_chart

ggsave(
  "Output/Housing and non-housing cpaital share in 18 countries/Block 1.svg",
  plot = block1_chart)

# Block 2 (6 countires)
block2<- df %>%
  filter(country > "Finland" & country <= "Luxembourg")

block2_chart <- ggplot(block2, 
                       aes(x=year, y=value)) +
  geom_line(alpha = 0.8, aes(linetype = share, colour=series)) +
  ggtitle("Housing and non-housing capital share of total value added (at factor prices)") + 
  scale_linetype_manual(values=c("solid", "dashed")) +
  facet_wrap(~country, ncol=2) +
  theme(text = element_text(size=7),
        axis.title.x = element_blank(),
        axis.title.y = element_blank(),
        axis.text.x = element_text(angle=90,vjust=0.5),
        legend.title=element_blank()) +
  theme_light()

block2_chart

ggsave(
  "Output/Housing and non-housing cpaital share in 18 countries/Block 2.svg",
  plot = block2_chart)

# Block 3 (6 countires)
block3<- df %>%
  filter(country > "Luxembourg")

block3_chart <- ggplot(block3, 
                       aes(x=year, y=value)) +
  geom_line(alpha = 0.8, aes(linetype = share, colour=series)) +
  ggtitle("Housing and non-housing capital share of total value added (at factor prices)") + 
  scale_linetype_manual(values=c("solid", "dashed")) +
  facet_wrap(~country, ncol=2) +
  theme(text = element_text(size=7),
        axis.title.x = element_blank(),
        axis.title.y = element_blank(),
        axis.text.x = element_text(angle=90,vjust=0.5),
        legend.title=element_blank()) +
  theme_light()

block3_chart

ggsave(
  "Output/Housing and non-housing cpaital share in 18 countries/Block 3.svg",
  plot = block3_chart)

# AVERAGE HOUSING AND NON-HOUSING CAP SHARE ------

# load list of average series under different specs
load("Manipulated data/avg_H_and_nonH_cap_shares.Rda")

# Plot one series only -----
# specify if you want to see the average across all data, or the selected data 
  # under baseline or alt spec ("all", "switch1995", "switch2000", "KLEMSplus",
    # "OECDindustPlus", "KLEMSplus_no_IRL_PRT", "OECDindustPlus_no_IRL_PRT")
spec<- "switch1995"

df<- avg_H_and_nonH_cap_shares[[spec]]

avg_housing_and_non_housing_share<- ggplot(df, 
                           aes(x=year, y=value)) +
  geom_line(aes(colour=share, linetype =  weights)) +
  theme_light()

avg_housing_and_non_housing_share

# BASELINE: Plot KLEMS and OECD plus '2' series without IRL or PRT ----

  # The 'early' series is KLEMS plus OECD industry data for Denmark and Norway
  # The 'later' series is OECD industry plus:
        # - OECD sector data for US and Spain
        # - re-introducing KLEMS back in for Belgium, Canada and Japan
        #  (for Belgium the KLEMS data is only included up to the start of the 
          # OECD industry data)

# Grab the series
KLEMSplus_no_IRL_PRT<- avg_H_and_nonH_cap_shares[["KLEMSplus_no_IRL_PRT"]] %>%
  mutate(spec = "KLEMSplus_no_IRL_PRT")

OECDindustPlus2_no_IRL_PRT<- avg_H_and_nonH_cap_shares[["OECDindustPlus2_no_IRL_PRT"]] %>%
  mutate(spec = "OECDindustPlus2_no_IRL_PRT")

# append together
specs_together<- rbind(KLEMSplus_no_IRL_PRT, OECDindustPlus2_no_IRL_PRT)



# set order of series legend
specs_together$spec <- factor(specs_together$spec, 
                            levels=c("KLEMSplus_no_IRL_PRT",
                                      "OECDindustPlus2_no_IRL_PRT") )

specs_together$share <- factor(specs_together$share, 
                              levels=c("non_housing_cap_share",
                                       "housing_cap_share") )

# plot
compare_averages_across_specs<- ggplot(specs_together, 
                                           aes(x=year, y=value)) +
  geom_line(aes(colour=spec, linetype = share)) +
  ggtitle("Average housing and non-housing capital shares across 18 countries") + 
  scale_colour_discrete(labels = c( "Early series (mainly KLEMS industry data)",
                                    "Later series (mainly OECD industry data)")) +
  scale_linetype_discrete(labels = c("Non-housing capital share",
                                     "Housing capital share")) +
  facet_wrap(~weights, nrow=2) +
  theme_light() + 
  scale_y_continuous(labels = scales::percent_format(accuracy = 1))

compare_averages_across_specs


ggsave(
  "Output/Housing and non-housing cpaital share in 18 countries/baseline hosing vs non-housing average shares.svg",
  plot = compare_averages_across_specs)

# Compare with and without Ireland and Portugal -----


# Grab the series
KLEMSplus<- avg_H_and_nonH_cap_shares[["KLEMSplus"]] %>%
  mutate(spec = "KLEMSplus")

OECDindustPlus2<- avg_H_and_nonH_cap_shares[["OECDindustPlus2"]] %>%
  mutate(spec = "OECDindustPlus2")

KLEMSplus_no_IRL_PRT<- avg_H_and_nonH_cap_shares[["KLEMSplus_no_IRL_PRT"]] %>%
  mutate(spec = "KLEMSplus_no_IRL_PRT")

OECDindustPlus2_no_IRL_PRT<- avg_H_and_nonH_cap_shares[["OECDindustPlus2_no_IRL_PRT"]] %>%
  mutate(spec = "OECDindustPlus2_no_IRL_PRT")

# append together
specs_together<- rbind(KLEMSplus, OECDindustPlus2)
specs_together<- rbind(specs_together, OECDindustPlus2_no_IRL_PRT)
specs_together<- rbind(specs_together, KLEMSplus_no_IRL_PRT)

specs_together<- specs_together %>%
  filter(weights == "unweighted_average") %>%
  mutate(inc_IRL_and_PRT = "Including Ireland and Portugal") %>%
  mutate(inc_IRL_and_PRT = replace(inc_IRL_and_PRT,
                                   grepl("no_IRL_PRT", spec, fixed = TRUE),
                                    "Excluding Ireland and Portugal"))

specs_together$spec<- gsub("_no_IRL_PRT", "", specs_together$spec)


# plot
compare_averages_across_specs<- ggplot(specs_together, 
                                       aes(x=year, y=value)) +
  geom_line(aes(colour=spec, linetype = share)) +
  ggtitle("Unweighted average, including and excluding Ireland and Portugal") + 
  facet_wrap(~inc_IRL_and_PRT) +
  theme_light()

compare_averages_across_specs

# Average housing share -----

load("Manipulated data/average_housing_share.Rda")

avg_housing_share<- ggplot(average_housing_share, 
                           aes(x=year, y=value)) +
          geom_line(aes(colour=weights, linetype = link_type)) +
  theme_light()

avg_housing_share

# Non-housing cap shares ------

# load data
load("Manipulated data/non_housing_cap_shares.Rda")

# set order of series legend
non_housing_cap_shares$series <- factor(non_housing_cap_shares$series, 
                              levels=c("OECD_industry_non_housing_cap_shares",
                                       "KLEMS_industry_non_housing_cap_shares",
                                       "OECD_sector_non_housing_cap_shares") )

non_housing_cap_small_multiple <- ggplot(non_housing_cap_shares, 
                                          aes(x=year, y=value, colour=series)) +
  geom_line(alpha = 0.8)  + 
  scale_colour_discrete(labels = c( "Capital income less Real estate capital income (OECD)",
                                    "Capital income less Real estate capital income (KLEMS)",
                                    "Capital income less Gross operating surplus in Household sector")) +
  ggtitle("Non-housing capital share of total value added (at factor prices)") + 
  facet_wrap(~country, ncol=4) +
  theme(text = element_text(size=7),
        axis.title.x = element_blank(),
        axis.title.y = element_blank(),
        axis.text.x = element_text(angle=90,vjust=0.5),
        legend.title=element_blank()) +
  theme_light()

non_housing_cap_small_multiple



# OECD CHARTS ------
# Load aggregate share data

load("Manipulated data/OECD industry data - aggregate factor shares.Rda") 

# Non-housing capital share - two scenarios -----
two_scenarios_data<- aggregate_factor_shares %>%
  filter(transaction %in% c("non_housing_gross_CAP_1",
                            "non_housing_gross_CAP_2"))

two_scenarios_small_multiple <- ggplot(two_scenarios_data, 
                               aes(x=year, y=gross_share, colour=transaction)) +
  geom_line(alpha = 0.8)  + 
  ggtitle("Non-housing capital share - two methods for treating self-employment income") + 
  facet_wrap(~country, ncol=4) +
  theme(text = element_text(size=7),
        axis.title.x = element_blank(),
        axis.title.y = element_blank(),
        axis.text.x = element_text(angle=90,vjust=0.5),
        legend.title=element_blank()) 

two_scenarios_small_multiple


# gross share country small multiple -------
gross_plot_data<- aggregate_factor_shares %>%
  filter(transaction %in% c("non_housing_gross_CAP_1",
                            "housing_gross_CAP",
                            "CoSE_1",
                            "CoE"))


# set order of stack
gross_plot_data$transaction <- factor(gross_plot_data$transaction, 
                                levels=c("CoE",
                                         "CoSE_1",
                                         "housing_gross_CAP",
                                         "non_housing_gross_CAP_1") )


gross_small_multiple_breakdown <- ggplot(gross_plot_data, 
                           aes(x=year, y=gross_share, fill=transaction)) +
  geom_area(alpha=0.6 , size=0.3, colour="black")  + 
  scale_fill_discrete(labels = c( "Compensation of employees",
                                  "Imputed labour income of self-employed",
                                  "Housing capital income", 
                                  "Non-housing capital income")) +
  ggtitle("Decomposition of factor price value added (gross)") + 
  facet_wrap(~country, ncol=4) +
  theme(text = element_text(size=7),
        axis.title.x = element_blank(),
        axis.title.y = element_blank(),
        axis.text.x = element_text(angle=90,vjust=0.5),
        legend.title=element_blank()) 

gross_small_multiple_breakdown

# net share country small multiple -------

net_plot_data<- aggregate_factor_shares %>%
  filter(transaction %in% c("non_housing_net_CAP_1",
                            "housing_net_CAP",
                            "CoSE_1",
                            "CoE"))


# set order of stack
net_plot_data$transaction <- factor(net_plot_data$transaction, 
                                      levels=c("CoE",
                                               "CoSE_1",
                                               "housing_net_CAP",
                                               "non_housing_net_CAP_1") )


net_small_multiple_breakdown <- ggplot(net_plot_data, 
                              aes(x=year, y=net_share, fill=transaction)) +
  geom_area(alpha=0.6 , size=0.3, colour="black")  + 
  scale_fill_discrete(labels = c( "Compensation of employees",
                                  "Imputed labour income of self-employed",
                                  "Housing capital income", 
                                  "Non-housing capital income")) +
  ggtitle("Decomposition of factor price value added (net)") + 
  facet_wrap(~country, ncol=4) +
  theme(text = element_text(size=7),
        axis.title.x = element_blank(),
        axis.title.y = element_blank(),
        axis.text.x = element_text(angle=90,vjust=0.5),
        legend.title=element_blank()) 

net_small_multiple_breakdown

# KLEMS DATA ------

# Load aggregate share data

load("Manipulated data/KLEMS - aggregate factor shares.Rda") 

# Non-housing capital share - two scenarios -----
two_scenarios_data<- aggregate_factor_shares %>%
  filter(transaction %in% c("non_housing_gross_CAP_1",
                            "non_housing_gross_CAP_2"))

two_scenarios_small_multiple <- ggplot(two_scenarios_data, 
                                       aes(x=year, y=gross_share, colour=transaction)) +
  geom_line(alpha = 0.8)  + 
  ggtitle("Non-housing capital share - two methods for treating self-employment income") + 
  facet_wrap(~country, ncol=4) +
  theme(text = element_text(size=7),
        axis.title.x = element_blank(),
        axis.title.y = element_blank(),
        axis.text.x = element_text(angle=90,vjust=0.5),
        legend.title=element_blank()) 

two_scenarios_small_multiple

# HOUSING SHARE - THREE APPROACHES ------
  # This chart looks at the KLEMS industry data, alongside
  # three series from the OECD data: consumption, sector
  # and industry (i.e. same idea as KLEMS but for later years)



# small multiple of the three approaches (4 series) for each country

# set order of series legend
housing_share_three_approaches$series_name <- factor(housing_share_three_approaches$series_name, 
                                levels=c("KLEMS_RE_industry_CAP_share",
                                         "OECD_RE_industry_CAP_share",
                                         "OECD_consumption_share",
                                         "OECD_hh_GOS_share") )

three_approaches_small_multiple <- ggplot(housing_share_three_approaches, 
                                       aes(x=year, y=value, colour=series_name)) +
  geom_line(alpha = 0.8)  + 
  scale_colour_discrete(labels = c( "Real estate capital income (KLEMS)",
                                  "Real estate capital income (OECD)",
                                  "Household final consumption of rent", 
                                  "Gross operating surplus in Household sector")) +
  ggtitle("Housing share of total value added (at factor prices)") + 
  facet_wrap(~country, ncol=4) +
  theme(text = element_text(size=7),
        axis.title.x = element_blank(),
        axis.title.y = element_blank(),
        axis.text.x = element_text(angle=90,vjust=0.5),
        legend.title=element_blank()) +
  theme_light()

three_approaches_small_multiple

# HOUSING SHARE AND PREICES BY COUNTRY ------

load("Manipulated data/housing_shares_and_prices.Rda")

# gather housing share and price series to plot
housing_shares_and_prices<- housing_shares_and_prices %>%
  gather(series, value, -c(country, year))

# set order of series legend
housing_shares_and_prices$series <- factor(housing_shares_and_prices$series, 
                             levels=c("diff_log_housing_share",
                                       "diff_log_relative_rent_price"))


housing_share_price_small_multiple <- ggplot(housing_shares_and_prices, 
                                   aes(x=year, y=value, colour = series)) +
  geom_line(alpha = 0.8) +
  scale_colour_discrete(labels = c("Housing share",
                                    "Relative rent price")) +
  ggtitle("Evolution of housing shares and relative rent prices") + 
  facet_wrap(~country, ncol=4) +
  theme(text = element_text(size=7),
        axis.title.x = element_blank(),
        axis.title.y = element_blank(),
        axis.text.x = element_text(angle=90,vjust=0.5),
        legend.title=element_blank()) +
  theme_light()

housing_share_price_small_multiple

# AVERAGE HOUSING SHARE ------

load("Manipulated data/average_housing_share.Rda")

# gather the weighted and unweighted averages to plot together
average_housing_share<- average_housing_share %>%
  gather(series, average_housing_share, -year)


# set order of series legend
average_housing_share$series <- factor(average_housing_share$series, 
                                  levels=c("unweighted_average_housing_share",
                                           "weighted_average_housing_share"))

# plot
average_housing_share_plot<-  ggplot(average_housing_share, 
                                     aes(x=year, y=average_housing_share,
                                         colour = series)) +
  scale_colour_discrete(labels = c( "Unweighted",
                                    "Weighted (GDP at PPPs)")) +
  ggtitle("Average housing share across 20 countries") + 
  geom_line(alpha = 0.8) +
  theme_light()

average_housing_share_plot

# COMPARE GROSS CAP SHARES ACROSS THREE SERIES -----

load("Manipulated data/gross_cap_shares.Rda")


# set order of series legend
gross_cap_shares$series <- factor(gross_cap_shares$series, 
                                 levels=c("KLEMS_industry_gross_cap_share",
                                          "OECD_industry_gross_cap_share",
                                          "OECD_sector_gross_cap_share"))


cap_share_3_series_small_multiple <- ggplot(gross_cap_shares, 
                                      aes(x=year, y=value, colour = series)) +
  geom_line(alpha = 0.8) +
  scale_colour_discrete(labels = c("KLEMS industry data",
                                   "OECD industry data",
                                   "OECD institutional sector data")) +
  ggtitle("Gross capital share of value added (at factor cost)") + 
  facet_wrap(~country, ncol=4) +
  theme(text = element_text(size=7),
        axis.title.x = element_blank(),
        axis.title.y = element_blank(),
        axis.text.x = element_text(angle=90,vjust=0.5),
        legend.title=element_blank()) +
  theme_light()

cap_share_3_series_small_multiple


