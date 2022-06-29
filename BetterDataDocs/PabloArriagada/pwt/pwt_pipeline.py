from IPython.display import Markdown as md


# %% [markdown]
# This is the pipeline for PWT....


# %% [markdown]

# *This article describes the data in the Penn World Tables version 10.0 and documents how Our World in Data have handled and transformed this data in order to make use of it in our publication.*
#
# *This article is an unsual, experimental format, which we have designed to make our data work more transparent and reusable.*
#
# *To prepare the data for use in our publication we write and then execute a computer programme. Within that computer programme we include extensive notes, explanations and visualizations to make any choices concerning the treatment of the data more visible and to explain our reasoning. This article is a web version of that computer programme in which priority is given to the notes and explanations and much of the code is hidden or not shown to improve readability. You can read this article whether or not you are familiar with (python) code in order to understand more about the Penn World Tables and our treatment of the data.*
#
# *The full code we use to prepare this data can be found in GitHub.*


# ## About this data

# *JH comment: My idea here is that we show here the metadata as in our database (and Sources tab). Possibly we could **specifiy** the metadata here? (We write it here, and then when you run the script it's these fields that end up in the database/grapher admin.

# %%
# Provide dataset metadata (as specified in Grapher Admin)
datasetName = "Penn World Tables version 10.0"
datasetSourceName = "Penn World Tables"
datasetLink = "https://www.rug.nl/ggdc/productivity/pwt"
datasetDescription = "PWT version 10.0 is a database with information on relative levels of income, output, input and productivity, covering 183 countries between 1950 and 2019."
datasetRetrieved = "XX June 2022"
datasetNextUpdateExpected = "Unknown"

# %%
# Print the metadata
print("Name: " + datasetName)
print("Source: " + datasetSourceName)
print("Link: " + datasetLink)
print("Description: " + datasetDescription)
print("Last updated: " + datasetRetrieved)
print("Expected data of next update: " + datasetNextUpdateExpected)

# %% [markdown]
# #### **All charts using this data**

# %% [markdown]
# *JH comment: I don't know whether it would be possible to add some query here to produce an up-to-date list?*

# %% [markdown]
# ## Details about how we obtained the original data file and the intial steps we take to load and clean it

# %% [markdown]
# *JH comment: The idea is to give a breakdown of the etl stages, but with plain English description of what is going on. These section will be collapsed by default.*
#
# *Note that here I am just loading an Excel file from GitHub that was manually downloaded. But in the future this could refer to the first etl step.*

# ### Details of which libraries and packages we use to prepare the data

# %% [markdown]
# %%

# Pandas is the standard package used for data manipulation in python code
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

# %% [markdown]
# ## Details on the the initial loading and cleaning of the data

# %% 
md("#### Load our stored copy of the original data file (Retrieved on {})".format(datasetRetrieved))

# %%
#ETL note – This step is a bit like grabbing the data from Walden

#Here we have original Excel file in GitHub
url = 'https://raw.githubusercontent.com/owid/notebooks/main/PabloArriagada/pwt/data/pwt100.xlsx'

#We load it 
r = requests.get(url)
tempf = tempfile.TemporaryFile()
tempf.write(r.content)

df_original = pd.read_excel(tempf, sheet_name='Data')


# %% [markdown]
# #### Standardize country names

# %% [markdown]
# Our World in Data standardizes country names to allow us to compare data across different data sources.
# %%
# Pablo: can you add the country harmonization step here
#ETL note – This step is a bit like grabbing the data from Walden



df_final = df_original['countrycode', 'country']

# %%
# You can see a mapping of country names here:

# Pablo: please provide a table of the country name mapping


# %%
df_original.head()
# %% [markdown]
# ### Details of how we standardize the names of countries and world regions
# %% [markdown]
# *JH comment: Let's do this step here early on – as it would be in the etl process*

# ## Details of each variable we have prepared from Penn World Tables version 10

# *JH comment: I am adapting the text from [Diana's Google Doc](https://docs.google.com/document/d/1Kg9ZqxXXfDWA7WxfDysB0GjwlQ6kK5x6kNP-m7Sjl-I/edit?pli=1#heading=h.3iglji7a4k32)*

# *JH comment: See my comment at the top of this doc about the Dataset-level metadata. Maybe we can define the variable-level metadata in a way that's helpful. For instance, below I make a set of ordered arrays that provide the metadata for for each variable. The idea is that this will be passed to the database/garpher admin. But we can also use to e.g. make the title of subsections. In that way the titles and the variable name will always be linked.*
# %%
#Initialize empty arrays for variable-level metadata
variableFinalNames = []
variableDisplayNames = []
variableUnitLongs = []
variableUnitShorts = []
variableDescription = []
variableNames = []
# %% [markdown]
# ### GDP
# %% [markdown]
# *JH comment: Here let's explain the different approaches to prices that define the different GDP variables.*
#
# *The point it if you want to compare across countries and over time then you can't have everything:*
# *"Diewert (1999) and Van
# Veelen (2002) have argued that no multilateral measure of real GDP can satisfy all the axioms
# we might like, so there are tradeoffs involved with any construction of this concept."*
#
# *PWT provide different measures for different purposes, in two different dimensions:*
#
# *1. Expenditure vs Output side*
# *2. constant vs current prices vs NA growth rates
#
# *The issue with the (1) is – which prices do you look at?*
# *The issue with (2) is How do you handle changing price structures over time if you want to compare across countries and over time?
#
#
#
#

# %%
# Append metadata for this variable to the arrays
variableNames = np.append(variableNames,["Real GDP (expenditure-side)"])
variableDisplayNames = np.append(variableDisplayNames,["Real GDP"])
variableUnitLongs = np.append(variableUnitLongs,["International-$ at 2017 prices"])
variableUnitShorts = np.append(variableUnitShorts,["$"])
variableDescription = np.append(variableDescription,["[Joe to write a description of this variable]"])

# %%
# Print display name of current variable. It would be great if we could figure out a way to render this output as a html heading...

md("## {}".format(variableDisplayNames[len(variableDisplayNames)-1]))

# %% [markdown]
# ##### About this variable

# %%
variableDescription[len(variableDescription)-1]
# %% [markdown]
# ##### How did we obtain this variable from the original data?
# %% [markdown]
# **Original variable name within PWT:** rgdpe

# %% [markdown]
#The original data is given in millions of dollars. We multiply the variable by 1,000,000 to give the figures in dollars.

# %%
pwt10['rgdpe'] = df_original['rgdpe']*1000000
# %% [markdown]
# *“real GDP on
# the output-side”, or real GDPo
# , which is intended to measure the production possibilities of an
# economy.*
# %% [markdown]
# ### GDP per capita
# %% [markdown]
# Each GDP variable discussed above is divided by the population figures provided in PWT to produce corresponding series for GDP per capita.
# %% [markdown]
# Divide by pop...


# %%
