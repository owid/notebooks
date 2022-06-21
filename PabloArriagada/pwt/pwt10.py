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

# # Penn World Table dataset

# The Penn World Table allows for cross-country comparisons of real GDP across time, making use of prices collected in multiple benckmark years by the International Comparisons Program (ICP) to construct purchasing-power-parity (PPP) exchange rates. The most recent version (10.0) contains information for 183 countries and regions from 1950 to 2019 (when it can be estimated).

# ## Index
# - [Metrics from the original dataset](#Derived-metrics-from-the-original-dataset)
#     - [Based on prices that are constant across countries and over time](#Based-on-prices-that-are-constant-across-countries-and-over-time)
#     - [Based on prices that are constant across countries in a given year](#Based-on-prices-that-are-constant-across-countries-in-a-given-year)
#     - [Based on national prices that are constant over time](#Based-on-national-prices-that-are-constant-over-time)
#     - [Other variables](#Other-variables)
# - [Derived metrics from this dataset](#Derived-metrics-from-this-dataset)
# - [Code for dataset transformations](#Code-for-dataset-transformations)
# - [Comparing the results to the OWID-modified PWT 9.1](#Comparing-the-results-to-the-OWID-modified-PWT-9.1)
#
# ## Appendix
# - [The changes in PWT 10.0](#The-changes-in-PWT-10.0)
# - [The variables of PWT](#The-variables-of-PWT)
# - [Exploratory Data Analysis](#Exploratory-Data-Analysis)

# ## Metrics from the original dataset

# ### Based on prices that are constant across countries and over time

# **Expenditure-side real GDP at chained PPPs (2017US$)**
# <br>
# *rgdpe*
# <br>
# It measures living standards across countries and across years using prices for final goods that are constant across countries and over time. This variable is multiplied by 1,000,000 to get the measure in 2017 USD instead of millions of USD.

# **Output-side real GDP at chained PPPs (2017US$)**
# <br>
# *rgdpo*
# <br>
# It measures productive capacity across countries and across years using prices for final goods, exports and imports that are constant across countries and over time. This variable is multiplied by 1,000,000 to get the measure in 2017 USD instead of millions of USD.

# ### Based on prices that are constant across countries in a given year

# **Real consumption of households and government, at current PPPs**
# <br>
# *ccon*
# <br>
# It is the sum of real household and government consumption, use to measure and compare living standards across countries. This variable is multiplied by 1,000,000 to get the measure in 2017 USD instead of millions of USD.

# **Real domestic absorption, at current PPPs (2017US$)**
# <br>
# *cda*
# <br>
# It is computed as the real consumption (*ccon*) plus real investment. The sum of *cda* and the real trade balance generates *rgdpe*, the expenditure-side real GDP at chained PPPs. This variable is multiplied by 1,000,000 to get the measure in 2017 USD instead of millions of USD.

# **Expenditure-side real GDP at current PPPs (2017US$)**
# <br>
# *cgdpe*
# <br>
# It measures the standards of living across countries in each year by using prices for final goods that are constant across countries. This variable is multiplied by 1,000,000 to get the measure in 2017 USD instead of millions of USD.

# **Output-side real GDP at current PPPs (2017US$)**
# <br>
# *cgdpo*
# <br>
# It measures the productive capacity across countries in each year by using prices for final goods, exports and imports that are constant across countries. This variable is multiplied by 1,000,000 to get the measure in 2017 USD instead of millions of USD.

# **Capital stock at current PPPs (2017US$)**
# <br>
# *cn*
# <br>
# It is estimated from investment by asset in each country, as structures, transport equipment, machinery and also computers, communication equipment and sofware on selected countries. Prices for these assets are constant across countries each year. This variable is multiplied by 1,000,000 to get the measure in 2017 USD instead of millions of USD.

# **Capital services levels at current PPPs (USA=1)**
# <br>
# *ck*

# **TFP level at current PPPs (USA=1)**
# <br>
# *ctfp*
# Total factor productivity level, computed with *cgdpo*, *cn*, labor input data and *labsh*, the share of labor income of employees and self-employed workers in GDP. It is useful to compare productivity levels across countries in each year.

# **Welfare-relevant TFP levels at current PPPs (USA=1)**
# <br>
# *cwtfp*
# Computed from *ctfp* and the real domestic absorption (*cda*), it measures living standards across countries in each year.

# + [markdown] tags=[]
# ### Based on national prices that are constant over time
# -

# **Real GDP at constant 2017 national prices (2017US$)**
# <br>
# *rgdpna*
# <br>
# The difference with the other GDP variables is this is obtained from national accounts data for each country and it is useful for comparing growth of GDP over time in each country. This variable is multiplied by 1,000,000 to get the measure in 2017 USD instead of millions of USD.

# **Real consumption at constant 2017 national prices (2017US$)**
# <br>
# *rconna*
# <br>
# Real household and government consumption at constant national prices. It is useful to compare growth of consumption over time in one country. This variable is multiplied by 1,000,000 to get the measure in 2017 USD instead of millions of USD.

# **Real domestic absorption at constant 2017 national prices (2017US$)**
# <br>
# *rdana*
# <br>
# Real consumption plus real investment at constant national prices. It is useful for comparing the growth of the absorption over time in each country. This variable is multiplied by 1,000,000 to get the measure in 2017 USD instead of millions of USD.

# **Capital stock at constant 2017 national prices (2017US$)**
# <br>
# *rnna*
# <br>
# Capital stock at constant national prices, based on investment and prices of structures and equipment. Useful for comparing growth of this variable over time in each country. This variable is multiplied by 1,000,000 to get the measure in 2017 USD instead of millions of USD.

# **Capital services at constant 2017 national prices (2017=1)**
# <br>
# *rkna*

# **TFP at constant national prices (2017=1)**
# <br>
# *rtfpna*
# <br>
# Total factor productivity level, computed with *rgdna*, *rnna*, labor input data and *labsh*, the share of labor income of employees and self-employed workers in GDP. It is useful to compare the growth of productivity over time in each country.

# **Welfare-relevant TFP at constant national prices (2017=1)**
# <br>
# *rwtfpna*
# <br>
# Computed from *rtfpna* and the real domestic absorption (*rdana*), it is useful for comparing the growth of welfare-relevant productivity over time in each country.

# + [markdown] jp-MarkdownHeadingCollapsed=true tags=[]
# ### Other variables
# -

# **Population**
# <br>
# *pop*
# <br>
# Number of people living in the country. This variable is multiplied by 1,000,000 to get the measure in people instead of millions of people.

# **Number of persons engaged (in millions)**
# <br>
# *emp*
# <br>
# This is the number of people working in the country (employees and self-employed). This variable is multiplied by 1,000,000 to get the measure in people instead of millions of people.

# **Average annual hours worked by persons engaged**
# <br>
# *avh*
# <br>
# It is the average sum of hours worked by employess and self-employed people during each year in a country.

# **Human capital index**
# <br>
# *hc*
# <br>
# This index is constructed using two estimates on years of schooling and returns to education.

# **Share of labour compensation in GDP at current national prices**
# <br>
# *labsh*
# <br>
# It is the share of labor income of employees and self-employed workers in GDP and it is used to compare total inputs across countries or over time

# **Real internal rate of return**
# <br>
# *irr*
# <br>

# **Average depreciation rate of the capital stock**
# <br>
# *delta*
# <br>

# **Exchange rate, national currency/USD (market+estimated)**
# <br>
# *xr*
# <br>

# **Price level of CCON (PPP/XR), price level of USA GDPo in 2017=1**
# <br>
# *pl_con*
# <br>
# Price level of *ccon*, equal to the PPP (ratio of *rconna* to *ccon*) divided by the nominal exchange rate, *xr*

# **Price level of CDA (PPP/XR), price level of USA GDPo in 2017=1**
# <br>
# *pl_da*
# <br>
# Price level of *cda* and *cgdpe*, equal to the PPP (ratio of *rdana* to *cda*) divided by the nominal exchange rate, *xr*

# **Price level of CGDPo (PPP/XR), price level of USA GDPo in 2017=1**
# <br>
# *pl_gdpo*
# <br>
# Price level of *cgdpo*, equal to the PPP (ratio of *rgdpna* to *cgdpo*) divided by the nominal exchange rate, *xr*

# **0/1/2/3/4: relative price data for consumption, investment and government is extrapolated (0), benchmark (1), interpolated (2), ICP PPP timeseries: benchmark or interpolated (3) or  ICP PPP timeseries: extrapolated (4)**
# <br>
# *i_cig*
# <br>

# **0/1/2: relative price data for exports and imports is extrapolated (0), benchmark (1) or interpolated (2)**
# <br>
# *i_xm*
# <br>

# **0/1: the exchange rate is market-based (0) or estimated (1)**
# <br>
# *i_xr*
# <br>

# **0/1: the observation on pl_gdpe or pl_gdpo is not an outlier (0) or an outlier (1)**
# <br>
# *i_outlier*
# <br>

# **0/1/2/3: the observation for irr is not an outlier (0), may be biased due to a low capital share (1), hit the lower bound of 1 percent (2), or is an outlier (3)**
# <br>
# *i_irr*
# <br>

# **Correlation between expenditure shares of the country and the US (benchmark observations only)**
# <br>
# *cor_exp*
# <br>

# **Statistical capacity indicator (source: World Bank, developing countries only)**
# <br>
# *statcap*
# <br>

# **Share of household consumption at current PPPs**
# <br>
# *csh_c*
# <br>

# **Share of gross capital formation at current PPPs**
# <br>
# *csh_i*
# <br>

# **Share of government consumption at current PPPs**
# <br>
# *csh_g*
# <br>

# **Share of merchandise exports at current PPPs**
# <br>
# *csh_x*
# <br>

# **Share of merchandise imports at current PPPs**
# <br>
# *csh_m*
# <br>

# **Share of residual trade and GDP statistical discrepancy at current PPPs**
# <br>
# *csh_r*
# <br>

# **Price level of household consumption,  price level of USA GDPo in 2017=1**
# <br>
# *pl_c*
# <br>

# **Price level of capital formation,  price level of USA GDPo in 2017=1**
# <br>
# *pl_i*
# <br>

# **Price level of government consumption,  price level of USA GDPo in 2017=1**
# <br>
# *pl_g*
# <br>

# **Price level of exports, price level of USA GDPo in 2017=1**
# <br>
# *pl_x*
# <br>

# **Price level of imports, price level of USA GDPo in 2017=1**
# <br>
# *pl_m*
# <br>

# **Price level of the capital stock, price level of USA in 2017=1**
# <br>
# *pl_n*
# <br>

# **Price level of the capital services, price level of USA=1**
# <br>
# *pl_k*
# <br>

# ## Derived metrics from this dataset

# **Output-side real GDP per capita**
# <br>
# *gdppc_o*
# <br>
# Estimated as the output-side real GDP in chained PPPs, 2017 USD (*rgdpo*) divided by the population of each country (*pop*).

# **Expenditure-side real GDP per capita**
# <br>
# *gdppc_e*
# <br>
# Estimated as the expenditure-side real GDP in chained PPPs, 2017 USD (*rgdpe*) divided by the population of each country (*pop*).

# **Productivity**
# <br>
# *productivity*
# <br>
# It is estimated as the total real output-side GDP per hour worked; it is then the GDP per capita (output-side) (*rgdpo*) divided by the average hours worked per persons engaged (*avh*) and the total number of persons engaged (*emp*).

# **Real GDP per capita (expenditure-side) in 1960**
# <br>
# *rgdpe_60*
# <br>
# This is the real GDP per capita (expenditure-side) (*gdppc_e*) for the year 1960.

# **Ratio of exports and imports to GDP (% of GDP)**
# <br>
# *ratio*
# <br>
# It is defined as the sum of exports and imports divided by the GDP at current prices.

# **Average real GDP per capita growth from 1960**
# <br>
# *rgdpo_growth*
# <br>
# It is defined as the average of the yearly growth rate of GDP per capita over the period 1960-2019. This is the mean of the logarithm of the output-side GDP per capita (*gdppc_o*) minus the GDP per capita (output-side) lagged by one year

# **World trade (% of GDP)**
# <br>
# *world_trade*
# <br>
# It is defined as the sum of all world exports and imports divided by the world GDP

# ## Code for dataset transformations

# ### Data sources
# - [PWT 10.0](https://www.rug.nl/ggdc/productivity/pwt/?lang=en)
# - [PWT 9.1](https://www.rug.nl/ggdc/productivity/pwt/pwt-releases/pwt9.1)
# - [PWT 9.1 in Grapher](https://owid.cloud/admin/datasets/4239) (Processed by Diana Beltekian)

# ### Documentation
# 1. [Diana Beltekian PWT 9.1 documentation for OWID](https://docs.google.com/document/d/1Kg9ZqxXXfDWA7WxfDysB0GjwlQ6kK5x6kNP-m7Sjl-I/edit?pli=1#)
# 2. [User Guide to PWT 10.0](https://www.rug.nl/ggdc/docs/pwt100-user-guide-to-data-files.pdf) (Recommended for new users)
# 3. [What's new in PWT 10.0?](https://www.rug.nl/ggdc/docs/pwt100-whatsnew.pdf) (Recommended for experienced users)
# 4. [The Next Generation of the Penn World Table](https://www.rug.nl/ggdc/productivity/pwt/related-research-papers/the_next_generation_of_the_penn_world_table.pdf) (Section I is recommended, because it explains what types of real GDP variables are available and when should be used)
# 5. [PWT 8.0 - A user guide](https://www.rug.nl/ggdc/docs/pwt_80_user_guide.pdf) (For *a broader understanding of the choices that were made in constructing PWT and some of the ‘health warnings’*)

# ### Transformations
# Using as a reference the document [(1)](https://docs.google.com/document/d/1Kg9ZqxXXfDWA7WxfDysB0GjwlQ6kK5x6kNP-m7Sjl-I/edit?pli=1#), the following transformations to PWT 10.0 are done to match the OWID structure in Grapher.
# The transformation of many variables consists in multiplying them by 1,000,000 to change their units from "million USD" to just "USD". It is the case for:
#
# - **Expenditure-side real GDP at chained PPPs**, `rgdpe`
# - **Output-side real GDP at chained PPPs**, `rgdpo`
# - **Real consumption of households and government at current PPPs**, `ccon`
# - **Real domestic absorption at current PPPs**, `cda`
# - **Expenditure-side real GDP at current PPPs**, `cgdpe`
# - **Output-side real GDP at current PPPs**, `cgdpo`
# - **Capital stock at current PPPs**, `cn`
# - **Real GDP at constant 2011 national prices**, `rgdpna`
# - **Real consumption at constant 2011 national prices**, `rconna`
# - **Real domestic absorption at constant 2011 national prices**, `rdana`
# - **Capital stock at constant 2011 national prices**, `rnna`
#
# Two variables are multiplied by 1,000,000 to express their units in "people" instead of "million people"
#
# - **Population**, `pop`
# - **Number of persons engaged**, `emp`
#
# The variable `productivity` is estimated as the **total real output-side GDP per hour worked**; it is then `rgdpo` divided by the average hours worked per persons engaged (`avh`) and the total number of persons engaged (`emp`)
#
# Two real GDP per capita measures are also calculated:
# - **Output-side real GDP per capita** (`gdppc_o`), as the total output-side real GDP `rgdpo` divided by the population `pop`
# - **Expenditure-side real GDP per capita** (`gdppc_e`) , as the total expenditure-side real GDP `rgdpe` divided by the population `pop`

# +
import pandas as pd
from pathlib import Path
import seaborn as sns
import numpy as np
import plotly.express as px
import plotly.io as pio

#Loading PWT 9.1
pwt9_path = Path('data/pwt91.xlsx')
pwt9 = pd.read_excel(pwt9_path,sheet_name='Data')

#Loading PWT 10.0
pwt10_path = Path('data/pwt100.xlsx')
pwt10 = pd.read_excel(pwt10_path,sheet_name='Data')

#Multiplying by 1 million to get USD instead of millions of USD
pwt10['rgdpe'] = pwt10['rgdpe']*1000000
pwt10['rgdpo'] = pwt10['rgdpo']*1000000
pwt10['ccon'] = pwt10['ccon']*1000000
pwt10['cda'] = pwt10['cda']*1000000
pwt10['cgdpe'] = pwt10['cgdpe']*1000000
pwt10['cgdpo'] = pwt10['cgdpo']*1000000
pwt10['cn'] = pwt10['cn']*1000000
pwt10['rgdpna'] = pwt10['rgdpna']*1000000
pwt10['rconna'] = pwt10['rconna']*1000000
pwt10['rdana'] = pwt10['rdana']*1000000
pwt10['rnna'] = pwt10['rnna']*1000000

#Multiplying by 1 million to get "people" instead of "millions of people"
pwt10['pop'] = pwt10['pop']*1000000
pwt10['emp'] = pwt10['emp']*1000000

#Productivity = (rgdpo) / (avh*emp)
#Productivity is total real output-side GDP per hour worked; where hours worked are calculated by multiplying
#the average hours worked per persons engaged by the total number of persons engaged.
pwt10['productivity'] = pwt10['rgdpo']/(pwt10['avh']*pwt10['emp'])

#Gdppc_o = rgdpo / pop
#Output-side real GDP per capita is calculated by dividing total output-side GDP by the total population.
pwt10['gdppc_o'] = pwt10['rgdpo']/pwt10['pop']

#Gdppc_e = rgdpe / pop
#Expenditure-side real GDP per capita is calculated by dividing total expenditure-side GDP by the total population.
pwt10['gdppc_e'] = pwt10['rgdpe']/pwt10['pop']
# -

# An interative calculation is necessary to create the `rgdpe_60`. This is the **real GDP per capita (expenditure-side) in 1960**. It is then `gdppc_e` value for each country in 1960.

for i in range(len(pwt10)): #runs for the entire length of th dataframe
    country = pwt10['countrycode'][i] #gets the country from row i
    #gets GDP_E from 1960 and the country I calculated in the previous row:
    gdp60_country = pwt10.loc[(pwt10['countrycode'] == country) & (pwt10['year'] == 1960), 'gdppc_e'].iloc[0]
    pwt10.loc[i,'rgdpe_60'] = gdp60_country #assigns the 1960 GDP value from "country" to every year for that country

# The variable `gdppc_o_yearbefore` is the **GDP per capita (output-side) lagged by one year**. This variable will be useful for the estimation of `rgdpo_growth`, the average growth between 1960 and 2019.

for i in range(len(pwt10)): #runs for the entire length of th dataframe
    country = pwt10['countrycode'][i] #gets the country from row i
    year = pwt10['year'][i] #gets the year from row i
    try:
        #gets the gdp from "country" the year before to "year"
        gdp_yearbefore = pwt10.loc[(pwt10['countrycode'] == country) & (pwt10['year'] == year-1), 'gdppc_o'].iloc[0]
    except: #in case of error (no row available, no year before)
        gdp_yearbefore = None
    pwt10.loc[i,'gdppc_o_yearbefore'] = gdp_yearbefore #assigns the gdp from the previous year to the following year's row

# **The real GDP growth per capita 1960-2019** (`gdppc_o_growth`) is defined as the average of the yearly growth rate of GDP per capita over the period 1960-2019. This is the mean of the logarithm of the GDP per capita (output-side) minus the GDP per capita (output-side) lagged by one year. To estimate this a separate dataset by country is generated.

# +
#rgdpo_growth = mean(logrgdppco[_n] - logrgdppco[_n-1]) where logrgdppco = log(rgdpo/pop)
#Real GDP growth per capita is calculated as the average of the yearly growth rate of GDP per capita over the period 1960-2017.

#Filters the data only between 1960 and 2019 (before it was until 2017)
pwt10_60 = pwt10[(pwt10['year']>=1960) & (pwt10['year']<=2019)].copy().reset_index(drop=True)
#Calculates the difference between log(gdppc_o) from current year and the one from previous year
pwt10_60['log_diff'] = np.log(pwt10_60['gdppc_o']) - np.log(pwt10_60['gdppc_o_yearbefore'])

country_list = list(pwt10_60['countrycode'].unique()) #gets list of countries
growth_db = pd.DataFrame(columns=pwt10_60.columns) #creates an empty dataframe to use it in the following interation

for i in country_list: #for each country
    db_percountry = pwt10_60[pwt10_60['countrycode']==i].copy().reset_index(drop=True) #dataframe with data from country i
    growth_db_aux = pd.DataFrame(columns=db_percountry.columns) #another empty dataset to temporarily poblate fill it with data
    
    growth_db_aux.loc[0,'countrycode'] = i #assigns country i
    growth_db_aux.loc[0,'gdppc_o_growth'] = db_percountry['log_diff'].mean() #assigns the average gdp from 1960 to 1960
    growth_db_aux.loc[0,'gdppc_o_growth_count'] = db_percountry['log_diff'].count() #counts how many times the log diff is
    
    #growth_db = growth_db.append(growth_db_aux,ignore_index=True) #Each country row is appended to get the growth per country db
    growth_db = pd.concat([growth_db, growth_db_aux], ignore_index=True)

growth_db['year'] = 1960
growth_db
# -

# To derive variables associated with imports and exports it is necessary to load the additional National Accounts data file from PWT 10.0:

#loads the PWT 10.0 National Accounts dataset
pwt10_na_path = Path('data/pwt100-na-data.xlsx')
pwt10_na = pd.read_excel(pwt10_na_path,sheet_name='Data')
pwt10_na

# This dataset is now merged with the PWT 10.0 (only the variables needed are selected):

#merge between pwt10 and pwt10_na (only 'v_x','v_m','v_gdp','xr2')
merge_pwtna_10 = pd.merge(pwt10, pwt10_na[['countrycode','year','v_x','v_m','v_gdp','xr2']], 
                          on=['countrycode','year'], how='left',validate='one_to_one')

# Now the variable `ratio` can be generated. This is the **Ratio of exports and imports to GDP (%)** and it is defined as the sum of exports and imports divided by the GDP at current prices. Although it is not necessary to transform them to USD, the calculation is useful to get the world trade variable afterwards.

# +
#Ratio = ((ex_usd + imp_usd) / gdp_usd )*100, where ex_usd = v_x / xr2 to convert export (and v_m for import) values into US$.
#The ratio of exports and imports to GDP is calculated by summing a country’s total imports and exports, then dividing by the country’s GDP - after all values have been converted to US$.

merge_pwtna_10['exp_usd'] = merge_pwtna_10['v_x']/merge_pwtna_10['xr2']
merge_pwtna_10['imp_usd'] = merge_pwtna_10['v_m']/merge_pwtna_10['xr2']
merge_pwtna_10['gdp_usd'] = merge_pwtna_10['v_gdp']/merge_pwtna_10['xr2']
merge_pwtna_10['ratio'] = (merge_pwtna_10['exp_usd'] + merge_pwtna_10['imp_usd'])/merge_pwtna_10['gdp_usd']*100
# -

# Similarly to the `ratio`, **the world trade (% of GDP)** is defined as the sum of all world exports and imports divided by the world GDP. To estimate this a separate dataset by year is generated.

# +
#World trade (% of GDP) = [ (world imports + world exports) / (world GDP) ]*100
#World trade is constructed by summing countries’ total imports to arrive at the ‘world’ estimate of imports,
#and doing the same for total exports, and GDP in each year to arrive at a ‘world’ estimate for each of the respective variables.

year_list = list(merge_pwtna_10['year'].unique()) #gets the list of years
world_db = pd.DataFrame(columns=merge_pwtna_10.columns) #creates an empty dataframe to use in the following interation

for i in year_list: #for each year
    #creates a filtered dataset for year i
    db_peryear = merge_pwtna_10[merge_pwtna_10['year']==i].copy().reset_index(drop=True)
    world_db_aux = pd.DataFrame(columns=db_peryear.columns) #auxiliar dataset to fill it with data per year
    
    world_db_aux.loc[0,'year'] = i #assign year i to the auxiliar dataset 
    world_db_aux.loc[0,'world_imports'] = db_peryear['imp_usd'].sum() #assign the sum of imp_usd to the auxiliar dataset 
    world_db_aux.loc[0,'world_exports'] = db_peryear['exp_usd'].sum() #assign the sum of exp_usd to the auxiliar dataset 
    world_db_aux.loc[0,'world_gdp'] = db_peryear['gdp_usd'].sum() #assign the sum of gdp_usd to the auxiliar dataset 
    
    #world_db = world_db.append(world_db_aux,ignore_index=True) #Each year row is appended to get the trade per year db afterwards
    world_db = pd.concat([world_db, world_db_aux], ignore_index=True)

world_db['country'] = "World" #assigns the country "World"

#estimation of the world trade, according to the formula
world_db['world_trade'] = (world_db['world_imports'] + world_db['world_exports'])/world_db['world_gdp']*100
world_db
# -

# To have every variable in the same dataset, this code joins the main PWT 10.0 with the by country and by year datasets used to generate the real GDP growth per capita 1960-2019 and the world trade.

# +
pwt10_owid = pd.merge(merge_pwtna_10, growth_db[['countrycode','year','gdppc_o_growth','gdppc_o_growth_count']], 
                      on=['countrycode','year'], how='left',validate='one_to_one')
#pwt10_owid = pwt10_owid.append(world_db,ignore_index=True)
pwt10_owid = pd.concat([pwt10_owid, world_db], ignore_index=True)

pwt10_owid
# -

# This is the consolidated PWT dataset with the transformations. A little clean-up is needed though, to match the variables with the previous version uploaded at OWID.
#
# The PWT 9.1 transformed file is uploaded here:

pwt9_path = Path('data/Penn World Tables version 9.1 (2019).csv')
pwt9_owid = pd.read_csv(pwt9_path)
pwt9_owid

# PWT 10.0 has currently 72 columns (variables), much more than the 57 in v9.1, so a check is needed to leave only the necessary.

pwt9_owid.columns

pwt10_owid.columns

# OWID's v9.1 consists in every variable kept from the original dataset but `currency_unit` and the newly created variables, so this code removes the auxiliar variables used to create others and the ones that came from the national accounts file:

pwt10_owid.drop(['exp_usd', 'gdp_usd', 'gdppc_o_yearbefore', 'imp_usd', 'gdppc_o_growth_count', 'v_gdp', 'v_m', 'v_x', 
                 'world_exports', 'world_gdp', 'world_imports', 'xr2'], axis = 1)

# There are two more variables in v10.0 compared to v9.1, because both `countrycode` and `currency_unit` are kept for reference.

# The file is saved to use the [Country Standardizer Tool](https://owid.cloud/admin/standardize) from OWID.

file = Path('data/pwt10_owid_beforestd.csv')
pwt10_owid.to_csv(file, index=False)

# The tool provides with a new variable called `Our World In Data Name`, which is OWID's standardisation applied.

pwt10_path = Path('data/pwt10_owid_country_standardized.csv')
pwt10_owid = pd.read_csv(pwt10_path)
pwt10_owid

pwt10_owid = pwt10_owid.rename(columns={'Our World In Data Name': 'entity'}) #To keep variable name from v9.1

file = Path('data/pwt10_owid.csv')
pwt10_owid.to_csv(file, index=False)

# ## Comparing the results to the OWID-modified PWT 9.1

# One option to compare the results is to merge both PWT 9.1 and 10.0 modified files by country and year:

pwt910_owid = pd.merge(pwt10_owid, pwt9_owid, left_on=['entity','year'], right_on=['Entity', 'Year'],
                       how='left')
pwt910_owid = pwt910_owid.apply(pd.to_numeric, errors='ignore')

# Th `describe()` command provides descriptive statistics for each pair of created variables, the ones from 10.0 and the ones from 9.1.
#
#
# **Productivity** statistics for PWT 9.1 and PWT 10.0:

pwt910_owid[['productivity',
            'Productivity (PWT 9.1 (2019))']].describe()

# **Output-side real GDP per capita (gdppc_o)** statistics for PWT 9.1 and PWT 10.0:

pwt910_owid[['gdppc_o',
            'Output-side real GDP per capita (gdppc_o) (PWT 9.1 (2019))']].describe()

# **Expenditure-side real GDP per capita (gdppc_e)** statistics for PWT 9.1 and PWT 10.0:

pwt910_owid[['gdppc_e',
            'Expenditure-side real GDP per capita (gdppc_e) (PWT 9.1 (2019))']].describe()

# **Real GDP per capita in 1960 at chained PPPs** statistics for PWT 9.1 and PWT 10.0:

pwt910_owid[['rgdpe_60',
            'Real GDP per capita in 1960 at chained PPPs in 2011 US$ (PWT 9.1 (2019))']].describe()

# **Average real GDP per capita growth 1960-2017 (2019), chained PPPs** statistics for PWT 9.1 and PWT 10.0:

pwt910_owid[['gdppc_o_growth',
            'Average real GDP per capita growth 1960-2017, chained PPPs in 2011 US$ (PWT 9.1 (2019))']].describe()

# **Ratio of exports and imports to GDP (%)** statistics for PWT 9.1 and PWT 10.0:

pwt910_owid[['ratio',
            ' Ratio of exports and imports to GDP (%) (PWT 9.1 (2019))']].describe()

# **World trade (% of GDP)** statistics for PWT 9.1 and PWT 10.0:

pwt910_owid[['world_trade',
            'World trade (% of GDP) (PWT 9.1) (PWT 9.1 (2019))']].describe()

# Every variable shows consistency between v9.1 and 10.0 in aggregate statistics.
#
# But how about differences **by country**?
#
# A practical way to compare the transformed variables between both versions is creating a ratio between both estimates (v10.0/v9.1): if the ratio equals 1 it means the values stay the same, if it is greater than 1 it means the value has been corrected upwards and if it less than one it means the value has been reduced for v10.0.
#
# The `_vs` variables in this code represent these values.

# +
pwt910_owid['gdppc_o_vs'] = pwt910_owid['gdppc_o']/pwt910_owid['Output-side real GDP per capita (gdppc_o) (PWT 9.1 (2019))']

pwt910_owid['gdppc_e_vs'] = pwt910_owid['gdppc_e']/pwt910_owid['Expenditure-side real GDP per capita (gdppc_e) (PWT 9.1 (2019))']

pwt910_owid['rgdpe_60_vs'] = pwt910_owid['rgdpe_60']/pwt910_owid['Real GDP per capita in 1960 at chained PPPs in 2011 US$ (PWT 9.1 (2019))']

pwt910_owid['productivity_vs'] = pwt910_owid['productivity']/pwt910_owid['Productivity (PWT 9.1 (2019))']

pwt910_owid['gdppc_o_growth_vs'] = pwt910_owid['gdppc_o_growth']/pwt910_owid['Average real GDP per capita growth 1960-2017, chained PPPs in 2011 US$ (PWT 9.1 (2019))']

pwt910_owid['ratio_vs'] = pwt910_owid['ratio']/pwt910_owid[' Ratio of exports and imports to GDP (%) (PWT 9.1 (2019))']

pwt910_owid['world_trade_vs'] = pwt910_owid['world_trade']/pwt910_owid['World trade (% of GDP) (PWT 9.1) (PWT 9.1 (2019))']

pwt910_owid_0 = pwt910_owid.fillna(0)
# -

# It seems [it's not possible](https://github.com/plotly/plotly.py/issues/931) to render Plotly with interactivity on GitHub, so it is necessary to switch renderers depending on use.
#
# [About renderers in Plotly](https://plotly.com/python/renderers/)

# **Output-side real GDP per capita (gdppc_o)** compared by country:

# +
#"png" for GitHub, "colab" for Google Colab, "notebook_connected" for Jupyter Notebooks, "jupyterlab" for JL
pio.renderers.default = "jupyterlab+png+colab+notebook_connected"

fig = px.scatter(pwt910_owid_0, x="gdppc_o", y="gdppc_o_vs", 
                 hover_data=['entity', 'year'], opacity=0.5, color='entity', 
                 title="Output-side real GDP per capita (gdppc_o) comparison: PWT 9.1 vs PWT 10.0",
                 log_x=True,
                 log_y=True,
                 height=600,
                labels={
                     "gdppc_o": "Output-side real GDP per capita (PWT 10.0)",
                     "gdppc_o_vs": "PWT 10.0 / PWT 9.1 (1 = same value)",
                     "entity": "Country"
                 })

fig.update_traces(marker=dict(size=10, line=dict(width=0, color='blue')))
fig.show()
# -

# Though most of the results show ratios around 1, there are extreme upward corrections for **Turks and Caicos Islands** (3x, 6x and even 11x in 2015, 2016 and 2017, respectively). Countries with ~2x corrections include **Liberia, Mauritania, Zimbabwe, Iraq (90s, early 2000s), Fiji, Paraguay, Antigua and Barbuda, Montserrat, Equatorial Guinea, British Virgin Islands and Cayman Islands**. Countries with noticeable reductions for the value of this measure include **El Salvador, Nigeria, Yemen (2017), Myanmar (2012), Kyrgyzstan, Iraq (2015, 2016, 2017), Barbados, Trinidad and Tobago, Seychelles (2017), Turks and Caicos Islands (70s to early 2000s) and Bermuda**, which stills shows some of the highest GDP per capita in the world, even if reduced by ~40%. But the most dramatic case is the one for **Venezuela (2017)**, which sees its value virtually destroyed by the reestimation: it is now 5% of the value from v9.1 (x0.05).

# **Expenditure-side real GDP per capita (gdppc_e)** compared by country:

# +
fig = px.scatter(pwt910_owid_0, x="gdppc_e", y="gdppc_e_vs", 
                 hover_data=['entity', 'year'], opacity=0.5, color='entity', 
                 title="Expenditure-side real GDP per capita (gdppc_e) comparison: PWT 9.1 vs PWT 10.0",
                 log_x=True,
                 log_y=True,
                 height=600,
                labels={
                     "gdppc_e": "Expenditure-side real GDP per capita (PWT 10.0)",
                     "gdppc_e_vs": "PWT 10.0 / PWT 9.1 (1 = same value)",
                     "entity": "Country"
                 })

fig.update_traces(marker=dict(size=10, line=dict(width=0, color='blue')))
fig.show()
# -

# For the expenditure-side GDP pc, there is a similar picture, but not identical. Corrections for **Mauritania** are the highest (~2x), followed by observations in **Niger, Liberia, Zimbabwe, Iraq, Paraguay, Fiji and Equatorial Guinea** (around 1.5x). The most evident decreases are in **El Salvador, Nigeria, Myanmar (2012, 2017), Iraq (2015, 2016, 2017), Barbados (1992, 1993) and Trinidad and Tobago** and above all **Venezuela in 2016 and 2017**.

# **Productivity** compared by country:

# +
fig = px.scatter(pwt910_owid_0, x="productivity", y="productivity_vs", 
                 hover_data=['entity', 'year'], opacity=0.5, color='entity', 
                 title="Productivity comparison: PWT 9.1 vs PWT 10.0",
                 log_x=True,
                 log_y=True,
                 height=600,
                 labels={
                     "productivity": "Productivity (PWT 10.0)",
                     "productivity_vs": "PWT 10.0 / PWT 9.1 (1 = same value)",
                     "entity": "Country"
                 })

fig.update_traces(marker=dict(size=10, line=dict(width=0, color='blue')))
fig.show()
# -

# In the case of productivity most of the values seem to have increased in the 10%-20% range. For **Myanmar** they have increased by 20%, 40% and even 60%, **Bulgaria** shows values in the nineties increased by around 50%. Around the 40% increase there is **Cambodia, Indonesia and Argentina** in recent years. On the other side, the more noticeable reductions are around 0.9x, so it seems not problematic.

# **Real GDP per capita in 1960 (expenditure-side)** compared by country:

# +
fig = px.scatter(pwt910_owid_0, x="rgdpe_60", y="rgdpe_60_vs", 
                 hover_data=['entity'], opacity=0.5, color='entity', 
                 title="Real GDP per capita in 1960 at chained PPPs comparison: PWT 9.1 vs PWT 10.0",
                 log_x=True,
                 log_y=True,
                 height=600,
                labels={
                     "rgdpe_60": "1960 Real GDP per capita PPP (PWT 10.0)",
                     "rgdpe_60_vs": "PWT 10.0 / PWT 9.1 (1 = same value)",
                     "entity": "Country",
                 })

fig.update_traces(marker=dict(size=10, line=dict(width=0, color='blue')))
fig.show()
# -

# Most of the data for 1960 seems to be corrected around 1.1x. The most notable corrections are for **Mauritania (1.8x), Niger (1.5), Burkina Faso,  Paraguay (1.3x), Nigeria (0.5x) and El Salvador (0.4x)**

# **Average real GDP per capita growth from 1960** compared by country:

# +
fig = px.scatter(pwt910_owid_0, x="gdppc_o_growth", y="gdppc_o_growth_vs", 
                 hover_data=['entity', "Average real GDP per capita growth 1960-2017, chained PPPs in 2011 US$ (PWT 9.1 (2019))"],
                 opacity=0.5, color='entity', 
                 title="Average real GDP per capita growth 1960-2017 (2019), chained PPPs comparison: PWT 9.1 vs PWT 10.0",
                 log_x=False,
                 log_y=False,
                 height=600,
                labels={
                     "gdppc_o_growth": "Average real GDP per capita growth 1960-2019, chained PPPs (PWT 10.0)",
                     "gdppc_o_growth_vs": "PWT 10.0 / PWT 9.1 (1 = same value)",
                     "entity": "Country",
                    "Average real GDP per capita growth 1960-2017, chained PPPs in 2011 US$ (PWT 9.1 (2019))": "Average real GDP per capita growth 1960-2017, chained PPPs (PWT 9.1)",
                 })

fig.update_traces(marker=dict(size=10, line=dict(width=0, color='blue')))
fig.show()
# -

# Differences in growth from 1960 are notable for **Guinea, Togo, Benin, El Salvador, Qatar, Barbados, Antigua and Barbuda (around 2x more in PWT 10.0), Cayman Islands (4x) and Nigeria (5x)**. The reductions are concentrated in **Liberia, Belize, Algeria, Burundi, Sin Maarten (Dutch), Haiti (0.2x-0.4x), Montserrat (0.1x) and Nicaragua (0.04x)**. But there are also examples where the estimated ratio is negative (the growth is negative in one of the PWT): **Venezuela** shows a value of -113.5x, because for PWT 9.1 the average growith for this country was 0.05% and for PWT 10.0 it is -5%. **Chad** is also in this situation with a value for V10.0 of -22x PWT 9.1. Other countries with smaller negative values include **Zimbabwe (-4.5x), Bahamas (-3.3x), Gambia (2.9x), Ukraine, Kyrgysztan, Brunei and Madagascar (0 to -1x)**.
#
# Bosnia and Herzegovina shows a higher growth than the rest, but it is mostly because it is a more recent country with less observations (29) and less variance.

# **Ratio of exports and imports to GDP (%)** compared by country:

# +
fig = px.scatter(pwt910_owid_0, x="ratio", y="ratio_vs", 
                 hover_data=['entity', 'year'], opacity=0.5, color='entity', 
                 title="Ratio of exports and imports to GDP (%) comparison: PWT 9.1 vs PWT 10.0",
                 log_x=True,
                 log_y=True,
                 height=600,
                labels={
                     "ratio": "Ratio of exports and imports to GDP (%) (PWT 10.0)",
                     "ratio_vs": "PWT 10.0 / PWT 9.1 (1 = same value)",
                     "entity": "Country"
                 })

fig.update_traces(marker=dict(size=10, line=dict(width=0, color='blue')))
fig.show()
# -

# Most of the ratios stay similar between PWT 9.1 and 10.0, but there are some cases to note, as **Myanmar** in 1992, where the Ratio in the last version increased by 11 times, **Djibouti** this factor ranges between 2 and 4, in **Venzuela** it is almost 3 and in **Anguilla** it is 1.8 in 2017. **Grenada, Dominica, Yemen and Gambia** in selected years increased by 1.5x. On the other side the largest decreases are in **Serbia in the nineties, Brazil 1982, Togo 2017 and Sudan 2017**, around 0.6x.

# + tags=[]
fig = px.scatter(pwt910_owid_0, x="world_trade", y="world_trade_vs", 
                 hover_data=['year'], opacity=0.5, 
                 title="World trade (% of GDP) comparison: PWT 9.1 vs PWT 10.0",
                 log_x=True,
                 log_y=True,
                 height=600,
                labels={
                     "world_trade": "World trade (% of GDP) (PWT 10.0)",
                     "world_trade_vs": "PWT 10.0 / PWT 9.1 (1 = same value)",
                     "entity": "Country"
                 })

fig.update_traces(marker=dict(size=10, line=dict(width=0, color='blue')))
fig.show()
# -

# Because of the aggregation of the world trade indicator the changes are not as noticeable as the ones in previous graphs and the ratio between v9.1 and v10.0 ranges between 0.99 (2003) and 1.05 (2017)

# ## Appendix

# ### The changes in PWT 10.0
# According to [(2)](https://www.rug.nl/ggdc/docs/pwt100-user-guide-to-data-files.pdf), in its variables and their construction, version 10 **"closely resembles PWT versions 8.0, 8.1, 9.0
# and 9.1"**. The changes from 9.1 to 10 include **"new relative price data, extended and revised
# national accounts data, revisions to how we estimate employment data and a modification to the methodology for estimating investment by asset"**.
#
# According to [(3)](https://www.rug.nl/ggdc/docs/pwt100-whatsnew.pdf), comparing with the 8.0 version (the last big change in the dataset) **"the main structure of the database and definition of its variables are unchanged in PWT 10.0"**. The changes fall in four broad categories:
# 1. *The incorporation of new purchasing power parities (PPPs) data for most countries for the years 2011 to 2017*
#     
#     PWT 10.0 adds revised ICP benchmarks for 2011, new benchmarks for 2017 and interpolated benchmarks for 2012-2016. Price levels for the expenditure categories are revised substantially. v9.1 interpolated the 2011 ICP benchmark for 2017 and for v10 they rely on direct ICP benchmark for nearly all countries, also replacing 2014 OECD and 2011-2017 Eurostat benchmarks. All of these changes lead to a higher dispersion in the differences. For years between the 2011 and 2017 ICP benchmarks, they rely on interpolations by the World Bank. Corrections to the GDP expenditure composition also result in additional adjustments clearer than household consumption in 2017.
#     
#     With the incorporation of the 2017 ICP data, the reference year has changed from 2011 in v9.0 and 9.1 to 2017 in v10.
#     
#     
# 2. *The incorporation of revised and extended National Accounts data, covering the period up to 2019*
#
#     (1) mainly affects price levels, the new National Accounts data mainly affects nominal GDP levels and real growth rates. These revisions are commonly observed for African nations, but also in Latin America, the Caribban and Middle East (Paraguay, Niger and Djibouti are highlighted. It is mentioned in the document that these revisions are both welcome and alarming, because they reflect the effort made the national agencies, but also underscore the uncertainty about the true size of some economies.
#     
#     
# 3. *Revisions to how we estimate employment data, in particular for low and middle-income countries*
#     
#     v10.0 makes substantial changes to the source data for employment, modifies the link procedure used to combine the employment estimate from different sources. They incorporated more up-to-date information and evaluated the comparability of sources, which leads to the improved the estimates for a few dozen African, South/South-East Asian and Latin American countries. Revisions to the employment data in their original sources also alter the estimates for some countries, especially for more recent years. More details about the use of sources in pages 5 and 6.
#     
#     
# 4. *A modification to the methodology for estimating investment by asset*
#
#     They adjusted the linking between National Account statistics dereived from the Total Economy Database and estimates using the Commodity-flow method (CFM). Argentina is shown as one of the more severe revisions, but in general the impact is for about 30 countries.
#     
# Other changes are:
# - They replaced the exchange rate [xr] for Sudan for the years 1970 to 2019 with estimates from the World Bank’s World Development Indicators. This predominantly affects the Sudanese level of real GDP at current PPPs, and variables depending on these estimates (i.e. [ctfp]).
# - They replaced the ICP benchmarks for the years 1996 and 2005 with benchmarks from Eurostat and the OECD whenever available. This resolved spikes in price levels for several European countries (notably GBR) and revised growth rates of price levels between 1985 and 1996 for several OECD countries.
# - They updated PWT 10.0 due to an error in the current value of GDP [v_gdp] for their alternative time-series of China. Note that the variables relying on current GDP (e.g. [cgdpo], [rgdpo], etc.) as well as the reported price levels, were also affected by this revision for CHN.
# - New TFP estimates: New employment and investment data has allowed them to extend TFP estimates for several countries: BWA, IDN, MUS, NAM, UZB, ZMB.
# - New output/expenditure estimates: A new 2017 PPP benchmark for GUY allowed them to include this country in PWT 10.0.
# - Update human capital [hc]: update from Barro and Lee v. 2.0 to 2.2. Revisions for CHN and DOM.
# - Revision capital services [rkna]: fixed an issue in PWT 9.1, where the implied capital compensation ([k] / [ucc]) did not always equal (1-[labsh]) * [gdp]. This fix solves several breaks in [rkna], most notably for CZE, LVA, ROU and RUS.
# - Revision price level capital stocks [pl_n]: fixed an issue in PWT 9.1, where the price level for capital stocks was always equal to the price level for GDP [pl_gdpo] for the USA. The price level for the USA is now estimated using asset-specific PPPs weighted by nominal capital stocks. It is set to 1 for the USA in the base year 2017.
# - Outliers price levels. They have identified a number of new outliers in the price levels for GDP and Domestic Absorption (DA). They used the criteria discussed at length in the document “Outliers in PWT8.0”, available on the PWT website. In short, price levels for [cgdpo] and [cda] are marked an outlier if the price level is extrapolated from the first or last available benchmark and the observed level exceeds the bounds of a predicted level, based on an OLS regression of the log of GDP per capita and the log price level of GDP and DA respectively. New outliers were identified for one or more years for ABW, ALB, ARM, ATG, BGR, BLR, CYM, IRQ, OMN, SDN, SXM, TGO, TJK, VEN. Some of the outliers identified in PWT 9.0 and 9.1 were no longer identified as such. Consult the [i_outlier] variable for further details.

# ### The variables of PWT
# In the documents [(2)](https://www.rug.nl/ggdc/docs/pwt100-user-guide-to-data-files.pdf) and [(3)](https://www.rug.nl/ggdc/docs/pwt100-whatsnew.pdf) is recommended to check the document [(4)](https://www.rug.nl/ggdc/productivity/pwt/related-research-papers/the_next_generation_of_the_penn_world_table.pdf) to see the variables that are published in the Penn World Tables. Although this paper refers to v8.1, there has not been major changes to the list. You can find below the list of key variables of PWT:

# ![PWT%20variables%201.jpg](attachment:PWT%20variables%201.jpg)

# ![PWT%20variables%202.jpg](attachment:PWT%20variables%202.jpg)

# ### Exploratory Data Analysis
#
# Although in the documents it is stated that both versions 9.1 and 10 are virtually the same in terms of the list of variables, it is necessary to check this with the actual datasets

# +
import pandas as pd
from pathlib import Path
import seaborn as sns
import numpy as np
import plotly.express as px

#Loading PWT 9.1
pwt9_path = Path('data/pwt91.xlsx')
pwt9 = pd.read_excel(pwt9_path,sheet_name='Data')
pwt9
# -

#Loading PWT 10.0
pwt10_path = Path('data/pwt100.xlsx')
pwt10 = pd.read_excel(pwt10_path,sheet_name='Data')
pwt10

# They have the same number of columns and the number of rows in PWT 10.0 is larger than in PWT 9.1, which is a good sign to think they have the same variables with new data for countries and years in PWT 10.0.
#
# This is obviously not enough, so I get a list of the variables from both datasets

list_pwt9 = list(pwt9)
list_pwt9

list_pwt10 = list(pwt10)
list_pwt10

# These two lists can be compared by using the `==` operator: 

list_pwt9 == list_pwt10

# The equality is true so it can be said that both datasets have the same variables and with the same order. If the result was false it would be necessary to order them first to confirm the equality:

list_pwt9_ordered = list_pwt9.sort()
list_pwt10_ordered = list_pwt10.sort()
list_pwt9_ordered == list_pwt10_ordered

# A join of both dataset is generated for a quick comparison between their variables

pwt9['version'] = "9.1"
pwt10['version'] = "10.0"
#pwt9_10 = pwt9.append(pwt10, ignore_index=True)
pwt9_10 = pd.concat([pwt9, pwt10], ignore_index=True)

# The `seaborn` library allows to plot pairwise relations in a dataset:

# - [pairplot documentation](https://seaborn.pydata.org/generated/seaborn.pairplot.html)
# - [PairGrid documentation](https://seaborn.pydata.org/generated/seaborn.PairGrid.html#seaborn.PairGrid)

# For instance, this way the differences in real and constant GDP each year can be plotted:

# +
#sns.pairplot(pwt9_10, x_vars='year',y_vars=['rgdpe','rgdpo', 'cgdpe', 'cgdpo'], 
#             hue = "version", height=5, aspect=3, kind="scatter", dropna=True)
# -

# The rest of the variables can also be plotted against `year`:

# +
#sns.pairplot(pwt9_10, x_vars='year', hue = "version", height=5, aspect=3)
# -

# It is clear that most variables change and not only for the most recent years, but for the entire time frame. The variables that don't change (much) are:
# - pop
# - emp
# - hc
# - xr (with outlier)
# - statcap




