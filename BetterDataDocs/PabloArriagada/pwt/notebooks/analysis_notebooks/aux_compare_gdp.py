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
# There are two based on prices that are constant across countries and over time, where multiple ICP benchmarks are applied:
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
# If these concepts are linked with macroeconomic theory, it seems weird to assign two different values to expenditure and output side GDP, because both sides in the GDP equation are equal. But this is due mainly to a distinction: only the output-side GDP includes prices of imports and exports, and that is why is connected with productive capacity. In fact, the output-side estimations have been more recently developed by PWT, due to the difficulty of constructing relative prices of imports and exports. Let's see the differences between `rgdpe` and `rgdpo` and also between `cgdpe` and `cgdpo`
#
# *This could be useful: https://documents1.worldbank.org/curated/en/346251468142506072/pdf/wps4166.pdf*

# %% [markdown]
# If we divide the output-side by the expenditure-side GDP values for each country and year we can see that most of the ratios are very close to 1, but there are some very large differences, concentrated in Bermuda, Kuwait, Turks and Caicos Islands and Malta. 

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

# %% [markdown]
# The outliers are seen more clearly on this plot:

# %%
fig = px.scatter(df, x="year", y="rgdp_ratio", 
                 hover_data=['entity', 'year', 'rgdpe_pc', 'rgdpo_pc'], opacity=0.5, color='entity', 
                 title="<b>Ratio of rgdpo to rgdpe vs. year</b>",
                 log_x=True,
                 log_y=True,
                 height=600,
                )

fig.update_traces(marker=dict(size=10, line=dict(width=0, color='blue')))
fig.show()

fig = px.scatter(df, x="year", y="cgdp_ratio", 
                 hover_data=['entity', 'year', 'cgdpe_pc', 'cgdpo_pc'], opacity=0.5, color='entity', 
                 title="<b>Ratio of cgdpo to cgdpe vs. year</b>",
                 log_x=True,
                 log_y=True,
                 height=600,
                )

fig.update_traces(marker=dict(size=10, line=dict(width=0, color='blue')))
fig.show()

# %% [markdown]
# ## Current vs. chained PPPs

# %% [markdown]
# Purchasing power parities (PPPs) are the rates of currency conversion that equalise the purchasing power of different currencies by eliminating the differences in price levels between countries. They are estimated with the prices of a large set of commodities and for a large number of countries, and associated outputs (quantities), all referring to some benchmark year. This works much better than market exchange rates, which are biased towards traded goods across countries.
#
# Both real GDPs in current and chained PPPs (`cgdpe`/`cgdpo` and `rgdpe`/`rgdpo`, respectively) allow for international comparisons between countries, but as chained PPPs use the multiple ICP's PPP benchmarks through the years (and interpolations between them), countries can be compared across time, unlike current PPPs (using only one benchmark). By construction, in the year 2017 the values of `cgdpe` and `rgdpe` and also the values of `cgdpo` and `rgdpo` coincide, as seen in the following plot hovering the data for that year.
#
# When comparing output-side and expenditure-side GDPs for current and chained PPPs we can see that for some countries the values are actually similar: the rgdpe values ranges between 0.9 and 1.25 times the cgdpe. Although in the output-side measures there are (very) large outliers (Bermuda has ratios between 7 and 21, Turks and Caicos Islands range around 3) or ratios between 1.5 and 2.5, most of the data also ranges between 0.9 and 1.25. 

# %%
df['output_side_ratio'] = df['rgdpo_pc']/df['cgdpo_pc']
df['expenditure_side_ratio'] = df['rgdpe_pc']/df['cgdpe_pc']


fig = px.histogram(df, x="output_side_ratio",
title = '<b>Ratio of rgdpo to cgdpo</b>', marginal="box", hover_data=['entity', 'year'])
fig.show()

fig = px.histogram(df, x="expenditure_side_ratio",
title = '<b>Ratio of rgdpe to cgdpe</b>', marginal="box", hover_data=['entity', 'year'])
fig.show()

# %%
fig = px.scatter(df, x="year", y="output_side_ratio", 
                 hover_data=['entity', 'year', 'rgdpo_pc', 'cgdpo_pc'], opacity=0.5, color='entity', 
                 title="<b>Ratio of rgdpo to cgdpo vs. year</b>",
                 log_x=True,
                 log_y=True,
                 height=600,
                )

fig.update_traces(marker=dict(size=10, line=dict(width=0, color='blue')))
fig.show()

fig = px.scatter(df, x="year", y="expenditure_side_ratio", 
                 hover_data=['entity', 'year', 'rgdpe_pc', 'cgdpe_pc'], opacity=0.5, color='entity', 
                 title="<b>Ratio of rgdpe to cgdpe vs. year</b>",
                 log_x=True,
                 log_y=True,
                 height=600,
                )

fig.update_traces(marker=dict(size=10, line=dict(width=0, color='blue')))
fig.show()

# %% [markdown]
# ## National accounts-based GDP

# %% [markdown]
# The GDP variable `rgdpna` is a real GDP based in the growth of rate of national accounts data and then converted to the last (2017) ICP PPP benchmark. By construction, the 2017 `rgdpna` value equals the `cgdpo` 2017 value but the values differ more than the other cases.

# %%
df['rgdpna_cgdpo_ratio'] = df['rgdpna_pc']/df['cgdpo_pc']


fig = px.histogram(df, x="rgdpna_cgdpo_ratio",
title = '<b>Ratio of rgdpna to cgdpo</b>', marginal="box", hover_data=['entity', 'year'])
fig.show()

# %%
fig = px.scatter(df, x="year", y="rgdpna_cgdpo_ratio", 
                 hover_data=['entity', 'year', 'rgdpna_pc', 'cgdpo_pc'], opacity=0.5, color='entity', 
                 title="<b>Ratio of rgdpna to cgdpo vs. year</b>",
                 log_x=True,
                 log_y=True,
                 height=600,
                )

fig.update_traces(marker=dict(size=10, line=dict(width=0, color='blue')))
fig.show()

# %% [markdown]
# ## Real GDP vs. Current price GDP vs. National accounts-based GDP

# %% [markdown]
# These plot matrices show the differences between all the four (per capita) variables: their correlations and their actual values.

# %%
df[['rgdpe_pc','rgdpo_pc', 'cgdpe_pc', 'cgdpo_pc', 'rgdpna_pc']].corr()

# %%
fig = px.imshow(df[['rgdpe_pc','rgdpo_pc', 'cgdpe_pc', 'cgdpo_pc', 'rgdpna_pc']].corr(),
                color_continuous_scale="Purples",
               text_auto='.2f')
fig.show()

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

# %%
