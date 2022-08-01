#%%
import pandas as pd

#%%
# For world regions, the popshare query is not available (or rather, it returns nonsense).


#%%
def p90_10_ratio(select_country, select_year, p90, p10):
    #Check p90 headcount is extremely close to 90%
    print(f"In {select_country}, {select_year}:")

    print(f"We see from the 'popshare' query that P90 and P10 were {p90} and {p10}.")

    print(f"P90/P10 raio is: {p90/p10}")
    
    print("Let's double check these yield the right headcount ratios (i.e. 90% and 10%)")

    fill_gaps = 'true'

    df_p90 = pd.read_csv(f'https://api.worldbank.org/pip/v1/pip?country={select_country}&year={select_year}&povline={p90}&fill_gaps={fill_gaps}&welfare_type=all&reporting_level=all&format=csv')

    heacount_p90 = df_p90['headcount'].values[0]
    print(f"P90 headcount is: {heacount_p90}")

    #Check p10 headcount is extremely close to 10%
    df_p10 = pd.read_csv(f'https://api.worldbank.org/pip/v1/pip?country={select_country}&year={select_year}&povline={p10}&fill_gaps={fill_gaps}&welfare_type=all&reporting_level=all&format=csv')

    heacount_p10 = df_p10['headcount'].values[0]
    print(f"P10 headcount is: {heacount_p10}")

    

#%%
select_country = "BWA"
select_year = 1985

p90 = 8.299255
p10 = 0.731530

p90_10_ratio(select_country,select_year, p90, p10)

#%%
select_country = "BWA"
select_year = 2003

p90 = 19.033194
p10 = 1.021057

p90_10_ratio(select_country,select_year, p90, p10)

#%%
#Check p90 headcount is extremely close to 90%
fill_gaps = 'true'

df_p90 = pd.read_csv(f'https://api.worldbank.org/pip/v1/pip?country={select_country}&year={select_year}&povline={p90}&fill_gaps={fill_gaps}&welfare_type=all&reporting_level=all&format=csv')

p90 = df_p90['headcount'].values[0]






#%%
select_country = "BWA"
select_year = 2003

p90 = 19.868751

#%%
#Check p90 headcount is extremely close to 90%
fill_gaps = 'true'

df_p90 = pd.read_csv(f'https://api.worldbank.org/pip/v1/pip?country={select_country}&year={select_year}&povline={p90}&fill_gaps={fill_gaps}&welfare_type=all&reporting_level=all&format=csv')

p90 = df_p90['headcount'].values[0]





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
# Note: region aggregates return incorrect/broken headcount data when requesting popshare.


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