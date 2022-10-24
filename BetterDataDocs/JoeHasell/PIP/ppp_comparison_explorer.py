import pandas as pd
import numpy as np

# +
#Read Google sheets
sheet_id = '1mR0LPEGlY-wCp1q9lNTlDbVIG65JazKvHL16my9tH8Y'

sheet_name = 'povlines_ppp2011'
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
povlines_ppp2011 = pd.read_csv(url, dtype={'dollars_text':'str'})

sheet_name = 'povlines_ppp2017'
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
povlines_ppp2017 = pd.read_csv(url, dtype={'dollars_text':'str'})

sheet_name = 'povlines_both'
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
povlines_both = pd.read_csv(url, dtype={'dollars_2011_text':'str', 'dollars_2017_text':'str'})

sheet_name = 'povlines_rel'
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
povlines_rel = pd.read_csv(url)

sheet_name = 'survey_type'
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
survey_type = pd.read_csv(url)
# -

# ## Long method
# ### Tables with variable definitions
# Variables are grouped by type to iterate by different poverty lines and survey types at the same time. The output is the list of all the variables being used in the explorer, separated by survey type in csv files.

# +
#Table generation
df_tables = pd.DataFrame()
j=0

for survey in range(len(survey_type)):
    for p_2011 in range(len(povlines_ppp2011)):
        df_tables.loc[j, 'name'] = f'Below ${povlines_ppp2011.dollars_text[p_2011]} a day (2011 prices)'
        df_tables.loc[j, 'slug'] = f'headcount_ratio_{povlines_ppp2011.cents[p_2011]}_ppp2011'
        df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df_tables.loc[j, 'description'] = f'% of population living in households with an {survey_type.text[survey]} per person below ${povlines_ppp2011.dollars_text[p_2011]} a day (2011 prices).'
        df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
        df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
        df_tables.loc[j, 'unit'] = "%"
        df_tables.loc[j, 'shortUnit'] = "%"
        df_tables.loc[j, 'tolerance'] = 5
        df_tables.loc[j, 'type'] = "Numeric"
        df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
        df_tables.loc[j, 'colorScaleNumericBins'] = "3;10;20;30;40;50;60;70;80;90;100"
        df_tables.loc[j, 'colorScaleEqualSizeBins'] = "'true"
        df_tables.loc[j, 'colorScaleScheme'] = "OrRd"
        df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1
    
    for p_2017 in range(len(povlines_ppp2017)):
        df_tables.loc[j, 'name'] = f'Below ${povlines_ppp2017.dollars_text[p_2017]} a day (2017 prices)'
        df_tables.loc[j, 'slug'] = f'headcount_ratio_{povlines_ppp2017.cents[p_2017]}_ppp2017'
        df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df_tables.loc[j, 'description'] = f'% of population living in households with an {survey_type.text[survey]} per person below ${povlines_ppp2017.dollars_text[p_2017]} a day (2017 prices).'
        df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
        df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
        df_tables.loc[j, 'unit'] = "%"
        df_tables.loc[j, 'shortUnit'] = "%"
        df_tables.loc[j, 'tolerance'] = 5
        df_tables.loc[j, 'type'] = "Numeric"
        df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
        df_tables.loc[j, 'colorScaleNumericBins'] = "3;10;20;30;40;50;60;70;80;90;100"
        df_tables.loc[j, 'colorScaleEqualSizeBins'] = "'true"
        df_tables.loc[j, 'colorScaleScheme'] = "OrRd"
        df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1
        
    for p_2011 in range(len(povlines_ppp2011)):
        df_tables.loc[j, 'name'] = f'Below ${povlines_ppp2011.dollars_text[p_2011]} a day (2011 prices)'
        df_tables.loc[j, 'slug'] = f'headcount_{povlines_ppp2011.cents[p_2011]}_ppp2011'
        df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df_tables.loc[j, 'description'] = f'Number of people living in households with an {survey_type.text[survey]} per person below ${povlines_ppp2011.dollars_text[p_2011]} a day (2011 prices).'
        df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
        df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
        df_tables.loc[j, 'unit'] = np.nan
        df_tables.loc[j, 'shortUnit'] = np.nan
        df_tables.loc[j, 'tolerance'] = 5
        df_tables.loc[j, 'type'] = "Numeric"
        df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
        df_tables.loc[j, 'colorScaleNumericBins'] = "100000;300000;1000000;3000000;10000000;30000000;100000000;300000000;1000000000;1000000001"
        df_tables.loc[j, 'colorScaleEqualSizeBins'] = "'true"
        df_tables.loc[j, 'colorScaleScheme'] = "Reds"
        df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1
        
    for p_2017 in range(len(povlines_ppp2017)):
        df_tables.loc[j, 'name'] = f'Below ${povlines_ppp2017.dollars_text[p_2017]} a day (2017 prices)'
        df_tables.loc[j, 'slug'] = f'headcount_{povlines_ppp2017.cents[p_2017]}_ppp2017'
        df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df_tables.loc[j, 'description'] = f'Number of people living in households with an {survey_type.text[survey]} per person below ${povlines_ppp2017.dollars_text[p_2017]} a day (2017 prices).'
        df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
        df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
        df_tables.loc[j, 'unit'] = np.nan
        df_tables.loc[j, 'shortUnit'] = np.nan
        df_tables.loc[j, 'tolerance'] = 5
        df_tables.loc[j, 'type'] = "Numeric"
        df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
        df_tables.loc[j, 'colorScaleNumericBins'] = "100000;300000;1000000;3000000;10000000;30000000;100000000;300000000;1000000000;1000000001"
        df_tables.loc[j, 'colorScaleEqualSizeBins'] = "'true"
        df_tables.loc[j, 'colorScaleScheme'] = "Reds"
        df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1
        
    for pct in range(len(povlines_rel)):
        df_tables.loc[j, 'name'] = f'{povlines_rel.percent[pct]} of median - share of population below poverty line (2011 prices)'
        df_tables.loc[j, 'slug'] = f'headcount_ratio_{povlines_rel.slug_suffix[pct]}_ppp2011'
        df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df_tables.loc[j, 'description'] = f'% of population living in households with an {survey_type.text[survey]} per person below {povlines_rel.percent[pct]} of the median (2011 prices).'
        df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
        df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP), adapted by Our World in Data."
        df_tables.loc[j, 'unit'] = "%"
        df_tables.loc[j, 'shortUnit'] = "%"
        df_tables.loc[j, 'tolerance'] = 5
        df_tables.loc[j, 'type'] = "Numeric"
        df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
        df_tables.loc[j, 'colorScaleNumericBins'] = "5;10;15;20;25;30;30.0001"
        df_tables.loc[j, 'colorScaleEqualSizeBins'] = "'true"
        df_tables.loc[j, 'colorScaleScheme'] = "YlOrBr"
        df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1
        
    for pct in range(len(povlines_rel)):
        df_tables.loc[j, 'name'] = f'{povlines_rel.percent[pct]} of median - share of population below poverty line (2017 prices)'
        df_tables.loc[j, 'slug'] = f'headcount_ratio_{povlines_rel.slug_suffix[pct]}_ppp2017'
        df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df_tables.loc[j, 'description'] = f'% of population living in households with an {survey_type.text[survey]} per person below {povlines_rel.percent[pct]} of the median (2017 prices).'
        df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
        df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP), adapted by Our World in Data."
        df_tables.loc[j, 'unit'] = "%"
        df_tables.loc[j, 'shortUnit'] = "%"
        df_tables.loc[j, 'tolerance'] = 5
        df_tables.loc[j, 'type'] = "Numeric"
        df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
        df_tables.loc[j, 'colorScaleNumericBins'] = "5;10;15;20;25;30;30.0001"
        df_tables.loc[j, 'colorScaleEqualSizeBins'] = "'true"
        df_tables.loc[j, 'colorScaleScheme'] = "YlOrBr"
        df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1
    
    for pct in range(len(povlines_rel)):
        df_tables.loc[j, 'name'] = f'{povlines_rel.percent[pct]} of median - total number of people below poverty line (2011 prices)'
        df_tables.loc[j, 'slug'] = f'headcount_{povlines_rel.slug_suffix[pct]}_ppp2011'
        df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df_tables.loc[j, 'description'] = f'Number of people living in households with an {survey_type.text[survey]} per person below {povlines_rel.percent[pct]} of the median (2011 prices).'
        df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
        df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP), adapted by Our World in Data."
        df_tables.loc[j, 'unit'] = np.nan
        df_tables.loc[j, 'shortUnit'] = np.nan
        df_tables.loc[j, 'tolerance'] = 5
        df_tables.loc[j, 'type'] = "Numeric"
        df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
        df_tables.loc[j, 'colorScaleNumericBins'] = "100000;300000;1000000;3000000;10000000;30000000;100000000;300000000;1000000000;1000000001"
        df_tables.loc[j, 'colorScaleEqualSizeBins'] = "'true"
        df_tables.loc[j, 'colorScaleScheme'] = "YlOrRd"
        df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1
        
    for pct in range(len(povlines_rel)):
        df_tables.loc[j, 'name'] = f'{povlines_rel.percent[pct]} of median - total number of people below poverty line (2017 prices)'
        df_tables.loc[j, 'slug'] = f'headcount_{povlines_rel.slug_suffix[pct]}_ppp2017'
        df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df_tables.loc[j, 'description'] = f'Number of people living in households with an {survey_type.text[survey]} per person below {povlines_rel.percent[pct]} of the median (2017 prices).'
        df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
        df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP), adapted by Our World in Data."
        df_tables.loc[j, 'unit'] = np.nan
        df_tables.loc[j, 'shortUnit'] = np.nan
        df_tables.loc[j, 'tolerance'] = 5
        df_tables.loc[j, 'type'] = "Numeric"
        df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
        df_tables.loc[j, 'colorScaleNumericBins'] = "100000;300000;1000000;3000000;10000000;30000000;100000000;300000000;1000000000;1000000001"
        df_tables.loc[j, 'colorScaleEqualSizeBins'] = "'true"
        df_tables.loc[j, 'colorScaleScheme'] = "YlOrRd"
        df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1
        

    df_tables.loc[j, 'name'] = f"Mean {survey_type.text[survey]} per day (2011 prices)"
    df_tables.loc[j, 'slug'] = "mean_ppp2011"
    df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
    df_tables.loc[j, 'description'] = f"The mean level of {survey_type.text[survey]} per day (2011 prices)."
    df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
    df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
    df_tables.loc[j, 'unit'] = "international-$ at 2011 prices"
    df_tables.loc[j, 'shortUnit'] = "$"
    df_tables.loc[j, 'tolerance'] = 5
    df_tables.loc[j, 'type'] = "Numeric"
    df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
    df_tables.loc[j, 'colorScaleNumericBins'] = "1;2;5;10;20;50;50.0001"
    df_tables.loc[j, 'colorScaleEqualSizeBins'] = "'true"
    df_tables.loc[j, 'colorScaleScheme'] = "BuGn"
    df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
    j += 1
    
    df_tables.loc[j, 'name'] = f"Mean {survey_type.text[survey]} per day (2017 prices)"
    df_tables.loc[j, 'slug'] = "mean_ppp2017"
    df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
    df_tables.loc[j, 'description'] = f"The mean level of {survey_type.text[survey]} per day (2017 prices)."
    df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
    df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
    df_tables.loc[j, 'unit'] = "international-$ at 2017 prices"
    df_tables.loc[j, 'shortUnit'] = "$"
    df_tables.loc[j, 'tolerance'] = 5
    df_tables.loc[j, 'type'] = "Numeric"
    df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
    df_tables.loc[j, 'colorScaleNumericBins'] = "1;2;5;10;20;50;50.0001"
    df_tables.loc[j, 'colorScaleEqualSizeBins'] = "'true"
    df_tables.loc[j, 'colorScaleScheme'] = "BuGn"
    df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
    j += 1
    
    df_tables.loc[j, 'name'] = f"Median {survey_type.text[survey]} per day (2011 prices)"
    df_tables.loc[j, 'slug'] = "median_ppp2011"
    df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
    df_tables.loc[j, 'description'] = f"The level of {survey_type.text[survey]} per day below which half of the population live (2011 prices)."
    df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
    df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
    df_tables.loc[j, 'unit'] = "international-$ at 2011 prices"
    df_tables.loc[j, 'shortUnit'] = "$"
    df_tables.loc[j, 'tolerance'] = 5
    df_tables.loc[j, 'type'] = "Numeric"
    df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
    df_tables.loc[j, 'colorScaleNumericBins'] = "1;2;5;10;20;50;50.0001"
    df_tables.loc[j, 'colorScaleEqualSizeBins'] = "'true"
    df_tables.loc[j, 'colorScaleScheme'] = "BuGn"
    df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
    j += 1
    
    df_tables.loc[j, 'name'] = f"Median {survey_type.text[survey]} per day (2017 prices)"
    df_tables.loc[j, 'slug'] = "median_ppp2017"
    df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
    df_tables.loc[j, 'description'] = f"The level of {survey_type.text[survey]} per day below which half of the population live (2017 prices)."
    df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
    df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
    df_tables.loc[j, 'unit'] = "international-$ at 2017 prices"
    df_tables.loc[j, 'shortUnit'] = "$"
    df_tables.loc[j, 'tolerance'] = 5
    df_tables.loc[j, 'type'] = "Numeric"
    df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
    df_tables.loc[j, 'colorScaleNumericBins'] = "1;2;5;10;20;50;50.0001"
    df_tables.loc[j, 'colorScaleEqualSizeBins'] = "'true"
    df_tables.loc[j, 'colorScaleScheme'] = "BuGn"
    df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
    j += 1
    
    df_tables.loc[j, 'name'] = "P10 (2011 prices)"
    df_tables.loc[j, 'slug'] = "decile1_thr_ppp2011"
    df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
    df_tables.loc[j, 'description'] = f"The level of {survey_type.text[survey]} per day below which 10% of the population falls (2011 prices)."
    df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
    df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
    df_tables.loc[j, 'unit'] = "international-$ at 2011 prices"
    df_tables.loc[j, 'shortUnit'] = "$"
    df_tables.loc[j, 'tolerance'] = 5
    df_tables.loc[j, 'type'] = "Numeric"
    df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
    df_tables.loc[j, 'colorScaleNumericBins'] = "1;2;5;10;20;20.0001"
    df_tables.loc[j, 'colorScaleEqualSizeBins'] = "'true"
    df_tables.loc[j, 'colorScaleScheme'] = "Greens"
    df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
    j += 1
    
    df_tables.loc[j, 'name'] = "P10 (2017 prices)"
    df_tables.loc[j, 'slug'] = "decile1_thr_ppp2017"
    df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
    df_tables.loc[j, 'description'] = f"The level of {survey_type.text[survey]} per day below which 10% of the population falls (2017 prices)."
    df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
    df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
    df_tables.loc[j, 'unit'] = "international-$ at 2017 prices"
    df_tables.loc[j, 'shortUnit'] = "$"
    df_tables.loc[j, 'tolerance'] = 5
    df_tables.loc[j, 'type'] = "Numeric"
    df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
    df_tables.loc[j, 'colorScaleNumericBins'] = "1;2;5;10;20;20.0001"
    df_tables.loc[j, 'colorScaleEqualSizeBins'] = "'true"
    df_tables.loc[j, 'colorScaleScheme'] = "Greens"
    df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
    j += 1
    
    df_tables.loc[j, 'name'] = "P90 (2011 prices)"
    df_tables.loc[j, 'slug'] = "decile9_thr_ppp2011"
    df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
    df_tables.loc[j, 'description'] = f"The level of {survey_type.text[survey]} per day above which 10% of the population falls (2011 prices)."
    df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
    df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
    df_tables.loc[j, 'unit'] = "international-$ at 2011 prices"
    df_tables.loc[j, 'shortUnit'] = "$"
    df_tables.loc[j, 'tolerance'] = 5
    df_tables.loc[j, 'type'] = "Numeric"
    df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
    df_tables.loc[j, 'colorScaleNumericBins'] = "5;10;20;50;100;100.0001"
    df_tables.loc[j, 'colorScaleEqualSizeBins'] = "'true"
    df_tables.loc[j, 'colorScaleScheme'] = "Blues"
    df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
    j += 1
    
    df_tables.loc[j, 'name'] = "P90 (2017 prices)"
    df_tables.loc[j, 'slug'] = "decile9_thr_ppp2017"
    df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
    df_tables.loc[j, 'description'] = f"The level of {survey_type.text[survey]} per day above which 10% of the population falls (2017 prices)."
    df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
    df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
    df_tables.loc[j, 'unit'] = "international-$ at 2017 prices"
    df_tables.loc[j, 'shortUnit'] = "$"
    df_tables.loc[j, 'tolerance'] = 5
    df_tables.loc[j, 'type'] = "Numeric"
    df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
    df_tables.loc[j, 'colorScaleNumericBins'] = "5;10;20;50;100;100.0001"
    df_tables.loc[j, 'colorScaleEqualSizeBins'] = "'true"
    df_tables.loc[j, 'colorScaleScheme'] = "Blues"
    df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
    j += 1
      
#Separate the tables into inc, cons and inc or cons
survey_list = list(survey_type['table_name'])
for i in survey_list:
    table_export = df_tables[df_tables['survey_type'] == i].copy().reset_index(drop=True)
    table_export = table_export.drop(columns=['survey_type'])
    table_export.to_csv(f'data/ppp_vs/final/OWID_internal_upload/explorer_ppp_vs/table_{i}.csv', index=False)
# -

# ### Grapher views
# Similar to the tables, this creates the grapher views by grouping by types of variables and then running by survey type and poverty lines.

# +
#Grapher table generation

df_graphers = pd.DataFrame()

j=0

for survey in range(len(survey_type)):
    for p_2011 in range(len(povlines_ppp2011)):

        df_graphers.loc[j, 'title'] = f'{povlines_ppp2011.title_share[p_2011]}'
        df_graphers.loc[j, 'ySlugs'] = f'headcount_ratio_{povlines_ppp2011.cents[p_2011]}_ppp2011'
        df_graphers.loc[j, 'Metric Dropdown'] = "Share in poverty"
        df_graphers.loc[j, 'International-$ Dropdown'] = "2011 prices"
        df_graphers.loc[j, 'Poverty line Dropdown'] = f'{povlines_ppp2011.povline_dropdown[p_2011]}'
        df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df_graphers.loc[j, 'subtitle'] = f'{povlines_ppp2011.subtitle[p_2011]}'
        df_graphers.loc[j, 'note'] = "This data is expressed in international-$ at 2011 prices."
        df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df_graphers.loc[j, 'relatedQuestionUrl'] = np.nan
        df_graphers.loc[j, 'type'] = np.nan
        df_graphers.loc[j, 'yAxisMin'] = 0
        df_graphers.loc[j, 'facet'] = np.nan
        df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
        df_graphers.loc[j, 'hasMapTab'] = "'true"
        df_graphers.loc[j, 'tab'] = "map"
        df_graphers.loc[j, 'mapTargetTime'] = 2019
        j += 1
        
    for p_2017 in range(len(povlines_ppp2017)):

        df_graphers.loc[j, 'title'] = f'{povlines_ppp2017.title_share[p_2017]}'
        df_graphers.loc[j, 'ySlugs'] = f'headcount_ratio_{povlines_ppp2017.cents[p_2017]}_ppp2017'
        df_graphers.loc[j, 'Metric Dropdown'] = "Share in poverty"
        df_graphers.loc[j, 'International-$ Dropdown'] = "2017 prices"
        df_graphers.loc[j, 'Poverty line Dropdown'] = f'{povlines_ppp2017.povline_dropdown[p_2017]}'
        df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df_graphers.loc[j, 'subtitle'] = f'{povlines_ppp2017.subtitle[p_2017]}'
        df_graphers.loc[j, 'note'] = "This data is expressed in international-$ at 2017 prices."
        df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df_graphers.loc[j, 'relatedQuestionUrl'] = np.nan
        df_graphers.loc[j, 'type'] = np.nan
        df_graphers.loc[j, 'yAxisMin'] = 0
        df_graphers.loc[j, 'facet'] = np.nan
        df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
        df_graphers.loc[j, 'hasMapTab'] = "'true"
        df_graphers.loc[j, 'tab'] = "map"
        df_graphers.loc[j, 'mapTargetTime'] = 2019
        j += 1
    
    for p_2011 in range(len(povlines_ppp2011)):

        df_graphers.loc[j, 'title'] = f'{povlines_ppp2011.title_number[p_2011]}'
        df_graphers.loc[j, 'ySlugs'] = f'headcount_{povlines_ppp2011.cents[p_2011]}_ppp2011'
        df_graphers.loc[j, 'Metric Dropdown'] = "Number in poverty"
        df_graphers.loc[j, 'International-$ Dropdown'] = "2011 prices"
        df_graphers.loc[j, 'Poverty line Dropdown'] = f'{povlines_ppp2011.povline_dropdown[p_2011]}'
        df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df_graphers.loc[j, 'subtitle'] = f'{povlines_ppp2011.subtitle[p_2011]}'
        df_graphers.loc[j, 'note'] = "This data is expressed in international-$ at 2011 prices."
        df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df_graphers.loc[j, 'relatedQuestionUrl'] = np.nan
        df_graphers.loc[j, 'type'] = np.nan
        df_graphers.loc[j, 'yAxisMin'] = 0
        df_graphers.loc[j, 'facet'] = np.nan
        df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
        df_graphers.loc[j, 'hasMapTab'] = "'true"
        df_graphers.loc[j, 'tab'] = "map"
        df_graphers.loc[j, 'mapTargetTime'] = 2019
        j += 1
        
    for p_2017 in range(len(povlines_ppp2017)):

        df_graphers.loc[j, 'title'] = f'{povlines_ppp2017.title_number[p_2017]}'
        df_graphers.loc[j, 'ySlugs'] = f'headcount_{povlines_ppp2017.cents[p_2017]}_ppp2017'
        df_graphers.loc[j, 'Metric Dropdown'] = "Number in poverty"
        df_graphers.loc[j, 'International-$ Dropdown'] = "2017 prices"
        df_graphers.loc[j, 'Poverty line Dropdown'] = f'{povlines_ppp2017.povline_dropdown[p_2017]}'
        df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df_graphers.loc[j, 'subtitle'] = f'{povlines_ppp2017.subtitle[p_2017]}'
        df_graphers.loc[j, 'note'] = "This data is expressed in international-$ at 2017 prices."
        df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df_graphers.loc[j, 'relatedQuestionUrl'] = np.nan
        df_graphers.loc[j, 'type'] = np.nan
        df_graphers.loc[j, 'yAxisMin'] = 0
        df_graphers.loc[j, 'facet'] = np.nan
        df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
        df_graphers.loc[j, 'hasMapTab'] = "'true"
        df_graphers.loc[j, 'tab'] = "map"
        df_graphers.loc[j, 'mapTargetTime'] = 2019
        j += 1

    for p in range(len(povlines_both)):

        df_graphers.loc[j, 'title'] = f'{povlines_both.title_share[p]}'
        df_graphers.loc[j, 'ySlugs'] = f'headcount_ratio_{povlines_both.cents_2011[p]}_ppp2011 headcount_ratio_{povlines_both.cents_2017[p]}_ppp2017'
        df_graphers.loc[j, 'Metric Dropdown'] = "Share in poverty"
        df_graphers.loc[j, 'International-$ Dropdown'] = "Compare 2017 and 2011 prices"
        df_graphers.loc[j, 'Poverty line Dropdown'] = f'{povlines_both.povline_dropdown[p]}'
        df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df_graphers.loc[j, 'subtitle'] = f'{povlines_both.subtitle[p]}'
        df_graphers.loc[j, 'note'] = np.nan
        df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df_graphers.loc[j, 'relatedQuestionUrl'] = np.nan
        df_graphers.loc[j, 'type'] = np.nan
        df_graphers.loc[j, 'yAxisMin'] = 0
        df_graphers.loc[j, 'facet'] = "entity"
        df_graphers.loc[j, 'selectedFacetStrategy'] = "entity"
        df_graphers.loc[j, 'hasMapTab'] = np.nan
        df_graphers.loc[j, 'tab'] = np.nan
        df_graphers.loc[j, 'mapTargetTime'] = np.nan
        j += 1
        
    for p in range(len(povlines_both)):

        df_graphers.loc[j, 'title'] = f'{povlines_both.title_number[p]}'
        df_graphers.loc[j, 'ySlugs'] = f'headcount_{povlines_both.cents_2011[p]}_ppp2011 headcount_{povlines_both.cents_2017[p]}_ppp2017'
        df_graphers.loc[j, 'Metric Dropdown'] = "Number in poverty"
        df_graphers.loc[j, 'International-$ Dropdown'] = "Compare 2017 and 2011 prices"
        df_graphers.loc[j, 'Poverty line Dropdown'] = f'{povlines_both.povline_dropdown[p]}'
        df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df_graphers.loc[j, 'subtitle'] = f'{povlines_both.subtitle[p]}'
        df_graphers.loc[j, 'note'] = np.nan
        df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df_graphers.loc[j, 'relatedQuestionUrl'] = np.nan
        df_graphers.loc[j, 'type'] = np.nan
        df_graphers.loc[j, 'yAxisMin'] = 0
        df_graphers.loc[j, 'facet'] = "entity"
        df_graphers.loc[j, 'selectedFacetStrategy'] = "entity"
        df_graphers.loc[j, 'hasMapTab'] = np.nan
        df_graphers.loc[j, 'tab'] = np.nan
        df_graphers.loc[j, 'mapTargetTime'] = np.nan
        j += 1
        
    for pct in range(len(povlines_rel)):

        df_graphers.loc[j, 'title'] = f'{povlines_rel.title_share[pct]} (2011 prices)'
        df_graphers.loc[j, 'ySlugs'] = f'headcount_ratio_{povlines_rel.slug_suffix[pct]}_ppp2011'
        df_graphers.loc[j, 'Metric Dropdown'] = "Share in poverty"
        df_graphers.loc[j, 'International-$ Dropdown'] = "2011 prices"
        df_graphers.loc[j, 'Poverty line Dropdown'] = f'{povlines_rel.dropdown[pct]}'
        df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df_graphers.loc[j, 'subtitle'] = f'Relative poverty is measured in terms of a poverty line that rises and falls over time with average incomes – in this case set at {povlines_rel.text[pct]} {survey_type.text[survey]}.'
        df_graphers.loc[j, 'note'] = "This data is adjusted for inflation and for differences in the cost of living between countries. It is expressed in international-$ at 2011 prices."
        df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df_graphers.loc[j, 'relatedQuestionUrl'] = np.nan
        df_graphers.loc[j, 'type'] = np.nan
        df_graphers.loc[j, 'yAxisMin'] = 0
        df_graphers.loc[j, 'facet'] = np.nan
        df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
        df_graphers.loc[j, 'hasMapTab'] = "'true"
        df_graphers.loc[j, 'tab'] = "map"
        df_graphers.loc[j, 'mapTargetTime'] = 2019
        j += 1
        
    for pct in range(len(povlines_rel)):

        df_graphers.loc[j, 'title'] = f'{povlines_rel.title_share[pct]} (2017 prices)'
        df_graphers.loc[j, 'ySlugs'] = f'headcount_ratio_{povlines_rel.slug_suffix[pct]}_ppp2017'
        df_graphers.loc[j, 'Metric Dropdown'] = "Share in poverty"
        df_graphers.loc[j, 'International-$ Dropdown'] = "2017 prices"
        df_graphers.loc[j, 'Poverty line Dropdown'] = f'{povlines_rel.dropdown[pct]}'
        df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df_graphers.loc[j, 'subtitle'] = f'Relative poverty is measured in terms of a poverty line that rises and falls over time with average incomes – in this case set at {povlines_rel.text[pct]} {survey_type.text[survey]}.'
        df_graphers.loc[j, 'note'] = "This data is adjusted for inflation and for differences in the cost of living between countries. It is expressed in international-$ at 2017 prices."
        df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df_graphers.loc[j, 'relatedQuestionUrl'] = np.nan
        df_graphers.loc[j, 'type'] = np.nan
        df_graphers.loc[j, 'yAxisMin'] = 0
        df_graphers.loc[j, 'facet'] = np.nan
        df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
        df_graphers.loc[j, 'hasMapTab'] = "'true"
        df_graphers.loc[j, 'tab'] = "map"
        df_graphers.loc[j, 'mapTargetTime'] = 2019
        j += 1
        
    for pct in range(len(povlines_rel)):

        df_graphers.loc[j, 'title'] = f'{povlines_rel.title_number[pct]} (2011 prices)'
        df_graphers.loc[j, 'ySlugs'] = f'headcount_{povlines_rel.slug_suffix[pct]}_ppp2011'
        df_graphers.loc[j, 'Metric Dropdown'] = "Number in poverty"
        df_graphers.loc[j, 'International-$ Dropdown'] = "2011 prices"
        df_graphers.loc[j, 'Poverty line Dropdown'] = f'{povlines_rel.dropdown[pct]}'
        df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df_graphers.loc[j, 'subtitle'] = f'Relative poverty is measured in terms of a poverty line that rises and falls over time with average incomes – in this case set at {povlines_rel.text[pct]} {survey_type.text[survey]}.'
        df_graphers.loc[j, 'note'] = "This data is adjusted for inflation and for differences in the cost of living between countries. It is expressed in international-$ at 2011 prices."
        df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df_graphers.loc[j, 'relatedQuestionUrl'] = np.nan
        df_graphers.loc[j, 'type'] = np.nan
        df_graphers.loc[j, 'yAxisMin'] = 0
        df_graphers.loc[j, 'facet'] = np.nan
        df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
        df_graphers.loc[j, 'hasMapTab'] = "'true"
        df_graphers.loc[j, 'tab'] = "map"
        df_graphers.loc[j, 'mapTargetTime'] = 2019
        j += 1
        
    for pct in range(len(povlines_rel)):

        df_graphers.loc[j, 'title'] = f'{povlines_rel.title_number[pct]} (2017 prices)'
        df_graphers.loc[j, 'ySlugs'] = f'headcount_{povlines_rel.slug_suffix[pct]}_ppp2017'
        df_graphers.loc[j, 'Metric Dropdown'] = "Number in poverty"
        df_graphers.loc[j, 'International-$ Dropdown'] = "2017 prices"
        df_graphers.loc[j, 'Poverty line Dropdown'] = f'{povlines_rel.dropdown[pct]}'
        df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df_graphers.loc[j, 'subtitle'] = f'Relative poverty is measured in terms of a poverty line that rises and falls over time with average incomes – in this case set at {povlines_rel.text[pct]} {survey_type.text[survey]}.'
        df_graphers.loc[j, 'note'] = "This data is adjusted for inflation and for differences in the cost of living between countries. It is expressed in international-$ at 2017 prices."
        df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df_graphers.loc[j, 'relatedQuestionUrl'] = np.nan
        df_graphers.loc[j, 'type'] = np.nan
        df_graphers.loc[j, 'yAxisMin'] = 0
        df_graphers.loc[j, 'facet'] = np.nan
        df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
        df_graphers.loc[j, 'hasMapTab'] = "'true"
        df_graphers.loc[j, 'tab'] = "map"
        df_graphers.loc[j, 'mapTargetTime'] = 2019
        j += 1
        

    df_graphers.loc[j, 'title'] = f'Relative poverty: Share of people below 60% of the median (2011 vs. 2017 prices)'
    df_graphers.loc[j, 'ySlugs'] = f'headcount_ratio_60_median_ppp2011 headcount_ratio_60_median_ppp2017'
    df_graphers.loc[j, 'Metric Dropdown'] = "Share in poverty"
    df_graphers.loc[j, 'International-$ Dropdown'] = "Compare 2017 and 2011 prices"
    df_graphers.loc[j, 'Poverty line Dropdown'] = f'Relative poverty: 60% of median'
    df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
    df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
    df_graphers.loc[j, 'subtitle'] = f'Relative poverty is measured in terms of a poverty line that rises and falls over time with average incomes – in this case set at 60% of the median {survey_type.text[survey]}.'
    df_graphers.loc[j, 'note'] = "This data is adjusted for inflation and for differences in the cost of living between countries."
    df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
    df_graphers.loc[j, 'relatedQuestionUrl'] = np.nan
    df_graphers.loc[j, 'type'] = np.nan
    df_graphers.loc[j, 'yAxisMin'] = 0
    df_graphers.loc[j, 'facet'] = "entity"
    df_graphers.loc[j, 'selectedFacetStrategy'] = "entity"
    df_graphers.loc[j, 'hasMapTab'] = np.nan
    df_graphers.loc[j, 'tab'] = np.nan
    df_graphers.loc[j, 'mapTargetTime'] = np.nan
    j += 1

    df_graphers.loc[j, 'title'] = f'Relative poverty: Number of people below 60% of the median (2011 vs. 2017 prices)'
    df_graphers.loc[j, 'ySlugs'] = f'headcount_60_median_ppp2011 headcount_60_median_ppp2017'
    df_graphers.loc[j, 'Metric Dropdown'] = "Number in poverty"
    df_graphers.loc[j, 'International-$ Dropdown'] = "Compare 2017 and 2011 prices"
    df_graphers.loc[j, 'Poverty line Dropdown'] = f'Relative poverty: 60% of median'
    df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
    df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
    df_graphers.loc[j, 'subtitle'] = f'Relative poverty is measured in terms of a poverty line that rises and falls over time with average incomes – in this case set at 60% of the median {survey_type.text[survey]}.'
    df_graphers.loc[j, 'note'] = "This data is adjusted for inflation and for differences in the cost of living between countries."
    df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
    df_graphers.loc[j, 'relatedQuestionUrl'] = np.nan
    df_graphers.loc[j, 'type'] = np.nan
    df_graphers.loc[j, 'yAxisMin'] = 0
    df_graphers.loc[j, 'facet'] = "entity"
    df_graphers.loc[j, 'selectedFacetStrategy'] = "entity"
    df_graphers.loc[j, 'hasMapTab'] = np.nan
    df_graphers.loc[j, 'tab'] = np.nan
    df_graphers.loc[j, 'mapTargetTime'] = np.nan
    j += 1


    df_graphers.loc[j, 'title'] = f"Mean {survey_type.text[survey]} per day (2011 prices)"
    df_graphers.loc[j, 'ySlugs'] = "mean_ppp2011"
    df_graphers.loc[j, 'Metric Dropdown'] = "Mean income or expenditure"
    df_graphers.loc[j, 'International-$ Dropdown'] = "2011 prices"
    df_graphers.loc[j, 'Poverty line Dropdown'] = np.nan
    df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
    df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
    df_graphers.loc[j, 'subtitle'] = "This data is adjusted for inflation and for differences in the cost of living between countries."
    df_graphers.loc[j, 'note'] = "This data is expressed in international-$ at 2011 prices."
    df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
    df_graphers.loc[j, 'relatedQuestionUrl'] = np.nan
    df_graphers.loc[j, 'type'] = np.nan
    df_graphers.loc[j, 'yAxisMin'] = 0
    df_graphers.loc[j, 'facet'] = np.nan
    df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
    df_graphers.loc[j, 'hasMapTab'] = "'true"
    df_graphers.loc[j, 'tab'] = "map"
    df_graphers.loc[j, 'mapTargetTime'] = 2019
    df_graphers.loc[j, 'yScaleToggle'] = "'true"
    j += 1

    df_graphers.loc[j, 'title'] = f"Mean {survey_type.text[survey]} per day (2017 prices)"
    df_graphers.loc[j, 'ySlugs'] = "mean_ppp2017"
    df_graphers.loc[j, 'Metric Dropdown'] = "Mean income or expenditure"
    df_graphers.loc[j, 'International-$ Dropdown'] = "2017 prices"
    df_graphers.loc[j, 'Poverty line Dropdown'] = np.nan
    df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
    df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
    df_graphers.loc[j, 'subtitle'] = "This data is adjusted for inflation and for differences in the cost of living between countries."
    df_graphers.loc[j, 'note'] = "This data is expressed in international-$ at 2017 prices."
    df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
    df_graphers.loc[j, 'relatedQuestionUrl'] = np.nan
    df_graphers.loc[j, 'type'] = np.nan
    df_graphers.loc[j, 'yAxisMin'] = 0
    df_graphers.loc[j, 'facet'] = np.nan
    df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
    df_graphers.loc[j, 'hasMapTab'] = "'true"
    df_graphers.loc[j, 'tab'] = "map"
    df_graphers.loc[j, 'mapTargetTime'] = 2019
    df_graphers.loc[j, 'yScaleToggle'] = "'true"
    j += 1

    df_graphers.loc[j, 'title'] = f"Mean {survey_type.text[survey]} per day: 2011 vs. 2017 prices"
    df_graphers.loc[j, 'ySlugs'] = "mean_ppp2011 mean_ppp2017"
    df_graphers.loc[j, 'Metric Dropdown'] = "Mean income or expenditure"
    df_graphers.loc[j, 'International-$ Dropdown'] = "Compare 2017 and 2011 prices"
    df_graphers.loc[j, 'Poverty line Dropdown'] = np.nan
    df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
    df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
    df_graphers.loc[j, 'subtitle'] = "This data is adjusted for inflation and for differences in the cost of living between countries."
    df_graphers.loc[j, 'note'] = np.nan
    df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
    df_graphers.loc[j, 'relatedQuestionUrl'] = np.nan
    df_graphers.loc[j, 'type'] = np.nan
    df_graphers.loc[j, 'yAxisMin'] = 0
    df_graphers.loc[j, 'facet'] = "entity"
    df_graphers.loc[j, 'selectedFacetStrategy'] = "entity"
    df_graphers.loc[j, 'hasMapTab'] = np.nan
    df_graphers.loc[j, 'tab'] = np.nan
    df_graphers.loc[j, 'mapTargetTime'] = np.nan
    df_graphers.loc[j, 'yScaleToggle'] = "'true"
    j += 1

    df_graphers.loc[j, 'title'] = f"Median {survey_type.text[survey]} per day (2011 prices)"
    df_graphers.loc[j, 'ySlugs'] = "median_ppp2011"
    df_graphers.loc[j, 'Metric Dropdown'] = "Median income or expenditure"
    df_graphers.loc[j, 'International-$ Dropdown'] = "2011 prices"
    df_graphers.loc[j, 'Poverty line Dropdown'] = np.nan
    df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
    df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
    df_graphers.loc[j, 'subtitle'] = "This data is adjusted for inflation and for differences in the cost of living between countries."
    df_graphers.loc[j, 'note'] = "This data is expressed in international-$ at 2011 prices."
    df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
    df_graphers.loc[j, 'relatedQuestionUrl'] = np.nan
    df_graphers.loc[j, 'type'] = np.nan
    df_graphers.loc[j, 'yAxisMin'] = 0
    df_graphers.loc[j, 'facet'] = np.nan
    df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
    df_graphers.loc[j, 'hasMapTab'] = "'true"
    df_graphers.loc[j, 'tab'] = "map"
    df_graphers.loc[j, 'mapTargetTime'] = 2019
    df_graphers.loc[j, 'yScaleToggle'] = "'true"
    j += 1

    df_graphers.loc[j, 'title'] = f"Median {survey_type.text[survey]} per day (2017 prices)"
    df_graphers.loc[j, 'ySlugs'] = "median_ppp2017"
    df_graphers.loc[j, 'Metric Dropdown'] = "Median income or expenditure"
    df_graphers.loc[j, 'International-$ Dropdown'] = "2017 prices"
    df_graphers.loc[j, 'Poverty line Dropdown'] = np.nan
    df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
    df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
    df_graphers.loc[j, 'subtitle'] = "This data is adjusted for inflation and for differences in the cost of living between countries."
    df_graphers.loc[j, 'note'] = "This data is expressed in international-$ at 2017 prices."
    df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
    df_graphers.loc[j, 'relatedQuestionUrl'] = np.nan
    df_graphers.loc[j, 'type'] = np.nan
    df_graphers.loc[j, 'yAxisMin'] = 0
    df_graphers.loc[j, 'facet'] = np.nan
    df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
    df_graphers.loc[j, 'hasMapTab'] = "'true"
    df_graphers.loc[j, 'tab'] = "map"
    df_graphers.loc[j, 'mapTargetTime'] = 2019
    df_graphers.loc[j, 'yScaleToggle'] = "'true"
    j += 1

    df_graphers.loc[j, 'title'] = f"Median {survey_type.text[survey]} per day: 2011 vs. 2017 prices"
    df_graphers.loc[j, 'ySlugs'] = "median_ppp2011 median_ppp2017"
    df_graphers.loc[j, 'Metric Dropdown'] = "Median income or expenditure"
    df_graphers.loc[j, 'International-$ Dropdown'] = "Compare 2017 and 2011 prices"
    df_graphers.loc[j, 'Poverty line Dropdown'] = np.nan
    df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
    df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
    df_graphers.loc[j, 'subtitle'] = "This data is adjusted for inflation and for differences in the cost of living between countries."
    df_graphers.loc[j, 'note'] = np.nan
    df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
    df_graphers.loc[j, 'relatedQuestionUrl'] = np.nan
    df_graphers.loc[j, 'type'] = np.nan
    df_graphers.loc[j, 'yAxisMin'] = 0
    df_graphers.loc[j, 'facet'] = "entity"
    df_graphers.loc[j, 'selectedFacetStrategy'] = "entity"
    df_graphers.loc[j, 'hasMapTab'] = np.nan
    df_graphers.loc[j, 'tab'] = np.nan
    df_graphers.loc[j, 'mapTargetTime'] = np.nan
    df_graphers.loc[j, 'yScaleToggle'] = "'true"
    j += 1

    df_graphers.loc[j, 'title'] = f"P10: The {survey_type.text[survey]} of the poorest tenth (2011 prices)"
    df_graphers.loc[j, 'ySlugs'] = "decile1_thr_ppp2011"
    df_graphers.loc[j, 'Metric Dropdown'] = "P10 (poorest tenth)"
    df_graphers.loc[j, 'International-$ Dropdown'] = "2011 prices"
    df_graphers.loc[j, 'Poverty line Dropdown'] = np.nan
    df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
    df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
    df_graphers.loc[j, 'subtitle'] = f"P10 is the level of {survey_type.text[survey]} per day below which 10% of the population falls."
    df_graphers.loc[j, 'note'] = "This data is adjusted for inflation and for differences in the cost of living between countries. It is expressed in international-$ at 2011 prices."
    df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
    df_graphers.loc[j, 'relatedQuestionUrl'] = np.nan
    df_graphers.loc[j, 'type'] = np.nan
    df_graphers.loc[j, 'yAxisMin'] = 0
    df_graphers.loc[j, 'facet'] = np.nan
    df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
    df_graphers.loc[j, 'hasMapTab'] = "'true"
    df_graphers.loc[j, 'tab'] = "map"
    df_graphers.loc[j, 'mapTargetTime'] = 2019
    df_graphers.loc[j, 'yScaleToggle'] = "'true"
    j += 1

    df_graphers.loc[j, 'title'] = f"P10: The {survey_type.text[survey]} of the poorest tenth (2017 prices)"
    df_graphers.loc[j, 'ySlugs'] = "decile1_thr_ppp2017"
    df_graphers.loc[j, 'Metric Dropdown'] = "P10 (poorest tenth)"
    df_graphers.loc[j, 'International-$ Dropdown'] = "2017 prices"
    df_graphers.loc[j, 'Poverty line Dropdown'] = np.nan
    df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
    df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
    df_graphers.loc[j, 'subtitle'] = f"P10 is the level of {survey_type.text[survey]} per day below which 10% of the population falls."
    df_graphers.loc[j, 'note'] = "This data is adjusted for inflation and for differences in the cost of living between countries. It is expressed in international-$ at 2017 prices."
    df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
    df_graphers.loc[j, 'relatedQuestionUrl'] = np.nan
    df_graphers.loc[j, 'type'] = np.nan
    df_graphers.loc[j, 'yAxisMin'] = 0
    df_graphers.loc[j, 'facet'] = np.nan
    df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
    df_graphers.loc[j, 'hasMapTab'] = "'true"
    df_graphers.loc[j, 'tab'] = "map"
    df_graphers.loc[j, 'mapTargetTime'] = 2019
    df_graphers.loc[j, 'yScaleToggle'] = "'true"
    j += 1

    df_graphers.loc[j, 'title'] = f"P10: The {survey_type.text[survey]} of the poorest tenth (2011 vs. 2017 prices)"
    df_graphers.loc[j, 'ySlugs'] = "decile1_thr_ppp2011 decile1_thr_ppp2017"
    df_graphers.loc[j, 'Metric Dropdown'] = "P10 (poorest tenth)"
    df_graphers.loc[j, 'International-$ Dropdown'] = "Compare 2017 and 2011 prices"
    df_graphers.loc[j, 'Poverty line Dropdown'] = np.nan
    df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
    df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
    df_graphers.loc[j, 'subtitle'] = f"P10 is the level of {survey_type.text[survey]} per day below which 10% of the population falls."
    df_graphers.loc[j, 'note'] = "This data is adjusted for inflation and for differences in the cost of living between countries."
    df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
    df_graphers.loc[j, 'relatedQuestionUrl'] = np.nan
    df_graphers.loc[j, 'type'] = np.nan
    df_graphers.loc[j, 'yAxisMin'] = 0
    df_graphers.loc[j, 'facet'] = "entity"
    df_graphers.loc[j, 'selectedFacetStrategy'] = "entity"
    df_graphers.loc[j, 'hasMapTab'] = np.nan
    df_graphers.loc[j, 'tab'] = np.nan
    df_graphers.loc[j, 'mapTargetTime'] = np.nan
    df_graphers.loc[j, 'yScaleToggle'] = "'true"
    j += 1

    df_graphers.loc[j, 'title'] = f"P90: The {survey_type.text[survey]} of the richest tenth (2011 prices)"
    df_graphers.loc[j, 'ySlugs'] = "decile9_thr_ppp2011"
    df_graphers.loc[j, 'Metric Dropdown'] = "P90 (richest tenth)"
    df_graphers.loc[j, 'International-$ Dropdown'] = "2011 prices"
    df_graphers.loc[j, 'Poverty line Dropdown'] = np.nan
    df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
    df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
    df_graphers.loc[j, 'subtitle'] = f"P90 is the level of {survey_type.text[survey]} per day above which 10% of the population falls."
    df_graphers.loc[j, 'note'] = "This data is adjusted for inflation and for differences in the cost of living between countries. It is expressed in international-$ at 2011 prices."
    df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
    df_graphers.loc[j, 'relatedQuestionUrl'] = np.nan
    df_graphers.loc[j, 'type'] = np.nan
    df_graphers.loc[j, 'yAxisMin'] = 0
    df_graphers.loc[j, 'facet'] = np.nan
    df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
    df_graphers.loc[j, 'hasMapTab'] = "'true"
    df_graphers.loc[j, 'tab'] = "map"
    df_graphers.loc[j, 'mapTargetTime'] = 2019
    df_graphers.loc[j, 'yScaleToggle'] = "'true"
    j += 1

    df_graphers.loc[j, 'title'] = f"P90: The {survey_type.text[survey]} of the richest tenth (2017 prices)"
    df_graphers.loc[j, 'ySlugs'] = "decile9_thr_ppp2017"
    df_graphers.loc[j, 'Metric Dropdown'] = "P90 (richest tenth)"
    df_graphers.loc[j, 'International-$ Dropdown'] = "2017 prices"
    df_graphers.loc[j, 'Poverty line Dropdown'] = np.nan
    df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
    df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
    df_graphers.loc[j, 'subtitle'] = f"P90 is the level of {survey_type.text[survey]} per day above which 10% of the population falls."
    df_graphers.loc[j, 'note'] = "This data is adjusted for inflation and for differences in the cost of living between countries. It is expressed in international-$ at 2017 prices."
    df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
    df_graphers.loc[j, 'relatedQuestionUrl'] = np.nan
    df_graphers.loc[j, 'type'] = np.nan
    df_graphers.loc[j, 'yAxisMin'] = 0
    df_graphers.loc[j, 'facet'] = np.nan
    df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
    df_graphers.loc[j, 'hasMapTab'] = "'true"
    df_graphers.loc[j, 'tab'] = "map"
    df_graphers.loc[j, 'mapTargetTime'] = 2019
    df_graphers.loc[j, 'yScaleToggle'] = "'true"
    j += 1

    df_graphers.loc[j, 'title'] = f"P90: The {survey_type.text[survey]} of the richest tenth (2011 vs. 2017 prices)"
    df_graphers.loc[j, 'ySlugs'] = "decile9_thr_ppp2011 decile9_thr_ppp2017"
    df_graphers.loc[j, 'Metric Dropdown'] = "P90 (richest tenth)"
    df_graphers.loc[j, 'International-$ Dropdown'] = "Compare 2017 and 2011 prices"
    df_graphers.loc[j, 'Poverty line Dropdown'] = np.nan
    df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
    df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
    df_graphers.loc[j, 'subtitle'] = f"P90 is the level of {survey_type.text[survey]} per day above which 10% of the population falls."
    df_graphers.loc[j, 'note'] = "This data is adjusted for inflation and for differences in the cost of living between countries."
    df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
    df_graphers.loc[j, 'relatedQuestionUrl'] = np.nan
    df_graphers.loc[j, 'type'] = np.nan
    df_graphers.loc[j, 'yAxisMin'] = 0
    df_graphers.loc[j, 'facet'] = "entity"
    df_graphers.loc[j, 'selectedFacetStrategy'] = "entity"
    df_graphers.loc[j, 'hasMapTab'] = np.nan
    df_graphers.loc[j, 'tab'] = np.nan
    df_graphers.loc[j, 'mapTargetTime'] = np.nan
    df_graphers.loc[j, 'yScaleToggle'] = "'true"
    j += 1
    
#Select one default view
df_graphers.loc[(df_graphers['ySlugs'] == "headcount_ratio_190_ppp2011 headcount_ratio_215_ppp2017") 
       & (df_graphers['tableSlug'] == "inc_or_cons"), ['defaultView']] = "'true"
    
    
#Reorder dropdown menus
povline_dropdown_list = ['$1 per day',
                         '$1.90 per day: International Poverty Line',
                         '$2.15 per day: International Poverty Line',
                         '$3.20 per day: Lower-middle income poverty line',
                         '$3.65 per day: Lower-middle income poverty line',
                         '$5.50 per day: Upper-middle income poverty line',
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


df_graphers_mapping = pd.DataFrame({'povline_dropdown': povline_dropdown_list,})
df_graphers_mapping = df_graphers_mapping.reset_index().set_index('povline_dropdown')

df_graphers['povline_dropdown_aux'] = df_graphers['Poverty line Dropdown'].map(df_graphers_mapping['index'])
df_graphers = df_graphers.sort_values('povline_dropdown_aux', ignore_index=True)
df_graphers = df_graphers.drop(columns=['povline_dropdown_aux'])

#Export Grapher table    
df_graphers.to_csv(f'data/ppp_vs/final/OWID_internal_upload/explorer_ppp_vs/grapher.csv', index=False)
