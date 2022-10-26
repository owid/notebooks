import pandas as pd
import numpy as np

# +
#Read Google sheets
sheet_id = '17KJ9YcvfdmO_7-Sv2Ij0vmzAQI6rXSIqHfJtgFHN-a8'

sheet_name = 'povlines_abs'
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
povlines_abs = pd.read_csv(url, dtype={'dollars_text':'str'})

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
    
    #Headcount ratio (abs)
    for p in range(len(povlines_abs)):
        df_tables.loc[j, 'name'] = f'Share of population below ${povlines_abs.dollars_text[p]} a day'
        df_tables.loc[j, 'slug'] = f'headcount_ratio_{povlines_abs.cents[p]}'
        df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df_tables.loc[j, 'description'] = f'% of population living in households with an {survey_type.text[survey]} per person below ${povlines_abs.dollars_text[p]} a day.'
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
        
    #Headcount (abs)
    for p in range(len(povlines_abs)):
        df_tables.loc[j, 'name'] = f'Number of people below ${povlines_abs.dollars_text[p]} a day'
        df_tables.loc[j, 'slug'] = f'headcount_{povlines_abs.cents[p]}'
        df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df_tables.loc[j, 'description'] = f'Number of people living in households with an {survey_type.text[survey]} per person below ${povlines_abs.dollars_text[p]} a day.'
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
        
    #Total shortfall (abs)
    for p in range(len(povlines_abs)):
        df_tables.loc[j, 'name'] = f'${povlines_abs.dollars_text[p]} a day - total daily shortfall'
        df_tables.loc[j, 'slug'] = f'total_shortfall_{povlines_abs.cents[p]}'
        df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df_tables.loc[j, 'description'] = f'The total shortfall from a poverty line of ${povlines_abs.dollars_text[p]} a day. This is the amount of money that would be theoretically needed to lift the {survey_type.text[survey]} of all people in poverty up to the poverty line. However this is not a measure of the actual cost of eliminating poverty, since it does not take into account the costs involved in making the necessary transfers nor any changes in behaviour they would bring about.'
        df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
        df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
        df_tables.loc[j, 'unit'] = "international-$ at 2017 prices"
        df_tables.loc[j, 'shortUnit'] = "$"
        df_tables.loc[j, 'tolerance'] = 5
        df_tables.loc[j, 'type'] = "Numeric"
        df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
        df_tables.loc[j, 'colorScaleNumericBins'] = "100000;300000;1000000;3000000;10000000;30000000;100000000;300000000;1000000000;1000000001"
        df_tables.loc[j, 'colorScaleEqualSizeBins'] = "'true"
        df_tables.loc[j, 'colorScaleScheme'] = "Oranges"
        df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1
    
    #Average shortfall ($ per day)
    for p in range(len(povlines_abs)):
        df_tables.loc[j, 'name'] = f'${povlines_abs.dollars_text[p]} a day - average daily shortfall'
        df_tables.loc[j, 'slug'] = f'avg_shortfall_{povlines_abs.cents[p]}'
        df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df_tables.loc[j, 'description'] = f'The average shortfall from a poverty line of ${povlines_abs.dollars_text[p]} a day (averaged across the population in poverty).'
        df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
        df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
        df_tables.loc[j, 'unit'] = "international-$ at 2017 prices"
        df_tables.loc[j, 'shortUnit'] = "$"
        df_tables.loc[j, 'tolerance'] = 5
        df_tables.loc[j, 'type'] = "Numeric"
        df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
        df_tables.loc[j, 'colorScaleNumericBins'] = povlines_abs.scale_avg_shortfall[p]
        df_tables.loc[j, 'colorScaleEqualSizeBins'] = "'true"
        df_tables.loc[j, 'colorScaleScheme'] = "Purples"
        df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1
    
    #Average shortfall (% of poverty line) [this is the income gap ratio]
    for p in range(len(povlines_abs)):
        df_tables.loc[j, 'name'] = f'${povlines_abs.dollars_text[p]} a day - income gap ratio'
        df_tables.loc[j, 'slug'] = f'income_gap_ratio_{povlines_abs.cents[p]}'
        df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df_tables.loc[j, 'description'] = f'The average shortfall from a poverty line of ${povlines_abs.dollars_text[p]} a day (averaged across the population in poverty) expressed as a share of the poverty line. This metric is sometimes called the "income gap ratio". It captures the depth of poverty in which those below the poverty line are living.'
        df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
        df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
        df_tables.loc[j, 'unit'] = "%"
        df_tables.loc[j, 'shortUnit'] = "%"
        df_tables.loc[j, 'tolerance'] = 5
        df_tables.loc[j, 'type'] = "Numeric"
        df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
        df_tables.loc[j, 'colorScaleNumericBins'] = "10;20;30;40;50;60;70;80;90;100"
        df_tables.loc[j, 'colorScaleEqualSizeBins'] = "'true"
        df_tables.loc[j, 'colorScaleScheme'] = "YlOrRd"
        df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1
    
    #Poverty gap index
    for p in range(len(povlines_abs)):
        df_tables.loc[j, 'name'] = f'${povlines_abs.dollars_text[p]} a day - poverty gap index'
        df_tables.loc[j, 'slug'] = f'poverty_gap_index_{povlines_abs.cents[p]}'
        df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df_tables.loc[j, 'description'] = f'The poverty gap index calculated at a poverty line of ${povlines_abs.dollars_text[p]} a day. The poverty gap index is a measure that reflects both the depth and prevalence of poverty. It is defined as the mean shortfall of the total population from the poverty line counting the non-poor as having zero shortfall and expressed as a percentage of the poverty line.  It is worth unpacking that definition a little. For those below the poverty line, the shortfall corresponds to the amount of money required in order to reach the poverty line. For those at or above the poverty line, the shortfall is counted as zero. The average shortfall is then calculated across the total population – both poor and non-poor – and then expressed as a share of the poverty line. Unlike the more commonly-used metric of the headcount ratio, the poverty gap index is thus sensitive not only to whether a person’s income falls below the poverty line or not, but also by how much – i.e. to the depth of poverty they experience.'
        df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
        df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
        df_tables.loc[j, 'unit'] = "%"
        df_tables.loc[j, 'shortUnit'] = "%"
        df_tables.loc[j, 'tolerance'] = 5
        df_tables.loc[j, 'type'] = "Numeric"
        df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
        df_tables.loc[j, 'colorScaleNumericBins'] = "10;20;30;40;50;60;70;80;90;100"
        df_tables.loc[j, 'colorScaleEqualSizeBins'] = "'true"
        df_tables.loc[j, 'colorScaleScheme'] = "RdPu"
        df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1
        
    #Headcount ratio (rel)
    for pct in range(len(povlines_rel)):
        df_tables.loc[j, 'name'] = f'{povlines_rel.percent[pct]} of median - share of population below poverty line'
        df_tables.loc[j, 'slug'] = f'headcount_ratio_{povlines_rel.slug_suffix[pct]}'
        df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df_tables.loc[j, 'description'] = f'% of population living in households with an {survey_type.text[survey]} per person below {povlines_rel.percent[pct]} of the median.'
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
        
    #Headcount (rel)
    for pct in range(len(povlines_rel)):
        df_tables.loc[j, 'name'] = f'{povlines_rel.percent[pct]} of median - total number of people below poverty line'
        df_tables.loc[j, 'slug'] = f'headcount_{povlines_rel.slug_suffix[pct]}'
        df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df_tables.loc[j, 'description'] = f'Number of people living in households with an {survey_type.text[survey]} per person below {povlines_rel.percent[pct]} of the median.'
        df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
        df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP), adapted by Our World in Data."
        df_tables.loc[j, 'unit'] = np.nan
        df_tables.loc[j, 'shortUnit'] = np.nan
        df_tables.loc[j, 'tolerance'] = 5
        df_tables.loc[j, 'type'] = "Numeric"
        df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
        df_tables.loc[j, 'colorScaleNumericBins'] = "100000;300000;1000000;3000000;10000000;30000000;100000000;300000000;1000000000;1000000001"
        df_tables.loc[j, 'colorScaleEqualSizeBins'] = "'true"
        df_tables.loc[j, 'colorScaleScheme'] = "YlOrBr"
        df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1
        
    #Total shortfall (rel)
    for pct in range(len(povlines_rel)):
        df_tables.loc[j, 'name'] = f'{povlines_rel.percent[pct]} of median - total daily shortfall'
        df_tables.loc[j, 'slug'] = f'total_shortfall_{povlines_rel.slug_suffix[pct]}'
        df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df_tables.loc[j, 'description'] = f'The total shortfall from a poverty line of {povlines_rel.text[pct]} {survey_type.text[survey]}. This is the amount of money that would be theoretically needed to lift the {survey_type.text[survey]} of all people in poverty up to the poverty line. However this is not a measure of the actual cost of eliminating poverty, since it does not take into account the costs involved in making the necessary transfers nor any changes in behaviour they would bring about.'
        df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
        df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP), adapted by Our World in Data."
        df_tables.loc[j, 'unit'] = np.nan
        df_tables.loc[j, 'shortUnit'] = np.nan
        df_tables.loc[j, 'tolerance'] = 5
        df_tables.loc[j, 'type'] = "Numeric"
        df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
        df_tables.loc[j, 'colorScaleNumericBins'] = "100000;300000;1000000;3000000;10000000;30000000;100000000;300000000;1000000000;1000000001"
        df_tables.loc[j, 'colorScaleEqualSizeBins'] = "'true"
        df_tables.loc[j, 'colorScaleScheme'] = "YlOrBr"
        df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1
        
    #Average shortfall ($ per day)
    for pct in range(len(povlines_rel)):
        df_tables.loc[j, 'name'] = f'{povlines_rel.percent[pct]} of median - average daily shortfall'
        df_tables.loc[j, 'slug'] = f'avg_shortfall_{povlines_rel.slug_suffix[pct]}'
        df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df_tables.loc[j, 'description'] = f'The average shortfall from a poverty line of of {povlines_rel.text[pct]} {survey_type.text[survey]} (averaged across the population in poverty).'
        df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
        df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
        df_tables.loc[j, 'unit'] = "international-$ at 2017 prices"
        df_tables.loc[j, 'shortUnit'] = "$"
        df_tables.loc[j, 'tolerance'] = 5
        df_tables.loc[j, 'type'] = "Numeric"
        df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
        df_tables.loc[j, 'colorScaleNumericBins'] = "1;2;5;10;20;20.0001"
        df_tables.loc[j, 'colorScaleEqualSizeBins'] = "'true"
        df_tables.loc[j, 'colorScaleScheme'] = "YlOrBr"
        df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1
    
    #Average shortfall (% of poverty line) [this is the income gap ratio]
    for pct in range(len(povlines_rel)):
        df_tables.loc[j, 'name'] = f'{povlines_rel.percent[pct]} of median - income gap ratio'
        df_tables.loc[j, 'slug'] = f'income_gap_ratio_{povlines_rel.slug_suffix[pct]}'
        df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df_tables.loc[j, 'description'] = f'The average shortfall from a poverty line of of {povlines_rel.text[pct]} {survey_type.text[survey]} (averaged across the population in poverty) expressed as a share of the poverty line. This metric is sometimes called the "income gap ratio". It captures the depth of poverty in which those below the poverty line are living.'
        df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
        df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
        df_tables.loc[j, 'unit'] = "%"
        df_tables.loc[j, 'shortUnit'] = "%"
        df_tables.loc[j, 'tolerance'] = 5
        df_tables.loc[j, 'type'] = "Numeric"
        df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
        df_tables.loc[j, 'colorScaleNumericBins'] = "10;20;30;40;50;60;70;80;90;100"
        df_tables.loc[j, 'colorScaleEqualSizeBins'] = "'true"
        df_tables.loc[j, 'colorScaleScheme'] = "YlOrBr"
        df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1
    
    #Poverty gap index
    for pct in range(len(povlines_rel)):
        df_tables.loc[j, 'name'] = f'{povlines_rel.percent[pct]} of median - poverty gap index'
        df_tables.loc[j, 'slug'] = f'poverty_gap_index_{povlines_rel.slug_suffix[pct]}'
        df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df_tables.loc[j, 'description'] = f'The poverty gap index calculated at a poverty line of {povlines_rel.text[pct]} {survey_type.text[survey]}. The poverty gap index is a measure that reflects both the depth and prevalence of poverty. It is defined as the mean shortfall of the total population from the poverty line counting the non-poor as having zero shortfall and expressed as a percentage of the poverty line.  It is worth unpacking that definition a little. For those below the poverty line, the shortfall corresponds to the amount of money required in order to reach the poverty line. For those at or above the poverty line, the shortfall is counted as zero. The average shortfall is then calculated across the total population – both poor and non-poor – and then expressed as a share of the poverty line. Unlike the more commonly-used metric of the headcount ratio, the poverty gap index is thus sensitive not only to whether a person’s income falls below the poverty line or not, but also by how much – i.e. to the depth of poverty they experience.'
        df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
        df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
        df_tables.loc[j, 'unit'] = "%"
        df_tables.loc[j, 'shortUnit'] = "%"
        df_tables.loc[j, 'tolerance'] = 5
        df_tables.loc[j, 'type'] = "Numeric"
        df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
        df_tables.loc[j, 'colorScaleNumericBins'] = "3;6;9;12;15;18;21"
        df_tables.loc[j, 'colorScaleEqualSizeBins'] = "'true"
        df_tables.loc[j, 'colorScaleScheme'] = "YlOrBr"
        df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1
        
    
      
#Separate the tables into inc, cons and inc or cons
survey_list = list(survey_type['table_name'])
for i in survey_list:
    table_export = df_tables[df_tables['survey_type'] == i].copy().reset_index(drop=True)
    table_export = table_export.drop(columns=['survey_type'])
    table_export.to_csv(f'data/ppp_2017/final/OWID_internal_upload/explorer_database/complete_poverty/table_{i}.csv', index=False)
# -

# ### Grapher views
# Similar to the tables, this creates the grapher views by grouping by types of variables and then running by survey type and poverty lines.

# +
#Grapher table generation

df_graphers = pd.DataFrame()

j=0

for survey in range(len(survey_type)):
    
    #Headcount ratio (abs)    
    for p in range(len(povlines_abs)):

        df_graphers.loc[j, 'title'] = f'{povlines_abs.title_share[p]}'
        df_graphers.loc[j, 'ySlugs'] = f'headcount_ratio_{povlines_abs.cents[p]}'
        df_graphers.loc[j, 'Metric Dropdown'] = "Share in poverty"
        df_graphers.loc[j, 'Poverty line Dropdown'] = f'{povlines_abs.povline_dropdown[p]}'
        df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df_graphers.loc[j, 'subtitle'] = f'{povlines_abs.subtitle[p]}'
        df_graphers.loc[j, 'note'] = "This data is expressed in international-$ at 2017 prices."
        df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df_graphers.loc[j, 'relatedQuestionUrl'] = "https://ourworldindata.org/poverty"
        df_graphers.loc[j, 'type'] = np.nan
        df_graphers.loc[j, 'yAxisMin'] = 0
        df_graphers.loc[j, 'facet'] = np.nan
        df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
        df_graphers.loc[j, 'hasMapTab'] = "'true"
        df_graphers.loc[j, 'tab'] = "map"
        df_graphers.loc[j, 'mapTargetTime'] = 2019
        j += 1
        
    #Headcount (abs)
    for p in range(len(povlines_abs)):

        df_graphers.loc[j, 'title'] = f'{povlines_abs.title_number[p]}'
        df_graphers.loc[j, 'ySlugs'] = f'headcount_{povlines_abs.cents[p]}'
        df_graphers.loc[j, 'Metric Dropdown'] = "Number in poverty"
        df_graphers.loc[j, 'Poverty line Dropdown'] = f'{povlines_abs.povline_dropdown[p]}'
        df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df_graphers.loc[j, 'subtitle'] = f'{povlines_abs.subtitle[p]}'
        df_graphers.loc[j, 'note'] = "This data is expressed in international-$ at 2017 prices."
        df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df_graphers.loc[j, 'relatedQuestionUrl'] = "https://ourworldindata.org/poverty"
        df_graphers.loc[j, 'type'] = np.nan
        df_graphers.loc[j, 'yAxisMin'] = 0
        df_graphers.loc[j, 'facet'] = np.nan
        df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
        df_graphers.loc[j, 'hasMapTab'] = "'true"
        df_graphers.loc[j, 'tab'] = "map"
        df_graphers.loc[j, 'mapTargetTime'] = 2019
        j += 1
        
    #Total shortfall (abs)
    for p in range(len(povlines_abs)):

        df_graphers.loc[j, 'title'] = f'{povlines_abs.title_total_shortfall[p]}'
        df_graphers.loc[j, 'ySlugs'] = f'total_shortfall_{povlines_abs.cents[p]}'
        df_graphers.loc[j, 'Metric Dropdown'] = "Total shortfall from poverty line"
        df_graphers.loc[j, 'Poverty line Dropdown'] = f'{povlines_abs.povline_dropdown[p]}'
        df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df_graphers.loc[j, 'subtitle'] = f'{povlines_abs.subtitle_total_shortfall[p]}'
        df_graphers.loc[j, 'note'] = "This data is expressed in international-$ at 2017 prices. The cost of closing the poverty gap does not take into account costs and inefficiencies from making the necessary transfers."
        df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df_graphers.loc[j, 'relatedQuestionUrl'] = "https://ourworldindata.org/poverty"
        df_graphers.loc[j, 'type'] = np.nan
        df_graphers.loc[j, 'yAxisMin'] = 0
        df_graphers.loc[j, 'facet'] = np.nan
        df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
        df_graphers.loc[j, 'hasMapTab'] = "'true"
        df_graphers.loc[j, 'tab'] = "map"
        df_graphers.loc[j, 'mapTargetTime'] = 2019
        j += 1
    
    #Average shortfall ($ per day)
    for p in range(len(povlines_abs)):

        df_graphers.loc[j, 'title'] = f'{povlines_abs.title_avg_shortfall[p]}'
        df_graphers.loc[j, 'ySlugs'] = f'avg_shortfall_{povlines_abs.cents[p]}'
        df_graphers.loc[j, 'Metric Dropdown'] = "Average shortfall ($ per day)"
        df_graphers.loc[j, 'Poverty line Dropdown'] = f'{povlines_abs.povline_dropdown[p]}'
        df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df_graphers.loc[j, 'subtitle'] = f'{povlines_abs.subtitle_avg_shortfall[p]}'
        df_graphers.loc[j, 'note'] = "This data relates to household income or expenditure, measured in international-$ at 2017 prices to account for inflation and differences in the cost of living between countries."
        df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df_graphers.loc[j, 'relatedQuestionUrl'] = "https://ourworldindata.org/poverty"
        df_graphers.loc[j, 'type'] = np.nan
        df_graphers.loc[j, 'yAxisMin'] = 0
        df_graphers.loc[j, 'facet'] = np.nan
        df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
        df_graphers.loc[j, 'hasMapTab'] = "'true"
        df_graphers.loc[j, 'tab'] = "map"
        df_graphers.loc[j, 'mapTargetTime'] = 2019
        j += 1
        
    #Average shortfall (% of poverty line)
    for p in range(len(povlines_abs)):

        df_graphers.loc[j, 'title'] = f'{povlines_abs.title_income_gap_ratio[p]}'
        df_graphers.loc[j, 'ySlugs'] = f'income_gap_ratio_{povlines_abs.cents[p]}'
        df_graphers.loc[j, 'Metric Dropdown'] = "Average shortfall (% of poverty line)"
        df_graphers.loc[j, 'Poverty line Dropdown'] = f'{povlines_abs.povline_dropdown[p]}'
        df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df_graphers.loc[j, 'subtitle'] = f'{povlines_abs.subtitle_income_gap_ratio[p]}'
        df_graphers.loc[j, 'note'] = "This data relates to household income or expenditure, measured in international-$ at 2017 prices to account for inflation and differences in the cost of living between countries."
        df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df_graphers.loc[j, 'relatedQuestionUrl'] = "https://ourworldindata.org/poverty"
        df_graphers.loc[j, 'type'] = np.nan
        df_graphers.loc[j, 'yAxisMin'] = 0
        df_graphers.loc[j, 'facet'] = np.nan
        df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
        df_graphers.loc[j, 'hasMapTab'] = "'true"
        df_graphers.loc[j, 'tab'] = "map"
        df_graphers.loc[j, 'mapTargetTime'] = 2019
        j += 1
        
    #Poverty gap index
    for p in range(len(povlines_abs)):

        df_graphers.loc[j, 'title'] = f'Poverty gap index at ${povlines_abs.dollars_text[p]} a day'
        df_graphers.loc[j, 'ySlugs'] = f'poverty_gap_index_{povlines_abs.cents[p]}'
        df_graphers.loc[j, 'Metric Dropdown'] = "Poverty gap index"
        df_graphers.loc[j, 'Poverty line Dropdown'] = f'{povlines_abs.povline_dropdown[p]}'
        df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df_graphers.loc[j, 'subtitle'] = f'The poverty gap index is the mean shortfall from the poverty line counting the non-poor as having zero shortfall, and expressed as a percentage of the poverty line. This data is adjusted for inflation and for differences in the cost of living between countries.'
        df_graphers.loc[j, 'note'] = "This data is expressed in international-$ at 2017 prices. Depending on the country and year, the data relates to either income or expenditure."
        df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df_graphers.loc[j, 'relatedQuestionUrl'] = "https://ourworldindata.org/poverty"
        df_graphers.loc[j, 'type'] = np.nan
        df_graphers.loc[j, 'yAxisMin'] = 0
        df_graphers.loc[j, 'facet'] = np.nan
        df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
        df_graphers.loc[j, 'hasMapTab'] = "'true"
        df_graphers.loc[j, 'tab'] = "map"
        df_graphers.loc[j, 'mapTargetTime'] = 2019
        j += 1
        
    #Headcount ratio (rel)
    for pct in range(len(povlines_rel)):

        df_graphers.loc[j, 'title'] = f'{povlines_rel.title_share[pct]}'
        df_graphers.loc[j, 'ySlugs'] = f'headcount_ratio_{povlines_rel.slug_suffix[pct]}'
        df_graphers.loc[j, 'Metric Dropdown'] = "Share in poverty"
        df_graphers.loc[j, 'Poverty line Dropdown'] = f'{povlines_rel.dropdown[pct]}'
        df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df_graphers.loc[j, 'subtitle'] = f'Relative poverty is measured in terms of a poverty line that rises and falls over time with average incomes – in this case set at {povlines_rel.text[pct]} {survey_type.text[survey]}.'
        df_graphers.loc[j, 'note'] = "This data is adjusted for inflation and for differences in the cost of living between countries. It is expressed in international-$ at 2017 prices."
        df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df_graphers.loc[j, 'relatedQuestionUrl'] = "https://ourworldindata.org/poverty"
        df_graphers.loc[j, 'type'] = np.nan
        df_graphers.loc[j, 'yAxisMin'] = 0
        df_graphers.loc[j, 'facet'] = np.nan
        df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
        df_graphers.loc[j, 'hasMapTab'] = "'true"
        df_graphers.loc[j, 'tab'] = "map"
        df_graphers.loc[j, 'mapTargetTime'] = 2019
        j += 1
        
    #Headcount (rel)    
    for pct in range(len(povlines_rel)):

        df_graphers.loc[j, 'title'] = f'{povlines_rel.title_number[pct]}'
        df_graphers.loc[j, 'ySlugs'] = f'headcount_{povlines_rel.slug_suffix[pct]}'
        df_graphers.loc[j, 'Metric Dropdown'] = "Number in poverty"
        df_graphers.loc[j, 'Poverty line Dropdown'] = f'{povlines_rel.dropdown[pct]}'
        df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df_graphers.loc[j, 'subtitle'] = f'Relative poverty is measured in terms of a poverty line that rises and falls over time with average incomes – in this case set at {povlines_rel.text[pct]} {survey_type.text[survey]}.'
        df_graphers.loc[j, 'note'] = "This data is adjusted for inflation and for differences in the cost of living between countries. It is expressed in international-$ at 2017 prices."
        df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df_graphers.loc[j, 'relatedQuestionUrl'] = "https://ourworldindata.org/poverty"
        df_graphers.loc[j, 'type'] = np.nan
        df_graphers.loc[j, 'yAxisMin'] = 0
        df_graphers.loc[j, 'facet'] = np.nan
        df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
        df_graphers.loc[j, 'hasMapTab'] = "'true"
        df_graphers.loc[j, 'tab'] = "map"
        df_graphers.loc[j, 'mapTargetTime'] = 2019
        j += 1
        
    #Total shortfall (rel)    
    for pct in range(len(povlines_rel)):

        df_graphers.loc[j, 'title'] = f'Total shortfall from a poverty line of {povlines_rel.text[pct]} {survey_type.text[survey]}'
        df_graphers.loc[j, 'ySlugs'] = f'total_shortfall_{povlines_rel.slug_suffix[pct]}'
        df_graphers.loc[j, 'Metric Dropdown'] = "Total shortfall from poverty line"
        df_graphers.loc[j, 'Poverty line Dropdown'] = f'{povlines_rel.dropdown[pct]}'
        df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df_graphers.loc[j, 'subtitle'] = f'This is the amount of money that would be theoretically needed to lift the incomes of all people in poverty up to the {povlines_rel.text[pct]} {survey_type.text[survey]}. This data is adjusted for inflation and for differences in the cost of living between countries.'
        df_graphers.loc[j, 'note'] = "This data is adjusted for inflation and for differences in the cost of living between countries. It is expressed in international-$ at 2017 prices."
        df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df_graphers.loc[j, 'relatedQuestionUrl'] = "https://ourworldindata.org/poverty"
        df_graphers.loc[j, 'type'] = np.nan
        df_graphers.loc[j, 'yAxisMin'] = 0
        df_graphers.loc[j, 'facet'] = np.nan
        df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
        df_graphers.loc[j, 'hasMapTab'] = "'true"
        df_graphers.loc[j, 'tab'] = "map"
        df_graphers.loc[j, 'mapTargetTime'] = 2019
        j += 1
        
    #Average shortfall ($ per day) (rel)    
    for pct in range(len(povlines_rel)):

        df_graphers.loc[j, 'title'] = f'Average shortfall from a poverty line of {povlines_rel.text[pct]} {survey_type.text[survey]}'
        df_graphers.loc[j, 'ySlugs'] = f'avg_shortfall_{povlines_rel.slug_suffix[pct]}'
        df_graphers.loc[j, 'Metric Dropdown'] = "Average shortfall ($ per day)"
        df_graphers.loc[j, 'Poverty line Dropdown'] = f'{povlines_rel.dropdown[pct]}'
        df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df_graphers.loc[j, 'subtitle'] = f'This is the amount of money that would be theoretically needed to lift the incomes of all people in poverty up to the {povlines_rel.text[pct]} {survey_type.text[survey]}, averaged across the population in poverty.'
        df_graphers.loc[j, 'note'] = "This data relates to household income or expenditure, measured in international-$ at 2017 prices to account for inflation and differences in the cost of living between countries."
        df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df_graphers.loc[j, 'relatedQuestionUrl'] = "https://ourworldindata.org/poverty"
        df_graphers.loc[j, 'type'] = np.nan
        df_graphers.loc[j, 'yAxisMin'] = 0
        df_graphers.loc[j, 'facet'] = np.nan
        df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
        df_graphers.loc[j, 'hasMapTab'] = "'true"
        df_graphers.loc[j, 'tab'] = "map"
        df_graphers.loc[j, 'mapTargetTime'] = 2019
        j += 1
        
    #Average shortfall (% of poverty line) (rel)    
    for pct in range(len(povlines_rel)):

        df_graphers.loc[j, 'title'] = f'Average shortfall from a poverty line of {povlines_rel.text[pct]} {survey_type.text[survey]} (as a share of the poverty line)'
        df_graphers.loc[j, 'ySlugs'] = f'income_gap_ratio_{povlines_rel.slug_suffix[pct]}'
        df_graphers.loc[j, 'Metric Dropdown'] = "Average shortfall (% of poverty line)"
        df_graphers.loc[j, 'Poverty line Dropdown'] = f'{povlines_rel.dropdown[pct]}'
        df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df_graphers.loc[j, 'subtitle'] = f'This is the average shortfall expressed as a share of the poverty line, sometimes called the "income gap ratio". It captures the depth of poverty in which those below {povlines_rel.text[pct]} {survey_type.text[survey]} a day are living.'
        df_graphers.loc[j, 'note'] = "This data relates to household income or expenditure, measured in international-$ at 2017 prices to account for inflation and differences in the cost of living between countries."
        df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df_graphers.loc[j, 'relatedQuestionUrl'] = "https://ourworldindata.org/poverty"
        df_graphers.loc[j, 'type'] = np.nan
        df_graphers.loc[j, 'yAxisMin'] = 0
        df_graphers.loc[j, 'facet'] = np.nan
        df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
        df_graphers.loc[j, 'hasMapTab'] = "'true"
        df_graphers.loc[j, 'tab'] = "map"
        df_graphers.loc[j, 'mapTargetTime'] = 2019
        j += 1
        
    #Poverty gap index (rel)    
    for pct in range(len(povlines_rel)):

        df_graphers.loc[j, 'title'] = f'Poverty gap index at {povlines_rel.text[pct]} {survey_type.text[survey]}'
        df_graphers.loc[j, 'ySlugs'] = f'poverty_gap_index_{povlines_rel.slug_suffix[pct]}'
        df_graphers.loc[j, 'Metric Dropdown'] = "Poverty gap index"
        df_graphers.loc[j, 'Poverty line Dropdown'] = f'{povlines_rel.dropdown[pct]}'
        df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df_graphers.loc[j, 'subtitle'] = f'The poverty gap index is the mean shortfall from the poverty line counting the non-poor as having zero shortfall, and expressed as a percentage of the poverty line. This data is adjusted for inflation and for differences in the cost of living between countries.'
        df_graphers.loc[j, 'note'] = "This data is expressed in international-$ at 2017 prices. Depending on the country and year, the data relates to either income or expenditure."
        df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df_graphers.loc[j, 'relatedQuestionUrl'] = "https://ourworldindata.org/poverty"
        df_graphers.loc[j, 'type'] = np.nan
        df_graphers.loc[j, 'yAxisMin'] = 0
        df_graphers.loc[j, 'facet'] = np.nan
        df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
        df_graphers.loc[j, 'hasMapTab'] = "'true"
        df_graphers.loc[j, 'tab'] = "map"
        df_graphers.loc[j, 'mapTargetTime'] = 2019
        j += 1
    
#Select one default view
df_graphers.loc[(df_graphers['ySlugs'] == "headcount_ratio_215") 
       & (df_graphers['tableSlug'] == "inc_or_cons"), ['defaultView']] = "'true"
    
    
# #Reorder dropdown menus
# povline_dropdown_list = ['$1 per day',
#                          '$1.90 per day: International Poverty Line',
#                          '$2.15 per day: International Poverty Line',
#                          '$3.20 per day: Lower-middle income poverty line',
#                          '$3.65 per day: Lower-middle income poverty line',
#                          '$5.50 per day: Upper-middle income poverty line',
#                          '$6.85 per day: Upper-middle income poverty line',
#                          '$10 per day',
#                          '$20 per day',
#                          '$30 per day',
#                          '$40 per day',
#                          'International Poverty Line',
#                          'Lower-middle income poverty line',
#                          'Upper-middle income poverty line',
#                          'Relative poverty: 40% of median',
#                          'Relative poverty: 50% of median',
#                          'Relative poverty: 60% of median']


# df_graphers_mapping = pd.DataFrame({'povline_dropdown': povline_dropdown_list,})
# df_graphers_mapping = df_graphers_mapping.reset_index().set_index('povline_dropdown')

# df_graphers['povline_dropdown_aux'] = df_graphers['Poverty line Dropdown'].map(df_graphers_mapping['index'])
# df_graphers = df_graphers.sort_values('povline_dropdown_aux', ignore_index=True)
# df_graphers = df_graphers.drop(columns=['povline_dropdown_aux'])

#Export Grapher table    
df_graphers.to_csv(f'data/ppp_2017/final/OWID_internal_upload/explorer_database/complete_poverty/graphers.csv', index=False)
# -


