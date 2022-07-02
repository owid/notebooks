
# %%
# ––––––––– SET UP –––––––––––
# ---- Import libraries ------
# Here we provide details of which libraries and packages we use to prepare the data

# Markdown lets us use variables within markdown chunks.
from operator import index
from IPython.display import Markdown as md

#Pablo: I got a warning of the previous import being deprecated. With this I have no warnings:
from IPython.display import IFrame

# Pandas is a standard package used for data manipulation in python code
import pandas as pd

# This package allows us to import the original Excel file via a URL
import requests

# This package allows us to save a temporary file of the orginal data file
import tempfile

# Pathlib is a standard package for making it easier to work with file paths
from pathlib import Path

# Seaborn is a Python data visualization library (based on matplotlib)
#import seaborn as sns

# NumPy is a standard package that provides a range of useful mathematical functions 
import numpy as np

# Plotly is a package for creating interactive charts
import plotly.express as px
import plotly.io as pio
pio.renderers.default='notebook'

# boto3  allows us to write data to our s3 cloud storage
import boto3

# Keys for accessing s3
from joes_key import ENDPOINT, KEY_ID, SECRET_KEY 

# Dataset metadata is defined in dataset_metadata.py
from metadata.dataset_metadata import dataset_meta

# Variable metadata is defined in another script in variable_metadata.py
from metadata.variable_metadata import variable_meta

# Function to standardize entities from mapping file
from scripts.harmonize import standardize_entities


# %%
# Set up access for writing files to s3  
session = boto3.session.Session()

client = session.client('s3',
                        endpoint_url="https://{}.digitaloceanspaces.com".format(ENDPOINT),
                        aws_access_key_id=KEY_ID,
                        aws_secret_access_key=SECRET_KEY)


# %%
# Load the 'harmonized' data (i.e with standardized country names)
# – For the time being, this is stored in Joe's Digital Ocean account.

url = 'https://joeh.fra1.digitaloceanspaces.com/pwt/harmonized.csv'

df = pd.read_csv(url)


# –––––––– TEXT BEGINS ––––––––

# %% [markdown]
# # Data document: Penn World Tables


# %%
#Print the metadata as markdown
md("**Last updated:**  {} <br><br>\
    **Expected data of next update:**  {} <br><br>\
    {}"\
    .format(dataset_meta["dateRetrieved"],
            dataset_meta["nextUpdate"],
            dataset_meta["description"]))


# %% [markdown]
# """
# *This article describes the data in the Penn World Tables version 10.0 
# and documents how Our World in Data have handled and transformed this data 
# in order to make use of it in our publication.*
# <br><br>
# *This article is an unsual, experimental format, which we have designed 
# to make our data work more transparent and reusable.*
# <br><br>
# *To prepare the data for use in our publication we write and then execute
#  a computer programme. Within that computer programme we include extensive 
#  notes, explanations and visualizations to make any choices concerning the 
#  treatment of the data more visible and to explain our reasoning. 
#  This article is a web version of that computer programme in which 
#  priority is given to the notes and explanations and much of the code 
#  is hidden or not shown to improve readability. You can read this 
#  article whether or not you are familiar with (python) code in order 
#  to understand more about the Penn World Tables and our treatment of the data.*
# <br><br>
# *The full code we use to prepare this data can be found in here GitHub. (provide link)*
# """
#




# %% [markdown]
# ## Sourcing and initial preparation of the data
# %%
md("We downloaded the orginal data from {} on {}."\
    .format(dataset_meta["link"],
            dataset_meta["dateRetrieved"]))



# %% [markdown]
# Our World in Data standardizes country names to allow us to compare data across different data sources.
#
# * The mapping of country names we applied to the Penn World Tables is [here in GitHub](https://github.com/owid/notebooks/blob/main/BetterDataDocs/PabloArriagada/pwt/country_standardization_mapping.csv).
# * You can find the code used to implement this step [here in GitHub](https://github.com/owid/notebooks/blob/main/BetterDataDocs/PabloArriagada/pwt/scripts/harmonize.py).





# %%
# ––––– DISCUSSION OF VARIABLES –––––––––––

# %% [markdown]
# ## Which data series do we use and how do we prepare them?

# %%
# JH comment: See [Diana's Google Doc](https://docs.google.com/document/d/1Kg9ZqxXXfDWA7WxfDysB0GjwlQ6kK5x6kNP-m7Sjl-I/edit?pli=1#heading=h.3iglji7a4k32) for a previous attempt at this*


# %% [markdown]
# ### GDP and GDP per capita


# %% [markdown]
"""
*JH comment: Joe is drafting here an explanation of the different approaches to prices that define the different GDP variables.*
<br><br>
The Penn World Tables provides five different measures of GDP over time.
<br><br>
They produce these different series... [explain about prices].
<br><br>
* Joe's notes:
The point it if you want to compare across countries and over time then you can't have everything:*
> "Diewert (1999) and Van Veelen (2002) have argued that no multilateral measure of real GDP can satisfy all the axioms we might like, so there are tradeoffs involved with any construction of this concept."
<br><br>
PWT provide different measures for different purposes, in two different dimensions:

 1. Expenditure vs Production*
 2. Constant vs current prices vs NA growth rates
<br><br>
 * (1) is basically about the terms of trade: only if your terms of trade are especially favourable or especially bad will there be much difference between Expenditure and Output measures.
 * The issue with (2) is this: Because price structures change over time, cross-country benchmarks 
  for two periods typically won't be consistent with nationally measured 
  inflation in each country. If you want to compare prices across place
 and time, then you need to fudge this somehow. `rgdp(e/o)` is such a fudge:
  They take the benchmark years as gospel and then make the national inflation 
  fit somehow with that. `cgdp(e/o)` instead takes only the latest benchmark and
  then applies national inflation. For this reason it is better for looking 
  at trends in one country over time, but not so much for cross-country differences
   over time. `gdpna` applies NA growth rates (I don't yet get why this is different – 
   because pwt are using a different series for inflation than the NA GDP deflator?)

<br><br>
You can read more about prices in our post here. (Joe to write this at some point in the future)
<br><br>
To calculate GDP per capita in each case, we divide the GDP variables by the 
population data given in the same dataset.
"""

# %%
#Pablo: Once the df_harmonized dataframe is defined there's no need to use the df_original in these formulas.
#We just define df_harmonized['xxxx'] = df_harmonized['xxxx']*1000000


# –––– Construct absolute GDP variables –––––
#The original data is given in millions of dollars.
# We multiply the variable by 1,000,000 to give the figures in dollars.
df['rgdpe'] = df['rgdpe']*1000000
df['rgdpo'] = df['rgdpo']*1000000
df['cgdpe'] = df['cgdpe']*1000000
df['cgdpo'] = df['cgdpe']*1000000
df['rgdpna'] = df['rgdpna']*1000000


# –––– Construct GDP per capita variables –––––
# GDP per capita is GDP divided by popultion (both are given in millions)
df['rgdpe_pc'] = df['rgdpe']/df['pop']
df['rgdpo_pc'] = df['rgdpo']/df['pop']
df['cgdpe_pc'] = df['cgdpe']/df['pop']
df['cgdpo_pc'] = df['cgdpe']/df['pop']
df['rgdpna_pc'] = df['rgdpna']/df['pop']


# %% [markdown]
"""
For most countries, the diferences between the different series for GDP are 
relatively small. For instance here we see GDP per capita according to the five different 
definitions plotted for United States.
<br><br>
Countries where these measures differ significantly tend to be/have... [explain]
<br><br>
*JH comment: This would be a good place to put a link to an 'auxiliary notebook' where 
we look in more detail where the measures differ.*
"""
# %%
selected_country = 'United States'
fig = px.line(df[df['country']== selected_country],
             x='year', 
             y=['rgdpe_pc','rgdpo_pc','cgdpe_pc', 'cgdpo_pc', 'rgdpna_pc'],
             title="Comparison of PWT GDP per capita measures, " + selected_country)
fig.show()



# %%




# %%
# --- Employment and labour productivity variables ––––


# %%
# --- Components of GDP variables ––––

# %%
#Here I'm selecting the UK, summing all the csh variables and tabulating the basic stats of the sum
df_uk = df[df['country']== "United Kingdom"].reset_index()
column_names = ['csh_c', 'csh_i', 'csh_g', 'csh_r', 'csh_x', 'csh_m']
df_uk['sum'] = df_uk[column_names].sum(axis=1)
df_uk[['sum']].describe()

# %%
# Here I gather net exports and the residual into a single series
df['csh_nx_and_r'] = df['csh_x'] + df['csh_m'] + df['csh_r']

# And then plot the components of GDP as a stacked area 
# (note that `csh_nx_and_r` is often negative – i.e. a trade deficit).

selected_country = 'United Kingdom'

df_stacked_area = df[df['country']== selected_country]
df_stacked_area = df_stacked_area[['year','csh_c', 'csh_i', 'csh_g', 'csh_nx_and_r']]

df_stacked_area = df_stacked_area.reset_index()
df_stacked_area = pd.melt(df_stacked_area, id_vars='year', value_vars=['csh_c', 'csh_i', 'csh_g', 'csh_nx_and_r'])


fig = px.area(df_stacked_area,
             x='year', 
             y='value',
             color="variable",
             title="Components of GDP, " + selected_country)
             
fig.show()





# %%
# --- Trade variables––––



# %%
# --- Total Factor Productivity variables ––––


# %%
# --- Other variables ––––




# %% [Markdown]
# As well as GDP per capita, we derive other variables from the GDP data, as listed in the collapsed section here.

# %% [Markdown] 
# # A list of all variables we derive from Penn World Tables

# ### GDP per capita
# %%
# –– # GDP per capita (expenditure, multiple price benchmarks)
# %%
md("#### {}"\
    .format(variable_meta['rgdpe_pc']['name']))
# %%
md("{}"\
    .format(variable_meta['rgdpe_pc']['description']))


# %%
IFrame(src='https://ourworldindata.org/grapher/real-gdp-per-capita-PennWT', width='100%', height='600')



# –– # GDP per capita (output, multiple price benchmarks)
# %%
#Pablo: this is the recommended function, I have warnings with the other (see also the import in the first cell) 
IFrame(src='https://ourworldindata.org/grapher/real-gdp-per-capita-PennWT', width='100%', height='600')

# %%
md("#### {}"\
    .format(variable_meta['rgdpo_pc']['name']))
# %%
md("{}"\
    .format(variable_meta['rgdpo_pc']['description']))


# %%
IFrame(src='https://ourworldindata.org/grapher/real-gdp-per-capita-PennWT', width='100%', height='600')




# –– # GDP per capita (expenditure, single price benchmark)
# %%
md("#### {}"\
    .format(variable_meta['cgdpe_pc']['name']))
# %%
md("{}"\
    .format(variable_meta['cgdpe_pc']['description']))


# %%
IFrame(src='https://ourworldindata.org/grapher/real-gdp-per-capita-PennWT', width='100%', height='600')



# –– # GDP per capita (output, single price benchmark)
# %%
md("#### {}"\
    .format(variable_meta['cgdpo_pc']['name']))
# %%
md("{}"\
    .format(variable_meta['cgdpo_pc']['description']))


# %%
IFrame(src='https://ourworldindata.org/grapher/real-gdp-per-capita-PennWT', width='100%', height='600')




# –– # GDP per capita (national accounts)
# %%
md("#### {}"\
    .format(variable_meta['rgdpna_pc']['name']))
# %%
md("{}"\
    .format(variable_meta['rgdpna_pc']['description']))


# %%
IFrame(src='https://ourworldindata.org/grapher/real-gdp-per-capita-PennWT', width='100%', height='600')


# %% [markdown]
# ### Total GDP



# %%
# –– # GDP (expenditure, multiple price benchmarks)
# %%
md("#### {}"\
    .format(variable_meta['rgdpe']['name']))
# %%
md("{}"\
    .format(variable_meta['rgdpe']['description']))


# %%
IFrame(src='https://ourworldindata.org/grapher/real-gdp-per-capita-PennWT', width='100%', height='600')



# –– # GDP (output, multiple price benchmarks)
# %%
md("#### {}"\
    .format(variable_meta['rgdpo']['name']))
# %%
md("{}"\
    .format(variable_meta['rgdpo']['description']))


# %%
IFrame(src='https://ourworldindata.org/grapher/real-gdp-per-capita-PennWT', width='100%', height='600')




# –– # GDP (expenditure, single price benchmark)
# %%
md("#### {}"\
    .format(variable_meta['cgdpe']['name']))
# %%
md("{}"\
    .format(variable_meta['cgdpe']['description']))


# %%
IFrame(src='https://ourworldindata.org/grapher/real-gdp-per-capita-PennWT', width='100%', height='600')



# –– # GDP (output, single price benchmark)
# %%
md("#### {}"\
    .format(variable_meta['cgdpo']['name']))
# %%
md("{}"\
    .format(variable_meta['cgdpo']['description']))


# %%
IFrame(src='https://ourworldindata.org/grapher/real-gdp-per-capita-PennWT', width='100%', height='600')




# –– # GDP (national accounts)
# %%
md("#### {}"\
    .format(variable_meta['rgdpna']['name']))
# %%
md("{}"\
    .format(variable_meta['rgdpna']['description']))


# %%
IFrame(src='https://ourworldindata.org/grapher/real-gdp-per-capita-PennWT', width='100%', height='600')



# %% [markdown]
# ## **All charts using this dataset on Our World in Data**
"""
*JH comment: The idea is that we could have an 'all charts' block – but where 
the tag is the dataset. I don't know if that will be possible with. It could just be 
(automatically generated) list of links.
"""


# %% [markdown]
# # Appendix
"""
Here we provide links to further documentation of the Penn World Tables data 
and our treatment of it. 
#
* A comparison of version 10.0 with a previous release of the data (JH comment: Pablo, at some point let's add this as an 'auxiliary notebook')
* A list of further documentation discussing various vintages of the dataset can be found at the [Groningen Growth and Development Centre's website](https://www.rug.nl/ggdc/productivity/pwt/pwt-documentation). 
"""





# %%

