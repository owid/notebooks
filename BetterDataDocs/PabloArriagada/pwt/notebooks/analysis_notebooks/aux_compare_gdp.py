# %%

# %% [markdown]
# # Data document: Comparing GDP series within the Penn World Tables
# %%
# ---- Import libraries ------
# Here we provide details of which libraries and packages we use to prepare the data

# Markdown lets us use variables within markdown chunks.
from IPython.display import Markdown as md

# This allows us to embed iframes in the output of the code cells.
from IPython.core.display import display, HTML

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


# Plotly is a package for creating interactive charts
import plotly.express as px
import plotly.io as pio
pio.renderers.default='notebook'


# %% [markdown]
# *JH comment: When the data is into our database, we 
# will use the owid catalogue/API to grab the data. For now 
# I just load it from the same place as in the main pipeline.*


# %%
# ------- Load and prep the GDP per capita data –––––––––

#Here we have stored the original Excel file in GitHub
url = 'https://raw.githubusercontent.com/owid/notebooks/main/PabloArriagada/pwt/data/pwt100.xlsx'

#We load it, via a temporary file 
# *Pablo comment: Maybe this is not needed, because the file can be loaded by using the url variable instead of tempf
# The file is downloaded once and then it is on the memory as a dataframe
# Please tell me if you have something else in mind with the library
r = requests.get(url)
tempf = tempfile.TemporaryFile()
tempf.write(r.content)

df_original = pd.read_excel(tempf, sheet_name='Data')


df_harmonized = df_original.copy()


# –– Construct GDP per capita variables –––––
# GDP per capita is GDP divided by popultion (both are given in millions)
df_harmonized['rgdpe_pc'] = df_harmonized['rgdpe']/df_harmonized['pop']
df_harmonized['rgdpo_pc'] = df_harmonized['rgdpo']/df_harmonized['pop']
df_harmonized['cgdpe_pc'] = df_harmonized['cgdpe']/df_harmonized['pop']
df_harmonized['cgdpo_pc'] = df_harmonized['cgdpo']/df_harmonized['pop']
df_harmonized['rgdpna_pc'] = df_harmonized['rgdpna']/df_harmonized['pop']



# %% [markdown]
# ## How big are the differences between the GDP variables in Penn World Tables?

# %%
# Calculate ratios to `rgdpe_pc`
df_harmonized['rgdpo_pc_ratio'] = df_harmonized['rgdpo_pc']/df_harmonized['rgdpe_pc']
df_harmonized['cgdpe_pc_ratio'] = df_harmonized['cgdpe_pc']/df_harmonized['rgdpe_pc']
df_harmonized['cgdpo_pc_ratio'] = df_harmonized['cgdpo_pc']/df_harmonized['rgdpe_pc']
df_harmonized['rgdpna_pc_ratio'] = df_harmonized['rgdpna_pc']/df_harmonized['rgdpe_pc']


fig = px.histogram(df_harmonized, x="rgdpo_pc_ratio",
title = 'Ratio of rgdpo to rgdpe')
fig.show()

fig = px.histogram(df_harmonized, x="cgdpe_pc_ratio",
title = 'Ratio of cgdpe to rgdpe')
fig.show()

fig = px.histogram(df_harmonized, x="cgdpo_pc_ratio",
title = 'Ratio of cgdpo to rgdpe')
fig.show()

fig = px.histogram(df_harmonized, x="rgdpna_pc_ratio",
title = 'Ratio of rgdpna to rgdpe')
fig.show()

# %%
#Pablo: We can explore using Seaborn's pairplot: plots each variable I choose against the other, and the diagonal is a histogram
#I can see with this that rgdpe_pc and cgdp_e are the only with almost equal values for each country-year, the other cases are more scattered

import seaborn as sns
sns.pairplot(df_harmonized, x_vars=['rgdpe_pc','rgdpo_pc', 'cgdpe_pc', 'cgdpo_pc', 'rgdpna_pc'], 
             y_vars=['rgdpe_pc','rgdpo_pc', 'cgdpe_pc', 'cgdpo_pc', 'rgdpna_pc'], 
             dropna=True, corner=False, diag_kind='kde', kind='reg',
             plot_kws={'line_kws':{'color':'#f28e2b'}, 'scatter_kws': {'alpha': 0.5}}
             )
#, height=5, aspect=3 ,plot_kws={'line_kws':{'color':'#f28e2b'}, 'scatter_kws': {'alpha': 0.5}}

# %%
#Pablo: With scatter_matrix in Plotly I can distinguish the countries which deviate from the y=x line
#For example, Bermuda (also seen as an outlier before)

fig = px.scatter_matrix(df_harmonized,
    dimensions=['rgdpe_pc','rgdpo_pc', 'cgdpe_pc', 'cgdpo_pc', 'rgdpna_pc'],
    color="countrycode",
    title="<b>GDP comparison (interactive)</b><br>Hover to see values, double click in legend to filter country",
    height=700, hover_data=['country', 'year'], opacity=0.5)
fig.update_traces(diagonal_visible=False)
fig.show()

# %%
