# %% [markdown]
# # A first look at the MPI data
# Our MPI data is quite out of date. Max and Joe had a meeting with Nicolai, Usha and Sabina from OPHI.
#
# We were provided with a csv and codebook (in the 'Original' folder) by Nicolai and Usha in email correspondence.
#
# The idea is for us to take a look and then get back to them with any requests about the structure of the data.

# %%
# Import
import pandas as pd
from plotnine import *

# %%
#read original data file provided by Nicolai and Usha
df = pd.read_csv('Original/GMPI2021_publicuse.csv')

# %%
# Standardize country names

# df.head()
## Export to pass through country name tool
# df[['cty_lab']].rename(columns={'cty_lab': 'country'}).drop_duplicates().to_csv("Manipulation/MPI countries.csv", index = False)

# Grab country name mapping csv
country_names_map = pd.read_csv("Manipulation/MPI countries_country_standardized.csv")

# Merge into main data
df = pd.merge(df.rename(columns={'cty_lab': 'country'}),country_names_map,how='left', on='country')

# Swap country vars over
df = df.drop(columns='country')
df = df.rename(columns={'Our World In Data Name': 'country'})

# Rearrange columns
df = df[["year", "country", "area_lab", "flav", "t", "measure_lab",  "ind_lab", "b", "se", "indicator", "measure", "survey", "loa", "w_region", "k", "wgts", "spec",  "misind_lab"]]

# %% [markdown]
# ## The structure of the data

# %%
df.head()

# %% [markdown]
# The data is arranged by country, area, year and measure.
#
# Area is coded in `area_lab` and is set to one of 'National', 'Rural' or 'Urban' (NB. Palestine (alone) has some rows where `area = 'Camp'`).
#
# `year` is a string variable that often covers a two year period (reflecting the fact that the survey was spread over two calendar years). This is discussed more below.
#
# There are 8 different measures, given in `measure_lab`.

# %%
print("Count of countries with observations for each measure and area breakdown")
# Count unique countries by measure, and pivot by area
df.groupby(['measure_lab', 'area_lab'], as_index=False).agg({"country":"nunique"})\
   .rename(columns={'country':'unique_countries'})\
   .pivot_table(index = ["measure_lab"],
                columns = ["area_lab"],
                values = "unique_countries").reset_index()

# %% [markdown]
# ### Note on `year` 
#
# The way `year` is formatted – as a string variable often spanning two calendar years – won't work with our schema. We have to map the data to a single (integer) year.
#
# For now, arbitrarily, I take the first year in these cases and convert to integer.

# %%
# First year = first 4 characters of the year string
df['year'] = df['year'].str[:4].astype(int)
# df.head()

# %% [markdown]
# But it would be good to understand from OPHI what how best for us to handle this. Is there something better we could do than just taking the first year?
#
# I imagine it's not only Our World in Data who will be facing this issue, so perhaps it would be worth OPHI thinking about providing the year in an additional, programming-friednly format.
#
# For example, the World Bank's poverty data in the PIP (formerly Povcal) platform faces a similar issue where survey data spans across calendar years. The solution they come up with is to provide the year as a fraction e.g. 2011.75 – where the integer is the first calendar year in which the survey began and the decimal is the share of the second calendar year over which the survey took place. So if the survey occured for 3 months in 2011 and 9 months in 2012 the year would be recorded as 2011.75 (9/12 = 0.75).
#
# This means when you're pulling in the data, the `year` variable can be rounded – where 'rounding' effectively means selecting the year in which the bulk of the survey fell. This is at least a bit better than arbitrarily selecting the first or second celendar year. (Though note that in the World Bank data, the year fraction is coded only in terms of the start and end date of the survey. So it might not reflect the actual distribution of when the survey questions happened if they weren't evenly distributed across full period).

# %% [markdown]
# ### Note on `flav`
# Due to changing data coverage across surveys, OPHI produce two sets of estiamtes: point estimates for single years (`flav = cme` – "current marginal estimates") and estiamtes intended to track change over time (`flav = hot` – "harmonized over time"). The latter are based on the subset of survey data that is available across all years. The former is considered the most accurated for the most recent year.
# Note that the values can and do differ between these two sets of data. For instance, the MPI in Indonesia in 2017: 
# %%
df.loc[(df.country=="Indonesia")\
       & (df.measure_lab=="MPI")\
       & (df.area_lab=="National")\
       & (df.year==2017)]

# %% [markdown]
# #### `hot` data
#
# 'Harmonized over time' rows are given an ordering variable – `t  ∈ {1,2,3}` – as well as `year`.
# %%
df.loc[df.flav=="hot"].head()

# %% [markdown]
# Most countries only have two distinct years with observations. But about 1/3rd have three.

# %%
n_years = df.loc[df.flav=="hot"].groupby('country', as_index=False)\
            .agg({"year":"nunique"}).rename(columns={'year':'unique_years'})

country_group_n_years = n_years.groupby('unique_years', as_index=False)\
                               .agg({"country":"nunique"})\
                               .rename(columns={'countr':'countries_count'})

country_group_n_years.head()

# %%
# # Examples of countries with three year observations
n_years.loc[n_years.unique_years>2].head()

# %% [markdown]
# Bolivia is an example of a country with three observations.

# %%
df.loc[(df.flav=="hot") & (df.country=="Bolivia")].head()

# %% [markdown]
# #### `cme` data
# For 'Current marginal estmiates', only the latest year from the `hot` data is included and `t = NaN`.
#
# Note that not all countries have `hot` data (e.g. Angola).

# %%
df.groupby(["country","flav"]).agg({"year":["min", "max"]}).head(n=8)

# %% [markdown]
# ## Multi-dimesional poverty measures
#
# At least initially, we will be primarily concerned with the three measures that relate to overall multi-dimensional poverty:
# - `Headcount ratio`: the share of population in multidimensional poverty
# - `Intensity`: a measure of the average depth of poverty (of the poor only – NB, not like the World Bank's poverty gap index)
# - `MPI`: the product of `Headcount ratio` and `Intensity`.
#
# These are multi-dimensional poverty measures – a weighted aggregation across many individual indicators.
# Here I prepare this data as I would for uploading to OWID grapher and visualize it – separating the `hot` from the `cme` data.

# %%
# Prep data for OWID

# filter for main multi-dimensional pov measures
df_main = df.loc[(df['measure_lab'].isin(["MPI", "Intensity", "Headcount ratio"]))]

# pivot to wide format
df_main = df_main.pivot_table(index = ["year","country", "flav"],
                                           columns = ["measure_lab", "area_lab"],
                                           values = "b").reset_index()

# collapse multi-level index into single column names
df_main.columns = [' '.join(col).strip() for col in df_main.columns.values]

# Separate hot and cme data. These are the files we would upload to OWID grapher
df_main_hot = df_main.loc[df_main.flav=="hot"].drop(columns = ['flav'])
df_main_cme = df_main.loc[df_main.flav=="cme"].drop(columns = ['flav'])

# %% [markdown]
# #### `hot` data

# %%
df_main_hot.head()

# %%
# Write to csv
df_main_hot.to_csv("final/MPI (2021) – Harmonized over time estimates.csv")

# %%
# Plot HOT data
# select countries to plot
select_countries = ["Bolivia", "Indonesia", "Liberia"]

# filter hot data
chart_df = df_main_hot.loc[df_main_hot['country'].isin(select_countries)]

# plot
(ggplot(chart_df, aes(x='year', y='Headcount ratio National', color='country')) 
     + geom_point()
     + geom_line())

# %% [markdown]
# #### `cme` data
# %%
df_main_cme.head()

# %%
# Write to csv
df_main_cme.to_csv("final/MPI (2021) – Current estimates.csv")

# %%
# Plot CME data
(ggplot(df_main_cme, aes(x='Headcount ratio National', y='MPI National', color='year')) 
     + geom_point())

# %% [markdown]
# ## Other measures
#
# In addition there are a number of measures which are in turn broken down by individual indicators.
#
# In the future we could consider make an explorer to help navigate these.
#
# This includes:
#
# - the share who are poor in that indicator alone
#    - `Uncensored headcount ratio` = share who are deprived in that indicator out of the total population
#    - `Censored headcount ratio` = share who are deprived in that indicator out of the population who are multidimensionally poor
#     
# (Note that not all indicators are available for all countries – the composition of the MPI varies according to what's available in the survey data).

# %%
df.loc[df['measure_lab'].isin(["Censored headcount ratio", "Uncensored headcount ratio"])]\
   .groupby(['measure_lab', 'ind_lab'], as_index=False).agg({"country":"nunique"})\
   .rename(columns={'country':'unique_countries'})

# %% [markdown]
# - The `Absolute` and `Relative contribution` each indicator makes to the MPI measure.
# (As we show below, the relative contributions sum to 100% and the absolute contributions sum to the MPI value).

# %%
# Sum relative contributions by country-year-area-flav
df_rel_sum = df.loc[(df.measure_lab=="Relative contribution") & (df.ind_lab.notnull())]\
    .groupby(['country', 'year', 'area_lab', 'flav'], as_index=False)\
    .agg({"b":"sum"}).rename(columns={'b':'sum_of_relative_contributions'})

# Sum absolute contributions by country-year-area-flav
df_abs_sum = df.loc[(df.measure_lab=="Absolute contribution") & (df.ind_lab.notnull())]\
    .groupby(['country', 'year', 'area_lab', 'flav'], as_index=False)\
    .agg({"b":"sum"}).rename(columns={'b':'sum_of_absolute_contributions'})

# Store MPI by country-year-area-flav
df_MPI = df.loc[(df.measure_lab=="MPI")]\
    .rename(columns={'b':'MPI'})\
    [['country', 'year', 'area_lab', 'flav', 'MPI']]

# Merge the sums with the MPI
df_rel_abs_sums = pd.merge(df_rel_sum,df_abs_sum)
df_rel_abs_sums = pd.merge(df_rel_abs_sums,df_MPI)

print("The sum of relative contributions = 100%; the sum of absolute contributions = MPI")
df_rel_abs_sums.head()


# %% [markdown]
# One mistake in the data (I think – though I may be misunderstanding something) is that there are some rows where `measure_lab` = *"Absolute contribution"* or *"Relative contribution"* but `indicator` is blank (- in the calculation and table in the previous step, I dropped these).
#
# For each country-year-area-flav observation, there are three such 'blanks'.
#
# I think these relate to the relative contribution of the three _dimensions_ of indicators (Health, Education, Living Standards) – see [OPHI's description](https://ophi.org.uk/multidimensional-poverty-index/). But, as far as I can see, there is no variable that tells you which is which.

# %%
df.loc[(df['measure_lab'].isin(["Absolute contribution", "Relative contribution"]))\
           & (~df.ind_lab.notnull())]\
  .head(n=12)

# %% [markdown]
# Finally, `population share` gives the share of national population in each subnational unit.

# %%
print("Subnational breakdown of population")
df.loc[(df.measure_lab=="Population share")]\
  .pivot_table(index = ["year","country", "flav"],
              columns = ["area_lab"],
              values = "b",
              margins=True,
              aggfunc='sum').reset_index().head()

# %%
