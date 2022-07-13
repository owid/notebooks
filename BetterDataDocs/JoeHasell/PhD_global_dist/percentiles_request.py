
#%%
import pandas as pd
import gc

from API_query_lists import percentiles

#%%

for p in percentiles:
    print(f"Fetching P{p}")
    popshare = p/100


    # 'filled'/'lined up' data – countries

    request_url = f'https://api.worldbank.org/pip/v1/pip?country=all&year=all&popshare={popshare}&fill_gaps=true&welfare_type=all&reporting_level=all&format=csv'

    df_filled = pd.read_csv(request_url)

    df_filled = df_filled.rename(columns={'country_name':'entity', 
                        'reporting_year':'year'})

    df_filled = df_filled[['entity', 'year', 'reporting_level', 'welfare_type', 'poverty_line','headcount']]

    df_filled['requested_p'] = p

    # Write to .CSV
    df_filled.to_csv(f'data/PIP_percentiles_raw/P{p}.csv', index=False)


    # Drop from memory
    del df_filled
    gc.collect()
#%%
