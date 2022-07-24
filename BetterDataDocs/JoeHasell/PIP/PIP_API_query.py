import pandas as pd

def pip_query_country(popshare_or_povline, value, country_code="all", year="all", fill_gaps="true", welfare_type="all", reporting_level="all"):

    # Build query
    request_url = f'https://api.worldbank.org/pip/v1/pip?{popshare_or_povline}={value}&country={country_code}&year={year}&fill_gaps={fill_gaps}&welfare_type={welfare_type}&reporting_level={reporting_level}&format=csv'

    df = pd.read_csv(request_url)

    return df


# For world regions, the popshare query is not available (or rather, it returns nonsense).
def pip_query_region(povline, year="all"):

    # Build query
    request_url = f'https://api.worldbank.org/pip/v1/pip-grp?povline={povline}&year={year}&group_by=wb&format=csv'

    df = pd.read_csv(request_url)

    return df