# %% [markdown]
# # PIP issues
# This document is to find issues in the data extracted with World Bank's PIP query

# %% [markdown]
# ## Imports and functions from *functions* folder

# %%
import pandas as pd
import numpy as np
import time
import plotly.express as px
import plotly.io as pio
import requests
import io
pio.renderers.default='jupyterlab+png+colab+notebook_connected+vscode'


# %%
def pip_query_country(popshare_or_povline, value, country_code="all", year="all", fill_gaps="true", welfare_type="all", reporting_level="all"):

    # Build query
    request_url = f'https://api.worldbank.org/pip/v1/pip?{popshare_or_povline}={value}&country={country_code}&year={year}&fill_gaps={fill_gaps}&welfare_type={welfare_type}&reporting_level={reporting_level}&format=csv'

    #df = pd.read_csv(request_url)
    response = requests.get(request_url, timeout=50).content
    df = pd.read_csv(io.StringIO(response.decode('utf-8')))

    return df


# %%
# For world regions, the popshare query is not available (or rather, it returns nonsense).
def pip_query_region(povline, year="all"):

    # Build query
    request_url = f'https://api.worldbank.org/pip/v1/pip-grp?povline={povline}&year={year}&group_by=wb&format=csv'

    #df = pd.read_csv(request_url)
    response = requests.get(request_url, timeout=50).content
    df = pd.read_csv(io.StringIO(response.decode('utf-8')))

    return df


# %% [markdown]
# ## Getting the data

# %%
df_final = pd.read_csv('allthedata.csv')

poverty_lines_cents = [100, 190, 320, 550, 1000, 2000, 3000, 4000]
poverty_lines_cents.sort()

col_ids = ['Entity', 'Year', 'reporting_level', 'welfare_type']
col_avg_shortfall = []
col_headcount = []
col_headcount_ratio = []
col_incomegap = []
col_povertygap = []
col_tot_shortfall = []
col_poverty_severity = []
col_watts = []
col_central = ['mean', 'median', 'reporting_pop']
col_inequality = ['mld', 'gini', 'polarization', 'palma_ratio', 's80_s20_ratio', 'p90_p10_ratio', 'p90_p50_ratio', 'p90_p10_ratio']
col_extra = ['survey_year', 'survey_comparability', 'comparable_spell', 'distribution_type', 'estimation_type',
            'cpi', 'ppp', 'reporting_gdp', 'reporting_pce']

for i in range(len(poverty_lines_cents)):
    col_avg_shortfall.append(f'avg_shortfall_{poverty_lines_cents[i]}')
    col_headcount.append(f'headcount_{poverty_lines_cents[i]}')
    col_headcount_ratio.append(f'headcount_ratio_{poverty_lines_cents[i]}')
    col_incomegap.append(f'income_gap_ratio_{poverty_lines_cents[i]}')
    col_povertygap.append(f'poverty_gap_index_{poverty_lines_cents[i]}')
    col_tot_shortfall.append(f'total_shortfall_{poverty_lines_cents[i]}')
    col_poverty_severity.append(f'poverty_severity_{poverty_lines_cents[i]}')
    col_watts.append(f'watts_{poverty_lines_cents[i]}')

    
# Create average decile income/consumption
col_decile_share = []
col_decile_avg = []
col_decile_thr = []

for i in range(1,11):
    
    if i !=10:
        varname_thr = f'decile{i}_thr'
        col_decile_thr.append(varname_thr)
    
    varname_share = f'decile{i}_share'
    varname_avg = f'decile{i}_avg'
    
    col_decile_share.append(varname_share)
    col_decile_avg.append(varname_avg)
    
    
col_stacked_n = []
col_stacked_pct = []

#For each poverty line in poverty_lines_cents
for i in range(len(poverty_lines_cents)):
    #if it's the first value only get people below this poverty line (and percentage)
    if i == 0:
        varname_n = f'headcount_stacked_below_{poverty_lines_cents[i]}'
        col_stacked_n.append(varname_n)

        varname_pct = f'headcount_ratio_stacked_below_{poverty_lines_cents[i]}'
        col_stacked_pct.append(varname_pct)

    #If it's the last value calculate the people between this value and the previous 
    #and also the people over this poverty line (and percentages)
    elif i == len(poverty_lines_cents)-1:

        varname_n = f'headcount_stacked_below_{poverty_lines_cents[i]}'
        col_stacked_n.append(varname_n)

        varname_pct = f'headcount_ratio_stacked_below_{poverty_lines_cents[i]}'
        col_stacked_pct.append(varname_pct)

        varname_n = f'headcount_stacked_above_{poverty_lines_cents[i]}'
        col_stacked_n.append(varname_n)

        varname_pct = f'headcount_ratio_stacked_above_{poverty_lines_cents[i]}'
        col_stacked_pct.append(varname_pct)

    #If it's any value between the first and the last calculate the people between this value and the previous (and percentage)
    else:
        varname_n = f'headcount_stacked_below_{poverty_lines_cents[i]}'
        col_stacked_n.append(varname_n)

        varname_pct = f'headcount_ratio_stacked_below_{poverty_lines_cents[i]}'
        col_stacked_pct.append(varname_pct)


#Save the relative poverty variables
col_relative = list(df_final.columns)
col_relative = [e for e in col_relative if e not in col_ids + col_central + col_headcount + col_headcount_ratio + col_povertygap + col_tot_shortfall + col_avg_shortfall + col_incomegap + col_stacked_n + col_stacked_pct + col_poverty_severity + col_watts + col_decile_share + col_inequality + col_extra + col_decile_share + col_decile_thr + col_decile_avg]

# %% [markdown]
# ## Missing values
# In this section I look for observations which are missing or with a zero value for the poverty variables. First, I check the null observations:

# %%
cols_to_check = ['reporting_pop'] + col_central + col_headcount + col_headcount_ratio + col_povertygap + col_tot_shortfall + col_avg_shortfall + col_incomegap + col_stacked_n + col_stacked_pct + col_poverty_severity + col_watts + col_decile_share + col_inequality

df_null = df_final[df_final[cols_to_check].isna().any(1)].copy().reset_index(drop=True)
df_null

# %% [markdown]
# 701 rows have at least one null value. But the distribution of them by variable is not uniform:

# %%
# Count number of nulls in all columns of Dataframe
for column_name in cols_to_check:
    column = df_null[column_name]
    # Get the count of nulls in column 
    count = (column.isnull()).sum()
    print(f'Count of nulls in column {column_name} is : {count}')

# %% [markdown]
# ### Selected poverty variables

# %% [markdown]
# The average shortfall and income gap ratio have much more null values compared to the rest of poverty variables. If I exclude them from the analysis (besides poverty severity and the Watts index) I only have one observation with nulls: **Guinea-Bissau** in 1991:

# %%
cols_to_check = col_headcount + col_headcount_ratio + col_povertygap + col_tot_shortfall + col_stacked_n + col_stacked_pct

df_null_selected = df_final[df_final[cols_to_check].isna().any(1)].copy().reset_index(drop=True)
df_null_selected[['Entity', 'Year', 'reporting_level', 'welfare_type'] + cols_to_check]

# %% [markdown]
# ### Poverty severity and Watts index

# %% [markdown]
# Isolating the poverty severity and the Watts index they have 8 null observations, including **Guinea-Bissau 1991**. The others are in **China (2012, 2014, 2015, 2018 and 2019), El Salvador 1989 and Sierra Leone 1989**. 

# %%
cols_to_check = col_poverty_severity + col_watts

df_null_selected = df_final[df_final[cols_to_check].isna().any(1)].copy().reset_index(drop=True)
df_null_selected[['Entity', 'Year', 'reporting_level', 'welfare_type'] + cols_to_check]

# %% [markdown]
# ### Average shortfall and income gap ratio

# %% [markdown]
# 76 different countries show null values for average shortfall and income gap ratio variables.

# %%
cols_to_check = col_avg_shortfall + col_incomegap

df_null_selected = df_final[df_final[cols_to_check].isna().any(1)].copy().reset_index(drop=True)
df_null_selected['Entity'].value_counts()

# %% [markdown]
# ### Mean, median, decile shares and inequality measures

# %% [markdown]
# If mean, median, deciles and inequality statistics are grouped together we have a larger group of nulls:

# %%
cols_to_check = col_central + col_decile_share + col_inequality

df_null_selected = df_final[df_final[cols_to_check].isna().any(1)].copy().reset_index(drop=True)
df_null_selected[['Entity', 'Year', 'reporting_level', 'welfare_type'] + cols_to_check]

# %% [markdown]
# Though a considerable part of the nulls are concentrated on the regional data, so I filter out them:

# %%
#Defining the different aggregations
world_list = ['World']

regions_list = ['East Asia and Pacific', 
           'Europe and Central Asia',
           'Latin America and the Caribbean', 
           'Middle East and North Africa', 
           'South Asia', 
           'Sub-Saharan Africa']

high_income_list = ['High income countries', 'Other high Income']

redundant_countries = ['China - urban', 
                       'China - rural', 
                       'India - urban', 
                       'India - rural', 
                       'Indonesia - urban',
                       'Indonesia - rural']

countries_list = list(set(list(df_final['Entity'].unique())) - set(regions_list) - set(world_list) - set(high_income_list) - set(redundant_countries))

# %% [markdown]
# Now they are 65 different observations with null values for these variables

# %%
df_null_selected_noregions = df_null_selected[~df_null_selected['Entity'].isin(world_list + regions_list + high_income_list)]
df_null_selected_regions = df_null_selected[df_null_selected['Entity'].isin(world_list + regions_list + high_income_list)]
df_null_selected_noregions[['Entity', 'Year', 'reporting_level', 'welfare_type'] + cols_to_check]

# %% [markdown]
# The nulls for mean, median, deciles and inequality statistics are concentrated mostly in Indonesia, China and India:

# %%
df_null_selected_noregions['Entity'].value_counts()

# %% [markdown]
# This is actually all the observations for these three countries.

# %%
df_excluding_null = df_final[~df_final[cols_to_check].isna().any(1)].copy().reset_index(drop=True)
df_excluding_null = df_excluding_null[df_excluding_null['Entity'].isin(['Indonesia', 'China', 'India'])]
df_excluding_null[['Entity', 'Year', 'reporting_level', 'welfare_type'] + cols_to_check]

# %% [markdown]
# And for these three countries only the median is missing.

# %%
# Count number of nulls in all columns of Dataframe
df_null_chn_ind_idn = df_null_selected_noregions[df_null_selected_noregions['Entity'].isin(['Indonesia', 'China', 'India'])].copy().reset_index(drop=True)

for column_name in cols_to_check:
    column = df_null_chn_ind_idn[column_name]
    # Get the count of nulls in column 
    count = (column.isnull()).sum()
    print(f'Count of nulls in column {column_name} is : {count}')

# %% [markdown]
# It is interesting that there are less null values for the share of decile 5 (9) than for the median (62), because one should be obtained from the other. 56/62 missing median values are concentrated in China, India and Indonesia:

# %%
# Count number of nulls in all columns of Dataframe
for column_name in cols_to_check:
    column = df_null_selected_noregions[column_name]
    # Get the count of nulls in column 
    count = (column.isnull()).sum()
    print(f'Count of nulls in column {column_name} is : {count}')

# %% [markdown]
# For regions only mean values are included:

# %%
# Count number of nulls in all columns of Dataframe
for column_name in cols_to_check:
    column = df_null_selected_regions[column_name]
    # Get the count of nulls in column 
    count = (column.isnull()).sum()
    print(f'Count of nulls in column {column_name} is : {count}')

# %% [markdown]
# ### Median

# %% [markdown]
# These are the cases with missing median:

# %%
df_null_selected_median = df_null_selected_noregions[df_null_selected_noregions['median'].isna()].copy().reset_index(drop=True)
df_null_selected_median['Entity'].value_counts()

# %% [markdown]
# ### Inequality indices
# Six observations have their mean log deviation, gini and polarization measures missing: El Salvador 89, Guatemala 98, Guinea-Bissau 91, Guyana 92, Namibia 93 and Sierra Leone 89.

# %%
cols_to_check = col_inequality

df_null_selected = df_final[df_final[cols_to_check].isna().any(1)].copy().reset_index(drop=True)
df_null_selected[['Entity', 'Year', 'reporting_level', 'welfare_type'] + cols_to_check]
df_null_selected_noregions = df_null_selected[~df_null_selected['Entity'].isin(world_list + regions_list + high_income_list)]
df_null_selected_regions = df_null_selected[df_null_selected['Entity'].isin(world_list + regions_list + high_income_list)]
df_null_selected_noregions[['Entity', 'Year', 'reporting_level', 'welfare_type'] + cols_to_check]

# %% [markdown]
# ## Zero values
# What about zero values? 613 observations include at least one value equal to zero.

# %%
cols_to_check = ['reporting_pop'] + col_central + col_headcount + col_headcount_ratio + col_povertygap + col_tot_shortfall + col_avg_shortfall + col_incomegap + col_stacked_n + col_stacked_pct + col_poverty_severity + col_watts + col_decile_share + col_inequality
df_zero = df_final[(df_final[cols_to_check] == 0).any(1)].reset_index(drop=True)
df_zero

# %% [markdown]
# The distribution of zeros is certainly more uniform compared to the nulls:

# %%
# Count number of zeros in all columns of Dataframe
for column_name in cols_to_check:
    column = df_zero[column_name]
    # Get the count of zeros in column 
    count = (column == 0).sum()
    print(f'Count of zeros in column {column_name} is : {count}')

# %% [markdown]
# This is for a reason. See for example this table: the higher number of nulls for the average shortfall and income gap ratio variables is directly associated with the number of zero values for the headcount variable, as this is generated by dividing by the headcount. The higher number of nulls is explained by the sum of headcount zeros and nulls.
#
# | Poverty line | Zero values<br>Headcount | Null values<br>Average shortfall<br>Income gap ratio | Difference | Null values<br>Headcount |
# | --- | --- | --- | --- | --- |
# | 1.0 | 358 | 358 | 0 | 0 |
# | 1.9 | 154 | 154 | 0 | 0 |
# | 3.2 | 54 | 54 | 0 | 0 |
# | 5.5 | 8 | 9 | 1 | 1 |
# | 10 | 3 | 4 | 1 | 1 |
# | 20 | 0 | 1 | 1 | 1 |
# | 30 | 0 | 1 | 1 | 1 |
# | 40 | 0 | 1 | 1 | 1 |

# %% [markdown]
# 76 different countries have 0 values for headcount:

# %%
cols_to_check = col_headcount

df_zero_selected = df_final[(df_final[cols_to_check] == 0).any(1)].reset_index(drop=True)
df_zero_selected['Entity'].value_counts()

# %% [markdown]
# There are more zero values for the Watts index than for the other poverty variables

# %%
cols_to_check = col_poverty_severity + col_watts

df_zero_selected = df_final[(df_final[cols_to_check] == 0).any(1)].copy().reset_index(drop=True)
df_zero_selected[['Entity', 'Year', 'reporting_level', 'welfare_type'] + cols_to_check]

# %% [markdown]
# 77 different countries have zero values for the Watts index (and the poverty severity as well)

# %%
df_zero_selected['Entity'].value_counts()

# %% [markdown]
# If mean, median, deciles and inequality statistics are grouped together we only find one zero value, and it is for `decile1` in the case of <b>Suriname - urban</b>

# %%
cols_to_check = col_central + col_decile_share + col_inequality

df_zero_selected = df_final[(df_final[cols_to_check] == 0).any(1)].copy().reset_index(drop=True)
df_zero_selected[['Entity', 'Year', 'reporting_level', 'welfare_type'] + cols_to_check]

# %% [markdown]
# ## Negative values
# Two observations show negative values

# %%
cols_to_check = [e for e in df_final.columns if e not in col_ids + col_extra]

df_negative = df_final[(df_final[cols_to_check] < 0).any(1)].copy().reset_index(drop=True)
df_negative[['Entity', 'Year', 'reporting_level', 'welfare_type'] + cols_to_check]

# %% [markdown]
# They are concentrated in the stacked headcount (ratio) variables

# %%
# Count number of negative values in all columns of Dataframe
col_negative = []
for column_name in cols_to_check:
    column = df_negative[column_name]
    # Get the count of zeros in column 
    count = (column < 0).sum()
    if count > 0:
        print(f'Count of negatives in column {column_name} is : {count}')
        col_negative.append(column_name)

# %%
df_negative[['Entity', 'Year', 'reporting_level', 'welfare_type'] + col_negative]

# %% [markdown]
# These columns are dropped because they fail monoticity checks for headcount (see monotonicity section).

# %% [markdown]
# ## Missing median values cannot be replaced with the `popshare` command
# The most straightforward solution for patching missing median data would be to obtain them from a `popshare` query for value=0.5, but this does not provide the desired output.
#
# Returning to the countries with missing data:

# %%
df_null_selected_median['Entity'].value_counts()

# %% [markdown]
# Or, more in detail:

# %%
df_null_selected_median['missing_obs'] = df_null_selected_median['Entity'] + "-" + df_null_selected_median['Year'].astype(str) + "-" + df_null_selected_median['reporting_level'] + "-" + df_null_selected_median['welfare_type']
missing_obs_list = list(df_null_selected_median['missing_obs'].unique())
missing_obs_list

# %% [markdown]
# In theory, while `povline` returns the headcount (and other poverty/inequality values) when a poverty line is given, `popshare` returns the poverty line when a population share (headcount) is given. This way, the poverty line the latter command would return when the popshare value is 0.5 is the median income/consumption value

# %%
df_popshare = pip_query_country(
                    popshare_or_povline = "popshare",
                    country_code = "all",
                    value = 0.5,
                    reporting_level = "all",
                    fill_gaps="false")

df_popshare['missing_obs'] = df_popshare['country_name'] + "-" + df_popshare['reporting_year'].astype(str)

df_null_selected_median['missing_obs'] = df_null_selected_median['Entity'] + "-" + df_null_selected_median['Year'].astype(str)
missing_countryyear_list = list(df_null_selected_median['missing_obs'].unique())

df_popshare = df_popshare[df_popshare['missing_obs'].isin(missing_countryyear_list)].reset_index(drop=True)

# %% [markdown]
# Filtering for the countries with missing median, we can see the headcount is in fact ~0.5 for every observation

# %%
df_popshare[['headcount']].describe(include='all')

# %% [markdown]
# The data generated by povshare patches all the missing medians, but in countries like China, India and Indonesia it just replaces national data with rural data, as you can see by deselecting the "national" legend. This is obviously wrong, because the national value should lie between the urban and rural data.

# %%
fig = px.line(df_popshare, x="reporting_year", y="poverty_line", 
              title=f"<b>New medians generated by `povshare`</b><br>Country-years with missing medians",
              color='reporting_level', facet_col="country_name", facet_col_wrap=3, markers=True)
fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
fig.update_yaxes(matches=None)
fig.show()

# %% [markdown]
# If the percentile thresholds are iteratively obtained with the povline command (see `extract_percentiles.py`), the medians can be properly obtained

# %%
df_median = pd.read_csv('percentiles.csv')
df_median = df_median[df_median['target_percentile'] == "P50"].reset_index(drop=True)

df_median_merge = pd.merge(df_final, 
                    df_median[['Entity', 'Year', 'reporting_level', 'welfare_type',
                                    'poverty_line']], 
                    how='left', 
                    on=['Entity', 'Year', 'reporting_level', 'welfare_type'],
                    validate='many_to_one')

#Create the column median2, a combination between the old and new median values
df_median_merge['median2'] = np.where((df_median_merge['median'].isnull()) & ~(df_median_merge['poverty_line'].isnull()), df_median_merge['poverty_line'], df_median_merge['median'])

df_median_merge['missing_obs'] = df_median_merge['Entity'] + "-" + df_median_merge['Year'].astype(str)

df_median_merge = df_median_merge[df_median_merge['missing_obs'].isin(missing_countryyear_list)].reset_index(drop=True)

# %% [markdown]
# And now the national medians lie between the urban and rural observations for China, Indian and Indonesia.

# %%
fig = px.line(df_median_merge, x="Year", y="median2", 
              title=f"<b>New medians generated by brute-force method</b><br>Country-years with missing medians",
              color='reporting_level', facet_col="Entity", facet_col_wrap=3, markers=True)
fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
fig.update_yaxes(matches=None)
fig.show()

# %%
df_median_merge = pd.merge(df_median_merge, 
                    df_popshare[['country_name', 'reporting_year', 'reporting_level', 'welfare_type',
                                    'poverty_line']], 
                    how='left', 
                    left_on=['Entity', 'Year', 'reporting_level', 'welfare_type'],
                    right_on=['country_name', 'reporting_year', 'reporting_level', 'welfare_type'],
                    validate='many_to_one')
df_median_merge

# %% [markdown]
# The missing medians for the countries which are not China, India or Indonesia are fairly similar. The difference seems to be related more with less presition in the brute force method (2 decimals)

# %%
df_median_merge['median_ratio'] = df_median_merge['median2'] / df_median_merge['poverty_line_y']
df_median_merge = df_median_merge[~df_median_merge['Entity'].isin(['China', 'India', 'Indonesia'])].reset_index(drop=True)

df_median_merge.rename(columns={'median2': 'median_bruteforce',
                               'poverty_line_y': 'median_popshare'}, inplace=True)

df_median_merge[['Entity', 'Year', 'reporting_level', 'welfare_type', 'median_bruteforce', 'median_popshare', 'median_ratio']]

# %%
fig = px.scatter(df_median_merge, x="Year", y="median_ratio", color="Entity",
                 hover_data=['median_bruteforce', 'median_popshare'], opacity=0.5,
                 title="<b>Median comparison for missing observations</b><br>Ratio between popshare and brute force methods",
                 log_y=False,
                 height=600)
fig.update_traces(marker=dict(size=10, line=dict(width=0, color='blue')))
fig.show()

# %% [markdown]
# ## Percentage on different poverty lines do not add up to 100%
# For each country-year the total number of people below, between and over multiple poverty lines are estimated to create a stacked chart with the distribution of income/consumption of the population. It is important then that these numbers add together to the total population (the aggregated percentage is 100%)

# %% [markdown]
# One country show issues and it is again **Guinea-Bissau** in 1991: the total for this year is less than 1 (0.64). In the table we can see why: there are no estimation of poor people living below \\$5.5 or any higher poverty line.

# %%
df_final['sum_pct'] = df_final[col_stacked_pct].sum(axis=1)
df_not_1 = df_final[(df_final['sum_pct'] >= 1.00000001) | (df_final['sum_pct'] <= 0.99999999)].copy().reset_index(drop=True)
df_not_1

# %% [markdown]
# ## Percentage for decile shares do not add up to 100%
# Similarly, in the case of decile shares, in every row the sum of `decile1` to `decile10` should be 1

# %% [markdown]
# 9 different countries-years fail in this requirement: **El Salvador 1989, Guatemala 1998, Guinea-Bissau 1991 (again), Guyana 1992, Namibia 1993, Sierra Leone 1989, Somalia 2017, South Sudan 2016 and Zimbabwe 2019**. And this is because every `decile` variable for these observations is null.

# %%
df_final['sum_deciles'] = df_final[col_decile_share].sum(axis=1)
df_not_1 = df_final[((df_final['sum_deciles'] >= 100.000001) | (df_final['sum_deciles'] <= 99.999999))].copy().reset_index(drop=True)
df_not_1 = df_not_1[~df_not_1['Entity'].isin(regions_list + world_list + high_income_list)].reset_index(drop=True)
df_not_1[['Entity', 'Year', 'reporting_level', 'welfare_type'] + col_decile_share + ['sum_deciles']]

# %% [markdown]
# ## Monotonicity checks
# ###  Headcount poverty
#
# As poverty lines increase, the number of people below these poverty lines should increase as well. Let's see if that's the case

# %%
m_check_vars = []
for i in range(len(col_headcount)):
    if i > 0:
        check_varname = f'm_check_{i}'
        df_final[check_varname] = df_final[f'{col_headcount[i]}'] >= df_final[f'{col_headcount[i-1]}']
        m_check_vars.append(check_varname)


# %% [markdown]
# **Croatia, Guinea-Bissau and United Arab Emirates** show issues. This is because for Croatia there are not headcount values for the \\$5.5 poverty line for years between 1981 and 1988. Guinea Bissau 1991 is the same considered for the stacked variables in the previous section and the UAE situation is the strangest of the group: the headcount below the \\$10 poverty line is one order of magnitude greater than the headcount below \\$20

# %%
df_final['check_total'] = df_final[m_check_vars].all(1)
df_check = df_final[df_final['check_total'] == False]
df_check[['Entity', 'Year', 'reporting_level', 'welfare_type'] + col_headcount]

# %%
print('Percentage of errors for each variable')
(len(df_check) - df_check[m_check_vars].sum(0))/len(df_check)*100

# %% [markdown]
# **What if the condition is stricter?** If filter the values not strictly increasing I have more rows: 

# %%
m_check_vars = []
for i in range(len(col_headcount)):
    if i > 0:
        check_varname = f'm_check_{i}'
        df_final[check_varname] = (df_final[f'{col_headcount[i]}'] > df_final[f'{col_headcount[i-1]}'])
        m_check_vars.append(check_varname)


# %% [markdown]
# 382 observations have at least one headcount value equal to the previous one.

# %%
df_final['check_total'] = df_final[m_check_vars].all(1)
df_check = df_final[df_final['check_total'] == False]
df_check[['Entity', 'Year', 'reporting_level', 'welfare_type'] + col_headcount]

# %% [markdown]
# If the zero values for the second headcount are filtered out, we exclude the richest countries with multiple zero headcounts. If I also exclude the second to last headcount ratio values greater than 99, the repeated valued at the top 1% are gone. There are 153 observations left

# %%
df_check = df_check[(df_check[col_headcount[1]] != 0) & (df_check[col_headcount_ratio[-2]] <= 99)]
df_check[['Entity', 'Year', 'reporting_level', 'welfare_type'] + col_headcount]

# %% [markdown]
# All of these issues are concentrated for the first three comparisons (the first four headcounts)

# %%
print('Percentage of errors for each variable')
(len(df_check) - df_check[m_check_vars].sum(0))/len(df_check)*100

# %% [markdown]
# And this is the list of countries showing the issue (mostly advanced economies, probably very few observations at the bottom of the distribution):

# %%
df_check['Entity'].value_counts()

# %% [markdown]
# Further evidence to think about few observations at the bottom is that the fourth headcount ratio for this group of countries ($5.5 poverty line) has a median of 0.73\% and a maximum of 6.36\%. These observations should not be dropped.

# %%
fig = px.histogram(df_check, x=col_headcount_ratio[3], histnorm="percent", marginal="box",
                  title=f"<b>Distribution of values for {col_headcount_ratio[3]}</b>")
fig.show()

# %% [markdown]
# ### Average shortfall
# With this variable there are much more monotonicity issues: 573 observations are affected (*though I am not sure monotonicity should exist*)

# %%
m_check_vars = []
for i in range(len(col_avg_shortfall)):
    if i > 0:
        check_varname = f'm_check_{i}'
        df_final[check_varname] = df_final[f'{col_avg_shortfall[i]}'] >= df_final[f'{col_avg_shortfall[i-1]}']
        m_check_vars.append(check_varname)


# %%
df_final['check_total'] = df_final[m_check_vars].all(1)
df_check = df_final[df_final['check_total'] == False]
df_check[['Entity', 'Year', 'reporting_level', 'welfare_type'] + col_avg_shortfall]

# %% [markdown]
# Excluding null values for the lowest poverty line there are 215 rows with the issue

# %%
df_check = df_check[~df_check[col_avg_shortfall[0]].isnull()]
df_check[['Entity', 'Year', 'reporting_level', 'welfare_type'] + col_avg_shortfall]

# %%
print('Percentage of errors for each variable')
(len(df_check) - df_check[m_check_vars].sum(0))/len(df_check)*100

# %% [markdown]
# ### Income gap ratio
# With this variable there are even more monotonicity issues: 1670 observations are affected (*though I am not sure monotonicity should exist*)

# %%
m_check_vars = []
for i in range(len(col_incomegap)):
    if i > 0:
        check_varname = f'm_check_{i}'
        df_final[check_varname] = df_final[f'{col_incomegap[i]}'] >= df_final[f'{col_incomegap[i-1]}']
        m_check_vars.append(check_varname)


# %%
df_final['check_total'] = df_final[m_check_vars].all(1)
df_check = df_final[df_final['check_total'] == False]
df_check[['Entity', 'Year', 'reporting_level', 'welfare_type'] + col_incomegap]

# %% [markdown]
# Excluding null values for the lowest poverty line there are 1321 rows with the issue

# %%
df_check = df_check[~df_check[col_incomegap[0]].isnull()]
df_check[['Entity', 'Year', 'reporting_level', 'welfare_type'] + col_incomegap]

# %%
print('Percentage of errors for each variable')
(len(df_check) - df_check[m_check_vars].sum(0))/len(df_check)*100

# %% [markdown]
# ### Decile shares

# %%
m_check_vars = []
for i in range(len(col_decile_share)):
    if i > 0:
        check_varname = f'm_check_{i}'
        df_final[check_varname] = df_final[f'{col_decile_share[i]}'] >= df_final[f'{col_decile_share[i-1]}']
        m_check_vars.append(check_varname)


# %% [markdown]
# 286 observations show issues..

# %%
df_final['check_total'] = df_final[m_check_vars].all(1)
df_check = df_final[df_final['check_total'] == False].reset_index(drop=True)
df_check[['Entity', 'Year', 'reporting_level', 'welfare_type'] + col_decile_share]

# %% [markdown]
# ... but they are all because the columns are empty. The same happens with decile averages, which are derived from the shares

# %%
df_check = df_check[~df_check['decile1_share'].isnull()].reset_index(drop=True)
df_check[['Entity', 'Year', 'reporting_level', 'welfare_type'] + col_decile_share]

# %% [markdown]
# ### Decile thresholds

# %%
m_check_vars = []
for i in range(len(col_decile_thr)):
    if i > 0:
        check_varname = f'm_check_{i}'
        df_final[check_varname] = df_final[f'{col_decile_thr[i]}'] >= df_final[f'{col_decile_thr[i-1]}']
        m_check_vars.append(check_varname)


# %% [markdown]
# No issues

# %%
df_final['check_total'] = df_final[m_check_vars].all(1)
df_check = df_final[df_final['check_total'] == False].reset_index(drop=True)
df_check[['Entity', 'Year', 'reporting_level', 'welfare_type'] + col_decile_thr]

# %% [markdown]
# ## Reporting and survey year comparison
# The dataset contains two different year variables. One is `reporting_year`, renamed `year` for OWID processing, which is an integer value, but there is also a `survey_year` which represents when the income/consumption survey is ran in more than one year: the value has decimals representing the weight of the years. 
#
# >The decimal year notation is used when data are collected over **two calendar years**. The number before the decimal
# point refers to the first year of data collection, while the numbers after the decimal point show the proportion of data
# collected in the second year. For example, the Fiji survey (2013.24) was conducted in 2013 and 2014, with 24% of
# the data collected in 2014. For these countries, we use a weighted average of the annual CPI series, where the weights
# are based on the data collection. In the case of Fiji, we use a CPI that is the weighted average of the 2013 and 2014
# CPIs, with weights of 76% and 24%, respectively.
#
# (Atamanov et al. 2018. “April 2018 PovcalNet update: What’s new.” Global Poverty Monitoring Technical Note 1. Washington, DC: World Bank. Footnote 2, available [here](https://documents1.worldbank.org/curated/en/173171524715215230/pdf/April-2018-Povcalnet-Update-What-s-New.pdf))
#
# We can compare these values by dividing them and see how different they are.

# %% [markdown]
# The absolute difference between the values is always less than 1. The cases in which they are more apart are when the survey year is 0.92 greater than the reporting year (Tanzania 91, Vietnam 97, Eswatini 2000). On the other side we have the only observation where reporting year is greater than survey year is Tanzania 2018 (2018 vs 2017.92) 

# %%
df_final['year_diff'] = df_final['Year'] - df_final['survey_year']

fig = px.scatter(df_final, x="Year", y="year_diff", color="Entity",
                 hover_data=['survey_year'], opacity=0.5,
                 title="<b>Reporting year vs Survey year</b><br>Difference between both measures vs reporting year",
                 log_y=False,
                 height=600)
fig.update_traces(marker=dict(size=10, line=dict(width=0, color='blue')))
fig.show()

# %% [markdown]
# Most of the data though is the same. The difference is 0 for about 89% of the data.

# %%
fig = px.histogram(df_final, x="year_diff", nbins=50, histnorm="percent", marginal="box",
                  title=f"<b>Distribution of values for the difference between years</b>")
fig.show()

# %% [markdown]
# For OWID purposes, `reporting_year` is preferred, though `survey_year` is also available.

# %% [markdown]
# ## Aggregation of data
# This section shows how countries and regions aggregations are compared to the world aggregation.

# %%
#Defining the different aggregations
world = ['World']

regions = ['East Asia and Pacific', 
           'Europe and Central Asia',
           'Latin America and the Caribbean', 
           'Middle East and North Africa', 
           'South Asia', 
           'Sub-Saharan Africa']

high_income = ['Other high income']

redundant_countries = ['China - urban', 
                       'China - rural', 
                       'India - urban', 
                       'India - rural', 
                       'Indonesia - urban',
                       'Indonesia - rural']

countries = list(set(list(df_final['Entity'].unique())) - set(regions) - set(world) - set(high_income) - set(redundant_countries))

# %% [markdown]
# On a first visual inspection we can hardly compare the countries data without inter/extrapolations with the world aggregation, because all the countries are never available for the same year. Regarding regional aggregations there is missing headcount data for South Asia between 1997 and 2001 and in Sub Saharan Africa before 1990, but it seems not to be affected for the world aggregation.

# %%
for i in col_headcount:
    fig = px.area(df_final[df_final['Entity'].isin(countries)], x="Year", y=i, color="Entity",
                  title=f'Variable: <b>{i}, countries</b>', template='none', height=450)
    fig.show()
    fig = px.area(df_final[df_final['Entity'].isin(regions)], x="Year", y=i, color="Entity",
                  title=f'Variable: <b>{i}, regions</b>', template='none', height=450)
    fig.show()
    fig = px.area(df_final[df_final['Entity'].isin(world)], x="Year", y=i, color="Entity",
                  title=f'Variable: <b>{i}, world</b>', template='none', height=450)
    fig.show()

# %% [markdown]
# For a more direct comparison we calculate the ratio between the headcount aggregate for countries or regions and the World aggregate provided by the World Bank.

# %%
#Generate dataframes for each level of aggregation
df_countries = df_final[df_final['Entity'].isin(countries)].copy().reset_index(drop=True)
df_regions = df_final[df_final['Entity'].isin(regions)].copy().reset_index(drop=True)
df_world = df_final[df_final['Entity'].isin(world)].copy().reset_index(drop=True)

# %% [markdown]
# We can see the countries aggregations for headcount in different poverty lines fluctuate a lot: between a 2 and 70% of the world aggregation. Similar situation happens with the total shortfall. These aggregations can't be compared.

# %%
df_countries_year = df_countries.groupby(['Year']).sum().reset_index()
df_countries_year['Entity'] = "World (countries)"
df_countries_year = df_countries_year[['Entity', 'Year'] + col_headcount]
df_countries_year = pd.melt(df_countries_year, id_vars=['Year', 'Entity'], value_vars=col_headcount,
                            var_name='headcount_name', value_name='headcount_value')

df_world_year = df_world[['Entity', 'Year'] + col_headcount]
df_world_year = pd.melt(df_world_year, id_vars=['Year', 'Entity'], value_vars=col_headcount,
                            var_name='headcount_name', value_name='headcount_value')

df_world_comparison = pd.merge(df_countries_year,df_world_year, on=['Year','headcount_name'])
df_world_comparison['ratio'] = df_world_comparison['headcount_value_x'] / df_world_comparison['headcount_value_y']

fig = px.line(df_world_comparison, x="Year", y="ratio", color="headcount_name", title='<b>Headcount</b>: Countries aggregations vs. World')
fig.show()

# %% [markdown]
# Regional aggregations are a similar story. The missing data for South Asia and Sub Saharan Africa makes the aggregations less reliable: ranging from 55-70% to almost 100% of the world aggregation. We recommend to not use the regional aggregations together without any transformation. Similar situation happens with the total shortfall.

# %%
df_regions_year = df_regions.groupby(['Year']).sum().reset_index()
df_regions_year['Entity'] = "World (regions)"
df_regions_year = df_regions_year[['Entity', 'Year'] + col_headcount]
df_regions_year = pd.melt(df_regions_year, id_vars=['Year', 'Entity'], value_vars=col_headcount,
                            var_name='headcount_name', value_name='headcount_value')

df_world_year = df_world[['Entity', 'Year'] + col_headcount]
df_world_year = pd.melt(df_world_year, id_vars=['Year', 'Entity'], value_vars=col_headcount,
                            var_name='headcount_name', value_name='headcount_value')

df_world_comparison = pd.merge(df_regions_year,df_world_year, on=['Year','headcount_name'])
df_world_comparison['ratio'] = df_world_comparison['headcount_value_x'] / df_world_comparison['headcount_value_y']

fig = px.line(df_world_comparison, x="Year", y="ratio", color="headcount_name", title='<b>Headcount</b>: Regional aggregation vs. World')
fig.show()

# %% [markdown]
# ## Additional issues
# For world regions, the popshare query is not available (or rather, it returns nonsense).

# %%
regions = pip_query_region(1.9)
regions.columns


# %%
def p90_10_ratio(select_country, select_year, p90, p10):
    #Check p90 headcount is extremely close to 90%
    print(f"In {select_country}, {select_year}:")

    print(f"We see from the 'popshare' query that P90 and P10 were {p90} and {p10}.")

    print(f"P90/P10 ratio is: {p90/p10}")
    
    print("Let's double check these yield the right headcount ratios (i.e. 90% and 10%)")

    fill_gaps = 'true'

    df_p90 = pd.read_csv(f'https://api.worldbank.org/pip/v1/pip?country={select_country}&year={select_year}&povline={p90}&fill_gaps={fill_gaps}&welfare_type=all&reporting_level=all&format=csv')

    heacount_p90 = df_p90['headcount'].values[0]
    print(f"P90 headcount is: {heacount_p90}")

    #Check p10 headcount is extremely close to 10%
    df_p10 = pd.read_csv(f'https://api.worldbank.org/pip/v1/pip?country={select_country}&year={select_year}&povline={p10}&fill_gaps={fill_gaps}&welfare_type=all&reporting_level=all&format=csv')

    heacount_p10 = df_p10['headcount'].values[0]
    print(f"P10 headcount is: {heacount_p10}")


# %%
select_country = "BWA"
select_year = 1985

p90 = 8.299255
p10 = 0.731530

p90_10_ratio(select_country,select_year, p90, p10)

# %%
select_country = "BWA"
select_year = 2003

p90 = 19.033194
p10 = 1.021057

p90_10_ratio(select_country,select_year, p90, p10)

# %%
#Check p90 headcount is extremely close to 90%
fill_gaps = 'true'

df_p90 = pd.read_csv(f'https://api.worldbank.org/pip/v1/pip?country={select_country}&year={select_year}&povline={p90}&fill_gaps={fill_gaps}&welfare_type=all&reporting_level=all&format=csv')

p90 = df_p90['headcount'].values[0]






# %%
select_country = "BWA"
select_year = 2003

p90 = 19.868751

# %%
#Check p90 headcount is extremely close to 90%
fill_gaps = 'true'

df_p90 = pd.read_csv(f'https://api.worldbank.org/pip/v1/pip?country={select_country}&year={select_year}&povline={p90}&fill_gaps={fill_gaps}&welfare_type=all&reporting_level=all&format=csv')

p90 = df_p90['headcount'].values[0]





# %%
fill_gaps = 'false' 
popshare = '0.90'
request_url = f'https://api.worldbank.org/pip/v1/pip?country=all&year=all&popshare={popshare}&fill_gaps={fill_gaps}&welfare_type=all&reporting_level=all&format=csv'

df_p90_survey = pd.read_csv(request_url)
df_p10_survey = pd.read_csv(request_url)


#Then compare – say for Botswansa – inequality changes over the interpolation. 

# %%
# Note: region aggregates return incorrect/broken headcount data when requesting popshare.


# %%
# Note: distributional data (median, Dini, deciles etc.) are missing for ~2000 rows,
#  without it being clear why or what the patten is. For instnce Angola in 2000 yes, but 2001 no. 
# Perhaps something to do with interpolation vs extrpolation


# %%
#Note on negative poverty lines returned by Sierra Leone and El Salvador.
# For instance, see El Salvador povshare=0.19 in 1981. Or Sierra Leone 
# poveshare =0.14 in 1990, using the following request

fill_gaps = 'true' 
popshare = '0.19'
request_url = f'https://api.worldbank.org/pip/v1/pip?country=all&year=all&popshare={popshare}&fill_gaps={fill_gaps}&welfare_type=all&reporting_level=all&format=csv'

df = pd.read_csv(request_url)

df[(df['country_name']=='El Salvador') & (df['reporting_year']==1981)]


# %%
# Monotonicity issues.

# In the filled percentile data (at percentile resolution) it's only Ghana and Guyana.

# In the survey percentile data:
#Ghana 1987 – headcount= .10
#Guyana 1992 – headcoutn - .20
# India 1977 national and rural – headcount - ~.18

# Odd issue with India 1977: the National distribution seems to be (exactly) equal to the Rural distribution.
df_survey %>% filter(country_name=="India", reporting_year ==1977, requested_p<20, requested_p>15) %>% arrange(reporting_level, headcount)


# Sierra Leone in general (filled data) – lots of negative values and lots of monotonicity issues.
