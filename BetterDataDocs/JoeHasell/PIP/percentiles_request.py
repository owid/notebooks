
#%%
import pandas as pd
from pathlib import Path

import gc

from API_query_lists import percentiles

#%%
request_url_stub = 'https://api.worldbank.org/pip/v1/pip?country=all&year=all&popshare={popshare}&fill_gaps={fill_gaps}&welfare_type=all&reporting_level=all&format=csv'



for fill_gaps in ['true', 'false']:

    print(f"– fill gaps: {fill_gaps}")

    for p in percentiles:

        print(f"Fetching P{p}")
        popshare = p/100

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
        df.to_csv(f'data/API_output/percentiles/filled_{fill_gaps}/P{p}.csv', index=False)


        # Drop from memory
        del df
        gc.collect()


    # Gather individual percentiles together into a single file

    # Make a list of all csv files in the relevant folder using pathlib
    all_files = Path(f'data/API_output/percentiles/filled_{fill_gaps}').glob('*.csv')

    # Read in and concat (append together) all the files
    df_gathered = pd.concat((pd.read_csv(f) for f in all_files))

    # Write to .CSV
    df_gathered.to_csv(f'data/intermediate/percentiles/filled_{fill_gaps}/percentiles_before_Gpinter.csv', index=False)

