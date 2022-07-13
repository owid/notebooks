# %% [markdown]
# # OWID Data Document<br>Checking data availability for countries in Penn World Table

# %% [markdown]
# ### About OWID Data documents
#
# OWID data documents combine computer code and text to explain and document the data we and how we prepare it from the original sources.
#
# We make these documents available in different formats:
#
# - A [read-only version](https://htmlpreview.github.io/?https://raw.githubusercontent.com/owid/notebooks/main/BetterDataDocs/PabloArriagada/pwt/notebooks/analysis_notebooks/compare_trade_shares/compare_trade_shares.html) online
# - A script in [GitHub](https://github.com/owid/notebooks/blob/main/BetterDataDocs/PabloArriagada/pwt/notebooks/analysis_notebooks/compare_trade_shares/compare_trade_shares.qmd)
# - A runnable version in [Google Colab](https://colab.research.google.com/drive/1e0wmNlZI_8Sw5b0ocLePNMTpbcqLNHDY#scrollTo=Xf_VyXxPjMAL)
#
#
#
# If you have this open in _Google Colab_, you can run the code blocks below and see their outputs. Clicking on **'Copy to Drive'** in the menu bar above will open up a new copy in your own Google Drive that you can then _edit_ the code to explore the data further.

# %% [markdown]
# ## Coverage by year

# %% [markdown]
# This notebook is to analyse in detail the availability of data for each country in Penn World Table 10.0, as not all countries cover the entire 1950-2019 range of the dataset.

# %% [markdown]
# First, the necessary libraries are imported.

# %%
import pandas as pd
import plotly.express as px
import plotly.io as pio
import numpy as np
from IPython.display import Image

pio.renderers.default = "jupyterlab+png+colab+notebook_connected+vscode"

# %%
#Main data file
url = "https://joeh.fra1.digitaloceanspaces.com/pwt/entities_standardized.csv"
df = pd.read_csv(url)

#National Accounts file
url = "https://joeh.fra1.digitaloceanspaces.com/pwt/entities_standardized_national_accounts.csv"
df_na = pd.read_csv(url)

# %% [markdown]
# Penn World Table only defines countries with their current name. There is no Soviet Union, Yugoslavia, Czechoslovakia or East Germany and consequentially the time range of each country's data is affected.

# %%
df.entity.unique()

# %% [markdown]
# The original file is grouped by year, the number of observations per year are counted and the dataframe is transformed to a long structure, to be able to plot more easily.

# %%
df_all_year = df.groupby(['year']).count().reset_index()
df_all_year = pd.melt(df_all_year, id_vars=['year'])
df_all_year = df_all_year[~df_all_year['variable'].isin(['cor_exp', 'statcap'])].reset_index(drop=True)

df_all_countryyear = df.groupby(['entity', 'year']).count().reset_index()
df_all_countryyear = pd.melt(df_all_countryyear, id_vars=['entity', 'year'])

# %% [markdown]
# When plotting the number of observations (i.e. countries) against years for each variable available in PWT we can see the jumps in coverage. For example, for the GDP variables, in 1950 there are over 50 countries covered, in 1960 they are over 100 and in 1970 the number is 157. The last big jump is in 1990 to reach 181 countries to get 183 between 2005 and 2019. For some other variables the number of countries available is a smaller quantity, it is important to have in mind this when aggregating regional data especially in previous decades.

# %%
fig = px.line(df_all_year, x="year", y="value", color="variable", height=600,
              title='<b>Country coverage in PWT</b>',
             labels={
                     "value": "Number of countries",
                 })
fig.show()

# %% [markdown]
# ## Coverage by country and year

# %% [markdown]
# How is this availability shown by country? In this graph the countries are in ascending order of the number of observations available. For instance, the entities with the lowest number of years available (for `rgdpe`) are Curaçao and Sint Maarten (Dutch part), incorporated in 2005. They are followed by the countries included from 1990 onwards, mostly former Soviet republics, the nations that formed Yugoslavia, Czechia and Slovakia. The countries incorporated from 1970 onwards are more varied, including Caribbean countries as Antigua and Barbuda or Bahamas and several Asian countries, like Saudi Arabia, Iraq, Laos or Mongolia. The 1960 batch is mostly from Africa (Botswana, Cameroon, Mozambique, Senegal...). The countries that cover the entire timeframe of PWT are most of the advanced economies of Europe and North America, several South American countries and Australia and New Zealand.
# <br><br>*Pablo: For now I couldn't generate a plot in Plotly to correctly display this, so I used Tableau, which took no time for me. See [here](https://public.tableau.com/app/profile/parriagadap/viz/PWT/CountriesinPWT.png) if the picture is not displayed correctly or [here](https://public.tableau.com/app/profile/parriagadap/viz/PWT/CountriesinPWT) to see the interactive version (which wasn't possible to embed here)*

# %%
Image(url="https://raw.githubusercontent.com/owid/notebooks/main/BetterDataDocs/PabloArriagada/pwt/notebooks/analysis_notebooks/CountriesinPWT.png",
      width=1100, height=2000)

# %% [markdown]
# Please note that the range is mostly continous after each country is included, but there are exceptions, like in `cgdpo` in the case of Bermuda, unavailable for 1999, 2000, 2001 and 2003.
# See [here](https://public.tableau.com/app/profile/parriagadap/viz/PWT/CountriesinPWT.png?Variable=cgdpo) if the picture is not displayed correctly or [here](https://public.tableau.com/app/profile/parriagadap/viz/PWT/CountriesinPWT?Variable=cgdpo) to see the interactive version.

# %%
Image(url="https://raw.githubusercontent.com/owid/notebooks/main/BetterDataDocs/PabloArriagada/pwt/notebooks/analysis_notebooks/CountriesinPWT_cgdpo.png",
      width=1100, height=2000)

# %% [markdown]
# What about the National Accounts data? This is where we are taking the `trade_openness` variable from. If we count how many times the `v_x`, `v_m`, `v_gdp` and `xr2` variables are included by each country-year (the variables needed to construct `trade_openness`) we have this availability by entity. See [here](https://public.tableau.com/views/PWT/CountriesinPWTNA.png) if the picture is not displayed correctly or [here](https://public.tableau.com/views/PWT/CountriesinPWTNA) to see the interactive version:

# %%
Image(url="https://raw.githubusercontent.com/owid/notebooks/main/BetterDataDocs/PabloArriagada/pwt/notebooks/analysis_notebooks/CountriesinPWTNA.png",
      width=1100, height=2000)

# %% [markdown]
# ## Country consistency between both datasets

# %% [markdown]
# In the `NA` dataset there are more entities included than the official PWT table, like Czechoslovakia and the Soviet Union. A full list of the differences can be observed here:

# %%
list_country = list(df['entity'].unique())
list_country_na = list(df_na['entity'].unique())

pwt_vs_na = list(set(list_country).difference(list_country_na))
pwt_vs_na.sort()
na_vs_pwt = list(set(list_country_na).difference(list_country))
na_vs_pwt.sort()

# %% [markdown]
# There is not any country available in the PWT file but not in the NA file:

# %%
pwt_vs_na

# %% [markdown]
# But the national accounts file contains multiple country not in PWT:

# %%
na_vs_pwt

# %% [markdown]
# From this list and the previous graphs I can check which countries require to be included for constructing the `trade_openness` variable:

# %% [markdown]
# | Country | All 4 variables<br>available in NA | Should we keep it<br>for calculations? |
# | --- | --- | --- |
# | Afghanistan | From 1970 | Yes |
# | Andorra | From 1970 | Yes |
# | China (alternative inflation series) | From 1952 | **NO** |
# | Cook Islands | From 1970 | Yes |
# | Cuba | From 1970 | Yes |
# | Czechoslovakia | **NO** | **NO** |
# | Eritrea | From 1990 | Yes |
# | French Polynesia | From 1970 | Yes |
# | Greenland | From 1970 | Yes |
# | Kiribati | From 1970 | Yes |
# | Kosovo | From 1990 | Yes |
# | Libya | From 1970 | Yes |
# | Liechtenstein | From 1970 | Yes |
# | Marshall Islands | From 1970 | Yes |
# | Micronesia (country) | From 1970 | Yes |
# | Monaco | From 1970 | Yes |
# | Nauru | From 1970 | Yes |
# | Netherlands Antilles | **NO** | **NO** |
# | New Caledonia | From 1970 | Yes |
# | North Korea | From 1970 | Yes |
# | Palau | From 1970 | Yes |
# | Papua New Guinea | From 1960 | Yes |
# | Puerto Rico | From 1950 | Yes |
# | Samoa | From 1970 | Yes |
# | San Marino | From 1970 | Yes |
# | Solomon Islands | From 1970 | Yes |
# | Somalia | From 1970 | Yes |
# | South Sudan | From 2008 | Yes |
# | Timor | From 1990 | Yes |
# | Tonga | From 1970 | Yes |
# | Tuvalu | From 1970 | Yes |
# | USSR | **NO** | **NO** |
# | Vanuatu | From 1970 | Yes |
# | Yugoslavia | **NO** | **NO** |

# %% [markdown]
# There's an alternative China series that needs to be excluded, together with Czechoslovakia, Netherlands Antilles, the USSR and Yugoslavia. The remaining countries will allow for a greater coverage of the `trade_openness` series.

# %% [markdown]
# ## Year consistency between both datasets 

# %% [markdown]
# Does the NA file cover more years than the final PWT file? For the countries common to both files we can see this is not true: the minimum year with non-null `rgdpe` data (for the main file) or non-null `v_x`, `v_m`, `v_gdp` and `xr2` data (for the NA file) is always the same for each country.

# %%
df_clean = df.dropna(subset=['rgdpe']).reset_index(drop=True)
df_na_clean = df_na.dropna(subset=['v_x', 'v_m', 'v_gdp', 'xr2']).reset_index(drop=True)

df_clean = df_clean[['entity', 'year']].groupby(by=["entity"]).min().reset_index()
df_na_clean = df_na_clean[['entity', 'year']].groupby(by=["entity"]).min().reset_index()

#left join to compare only common countries
df_clean_merge = pd.merge(df_clean, df_na_clean, how='left', on='entity', suffixes=(None, '_na'), validate='one_to_one') 
df_clean_merge['equal_min_year'] = df_clean_merge['year'] == df_clean_merge['year_na']

# %%
#Filtering only the countries with different minimum years
df_clean_merge[df_clean_merge['equal_min_year']==False]

# %% [markdown]
# ## Data quality variables

# %% [markdown]
# PWT also includes data quality variables which are not necessarily applied uniformly between countries. See for example `i_cig`, the variable referring to the quality of the relative price data for consumption, investment and government. Each point in the scatter plot is one country-year: some quality categories are evenly distributed (as *ICP PPP timeseries...*, the vintages for the PPP), but some others are assigned differently (double-click in *Benchmark*).

# %%
#Generating percapita measures to see them plotted
df['rgdpe_pc'] = df['rgdpe']/df['pop']
df['rgdpo_pc'] = df['rgdpo']/df['pop']
df['cgdpe_pc'] = df['cgdpe']/df['pop']
df['cgdpo_pc'] = df['cgdpo']/df['pop']
df['rgdpna_pc'] = df['rgdpna']/df['pop']

# %%
df['i_cig'] = df['i_cig'].astype(str)

# %%
#Change the log_x and log_y parameters to "False" to see negative values

fig = px.scatter(df, x="year", y="rgdpe_pc", 
                 hover_data=['entity', 'year'], opacity=0.5, color='i_cig', 
                 title="<b>Type of estimation for the relative price data for consumption, investment and government (<i>i_cig</i>)</b><br>rgdpe_pc vs year",
                 log_x=False,
                 log_y=True,
                 height=600,
                )

fig.update_traces(marker=dict(size=10, line=dict(width=0, color='blue')))
fig.show()

# %%
