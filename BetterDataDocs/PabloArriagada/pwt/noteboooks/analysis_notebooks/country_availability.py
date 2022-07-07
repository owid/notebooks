# %% [markdown]
# # Checking data availability for countries

# %%
import pandas as pd
import plotly.express as px
import plotly.io as pio

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
df_nulls = df.rgdpe.isnull().groupby([df['entity']]).sum().astype(int).reset_index(name='count')

# %%
df_nulls.sort_values(by='count', ascending=False)

# %%
df_all = df.groupby(['entity']).count().reset_index()

# %%
df_all

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
