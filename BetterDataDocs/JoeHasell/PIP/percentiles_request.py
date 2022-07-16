
#%%
import pandas as pd
import gc

from API_query_lists import percentiles

#%%
request_url_stub = 'https://api.worldbank.org/pip/v1/pip?country=all&year=all&popshare={popshare}&fill_gaps={fill_gaps}&welfare_type=all&reporting_level=all&format=csv'

#%%
# filled/lined up data
fill_gaps = 'true'

# for p in percentiles:
#     print(f"Fetching P{p}")
#     popshare = p/100

#     request_url = request_url_stub.format(popshare = popshare, fill_gaps = fill_gaps)

#     df = pd.read_csv(request_url)

#     df = df.rename(columns={'country_name':'entity', 
#                         'reporting_year':'year'})

#     df = df[['entity', 'year', 'reporting_level', 'welfare_type', 'poverty_line','headcount']]

#     df['requested_p'] = p

#     # Write to .CSV
#     df.to_csv(f'API_output/percentiles/filled_data/P{p}.csv', index=False)


#     # Drop from memory
#     del df
#     gc.collect()
#%%



# for p in percentiles:
#     print(f"Fetching P{p}")
#     popshare = p/100

#     # 'filled'/'lined up' data – countries
#     fill_gaps = 'false'

#     request_url = request_url_stub.format(popshare = popshare, fill_gaps = fill_gaps)

#     df = pd.read_csv(request_url)

#     df = df.rename(columns={'country_name':'entity', 
#                         'reporting_year':'year'})

#     df = df[['entity', 'year', 'reporting_level', 'welfare_type', 'poverty_line','headcount']]

#     df['requested_p'] = p

#     # Write to .CSV
#     df.to_csv(f'API_output/percentiles/filled_data/P{p}.csv', index=False)


#     # Drop from memory
#     del df
#     gc.collect()

#%%
# filled/lined up data
fill_gaps = 'true'
popshare = '0.5'

request_url = request_url_stub.format(popshare = popshare, fill_gaps = fill_gaps)

df = pd.read_csv(request_url)

