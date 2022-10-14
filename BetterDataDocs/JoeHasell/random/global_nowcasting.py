#%%
import pandas as pd
from plotnine import *

#%%

fp = 'https://api.worldbank.org/pip/v1/pip?country=all&year=all&povline=1.9&fill_gaps=false&welfare_type=all&reporting_level=all&version=20220909_2017_01_02_PROD'

df_test = pd.read_csv(fp)

#%%
fp = 'https://raw.githubusercontent.com/owid/notebooks/main/BetterDataDocs/JoeHasell/PIP/data/ppp_2011/final/OWID_internal_upload/admin_database/pip_final.csv'
df_2011 = pd.read_csv(fp)

# %%
fp = 'https://raw.githubusercontent.com/owid/notebooks/main/BetterDataDocs/JoeHasell/PIP/data/ppp_2017/final/OWID_internal_upload/admin_database/pip_final.csv'
df_2017 = pd.read_csv(fp)
# %%

df_plot = df_2017[(df_2017['Entity']=='World') & (df_2017['Year']>=1990)]

df_plot = df_plot[['Year', '$2.15 - total number of people below poverty line']]
df_plot['Estimate_type'] = 'Historical'
df_plot['$2.15 - total number of people below poverty line'] = df_plot['$2.15 - total number of people below poverty line']/1000000 

df_nowcasts = pd.DataFrame(columns= ['Year', '$2.15 - total number of people below poverty line', 'Estimate_type'],
data = [[2019, 648, 'pre_covid'],
        [2020, 629, 'pre_covid'],
        [2021, 612, 'pre_covid'],
        [2022, 596, 'pre_covid'],
        [2019, 648, 'current'],
        [2020, 719, 'current'],
        [2021, 690, 'current'],
        [2022, 667, 'current'],
        [2021, 690, 'pessimistic'],
        [2022, 685, 'pessimistic'],
])

df_plot = pd.concat([df_plot, df_nowcasts], ignore_index=True)
# %%
(
    ggplot(df_plot)  # What data to use
    + aes(x="Year", y='$2.15 - total number of people below poverty line', colour = 'Estimate_type')  # What variable to use
    + geom_line()  # Geometric object to use for drawing
)

