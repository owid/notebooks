import pandas as pd

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
                    hola = table_base['name'][i]
                    print('{}'.format(table_base['name'][i]))
                    #df['name'][j] = table_base['name'][i]
                    j += 1
# -

print('Below ${hola} a day (2017 prices)'.format(hola= povlines_ppp2017['dollars'][1]))

print('{hola}'.format(hola= table_base['name'][0]))

print(table_base['name'][0].format(povlines=povlines_ppp2011['dollars'][1]))

print("My name is {fname}, I'm {age}".format(fname = "John", age = 36))

povlines_ppp2011.dollars[0]

print('{}'.format(table_base['name'][0], povlines_ppp2011['dollars'][1]))

povlines_ppp2011['dollars'][1]

"{}".format(name=table_base['name'][0])


