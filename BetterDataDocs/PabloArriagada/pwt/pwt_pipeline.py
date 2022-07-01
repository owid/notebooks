
# %% [markdown]
# # Data document: Penn World Tables
# %%
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



# %%
# Set up access for writing files to s3  
session = boto3.session.Session()

client = session.client('s3',
                        endpoint_url="https://{}.digitaloceanspaces.com".format(ENDPOINT),
                        aws_access_key_id=KEY_ID,
                        aws_secret_access_key=SECRET_KEY)



# %%
# -------- Introduction ----------

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
# ## About this data

# %%
#Print the metadata as markdown
md("**Last updated:**  {} <br><br>\
    **Expected data of next update:**  {} <br><br>\
    {}"\
    .format(dataset_meta["dateRetrieved"],
            dataset_meta["nextUpdate"],
            dataset_meta["description"]))




# %% [markdown]
# ## Details about how we source and prepare the original data
# %%
md("We downloaded the orginal data from {} on {}."\
    .format(dataset_meta["link"],
            dataset_meta["dateRetrieved"]))




# %%
# ------- Load the data –––––––––

#Here we have stored the original Excel file in GitHub
url = 'https://joeh.fra1.digitaloceanspaces.com/pwt/pwt100-original.xlsx'

#We load it, via a temporary file 
# *Pablo comment: Maybe this is not needed, because the file can be loaded by using the url variable instead of tempf
# The file is downloaded once and then it is on the memory as a dataframe
# Please tell me if you have something else in mind with the library
r = requests.get(url)
tempf = tempfile.TemporaryFile()
tempf.write(r.content)

df_original = pd.read_excel(tempf, sheet_name='Data')


# %%
# ––––––––– Standardize country names ––––––––––


# %% [markdown]
# Our World in Data standardizes country names to allow us to compare data across different data sources.
# %%
# *JH comment: Pablo, can you add the country harmonization step here please (df_harmonized is the df with standardized country names)*
# *Pablo comment: the country harmonization process I know is the one from the web portal, that's why I left it like that in the original notebook
# https://owid.cloud/admin/standardize
# *If there's a command to do this we need to ask

df_harmonized = df_original.copy()

# I couldn't find a solution for writing to a tempfile csv that worked with the boto3 upload. So
# I take the roundabout root of creating a temp directory and adding the file to that.
temp_folder_for_data = tempfile.TemporaryDirectory()

# Write a csv to the temp folder
df_harmonized.to_csv(f'{temp_folder_for_data.name}/harmonized.csv', index=False)
# Upload to Digital Ocean – pwt bucket
client.upload_file(f'{temp_folder_for_data.name}/harmonized.csv',  # Path to local file
                   'pwt',  # Name of Space 
                   'harmonized.csv', # Name for remote file
                   ExtraArgs={'ACL':'public-read'})  # specify file is public


# %% [markdown]
# Click here to see a table of how we mapped country names.
#
# *JH comment: Pablo, please provide a table of the country name mapping here*


# %%
# Inspect the resulting dataframe.
#df_harmonized.head()



# %%
# ––––– CONSTRUCTION AND DISCUSSION OF INDIVIDUAL VARIABLES –––––––––––

# %% [markdown]
# ## A summary of each variable
#
# *JH comment: See [Diana's Google Doc](https://docs.google.com/document/d/1Kg9ZqxXXfDWA7WxfDysB0GjwlQ6kK5x6kNP-m7Sjl-I/edit?pli=1#heading=h.3iglji7a4k32) for a previous attempt at this*


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
df_harmonized['rgdpe'] = df_original['rgdpe']*1000000
df_harmonized['rgdpo'] = df_original['rgdpo']*1000000
df_harmonized['cgdpe'] = df_original['cgdpe']*1000000
df_harmonized['cgdpo'] = df_original['cgdpe']*1000000
df_harmonized['rgdpna'] = df_original['rgdpna']*1000000


# –––– Construct GDP per capita variables –––––
# GDP per capita is GDP divided by popultion (both are given in millions)
df_harmonized['rgdpe_pc'] = df_harmonized['rgdpe']/df_harmonized['pop']
df_harmonized['rgdpo_pc'] = df_harmonized['rgdpo']/df_harmonized['pop']
df_harmonized['cgdpe_pc'] = df_harmonized['cgdpe']/df_harmonized['pop']
df_harmonized['cgdpo_pc'] = df_harmonized['cgdpe']/df_harmonized['pop']
df_harmonized['rgdpna_pc'] = df_harmonized['rgdpna']/df_harmonized['pop']


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
fig = px.line(df_harmonized[df_harmonized['country']== selected_country],
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
# *JH comment: The components don't sum to 100%. We should understand why that is 
# the case. Is it not the case that `csh_r` equals net exports plus discrepancy? 

# Pablo: They actually do, but it is not possible to show a stable 100% sum in this stacked area chart
#because of the negative values: they just intersect the other areas.
#I see csh_r is not net exports plus discrepancy, because actually the sum of all the csh variables
#(including _x and _m) is 1:

#Here I'm selecting the UK, summing all the csh variables and tabulating the basic stats of the sum
df_uk = df_harmonized[df_harmonized['country']== "United Kingdom"].reset_index()
column_names = ['csh_c', 'csh_i', 'csh_g', 'csh_r', 'csh_x', 'csh_m']
df_uk['sum'] = df_uk[column_names].sum(axis=1)
df_uk[['sum']].describe()

# %%

selected_country = 'United Kingdom'

df_stacked_area = df_harmonized[df_harmonized['country']== selected_country]
df_stacked_area = df_stacked_area[['year','csh_c', 'csh_i', 'csh_g', 'csh_r']]

df_stacked_area = df_stacked_area.reset_index()
df_stacked_area = pd.melt(df_stacked_area, id_vars='year', value_vars=['csh_c','csh_i', 'csh_g', 'csh_r'])


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

