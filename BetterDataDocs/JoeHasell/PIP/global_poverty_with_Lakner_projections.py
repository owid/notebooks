# %% [markdown]
# # Static charts
# These are codes to replicate charts from the World Bank to export and edit them in Illustrator

# %% [markdown]
# ## First chart
# In this script I am preparing the data for the static chart included in the Key Insight 'The pandemic
# pushed millions into extreme poverty'.
#
# https://owid.cloud/admin/posts/preview/51861?insight=the-pandemic-pushed-millions-into-extreme-poverty#key-insights-on-poverty
#
# I plot it with plotly and then save it as an svg, which I then have edited in Illustrator by hand.

# %%
from numpy import NaN
import pandas as pd
import plotly.express as px
# %%
povline='2.15'

version='20220909_2017_01_02_PROD'
request_url = f'https://api.worldbank.org/pip/v1/pip-grp?povline={povline}&version={version}&year=all&group_by=wb&format=csv'

df = pd.read_csv(request_url)


# %%
df = df[df['region_name']=="World"]

df = df[["reporting_year", "pop_in_poverty"]].\
    rename(columns={"reporting_year":"year"})

df["estimate"] = "historic"
# %%
# Make dataframes of projections from Poverty and Shared Prosperity report 2022, Figure 0.3
# We match the 2018 value onto the exact value from the API data
value_in_2019 = df[df["year"]==2019]["pop_in_poverty"].values[0]

no_pandemic_df = pd.DataFrame(
    
        {'year': [2019, 2020, 2021, 2022],
        'pop_in_poverty': [value_in_2019/1000000, 629, 612, 596]}

)

no_pandemic_df["estimate"] = "no pandemic"
no_pandemic_df["pop_in_poverty"] = no_pandemic_df["pop_in_poverty"]*1000000


baseline_df = pd.DataFrame(
    
        {'year': [2019, 2020, 2021, 2022],
        'pop_in_poverty': [value_in_2019/1000000, 719, 690, 667]}

)

baseline_df["estimate"] = "baseline"
baseline_df["pop_in_poverty"] = baseline_df["pop_in_poverty"]*1000000


pessimistic_df = pd.DataFrame(
    
        {'year': [2021, 2022],
        'pop_in_poverty': [690, 685]}

)

pessimistic_df["estimate"] = "pessimistic"
pessimistic_df["pop_in_poverty"] = pessimistic_df["pop_in_poverty"]*1000000


# %%
# append projections to historic data
df = pd.concat([
    df, 
    no_pandemic_df, 
    baseline_df,
    pessimistic_df],
        ignore_index=True)

# %%
# Make plot to base ilulstrator design on

# Use only 1990 onwards data – to avoid confusion around the China bump in 1989
df = df[df['year']>=1990]

fig = px.line(df, x="year", y="pop_in_poverty", color='estimate',
        template='none')

fig.update_yaxes(rangemode="tozero")
fig.update_layout(showlegend=False)


fig.show()

# %%
fig.write_image("graphics/global_pov_with_projections.svg")



# %%
# Only keep from 2017 onwards for detail panel of graphic
df = df[df['year']>=2017]


fig = px.line(df, x="year", y="pop_in_poverty", color='estimate',
        template='none')

fig.update_layout(showlegend=False)


fig.show()

# %%
fig.write_image("graphics/global_pov_with_projections_detail_panel.svg")


# %% [markdown]
# ## Second chart
#
# It comes from this [2020 article](https://blogs.worldbank.org/opendata/projecting-global-extreme-poverty-2030-how-close-are-we-world-banks-3-goal), estimating the population in poverty by region and the projection to 2030.
#
# One option to replicate it is to get the (non-projected) data from PIP's API and manually copy the projections from the graph. The oldest version available is more recent than the article, `20210401_2011_02_02_PROD`

# %%
povline='1.9'
# We will use a specific older version of the data in order to match up with the projections.
version='20210401_2011_02_02_PROD'
request_url = f'https://api.worldbank.org/pip/v1/pip-grp?povline={povline}&version={version}&year=all&group_by=wb&format=csv'

df_stacked = pd.read_csv(request_url)
df_stacked = df_stacked[(df_stacked['region_name'] != "World") & 
                       (df_stacked['reporting_year'] >= 1990)].reset_index(drop=True)


# %% [markdown]
# The data from the API does not have the same values. For instance, in 1990 the number of poor in East Asia is 977.17 million people (vs 976.87) and in Latin America and the Caribbean is 69.62 million (vs. 66.3). So this option is discarded.

# %%
df_stacked[(df_stacked['reporting_year'] == 1990)]

# %% [markdown]
# These data also shows missing values for South Asia between 1997 and 2001, so it would also need to be transformed

# %%
fig = px.area(df_stacked, x="reporting_year", y="pop_in_poverty", color="region_name")
fig.show()

# %% [markdown]
# As the graph is visualised with Flourish, the underlying data is available internally as json, so it can be extracted.

# %%
#Based on https://stackoverflow.com/questions/62031809/extracting-javascript-variables-into-python-dictionaries

import re
import json
import requests

url = 'https://flo.uri.sh/visualisation/3963899/embed?auto=1'

html_data = requests.get(url).text
data = re.search(r'_Flourish_data = (\{.*?\});', html_data).group(1)
#data = re.search(r'_Flourish_data_column_names = (\{.*?\});', html_data)

data = json.loads(data)

# uncomment this to print all data:
print(json.dumps(data, indent=4))

#for row in data['data']:
#    print('{:<55}{}'.format(*map(str.strip, row['filter'][:2])))

# %% [markdown]
# The values are show as lists in each row, so further transformations are required.

# %%
df_flourish = pd.DataFrame.from_dict(data['data'])
df_flourish

# %%
values = df_flourish["value"].apply(pd.Series)

# %%
values

# %%
df_stacked = pd.concat([df_flourish, values], axis=1)

cols_dict = {
    0: "Sub-Saharan Africa",
    1: "South Asia",
    2: "Rest of the world",
    3: "Middle East & North Africa",
    4: "Latin America & Caribbean",
    5: "Europe & Central Asia",
    6: "East Asia & Pacific"
}

df_stacked = df_stacked.rename(columns=cols_dict)
df_stacked = df_stacked.rename(columns = {'label': 'year',
                                         'filter': 'c19_estimation',
                                         })
df_stacked = df_stacked.drop(columns=['metadata', 'value'])
df_stacked = df_stacked.rename(columns = {'filter': 'c19_estimation'})

replace_strings = {
    'Historical poverty + COVID-19-baseline\n  forecast': "baseline",
    'Historical poverty + COVID-19-downside\n  forecast': "downside",
    'Historical poverty + Pre-COVID-19\n  forecast': "pre",
}
df_stacked['c19_estimation'] = df_stacked['c19_estimation'].replace(replace_strings)


df_stacked = pd.melt(df_stacked, id_vars=['c19_estimation', 'year'],
                     value_vars=["Europe & Central Asia",
                                    "Rest of the world",
                                    "Latin America & Caribbean",
                                    "Middle East & North Africa",
                                    "Sub-Saharan Africa",
                                    "East Asia & Pacific",
                                    "South Asia"],
                    var_name='region', value_name='pop_poverty')

df_stacked['year'] = df_stacked['year'].astype(int)
df_stacked['pop_poverty'] = df_stacked['pop_poverty'].astype(float)

df_stacked = df_stacked.rename(columns = {'label': 'year',
                                         'filter': 'c19_estimation',
                                         })


# %%
df_stacked

# %%
estimation_list = list(df_stacked['c19_estimation'].unique())

for i in estimation_list:
    fig = px.area(df_stacked[df_stacked['c19_estimation'] == i], x="year", y="pop_poverty", color="region",
                  title=f'Estimation: <b>{i}</b>', template='none')
    fig.add_vrect(x0=2018, x1=2030, line_width=0, fillcolor="#8b9598", opacity=0.2,
                 annotation_text="<b>Projection</b>", annotation_position="top left")

    fig.write_image(f'graphics/global_pov_with_projections_region_{i}.svg')

    fig.show()

# %%
# Calculate global total
df_global = df_stacked.groupby(['c19_estimation','year']).sum()
df_global = df_global.reset_index()
# %%
df_global[df_global['c19_estimation']=="baseline"]


# %%
