
#%%
import pandas as pd
import requests
import io
import wbgapi as wb


#%%

wb.source.info()
#%%
wb.db = 62     # Database ID for ICP 2011
wb.series.info('110000')


#%%
df = wb.data.DataFrame('SP.POP.TOTL', 'BRA').reset_index()

#%%
df = wb.data.DataFrame({'PA.NUS.PRVT.PP': "PPP_PrivCons_WDI","FP.CPI.TOTL":"CPI_WDI"}, "all", time=range(2011, 2020), columns='series').reset_index()
#%%
def pip_query_country(popshare_or_povline, value, country_code="all", year="all", fill_gaps="true", welfare_type="all", reporting_level="all"):

    # Build query
    request_url = f'https://api.worldbank.org/pip/v1/pip?{popshare_or_povline}={value}&country={country_code}&year={year}&fill_gaps={fill_gaps}&welfare_type={welfare_type}&reporting_level={reporting_level}&format=csv'

    #df = pd.read_csv(request_url)
    response = requests.get(request_url, timeout=200).content
    df = pd.read_csv(io.StringIO(response.decode('utf-8')))

    return df

#%%

df_PIP = pip_query_country("povline", 1.90,fill_gaps="false" )

#%%


df_WDI = wb.data.DataFrame({'PA.NUS.PRVT.PP': "PPP_PrivCons_WDI","FP.CPI.TOTL":"CPI_WDI"}, "all", time=range(2011, 2020), columns='series').reset_index()

# Pivot longer
# %%
# compare WDI and PIP and CPIs


# %%
# Check calculation of annual PPP series – 2017 PPPs updated with ratio of country and US CPI.




# %%
# Pull in global income distribution


# %%
# Add input for your household income and size of household and local currency (just your country)



# %%
# Calculate rough position in global economy. (ideally – where are you in your own country, and where are you globally)


# %%
# Link to country specific searches




