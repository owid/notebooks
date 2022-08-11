# %%
# This script is just to check which version of the WB data used by Yonzan, 
# Lakner and Mahler in their Oct 2020 blog post here: 
# https://blogs.worldbank.org/opendata/projecting-global-extreme-poverty-2030-how-close-are-we-world-banks-3-goal

import pandas as pd

from functions.PIP_API_query import pip_query_country, pip_query_region

from global_poverty_with_Lakner_projections import df_stacked

# %%
# Compare with the values in the Stacked area chart in the blog post (any scenario)
df_stacked[df_stacked['c19_estimation'] == 'baseline']

# %%
p_dollar = 1.9 

df = pip_query_region(p_dollar)
# %%
