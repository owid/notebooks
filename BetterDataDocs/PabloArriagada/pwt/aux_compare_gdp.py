
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

# Seaborn is a Python data visualization library (based on matplotlib)
#import seaborn as sns

# NumPy is a standard package that provides a range of useful mathematical functions 
import numpy as np

# Plotly is a package for creating interactive charts
import plotly.express as px
import plotly.io as pio
pio.renderers.default='notebook'
