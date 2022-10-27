import pandas as pd
import numpy as np

# +
#Read Google sheets
sheet_id = '1Oit-4xH6pg5fVKe5gfgd4H7CKRpAe7dQhrmkBc4IpkU'

sheet_name = 'ratios'
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
ratios = pd.read_csv(url)

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
    
    #Gini coefficient
    df_tables.loc[j, 'name'] = f'Gini coefficient'
    df_tables.loc[j, 'slug'] = f'gini'
    df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
    df_tables.loc[j, 'description'] = f'The Gini coefficient measures inequality on a scale between 0 and 1, where higher values indicate greater inequality.'
    df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
    df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
    df_tables.loc[j, 'unit'] = np.nan
    df_tables.loc[j, 'shortUnit'] = np.nan
    df_tables.loc[j, 'tolerance'] = 5
    df_tables.loc[j, 'type'] = "Numeric"
    df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
    df_tables.loc[j, 'colorScaleNumericBins'] = "0.2;0.25;0.3;0.35;0.4;0.45;0.5;0.55;0.6;0.65;0.7"
    df_tables.loc[j, 'colorScaleEqualSizeBins'] = "'true"
    df_tables.loc[j, 'colorScaleScheme'] = "Reds"
    df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
    j += 1
    
    #Share of the top 10%
    df_tables.loc[j, 'name'] = f'Share of the richest decile in total {survey_type.text[survey]}'
    df_tables.loc[j, 'slug'] = f'decile10_share'
    df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
    df_tables.loc[j, 'description'] = f'The {survey_type.text[survey]} of the richest decile (tenth of the population) as a share of total {survey_type.text[survey]}.'
    df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
    df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
    df_tables.loc[j, 'unit'] = "%"
    df_tables.loc[j, 'shortUnit'] = "%"
    df_tables.loc[j, 'tolerance'] = 5
    df_tables.loc[j, 'type'] = "Numeric"
    df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
    df_tables.loc[j, 'colorScaleNumericBins'] = "0;5;10;15;20;25;30;35;40;45;50"
    df_tables.loc[j, 'colorScaleEqualSizeBins'] = "'true"
    df_tables.loc[j, 'colorScaleScheme'] = "Greens"
    df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
    j += 1
    
    #P90/P10
    df_tables.loc[j, 'name'] = f'P90/P10 ratio'
    df_tables.loc[j, 'slug'] = f'p90_p10_ratio'
    df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
    df_tables.loc[j, 'description'] = f'P90 is the the level of {survey_type.text[survey]} below which 90% of the population lives. P10 is the level of {survey_type.text[survey]} below which 10% of the population lives. This variable gives the ratio of the two. It is a measure of inequality that indicates the gap between the richest and poorest tenth of the population. It tells you how many times richer someone just in the the poorest tenth would need to be in order to be counted in the richest tenth.'
    df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
    df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP), adapted by Our World in Data."
    df_tables.loc[j, 'unit'] = np.nan
    df_tables.loc[j, 'shortUnit'] = np.nan
    df_tables.loc[j, 'tolerance'] = 5
    df_tables.loc[j, 'type'] = "Numeric"
    df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
    df_tables.loc[j, 'colorScaleNumericBins'] = "0;2;4;6;8;10;12;14;16;18"
    df_tables.loc[j, 'colorScaleEqualSizeBins'] = "'true"
    df_tables.loc[j, 'colorScaleScheme'] = "OrRd"
    df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
    j += 1
    
    #P90/P50
    df_tables.loc[j, 'name'] = f'P90/P50 ratio'
    df_tables.loc[j, 'slug'] = f'p90_p50_ratio'
    df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
    df_tables.loc[j, 'description'] = f'P90 is the the level of {survey_type.text[survey]} above which 10% of the population lives. P50 is the median – the level of {survey_type.text[survey]} below which 50% of the population lives. This variable gives the ratio of the two. It is a measure of inequality within the top half of the distribution. It tells you how many times richer someone in the middle of the distribution would need to be in order to be counted in the richest tenth.'
    df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
    df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP), adapted by Our World in Data."
    df_tables.loc[j, 'unit'] = np.nan
    df_tables.loc[j, 'shortUnit'] = np.nan
    df_tables.loc[j, 'tolerance'] = 5
    df_tables.loc[j, 'type'] = "Numeric"
    df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
    df_tables.loc[j, 'colorScaleNumericBins'] = "0;2;4;6;8;10;12;14;16;18"
    df_tables.loc[j, 'colorScaleEqualSizeBins'] = "'true"
    df_tables.loc[j, 'colorScaleScheme'] = "Purples"
    df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
    j += 1
    
    #P50/P10
    df_tables.loc[j, 'name'] = f'P50/P10 ratio'
    df_tables.loc[j, 'slug'] = f'p50_p10_ratio'
    df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
    df_tables.loc[j, 'description'] = f'P50 is the median – the level of {survey_type.text[survey]} below which 50% of the population lives. P10 is the the level of {survey_type.text[survey]} below which 10% of the population lives. This variable gives the ratio of the two. It is a measure of inequality within the bottom half of the distribution. It tells you how many times richer someone just in the the poorest tenth would need to be in order to be reach the median.'
    df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
    df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP), adapted by Our World in Data."
    df_tables.loc[j, 'unit'] = np.nan
    df_tables.loc[j, 'shortUnit'] = np.nan
    df_tables.loc[j, 'tolerance'] = 5
    df_tables.loc[j, 'type'] = "Numeric"
    df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
    df_tables.loc[j, 'colorScaleNumericBins'] = "0;2;4;6;8;10;12;14;16;18"
    df_tables.loc[j, 'colorScaleEqualSizeBins'] = "'true"
    df_tables.loc[j, 'colorScaleScheme'] = "YlOrRd"
    df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
    j += 1
    
    #Palma ratio
    df_tables.loc[j, 'name'] = f'Palma ratio'
    df_tables.loc[j, 'slug'] = f'palma_ratio'
    df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
    df_tables.loc[j, 'description'] = f'The Palma ratio is a measure of inequality: it is the share of total {survey_type.text[survey]} of the top 10% divided by the share of the bottom 40%.'
    df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
    df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP), adapted by Our World in Data."
    df_tables.loc[j, 'unit'] = np.nan
    df_tables.loc[j, 'shortUnit'] = np.nan
    df_tables.loc[j, 'tolerance'] = 5
    df_tables.loc[j, 'type'] = "Numeric"
    df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
    df_tables.loc[j, 'colorScaleNumericBins'] = "0;2;4;6;8;10;12;14;16;18"
    df_tables.loc[j, 'colorScaleEqualSizeBins'] = "'true"
    df_tables.loc[j, 'colorScaleScheme'] = "Oranges"
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
        
    #MLD
    df_tables.loc[j, 'name'] = f'Mean Log Deviation'
    df_tables.loc[j, 'slug'] = f'mld'
    df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
    df_tables.loc[j, 'description'] = f"The mean log deviation (MLD) is a measure of inequality. An MLD of zero indicates perfect equality and it takes on larger positive values as incomes become more unequal. The measure is also referred to as 'Theil L' or 'GE(0)', in reference to the wider families of inequality measures to which the MLD belongs."
    df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
    df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
    df_tables.loc[j, 'unit'] = np.nan
    df_tables.loc[j, 'shortUnit'] = np.nan
    df_tables.loc[j, 'tolerance'] = 5
    df_tables.loc[j, 'type'] = "Numeric"
    df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
    df_tables.loc[j, 'colorScaleNumericBins'] = "0;2;4;6;8;10;12;14;16;18"
    df_tables.loc[j, 'colorScaleEqualSizeBins'] = "'true"
    df_tables.loc[j, 'colorScaleScheme'] = "RdPu"
    df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
    j += 1
    
    #Polarization
    df_tables.loc[j, 'name'] = f'Polarization index'
    df_tables.loc[j, 'slug'] = f'polarization'
    df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
    df_tables.loc[j, 'description'] = f"The polarization index, also known as the Wolfson polarization index, measures the extent to which the distribution of {survey_type.text[survey]} is “spread out” and bi-modal. Like the Gini coefficient, the polarization index ranges from 0 (no polarization) to 1 (complete polarization). The polarization index is based on Wolfson (1994) and Ravallion and Chen (1997). See Wolfson, Michael C. 1994. “When Inequalities Diverge.” The American Economic Review 84 (2): 353–58. https://www.jstor.org/stable/2117858 and Ravallion, Martin, and Shaohua Chen. 1997. “What Can New Survey Data Tell Us about Recent Changes in Distribution and Poverty?” The World Bank Economic Review 11 (2): 357–82. https://www.jstor.org/stable/3990232."
    df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
    df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
    df_tables.loc[j, 'unit'] = np.nan
    df_tables.loc[j, 'shortUnit'] = np.nan
    df_tables.loc[j, 'tolerance'] = 5
    df_tables.loc[j, 'type'] = "Numeric"
    df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
    df_tables.loc[j, 'colorScaleNumericBins'] = "0;2;4;6;8;10;12;14;16;18"
    df_tables.loc[j, 'colorScaleEqualSizeBins'] = "'true"
    df_tables.loc[j, 'colorScaleScheme'] = "Reds"
    df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
    j += 1
      
#Separate the tables into inc, cons and inc or cons
survey_list = list(survey_type['table_name'])
for i in survey_list:
    table_export = df_tables[df_tables['survey_type'] == i].copy().reset_index(drop=True)
    table_export = table_export.drop(columns=['survey_type'])
    table_export.to_csv(f'data/ppp_2017/final/OWID_internal_upload/explorer_database/inequality/table_{i}.csv', index=False)
# -

# ### Grapher views
# Similar to the tables, this creates the grapher views by grouping by types of variables and then running by survey type and poverty lines.

# +
#Grapher table generation

df_graphers = pd.DataFrame()

j=0

for survey in range(len(survey_type)):
    
    #Gini coefficient    
    df_graphers.loc[j, 'title'] = f'Income inequality: Gini coefficient'
    df_graphers.loc[j, 'ySlugs'] = f'gini'
    df_graphers.loc[j, 'Metric Dropdown'] = "Gini coefficient"
    df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
    df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
    df_graphers.loc[j, 'subtitle'] = f'The Gini coefficient is a measure of the inequality of the income distribution in a population. Higher values indicate a higher level of inequality.'
    df_graphers.loc[j, 'note'] = f"This data relates to disposable {survey_type.text[survey]} per capita (exact definitions vary)."
    df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
    df_graphers.loc[j, 'type'] = np.nan
    df_graphers.loc[j, 'yAxisMin'] = 0
    df_graphers.loc[j, 'facet'] = np.nan
    df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
    df_graphers.loc[j, 'hasMapTab'] = "'true"
    df_graphers.loc[j, 'tab'] = "map"
    df_graphers.loc[j, 'mapTargetTime'] = 2019
    j += 1
    
    #Share of the top 10%  
    df_graphers.loc[j, 'title'] = f'{survey_type.text[survey].capitalize()} share of the top 10%'
    df_graphers.loc[j, 'ySlugs'] = f'decile10_share'
    df_graphers.loc[j, 'Metric Dropdown'] = "Top 10% share"
    df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
    df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
    df_graphers.loc[j, 'subtitle'] = f'This is the {survey_type.text[survey]} of the richest decile (tenth of the population) as a share of total {survey_type.text[survey]}.'
    df_graphers.loc[j, 'note'] = f"This data relates to disposable {survey_type.text[survey]} per capita (exact definitions vary)."
    df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
    df_graphers.loc[j, 'type'] = np.nan
    df_graphers.loc[j, 'yAxisMin'] = 0
    df_graphers.loc[j, 'facet'] = np.nan
    df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
    df_graphers.loc[j, 'hasMapTab'] = "'true"
    df_graphers.loc[j, 'tab'] = "map"
    df_graphers.loc[j, 'mapTargetTime'] = 2019
    j += 1
    
    #P90/P10 
    df_graphers.loc[j, 'title'] = f'Income inequality: P90/P10 ratio'
    df_graphers.loc[j, 'ySlugs'] = f'p90_p10_ratio'
    df_graphers.loc[j, 'Metric Dropdown'] = "P90/P10"
    df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
    df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
    df_graphers.loc[j, 'subtitle'] = f'P90 is the the level of {survey_type.text[survey]} below which 90% of the population lives. P10 is the level of {survey_type.text[survey]} below which 10% of the population lives. This variable gives the ratio of the two. It is a measure of inequality that indicates the gap between the richest and poorest tenth of the population.'
    df_graphers.loc[j, 'note'] = f"This data relates to disposable {survey_type.text[survey]} per capita (exact definitions vary)."
    df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
    df_graphers.loc[j, 'type'] = np.nan
    df_graphers.loc[j, 'yAxisMin'] = 0
    df_graphers.loc[j, 'facet'] = np.nan
    df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
    df_graphers.loc[j, 'hasMapTab'] = "'true"
    df_graphers.loc[j, 'tab'] = "map"
    df_graphers.loc[j, 'mapTargetTime'] = 2019
    j += 1
    
    #P90/P50 
    df_graphers.loc[j, 'title'] = f'Income inequality: P90/P50 ratio'
    df_graphers.loc[j, 'ySlugs'] = f'p90_p50_ratio'
    df_graphers.loc[j, 'Metric Dropdown'] = "P90/P50"
    df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
    df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
    df_graphers.loc[j, 'subtitle'] = f'P90 is the the level of {survey_type.text[survey]} above which 10% of the population lives. P50 is the median – the level of {survey_type.text[survey]} below which 50% of the population lives. This variable gives the ratio of the two. It is a measure of inequality within the top half of the distribution.'
    df_graphers.loc[j, 'note'] = f"This data relates to disposable {survey_type.text[survey]} per capita (exact definitions vary)."
    df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
    df_graphers.loc[j, 'type'] = np.nan
    df_graphers.loc[j, 'yAxisMin'] = 0
    df_graphers.loc[j, 'facet'] = np.nan
    df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
    df_graphers.loc[j, 'hasMapTab'] = "'true"
    df_graphers.loc[j, 'tab'] = "map"
    df_graphers.loc[j, 'mapTargetTime'] = 2019
    j += 1
    
    #P50/P10 
    df_graphers.loc[j, 'title'] = f'Income inequality: P50/P10 ratio'
    df_graphers.loc[j, 'ySlugs'] = f'p50_p10_ratio'
    df_graphers.loc[j, 'Metric Dropdown'] = "P90/P50"
    df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
    df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
    df_graphers.loc[j, 'subtitle'] = f'P50 is the median – the level of {survey_type.text[survey]} below which 50% of the population lives. P10 is the the level of {survey_type.text[survey]} below which 10% of the population lives. This variable gives the ratio of the two. It is a measure of inequality within the bottom half of the distribution.'
    df_graphers.loc[j, 'note'] = f"This data relates to disposable {survey_type.text[survey]} per capita (exact definitions vary)."
    df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
    df_graphers.loc[j, 'type'] = np.nan
    df_graphers.loc[j, 'yAxisMin'] = 0
    df_graphers.loc[j, 'facet'] = np.nan
    df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
    df_graphers.loc[j, 'hasMapTab'] = "'true"
    df_graphers.loc[j, 'tab'] = "map"
    df_graphers.loc[j, 'mapTargetTime'] = 2019
    j += 1
    
    #Palma ratio
    df_graphers.loc[j, 'title'] = f'Income inequality: Palma ratio'
    df_graphers.loc[j, 'ySlugs'] = f'palma_ratio'
    df_graphers.loc[j, 'Metric Dropdown'] = "Palma ratio"
    df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
    df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
    df_graphers.loc[j, 'subtitle'] = f'The Palma ratio is a measure of inequality: it is the share of total {survey_type.text[survey]} of the top 10% divided by the share of the bottom 40%.'
    df_graphers.loc[j, 'note'] = f"This data relates to disposable {survey_type.text[survey]} per capita (exact definitions vary)."
    df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
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
        df_graphers.loc[j, 'Metric Dropdown'] = f"Share in poverty (< {povlines_rel.text[pct]})"
        df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df_graphers.loc[j, 'subtitle'] = f'Relative poverty is measured in terms of a poverty line that rises and falls over time with average incomes – in this case set at {povlines_rel.text[pct]} {survey_type.text[survey]}.'
        df_graphers.loc[j, 'note'] = "This data is adjusted for inflation and for differences in the cost of living between countries. It is expressed in international-$ at 2017 prices."
        df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df_graphers.loc[j, 'type'] = np.nan
        df_graphers.loc[j, 'yAxisMin'] = 0
        df_graphers.loc[j, 'facet'] = np.nan
        df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
        df_graphers.loc[j, 'hasMapTab'] = "'true"
        df_graphers.loc[j, 'tab'] = "map"
        df_graphers.loc[j, 'mapTargetTime'] = 2019
        j += 1
        
    #MLD
    df_graphers.loc[j, 'title'] = f'Income inequality: Mean log deviation'
    df_graphers.loc[j, 'ySlugs'] = f'mld'
    df_graphers.loc[j, 'Metric Dropdown'] = "Mean log deviation"
    df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
    df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
    df_graphers.loc[j, 'subtitle'] = f"The mean log deviation (MLD) is a measure of inequality. An MLD of zero indicates perfect equality and it takes on larger positive values as incomes become more unequal."
    df_graphers.loc[j, 'note'] = f"This data relates to disposable {survey_type.text[survey]} per capita (exact definitions vary)."
    df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
    df_graphers.loc[j, 'type'] = np.nan
    df_graphers.loc[j, 'yAxisMin'] = 0
    df_graphers.loc[j, 'facet'] = np.nan
    df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
    df_graphers.loc[j, 'hasMapTab'] = "'true"
    df_graphers.loc[j, 'tab'] = "map"
    df_graphers.loc[j, 'mapTargetTime'] = 2019
    j += 1
    
    #Polarization
    df_graphers.loc[j, 'title'] = f'Income inequality: Polarization index'
    df_graphers.loc[j, 'ySlugs'] = f'polarization'
    df_graphers.loc[j, 'Metric Dropdown'] = "Polarization index"
    df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
    df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
    df_graphers.loc[j, 'subtitle'] = f"The polarization index, also known as the Wolfson polarization index, measures the extent to which the distribution of {survey_type.text[survey]} is “spread out” and bi-modal. Like the Gini coefficient, the polarization index ranges from 0 (no polarization) to 1 (complete polarization)."
    df_graphers.loc[j, 'note'] = f"This data relates to disposable {survey_type.text[survey]} per capita (exact definitions vary)."
    df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
    df_graphers.loc[j, 'type'] = np.nan
    df_graphers.loc[j, 'yAxisMin'] = 0
    df_graphers.loc[j, 'facet'] = np.nan
    df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
    df_graphers.loc[j, 'hasMapTab'] = "'true"
    df_graphers.loc[j, 'tab'] = "map"
    df_graphers.loc[j, 'mapTargetTime'] = 2019
    j += 1
    
#Select one default view
df_graphers.loc[(df_graphers['ySlugs'] == "gini") 
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
df_graphers.to_csv(f'data/ppp_2017/final/OWID_internal_upload/explorer_database/inequality/graphers.csv', index=False)
# -


