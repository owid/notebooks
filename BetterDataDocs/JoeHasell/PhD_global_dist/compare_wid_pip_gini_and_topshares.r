# -*- coding: utf-8 -*-
library(tidyverse)

# Pull in WID-PIP data

df<- read.csv("https://joeh.fra1.digitaloceanspaces.com/phd_global_dist/wid_pip_gini_and_topshares.csv")


# ## Charts

# Calculate change in Gini 1990 – 2019

ineq_change<- df %>% filter(year %in% c(1990, 2019)) %>% 
                select(entity, year, wid_gini, gini, wid_top_10_share, shares_decile_10, wid_top_1_share, shares_top_1pc) %>%
                pivot_wider(names_from = year, values_from = c(wid_gini, gini, wid_top_10_share, shares_decile_10, wid_top_1_share, shares_top_1pc), names_sep = "_") %>%
                mutate(wid_gini_change = wid_gini_2019 - wid_gini_1990,
                       pip_gini_change = gini_2019 - gini_1990,
                       wid_top10share_change = wid_top_10_share_2019 - wid_top_10_share_1990,
                       pip_top10share_change = shares_decile_10_2019 - shares_decile_10_1990,
                       wid_top1share_change = wid_top_1_share_2019 - wid_top_1_share_1990,
                       pip_top1share_change = shares_top_1pc_2019 - shares_top_1pc_1990)


ggplot(ineq_change, aes(x = pip_gini_change, y = wid_gini_change)) +
       geom_point() +            
        geom_abline(intercept = 0,
              slope = 1)

# +
change_threshold = 0.01

ineq_change %>%
    select(entity, wid_gini_change, pip_gini_change) %>%
    drop_na() %>%
    summarize(n_entity = n(),
              n_fall_wid = sum(wid_gini_change < -change_threshold),
              n_fall_pip = sum(pip_gini_change < -change_threshold),
              n_rise_wid = sum(wid_gini_change > change_threshold),
              n_rise_pip = sum(pip_gini_change > change_threshold))
# -

ggplot(ineq_change, aes(x = pip_top10share_change, y = wid_top10share_change)) +
       geom_point() +            
        geom_abline(intercept = 0,
              slope = 1)

# +
change_threshold = 0.03

ineq_change %>%
    select(entity, wid_top10share_change, pip_top10share_change) %>%
    drop_na() %>%
    summarize(n_entity = n(),
              n_fall_wid = sum(wid_top10share_change < -change_threshold),
              n_fall_pip = sum(pip_top10share_change < -change_threshold),
              n_rise_wid = sum(wid_top10share_change > change_threshold),
              n_rise_pip = sum(pip_top10share_change > change_threshold))
# -

ggplot(ineq_change, aes(x = pip_top1share_change, y = wid_top1share_change)) +
       geom_point() +            
        geom_abline(intercept = 0,
              slope = 1)


