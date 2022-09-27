import pandas as pd
import requests
import io

def pip_query_country(popshare_or_povline, value, country_code="all", year="all", fill_gaps="true", welfare_type="all", reporting_level="all", ppp_version=2011):

    # Build query
    request_url = f'https://api.worldbank.org/pip/v1/pip?{popshare_or_povline}={value}&country={country_code}&year={year}&fill_gaps={fill_gaps}&welfare_type={welfare_type}&reporting_level={reporting_level}&ppp_version={ppp_version}&format=csv'

    #df = pd.read_csv(request_url)
    response = requests.get(request_url, timeout=500).content
    df = pd.read_csv(io.StringIO(response.decode('utf-8')))

    return df


# For world regions, the popshare query is not available (or rather, it returns nonsense).
def pip_query_region(povline, year="all", ppp_version=2011):

    # Build query
    request_url = f'https://api.worldbank.org/pip/v1/pip-grp?country=all&povline={povline}&year={year}&ppp_version={ppp_version}&group_by=wb&format=csv'

    #df = pd.read_csv(request_url)
    response = requests.get(request_url, timeout=500).content
    df = pd.read_csv(io.StringIO(response.decode('utf-8')))

    return df
