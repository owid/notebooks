from IPython.display import Markdown as md
from IPython.core.display import display, HTML


# %% [markdown]
# This is the pipeline for PWT....


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
# Specify dataset metadata - (this will end up in e.g. our database, 'Sources' tab etc.)
dataset_meta = {
    "name": "Penn World Tables version 10.0",
    "sourceName": "Penn World Tables",
    "link": "https://www.rug.nl/ggdc/productivity/pwt",
    "description": "PWT version 10.0 is a database with information on relative levels of income, output, input and productivity, covering 183 countries between 1950 and 2019.",
    "dateRetrieved": "dd/mm/2022",
    "nextUpdate": "Unknown"
}


# %%
#Print the metadata as markdown
md("**Name:**  {} <br><br>\
    **Source:**  {} <br><br>\
    **Link:**  {} <br><br>\
    **Description:**  {} <br><br>\
    **Last updated:**  {} <br><br>\
    **Expected data of next update:**  {} "\
    .format(dataset_meta["name"], 
            dataset_meta["sourceName"],
            dataset_meta["link"],
            dataset_meta["description"],
            dataset_meta["dateRetrieved"],
            dataset_meta["nextUpdate"]))




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
# Pablo: can you add the country harmonization step here (df_harmonized is the df with standardized country names)

df_harmonized = df_original


# %%
# You can see a mapping of country names here:

# Pablo: please provide a table of the country name mapping


# %% [markdown]
#The resulting data looks like this:
# %%
df_harmonized.head()

# %% [markdown]
# ## A summary of each variable

# *JH comment: See [Diana's Google Doc](https://docs.google.com/document/d/1Kg9ZqxXXfDWA7WxfDysB0GjwlQ6kK5x6kNP-m7Sjl-I/edit?pli=1#heading=h.3iglji7a4k32) for a previous attempt at this*



# %% [markdown]
# ### GDP


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


"""
# %% 
# Prepare GDP data
df_harmonized['rgdpe'] = df_original['rgdpe']*1000000
df_harmonized['rgdpo'] = df_original['rgdpo']*1000000
df_harmonized['cgdpe'] = df_original['cgdpe']*1000000
df_harmonized['cgdpo'] = df_original['cgdpe']*1000000
df_harmonized['rgdpna'] = df_original['rgdpna']*1000000


# %%
# Create a dictionary (of dictionaries)
variable_meta = {}

# Add to dictionary variable metadata - (this will end up in e.g. our database, 'Sources' tab etc.)
variable_meta['rgdpe'] = {}

variable_meta['rgdpe']['name'] = "Real GDP (expenditure-side)"
variable_meta['rgdpe']['displayName'] = "Real GDP"
variable_meta['rgdpe']['unitsLong'] = "International-$ at 2017 prices"
variable_meta['rgdpe']['unitsShort'] = "$"
variable_meta['rgdpe']['description'] = "[Long description here]"


# %%
#The original data is given in millions of dollars. We multiply the variable by 1,000,000 to give the figures in dollars.


# %%
df_harmonized['rgdpe'] = df_original['rgdpe']*1000000


# %%
display(HTML('<iframe src="https://ourworldindata.org/grapher/real-gdp-per-capita-PennWT" loading="lazy" style="width: 100%; height: 600px; border: 0px none;"></iframe>'))

# %%
# Append metadata for this variable to the arrays
variableNames = np.append(variableNames,["Real GDP (expenditure-side)"])
variableDisplayNames = np.append(variableDisplayNames,["Real GDP"])
variableUnitLongs = np.append(variableUnitLongs,["International-$ at 2017 prices"])
variableUnitShorts = np.append(variableUnitShorts,["$"])
variableDescription = np.append(variableDescription,["[Joe to write a description of this variable]"])
variableNames = ['final_rgdpe']
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
