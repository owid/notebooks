# %% [markdown]
# # Brute force algorithm to get all the percentiles from the PIP API

# %%
import pandas as pd
from functions.PIP_API_query import pip_query_country, pip_query_region
from functions.standardize_entities import standardize_entities
import time
import plotly.express as px

# %% [markdown]
# ## Countries data

# %%
query_durations = {"povline":[],"duration":[]}

# %%
# Define list of poverty lines to query (max 500 requests per category)

under_5_dollars = list(range(1,500, 1))

between_5_and_10_dollars = list(range(500,1000, 1))

between_10_and_20_dollars = list(range(1000,2000, 2))

between_20_and_30_dollars = list(range(2000,3000, 2))

between_30_and_55_dollars = list(range(3000,5500, 5))

between_55_and_80_dollars = list(range(5500,8000, 5))

between_80_and_100_dollars = list(range(8000,10000, 5))

between_100_and_150_dollars = list(range(10000,15000, 10))

between_150_and_175_dollars = list(range(15000,17500, 10))

# %%
povline_list_dict = {
    'under_5_dollars': under_5_dollars, 
    'between_5_and_10_dollars': between_5_and_10_dollars,
    'between_10_and_20_dollars': between_10_and_20_dollars,
    'between_20_and_30_dollars': between_20_and_30_dollars,
    'between_30_and_55_dollars': between_30_and_55_dollars,
    'between_55_and_80_dollars': between_55_and_80_dollars,
    'between_80_and_100_dollars': between_80_and_100_dollars,
    'between_100_and_150_dollars': between_100_and_150_dollars,
    'between_150_and_175_dollars': between_150_and_175_dollars
                   }

# %%
start_time_overall = time.time()

for key in povline_list_dict:


    df_complete = pd.DataFrame()


    for povline in povline_list_dict[key]:

        start_time = time.time()

        povline_dollars = povline/100
        print(f'Fetching headcounts for: ${povline_dollars} a day')


        #For China, India and Indonesia use on the second line: CHN&country=IND&country=IDN
        df = pip_query_country("povline", povline_dollars, 
                        "USA", 
                        "all", "false", "all", "all")



        df_complete = pd.concat([df_complete, df],ignore_index=True)


        end_time = time.time()
        query_durations["povline"].append(povline_dollars)
        query_durations["duration"].append(end_time - start_time)


    #Write the complete data to csv
    df_complete.to_csv(f'data/full_dist/{key}.csv', index=False)

end_time_overall = time.time()


# %%
elapsed_time_overall = end_time_overall - start_time_overall

print(f'Execution time: {elapsed_time_overall/60} minutes')

# %%
# Take a look at how long each query took
df_query_durations = pd.DataFrame.from_dict(query_durations)

fig = px.line(df_query_durations, x="povline", y="duration", title=f'Execution time for poverty line queries')
fig.show()

fig.write_image(f'graphics/time_plot.svg')


# %%
povline_list_dict = {
    'under_5_dollars': under_5_dollars, 
    'between_5_and_10_dollars': between_5_and_10_dollars,
    'between_10_and_20_dollars': between_10_and_20_dollars,
    'between_20_and_30_dollars': between_20_and_30_dollars,
    'between_30_and_55_dollars': between_30_and_55_dollars,
    'between_55_and_80_dollars': between_55_and_80_dollars,
    'between_80_and_100_dollars': between_80_and_100_dollars,
    'between_100_and_150_dollars': between_100_and_150_dollars,
    'between_150_and_175_dollars': between_150_and_175_dollars
                   }


df_complete = pd.DataFrame()
for key in povline_list_dict:
    df = pd.read_csv(f'data/full_dist/{key}.csv')
    df_complete = pd.concat([df_complete, df], ignore_index=True)

# %%
# Find closest to percentiles

start_time = time.time()

percentiles = range(1, 100, 1)

df_closest_complete = pd.DataFrame()

for p in percentiles:

    df_complete['distance_to_p'] = abs(df_complete['headcount']-p/100)

    df_closest = df_complete.sort_values("distance_to_p").groupby(['country_name', 'reporting_year','reporting_level','welfare_type'], as_index=False).first()
    
    df_closest['target_percentile'] = f'P{p}'

    df_closest = df_closest[['country_name', 'reporting_year','reporting_level','welfare_type', 'target_percentile', 'poverty_line', 'headcount', 'distance_to_p']]

    df_closest_complete = pd.concat([df_closest_complete, df_closest],ignore_index=True)
    
end_time = time.time()
print(f'Execution time: {end_time - start_time} seconds')

# %%
fig = px.scatter(df_closest_complete, x="target_percentile", y="distance_to_p", color="country_name",
                 hover_data=['poverty_line', 'headcount', 'reporting_year'], opacity=0.5,
                 title="<b>Target p vs. Distance to p</b><br>Percentiles",
                 log_y=False,
                 height=600)
fig.update_traces(marker=dict(size=10, line=dict(width=0, color='blue')))
fig.show()
fig.write_image(f'graphics/target_p_vs_distance_percentiles.svg')
fig.write_html(f'graphics/target_p_vs_distance_percentiles.html')

# %%
fig = px.scatter(df_closest_complete, x="poverty_line", y="distance_to_p", color="country_name",
                 hover_data=['poverty_line', 'headcount', 'reporting_year', 'target_percentile'], opacity=0.5,
                 title="<b>Poverty line vs. Distance to p</b><br>Percentiles",
                 log_y=False,
                 height=600)
fig.update_traces(marker=dict(size=10, line=dict(width=0, color='blue')))
fig.show()
fig.write_image(f'graphics/povline_vs_distance_percentiles.svg')
fig.write_html(f'graphics/povline_vs_distance_percentiles.html')

# %%
fig = px.histogram(df_closest_complete, x="distance_to_p", histnorm="percent", marginal="box")
fig.show()
fig.write_image(f'graphics/distance_percentiles_histogram.svg')
fig.write_html(f'graphics/distance_percentiles_histogram.html')

# %%
deciles = []

for i in range(10,100,10):
    deciles.append(f'P{i}')
    
df_closest_deciles = df_closest_complete[df_closest_complete['target_percentile'].isin(deciles)].copy().reset_index(drop=True)

fig = px.scatter(df_closest_deciles, x="target_percentile", y="distance_to_p", color="country_name",
                 hover_data=['poverty_line', 'headcount', 'reporting_year'], opacity=0.5,
                 title="<b>Target p vs. Distance to p</b><br>Deciles",
                 log_y=False,
                 height=600)
fig.update_traces(marker=dict(size=10, line=dict(width=0, color='blue')))
fig.show()
fig.write_image(f'graphics/target_p_vs_distance_deciles.svg')
fig.write_html(f'graphics/target_p_vs_distance_deciles.html')

# %%
deciles = []

for i in range(10,100,10):
    deciles.append(f'P{i}')
    
df_closest_deciles = df_closest_complete[df_closest_complete['target_percentile'].isin(deciles)].copy().reset_index(drop=True)

fig = px.scatter(df_closest_deciles, x="poverty_line", y="distance_to_p", color="country_name",
                 hover_data=['poverty_line', 'headcount', 'reporting_year', 'target_percentile'], opacity=0.5,
                 title="<b>Poverty line vs. Distance to p</b><br>Deciles",
                 log_y=False,
                 height=600)
fig.update_traces(marker=dict(size=10, line=dict(width=0, color='blue')))
fig.show()
fig.write_image(f'graphics/povline_vs_distance_deciles.svg')
fig.write_html(f'graphics/povline_vs_distance_deciles.html')

# %%
fig = px.histogram(df_closest_deciles, x="distance_to_p", histnorm="percent", marginal="box")
fig.show()
fig.write_image(f'graphics/distance_deciles_histogram.svg')
fig.write_html(f'graphics/distance_deciles_histogram.html')

# %%

df_closest_complete.to_csv('data/full_dist/percentiles_countries.csv', index=False)

# %% [markdown]
# ## Regional data

# %%
query_durations_regions = {"povline":[],"duration":[]}

# %%
# Define list of poverty lines to query (max 500 requests per category)

under_5_dollars = list(range(1,500, 1))

between_5_and_10_dollars = list(range(500,1000, 1))

between_10_and_20_dollars = list(range(1000,2000, 2))

between_20_and_30_dollars = list(range(2000,3000, 2))

between_30_and_55_dollars = list(range(3000,5500, 5))

between_55_and_80_dollars = list(range(5500,8000, 5))

between_80_and_100_dollars = list(range(8000,10000, 5))

between_100_and_150_dollars = list(range(10000,15000, 10))

# %%
povline_list_dict = {
    'under_5_dollars': under_5_dollars, 
    'between_5_and_10_dollars': between_5_and_10_dollars,
    'between_10_and_20_dollars': between_10_and_20_dollars,
    'between_20_and_30_dollars': between_20_and_30_dollars,
    'between_30_and_55_dollars': between_30_and_55_dollars,
    'between_55_and_80_dollars': between_55_and_80_dollars,
    'between_80_and_100_dollars': between_80_and_100_dollars,
    'between_100_and_150_dollars': between_100_and_150_dollars
                   }

# %%
start_time_overall = time.time()

for key in povline_list_dict:


    df_complete_regions = pd.DataFrame()


    for povline in povline_list_dict[key]:

        start_time = time.time()

        povline_dollars = povline/100
        print(f'Fetching headcounts for: ${povline_dollars} a day')


        df = pip_query_region(povline=povline_dollars)

        df_complete_regions = pd.concat([df_complete_regions, df],ignore_index=True)


        end_time = time.time()
        query_durations_regions["povline"].append(povline_dollars)
        query_durations_regions["duration"].append(end_time - start_time)


    #Write the complete data to csv
    df_complete_regions.to_csv(f'data/full_dist_regions/{key}_regions.csv', index=False)

end_time_overall = time.time()


# %%
elapsed_time_overall = end_time_overall - start_time_overall

print(f'Execution time for regions: {elapsed_time_overall/60} minutes')

# %%
# Take a look at how long each query took
df_query_durations_regions = pd.DataFrame.from_dict(query_durations_regions)

fig = px.line(df_query_durations_regions, x="povline", y="duration", title=f'Execution time for poverty line queries (regions)')
fig.show()

fig.write_image(f'graphics/time_plot_regions.svg')


# %%
df_complete_regions = pd.DataFrame()
for key in povline_list_dict:
    df = pd.read_csv(f'data/full_dist_regions/{key}_regions.csv')
    df_complete_regions = pd.concat([df_complete_regions, df], ignore_index=True)

# %%
# Find closest to percentiles

start_time = time.time()

percentiles = range(1, 100, 1)

df_closest_complete_regions = pd.DataFrame()

for p in percentiles:

    df_complete_regions['distance_to_p'] = abs(df_complete_regions['headcount']-p/100)

    df_closest = df_complete_regions.sort_values("distance_to_p").groupby(['region_name', 'reporting_year'], as_index=False).first()
    
    df_closest['target_percentile'] = f'P{p}'

    df_closest = df_closest[['region_name', 'reporting_year', 'target_percentile', 'poverty_line', 'headcount', 'distance_to_p']]

    df_closest_complete_regions = pd.concat([df_closest_complete_regions, df_closest],ignore_index=True)
    
end_time = time.time()
print(f'Execution time: {end_time - start_time} seconds')

# %%
fig = px.scatter(df_closest_complete_regions, x="target_percentile", y="distance_to_p", color="region_name",
                 hover_data=['poverty_line', 'headcount', 'reporting_year'], opacity=0.5,
                 title="<b>Target p vs. Distance to p for regions</b><br>Percentiles",
                 log_y=False,
                 height=600)
fig.update_traces(marker=dict(size=10, line=dict(width=0, color='blue')))
fig.show()
fig.write_image(f'graphics/target_p_vs_distance_percentiles_regions.svg')
fig.write_html(f'graphics/target_p_vs_distance_percentiles_regions.html')

# %%
fig = px.scatter(df_closest_complete_regions, x="poverty_line", y="distance_to_p", color="region_name",
                 hover_data=['poverty_line', 'headcount', 'reporting_year', 'target_percentile'], opacity=0.5,
                 title="<b>Poverty line vs. Distance to p for regions</b><br>Percentiles",
                 log_y=False,
                 height=600)
fig.update_traces(marker=dict(size=10, line=dict(width=0, color='blue')))
fig.show()
fig.write_image(f'graphics/povline_vs_distance_percentiles_regions.svg')
fig.write_html(f'graphics/povline_vs_distance_percentiles_regions.html')

# %%
fig = px.histogram(df_closest_complete_regions, x="distance_to_p", histnorm="percent", marginal="box")
fig.show()
fig.write_image(f'graphics/distance_percentiles_histogram_regions.svg')
fig.write_html(f'graphics/distance_percentiles_histogram_regions.html')

# %%
deciles = []

for i in range(10,100,10):
    deciles.append(f'P{i}')
    
df_closest_deciles_regions = df_closest_complete_regions[df_closest_complete_regions['target_percentile'].isin(deciles)].copy().reset_index(drop=True)

fig = px.scatter(df_closest_deciles_regions, x="target_percentile", y="distance_to_p", color="region_name",
                 hover_data=['poverty_line', 'headcount', 'reporting_year'], opacity=0.5,
                 title="<b>Target p vs. Distance to p for regions</b><br>Deciles",
                 log_y=False,
                 height=600)
fig.update_traces(marker=dict(size=10, line=dict(width=0, color='blue')))
fig.show()
fig.write_image(f'graphics/target_p_vs_distance_deciles_regions.svg')
fig.write_html(f'graphics/target_p_vs_distance_deciles_regions.html')

# %%
deciles = []

for i in range(10,100,10):
    deciles.append(f'P{i}')
    
df_closest_deciles_regions = df_closest_complete_regions[df_closest_complete_regions['target_percentile'].isin(deciles)].copy().reset_index(drop=True)

fig = px.scatter(df_closest_deciles_regions, x="poverty_line", y="distance_to_p", color="region_name",
                 hover_data=['poverty_line', 'headcount', 'reporting_year', 'target_percentile'], opacity=0.5,
                 title="<b>Poverty line vs. Distance to p for regions</b><br>Deciles",
                 log_y=False,
                 height=600)
fig.update_traces(marker=dict(size=10, line=dict(width=0, color='blue')))
fig.show()
fig.write_image(f'graphics/povline_vs_distance_deciles_regions.svg')
fig.write_html(f'graphics/povline_vs_distance_deciles_regions.html')

# %%
fig = px.histogram(df_closest_deciles_regions, x="distance_to_p", histnorm="percent", marginal="box")
fig.show()
fig.write_image(f'graphics/distance_deciles_histogram_regions.svg')
fig.write_html(f'graphics/distance_deciles_histogram_regions.html')

# %%
df_closest_complete_regions.to_csv('data/full_dist_regions/percentiles_regions.csv', index=False)

# %% [markdown]
# ## Merge countries and regional data

# %%
df_closest_complete = pd.read_csv('data/full_dist/percentiles_countries.csv')
df_closest_complete_regions = pd.read_csv('data/full_dist_regions/percentiles_regions.csv')

df_closest_complete = df_closest_complete.rename(columns={'country_name': 'Entity',
                                                          'reporting_year': 'Year'})
df_closest_complete_regions = df_closest_complete_regions.rename(columns={'region_name': 'Entity',
                                                                          'reporting_year': 'Year'})

df_percentiles = pd.concat([df_closest_complete, df_closest_complete_regions], ignore_index=True)

# %%
df_percentiles.to_csv('data/final/OWID_internal_upload/additional_files/percentiles.csv', index=False)
#To use it in PIP issues
df_percentiles.to_csv('notebooks/percentiles.csv', index=False)

# %%
