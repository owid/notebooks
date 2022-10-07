import pandas as pd
import numpy as np

# +
#Read Google sheets
sheet_id = '1mR0LPEGlY-wCp1q9lNTlDbVIG65JazKvHL16my9tH8Y'

sheet_name = 'table_base'
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
table_base = pd.read_csv(url)

sheet_name = 'grapher_base'
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
grapher_base = pd.read_csv(url)

sheet_name = 'povlines_ppp2011'
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
povlines_ppp2011 = pd.read_csv(url)

sheet_name = 'povlines_ppp2017'
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
povlines_ppp2017 = pd.read_csv(url)

sheet_name = 'povlines_both'
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
povlines_both = pd.read_csv(url)

sheet_name = 'survey_type'
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
survey_type = pd.read_csv(url)
# -

dict_table = table_base.to_dict('records')
dict_table

survey_type

povlines_ppp2011

# +
df = pd.DataFrame()

j=0
for i in range(len(table_base)):
    for p_2017 in range(len(povlines_ppp2017)):
        for p_2011 in range(len(povlines_ppp2011)):
            for p in range(len(povlines_both)):
                for survey in range(len(survey_type)):
                    df.loc[j, 'name'] = f'Below ${povlines_ppp2011.dollars[p_2011]} a day (2011 prices)'
                    df.loc[j, 'slug'] = f'headcount_ratio_{povlines_ppp2011.cents[p_2011]}_ppp2011'
                    df.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
                    df.loc[j, 'description'] = f'% of population living in households with an income or expenditure per person below ${povlines_ppp2011.dollars[p_2011]} a day (2011 prices).'
                    df.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
                    df.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
                    df.loc[j, 'unit'] = "%"
                    df.loc[j, 'shortUnit'] = "%"
                    df.loc[j, 'tolerance'] = 5
                    df.loc[j, 'retrievedDate'] = np.nan
                    df.loc[j, 'type'] = "Numeric"
                    df.loc[j, 'colorScaleNumericMinValue'] = 0
                    df.loc[j, 'colorScaleNumericBins'] = "3;10;20;30;40;50;60;70;80;90;100"
                    df.loc[j, 'colorScaleEqualSizeBins'] = "true"
                    df.loc[j, 'colorScaleScheme'] = "OrRd"
                    j += 1
# -

df

table_base.loc[0, 'name']

print('Below ${hola} a day (2017 prices)'.format(hola= povlines_ppp2017['dollars'][1]))

print('{hola}'.format(hola= table_base['name'][0]))

print(table_base['name'][0].format(povlines=povlines_ppp2011['dollars'][1]))

print("My name is {fname}, I'm {age}".format(fname = "John", age = 36))

povlines_ppp2011.dollars[0]

print('{}'.format(table_base['name'][0], povlines_ppp2011['dollars'][1]))

povlines_ppp2011['dollars'][1]

"{}".format(name=table_base['name'][0])


