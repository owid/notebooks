
#%%
from numpy import NaN
import pandas as pd
from PIP_API_query import pip_query_regions
import plotly.express as px



#%%
povline='1.9'
# We will use a specific older version of the data in order to match up with the projections.
version='20220408_2011_02_02_PROD'
request_url = f'https://api.worldbank.org/pip/v1/pip-grp?povline={povline}&version={version}&year=all&group_by=wb&format=csv'

df = pd.read_csv(request_url)


# %%
df = df[df['region_name']=="World"]

df = df[["reporting_year", "pop_in_poverty"]].\
    rename(columns={"reporting_year":"year"})

df["estimate"] = "historic"
# %%
# Make dataframes of projections from https://blogs.worldbank.org/opendata/pandemic-prices-and-poverty
# We match the 2018 value onto the exact value from the API data
value_in_2018 = df[df["year"]==2018]["pop_in_poverty"].values[0]

no_pandemic_df = pd.DataFrame(
    
        {'year': [2018, 2019, 2020, 2021, 2022],
        'pop_in_poverty': [value_in_2018/1000000, 641.4, 621.1, 599.7, 581.3]}

)

no_pandemic_df["estimate"] = "no pandemic"
no_pandemic_df["pop_in_poverty"] = no_pandemic_df["pop_in_poverty"]*1000000


baseline_df = pd.DataFrame(
    
        {'year': [2019, 2020, 2021, 2022],
        'pop_in_poverty': [641.4, 713.8, 684.2, 656.7]}

)

baseline_df["estimate"] = "baseline"
baseline_df["pop_in_poverty"] = baseline_df["pop_in_poverty"]*1000000


pessimistic_df = pd.DataFrame(
    
        {'year': [2021, 2022],
        'pop_in_poverty': [684.2, 676.5]}

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

fig = px.line(df, x="year", y="pop_in_poverty", color='estimate')
fig.show()

# %%

fig.write_image("graphics/global_pov_with_projections.svg")
# %%
