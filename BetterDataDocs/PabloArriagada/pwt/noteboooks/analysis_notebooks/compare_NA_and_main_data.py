# %% [markdown]
# # Comparing PWT's main dataset vs National Accounts dataset 

# %%
import pandas as pd
import plotly.express as px
import plotly.io as pio

#pio.renderers.default = "jupyterlab+png+colab+notebook_connected+vscode"
#JH comment: When running this in VC Code, this line creates problems for me. There seems to be a dependency missing.
#Pablo: As long as it runs for the both of us without the code it's fine

# %%
#Main data file
url = "https://joeh.fra1.digitaloceanspaces.com/pwt/entities_standardized.csv"

df_main = pd.read_csv(url)

# %%
df_main.head()

# %%
# National Accounts data file
url = "https://joeh.fra1.digitaloceanspaces.com/pwt/entities_standardized_national_accounts.csv"

df_na = pd.read_csv(url)
# %%
df_na.head()



# %% [markdown]
# # Trade shares using the main data file
# The variable `x_m_share` is the trade ratio estimated with `csh_x` (share of exports) and `csh_m` (share of imports) in `cgdpo`
# Note that exports are expressed as positive numbers, and imports as negative numbers.
# But there are four observations for Bermuda where this is reversed. We are not sure how to interpret that.

# %%
# Exports are (mostly) positive
fig = px.histogram(df_main, x="csh_x", marginal="box", hover_data=df_main[['entity', 'year']])
fig.show()


# %%
# And imports are (mostly) negative
fig = px.histogram(df_main, x="csh_m", marginal="box", hover_data=df_main[['entity', 'year']])
fig.show()

# %%
# Show observations with either negative exports or positive imports.
df_main[(df_main['csh_x']<0) | (df_main['csh_m']>0)]



# %%
# Sum exports as share of GDP and imports as share of GDP (using absolute values)
df_main['x_m_share'] = (abs(df_main['csh_x']) + abs(df_main['csh_m'])) * 100
#Pablo: at least to keep the logic of the ratio variable it should be exports **minus** the imports
#Because the import shares are (mostly) negative. See statistics in next cell
#JH reply: Yes you're right! Above I changed it to absolute values (for the Bermuda issue noted above. 
# But possibly we should drop these observations for Bermuda? 
# In any case, it would be good to understand what the signs for these observations being reversed means. 
# %% [markdown]
# There is a very wide range of values for trade openness.
# %%
#Histogram of trade openness observations.
fig = px.histogram(df_main, x="x_m_share", marginal="box",hover_data=df_main[['entity', 'year']])
fig.show()

# %% [markdown]
# Here we show the time series for countries with any values that exceed 500%.
# <br>
# We see that ther very large values we saw in the histogram come from 
# spikes seen in a handful of offshore financial centres. The largest spike is seen 
# in Bermuda for the years where the sign on the imports and export values were 
# reversed. (See discussion above).
#
# Pablo: I am not able to see this following bit of code as actual code, it runs as markdown in Jupyter
#
# threshold = 1
# high_value_countries = df_main.loc[df_main['x_m_share'] > 500, 'entity'].drop_duplicates()
# high_value_countries.values.tolist()
# print(high_value_countries)
#
# plot_data = df_main[df_main['entity'].isin(high_value_countries)]
# fig = px.line(plot_data, x = 'year', y='x_m_share', 
#     title = "Countries with large trade flows",
#     color = 'entity')
# fig.show()

# %%
threshold = 500
high_value_countries = df_main.loc[df_main['x_m_share'] > threshold, 'entity'].drop_duplicates()
high_value_countries.values.tolist()
print(high_value_countries)

plot_data = df_main[df_main['entity'].isin(high_value_countries)]
fig = px.line(plot_data, x = 'year', y='x_m_share', 
    title = "Countries with large trade flows",
    color = 'entity')
fig.show()

# %% [markdown]
# Here we calculate the same measure of trade openness for the world in 
# aggregate and add it as a new 'entity' to the dataset.


# %%
df_main_world = df_main.copy()
df_main_world['trade_x_gdp'] = df_main_world['x_m_share'] * df_main_world['cgdpo']
df_main_world = df_main_world.groupby(['year']).sum()
df_main_world.reset_index(inplace=True)

df_main_world['x_m_share'] = df_main_world['trade_x_gdp'] / df_main_world['cgdpo']
df_main_world.drop(['trade_x_gdp'], axis = 1, inplace=True)

df_main_world['entity'] = 'World'
df_main_world = df_main_world[['entity', 'year', 'x_m_share']]
df_main = pd.concat([df_main,df_main_world], ignore_index=True)

# %% [markdown]
# # Trade shares using the national accounts data file


# %%
# Exports distribution for NA
df_na['v_x_sh'] = df_na['v_x']/df_na['v_gdp'] 
fig = px.histogram(df_na, x="v_x", marginal="box", hover_data=df_na[['entity', 'year']])
fig.show()


# %%
# Imports distribution for NA
fig = px.histogram(df_na, x="v_m", marginal="box", hover_data=df_na[['entity', 'year']])
fig.show()

# %%
# Show observations with either negative exports or positive imports: None
df_na[(df_na['v_x']<0) | (df_na['v_m']<0)]



# %% [markdown]
# The variable 'ratio' is the trade ratio estimated with `v_x` (value of exports) `v_m` (value of imports) and `v_gdp`, the GDP taken from the National Accounts dataset from PWT.

# %%
df_na['ratio'] = (df_na['v_x'] + df_na['v_m']) / df_na['v_gdp'] *100

df_na_world = df_na.copy()

df_na_world['gdp_usd'] = df_na_world['v_gdp']/df_na_world['xr2'] #Also check with xr
df_na_world['trade_x_gdp'] = df_na_world['ratio'] * df_na_world['gdp_usd'] 
df_na_world = df_na_world.groupby(['year']).sum()
df_na_world.reset_index(inplace=True)

df_na_world['ratio'] = df_na_world['trade_x_gdp'] / df_na_world['gdp_usd']
df_na_world.drop(['trade_x_gdp'], axis = 1, inplace=True)

df_na_world['entity'] = 'World'
df_na_world = df_na_world[['entity', 'year', 'ratio']]
df_na = pd.concat([df_na,df_na_world], ignore_index=True)

# %% [markdown]
# Merging to compare both datasets for each entity and year:

# %%
df_merge = pd.merge(df_main, df_na[['entity', 'year', 'ratio']], on=['entity','year'], how='left',validate='one_to_one')

# %% [markdown]
# Descriptive statistics for both measures:

# %%
df_merge[['x_m_share', 'ratio']].describe()

# %%
#Reshape for line plot
df_long = df_merge[['year','entity','x_m_share', 'ratio']]
df_long = df_long.melt(id_vars=['year','entity'], var_name='measure')
df_long
# %%

select_entities = ['United Kingdom', "United States", "China", "South Africa"]

plot_data = df_long[df_long['entity'].isin(select_entities)]

fig = px.line(plot_data, x = 'year', y='value', 
    title = "Compare measures of trade openness",
    color = 'measure',
    facet_col='entity',
    facet_col_wrap=2)
fig.show()

# %% [markdown]
# A division between both measures is done to compare their magnitudes.

# %%
df_merge['ratio_vs'] = df_merge['x_m_share'] / df_merge['ratio']

# %% [markdown]
# The numbers differ greatly, and it seems the difference is bigger as `x_m_share` is (exponentially) bigger. The division of the two measures is less than 0.1 for many countries and years. The year of the data does not seem to influence the differences

# %%
#Change the log_x and log_y parameters to "False" to see negative values

fig = px.scatter(df_merge, x="x_m_share", y="ratio_vs", 
                 hover_data=['entity', 'year'], opacity=0.5, color='entity', 
                 title="<b>Trade ratio comparison</b><br>Ratio between both measures vs x_m_share",
                 log_x=True,
                 log_y=True,
                 height=600,
                )

fig.update_traces(marker=dict(size=10, line=dict(width=0, color='blue')))
fig.show()

# %%
#Change log_y parameter to "False" to see negative values

fig = px.scatter(df_merge, x="year", y="ratio_vs", 
                 hover_data=['entity', 'year'], opacity=0.5, color='entity', 
                 title="<b>Trade ratio comparison</b><br>Ratio between both measures vs year",
                 log_y=True,
                 height=600
                )

fig.update_traces(marker=dict(size=10, line=dict(width=0, color='blue')))
fig.show()

# %% [markdown]
# **Bermuda** is a case with multiple negative values (change log_axis values to False). See the basic stats for both variables.

# %%
bermuda = df_merge[df_merge['entity']=='Bermuda'].reset_index()
bermuda[['x_m_share', 'ratio']].describe()

# %% [markdown]
# For the aggregated "World" entity the differences range between a `x_m_share` / `ratio` value ranging from 0.79 to 0.92. Using the `xr` exchange rate the value changes to ~0.3 for the late 90s and early 2000s, and it is 7.9 for 2019.

# %%
#Change the log_x and log_y parameters to "False" to see negative values

fig = px.scatter(df_merge[df_merge['entity']=="World"], x="x_m_share", y="ratio_vs", 
                 hover_data=['entity', 'year'], opacity=0.5, color='entity', 
                 title="<b>Trade ratio comparison (for <i>World</i> entity)</b><br>Ratio between both measures vs x_m_share",
                 log_x=True,
                 log_y=True,
                 height=600,
                )

fig.update_traces(marker=dict(size=10, line=dict(width=0, color='blue')))
fig.show()

# %%
#Change log_y parameter to "False" to see negative values

fig = px.scatter(df_merge[df_merge['entity']=="World"], x="year", y="ratio_vs", 
                 hover_data=['entity', 'year'], opacity=0.5, color='entity', 
                 title="<b>Trade ratio comparison (for <i>World</i> entity)</b><br>Ratio between both measures vs year",
                 log_y=True,
                 height=600
                )

fig.update_traces(marker=dict(size=10, line=dict(width=0, color='blue')))
fig.show()

# %%
