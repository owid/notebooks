import pandas as pd
import numpy as np

# +
#Read Google sheets
sheet_id = '13Fv0aWgG8_3eB2TdGtIGS4cECUjdzIOQTpcMJ3XdtI8'

sheet_name = 'deciles10'
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
deciles10 = pd.read_csv(url, dtype={'dropdown':'str', 'decile':'str'})

sheet_name = 'deciles9'
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
deciles9 = pd.read_csv(url, dtype={'dropdown':'str', 'decile':'str'})

sheet_name = 'income_aggregation'
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
income_aggregation = pd.read_csv(url, dtype={'multiplier':'str'})

sheet_name = 'survey_type'
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
survey_type = pd.read_csv(url)
# -

# ## Long method
# ### Tables with variable definitions
# Variables are grouped by type to iterate by different poverty lines and survey types at the same time. The output is the list of all the variables being used in the explorer, separated by survey type in csv files.

# +
#Table generation
df = pd.DataFrame()
j=0

for survey in range(len(survey_type)):
    for agg in range(len(income_aggregation)):
        
        #mean
        df.loc[j, 'name'] = f"Mean {survey_type.text[survey]} per {income_aggregation.aggregation[agg]}"
        df.loc[j, 'slug'] = f"mean{income_aggregation.slug_suffix[agg]}"
        df.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df.loc[j, 'description'] = f"The mean level of {survey_type.text[survey]} per {income_aggregation.aggregation[agg]}."
        df.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
        df.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
        df.loc[j, 'unit'] = "international-$ at 2017 prices"
        df.loc[j, 'shortUnit'] = "$"
        df.loc[j, 'tolerance'] = 5
        df.loc[j, 'type'] = "Numeric"
        df.loc[j, 'colorScaleNumericMinValue'] = 0
        df.loc[j, 'colorScaleNumericBins'] = income_aggregation.scale[agg]
        df.loc[j, 'colorScaleEqualSizeBins'] = "'true"
        df.loc[j, 'colorScaleScheme'] = "BuGn"
        df.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        df.loc[j, 'transform'] = f'multiplyBy mean {income_aggregation.multiplier[agg]}'
        j += 1

        #median
        df.loc[j, 'name'] = f"Median {survey_type.text[survey]} per {income_aggregation.aggregation[agg]}"
        df.loc[j, 'slug'] = f"median{income_aggregation.slug_suffix[agg]}"
        df.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df.loc[j, 'description'] = f"The level of {survey_type.text[survey]} per {income_aggregation.aggregation[agg]} below which half of the population live."
        df.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
        df.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
        df.loc[j, 'unit'] = "international-$ at 2017 prices"
        df.loc[j, 'shortUnit'] = "$"
        df.loc[j, 'tolerance'] = 5
        df.loc[j, 'type'] = "Numeric"
        df.loc[j, 'colorScaleNumericMinValue'] = 0
        df.loc[j, 'colorScaleNumericBins'] = income_aggregation.scale[agg]
        df.loc[j, 'colorScaleEqualSizeBins'] = "'true"
        df.loc[j, 'colorScaleScheme'] = "BuGn"
        df.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        df.loc[j, 'transform'] = f'multiplyBy median {income_aggregation.multiplier[agg]}'
        j += 1

        for dec9 in range(len(deciles9)):
            
            #thresholds
            df.loc[j, 'name'] = deciles9.ordinal[dec9]
            df.loc[j, 'slug'] = f"decile{deciles9.ordinal[dec9]}_thr{income_aggregation.slug_suffix[agg]}"
            df.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
            df.loc[j, 'description'] = f"The level of {survey_type.text[survey]} per {income_aggregation.aggregation[agg]} below which {income_aggregation.slug_suffix[agg]}0% of the population falls."
            df.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
            df.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
            df.loc[j, 'unit'] = "international-$ at 2017 prices"
            df.loc[j, 'shortUnit'] = "$"
            df.loc[j, 'tolerance'] = 5
            df.loc[j, 'type'] = "Numeric"
            df.loc[j, 'colorScaleNumericMinValue'] = 0
            df.loc[j, 'colorScaleNumericBins'] = income_aggregation.scale[agg]
            df.loc[j, 'colorScaleEqualSizeBins'] = "'true"
            df.loc[j, 'colorScaleScheme'] = "Greens"
            df.loc[j, 'survey_type'] = survey_type['table_name'][survey]
            df.loc[j, 'transform'] = f'multiplyBy decile{deciles9.ordinal[dec9]}_thr {income_aggregation.multiplier[agg]}'
            j += 1
            
        for dec10 in range(len(deciles10)):

            #averages
            df.loc[j, 'name'] = deciles10.ordinal[dec10]
            df.loc[j, 'slug'] = f"decile{deciles10.ordinal[dec10]}_avg{income_aggregation.slug_suffix[agg]}"
            df.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
            df.loc[j, 'description'] = f"The mean {survey_type.text[survey]} per {income_aggregation.aggregation[agg]} within the {deciles10.ordinal[dec10]} (tenth of the population)."
            df.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
            df.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
            df.loc[j, 'unit'] = "international-$ at 2017 prices"
            df.loc[j, 'shortUnit'] = "$"
            df.loc[j, 'tolerance'] = 5
            df.loc[j, 'type'] = "Numeric"
            df.loc[j, 'colorScaleNumericMinValue'] = 0
            df.loc[j, 'colorScaleNumericBins'] = income_aggregation.scale[agg]
            df.loc[j, 'colorScaleEqualSizeBins'] = "'true"
            df.loc[j, 'colorScaleScheme'] = "Greens"
            df.loc[j, 'survey_type'] = survey_type['table_name'][survey]
            df.loc[j, 'transform'] = f'multiplyBy decile{deciles10.ordinal[dec10]}_avg {income_aggregation.multiplier[agg]}'
            j += 1
            
    for dec10 in range(len(deciles10)):
    
        #shares
        df.loc[j, 'name'] = deciles10.ordinal[dec10]
        df.loc[j, 'slug'] = f"decile{deciles10.ordinal[dec10]}_share"
        df.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df.loc[j, 'description'] = f"The {survey_type.text[survey]} of the {deciles10.ordinal[dec10]} (tenth of the population) as a share of total {survey_type.text[survey]}."
        df.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
        df.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
        df.loc[j, 'unit'] = "international-$ at 2017 prices"
        df.loc[j, 'shortUnit'] = "$"
        df.loc[j, 'tolerance'] = 5
        df.loc[j, 'type'] = "Numeric"
        df.loc[j, 'colorScaleNumericMinValue'] = 0
        df.loc[j, 'colorScaleNumericBins'] = income_aggregation.scale[agg]
        df.loc[j, 'colorScaleEqualSizeBins'] = "'true"
        df.loc[j, 'colorScaleScheme'] = "Greens"
        df.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1
      
#Separate the tables into inc, cons and inc or cons
survey_list = list(survey_type['table_name'])
for i in survey_list:
    table_export = df[df['survey_type'] == i].copy().reset_index(drop=True)
    table_export = table_export.drop(columns=['survey_type'])
    table_export.to_csv(f'data/ppp_2017/final/OWID_internal_upload/explorer_database/across_distribution/table_{i}.csv', index=False)
# -

# ### Grapher views
# Similar to the tables, this creates the grapher views by grouping by types of variables and then running by survey type and poverty lines.

# +
#Grapher table generation

df = pd.DataFrame()

j=0

for survey in range(len(survey_type)):
    for agg in range(len(income_aggregation)):
        
        #mean
        df.loc[j, 'title'] = f"Mean {survey_type.text[survey]} per {income_aggregation.aggregation[agg]}"
        df.loc[j, 'ySlugs'] = f"mean{income_aggregation.slug_suffix[agg]}"
        df.loc[j, 'Metric Dropdown'] = "Mean income or expenditure"
        df.loc[j, 'Decile Dropdown'] = np.nan
        df.loc[j, 'Aggregation Radio'] = f'{income_aggregation.aggregation[agg].title()}'
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
        df.loc[j, 'yScaleToggle'] = "'true"
        j += 1

        #median
        df.loc[j, 'title'] = f"Median {survey_type.text[survey]} per {income_aggregation.aggregation[agg]}"
        df.loc[j, 'ySlugs'] = f"median{income_aggregation.slug_suffix[agg]}"
        df.loc[j, 'Metric Dropdown'] = "Median income or expenditure"
        df.loc[j, 'Decile Dropdown'] = np.nan
        df.loc[j, 'Aggregation Radio'] = f'{income_aggregation.aggregation[agg].title()}'
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
        df.loc[j, 'yScaleToggle'] = "'true"
        j += 1

        for dec9 in range(len(deciles9)):

            #thresholds
            df.loc[j, 'title'] = f"Threshold {survey_type.text[survey]} per {income_aggregation.aggregation[agg]} marking the {deciles9.ordinal[dec9]}"
            df.loc[j, 'ySlugs'] = f"decile{deciles9.ordinal[dec9]}_thr{income_aggregation.slug_suffix[agg]}"
            df.loc[j, 'Metric Dropdown'] = "Decile threshold"
            df.loc[j, 'Decile Dropdown'] = f'{deciles9.dropdown[dec9]}'
            df.loc[j, 'Aggregation Radio'] = f'{income_aggregation.aggregation[agg].title()}'
            df.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
            df.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
            df.loc[j, 'subtitle'] = f"This is the level of {survey_type.text[survey]} per {income_aggregation.aggregation[agg]} below which {income_aggregation.slug_suffix[agg]}0% of the population falls."
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
            df.loc[j, 'yScaleToggle'] = "'true"
            j += 1

        for dec10 in range(len(deciles10)):

            #averages
            df.loc[j, 'title'] = f"Mean {survey_type.text[survey]} per {income_aggregation.aggregation[agg]} within the {deciles10.ordinal[dec10]}"
            df.loc[j, 'ySlugs'] = f"decile{deciles10.ordinal[dec10]}_thr{income_aggregation.slug_suffix[agg]}"
            df.loc[j, 'Metric Dropdown'] = "Mean within decile"
            df.loc[j, 'Decile Dropdown'] = f'{deciles10.dropdown[dec10]}'
            df.loc[j, 'Aggregation Radio'] = f'{income_aggregation.aggregation[agg].title()}'
            df.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
            df.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
            df.loc[j, 'subtitle'] = f"This is the mean {survey_type.text[survey]} per {income_aggregation.aggregation[agg]} within the {deciles10.ordinal[dec10]} (tenth of the population)."
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
            df.loc[j, 'yScaleToggle'] = "'true"
            j += 1
            
    for dec10 in range(len(deciles10)):

        #shares
        df.loc[j, 'title'] = f"Share of the {deciles10.ordinal[dec10]} in total {survey_type.text[survey]}"
        df.loc[j, 'ySlugs'] = f"decile{deciles10.ordinal[dec10]}_thr"
        df.loc[j, 'Metric Dropdown'] = "Decile shares"
        df.loc[j, 'Decile Dropdown'] = f'{deciles10.dropdown[dec10]}'
        df.loc[j, 'Aggregation Radio'] = f'{income_aggregation.aggregation[agg].title()}'
        df.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df.loc[j, 'subtitle'] = f"This is the {survey_type.text[survey]} of the {deciles10.ordinal[dec10]} (tenth of the population) as a share of total {survey_type.text[survey]}."
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
        df.loc[j, 'yScaleToggle'] = "'true"
        j += 1
    
# #Select one default view
# df.loc[(df['ySlugs'] == "headcount_ratio_190_ppp2011 headcount_ratio_215_ppp2017") 
#        & (df['tableSlug'] == "inc_or_cons"), ['defaultView']] = "'true"
    
    
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


# df_mapping = pd.DataFrame({'povline_dropdown': povline_dropdown_list,})
# df_mapping = df_mapping.reset_index().set_index('povline_dropdown')

# df['povline_dropdown_aux'] = df['Poverty line Dropdown'].map(df_mapping['index'])
# df = df.sort_values('povline_dropdown_aux', ignore_index=True)
# df = df.drop(columns=['povline_dropdown_aux'])

#Export Grapher table    
df.to_csv(f'data/ppp_2017/final/OWID_internal_upload/explorer_database/across_distribution/grapher.csv', index=False)
