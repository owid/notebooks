# %% [markdown]
# # Checking data availability for countries

# %% [markdown]
# This notebook is to analyse in detail the availability of data for each country in Penn World Table 10.0, as not all countries cover the entire 1950-2019 range.

# %%
import pandas as pd
import plotly.express as px
import plotly.io as pio
import numpy as np

pio.renderers.default = "jupyterlab+png+colab+notebook_connected+vscode"

# %%
#Main data file
url = "https://joeh.fra1.digitaloceanspaces.com/pwt/entities_standardized.csv"

df = pd.read_csv(url)

# %% [markdown]
# Penn World Table only defines countries with their current name. There is no Soviet Union, Yugoslavia, Czechoslovakia or East Germany and consequentially the time range of each country's data is affected.

# %%
df.entity.unique()

# %%
#Generating percapita measures
df['rgdpe_pc'] = df['rgdpe']/df['pop']
df['rgdpo_pc'] = df['rgdpo']/df['pop']
df['cgdpe_pc'] = df['cgdpe']/df['pop']
df['cgdpo_pc'] = df['cgdpo']/df['pop']
df['rgdpna_pc'] = df['rgdpna']/df['pop']

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
# How is this availability shown by country? In this graph the countries are in ascending order of the number of observations available. For instance, the entities with the lowest number of years available (for `rgdpe`) are Curaçao and Sint Maarten (Dutch part), incorporated in 2005. They are followed by the countries included from 1990 onwards, mostly former Soviet republics, the nations that formed Yugoslavia, Czechia and Slovakia. The countries incorporated from 1970 onwards are more varied, including Caribbean countries as Antigua and Barbuda or Bahamas and several Asian countries, like Saudi Arabia, Iraq, Laos or Mongolia. The 1960 batch is mostly from Africa (Botswana, Cameroon, Mozambique, Senegal...). The countries that cover the entire timeframe of PWT are most of the advanced economies of Europe and North America, several South American countries and Australia and New Zealand.
# <br><br>*Pablo: For now I couldn't generate a plot in Plotly to correctly display this, so I used Tableau, which took no time for me. See [here](https://public.tableau.com/app/profile/parriagadap/viz/PWT/CountriesinPWT.png) if the picture is not displayed correctly or [here](https://public.tableau.com/app/profile/parriagadap/viz/PWT/CountriesinPWT) to see the interactive version (which wasn't possible to embed here)*

# %% [markdown]
# ![CountriesinPWT.png](attachment:CountriesinPWT.png)

# %% [markdown]
# Please note that the range is mostly continous after each country is included, but there are exceptions, like in `cgdpo` in the case of Bermuda, unavailable for 1999, 2000, 2001 and 2003.
# See [here](https://public.tableau.com/app/profile/parriagadap/viz/PWT/CountriesinPWT.png?Variable=cgdpo) if the picture is not displayed correctly or [here](https://public.tableau.com/app/profile/parriagadap/viz/PWT/CountriesinPWT?Variable=cgdpo) to see the interactive version.

# %% [markdown]
# ![CountriesinPWT_cgdpo.png](attachment:CountriesinPWT_cgdpo.png)

# %% [markdown]
# PWT also includes data quality variables which are not necessarily applied uniformly between countries. See for example `i_cig`, the variable referring to the quality of the relative price data for consumption, investment and government. Each point in the scatter plot is one country-year: some quality categories are evenly distributed (as *ICP PPP timeseries...*, the vintages for the PPP), but some others are assigned differently (double-click in *Benchmark*).

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
