# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.8
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# + [markdown] tags=[]
# # World Inequality Database
# -

# The [World Inequality Database (WID.world)](https://wid.world/wid-world/) aims to provide open and convenient access to the most extensive available database on the historical evolution of the world distribution of income and wealth, both within countries and between countries. The dataset addresses some of the main limitations household surveys produce in national statistics of this kind: under-coverage at the top of the distribution due to non-response (the richest tend to not answer this kind of surveys or omit their income) or measurement error (the richest underreport their income for convenience or not actually knowing an exact figure if all their activities are added). The problem is handled with the combination of fiscal and national accounts data along household surveys based on the work of the leading researchers in the area: Anthony B. Atkinson, Thomas Piketty, Emmanuel Saez, Facundo Alvaredo, Gabriel Zucman, and hundreds of others. The initiative is based in the Paris School of Economics (as the [World Inequality Lab](https://inequalitylab.world/)) and compiles the World Inequality Report, a yearly publication about how inequality has evolved until the last year.
#
# Besides income and wealth distribution data, the WID has recently added carbon emissions to generate carbon inequality indices. It also offers decomposed stats on national income. The data can be obtained from the website and by R and Stata commands.

# + [markdown] tags=[]
# ## Distributions considered in this analysis
# -

# Three income distributions are considered, coming in three different csv files:
# - **wid_pretax_992j_dist.csv** is the pretax income distribution `ptinc`, which includes social insurance benefits (and remove corresponding contributions), but exclude other forms of redistribution (income tax, social assistance benefits, etc.).
# - **wid_posttax_nat_992j_dist.csv** is the post-tax national income distribution `diinc`, which includes both in-kind and in-cash redistribution.
# - **wid_posttax_dis_992j_dist.csv** is the post-tax disposable income distribution `cainc`, which excludes in-kind transfers (because the distribution of in-kind transfers requires a lot of assumptions).
#
# These distributions are the main DINA (distributional national accounts) income variables available at WID. DINA income concepts are distributed income concepts that are consistent with national accounts aggregates. The precise definitions are outlined in the [DINA guidelines](https://wid.world/es/news-article/2020-distributional-national-accounts-guidelines-dina-4/) and country-specific papers. 
#
# All of these distributions are generated using equal-split adults (j) as the population unit, meaning that the unit is the individual, but that income or wealth is distributed equally among all household members. The age group is individuals over age 20 (992, adult population), which excludes children (with 0 income in most of the cases). Extrapolations and interpolations are excluded from these files, as WID discourages its use at the level of individual countries (see the `exclude` description at `help wid` in Stata). More information about the variables and definitions can be found on [WID's codes dictionary](https://wid.world/codes-dictionary/).
#
# The distributions analysed in this notebook come from commands given in the `wid` function in Stata. These commands are located in the `wid_distribution.do` file from this same folder. Opening the file and pressing the *Execute (do)* button will generate the most recent data from WID. Both `.csv` and `.dta` files are available for analysis.

# + [markdown] tags=[]
# ## Main variables

# +
import pandas as pd
import numpy as np
from pathlib import Path
import time
import seaborn as sns
import time

#keep_default_na and na_values are included because there is a country labeled NA, Namibia, which becomes null without the parameters

file = Path('wid_pretax_992j_dist.csv')
wid_pretax = pd.read_csv(file, keep_default_na=False,
                         na_values=['-1.#IND', '1.#QNAN', '1.#IND', '-1.#QNAN', '#N/A N/A', '#N/A', 'N/A', 'n/a', '', '#NA', 
                                    'NULL', 'null', 'NaN', '-NaN', 'nan', '-nan', ''])

file = Path('wid_posttax_nat_992j_dist.csv')
wid_posttax_nat = pd.read_csv(file, keep_default_na=False,
                              na_values=['-1.#IND', '1.#QNAN', '1.#IND', '-1.#QNAN', '#N/A N/A', '#N/A', 'N/A', 'n/a', '', '#NA',
                                         'NULL', 'null', 'NaN', '-NaN', 'nan', '-nan', ''])

file = Path('wid_posttax_dis_992j_dist.csv')
wid_posttax_dis = pd.read_csv(file, keep_default_na=False,
                              na_values=['-1.#IND', '1.#QNAN', '1.#IND', '-1.#QNAN', '#N/A N/A', '#N/A', 'N/A', 'n/a', '', '#NA', 
                                         'NULL', 'null', 'NaN', '-NaN', 'nan', '-nan', ''])

#The variable 'country_year' is created, to identify unique distributions:
wid_pretax['country_year'] = wid_pretax['country'] + wid_pretax['year'].astype(str)
wid_posttax_nat['country_year'] = wid_posttax_nat['country'] + wid_posttax_nat['year'].astype(str)
wid_posttax_dis['country_year'] = wid_posttax_dis['country'] + wid_posttax_dis['year'].astype(str)
# -

# The key variables that come following transformations in Stata are:
# - **country** mostly follows the ISO 3166-1 alpha-2 standard, but also includes world regions, country subregions (rural and urban China, for example), former countries and countries not officially included in the standard. All the countries available are extracted. See https://wid.world/codes-dictionary/#country-code
# - **year** is the year of the distribution. All available years are extracted.
# - **percentile** is the percentile (or, more broadly, quantile) of the distribution. They are in the format *pXpY*, where X and Y are both numbers between 0 and 100. X correspond to the percentile for the lower bound of the group, and Y to the percentile for the upper bound (hence X < Y). 130 different quantiles are extracted, from p0p1 to p99p100, tenths of a percentile in the top 1% (p99p99.1, p99.1p99.2, p99.2p99.3, …, p99.8p99.9, p99.9p100), hundreds of a percentile in the top 0.1% (p99.9p99.91, p99.92p99.93, …, p99.98p99.99, p99.99p100), and thousands of a percentile in the top 0.01% (p99.99p99.991, p99.992p99.993, … , p99.998p99.999, p99.999p100). See https://wid.world/codes-dictionary/#percentile-code 
# - **p** represent the same variable *percentile*, but presented in a more simple way to sort the dataset: the lower bound X is extracted from *pXpY* and divided by 100 to get only numbers from 0 to 1.
# - **threshold** is the minimum level of income that gets you into a group. For example, the income threshold of the group p90p100 is the income of the poorest individuals in the top 10%. By definition, it is equal to the income threshold of the groups p90p99 or p90p91.
# - **average** is the average income of the people in the group. For example, the wealth average of the group p90p99 is the average income of the top 10% excluding the top 1%.
# - **share** is the income of the group, divided by the total for the whole population. For example, the income of the group p99p100 is the top 1% income share.
#
# Threshold and average data is converted to 2017 USD PPP with the `xlcusp` command in Stata (see https://wid.world/codes-dictionary/#exchange-rate). The variables **age** and **pop** (age group and population unit, respectively) are also in the dataset, but mainly for internal reference as it is the same value for each observation (992 and j). Although there are more age groups and population units available to query, most of them do not return results as massive as with the 992 and j combination or they just do not return data (see the options [here](https://wid.world/codes-dictionary/#three-digit-code) and [here](https://wid.world/codes-dictionary/#one-letter-code)).

# Basic descriptive statistics are presented for the three distributions:

wid_pretax.describe(include='all')

# With 731,157 observations, the pretax income distribution file is with difference the largest out of the three. It also contains 224 different countries/regions, almost 5 times the number of the post-tax files. This makes up for a total of 6451 different distributions (different country-years available). Although there is data starting from the year 1870, the data is concentrated mostly in the last three decades (the median of the *year* variable is 2001). 

wid_posttax_nat.describe(include='all')

# The post-tax national income distribution file contains 191,034 observations for only 48 countries, which make 1533 different distributions. The minimum year is 1900, although the distributions are again concentrated more recently (median 2001).

wid_posttax_dis.describe(include='all')

# The post-tax disposable income file is the one with less observations (177,552) for 48 countries making 1533 different distributions again. The minimum year is 1900 (median 2002).

# ## Sanity checks for the income distributions

# The distributions are explored more in detail to find and correct (if possible) errors in the original data. 

# ### The same quantiles available for each country-year

# It is very important that the distribution contains all 130 quantiles requested by the original query in Stata, to be able to estimate inequality statistics properly.
# One way to see if this holds is by counting the different occurrences of *percentile* for each distribution. The dataframes are grouped by country and year for this purpose.

# #### Pretax income

pretax_count = wid_pretax.groupby(['country', 'year', 'country_year']).nunique()
pretax_not130 = pretax_count[pretax_count['percentile']!=130].reset_index()
pretax_not130

# In the case of the pretax data there are 851 different distributions that do not have the 130 quantiles. The main stats of this group are in the following table.

pretax_not130.describe(include='all')

# 21 different countries are in this situation, with a range of years from 1870 to 1979 (median 1944). The amount of percentiles in this group range from 1 to 31 (median 3). The 21 countries are:

pretax_not130.country.value_counts(dropna=False)

# The list of country-years without 130 quantiles can be extracted and filtered to the original dataset to see which are the few quantiles presented.

# +
pretax_not130_list = list(pretax_not130.country_year.unique())
wid_pretax_not130 = wid_pretax[wid_pretax['country_year'].isin(pretax_not130_list)].reset_index(drop=True)
wid_pretax_clean = wid_pretax[~wid_pretax['country_year'].isin(pretax_not130_list)].reset_index(drop=True)

wid_pretax_not130.percentile.value_counts(dropna=False)
# -

# **All of them come from the top 1%**, the last percentile or one of its subdivisions.

# And filtering out the exceptions, now all the percentiles are represented uniformly in 5603 distributions:

wid_pretax_clean.percentile.value_counts(dropna=False)

# #### Post-tax national income

# For the post-tax national income distribution there are less cases:

posttax_nat_count = wid_posttax_nat.groupby(['country', 'year', 'country_year']).nunique()
posttax_nat_not130 = posttax_nat_count[posttax_nat_count['percentile']!=130].reset_index()
posttax_nat_not130

# 64 different distributions do not have 130 percentiles.

posttax_nat_not130.describe(include='all')

# Only one country is in this situation (France), with a range of years from 1900 to 1978 (median 1944). There is always 1 percentile for each of these distributions.
#
# All of these 64 percentiles are **p99p100, the top 1%**:

# +
posttax_nat_not130_list = list(posttax_nat_not130.country_year.unique())
wid_posttax_nat_not130 = wid_posttax_nat[wid_posttax_nat['country_year'].isin(posttax_nat_not130_list)].reset_index(drop=True)
wid_posttax_nat_clean = wid_posttax_nat[~wid_posttax_nat['country_year'].isin(posttax_nat_not130_list)].reset_index(drop=True)

wid_posttax_nat_not130.percentile.value_counts(dropna=False)

# + [markdown] tags=[]
# And filtering out the exceptions, now all the percentiles are represented uniformly in 1469 distributions:
# -

wid_posttax_nat_clean.percentile.value_counts(dropna=False)

# #### Post-tax disposable income

# There are more post-tax disposable income distributions that follow this category:

posttax_dis_count = wid_posttax_dis.groupby(['country', 'year', 'country_year']).nunique()
posttax_dis_not130 = posttax_dis_count[posttax_dis_count['percentile']!=130].reset_index()
posttax_dis_not130

# In the case of the post-tax disposable data there are 170 different distributions that do not have the 130 quantiles. The main stats of this group are in the following table.

posttax_dis_not130.describe(include='all')

# Only two countries are in this situation (France, US), with a range of years from 1900 to 2018 (median 1955). The amount of different percentiles for these groups range between 1 and 3. The cases are distributed as this table shows:

posttax_dis_not130.country.value_counts(dropna=False)

# In this case the percentiles are the **top 1%, 0.1% and 0.01%:**

# +
posttax_dis_not130_list = list(posttax_dis_not130.country_year.unique())
wid_posttax_dis_not130 = wid_posttax_dis[wid_posttax_dis['country_year'].isin(posttax_dis_not130_list)].reset_index(drop=True)
wid_posttax_dis_clean = wid_posttax_dis[~wid_posttax_dis['country_year'].isin(posttax_dis_not130_list)].reset_index(drop=True)

wid_posttax_dis_not130.percentile.value_counts(dropna=False)

# + [markdown] tags=[]
# And filtering out the exceptions, now all the percentiles are represented uniformly in 1363 distributions:
# -

wid_posttax_dis_clean.percentile.value_counts(dropna=False)

# ### Monotonicity

# When ordered by **p**, the threshold and average values for each country-year should not decrease. These can increase or stay the same, but never decrease. If this happens the construction of the distribution failed.

# #### Pretax income distribution

# +
excl_list = ['p99p100', 'p99.9p100', 'p99.99p100']

wid_pretax_monotonicity = wid_pretax_clean[~wid_pretax_clean['percentile'].isin(excl_list)].reset_index(drop=True)

distribution_list = list(wid_pretax_monotonicity['country_year'].unique())
percentile_list = sorted(list(wid_pretax_monotonicity['p'].unique()))
# -

# In the following code code the monotonicity is checked for the variables **average** and **threshold**.

# + tags=[]
#The average and threshold values are lagged by one row in the lagged_average and lagged_threshold variables for them to be compared

wid_pretax_monotonicity['lagged_average'] =  wid_pretax_monotonicity['average'].shift(1)
wid_pretax_monotonicity['monotonicity_check_avg'] =  wid_pretax_monotonicity['average'] >= wid_pretax_monotonicity['lagged_average']
wid_pretax_monotonicity.loc[(wid_pretax_monotonicity['percentile'] == 'p0p1'), 'monotonicity_check_avg'] = True
wid_pretax_monotonicity.loc[(wid_pretax_monotonicity['average'].isnull()) | (wid_pretax_monotonicity['lagged_average'].isnull()), 'monotonicity_check_avg'] = np.nan

wid_pretax_monotonicity['lagged_threshold'] =  wid_pretax_monotonicity['threshold'].shift(1)
wid_pretax_monotonicity['monotonicity_check_thr'] =  wid_pretax_monotonicity['threshold'] >= wid_pretax_monotonicity['lagged_threshold']
wid_pretax_monotonicity.loc[(wid_pretax_monotonicity['percentile'] == 'p0p1'), 'monotonicity_check_thr'] = True
wid_pretax_monotonicity.loc[(wid_pretax_monotonicity['threshold'].isnull()) | (wid_pretax_monotonicity['lagged_threshold'].isnull()), 'monotonicity_check_thr'] = np.nan
# -

# **99.85%** of the values for average and **99.64%** of the values for threshold **pass the test**:

wid_pretax_monotonicity.monotonicity_check_avg.value_counts(normalize=True)

wid_pretax_monotonicity.monotonicity_check_thr.value_counts(normalize=True)

# These are the countries showing discontinuities in some of their distributions:

pretax_avgfalse = wid_pretax_monotonicity[wid_pretax_monotonicity['monotonicity_check_avg']==False].reset_index(drop=True)
pretax_avgfalse.country.value_counts(dropna=False)

pretax_thrfalse = wid_pretax_monotonicity[wid_pretax_monotonicity['monotonicity_check_thr']==False].reset_index(drop=True)
pretax_thrfalse.country.value_counts(dropna=False)

# The discontinuities are more concentrated in the subdivisions of the top 1% for the average and is more mixed for threshold:

pretax_avgfalse.percentile.value_counts(dropna=False)

#pd.set_option("display.max_rows", None)
pretax_thrfalse.percentile.value_counts(dropna=False)

# #### Post-tax national income distribution

# +
excl_list = ['p99p100', 'p99.9p100', 'p99.99p100']

wid_posttax_nat_monotonicity = wid_posttax_nat_clean[~wid_posttax_nat_clean['percentile'].isin(excl_list)].reset_index(drop=True)

distribution_list = list(wid_posttax_nat_monotonicity['country_year'].unique())
percentile_list = sorted(list(wid_posttax_nat_monotonicity['p'].unique()))

# + tags=[]
#The average and threshold values are lagged by one row in the lagged_average and lagged_threshold variables for them to be compared

wid_posttax_nat_monotonicity['lagged_average'] =  wid_posttax_nat_monotonicity['average'].shift(1)
wid_posttax_nat_monotonicity['monotonicity_check_avg'] =  wid_posttax_nat_monotonicity['average'] >= wid_posttax_nat_monotonicity['lagged_average']
wid_posttax_nat_monotonicity.loc[(wid_posttax_nat_monotonicity['percentile'] == 'p0p1'), 'monotonicity_check_avg'] = True
wid_posttax_nat_monotonicity.loc[(wid_posttax_nat_monotonicity['average'].isnull()) | (wid_posttax_nat_monotonicity['lagged_average'].isnull()), 'monotonicity_check_avg'] = np.nan

wid_posttax_nat_monotonicity['lagged_threshold'] =  wid_posttax_nat_monotonicity['threshold'].shift(1)
wid_posttax_nat_monotonicity['monotonicity_check_thr'] =  wid_posttax_nat_monotonicity['threshold'] >= wid_posttax_nat_monotonicity['lagged_threshold']
wid_posttax_nat_monotonicity.loc[(wid_posttax_nat_monotonicity['percentile'] == 'p0p1'), 'monotonicity_check_thr'] = True
wid_posttax_nat_monotonicity.loc[(wid_posttax_nat_monotonicity['threshold'].isnull()) | (wid_posttax_nat_monotonicity['lagged_threshold'].isnull()), 'monotonicity_check_thr'] = np.nan
# -

# **99.995%** of the values for average and **100%** of the values of threshold **pass the test**:

wid_posttax_nat_monotonicity.monotonicity_check_avg.value_counts(normalize=True)

wid_posttax_nat_monotonicity.monotonicity_check_thr.value_counts(normalize=True)

posttax_nat_avgfalse = wid_posttax_nat_monotonicity[wid_posttax_nat_monotonicity['monotonicity_check_avg']==False].reset_index(drop=True)
posttax_nat_avgfalse.country.value_counts(dropna=False)

posttax_nat_thrfalse = wid_posttax_nat_monotonicity[wid_posttax_nat_monotonicity['monotonicity_check_thr']==False].reset_index(drop=True)
posttax_nat_thrfalse.country.value_counts(dropna=False)

posttax_nat_avgfalse.percentile.value_counts(dropna=False)

posttax_nat_thrfalse.percentile.value_counts(dropna=False)

# #### Post-tax disposable income distribution

# +
excl_list = ['p99p100', 'p99.9p100', 'p99.99p100']

wid_posttax_dis_monotonicity = wid_posttax_dis_clean[~wid_posttax_dis_clean['percentile'].isin(excl_list)].reset_index(drop=True)

distribution_list = list(wid_posttax_dis_monotonicity['country_year'].unique())
percentile_list = sorted(list(wid_posttax_dis_monotonicity['p'].unique()))

# + tags=[]
#The average and threshold values are lagged by one row in the lagged_average and lagged_threshold variables for them to be compared

wid_posttax_dis_monotonicity['lagged_average'] =  wid_posttax_dis_monotonicity['average'].shift(1)
wid_posttax_dis_monotonicity['monotonicity_check_avg'] =  wid_posttax_dis_monotonicity['average'] >= wid_posttax_dis_monotonicity['lagged_average']
wid_posttax_dis_monotonicity.loc[(wid_posttax_dis_monotonicity['percentile'] == 'p0p1'), 'monotonicity_check_avg'] = True
wid_posttax_dis_monotonicity.loc[(wid_posttax_dis_monotonicity['average'].isnull()) | (wid_posttax_dis_monotonicity['lagged_average'].isnull()), 'monotonicity_check_avg'] = np.nan

wid_posttax_dis_monotonicity['lagged_threshold'] =  wid_posttax_dis_monotonicity['threshold'].shift(1)
wid_posttax_dis_monotonicity['monotonicity_check_thr'] =  wid_posttax_dis_monotonicity['threshold'] >= wid_posttax_dis_monotonicity['lagged_threshold']
wid_posttax_dis_monotonicity.loc[(wid_posttax_dis_monotonicity['percentile'] == 'p0p1'), 'monotonicity_check_thr'] = True
wid_posttax_dis_monotonicity.loc[(wid_posttax_dis_monotonicity['threshold'].isnull()) | (wid_posttax_dis_monotonicity['lagged_threshold'].isnull()), 'monotonicity_check_thr'] = np.nan
# -

# **100%** of the values for average and threshold **pass the test**:

wid_posttax_dis_monotonicity.monotonicity_check_avg.value_counts(normalize=True)

wid_posttax_dis_monotonicity.monotonicity_check_thr.value_counts(normalize=True)

posttax_dis_avgfalse = wid_posttax_dis_monotonicity[wid_posttax_dis_monotonicity['monotonicity_check_avg']==False].reset_index(drop=True)
posttax_dis_avgfalse.country.value_counts(dropna=False)

posttax_dis_thrfalse = wid_posttax_dis_monotonicity[wid_posttax_dis_monotonicity['monotonicity_check_thr']==False].reset_index(drop=True)
posttax_dis_thrfalse.country.value_counts(dropna=False)

posttax_dis_avgfalse.percentile.value_counts(dropna=False)

posttax_dis_thrfalse.percentile.value_counts(dropna=False)

# This is important to check the robustness of the **threshold** and **average** data across the years, to see a logical evolution of these numbers and not sudden jumps which might due to errors in the construction or due to the quality of the microdata.

# ### Negative values

# Negative income values, although common in the construction of distributions, usually are bottom coded to 0. In this section, negative values for average and threshold are checked.
#
# As expected, negative values occurr only in the first percentiles of the distribution (max p6p7 in post-tax disposable income). All this values are bottom coded to 0 in the *_positive* dataframes

# #### Pretax income

# +
pretax_negative_avg = wid_pretax_clean[wid_pretax_clean['average'] < 0].reset_index(drop=True)
pretax_negative_thr = wid_pretax_clean[wid_pretax_clean['threshold'] < 0].reset_index(drop=True)

pretax_positive = wid_pretax_clean.copy()
pretax_positive.loc[(pretax_positive['average'] < 0), 'average'] = 0
pretax_positive.loc[(pretax_positive['threshold'] < 0), 'threshold'] = 0
# -

pretax_negative_thr.percentile.value_counts(dropna=False)

pretax_negative_thr.country.value_counts(dropna=False)

pretax_negative_thr.percentile.value_counts(dropna=False)

pretax_negative_thr.country.value_counts(dropna=False)

# #### Post-tax national income

# +
posttax_nat_negative_avg = wid_posttax_nat_clean[wid_posttax_nat_clean['average'] < 0].reset_index(drop=True)
posttax_nat_negative_thr = wid_posttax_nat_clean[wid_posttax_nat_clean['threshold'] < 0].reset_index(drop=True)

posttax_nat_positive = wid_posttax_nat_clean.copy()
posttax_nat_positive.loc[(posttax_nat_positive['average'] < 0), 'average'] = 0
posttax_nat_positive.loc[(posttax_nat_positive['threshold'] < 0), 'threshold'] = 0
# -

posttax_nat_negative_thr.percentile.value_counts(dropna=False)

posttax_nat_negative_thr.country.value_counts(dropna=False)

posttax_nat_negative_thr.percentile.value_counts(dropna=False)

posttax_nat_negative_thr.country.value_counts(dropna=False)

# #### Post-tax disposable income

# +
posttax_dis_negative_avg = wid_posttax_dis_clean[wid_posttax_dis_clean['average'] < 0].reset_index(drop=True)
posttax_dis_negative_thr = wid_posttax_dis_clean[wid_posttax_dis_clean['threshold'] < 0].reset_index(drop=True)

posttax_dis_positive = wid_posttax_dis_clean.copy()
posttax_dis_positive.loc[(posttax_dis_positive['average'] < 0), 'average'] = 0
posttax_dis_positive.loc[(posttax_dis_positive['threshold'] < 0), 'threshold'] = 0
# -

posttax_dis_negative_thr.percentile.value_counts(dropna=False)

posttax_dis_negative_thr.country.value_counts(dropna=False)

posttax_dis_negative_thr.percentile.value_counts(dropna=False)

posttax_dis_negative_thr.country.value_counts(dropna=False)

# ### Total sum of shares equalling 1

# The shares are all part of a total which have to sum 1 (if the percentile brackets represent the entire population analysed). Four different checks can be done here, playing with the tenths, hundreds and thousands of percentile at the 1%:
# - The share of the percentiles p0p1 to p99p100 should sum 1.
# - The share of the percentiles p0p1 to p98p99 and p99p99.1 to p99.9p100 should sum 1.
# - The share of the percentiles p0p1 to p98p99.9 and p99.9p99.91 to p99.99p100 should sum 1.
# - The share of the percentiles p0p1 to p98p99.99 and p99.99p99.991 to p99.999p100 should sum 1.
#
# Consequentially, four different lists of percentiles are generated to apply them to the "clean" datasets:

# +
file = Path('Percentile names.xlsx')
percentiles = pd.read_excel(file, sheet_name='percentiles')
percentiles_list = percentiles['pXpY'].to_list()

tenths = pd.read_excel(file, sheet_name='tenths')
tenths_list = tenths['pXpY'].to_list()

hundreds = pd.read_excel(file, sheet_name='hundreds')
hundreds_list = hundreds['pXpY'].to_list()

thousands = pd.read_excel(file, sheet_name='thousands')
thousands_list = thousands['pXpY'].to_list()
# -

# The three following tables show the descriptive statistics for these four different checks. Overall, in the pretax and both post-tax distributions the median sum of the shares is always 1, the minimum value is 0.998600 and the maximum value is 1.001200. This means **the most "extreme" values only differ in 0.1% or 0.2% to 1, which should not be a concern.**

# +
wid_pretax_percentiles = wid_pretax_clean[wid_pretax_clean['percentile'].isin(percentiles_list)].reset_index(drop=True)
wid_pretax_tenths = wid_pretax_clean[wid_pretax_clean['percentile'].isin(tenths_list)].reset_index(drop=True)
wid_pretax_hundreds = wid_pretax_clean[wid_pretax_clean['percentile'].isin(hundreds_list)].reset_index(drop=True)
wid_pretax_thousands = wid_pretax_clean[wid_pretax_clean['percentile'].isin(thousands_list)].reset_index(drop=True)


wid_pretax_percentiles_shares = wid_pretax_percentiles.groupby(['country', 'year', 'country_year']).sum().reset_index()
wid_pretax_percentiles_shares.rename(columns={"share": "share_percentiles"}, inplace=True)

wid_pretax_tenths_shares = wid_pretax_tenths.groupby(['country', 'year', 'country_year']).sum().reset_index()
wid_pretax_tenths_shares.rename(columns={"share": "share_tenths"}, inplace=True)

wid_pretax_hundreds_shares = wid_pretax_hundreds.groupby(['country', 'year', 'country_year']).sum().reset_index()
wid_pretax_hundreds_shares.rename(columns={"share": "share_hundreds"}, inplace=True)

wid_pretax_thousands_shares = wid_pretax_thousands.groupby(['country', 'year', 'country_year']).sum().reset_index()
wid_pretax_thousands_shares.rename(columns={"share": "share_thousands"}, inplace=True)


pretax_shares_check = pd.merge(wid_pretax_percentiles_shares, wid_pretax_tenths_shares[['country_year', 'share_tenths']], on='country_year', validate='one_to_one')
pretax_shares_check = pd.merge(pretax_shares_check, wid_pretax_hundreds_shares[['country_year', 'share_hundreds']], on='country_year', validate='one_to_one')
pretax_shares_check = pd.merge(pretax_shares_check, wid_pretax_thousands_shares[['country_year', 'share_thousands']], on='country_year', validate='one_to_one')


pretax_shares_check = pretax_shares_check[['country', 'year', 'country_year', 'share_percentiles', 'share_tenths', 'share_hundreds', 'share_thousands']]

pretax_shares_check.describe()

# +
wid_posttax_nat_percentiles = wid_posttax_nat_clean[wid_posttax_nat_clean['percentile'].isin(percentiles_list)].reset_index(drop=True)
wid_posttax_nat_tenths = wid_posttax_nat_clean[wid_posttax_nat_clean['percentile'].isin(tenths_list)].reset_index(drop=True)
wid_posttax_nat_hundreds = wid_posttax_nat_clean[wid_posttax_nat_clean['percentile'].isin(hundreds_list)].reset_index(drop=True)
wid_posttax_nat_thousands = wid_posttax_nat_clean[wid_posttax_nat_clean['percentile'].isin(thousands_list)].reset_index(drop=True)



wid_posttax_nat_percentiles_shares = wid_posttax_nat_percentiles.groupby(['country', 'year', 'country_year']).sum().reset_index()
wid_posttax_nat_percentiles_shares.rename(columns={"share": "share_percentiles"}, inplace=True)

wid_posttax_nat_tenths_shares = wid_posttax_nat_tenths.groupby(['country', 'year', 'country_year']).sum().reset_index()
wid_posttax_nat_tenths_shares.rename(columns={"share": "share_tenths"}, inplace=True)

wid_posttax_nat_hundreds_shares = wid_posttax_nat_hundreds.groupby(['country', 'year', 'country_year']).sum().reset_index()
wid_posttax_nat_hundreds_shares.rename(columns={"share": "share_hundreds"}, inplace=True)

wid_posttax_nat_thousands_shares = wid_posttax_nat_thousands.groupby(['country', 'year', 'country_year']).sum().reset_index()
wid_posttax_nat_thousands_shares.rename(columns={"share": "share_thousands"}, inplace=True)


posttax_nat_shares_check = pd.merge(wid_posttax_nat_percentiles_shares, wid_posttax_nat_tenths_shares[['country_year', 'share_tenths']], on='country_year', validate='one_to_one')
posttax_nat_shares_check = pd.merge(posttax_nat_shares_check, wid_posttax_nat_hundreds_shares[['country_year', 'share_hundreds']], on='country_year', validate='one_to_one')
posttax_nat_shares_check = pd.merge(posttax_nat_shares_check, wid_posttax_nat_thousands_shares[['country_year', 'share_thousands']], on='country_year', validate='one_to_one')



posttax_nat_shares_check = posttax_nat_shares_check[['country', 'year', 'country_year', 'share_percentiles', 'share_tenths', 'share_hundreds', 'share_thousands']]

posttax_nat_shares_check.describe()

# +
wid_posttax_dis_percentiles = wid_posttax_dis_clean[wid_posttax_dis_clean['percentile'].isin(percentiles_list)].reset_index(drop=True)
wid_posttax_dis_tenths = wid_posttax_dis_clean[wid_posttax_dis_clean['percentile'].isin(tenths_list)].reset_index(drop=True)
wid_posttax_dis_hundreds = wid_posttax_dis_clean[wid_posttax_dis_clean['percentile'].isin(hundreds_list)].reset_index(drop=True)
wid_posttax_dis_thousands = wid_posttax_dis_clean[wid_posttax_dis_clean['percentile'].isin(thousands_list)].reset_index(drop=True)



wid_posttax_dis_percentiles_shares = wid_posttax_dis_percentiles.groupby(['country', 'year', 'country_year']).sum().reset_index()
wid_posttax_dis_percentiles_shares.rename(columns={"share": "share_percentiles"}, inplace=True)

wid_posttax_dis_tenths_shares = wid_posttax_dis_tenths.groupby(['country', 'year', 'country_year']).sum().reset_index()
wid_posttax_dis_tenths_shares.rename(columns={"share": "share_tenths"}, inplace=True)

wid_posttax_dis_hundreds_shares = wid_posttax_dis_hundreds.groupby(['country', 'year', 'country_year']).sum().reset_index()
wid_posttax_dis_hundreds_shares.rename(columns={"share": "share_hundreds"}, inplace=True)

wid_posttax_dis_thousands_shares = wid_posttax_dis_thousands.groupby(['country', 'year', 'country_year']).sum().reset_index()
wid_posttax_dis_thousands_shares.rename(columns={"share": "share_thousands"}, inplace=True)


posttax_dis_shares_check = pd.merge(wid_posttax_dis_percentiles_shares, wid_posttax_dis_tenths_shares[['country_year', 'share_tenths']], on='country_year', validate='one_to_one')
posttax_dis_shares_check = pd.merge(posttax_dis_shares_check, wid_posttax_dis_hundreds_shares[['country_year', 'share_hundreds']], on='country_year', validate='one_to_one')
posttax_dis_shares_check = pd.merge(posttax_dis_shares_check, wid_posttax_dis_thousands_shares[['country_year', 'share_thousands']], on='country_year', validate='one_to_one')



posttax_dis_shares_check = posttax_dis_shares_check[['country', 'year', 'country_year', 'share_percentiles', 'share_tenths', 'share_hundreds', 'share_thousands']]

posttax_dis_shares_check.describe()
# + [markdown] tags=[]
# ### Comparability of values between periods
# -



