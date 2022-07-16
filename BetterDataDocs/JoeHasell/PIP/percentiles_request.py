
#%%
import pandas as pd
import gc

from API_query_lists import percentiles

#%%
request_url_stub = 'https://api.worldbank.org/pip/v1/pip?country=all&year=all&popshare={popshare}&fill_gaps={fill_gaps}&welfare_type=all&reporting_level=all&format=csv'

for p in percentiles:

    print(f"Fetching P{p}")
    popshare = p/100

    for fill_gaps in ['true', 'false']:
        print(f"– fill gaps: {fill_gaps}")

        request_url = request_url_stub.format(popshare = popshare, fill_gaps = fill_gaps)

        df = pd.read_csv(request_url)

        df = df[['country_name', 
            'reporting_year', 
            'reporting_level', 
            'welfare_type', 
            'survey_year', 
            'survey_acronym', 
            'survey_comparability', 
            'comparable_spell',
            'poverty_line',
            'headcount']]

        df['requested_p'] = p

        # Write to .CSV
        df.to_csv(f'API_output/percentiles/filled_{fill_gaps}/P{p}.csv', index=False)


        # Drop from memory
        del df
        gc.collect()
