# %%
# ---- Import libraries ------
# Here we provide details of which libraries and packages we use to prepare the data

# Markdown lets us use variables within markdown chunks.
from IPython.display import Markdown as md

# This allows us to embed iframes in the output of the code cells.
from IPython.core.display import display, HTML

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
#import plotly.express as px
#import plotly.io as pio



# %%
# ------- Dataset metadata ---------
# Create a 'dictionary' (an array whose elements are named) for the dataset metadata
# This will end up in e.g. our database, 'Sources' tab etc.
dataset_meta = {}

# %%
# Add dataset metadata to dictionary
dataset_meta['name'] = "Penn World Tables version 10.0"
dataset_meta['sourceName'] = "Penn World Tables"
dataset_meta['link'] = "https://www.rug.nl/ggdc/productivity/pwt"
dataset_meta['description'] = "PWT version 10.0 is a database with information \
    on relative levels of income, output, input and productivity, covering 183 \
    countries between 1950 and 2019."
dataset_meta['dateRetrieved'] = "dd/mm/2022"
dataset_meta['nextUpdate'] = "Unknown"


# %%
# ------- Variable metadata ---------

# Create a dictionary for the variable metadata
# This will be a dictionary of dictionaries – one for each variable 
variable_meta = {}

# ---- GDP variables ------

# GDP (expenditure, multiple price benchmarks)
variable_meta['rgdpe'] = {}

variable_meta['rgdpe']['name'] = "GDP (expenditure, multiple price benchmarks)"
variable_meta['rgdpe']['displayName'] = "GDP"
variable_meta['rgdpe']['unitsLong'] = "International-$ at 2017 prices"
variable_meta['rgdpe']['unitsShort'] = "$"
variable_meta['rgdpe']['description'] = "[Long description here]"


# GDP (output, multiple price benchmarks)
variable_meta['rgdpo'] = {}

variable_meta['rgdpo']['name'] = "GDP (output, multiple price benchmarks)"
variable_meta['rgdpo']['displayName'] = "GDP"
variable_meta['rgdpo']['unitsLong'] = "International-$ at 2017 prices"
variable_meta['rgdpo']['unitsShort'] = "$"
variable_meta['rgdpo']['description'] = "[Long description here]"



# GDP (expenditure, single price benchmark)
variable_meta['cgdpe'] = {}

variable_meta['cgdpe']['name'] = "GDP (expenditure, single price benchmark)"
variable_meta['cgdpe']['displayName'] = "GDP"
variable_meta['cgdpe']['unitsLong'] = "International-$ at 2017 prices"
variable_meta['cgdpe']['unitsShort'] = "$"
variable_meta['cgdpe']['description'] = "[Long description here]"


# GDP (expenditure, single price benchmark)
variable_meta['cgdpo'] = {}

variable_meta['cgdpo']['name'] = "GDP (output, single price benchmark)"
variable_meta['cgdpo']['displayName'] = "GDP"
variable_meta['cgdpo']['unitsLong'] = "International-$ at 2017 prices"
variable_meta['cgdpo']['unitsShort'] = "$"
variable_meta['cgdpo']['description'] = "[Long description here]"


# GDP (using national accounts growth rates)
variable_meta['rgdpna'] = {}

variable_meta['rgdpna']['name'] = "GDP (using national accounts growth rates)"
variable_meta['rgdpna']['displayName'] = "GDP"
variable_meta['rgdpna']['unitsLong'] = "International-$ at 2017 prices"
variable_meta['rgdpna']['unitsShort'] = "$"
variable_meta['rgdpna']['description'] = "[Long description here]"



# ---- GDP per capita variables ------

# GDP (expenditure, multiple price benchmarks)
variable_meta['rgdpe_pc'] = {}

variable_meta['rgdpe_pc']['name'] = "GDP per capita (expenditure, multiple price benchmarks)"
variable_meta['rgdpe_pc']['displayName'] = "GDP per capita"
variable_meta['rgdpe_pc']['unitsLong'] = "International-$ at 2017 prices"
variable_meta['rgdpe_pc']['unitsShort'] = "$"
variable_meta['rgdpe_pc']['description'] = "[Long description here]"


# GDP (output, multiple price benchmarks)
variable_meta['rgdpo_pc'] = {}

variable_meta['rgdpo_pc']['name'] = "GDP per capita (output, multiple price benchmarks)"
variable_meta['rgdpo_pc']['displayName'] = "GDP per capita"
variable_meta['rgdpo_pc']['unitsLong'] = "International-$ at 2017 prices"
variable_meta['rgdpo_pc']['unitsShort'] = "$"
variable_meta['rgdpo_pc']['description'] = "[Long description here]"



# GDP (expenditure, single price benchmark)
variable_meta['cgdpe_pc'] = {}

variable_meta['cgdpe_pc']['name'] = "GDP per capita (expenditure, single price benchmark)"
variable_meta['cgdpe_pc']['displayName'] = "GDP per capita"
variable_meta['cgdpe_pc']['unitsLong'] = "International-$ at 2017 prices"
variable_meta['cgdpe_pc']['unitsShort'] = "$"
variable_meta['cgdpe_pc']['description'] = "[Long description here]"


# GDP (expenditure, single price benchmark)
variable_meta['cgdpo_pc'] = {}

variable_meta['cgdpo_pc']['name'] = "GDP per capita (output, single price benchmark)"
variable_meta['cgdpo_pc']['displayName'] = "GDP per capita"
variable_meta['cgdpo_pc']['unitsLong'] = "International-$ at 2017 prices"
variable_meta['cgdpo_pc']['unitsShort'] = "$"
variable_meta['cgdpo_pc']['description'] = "[Long description here]"


# GDP (using national accounts growth rates)
variable_meta['rgdpna_pc'] = {}

variable_meta['rgdpna_pc']['name'] = "GDP per capita (using national accounts growth rates)"
variable_meta['rgdpna_pc']['displayName'] = "GDP per capita"
variable_meta['rgdpna_pc']['unitsLong'] = "International-$ at 2017 prices"
variable_meta['rgdpna_pc']['unitsShort'] = "$"
variable_meta['rgdpna_pc']['description'] = "[Long description here]"



# %%
# -------- Introduction ----------

# %% [markdown]
"""
*This article describes the data in the Penn World Tables version 10.0 
and documents how Our World in Data have handled and transformed this data 
in order to make use of it in our publication.*
#
*This article is an unsual, experimental format, which we have designed 
to make our data work more transparent and reusable.*
#
*To prepare the data for use in our publication we write and then execute
 a computer programme. Within that computer programme we include extensive 
 notes, explanations and visualizations to make any choices concerning the 
 treatment of the data more visible and to explain our reasoning. 
 This article is a web version of that computer programme in which 
 priority is given to the notes and explanations and much of the code 
 is hidden or not shown to improve readability. You can read this 
 article whether or not you are familiar with (python) code in order 
 to understand more about the Penn World Tables and our treatment of the data.*
#
*The full code we use to prepare this data can be found in here GitHub. (provide link)*
"""

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
# #### **All charts of this dataset on Our World in Data**
"""
*JH comment: The idea is that we could have a collapsed 'all charts' block – but where 
the tag is the dataset. I don't know if that will be possible with. It could just be 
(automatically generated) list of links.
"""


# %% [markdown]
# ## Details about how we source and prepare the original data
# %% 
md("We downloaded the orginal data from {} on {}."\
    .format(dataset_meta["link"],
            dataset_meta["dateRetrieved"]))




# %%
# ------- Load the data –––––––––

#Here we have stored the original Excel file in GitHub
url = 'https://raw.githubusercontent.com/owid/notebooks/main/PabloArriagada/pwt/data/pwt100.xlsx'

#We load it, via a temporary file 
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

df_harmonized = df_original


# %% [markdown]
# Click here to see a table of how we mapped country names.

# *JH comment: Pablo, please provide a table of the country name mapping here*


# %%
# Inspect the resulting dataframe.
#df_harmonized.head()



# %%
# ––––– CONSTRUCTION AND DISCUSSION OF INDIVIDUAL VARIABLES –––––––––––

# %% [markdown]
# ## A summary of each variable

# *JH comment: See [Diana's Google Doc](https://docs.google.com/document/d/1Kg9ZqxXXfDWA7WxfDysB0GjwlQ6kK5x6kNP-m7Sjl-I/edit?pli=1#heading=h.3iglji7a4k32) for a previous attempt at this*


# %% [markdown]
# ### GDP per capita


# %% [markdown]

"""
*JH comment: Joe is drafting here an explanation of the different approaches to prices that define the different GDP variables.*
#
The Penn World Tables provides five different measures of GDP over time.
#
They produce these different series... [explain about prices].
#
* Joe's notes:
The point it if you want to compare across countries and over time then you can't have everything:*
> "Diewert (1999) and Van Veelen (2002) have argued that no multilateral measure of real GDP can satisfy all the axioms we might like, so there are tradeoffs involved with any construction of this concept."
#
PWT provide different measures for different purposes, in two different dimensions:

 1. Expenditure vs Production*
 2. Constant vs current prices vs NA growth rates
#
 * (1) is basically about the terms of trade: only if your terms of trade are especially favourable or especially bad will there be much difference between Expenditure and Output measures.
 * The issue with (2) is this: Becasue price structures change over time, cross-country benchmarks 
  for two periods typically won't be consistent with nationally measured 
  inflation in each country. If you want to compare prices across place
 and time, then you need to fudge this somehow. `rgdp(e/o)` is such a fudge:
  They take the benchmark years as gospel and then make the national inflation 
  fit somehow with that. `cgdp(e/o)` instead takes only the latest benchmark and
  then applies national inflation. For this reason it is better for looking 
  at trends in one country over time, but not so much for cross-country differences
   over time. `gdpna` applies NA growth rates (I don't yet get why this is different – 
   because pwt are using a different series for inflation than the NA GDP deflator?)


You can read more about prices in our post here. (Joe to write this at some point in the future)

To calculate GDP per capita in each case, we divide the GDP variables by the 
population data given in the same dataset.

"""

# %% 
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
df_harmonized['rgdpe_pc'] = df_original['rgdpe']/df_original['pop']
df_harmonized['rgdpo_pc'] = df_original['rgdpo']/df_original['pop']
df_harmonized['cgdpe_pc'] = df_original['cgdpe']/df_original['pop']
df_harmonized['cgdpo_pc'] = df_original['cgdpe']/df_original['pop']
df_harmonized['rgdpna_pc'] = df_original['rgdpna']/df_original['pop']

# %% 
# ––– Print variable metadata as markdown and add iframe –––

# –– # GDP per capita (expenditure, multiple price benchmarks)
# %% 
md("#### {}"\
    .format(variable_meta['rgdpe_pc']['name']))
# %% 
md("{}"\
    .format(variable_meta['rgdpe_pc']['description']))
    

# %%
display(HTML('<iframe src="https://ourworldindata.org/grapher/real-gdp-per-capita-PennWT" loading="lazy" style="width: 100%; height: 600px; border: 0px none;"></iframe>'))



# –– # GDP per capita (output, multiple price benchmarks)
# %% 
md("#### {}"\
    .format(variable_meta['rgdpo_pc']['name']))
# %% 
md("{}"\
    .format(variable_meta['rgdpo_pc']['description']))
    

# %%
display(HTML('<iframe src="https://ourworldindata.org/grapher/real-gdp-per-capita-PennWT" loading="lazy" style="width: 100%; height: 600px; border: 0px none;"></iframe>'))




# –– # GDP per capita (expenditure, single price benchmark)
# %% 
md("#### {}"\
    .format(variable_meta['cgdpe_pc']['name']))
# %% 
md("{}"\
    .format(variable_meta['cgdpe_pc']['description']))
    

# %%
display(HTML('<iframe src="https://ourworldindata.org/grapher/real-gdp-per-capita-PennWT" loading="lazy" style="width: 100%; height: 600px; border: 0px none;"></iframe>'))



# –– # GDP per capita (output, single price benchmark)
# %% 
md("#### {}"\
    .format(variable_meta['cgdpo_pc']['name']))
# %% 
md("{}"\
    .format(variable_meta['cgdpo_pc']['description']))
    

# %%
display(HTML('<iframe src="https://ourworldindata.org/grapher/real-gdp-per-capita-PennWT" loading="lazy" style="width: 100%; height: 600px; border: 0px none;"></iframe>'))




# –– # GDP per capita (national accounts)
# %% 
md("#### {}"\
    .format(variable_meta['rgdpna_pc']['name']))
# %% 
md("{}"\
    .format(variable_meta['rgdpna_pc']['description']))
    

# %%
display(HTML('<iframe src="https://ourworldindata.org/grapher/real-gdp-per-capita-PennWT" loading="lazy" style="width: 100%; height: 600px; border: 0px none;"></iframe>'))





# %% [markdown]
## Appendix
"""
Here we provide links to further documentation of the Penn World Tables data 
and our treatment of it. 
#
* A comparison of version 10.0 with a previous release of the data (JH comment: Pablo, at some point let's add this as an 'auxiliary notebook')
* A list of further documentation discussing various vintages of the dataset can be found at the [Groningen Growth and Development Centre's website](https://www.rug.nl/ggdc/productivity/pwt/pwt-documentation). 
"""

# %%
