# %% [markdown]
# # OWID Data document<br>Comparing GDP series within the Penn World Tables
# %% [markdown]
# ### About OWID Data documents
#
# OWID data documents combine computer code and text to explain and document the data we and how we prepare it from the original sources.
#
# We make these documents available in different formats:
#
# - A [read-only version](https://htmlpreview.github.io/?https://raw.githubusercontent.com/owid/notebooks/main/BetterDataDocs/PabloArriagada/pwt/notebooks/analysis_notebooks/compare_trade_shares/compare_trade_shares.html) online
# - A script in [GitHub](https://github.com/owid/notebooks/blob/main/BetterDataDocs/PabloArriagada/pwt/notebooks/analysis_notebooks/compare_trade_shares/compare_trade_shares.qmd)
# - A runnable version in [Google Colab](https://colab.research.google.com/drive/1e0wmNlZI_8Sw5b0ocLePNMTpbcqLNHDY#scrollTo=Xf_VyXxPjMAL)
#
#
#
# If you have this open in _Google Colab_, you can run the code blocks below and see their outputs. Clicking on **'Copy to Drive'** in the menu bar above will open up a new copy in your own Google Drive that you can then _edit_ the code to explore the data further.

# %% [markdown]
# ## The 5 GDP variables available at PWT

# %% [markdown]
# Starting from version 8, the Penn World Table includes five different GDP measures.
#
# There are two based on prices that are constant across countries and over time:
#
# - **rgdpe**: Expenditure-side real GDP at chained PPPs (in mil. 2017USD), to compare living standards between countries and across years.
# - **rgdpo**: Output-side real GDP at chained PPPs (in mil. 2017USD), to compare productive capacity between countries and across years.
#
# There are two based on prices that are constant across countries in a given year:
#
# - **cgdpe**: Expenditure-side real GDP at current PPPs (in mil. 2017USD), to compare living standards across countries in each year.
# - **cgdpo**: Output-side real GDP at current PPPs (in mil. 2017USD), to compare productive capacity across countries in each year.
#
# And there is one based on national prices that are constant over time:
#
# - **rgdpna**: Real GDP at constant 2017 national prices (in mil. 2017USD), to compare growth of GDP over time in each country.

# %%
# ---- Import libraries ------
# Here we provide details of which libraries and packages we use to prepare the data

# Pandas is a standard package used for data manipulation in python code
import pandas as pd

# Plotly is a package for creating interactive charts
import plotly.express as px
import plotly.io as pio
pio.renderers.default='jupyterlab+png+colab+notebook_connected+vscode'


# %% [markdown]
# *JH comment: When the data is into our database, we 
# will use the owid catalogue/API to grab the data. For now 
# I just load it from the same place as in the main pipeline.*


# %%
# ------- Load and prep the GDP per capita data –––––––––

#Here we have stored the original Excel file in GitHub
url = 'https://joeh.fra1.digitaloceanspaces.com/pwt/entities_standardized.csv'
df = pd.read_csv(url)

# –– Construct GDP per capita variables –––––
# GDP per capita is GDP divided by population (both are given in millions)
df['rgdpe_pc'] = df['rgdpe']/df['pop']
df['rgdpo_pc'] = df['rgdpo']/df['pop']
df['cgdpe_pc'] = df['cgdpe']/df['pop']
df['cgdpo_pc'] = df['cgdpo']/df['pop']
df['rgdpna_pc'] = df['rgdpna']/df['pop']



# %%
df[['rgdpe_pc', 'rgdpo_pc', 'cgdpe_pc', 'cgdpo_pc', 'rgdpna_pc']].describe()

# %% [markdown]
# ## Expenditure-side vs. output-side

# %% [markdown]
# If these concepts are linked with macroeconomic theory, it seems weird to assign two different values to expenditure and output side GDP, because both sides in the GDP equation are equal. But this is due mainly to a distinction: only the output-side GDP includes prices of imports and exports, and that is why is connected with productive capacity. Let's see the differences between `rgdpe` and `rgdpo` and also between `cgdpe` and `cgdpo`
#
# *This could be useful: https://documents1.worldbank.org/curated/en/346251468142506072/pdf/wps4166.pdf*

# %%
# Calculate ratios to `rgdpe_pc`
df['rgdp_ratio'] = df['rgdpo_pc']/df['rgdpe_pc']
df['cgdp_ratio'] = df['cgdpo_pc']/df['cgdpe_pc']


fig = px.histogram(df, x="rgdp_ratio",
title = '<b>Ratio of rgdpo to rgdpe</b>', marginal="box", hover_data=['entity', 'year'])
fig.show()

fig = px.histogram(df, x="cgdp_ratio",
title = '<b>Ratio of cgdpo to cgdpe</b>', marginal="box", hover_data=['entity', 'year'])
fig.show()

# %%
fig = px.scatter(df, x="year", y="rgdp_ratio", 
                 hover_data=['entity', 'year', 'rgdpe_pc', 'rgdpo_pc'], opacity=0.5, color='entity', 
                 title="<b>Ratio of rgdpo to rgdpe</b>",
                 log_x=True,
                 log_y=True,
                 height=600,
                )

fig.update_traces(marker=dict(size=10, line=dict(width=0, color='blue')))
fig.show()

fig = px.scatter(df, x="year", y="cgdp_ratio", 
                 hover_data=['entity', 'year', 'cgdpe_pc', 'cgdpo_pc'], opacity=0.5, color='entity', 
                 title="<b>Ratio of cgdpo to cgdpe</b>",
                 log_x=True,
                 log_y=True,
                 height=600,
                )

fig.update_traces(marker=dict(size=10, line=dict(width=0, color='blue')))
fig.show()

# %% [markdown]
# ## Real GDP vs. Current price GDP vs. National accounts-based GDP

# %%
#Pablo: We can explore using Seaborn's pairplot: plots each variable I choose against the other, and the diagonal is a histogram
#I can see with this that rgdpe_pc and cgdp_e are the only with almost equal values for each country-year, the other cases are more scattered

import seaborn as sns
sns.pairplot(df, x_vars=['rgdpe_pc','rgdpo_pc', 'cgdpe_pc', 'cgdpo_pc', 'rgdpna_pc'], 
             y_vars=['rgdpe_pc','rgdpo_pc', 'cgdpe_pc', 'cgdpo_pc', 'rgdpna_pc'], 
             dropna=True, corner=False, diag_kind='kde', kind='reg',
             plot_kws={'line_kws':{'color':'#f28e2b'}, 'scatter_kws': {'alpha': 0.5}}
             )
#, height=5, aspect=3 ,plot_kws={'line_kws':{'color':'#f28e2b'}, 'scatter_kws': {'alpha': 0.5}}

# %%
#Pablo: With scatter_matrix in Plotly I can distinguish the countries which deviate from the y=x line
#For example, Bermuda (also seen as an outlier before)

fig = px.scatter_matrix(df,
    dimensions=['rgdpe_pc','rgdpo_pc', 'cgdpe_pc', 'cgdpo_pc', 'rgdpna_pc'],
    color="entity",
    title="<b>GDP comparison (interactive)</b><br>Hover to see values, double click in legend to filter country",
    height=600, hover_data=['entity', 'year'], opacity=0.5)
fig.update_traces(diagonal_visible=False)
fig.show()

# %%
