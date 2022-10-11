import pandas as pd
import numpy as np

# +
#Read Google sheets
sheet_id = '1mR0LPEGlY-wCp1q9lNTlDbVIG65JazKvHL16my9tH8Y'

# sheet_name = 'table_base'
# url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
# table_base = pd.read_csv(url)

# sheet_name = 'grapher_base'
# url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
# grapher_base = pd.read_csv(url)

sheet_name = 'povlines_ppp2011'
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
povlines_ppp2011 = pd.read_csv(url)

sheet_name = 'povlines_ppp2017'
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
povlines_ppp2017 = pd.read_csv(url)

sheet_name = 'povlines_both'
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
povlines_both = pd.read_csv(url)

sheet_name = 'povlines_rel'
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
povlines_rel = pd.read_csv(url)

sheet_name = 'survey_type'
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
survey_type = pd.read_csv(url)
# -

p_2017 = 0
p_2011 = 0
p = 0
survey = 0

table_base = {
0: {'name': f'Below ${povlines_ppp2011.dollars_text[p_2011]} a day (2011 prices)',
  'slug': f'headcount_ratio_{povlines_ppp2011.cents[p_2011]}_ppp2011',
  'sourceName': 'World Bank Poverty and Inequality Platform',
  'description': f'% of population living in households with an income or expenditure per person below ${povlines_ppp2011.dollars[p_2011]} a day (2011 prices).',
  'sourceLink': 'https://pip.worldbank.org/',
  'dataPublishedBy': 'World Bank Poverty and Inequality Platform (PIP)',
  'unit': '%',
  'shortUnit': '%',
  'tolerance': 5,
  'retrievedDate': np.nan,
  'type': 'Numeric',
  'colorScaleNumericMinValue': 0,
  'colorScaleNumericBins': '3;10;20;30;40;50;60;70;80;90;100',
  'colorScaleEqualSizeBins': 'true',
  'colorScaleScheme': 'OrRd'},
1: {'name': f'Below ${povlines_ppp2017.dollars_text[p_2017]} a day (2017 prices)',
  'slug': f'headcount_ratio_{povlines_ppp2017.cents[p_2017]}_ppp2017',
  'sourceName': 'World Bank Poverty and Inequality Platform',
  'description': f'% of population living in households with an income or expenditure per person below ${povlines_ppp2017.dollars_text[p_2017]} a day (2017 prices).',
  'sourceLink': 'https://pip.worldbank.org/',
  'dataPublishedBy': 'World Bank Poverty and Inequality Platform (PIP)',
  'unit': '%',
  'shortUnit': '%',
  'tolerance': 5,
  'retrievedDate': np.nan,
  'type': 'Numeric',
  'colorScaleNumericMinValue': 0,
  'colorScaleNumericBins': '3;10;20;30;40;50;60;70;80;90;100',
  'colorScaleEqualSizeBins': 'true',
  'colorScaleScheme': 'OrRd'},
2: {'name': f'Below ${povlines_ppp2011.dollars_text[p_2011]} a day (2011 prices)',
  'slug': f'headcount_{povlines_ppp2011.cents[p_2011]}_ppp2011',
  'sourceName': 'World Bank Poverty and Inequality Platform',
  'description': f'Number of people living in households with an income or expenditure per person below ${povlines_ppp2011.dollars_text[p_2011]} a day (2011 prices).',
  'sourceLink': 'https://pip.worldbank.org/',
  'dataPublishedBy': 'World Bank Poverty and Inequality Platform (PIP)',
  'unit': np.nan,
  'shortUnit': np.nan,
  'tolerance': 5,
  'retrievedDate': np.nan,
  'type': 'Numeric',
  'colorScaleNumericMinValue': 0,
  'colorScaleNumericBins': '100000;300000;1000000;3000000;10000000;30000000;100000000;300000000;1000000000;1000000001',
  'colorScaleEqualSizeBins': 'true',
  'colorScaleScheme': 'Reds'},
3: {'name': f'Below ${povlines_ppp2017.dollars_text[p_2017]} a day (2017 prices)',
  'slug': f'headcount_{povlines_ppp2017.cents[p_2017]}_ppp2017',
  'sourceName': 'World Bank Poverty and Inequality Platform',
  'description': f'Number of people living in households with an income or expenditure per person below ${povlines_ppp2017.dollars_text[p_2017]} a day (2017 prices).',
  'sourceLink': 'https://pip.worldbank.org/',
  'dataPublishedBy': 'World Bank Poverty and Inequality Platform (PIP)',
  'unit': np.nan,
  'shortUnit': np.nan,
  'tolerance': 5,
  'retrievedDate': np.nan,
  'type': 'Numeric',
  'colorScaleNumericMinValue': 0,
  'colorScaleNumericBins': '100000;300000;1000000;3000000;10000000;30000000;100000000;300000000;1000000000;1000000001',
  'colorScaleEqualSizeBins': 'true',
  'colorScaleScheme': 'Reds'}
}

table_base = [
{'name': f'Below ${povlines_ppp2011.dollars_text[p_2011]} a day (2011 prices)',
  'slug': f'headcount_ratio_{povlines_ppp2011.cents[p_2011]}_ppp2011',
  'sourceName': 'World Bank Poverty and Inequality Platform',
  'description': f'% of population living in households with an income or expenditure per person below ${povlines_ppp2011.dollars[p_2011]} a day (2011 prices).',
  'sourceLink': 'https://pip.worldbank.org/',
  'dataPublishedBy': 'World Bank Poverty and Inequality Platform (PIP)',
  'unit': '%',
  'shortUnit': '%',
  'tolerance': 5,
  'retrievedDate': np.nan,
  'type': 'Numeric',
  'colorScaleNumericMinValue': 0,
  'colorScaleNumericBins': '3;10;20;30;40;50;60;70;80;90;100',
  'colorScaleEqualSizeBins': 'true',
  'colorScaleScheme': 'OrRd'},
{'name': f'Below ${povlines_ppp2017.dollars_text[p_2017]} a day (2017 prices)',
  'slug': f'headcount_ratio_{povlines_ppp2017.cents[p_2017]}_ppp2017',
  'sourceName': 'World Bank Poverty and Inequality Platform',
  'description': f'% of population living in households with an income or expenditure per person below ${povlines_ppp2017.dollars_text[p_2017]} a day (2017 prices).',
  'sourceLink': 'https://pip.worldbank.org/',
  'dataPublishedBy': 'World Bank Poverty and Inequality Platform (PIP)',
  'unit': '%',
  'shortUnit': '%',
  'tolerance': 5,
  'retrievedDate': np.nan,
  'type': 'Numeric',
  'colorScaleNumericMinValue': 0,
  'colorScaleNumericBins': '3;10;20;30;40;50;60;70;80;90;100',
  'colorScaleEqualSizeBins': 'true',
  'colorScaleScheme': 'OrRd'},
{'name': f'Below ${povlines_ppp2011.dollars_text[p_2011]} a day (2011 prices)',
  'slug': f'headcount_{povlines_ppp2011.cents[p_2011]}_ppp2011',
  'sourceName': 'World Bank Poverty and Inequality Platform',
  'description': f'Number of people living in households with an income or expenditure per person below ${povlines_ppp2011.dollars_text[p_2011]} a day (2011 prices).',
  'sourceLink': 'https://pip.worldbank.org/',
  'dataPublishedBy': 'World Bank Poverty and Inequality Platform (PIP)',
  'unit': np.nan,
  'shortUnit': np.nan,
  'tolerance': 5,
  'retrievedDate': np.nan,
  'type': 'Numeric',
  'colorScaleNumericMinValue': 0,
  'colorScaleNumericBins': '100000;300000;1000000;3000000;10000000;30000000;100000000;300000000;1000000000;1000000001',
  'colorScaleEqualSizeBins': 'true',
  'colorScaleScheme': 'Reds'},
{'name': f'Below ${povlines_ppp2017.dollars_text[p_2017]} a day (2017 prices)',
  'slug': f'headcount_{povlines_ppp2017.cents[p_2017]}_ppp2017',
  'sourceName': 'World Bank Poverty and Inequality Platform',
  'description': f'Number of people living in households with an income or expenditure per person below ${povlines_ppp2017.dollars_text[p_2017]} a day (2017 prices).',
  'sourceLink': 'https://pip.worldbank.org/',
  'dataPublishedBy': 'World Bank Poverty and Inequality Platform (PIP)',
  'unit': np.nan,
  'shortUnit': np.nan,
  'tolerance': 5,
  'retrievedDate': np.nan,
  'type': 'Numeric',
  'colorScaleNumericMinValue': 0,
  'colorScaleNumericBins': '100000;300000;1000000;3000000;10000000;30000000;100000000;300000000;1000000000;1000000001',
  'colorScaleEqualSizeBins': 'true',
  'colorScaleScheme': 'Reds'}
]

# +
df = pd.DataFrame()
df_complete = pd.DataFrame()

j=0

for key in range(len(table_base)):
    for p_2017 in range(len(povlines_ppp2017)):
        for p_2011 in range(len(povlines_ppp2011)):
            for p in range(len(povlines_both)):
                for survey in range(len(survey_type)):
                    df.loc[j, 'name'] = table_base[key]['name']
                    df.loc[j, 'slug'] = table_base[key]['slug']
                    df.loc[j, 'sourceName'] = table_base[key]['sourceName']
                    df.loc[j, 'description'] = table_base[key]['description']
                    df.loc[j, 'sourceLink'] = table_base[key]['sourceLink']
                    df.loc[j, 'dataPublishedBy'] = table_base[key]['dataPublishedBy']
                    df.loc[j, 'unit'] = table_base[key]['unit']
                    df.loc[j, 'shortUnit'] = table_base[key]['shortUnit']
                    df.loc[j, 'tolerance'] = table_base[key]['tolerance']
                    df.loc[j, 'retrievedDate'] = table_base[key]['retrievedDate']
                    df.loc[j, 'type'] = table_base[key]['type']
                    df.loc[j, 'colorScaleNumericMinValue'] = table_base[key]['colorScaleNumericMinValue']
                    df.loc[j, 'colorScaleNumericBins'] = table_base[key]['colorScaleNumericBins']
                    df.loc[j, 'colorScaleEqualSizeBins'] = table_base[key]['colorScaleEqualSizeBins']
                    df.loc[j, 'colorScaleScheme'] = table_base[key]['colorScaleScheme']
                    j += 1
# -

# ## Long method
# ### Tables with variable definitions

# +
#Table generation
df = pd.DataFrame()
j=0

for survey in range(len(survey_type)):
    for p_2011 in range(len(povlines_ppp2011)):
        df.loc[j, 'name'] = f'Below ${povlines_ppp2011.dollars_text[p_2011]} a day (2011 prices)'
        df.loc[j, 'slug'] = f'headcount_ratio_{povlines_ppp2011.cents[p_2011]}_ppp2011'
        df.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df.loc[j, 'description'] = f'% of population living in households with an income or expenditure per person below ${povlines_ppp2011.dollars_text[p_2011]} a day (2011 prices).'
        df.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
        df.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
        df.loc[j, 'unit'] = "%"
        df.loc[j, 'shortUnit'] = "%"
        df.loc[j, 'tolerance'] = 5
        df.loc[j, 'type'] = "Numeric"
        df.loc[j, 'colorScaleNumericMinValue'] = 0
        df.loc[j, 'colorScaleNumericBins'] = "3;10;20;30;40;50;60;70;80;90;100"
        df.loc[j, 'colorScaleEqualSizeBins'] = "'true"
        df.loc[j, 'colorScaleScheme'] = "OrRd"
        df.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1
    
    for p_2017 in range(len(povlines_ppp2017)):
        df.loc[j, 'name'] = f'Below ${povlines_ppp2017.dollars_text[p_2017]} a day (2017 prices)'
        df.loc[j, 'slug'] = f'headcount_ratio_{povlines_ppp2017.cents[p_2017]}_ppp2017'
        df.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df.loc[j, 'description'] = f'% of population living in households with an income or expenditure per person below ${povlines_ppp2017.dollars_text[p_2017]} a day (2017 prices).'
        df.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
        df.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
        df.loc[j, 'unit'] = "%"
        df.loc[j, 'shortUnit'] = "%"
        df.loc[j, 'tolerance'] = 5
        df.loc[j, 'type'] = "Numeric"
        df.loc[j, 'colorScaleNumericMinValue'] = 0
        df.loc[j, 'colorScaleNumericBins'] = "3;10;20;30;40;50;60;70;80;90;100"
        df.loc[j, 'colorScaleEqualSizeBins'] = "'true"
        df.loc[j, 'colorScaleScheme'] = "OrRd"
        df.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1
        
    for p_2011 in range(len(povlines_ppp2011)):
        df.loc[j, 'name'] = f'Below ${povlines_ppp2011.dollars_text[p_2011]} a day (2011 prices)'
        df.loc[j, 'slug'] = f'headcount_{povlines_ppp2011.cents[p_2011]}_ppp2011'
        df.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df.loc[j, 'description'] = f'Number of people living in households with an income or expenditure per person below ${povlines_ppp2011.dollars_text[p_2011]} a day (2011 prices).'
        df.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
        df.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
        df.loc[j, 'unit'] = np.nan
        df.loc[j, 'shortUnit'] = np.nan
        df.loc[j, 'tolerance'] = 5
        df.loc[j, 'type'] = "Numeric"
        df.loc[j, 'colorScaleNumericMinValue'] = 0
        df.loc[j, 'colorScaleNumericBins'] = "100000;300000;1000000;3000000;10000000;30000000;100000000;300000000;1000000000;1000000001"
        df.loc[j, 'colorScaleEqualSizeBins'] = "'true"
        df.loc[j, 'colorScaleScheme'] = "Reds"
        df.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1
        
    for p_2017 in range(len(povlines_ppp2017)):
        df.loc[j, 'name'] = f'Below ${povlines_ppp2017.dollars_text[p_2017]} a day (2017 prices)'
        df.loc[j, 'slug'] = f'headcount_{povlines_ppp2017.cents[p_2017]}_ppp2017'
        df.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df.loc[j, 'description'] = f'Number of people living in households with an income or expenditure per person below ${povlines_ppp2017.dollars_text[p_2017]} a day (2017 prices).'
        df.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
        df.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
        df.loc[j, 'unit'] = np.nan
        df.loc[j, 'shortUnit'] = np.nan
        df.loc[j, 'tolerance'] = 5
        df.loc[j, 'type'] = "Numeric"
        df.loc[j, 'colorScaleNumericMinValue'] = 0
        df.loc[j, 'colorScaleNumericBins'] = "100000;300000;1000000;3000000;10000000;30000000;100000000;300000000;1000000000;1000000001"
        df.loc[j, 'colorScaleEqualSizeBins'] = "'true"
        df.loc[j, 'colorScaleScheme'] = "Reds"
        df.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1
        
    for pct in range(len(povlines_rel)):
        df.loc[j, 'name'] = f'{povlines_rel.percent[pct]} of median - share of population below poverty line (2011 prices)'
        df.loc[j, 'slug'] = f'headcount_ratio_{povlines_rel.slug_suffix[pct]}_ppp2011'
        df.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df.loc[j, 'description'] = f'% of population living in households with an income or expenditure per person below {povlines_rel.percent[pct]} of the median (2011 prices).'
        df.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
        df.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP), adapted by Our World in Data."
        df.loc[j, 'unit'] = "%"
        df.loc[j, 'shortUnit'] = "%"
        df.loc[j, 'tolerance'] = 5
        df.loc[j, 'type'] = "Numeric"
        df.loc[j, 'colorScaleNumericMinValue'] = 0
        df.loc[j, 'colorScaleNumericBins'] = "5;10;15;20;25;30;30.0001"
        df.loc[j, 'colorScaleEqualSizeBins'] = "'true"
        df.loc[j, 'colorScaleScheme'] = "YlOrBr"
        df.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1
        
    for pct in range(len(povlines_rel)):
        df.loc[j, 'name'] = f'{povlines_rel.percent[pct]} of median - share of population below poverty line (2017 prices)'
        df.loc[j, 'slug'] = f'headcount_ratio_{povlines_rel.slug_suffix[pct]}_ppp2017'
        df.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df.loc[j, 'description'] = f'% of population living in households with an income or expenditure per person below {povlines_rel.percent[pct]} of the median (2017 prices).'
        df.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
        df.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP), adapted by Our World in Data."
        df.loc[j, 'unit'] = "%"
        df.loc[j, 'shortUnit'] = "%"
        df.loc[j, 'tolerance'] = 5
        df.loc[j, 'type'] = "Numeric"
        df.loc[j, 'colorScaleNumericMinValue'] = 0
        df.loc[j, 'colorScaleNumericBins'] = "5;10;15;20;25;30;30.0001"
        df.loc[j, 'colorScaleEqualSizeBins'] = "'true"
        df.loc[j, 'colorScaleScheme'] = "YlOrBr"
        df.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1
    
    for pct in range(len(povlines_rel)):
        df.loc[j, 'name'] = f'{povlines_rel.percent[pct]} of median - total number of people below poverty line (2011 prices)'
        df.loc[j, 'slug'] = f'headcount_{povlines_rel.slug_suffix[pct]}_ppp2011'
        df.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df.loc[j, 'description'] = f'Number of people living in households with an income or expenditure per person below {povlines_rel.percent[pct]} of the median (2011 prices).'
        df.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
        df.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP), adapted by Our World in Data."
        df.loc[j, 'unit'] = np.nan
        df.loc[j, 'shortUnit'] = np.nan
        df.loc[j, 'tolerance'] = 5
        df.loc[j, 'type'] = "Numeric"
        df.loc[j, 'colorScaleNumericMinValue'] = 0
        df.loc[j, 'colorScaleNumericBins'] = "100000;300000;1000000;3000000;10000000;30000000;100000000;300000000;1000000000;1000000001"
        df.loc[j, 'colorScaleEqualSizeBins'] = "'true"
        df.loc[j, 'colorScaleScheme'] = "YlOrRd"
        df.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1
        
    for pct in range(len(povlines_rel)):
        df.loc[j, 'name'] = f'{povlines_rel.percent[pct]} of median - total number of people below poverty line (2017 prices)'
        df.loc[j, 'slug'] = f'headcount_{povlines_rel.slug_suffix[pct]}_ppp2017'
        df.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df.loc[j, 'description'] = f'Number of people living in households with an income or expenditure per person below {povlines_rel.percent[pct]} of the median (2017 prices).'
        df.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
        df.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP), adapted by Our World in Data."
        df.loc[j, 'unit'] = np.nan
        df.loc[j, 'shortUnit'] = np.nan
        df.loc[j, 'tolerance'] = 5
        df.loc[j, 'type'] = "Numeric"
        df.loc[j, 'colorScaleNumericMinValue'] = 0
        df.loc[j, 'colorScaleNumericBins'] = "100000;300000;1000000;3000000;10000000;30000000;100000000;300000000;1000000000;1000000001"
        df.loc[j, 'colorScaleEqualSizeBins'] = "'true"
        df.loc[j, 'colorScaleScheme'] = "YlOrRd"
        df.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1
        

    df.loc[j, 'name'] = "Mean income or expenditure per day (2011 prices)"
    df.loc[j, 'slug'] = "mean_ppp2011"
    df.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
    df.loc[j, 'description'] = "The mean level of income or expenditure per day (2011 prices)."
    df.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
    df.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
    df.loc[j, 'unit'] = "international-$ at 2011 prices"
    df.loc[j, 'shortUnit'] = "$"
    df.loc[j, 'tolerance'] = 5
    df.loc[j, 'type'] = "Numeric"
    df.loc[j, 'colorScaleNumericMinValue'] = 0
    df.loc[j, 'colorScaleNumericBins'] = "1;2;5;10;20;50;50.0001"
    df.loc[j, 'colorScaleEqualSizeBins'] = "'true"
    df.loc[j, 'colorScaleScheme'] = "BuGn"
    df.loc[j, 'survey_type'] = survey_type['table_name'][survey]
    j += 1
    
    df.loc[j, 'name'] = "Mean income or expenditure per day (2017 prices)"
    df.loc[j, 'slug'] = "mean_ppp2017"
    df.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
    df.loc[j, 'description'] = "The mean level of income or expenditure per day (2017 prices)."
    df.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
    df.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
    df.loc[j, 'unit'] = "international-$ at 2017 prices"
    df.loc[j, 'shortUnit'] = "$"
    df.loc[j, 'tolerance'] = 5
    df.loc[j, 'type'] = "Numeric"
    df.loc[j, 'colorScaleNumericMinValue'] = 0
    df.loc[j, 'colorScaleNumericBins'] = "1;2;5;10;20;50;50.0001"
    df.loc[j, 'colorScaleEqualSizeBins'] = "'true"
    df.loc[j, 'colorScaleScheme'] = "BuGn"
    df.loc[j, 'survey_type'] = survey_type['table_name'][survey]
    j += 1
    
    df.loc[j, 'name'] = "Median income or expenditure per day (2011 prices)"
    df.loc[j, 'slug'] = "median_ppp2011"
    df.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
    df.loc[j, 'description'] = "The level of income or expenditure per day below which half of the population live (2011 prices)."
    df.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
    df.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
    df.loc[j, 'unit'] = "international-$ at 2011 prices"
    df.loc[j, 'shortUnit'] = "$"
    df.loc[j, 'tolerance'] = 5
    df.loc[j, 'type'] = "Numeric"
    df.loc[j, 'colorScaleNumericMinValue'] = 0
    df.loc[j, 'colorScaleNumericBins'] = "1;2;5;10;20;50;50.0001"
    df.loc[j, 'colorScaleEqualSizeBins'] = "'true"
    df.loc[j, 'colorScaleScheme'] = "BuGn"
    df.loc[j, 'survey_type'] = survey_type['table_name'][survey]
    j += 1
    
    df.loc[j, 'name'] = "Median income or expenditure per day (2017 prices)"
    df.loc[j, 'slug'] = "median_ppp2017"
    df.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
    df.loc[j, 'description'] = "The level of income or expenditure per day below which half of the population live (2017 prices)."
    df.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
    df.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
    df.loc[j, 'unit'] = "international-$ at 2017 prices"
    df.loc[j, 'shortUnit'] = "$"
    df.loc[j, 'tolerance'] = 5
    df.loc[j, 'type'] = "Numeric"
    df.loc[j, 'colorScaleNumericMinValue'] = 0
    df.loc[j, 'colorScaleNumericBins'] = "1;2;5;10;20;50;50.0001"
    df.loc[j, 'colorScaleEqualSizeBins'] = "'true"
    df.loc[j, 'colorScaleScheme'] = "BuGn"
    df.loc[j, 'survey_type'] = survey_type['table_name'][survey]
    j += 1
    
    df.loc[j, 'name'] = "P10 (2011 prices)"
    df.loc[j, 'slug'] = "decile1_thr_ppp2011"
    df.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
    df.loc[j, 'description'] = "The level of income or expenditure per day below which 10% of the population falls (2011 prices)."
    df.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
    df.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
    df.loc[j, 'unit'] = "international-$ at 2011 prices"
    df.loc[j, 'shortUnit'] = "$"
    df.loc[j, 'tolerance'] = 5
    df.loc[j, 'type'] = "Numeric"
    df.loc[j, 'colorScaleNumericMinValue'] = 0
    df.loc[j, 'colorScaleNumericBins'] = "1;2;5;10;20;20.0001"
    df.loc[j, 'colorScaleEqualSizeBins'] = "'true"
    df.loc[j, 'colorScaleScheme'] = "Greens"
    df.loc[j, 'survey_type'] = survey_type['table_name'][survey]
    j += 1
    
    df.loc[j, 'name'] = "P10 (2017 prices)"
    df.loc[j, 'slug'] = "decile1_thr_ppp2017"
    df.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
    df.loc[j, 'description'] = "The level of income or expenditure per day below which 10% of the population falls (2017 prices)."
    df.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
    df.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
    df.loc[j, 'unit'] = "international-$ at 2017 prices"
    df.loc[j, 'shortUnit'] = "$"
    df.loc[j, 'tolerance'] = 5
    df.loc[j, 'type'] = "Numeric"
    df.loc[j, 'colorScaleNumericMinValue'] = 0
    df.loc[j, 'colorScaleNumericBins'] = "1;2;5;10;20;20.0001"
    df.loc[j, 'colorScaleEqualSizeBins'] = "'true"
    df.loc[j, 'colorScaleScheme'] = "Greens"
    df.loc[j, 'survey_type'] = survey_type['table_name'][survey]
    j += 1
    
    df.loc[j, 'name'] = "P90 (2011 prices)"
    df.loc[j, 'slug'] = "decile9_thr_ppp2011"
    df.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
    df.loc[j, 'description'] = "The level of income or expenditure per day above which 10% of the population falls (2011 prices)."
    df.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
    df.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
    df.loc[j, 'unit'] = "international-$ at 2011 prices"
    df.loc[j, 'shortUnit'] = "$"
    df.loc[j, 'tolerance'] = 5
    df.loc[j, 'type'] = "Numeric"
    df.loc[j, 'colorScaleNumericMinValue'] = 0
    df.loc[j, 'colorScaleNumericBins'] = "5;10;20;50;100;100.0001"
    df.loc[j, 'colorScaleEqualSizeBins'] = "'true"
    df.loc[j, 'colorScaleScheme'] = "Blues"
    df.loc[j, 'survey_type'] = survey_type['table_name'][survey]
    j += 1
    
    df.loc[j, 'name'] = "P90 (2017 prices)"
    df.loc[j, 'slug'] = "decile9_thr_ppp2017"
    df.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
    df.loc[j, 'description'] = "The level of income or expenditure per day above which 10% of the population falls (2017 prices)."
    df.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
    df.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
    df.loc[j, 'unit'] = "international-$ at 2017 prices"
    df.loc[j, 'shortUnit'] = "$"
    df.loc[j, 'tolerance'] = 5
    df.loc[j, 'type'] = "Numeric"
    df.loc[j, 'colorScaleNumericMinValue'] = 0
    df.loc[j, 'colorScaleNumericBins'] = "5;10;20;50;100;100.0001"
    df.loc[j, 'colorScaleEqualSizeBins'] = "'true"
    df.loc[j, 'colorScaleScheme'] = "Blues"
    df.loc[j, 'survey_type'] = survey_type['table_name'][survey]
    j += 1
# -

survey_list = list(survey_type['table_name'])
for i in survey_list:
    table_export = df[df['survey_type'] == i].copy().reset_index(drop=True)
    table_export = table_export.drop(columns=['survey_type'])
    table_export.to_csv(f'data/ppp_vs/final/OWID_internal_upload/explorer_ppp_vs/table_{i}.csv', index=False)

# ### Grapher views

# +
#Grapher table generation

df = pd.DataFrame()

j=0

for survey in range(len(survey_type)):
    for p_2011 in range(len(povlines_ppp2011)):

        df.loc[j, 'title'] = f'{povlines_ppp2011.title_share[p_2011]}'
        df.loc[j, 'ySlugs'] = f'headcount_ratio_{povlines_ppp2011.cents[p_2011]}_ppp2011'
        df.loc[j, 'Metric Dropdown'] = "Share in poverty"
        df.loc[j, 'International-$ Dropdown'] = "2011 prices"
        df.loc[j, 'Poverty line Dropdown'] = f'{povlines_ppp2011.povline_dropdown[p_2011]}'
        df.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df.loc[j, 'subtitle'] = f'{povlines_ppp2011.subtitle[p_2011]}'
        df.loc[j, 'note'] = "This data is expressed in international-$ at 2011 prices."
        df.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df.loc[j, 'relatedQuestionUrl'] = np.nan
        df.loc[j, 'type'] = np.nan
        df.loc[j, 'yAxisMin'] = 0
        df.loc[j, 'facet'] = np.nan
        df.loc[j, 'selectedFacetStrategy'] = np.nan
        df.loc[j, 'hasMapTab'] = "'true"
        df.loc[j, 'tab'] = "map"
        df.loc[j, 'mapTargetTime'] = 2019
        j += 1
        
    for p_2017 in range(len(povlines_ppp2017)):

        df.loc[j, 'title'] = f'{povlines_ppp2017.title_share[p_2017]}'
        df.loc[j, 'ySlugs'] = f'headcount_ratio_{povlines_ppp2017.cents[p_2017]}_ppp2017'
        df.loc[j, 'Metric Dropdown'] = "Share in poverty"
        df.loc[j, 'International-$ Dropdown'] = "2017 prices"
        df.loc[j, 'Poverty line Dropdown'] = f'{povlines_ppp2017.povline_dropdown[p_2017]}'
        df.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df.loc[j, 'subtitle'] = f'{povlines_ppp2017.subtitle[p_2017]}'
        df.loc[j, 'note'] = "This data is expressed in international-$ at 2017 prices."
        df.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df.loc[j, 'relatedQuestionUrl'] = np.nan
        df.loc[j, 'type'] = np.nan
        df.loc[j, 'yAxisMin'] = 0
        df.loc[j, 'facet'] = np.nan
        df.loc[j, 'selectedFacetStrategy'] = np.nan
        df.loc[j, 'hasMapTab'] = "'true"
        df.loc[j, 'tab'] = "map"
        df.loc[j, 'mapTargetTime'] = 2019
        j += 1
    
    for p_2011 in range(len(povlines_ppp2011)):

        df.loc[j, 'title'] = f'{povlines_ppp2011.title_number[p_2011]}'
        df.loc[j, 'ySlugs'] = f'headcount_{povlines_ppp2011.cents[p_2011]}_ppp2011'
        df.loc[j, 'Metric Dropdown'] = "Number in poverty"
        df.loc[j, 'International-$ Dropdown'] = "2011 prices"
        df.loc[j, 'Poverty line Dropdown'] = f'{povlines_ppp2011.povline_dropdown[p_2011]}'
        df.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df.loc[j, 'subtitle'] = f'{povlines_ppp2011.subtitle[p_2011]}'
        df.loc[j, 'note'] = "This data is expressed in international-$ at 2011 prices."
        df.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df.loc[j, 'relatedQuestionUrl'] = np.nan
        df.loc[j, 'type'] = np.nan
        df.loc[j, 'yAxisMin'] = 0
        df.loc[j, 'facet'] = np.nan
        df.loc[j, 'selectedFacetStrategy'] = np.nan
        df.loc[j, 'hasMapTab'] = "'true"
        df.loc[j, 'tab'] = "map"
        df.loc[j, 'mapTargetTime'] = 2019
        j += 1
        
    for p_2017 in range(len(povlines_ppp2017)):

        df.loc[j, 'title'] = f'{povlines_ppp2017.title_number[p_2017]}'
        df.loc[j, 'ySlugs'] = f'headcount_{povlines_ppp2017.cents[p_2017]}_ppp2017'
        df.loc[j, 'Metric Dropdown'] = "Number in poverty"
        df.loc[j, 'International-$ Dropdown'] = "2017 prices"
        df.loc[j, 'Poverty line Dropdown'] = f'{povlines_ppp2017.povline_dropdown[p_2017]}'
        df.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df.loc[j, 'subtitle'] = f'{povlines_ppp2017.subtitle[p_2017]}'
        df.loc[j, 'note'] = "This data is expressed in international-$ at 2017 prices."
        df.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df.loc[j, 'relatedQuestionUrl'] = np.nan
        df.loc[j, 'type'] = np.nan
        df.loc[j, 'yAxisMin'] = 0
        df.loc[j, 'facet'] = np.nan
        df.loc[j, 'selectedFacetStrategy'] = np.nan
        df.loc[j, 'hasMapTab'] = "'true"
        df.loc[j, 'tab'] = "map"
        df.loc[j, 'mapTargetTime'] = 2019
        j += 1

    for p in range(len(povlines_both)):

        df.loc[j, 'title'] = f'{povlines_both.title_share[p]}'
        df.loc[j, 'ySlugs'] = f'headcount_ratio_{povlines_both.cents_2011[p]}_ppp2011 headcount_ratio_{povlines_both.cents_2017[p]}_ppp2017'
        df.loc[j, 'Metric Dropdown'] = "Share in poverty"
        df.loc[j, 'International-$ Dropdown'] = "Compare 2017 and 2011 prices"
        df.loc[j, 'Poverty line Dropdown'] = f'{povlines_both.povline_dropdown[p]}'
        df.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df.loc[j, 'subtitle'] = f'{povlines_both.subtitle[p]}'
        df.loc[j, 'note'] = np.nan
        df.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df.loc[j, 'relatedQuestionUrl'] = np.nan
        df.loc[j, 'type'] = np.nan
        df.loc[j, 'yAxisMin'] = 0
        df.loc[j, 'facet'] = "entity"
        df.loc[j, 'selectedFacetStrategy'] = "entity"
        df.loc[j, 'hasMapTab'] = np.nan
        df.loc[j, 'tab'] = np.nan
        df.loc[j, 'mapTargetTime'] = np.nan
        j += 1
        
    for p in range(len(povlines_both)):

        df.loc[j, 'title'] = f'{povlines_both.title_number[p]}'
        df.loc[j, 'ySlugs'] = f'headcount_{povlines_both.cents_2011[p]}_ppp2011 headcount_{povlines_both.cents_2017[p]}_ppp2017'
        df.loc[j, 'Metric Dropdown'] = "Number in poverty"
        df.loc[j, 'International-$ Dropdown'] = "Compare 2017 and 2011 prices"
        df.loc[j, 'Poverty line Dropdown'] = f'{povlines_both.povline_dropdown[p]}'
        df.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df.loc[j, 'subtitle'] = f'{povlines_both.subtitle[p]}'
        df.loc[j, 'note'] = np.nan
        df.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df.loc[j, 'relatedQuestionUrl'] = np.nan
        df.loc[j, 'type'] = np.nan
        df.loc[j, 'yAxisMin'] = 0
        df.loc[j, 'facet'] = "entity"
        df.loc[j, 'selectedFacetStrategy'] = "entity"
        df.loc[j, 'hasMapTab'] = np.nan
        df.loc[j, 'tab'] = np.nan
        df.loc[j, 'mapTargetTime'] = np.nan
        j += 1
        
    for pct in range(len(povlines_rel)):

        df.loc[j, 'title'] = f'{povlines_rel.title_share[pct]} (2011 prices)'
        df.loc[j, 'ySlugs'] = f'headcount_ratio_{povlines_rel.slug_suffix[pct]}_ppp2011'
        df.loc[j, 'Metric Dropdown'] = "Share in poverty"
        df.loc[j, 'International-$ Dropdown'] = "2011 prices"
        df.loc[j, 'Poverty line Dropdown'] = f'{povlines_rel.dropdown[pct]}'
        df.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df.loc[j, 'subtitle'] = f'Relative poverty is measured in terms of a poverty line that rises and falls over time with average incomes – in this case set at {povlines_rel.text[pct]} {survey_type.text[survey]}.'
        df.loc[j, 'note'] = "This data is adjusted for inflation and for differences in the cost of living between countries. It is expressed in international-$ at 2011 prices."
        df.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df.loc[j, 'relatedQuestionUrl'] = np.nan
        df.loc[j, 'type'] = np.nan
        df.loc[j, 'yAxisMin'] = 0
        df.loc[j, 'facet'] = np.nan
        df.loc[j, 'selectedFacetStrategy'] = np.nan
        df.loc[j, 'hasMapTab'] = "'true"
        df.loc[j, 'tab'] = "map"
        df.loc[j, 'mapTargetTime'] = 2019
        j += 1
        
    for pct in range(len(povlines_rel)):

        df.loc[j, 'title'] = f'{povlines_rel.title_share[pct]} (2017 prices)'
        df.loc[j, 'ySlugs'] = f'headcount_ratio_{povlines_rel.slug_suffix[pct]}_ppp2017'
        df.loc[j, 'Metric Dropdown'] = "Share in poverty"
        df.loc[j, 'International-$ Dropdown'] = "2017 prices"
        df.loc[j, 'Poverty line Dropdown'] = f'{povlines_rel.dropdown[pct]}'
        df.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df.loc[j, 'subtitle'] = f'Relative poverty is measured in terms of a poverty line that rises and falls over time with average incomes – in this case set at {povlines_rel.text[pct]} {survey_type.text[survey]}.'
        df.loc[j, 'note'] = "This data is adjusted for inflation and for differences in the cost of living between countries. It is expressed in international-$ at 2017 prices."
        df.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df.loc[j, 'relatedQuestionUrl'] = np.nan
        df.loc[j, 'type'] = np.nan
        df.loc[j, 'yAxisMin'] = 0
        df.loc[j, 'facet'] = np.nan
        df.loc[j, 'selectedFacetStrategy'] = np.nan
        df.loc[j, 'hasMapTab'] = "'true"
        df.loc[j, 'tab'] = "map"
        df.loc[j, 'mapTargetTime'] = 2019
        j += 1
        
    for pct in range(len(povlines_rel)):

        df.loc[j, 'title'] = f'{povlines_rel.title_number[pct]} (2011 prices)'
        df.loc[j, 'ySlugs'] = f'headcount_{povlines_rel.slug_suffix[pct]}_ppp2011'
        df.loc[j, 'Metric Dropdown'] = "Number in poverty"
        df.loc[j, 'International-$ Dropdown'] = "2011 prices"
        df.loc[j, 'Poverty line Dropdown'] = f'{povlines_rel.dropdown[pct]}'
        df.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df.loc[j, 'subtitle'] = f'Relative poverty is measured in terms of a poverty line that rises and falls over time with average incomes – in this case set at {povlines_rel.text[pct]} {survey_type.text[survey]}.'
        df.loc[j, 'note'] = "This data is adjusted for inflation and for differences in the cost of living between countries. It is expressed in international-$ at 2011 prices."
        df.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df.loc[j, 'relatedQuestionUrl'] = np.nan
        df.loc[j, 'type'] = np.nan
        df.loc[j, 'yAxisMin'] = 0
        df.loc[j, 'facet'] = np.nan
        df.loc[j, 'selectedFacetStrategy'] = np.nan
        df.loc[j, 'hasMapTab'] = "'true"
        df.loc[j, 'tab'] = "map"
        df.loc[j, 'mapTargetTime'] = 2019
        j += 1
        
    for pct in range(len(povlines_rel)):

        df.loc[j, 'title'] = f'{povlines_rel.title_number[pct]} (2017 prices)'
        df.loc[j, 'ySlugs'] = f'headcount_{povlines_rel.slug_suffix[pct]}_ppp2017'
        df.loc[j, 'Metric Dropdown'] = "Number in poverty"
        df.loc[j, 'International-$ Dropdown'] = "2017 prices"
        df.loc[j, 'Poverty line Dropdown'] = f'{povlines_rel.dropdown[pct]}'
        df.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df.loc[j, 'subtitle'] = f'Relative poverty is measured in terms of a poverty line that rises and falls over time with average incomes – in this case set at {povlines_rel.text[pct]} {survey_type.text[survey]}.'
        df.loc[j, 'note'] = "This data is adjusted for inflation and for differences in the cost of living between countries. It is expressed in international-$ at 2017 prices."
        df.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df.loc[j, 'relatedQuestionUrl'] = np.nan
        df.loc[j, 'type'] = np.nan
        df.loc[j, 'yAxisMin'] = 0
        df.loc[j, 'facet'] = np.nan
        df.loc[j, 'selectedFacetStrategy'] = np.nan
        df.loc[j, 'hasMapTab'] = "'true"
        df.loc[j, 'tab'] = "map"
        df.loc[j, 'mapTargetTime'] = 2019
        j += 1
        
        #####
        
    for pct in range(len(povlines_rel)):

        df.loc[j, 'title'] = f'{povlines_rel.title_share_vs[pct]}'
        df.loc[j, 'ySlugs'] = f'headcount_ratio_{povlines_rel.slug_suffix[pct]}_ppp2011 headcount_ratio_{povlines_rel.slug_suffix[pct]}_ppp2017'
        df.loc[j, 'Metric Dropdown'] = "Share in poverty"
        df.loc[j, 'International-$ Dropdown'] = "Compare 2017 and 2011 prices"
        df.loc[j, 'Poverty line Dropdown'] = f'{povlines_rel.dropdown[pct]}'
        df.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df.loc[j, 'subtitle'] = f'Relative poverty is measured in terms of a poverty line that rises and falls over time with average incomes – in this case set at {povlines_rel.text[pct]} {survey_type.text[survey]}.'
        df.loc[j, 'note'] = "This data is adjusted for inflation and for differences in the cost of living between countries."
        df.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df.loc[j, 'relatedQuestionUrl'] = np.nan
        df.loc[j, 'type'] = np.nan
        df.loc[j, 'yAxisMin'] = 0
        df.loc[j, 'facet'] = "entity"
        df.loc[j, 'selectedFacetStrategy'] = "entity"
        df.loc[j, 'hasMapTab'] = np.nan
        df.loc[j, 'tab'] = np.nan
        df.loc[j, 'mapTargetTime'] = np.nan
        j += 1
        
    for pct in range(len(povlines_rel)):

        df.loc[j, 'title'] = f'{povlines_rel.title_number_vs[pct]}'
        df.loc[j, 'ySlugs'] = f'headcount_{povlines_rel.slug_suffix[pct]}_ppp2011 headcount_{povlines_rel.slug_suffix[pct]}_ppp2017'
        df.loc[j, 'Metric Dropdown'] = "Number in poverty"
        df.loc[j, 'International-$ Dropdown'] = "Compare 2017 and 2011 prices"
        df.loc[j, 'Poverty line Dropdown'] = f'{povlines_rel.dropdown[pct]}'
        df.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df.loc[j, 'subtitle'] = f'Relative poverty is measured in terms of a poverty line that rises and falls over time with average incomes – in this case set at {povlines_rel.text[pct]} {survey_type.text[survey]}.'
        df.loc[j, 'note'] = "This data is adjusted for inflation and for differences in the cost of living between countries."
        df.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df.loc[j, 'relatedQuestionUrl'] = np.nan
        df.loc[j, 'type'] = np.nan
        df.loc[j, 'yAxisMin'] = 0
        df.loc[j, 'facet'] = "entity"
        df.loc[j, 'selectedFacetStrategy'] = "entity"
        df.loc[j, 'hasMapTab'] = np.nan
        df.loc[j, 'tab'] = np.nan
        df.loc[j, 'mapTargetTime'] = np.nan
        j += 1

#####

    df.loc[j, 'title'] = f"Mean {survey_type.text[survey]} per day (2011 prices)"
    df.loc[j, 'ySlugs'] = "mean_ppp2011"
    df.loc[j, 'Metric Dropdown'] = "Mean"
    df.loc[j, 'International-$ Dropdown'] = "2011 prices"
    df.loc[j, 'Poverty line Dropdown'] = np.nan
    df.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
    df.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
    df.loc[j, 'subtitle'] = "This data is adjusted for inflation and for differences in the cost of living between countries."
    df.loc[j, 'note'] = "This data is expressed in international-$ at 2011 prices."
    df.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
    df.loc[j, 'relatedQuestionUrl'] = np.nan
    df.loc[j, 'type'] = np.nan
    df.loc[j, 'yAxisMin'] = 0
    df.loc[j, 'facet'] = np.nan
    df.loc[j, 'selectedFacetStrategy'] = np.nan
    df.loc[j, 'hasMapTab'] = "'true"
    df.loc[j, 'tab'] = "map"
    df.loc[j, 'mapTargetTime'] = 2019
    j += 1

    df.loc[j, 'title'] = f"Mean {survey_type.text[survey]} per day (2017 prices)"
    df.loc[j, 'ySlugs'] = "mean_ppp2017"
    df.loc[j, 'Metric Dropdown'] = "Mean"
    df.loc[j, 'International-$ Dropdown'] = "2017 prices"
    df.loc[j, 'Poverty line Dropdown'] = np.nan
    df.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
    df.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
    df.loc[j, 'subtitle'] = "This data is adjusted for inflation and for differences in the cost of living between countries."
    df.loc[j, 'note'] = "This data is expressed in international-$ at 2017 prices."
    df.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
    df.loc[j, 'relatedQuestionUrl'] = np.nan
    df.loc[j, 'type'] = np.nan
    df.loc[j, 'yAxisMin'] = 0
    df.loc[j, 'facet'] = np.nan
    df.loc[j, 'selectedFacetStrategy'] = np.nan
    df.loc[j, 'hasMapTab'] = "'true"
    df.loc[j, 'tab'] = "map"
    df.loc[j, 'mapTargetTime'] = 2019
    j += 1

    df.loc[j, 'title'] = f"Mean {survey_type.text[survey]} per day: 2011 vs. 2017 prices"
    df.loc[j, 'ySlugs'] = "mean_ppp2011 mean_ppp2017"
    df.loc[j, 'Metric Dropdown'] = "Mean"
    df.loc[j, 'International-$ Dropdown'] = "Compare 2017 and 2011 prices"
    df.loc[j, 'Poverty line Dropdown'] = np.nan
    df.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
    df.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
    df.loc[j, 'subtitle'] = "This data is adjusted for inflation and for differences in the cost of living between countries."
    df.loc[j, 'note'] = np.nan
    df.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
    df.loc[j, 'relatedQuestionUrl'] = np.nan
    df.loc[j, 'type'] = np.nan
    df.loc[j, 'yAxisMin'] = 0
    df.loc[j, 'facet'] = "entity"
    df.loc[j, 'selectedFacetStrategy'] = "entity"
    df.loc[j, 'hasMapTab'] = np.nan
    df.loc[j, 'tab'] = np.nan
    df.loc[j, 'mapTargetTime'] = np.nan
    j += 1

    df.loc[j, 'title'] = f"Median {survey_type.text[survey]} per day (2011 prices)"
    df.loc[j, 'ySlugs'] = "median_ppp2011"
    df.loc[j, 'Metric Dropdown'] = "Median"
    df.loc[j, 'International-$ Dropdown'] = "2011 prices"
    df.loc[j, 'Poverty line Dropdown'] = np.nan
    df.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
    df.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
    df.loc[j, 'subtitle'] = "This data is adjusted for inflation and for differences in the cost of living between countries."
    df.loc[j, 'note'] = "This data is expressed in international-$ at 2011 prices."
    df.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
    df.loc[j, 'relatedQuestionUrl'] = np.nan
    df.loc[j, 'type'] = np.nan
    df.loc[j, 'yAxisMin'] = 0
    df.loc[j, 'facet'] = np.nan
    df.loc[j, 'selectedFacetStrategy'] = np.nan
    df.loc[j, 'hasMapTab'] = "'true"
    df.loc[j, 'tab'] = "map"
    df.loc[j, 'mapTargetTime'] = 2019
    j += 1

    df.loc[j, 'title'] = f"Median {survey_type.text[survey]} per day (2017 prices)"
    df.loc[j, 'ySlugs'] = "median_ppp2017"
    df.loc[j, 'Metric Dropdown'] = "Median"
    df.loc[j, 'International-$ Dropdown'] = "2017 prices"
    df.loc[j, 'Poverty line Dropdown'] = np.nan
    df.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
    df.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
    df.loc[j, 'subtitle'] = "This data is adjusted for inflation and for differences in the cost of living between countries."
    df.loc[j, 'note'] = "This data is expressed in international-$ at 2017 prices."
    df.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
    df.loc[j, 'relatedQuestionUrl'] = np.nan
    df.loc[j, 'type'] = np.nan
    df.loc[j, 'yAxisMin'] = 0
    df.loc[j, 'facet'] = np.nan
    df.loc[j, 'selectedFacetStrategy'] = np.nan
    df.loc[j, 'hasMapTab'] = "'true"
    df.loc[j, 'tab'] = "map"
    df.loc[j, 'mapTargetTime'] = 2019
    j += 1

    df.loc[j, 'title'] = f"Median {survey_type.text[survey]} per day: 2011 vs. 2017 prices"
    df.loc[j, 'ySlugs'] = "median_ppp2011 median_ppp2017"
    df.loc[j, 'Metric Dropdown'] = "Median"
    df.loc[j, 'International-$ Dropdown'] = "Compare 2017 and 2011 prices"
    df.loc[j, 'Poverty line Dropdown'] = np.nan
    df.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
    df.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
    df.loc[j, 'subtitle'] = "This data is adjusted for inflation and for differences in the cost of living between countries."
    df.loc[j, 'note'] = np.nan
    df.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
    df.loc[j, 'relatedQuestionUrl'] = np.nan
    df.loc[j, 'type'] = np.nan
    df.loc[j, 'yAxisMin'] = 0
    df.loc[j, 'facet'] = "entity"
    df.loc[j, 'selectedFacetStrategy'] = "entity"
    df.loc[j, 'hasMapTab'] = np.nan
    df.loc[j, 'tab'] = np.nan
    df.loc[j, 'mapTargetTime'] = np.nan
    j += 1

    df.loc[j, 'title'] = f"P10: The {survey_type.text[survey]} of the poorest tenth (2011 prices)"
    df.loc[j, 'ySlugs'] = "decile1_thr_ppp2011"
    df.loc[j, 'Metric Dropdown'] = "P10 (poorest tenth)"
    df.loc[j, 'International-$ Dropdown'] = "2011 prices"
    df.loc[j, 'Poverty line Dropdown'] = np.nan
    df.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
    df.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
    df.loc[j, 'subtitle'] = f"P10 is the level of {survey_type.text[survey]} per day below which 10% of the population falls."
    df.loc[j, 'note'] = "This data is adjusted for inflation and for differences in the cost of living between countries. It is expressed in international-$ at 2011 prices."
    df.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
    df.loc[j, 'relatedQuestionUrl'] = np.nan
    df.loc[j, 'type'] = np.nan
    df.loc[j, 'yAxisMin'] = 0
    df.loc[j, 'facet'] = np.nan
    df.loc[j, 'selectedFacetStrategy'] = np.nan
    df.loc[j, 'hasMapTab'] = "'true"
    df.loc[j, 'tab'] = "map"
    df.loc[j, 'mapTargetTime'] = 2019
    j += 1

    df.loc[j, 'title'] = f"P10: The {survey_type.text[survey]} of the poorest tenth (2017 prices)"
    df.loc[j, 'ySlugs'] = "decile1_thr_ppp2017"
    df.loc[j, 'Metric Dropdown'] = "P10 (poorest tenth)"
    df.loc[j, 'International-$ Dropdown'] = "2017 prices"
    df.loc[j, 'Poverty line Dropdown'] = np.nan
    df.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
    df.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
    df.loc[j, 'subtitle'] = f"P10 is the level of {survey_type.text[survey]} per day below which 10% of the population falls."
    df.loc[j, 'note'] = "This data is adjusted for inflation and for differences in the cost of living between countries. It is expressed in international-$ at 2017 prices."
    df.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
    df.loc[j, 'relatedQuestionUrl'] = np.nan
    df.loc[j, 'type'] = np.nan
    df.loc[j, 'yAxisMin'] = 0
    df.loc[j, 'facet'] = np.nan
    df.loc[j, 'selectedFacetStrategy'] = np.nan
    df.loc[j, 'hasMapTab'] = "'true"
    df.loc[j, 'tab'] = "map"
    df.loc[j, 'mapTargetTime'] = 2019
    j += 1

    df.loc[j, 'title'] = f"P10: The {survey_type.text[survey]} of the poorest tenth (2011 vs. 2017 prices)"
    df.loc[j, 'ySlugs'] = "decile1_thr_ppp2011 decile1_thr_ppp2017"
    df.loc[j, 'Metric Dropdown'] = "P10 (poorest tenth)"
    df.loc[j, 'International-$ Dropdown'] = "Compare 2017 and 2011 prices"
    df.loc[j, 'Poverty line Dropdown'] = np.nan
    df.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
    df.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
    df.loc[j, 'subtitle'] = f"P10 is the level of {survey_type.text[survey]} per day below which 10% of the population falls."
    df.loc[j, 'note'] = "This data is adjusted for inflation and for differences in the cost of living between countries."
    df.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
    df.loc[j, 'relatedQuestionUrl'] = np.nan
    df.loc[j, 'type'] = np.nan
    df.loc[j, 'yAxisMin'] = 0
    df.loc[j, 'facet'] = "entity"
    df.loc[j, 'selectedFacetStrategy'] = "entity"
    df.loc[j, 'hasMapTab'] = np.nan
    df.loc[j, 'tab'] = np.nan
    df.loc[j, 'mapTargetTime'] = np.nan
    j += 1

    df.loc[j, 'title'] = f"P90: The {survey_type.text[survey]} of the richest tenth (2011 prices)"
    df.loc[j, 'ySlugs'] = "decile9_thr_ppp2011"
    df.loc[j, 'Metric Dropdown'] = "P90 (richest tenth)"
    df.loc[j, 'International-$ Dropdown'] = "2011 prices"
    df.loc[j, 'Poverty line Dropdown'] = np.nan
    df.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
    df.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
    df.loc[j, 'subtitle'] = f"P90 is the level of {survey_type.text[survey]} per day above which 10% of the population falls."
    df.loc[j, 'note'] = "This data is adjusted for inflation and for differences in the cost of living between countries. It is expressed in international-$ at 2011 prices."
    df.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
    df.loc[j, 'relatedQuestionUrl'] = np.nan
    df.loc[j, 'type'] = np.nan
    df.loc[j, 'yAxisMin'] = 0
    df.loc[j, 'facet'] = np.nan
    df.loc[j, 'selectedFacetStrategy'] = np.nan
    df.loc[j, 'hasMapTab'] = "'true"
    df.loc[j, 'tab'] = "map"
    df.loc[j, 'mapTargetTime'] = 2019
    j += 1

    df.loc[j, 'title'] = f"P90: The {survey_type.text[survey]} of the richest tenth (2017 prices)"
    df.loc[j, 'ySlugs'] = "decile9_thr_ppp2017"
    df.loc[j, 'Metric Dropdown'] = "P90 (richest tenth)"
    df.loc[j, 'International-$ Dropdown'] = "2017 prices"
    df.loc[j, 'Poverty line Dropdown'] = np.nan
    df.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
    df.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
    df.loc[j, 'subtitle'] = f"P90 is the level of {survey_type.text[survey]} per day above which 10% of the population falls."
    df.loc[j, 'note'] = "This data is adjusted for inflation and for differences in the cost of living between countries. It is expressed in international-$ at 2017 prices."
    df.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
    df.loc[j, 'relatedQuestionUrl'] = np.nan
    df.loc[j, 'type'] = np.nan
    df.loc[j, 'yAxisMin'] = 0
    df.loc[j, 'facet'] = np.nan
    df.loc[j, 'selectedFacetStrategy'] = np.nan
    df.loc[j, 'hasMapTab'] = "'true"
    df.loc[j, 'tab'] = "map"
    df.loc[j, 'mapTargetTime'] = 2019
    j += 1

    df.loc[j, 'title'] = f"P90: The {survey_type.text[survey]} of the richest tenth (2011 vs. 2017 prices)"
    df.loc[j, 'ySlugs'] = "decile9_thr_ppp2011 decile9_thr_ppp2017"
    df.loc[j, 'Metric Dropdown'] = "P90 (richest tenth)"
    df.loc[j, 'International-$ Dropdown'] = "Compare 2017 and 2011 prices"
    df.loc[j, 'Poverty line Dropdown'] = np.nan
    df.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
    df.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
    df.loc[j, 'subtitle'] = f"P90 is the level of {survey_type.text[survey]} per day above which 10% of the population falls."
    df.loc[j, 'note'] = "This data is adjusted for inflation and for differences in the cost of living between countries."
    df.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
    df.loc[j, 'relatedQuestionUrl'] = np.nan
    df.loc[j, 'type'] = np.nan
    df.loc[j, 'yAxisMin'] = 0
    df.loc[j, 'facet'] = "entity"
    df.loc[j, 'selectedFacetStrategy'] = "entity"
    df.loc[j, 'hasMapTab'] = np.nan
    df.loc[j, 'tab'] = np.nan
    df.loc[j, 'mapTargetTime'] = np.nan
    j += 1
    
#Select one default view
df.loc[(df['ySlugs'] == "headcount_ratio_190_ppp2011 headcount_ratio_215_ppp2017") 
       & (df['tableSlug'] == "inc_or_cons"), ['defaultView']] = "'true"
    
    
#Reorder dropdown menus
povline_dropdown_list = ['$1 per day',
                         '$1.9 per day: International Poverty Line',
                         '$2.15 per day: International Poverty Line',
                         '$3.2 per day: Lower-middle income poverty line',
                         '$3.65 per day: Lower-middle income poverty line',
                         '$5.5 per day: Upper-middle income poverty line',
                         '$6.85 per day: Upper-middle income poverty line',
                         '$10 per day',
                         '$20 per day',
                         '$30 per day',
                         '$40 per day',
                         'International Poverty Line',
                         'Lower-middle income poverty line',
                         'Upper-middle income poverty line',
                         'Relative poverty: 40% of median',
                         'Relative poverty: 50% of median',
                         'Relative poverty: 60% of median']


df_mapping = pd.DataFrame({'povline_dropdown': povline_dropdown_list,})
df_mapping = df_mapping.reset_index().set_index('povline_dropdown')

df['povline_dropdown_aux'] = df['Poverty line Dropdown'].map(df_mapping['index'])
df = df.sort_values('povline_dropdown_aux', ignore_index=True)
df = df.drop(columns=['povline_dropdown_aux'])
    
df.to_csv(f'data/ppp_vs/final/OWID_internal_upload/explorer_ppp_vs/grapher.csv', index=False)
# -

