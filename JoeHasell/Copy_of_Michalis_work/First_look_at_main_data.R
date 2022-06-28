# ---
# title: "First look at the main data"
# author: "Joe Hasell"
# date: "25/04/2022"
# output: html_document
# ---
# +
# %
# + name="setup" tags=["remove_cell"]
knitr::opts_chunk$set(echo = TRUE)
library(tidyverse)
library(RCurl)
library(knitr)
# -

# %
# Pull in data from Michalis' folder in Github repo
df <- read.csv("https://raw.githubusercontent.com/owid/notebooks/main/MichalisMoatsos/MainDataCountriesOnlyNew.csv", row.names = 1, header = T, sep = ";", dec = ",")


# %
# This is a brand new comment
head(df)

# %

# +
# * Can you add a $1 a day poverty line please.
#
# * There are observations where the poverty share = -1.
#
# See rough summary of poverty shares
# +
summary(df[ , grep("share.of.population.below.poverty.line", colnames(df))] )  


# -
# %
# For instance:
kable(head(df %>%
  filter(X.20.per.day...share.of.population.below.poverty.line < 0) %>%
    select(Entity, Year, X.20.per.day...share.of.population.below.poverty.line)))

# %
# * Relative poverty = 0 in some observations

kable(head(df %>%
  filter(X.40..of.median.income...share.of.population.below.poverty.line ==0) %>%
    select(Entity, Year, X.40..of.median.income...share.of.population.below.poverty.line, Median, Median_estimated)))


# * Missing values:
#
# Count NA's by column and filter for count>0
kable(data.frame(colSums(is.na(df))) %>%
  filter(colSums.is.na.df.. > 0))

# + Why are there some missing values for a very small number of relative poverty lines?

# + Povcal for some reason witholds a bunch of variables for loads of observations (2266 observations in your data it looks like). I've never really understood why. Is this also an issue in PIP? If so then I think the solution should be: use the direct output where available but fill in the NAs with the estimated value produced by us. (Not just for Median, but for all variables).
#
