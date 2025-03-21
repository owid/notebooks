# %% [markdown]
# # World Bank Poverty and Inequality Platform dataset
#
# ***To get the most updated dataset it is required to run the relative poverty and percentile extraction codes. Choosing "yes" will run the whole program (taking over a day).***
#
# The **Poverty and Inequality Platform (PIP)** is an interactive computational tool that offers users quick access to the World Bank’s estimates of poverty, inequality, and shared prosperity. PIP provides a comprehensive view of global, regional, and country-level trends for more than 150 economies around the world. Users can access to https://pip.worldbank.org/ to see country profiles and regional aggregations of poverty measures. This notebook makes use of the PIP API, which computes all poverty and inequality statistics available at PIP to allow users to set their own poverty lines and download several indicators on poverty and inequality. You can access to the API by clicking [here](https://pip.worldbank.org/api).
#
# World Bank Data are based on primary household survey data obtained from government statistical agencies and World Bank country departments.

# %%
import time
import shutil
from create_dataset_functions import *

# %% [markdown]
# ## Question: Do you want to run the entire program? (over 1 day of running time)
# If you choose `yes` it will run it entirely. When choosing `no` the program just loads the output of these long codes for generating relative poverty measures and income thresholds (plus patching missing medians). All the other variables are generated by queries.

# %%
print('CAUTION: If a full update is needed, first you have to run relative poverty and percentile extraction codes')
print('Together, these codes take over a day to run')

question = "Do you want to generate new percentiles data (running time ~1.5 DAYS)?"
answer_perc = query_yes_no(question)

question = "Do you want to generate new relative poverty data (running time ~1.5 hours)?"
answer_rel = query_yes_no(question)

# %% [markdown]
# ## Inputs
# In this section a set of poverty lines and the International Poverty Line are defined in cents

# %%
start_time = time.time()

#Define PPP version, which will change the poverty lines to query
ppp_version = 2017

if ppp_version == 2011:
    
    # Here we define the poverty lines to query as cents
    poverty_lines_cents = [100, 190, 320, 550, 1000, 2000, 2170, 3000, 4000]
    #Here we define the international poverty line
    extreme_povline_cents = 190
    
elif ppp_version == 2017:
    
    # Here we define the poverty lines to query as cents
    poverty_lines_cents = [100, 215, 365, 685, 1000, 2000, 2435, 3000, 4000]
    #Here we define the international poverty line
    extreme_povline_cents = 215    
    
print(f'The code will use the {ppp_version} PPPs')
    
povlines_count = len(poverty_lines_cents)
print(f'{povlines_count} poverty lines were defined (in cents):')
print(f'{poverty_lines_cents}')

print(f'The international poverty line is defined as (in cents):')
print(f'{extreme_povline_cents}')

# %% [markdown]
# ## Get queries for the International Poverty Line
# Here the code produces the output of PIP queries for countries (with and without inter/extrapolations), together with dataframes filter for only income data, only consumption or both (dropping duplicates). Also regional data is queried.

# %%
df_country, df_country_inc, df_country_cons, df_country_inc_or_cons = country_data(extreme_povline_cents, filled="false", ppp=ppp_version)
df_country_filled, df_country_inc_filled, df_country_cons_filled, df_country_inc_or_cons_filled = country_data(extreme_povline_cents, filled="true", ppp=ppp_version)
df_region = regional_data(extreme_povline_cents, ppp=ppp_version)

# %% [markdown]
# ## Get poverty data for multiple poverty lines
# The PIP data is queried multiple times for each poverty line set in the input section. This data is then made wide to get a `Entity`, `Year`, `reporting_level`, `welfare_type` structure for each row and multiple poverty measures by each poverty line in columns. The poverty measures include headcount, headcount ratio, poverty gap index, income gap ratio, average shortfall, total shortfall, poverty severity, and Watts index 

# %%
df_final = query_poverty(poverty_lines_cents, filled="false", ppp=ppp_version)

# %% [markdown]
# ## Get non-poverty data
# Data not affected by different poverty lines is obtained here. These are measures as population, mean, median, Gini coefficient, decile shares, to name some. This data is then merged with the poverty measures from the previous section. Note: only population and mean income are available by default for world regions.

# %%
df_final = query_non_poverty(df_final, df_country, df_region)

# %% [markdown]
# ## Integrate income thresholds
# If `yes` was selected at the start, it will first generate percentile data for each country and region. It takes between 1 and 2 DAYS. If `no` is selected, the code goes straight to the next step, which is merging the data with the previously generated percentile output.

# %%
df_final = thresholds(df_final, answer=answer_perc, ppp=ppp_version)

# %% [markdown]
# ## Integrate relative poverty data
# If `yes` was selected at the start, it will first generate relative poverty data from different queries for each country. It takes between 1 and 2 hours. If `no` is selected, the code goes straight to the next step, which is merging the data with the previously generated relative poverty output.

# %%
df_final, col_relative = integrate_relative_poverty(df_final, df_country, answer=answer_rel, ppp=ppp_version)

# %% [markdown]
# ## Generate additional variables and check for errors
# These new variables include headcount and headcount ratios in-between and above poverty lines, decile averages and percentile ratios. Also the list of the columns is obtained for the final output.
# Several tests are done to the data as well, related to monotonicity, missing values and stacked variables adding up to 100%. If rows do not follow these criteria, these are dropped.

# %%
df_final, cols = additional_variables_and_check(df_final, poverty_lines_cents, col_relative, ppp=ppp_version)

# %% [markdown]
# ## Patch missing median values
# For several countries (including all national data for China, India and Indonesia) and all the regions there is no median income data. With the percentile output we can patch the blanks by filtering the P50 value.

# %%
df_final = median_patch(df_final, ppp=ppp_version)

# %% [markdown]
# ## Standardise entity values
# Entities are formatted to OWID format and also urban and rural data is marked as such in the `Entity` column

# %%
df_final = standardise(df_final, ppp=ppp_version)

# %% [markdown]
# ## Export data for data explorer
# Three different outputs of the data are generated: only with income surveys, only with consumption surveys and with both, removing duplicates.

# %%
df_inc_only, df_cons_only, df_inc_or_cons = export(df_final, cols, ppp=ppp_version)

# %% [markdown]
# Also multiple files are created to show the breaks between different surveys in a country.

# %%
show_breaks(ppp=ppp_version)

# %% [markdown]
# ## Include metadata and export for main PIP dataset
# The version including both income and consumption data is reprocessed to filter only the required variables for the main PIP dataset. The names of the variables are also reformatted for a more human-friendly reading.

# %%
include_metadata(df_inc_or_cons, ppp=ppp_version)

# %% [markdown]
# ## Create regional headcount dataset
# A second dataset, calculating total headcount for world regions, is generated. When there is one region with missing data the number is obtained by the difference between the world headcount and the rest of the regions. China and India are also included to study the size of their poverty headcounts. Accordingly, the regions `East Asia and Pacific excluding China` and `South Asia excluding India` are created.

# %%
regional_headcount(df_region, df_country_inc_or_cons_filled, ppp=ppp_version)

# %% [markdown]
# ## Create survey count in the past decade dataset
# A third dataset with one variable is generated. This variable is the number of surveys ran in each country in the past decade, in order to compare data availability on poverty.

# %%
survey_count(df_country_inc_or_cons, ppp=ppp_version)

# %% [markdown]
# ## Create 2011 vs 2017 PPPs comparison files
# Data from 2011 and 2017 PPPs is merged to be compared in a 2011 vs 2017 PPPs explorer.

# %%
ppp_comparison()

# %% [markdown]
# ## Create national poverty lines dataset from Jolliffe et al (2022)
# This is the data of the paper which defined new international poverty lines, [here](https://openknowledge.worldbank.org/handle/10986/37061)

# %%
national_povlines()

# %%
end_time = time.time()
elapsed_time = end_time - start_time
print(f'The files were created in {elapsed_time} seconds :)')
print('Update the main PIP dataset with pip_final.csv')
print('Update the regional headcount dataset with pip_regional_headcount.csv')
print('Update the survey count dataset with pip_survey_count.csv')
print('Update the national poverty lines dataset with pip_national_povlines.csv')

# %%
