#%%
import pandas as pd

#%%
# fill_gaps = 'true' 
# popshare = '0.9'
# request_url = f'https://api.worldbank.org/pip/v1/pip?country=all&year=all&popshare={popshare}&fill_gaps={fill_gaps}&welfare_type=all&reporting_level=all&format=csv'
#%%
#... swap this for api call
df_p90_filled = pd.read_csv("data/API_output/percentiles/filled_true/P90.csv")

df_p10_filled = pd.read_csv("data/API_output/percentiles/filled_true/P10.csv")


#%%
df_p90_filled = df_p90_filled[["country_name", "reporting_year"]]

#%%
fill_gaps = 'false' 
popshare = '0.90'
request_url = f'https://api.worldbank.org/pip/v1/pip?country=all&year=all&popshare={popshare}&fill_gaps={fill_gaps}&welfare_type=all&reporting_level=all&format=csv'

df_p90_survey = pd.read_csv(request_url)
df_p10_survey = pd.read_csv(request_url)


#Then compare – say for Botswansa – inequality changes over the interpolation. 

#%%
# Note: region aggregates return incorrect/broken headcount data when requesting povshare.


#%%
# Note: distributional data (median, Dini, deciles etc.) are missing for ~2000 rows,
#  without it being clear why or what the patten is. For instnce Angola in 2000 yes, but 2001 no. 
# Perhaps something to do with interpolation vs extrpolation


#%%
#Note on negative poverty lines returned by Sierra Leone and El Salvador.
# For instance, see El Salvador povshare=0.19 in 1981. Or Sierra Leone 
# poveshare =0.14 in 1990, using the following request

fill_gaps = 'true' 
popshare = '0.19'
request_url = f'https://api.worldbank.org/pip/v1/pip?country=all&year=all&popshare={popshare}&fill_gaps={fill_gaps}&welfare_type=all&reporting_level=all&format=csv'

df = pd.read_csv(request_url)

df[(df['country_name']=='El Salvador') & (df['request_year']==1981)]


#%%
# Monotonicity issues.

# In the filled percentile data (at percentile resolution) it's only Ghana and Guyana.

# In the survey percentile data:
#Ghana 1987 – headcount= .10
#Guyana 1992 – headcoutn - .20
# India 1977 national and rural – headcount - ~.18

# Odd issue with India 1977: the National distribution seems to be (exactly) equal to the Rural distribution.
df_survey %>% filter(country_name=="India", reporting_year ==1977, requested_p<20, requested_p>15) %>% arrange(reporting_level, headcount)


# Sierra Leone in general (filled data) – lots of negative values and lots of monotonicity issues.