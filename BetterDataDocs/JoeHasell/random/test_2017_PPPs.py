#%%
from heapq import merge
import pandas as pd
from plotnine import *

#%%
fp = 'https://raw.githubusercontent.com/owid/notebooks/main/BetterDataDocs/JoeHasell/PIP/data/ppp_2011/final/OWID_internal_upload/admin_database/pip_final.csv'
df_2011 = pd.read_csv(fp)

# %%
fp = 'https://raw.githubusercontent.com/owid/notebooks/main/BetterDataDocs/JoeHasell/PIP/data/ppp_2017/final/OWID_internal_upload/admin_database/pip_final.csv'
df_2017 = pd.read_csv(fp)
# %%


plot_metric = 'Mean income or expenditure per day'

select_entities = ['East Asia and Pacific', 'South Asia','Sub-Saharan Africa', 'Middle East and North Africa', 'Europe and Central Asia', 'Latin America and the Caribbean', 'High income countries', 'World']
select_entities = ['Nigeria', 'United States', 'Colombia', 'France']

# %%
#Compare PPPs

df_compare = pd.merge(df_2011, df_2017, on=['Entity', 'Year'], suffixes=("_2011", "_2017"))


df_compare['mean_ratio'] = df_compare['Mean income or expenditure per day_2017']/df_compare['Mean income or expenditure per day_2011']
# %%

# %%
df_2017_filter = df_2017[df_2017['Entity'].isin(select_entities)]
df_2017_filter['PPPs'] = 2017

df_2011_filter = df_2011[df_2011['Entity'].isin(select_entities)]
df_2011_filter['PPPs'] = 2011


dfs = [df_2017_filter, df_2011_filter]
df_plot = pd.concat(dfs)

# %%
(
    ggplot(df_plot)  # What data to use
    + aes(x="Year", y=plot_metric, colour = 'factor(PPPs)')  # What variable to use
    + geom_line()  # Geometric object to use for drawing
    + facet_wrap('Entity')
)

# %%

# %%
(
    ggplot(df_compare[df_compare['Entity'].isin(select_entities)])  # What data to use
    + aes(x="Year", y='mean_ratio')  # What variable to use
    + geom_line()  # Geometric object to use for drawing
    + facet_wrap('Entity')
)
# %%
br = df_compare[df_compare['mean_ratio']<1]
# %%

(
    ggplot(df_compare[df_compare['Year']==2019])  # What data to use
    + aes(x='Mean income or expenditure per day_2011', y='Mean income or expenditure per day_2017')  # What variable to use
    + geom_point(aes(size='$1.90 - total number of people below poverty line'))
)


# %%
popshare_or_povline = "popshare"
value =1.9
country_code="all"
year="all",
fill_gaps="false"
welfare_type="all"
reporting_level="national"
version= '20220909_2011_02_02_PROD'


request_url = f'https://api.worldbank.org/pip/v1/pip?{popshare_or_povline}={value}&country={country_code}&year={year}&fill_gaps={fill_gaps}&welfare_type={welfare_type}&reporting_level={reporting_level}&version={version}&format=csv'

df_pip_2011 = pd.read_csv(request_url)

# %%

popshare_or_povline = "popshare"
value = 0.235
country_code="ETH"
year="all",
fill_gaps="false"
welfare_type="all"
reporting_level="national"
version= '20220909_2011_02_02_PROD'

request_url = f'https://api.worldbank.org/pip/v1/pip?{popshare_or_povline}={value}&country={country_code}&year={year}&fill_gaps={fill_gaps}&welfare_type={welfare_type}&reporting_level={reporting_level}&version={version}&format=csv'

df_popshare =  pd.read_csv(request_url)
# %%
popshare = 0.235
country_code = 'ETH'
year = 2016


 # Build query
request_url = 'https://api.worldbank.org/pip/v1/pip?' + \
      'country=' + country_code + \
      '&year=' + str(year) + \
      '&popshare=' + str(popshare) + \
      'version=20220909_2017_01_02_PROD' + \
      '&fill_gaps=true' + \
      '&welfare_type=all' + \
      '&reporting_level=national' + \
      '&format=csv'

#%%
country_code = 'ETH'
year = 2016
povline = 10
 # Build query
request_url = 'https://api.worldbank.org/pip/v1/pip?' + \
      'country=' + country_code + \
      '&year=' + 'all' + \
      '&povline=' + str(povline) + \
      'version=20220909_2017_01_02_PROD' + \
      '&fill_gaps=false' + \
      '&welfare_type=all' + \
      '&reporting_level=national' + \
      '&format=csv'

df =  pd.read_csv(request_url)


# %%
