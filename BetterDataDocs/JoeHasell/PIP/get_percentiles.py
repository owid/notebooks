
#%%
import pandas as pd
import gc

#%%
#percentiles = [10,20,30,40,50,60,70,80,90]
percentiles = range(1,100, 1)

#%%

for p in percentiles:
    print(f"Fetching P{p}")
    popshare = p/100

    # # survey estimates only
    # request_url = f'https://api.worldbank.org/pip/v1/pip?country=all&year=all&popshare={popshare}&fill_gaps=false&welfare_type=all&reporting_level=all&format=csv'

    # df_survey = pd.read_csv(request_url)

    # # Note we round survey year to nearest integer year
    # df_survey['year'] = round(df_survey['survey_year'])

    # df_survey = df_survey.rename(columns={'country_name':'entity', 
    #                 'poverty_line':'threshold'})

    # df_survey = df_survey[['entity', 'year', 'threshold','headcount']]

    # # Write to .CSV
    # df_survey.to_csv(f'API_output_percentiles/survey_data/P{p}.csv')



    # 'filled'/'lined up' data – countries

    request_url = f'https://api.worldbank.org/pip/v1/pip?country=all&year=all&popshare={popshare}&fill_gaps=true&welfare_type=all&reporting_level=all&format=csv'

    df_filled = pd.read_csv(request_url)

    df_filled = df_filled.rename(columns={'country_name':'entity', 
                        'reporting_year':'year', 
                        'poverty_line':'threshold'})

    df_filled = df_filled[['entity', 'year', 'threshold','headcount']]


    # Write to .CSV
    df_filled.to_csv(f'API_output_percentiles/filled_data/P{p}.csv')


    # Drop from memory
    del df_filled
    gc.collect()
#%%
