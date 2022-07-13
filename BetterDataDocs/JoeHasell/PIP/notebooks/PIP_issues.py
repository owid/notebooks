#%%


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
# In the percentile data (at percentile resolution) it's only Ghana and Guyana.