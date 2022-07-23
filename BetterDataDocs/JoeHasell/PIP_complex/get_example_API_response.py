#%%
import pandas as pd

from API_query_lists import percentiles


# Example of filled data
povline = '1.9'
fill_gaps = 'true'
request_url = f'https://api.worldbank.org/pip/v1/pip?country=all&year=all&povline={povline}&fill_gaps={fill_gaps}&welfare_type=all&reporting_level=all&format=csv'

df = pd.read_csv(request_url)

df.to_csv(f'API_output/example_response_filled.csv', index=False)


# Example of survey data
povline = '1.9'
fill_gaps = 'false'
request_url = f'https://api.worldbank.org/pip/v1/pip?country=all&year=all&povline={povline}&fill_gaps={fill_gaps}&welfare_type=all&reporting_level=all&format=csv'

df = pd.read_csv(request_url)

df.to_csv(f'API_output/example_response_survey.csv', index=False)
