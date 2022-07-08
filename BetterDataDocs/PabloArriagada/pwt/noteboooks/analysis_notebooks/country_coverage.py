# %% [markdown]
# # Checking data availability for countries

# %%
import pandas as pd
import plotly.express as px
import plotly.io as pio
import numpy as np

pio.renderers.default = "jupyterlab+png+colab+notebook_connected+vscode"

# %%
#Main data file
url = "https://joeh.fra1.digitaloceanspaces.com/pwt/entities_standardized.csv"

df = pd.read_csv(url)

# %%
df['rgdpe_pc'] = df['rgdpe']/df['pop']
df['rgdpo_pc'] = df['rgdpo']/df['pop']
df['cgdpe_pc'] = df['cgdpe']/df['pop']
df['cgdpo_pc'] = df['cgdpo']/df['pop']
df['rgdpna_pc'] = df['rgdpna']/df['pop']

# %%
df

# %%
df_all_year = df.groupby(['year']).count().reset_index()
df_all_year = pd.melt(df_all_year, id_vars=['year'])
df_all_year = df_all_year[~df_all_year['variable'].isin(['cor_exp', 'statcap'])].reset_index(drop=True)

df_all_countryyear = df.groupby(['entity', 'year']).count().reset_index()
df_all_countryyear = pd.melt(df_all_countryyear, id_vars=['entity', 'year'])

# %%
fig = px.line(df_all_year, x="year", y="value", color="variable", height=600,
              title='<b>Country coverage in PWT</b>',
             labels={
                     "value": "Number of countries",
                 })
fig.show()

# %%
variable = 'rgdpe_pc'
df_coverage = df_all_countryyear[(df_all_countryyear['variable'] == variable) & 
                                 (df_all_countryyear['value'] == 1)].reset_index(drop=True)

df_coverage.drop(columns=['variable', 'value'], inplace=True)
df_coverage = df_coverage.set_index('entity')
fig = px.imshow(df_coverage)
fig.show()

# %%
df_coverage

# %%
variable = 'rgdpe_pc'
df_coverage = df_all_countryyear[df_all_countryyear['variable'] == variable].reset_index(drop=True)
df_coverage['value'].replace(0, np.nan, inplace=True)
df_coverage['year'] = df_coverage['year'].astype(int)


fig = px.bar(df_coverage, x="year", y="entity", color="value",
             hover_data=["value"],
             height=3000, width=2000,
             title='Data Availabiltiy Plot',
             template='plotly_white',
             range_x=[min(df_coverage['year']),max(df_coverage['year'])]
            )

fig.show("png")

# %%
min(df_coverage['year'])

# %%
df['i_cig'] = df['i_cig'].astype(str)

# %%
#Change the log_x and log_y parameters to "False" to see negative values

fig = px.scatter(df, x="year", y="rgdpe_pc", 
                 hover_data=['entity', 'year'], opacity=0.5, color='i_cig', 
                 title="<b>Type of estimation for the relative price data for consumption, investment and government (<i>i_cig</i>)</b><br>rgdpe_pc vs year",
                 log_x=False,
                 log_y=True,
                 height=600,
                )

fig.update_traces(marker=dict(size=10, line=dict(width=0, color='blue')))
fig.show()

# %%
