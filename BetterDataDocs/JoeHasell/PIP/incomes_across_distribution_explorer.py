# %% [markdown]
# # Incomes across the distribution explorer
# This code creates the tsv file for the incomes across the distribution explorer from the World Bank PIP data, available [here](https://owid.cloud/admin/explorers/preview/incomes-across-distribution-ppp2017)

# %%
import pandas as pd
import numpy as np
import textwrap

# %% [markdown]
# ## Google sheets auxiliar data
# These spreadsheets provide with different details depending on each poverty line or survey type.

# %%
#Read Google sheets
sheet_id = '13Fv0aWgG8_3eB2TdGtIGS4cECUjdzIOQTpcMJ3XdtI8'

#Settings for 10 deciles variables (share, avg) sheet
sheet_name = 'deciles10'
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
deciles10 = pd.read_csv(url, dtype={'dropdown':'str', 'decile':'str'})

#Settings for 9 deciles variables (thr) sheet
sheet_name = 'deciles9'
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
deciles9 = pd.read_csv(url, dtype={'dropdown':'str', 'decile':'str'})

#Income aggregation sheet (day, month, year)
sheet_name = 'income_aggregation'
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
income_aggregation = pd.read_csv(url, keep_default_na=False, dtype={'multiplier':'str'})

#Survey type sheet
sheet_name = 'survey_type'
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
survey_type = pd.read_csv(url)
# %% [markdown]
# ## Header
# General settings of the explorer are defined here, like the title, subtitle, default country selection, publishing status and others.

# %%
#The header is defined as a dictionary first and then it is converted into a index-oriented dataframe
header_dict = {'explorerTitle': 'Incomes across the distribution (World Bank PIP)',
               'selection': ['Mozambique', 'Nigeria', 'Kenya', 'Bangladesh', 'Bolivia', 'World'],
               'explorerSubtitle': '<i><a href="https://github.com/owid/poverty-data">Download Poverty data on GitHub</a></i>',
               'isPublished': 'false',
               'googleSheet': 'https://docs.google.com/spreadsheets/d/13Fv0aWgG8_3eB2TdGtIGS4cECUjdzIOQTpcMJ3XdtI8',
               'wpBlockId': '52633',
               'entityType': 'country or region'}

#Index-oriented dataframe
df_header = pd.DataFrame.from_dict(header_dict, orient='index', columns=None)
#Assigns a cell for each entity separated by comma (like in `selection`)
df_header = df_header[0].apply(pd.Series)

# %% [markdown]
# ## Tables
# Variables are grouped by type to iterate by different poverty lines and survey types at the same time. The output is the list of all the variables being used in the explorer, with metadata.
# ### Tables for variables not showing breaks between surveys
# These variables consider a continous series, without breaks due to changes in surveys' methodology

# %%
#Table generation
df_tables = pd.DataFrame()
j=0

for survey in range(len(survey_type)):
    for agg in range(len(income_aggregation)):

        #mean
        df_tables.loc[j, 'name'] = f"Mean {survey_type.text[survey]} per {income_aggregation.aggregation[agg]}"
        df_tables.loc[j, 'slug'] = f"mean{income_aggregation.slug_suffix[agg]}"
        df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df_tables.loc[j, 'description'] = f"The mean level of {survey_type.text[survey]} per {income_aggregation.aggregation[agg]}."
        df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
        df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
        df_tables.loc[j, 'unit'] = "international-$ at 2017 prices"
        df_tables.loc[j, 'shortUnit'] = "$"
        df_tables.loc[j, 'tolerance'] = 5
        df_tables.loc[j, 'type'] = "Numeric"
        df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
        df_tables.loc[j, 'colorScaleNumericBins'] = income_aggregation.scale[agg]
        df_tables.loc[j, 'colorScaleEqualSizeBins'] = "true"
        df_tables.loc[j, 'colorScaleScheme'] = "BuGn"
        df_tables.loc[j, 'transform'] = f'multiplyBy mean {income_aggregation.multiplier[agg]}'
        df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1

        #median
        df_tables.loc[j, 'name'] = f"Median {survey_type.text[survey]} per {income_aggregation.aggregation[agg]}"
        df_tables.loc[j, 'slug'] = f"median{income_aggregation.slug_suffix[agg]}"
        df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df_tables.loc[j, 'description'] = f"The level of {survey_type.text[survey]} per {income_aggregation.aggregation[agg]} below which half of the population live."
        df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
        df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
        df_tables.loc[j, 'unit'] = "international-$ at 2017 prices"
        df_tables.loc[j, 'shortUnit'] = "$"
        df_tables.loc[j, 'tolerance'] = 5
        df_tables.loc[j, 'type'] = "Numeric"
        df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
        df_tables.loc[j, 'colorScaleNumericBins'] = income_aggregation.scale[agg]
        df_tables.loc[j, 'colorScaleEqualSizeBins'] = "true"
        df_tables.loc[j, 'colorScaleScheme'] = "Blues"
        df_tables.loc[j, 'transform'] = f'multiplyBy median {income_aggregation.multiplier[agg]}'
        df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1

        for dec9 in range(len(deciles9)):

            #thresholds
            df_tables.loc[j, 'name'] = deciles9.ordinal[dec9]
            df_tables.loc[j, 'slug'] = f"decile{deciles9.decile[dec9]}_thr{income_aggregation.slug_suffix[agg]}"
            df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
            df_tables.loc[j, 'description'] = f"The level of {survey_type.text[survey]} per {income_aggregation.aggregation[agg]} below which {deciles9.decile[dec9]}0% of the population falls."
            df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
            df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
            df_tables.loc[j, 'unit'] = "international-$ at 2017 prices"
            df_tables.loc[j, 'shortUnit'] = "$"
            df_tables.loc[j, 'tolerance'] = 5
            df_tables.loc[j, 'type'] = "Numeric"
            df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
            df_tables.loc[j, 'colorScaleNumericBins'] = income_aggregation.scale[agg]
            df_tables.loc[j, 'colorScaleEqualSizeBins'] = "true"
            df_tables.loc[j, 'colorScaleScheme'] = "Purples"
            df_tables.loc[j, 'transform'] = f'multiplyBy decile{deciles9.decile[dec9]}_thr {income_aggregation.multiplier[agg]}'
            df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
            j += 1

        for dec10 in range(len(deciles10)):

            #averages
            df_tables.loc[j, 'name'] = deciles10.ordinal[dec10]
            df_tables.loc[j, 'slug'] = f"decile{deciles10.decile[dec10]}_avg{income_aggregation.slug_suffix[agg]}"
            df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
            df_tables.loc[j, 'description'] = f"The mean {survey_type.text[survey]} per {income_aggregation.aggregation[agg]} within the {deciles10.ordinal[dec10]} (tenth of the population)."
            df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
            df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
            df_tables.loc[j, 'unit'] = "international-$ at 2017 prices"
            df_tables.loc[j, 'shortUnit'] = "$"
            df_tables.loc[j, 'tolerance'] = 5
            df_tables.loc[j, 'type'] = "Numeric"
            df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
            df_tables.loc[j, 'colorScaleNumericBins'] = income_aggregation.scale[agg]
            df_tables.loc[j, 'colorScaleEqualSizeBins'] = "true"
            df_tables.loc[j, 'colorScaleScheme'] = "Greens"
            df_tables.loc[j, 'transform'] = f'multiplyBy decile{deciles10.decile[dec10]}_avg {income_aggregation.multiplier[agg]}'
            df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
            j += 1

    for dec10 in range(len(deciles10)):

        #shares
        df_tables.loc[j, 'name'] = deciles10.ordinal[dec10]
        df_tables.loc[j, 'slug'] = f"decile{deciles10.decile[dec10]}_share"
        df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df_tables.loc[j, 'description'] = f"The {survey_type.text[survey]} of the {deciles10.ordinal[dec10]} (tenth of the population) as a share of total {survey_type.text[survey]}."
        df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
        df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
        df_tables.loc[j, 'unit'] = "%"
        df_tables.loc[j, 'shortUnit'] = "%"
        df_tables.loc[j, 'tolerance'] = 5
        df_tables.loc[j, 'type'] = "Numeric"
        df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
        df_tables.loc[j, 'colorScaleNumericBins'] = deciles10.scale_share[dec10]
        df_tables.loc[j, 'colorScaleEqualSizeBins'] = "true"
        df_tables.loc[j, 'colorScaleScheme'] = "OrRd"
        df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1

# %% [markdown]
# ### Tables for variables showing breaks between surveys
# These variables consider a breaks in the series due to changes in surveys' methodology. Special modifications have to be included to graph monthly and yearly variables properly.

# %%
#Create master table for line breaks
df_spells = pd.DataFrame()
j=0

for i in range(len(df_tables)):
    for c_spell in range(1,7):
        df_spells.loc[j, 'master_var'] = df_tables.slug[i]
        df_spells.loc[j, 'name'] = "Consumption surveys"
        df_spells.loc[j, 'slug'] = f"consumption_spell_{c_spell}"
        df_spells.loc[j, 'sourceName'] = df_tables.sourceName[i]
        df_spells.loc[j, 'description'] = df_tables.description[i]
        df_spells.loc[j, 'sourceLink'] = df_tables.sourceLink[i]
        df_spells.loc[j, 'dataPublishedBy'] = df_tables.dataPublishedBy[i]
        df_spells.loc[j, 'unit'] = df_tables.unit[i]
        df_spells.loc[j, 'shortUnit'] = df_tables.shortUnit[i]
        df_spells.loc[j, 'tolerance'] = df_tables.tolerance[i]
        df_spells.loc[j, 'type'] = df_tables.type[i]
        df_spells.loc[j, 'colorScaleNumericMinValue'] = df_tables.colorScaleNumericMinValue[i]
        df_spells.loc[j, 'colorScaleNumericBins'] = df_tables.colorScaleNumericBins[i]
        df_spells.loc[j, 'colorScaleEqualSizeBins'] = df_tables.colorScaleEqualSizeBins[i]
        df_spells.loc[j, 'colorScaleScheme'] = df_tables.colorScaleScheme[i]
        df_spells.loc[j, 'survey_type'] = df_tables.survey_type[i]
        j += 1
        
    for i_spell in range(1,8):
        df_spells.loc[j, 'master_var'] = df_tables.slug[i]
        df_spells.loc[j, 'name'] = "Income surveys"
        df_spells.loc[j, 'slug'] = f"income_spell_{i_spell}"
        df_spells.loc[j, 'sourceName'] = df_tables.sourceName[i]
        df_spells.loc[j, 'description'] = df_tables.description[i]
        df_spells.loc[j, 'sourceLink'] = df_tables.sourceLink[i]
        df_spells.loc[j, 'dataPublishedBy'] = df_tables.dataPublishedBy[i]
        df_spells.loc[j, 'unit'] = df_tables.unit[i]
        df_spells.loc[j, 'shortUnit'] = df_tables.shortUnit[i]
        df_spells.loc[j, 'tolerance'] = df_tables.tolerance[i]
        df_spells.loc[j, 'type'] = df_tables.type[i]
        df_spells.loc[j, 'colorScaleNumericMinValue'] = df_tables.colorScaleNumericMinValue[i]
        df_spells.loc[j, 'colorScaleNumericBins'] = df_tables.colorScaleNumericBins[i]
        df_spells.loc[j, 'colorScaleEqualSizeBins'] = df_tables.colorScaleEqualSizeBins[i]
        df_spells.loc[j, 'colorScaleScheme'] = df_tables.colorScaleScheme[i]
        df_spells.loc[j, 'survey_type'] = df_tables.survey_type[i]
        j += 1
        
#Delete monthly and yearly variables, because there are not spells files for them
df_spells = df_spells[~df_spells['master_var'].str.contains("_month")].reset_index(drop=True)
df_spells = df_spells[~df_spells['master_var'].str.contains("_year")].reset_index(drop=True)

#Create new rows for monthly and yearly aggregations
#Drop shares, because they are not aggregated
df_spells_agg = df_spells[~df_spells['master_var'].str.contains("_share")].copy().reset_index(drop=True)

#Create monthly columns
df_spells_month = df_spells_agg.copy()
df_spells_month['transform'] = "multiplyBy " + df_spells_month['slug'] + " 30"
df_spells_month['slug'] = df_spells_month['slug'] + "_month"
df_spells_month['description'] = df_spells_month['description'].str.replace("day", "month")

#Create yearly columns
df_spells_year = df_spells_agg.copy()
df_spells_year['transform'] = "multiplyBy " + df_spells_year['slug'] + " 365"
df_spells_year['slug'] = df_spells_year['slug'] + "_year"
df_spells_year['description'] = df_spells_year['description'].str.replace("day", "year")

#Concatenate all the spells tables
df_spells = pd.concat([df_spells, df_spells_month, df_spells_year], ignore_index=True)

# %% [markdown]
# ## Grapher views
# Similar to the tables, this creates the grapher views by grouping by types of variables and then running by survey type and poverty lines.

# %%
#Grapher table generation

df_graphers = pd.DataFrame()

j=0

for survey in range(len(survey_type)):
    for agg in range(len(income_aggregation)):
        
        #mean
        df_graphers.loc[j, 'title'] = f"Mean {survey_type.text[survey]} per {income_aggregation.aggregation[agg]}"
        df_graphers.loc[j, 'ySlugs'] = f"mean{income_aggregation.slug_suffix[agg]}"
        df_graphers.loc[j, 'Metric Dropdown'] = "Mean income or expenditure"
        df_graphers.loc[j, 'Decile Dropdown'] = np.nan
        df_graphers.loc[j, 'Aggregation Radio'] = f'{income_aggregation.aggregation[agg].title()}'
        df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df_graphers.loc[j, 'subtitle'] = "This data is adjusted for inflation and for differences in the cost of living between countries."
        df_graphers.loc[j, 'note'] = f"This data is measured in international-$ at 2017 prices. It relates to disposable {survey_type.text[survey]} per capita (exact definitions vary)."
        df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df_graphers.loc[j, 'type'] = np.nan
        df_graphers.loc[j, 'yAxisMin'] = 0
        df_graphers.loc[j, 'facet'] = np.nan
        df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
        df_graphers.loc[j, 'hasMapTab'] = "true"
        df_graphers.loc[j, 'tab'] = "map"
        df_graphers.loc[j, 'mapTargetTime'] = 2019
        df_graphers.loc[j, 'yScaleToggle'] = "true"
        df_graphers.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1
        
        for dec10 in range(len(deciles10)):

            #averages
            df_graphers.loc[j, 'title'] = f"Mean {survey_type.text[survey]} per {income_aggregation.aggregation[agg]} within the {deciles10.ordinal[dec10]}"
            df_graphers.loc[j, 'ySlugs'] = f"decile{deciles10.decile[dec10]}_avg{income_aggregation.slug_suffix[agg]}"
            df_graphers.loc[j, 'Metric Dropdown'] = "Mean income or expenditure, by decile"
            df_graphers.loc[j, 'Decile Dropdown'] = f'{deciles10.dropdown[dec10]}'
            df_graphers.loc[j, 'Aggregation Radio'] = f'{income_aggregation.aggregation[agg].title()}'
            df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
            df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
            df_graphers.loc[j, 'subtitle'] = f"This is the mean {survey_type.text[survey]} per {income_aggregation.aggregation[agg]} within the {deciles10.ordinal[dec10]} (tenth of the population)."
            df_graphers.loc[j, 'note'] = f"This data is measured in international-$ at 2017 prices to account for inflation and differences in the cost of living between countries. It relates to either {survey_type.text[survey]}  per capita (exact definitions vary)."
            df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
            df_graphers.loc[j, 'type'] = np.nan
            df_graphers.loc[j, 'yAxisMin'] = 0
            df_graphers.loc[j, 'facet'] = np.nan
            df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
            df_graphers.loc[j, 'hasMapTab'] = "true"
            df_graphers.loc[j, 'tab'] = "map"
            df_graphers.loc[j, 'mapTargetTime'] = 2019
            df_graphers.loc[j, 'yScaleToggle'] = "true"
            df_graphers.loc[j, 'survey_type'] = survey_type['table_name'][survey]
            j += 1

        #median
        df_graphers.loc[j, 'title'] = f"Median {survey_type.text[survey]} per {income_aggregation.aggregation[agg]}"
        df_graphers.loc[j, 'ySlugs'] = f"median{income_aggregation.slug_suffix[agg]}"
        df_graphers.loc[j, 'Metric Dropdown'] = "Median income or expenditure"
        df_graphers.loc[j, 'Decile Dropdown'] = np.nan
        df_graphers.loc[j, 'Aggregation Radio'] = f'{income_aggregation.aggregation[agg].title()}'
        df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df_graphers.loc[j, 'subtitle'] = "This data is adjusted for inflation and for differences in the cost of living between countries."
        df_graphers.loc[j, 'note'] = f"This data is measured in international-$ at 2017 prices. It relates to disposable {survey_type.text[survey]} per capita (exact definitions vary)."
        df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df_graphers.loc[j, 'type'] = np.nan
        df_graphers.loc[j, 'yAxisMin'] = 0
        df_graphers.loc[j, 'facet'] = np.nan
        df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
        df_graphers.loc[j, 'hasMapTab'] = "true"
        df_graphers.loc[j, 'tab'] = "map"
        df_graphers.loc[j, 'mapTargetTime'] = 2019
        df_graphers.loc[j, 'yScaleToggle'] = "true"
        df_graphers.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1

        for dec9 in range(len(deciles9)):

            #thresholds
            df_graphers.loc[j, 'title'] = f"Threshold {survey_type.text[survey]} per {income_aggregation.aggregation[agg]} marking the {deciles9.ordinal[dec9]}"
            df_graphers.loc[j, 'ySlugs'] = f"decile{deciles9.decile[dec9]}_thr{income_aggregation.slug_suffix[agg]}"
            df_graphers.loc[j, 'Metric Dropdown'] = "Decile thresholds"
            df_graphers.loc[j, 'Decile Dropdown'] = f'{deciles9.dropdown[dec9]}'
            df_graphers.loc[j, 'Aggregation Radio'] = f'{income_aggregation.aggregation[agg].title()}'
            df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
            df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
            df_graphers.loc[j, 'subtitle'] = f"This is the level of {survey_type.text[survey]} per {income_aggregation.aggregation[agg]} below which {deciles9.decile[dec9]}0% of the population falls."
            df_graphers.loc[j, 'note'] = f"This data is measured in international-$ at 2017 prices to account for inflation and differences in the cost of living between countries. It relates to either {survey_type.text[survey]}  per capita (exact definitions vary)."
            df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
            df_graphers.loc[j, 'type'] = np.nan
            df_graphers.loc[j, 'yAxisMin'] = 0
            df_graphers.loc[j, 'facet'] = np.nan
            df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
            df_graphers.loc[j, 'hasMapTab'] = "true"
            df_graphers.loc[j, 'tab'] = "map"
            df_graphers.loc[j, 'mapTargetTime'] = 2019
            df_graphers.loc[j, 'yScaleToggle'] = "true"
            df_graphers.loc[j, 'survey_type'] = survey_type['table_name'][survey]
            j += 1


            
        #thresholds - multiple deciles
        df_graphers.loc[j, 'title'] = f"Threshold {survey_type.text[survey]} per {income_aggregation.aggregation[agg]} for each decile"
        df_graphers.loc[j, 'ySlugs'] = f"decile1_thr{income_aggregation.slug_suffix[agg]} decile2_thr{income_aggregation.slug_suffix[agg]} decile3_thr{income_aggregation.slug_suffix[agg]} decile4_thr{income_aggregation.slug_suffix[agg]} decile5_thr{income_aggregation.slug_suffix[agg]} decile6_thr{income_aggregation.slug_suffix[agg]} decile7_thr{income_aggregation.slug_suffix[agg]} decile8_thr{income_aggregation.slug_suffix[agg]} decile9_thr{income_aggregation.slug_suffix[agg]}"
        df_graphers.loc[j, 'Metric Dropdown'] = "Decile thresholds"
        df_graphers.loc[j, 'Decile Dropdown'] = "All deciles"
        df_graphers.loc[j, 'Aggregation Radio'] = f'{income_aggregation.aggregation[agg].title()}'
        df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df_graphers.loc[j, 'subtitle'] = f"This is the level of {survey_type.text[survey]} per year below which 10%, 20%, 30%, etc. of the population falls. This data is adjusted for inflation and for differences in the cost of living between countries."
        df_graphers.loc[j, 'note'] = f"This data is measured in international-$ at 2017 prices. It relates to disposable {survey_type.text[survey]} per capita (exact definitions vary)."
        df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df_graphers.loc[j, 'type'] = np.nan
        df_graphers.loc[j, 'yAxisMin'] = 0
        df_graphers.loc[j, 'facet'] = "entity"
        df_graphers.loc[j, 'selectedFacetStrategy'] = "entity"
        df_graphers.loc[j, 'hasMapTab'] = np.nan
        df_graphers.loc[j, 'tab'] = np.nan
        df_graphers.loc[j, 'mapTargetTime'] = np.nan
        df_graphers.loc[j, 'yScaleToggle'] = "true"
        df_graphers.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1
        
        #averages - multiple deciles
        df_graphers.loc[j, 'title'] = f"Mean {survey_type.text[survey]} per {income_aggregation.aggregation[agg]} within each decile"
        df_graphers.loc[j, 'ySlugs'] = f"decile1_avg{income_aggregation.slug_suffix[agg]} decile2_avg{income_aggregation.slug_suffix[agg]} decile3_avg{income_aggregation.slug_suffix[agg]} decile4_avg{income_aggregation.slug_suffix[agg]} decile5_avg{income_aggregation.slug_suffix[agg]} decile6_avg{income_aggregation.slug_suffix[agg]} decile7_avg{income_aggregation.slug_suffix[agg]} decile8_avg{income_aggregation.slug_suffix[agg]} decile9_avg{income_aggregation.slug_suffix[agg]} decile10_avg{income_aggregation.slug_suffix[agg]}"
        df_graphers.loc[j, 'Metric Dropdown'] = "Mean income or expenditure, by decile"
        df_graphers.loc[j, 'Decile Dropdown'] = "All deciles"
        df_graphers.loc[j, 'Aggregation Radio'] = f'{income_aggregation.aggregation[agg].title()}'
        df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df_graphers.loc[j, 'subtitle'] = f"This data is adjusted for inflation and for differences in the cost of living between countries."
        df_graphers.loc[j, 'note'] = f"This data is measured in international-$ at 2017 prices. It relates to disposable {survey_type.text[survey]} per capita (exact definitions vary)."
        df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df_graphers.loc[j, 'type'] = np.nan
        df_graphers.loc[j, 'yAxisMin'] = 0
        df_graphers.loc[j, 'facet'] = "entity"
        df_graphers.loc[j, 'selectedFacetStrategy'] = "entity"
        df_graphers.loc[j, 'hasMapTab'] = np.nan
        df_graphers.loc[j, 'tab'] = np.nan
        df_graphers.loc[j, 'mapTargetTime'] = np.nan
        df_graphers.loc[j, 'yScaleToggle'] = "true"
        df_graphers.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1
        
            
    for dec10 in range(len(deciles10)):

        #shares
        df_graphers.loc[j, 'title'] = f"Share of the {deciles10.ordinal[dec10]} in total {survey_type.text[survey]}"
        df_graphers.loc[j, 'ySlugs'] = f"decile{deciles10.decile[dec10]}_share"
        df_graphers.loc[j, 'Metric Dropdown'] = "Decile shares"
        df_graphers.loc[j, 'Decile Dropdown'] = f'{deciles10.dropdown[dec10]}'
        df_graphers.loc[j, 'Aggregation Radio'] = np.nan
        df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df_graphers.loc[j, 'subtitle'] = f"This is the {survey_type.text[survey]} of the {deciles10.ordinal[dec10]} (tenth of the population) as a share of total {survey_type.text[survey]}."
        df_graphers.loc[j, 'note'] = f"This data relates to disposable {survey_type.text[survey]} per capita (exact definitions vary)."
        df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df_graphers.loc[j, 'type'] = np.nan
        df_graphers.loc[j, 'yAxisMin'] = 0
        df_graphers.loc[j, 'facet'] = np.nan
        df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
        df_graphers.loc[j, 'hasMapTab'] = "true"
        df_graphers.loc[j, 'tab'] = "map"
        df_graphers.loc[j, 'mapTargetTime'] = 2019
        df_graphers.loc[j, 'yScaleToggle'] = "false"
        df_graphers.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1
        
    #shares - multiple deciles
    df_graphers.loc[j, 'title'] = f"Share of the total {survey_type.text[survey]} per {income_aggregation.aggregation[agg]} for each decile"
    df_graphers.loc[j, 'ySlugs'] = f"decile1_share decile2_share decile3_share decile4_share decile5_share decile6_share decile7_share decile8_share decile9_share decile10_share"
    df_graphers.loc[j, 'Metric Dropdown'] = "Decile shares"
    df_graphers.loc[j, 'Decile Dropdown'] = "All deciles"
    df_graphers.loc[j, 'Aggregation Radio'] = np.nan
    df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
    df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
    df_graphers.loc[j, 'subtitle'] = f"This data is adjusted for inflation and for differences in the cost of living between countries."
    df_graphers.loc[j, 'note'] = f"This data relates to disposable {survey_type.text[survey]} per capita (exact definitions vary)."
    df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
    df_graphers.loc[j, 'type'] = np.nan
    df_graphers.loc[j, 'yAxisMin'] = 0
    df_graphers.loc[j, 'facet'] = "entity"
    df_graphers.loc[j, 'selectedFacetStrategy'] = "entity"
    df_graphers.loc[j, 'hasMapTab'] = np.nan
    df_graphers.loc[j, 'tab'] = np.nan
    df_graphers.loc[j, 'mapTargetTime'] = np.nan
    df_graphers.loc[j, 'survey_type'] = survey_type['table_name'][survey]
    j += 1
    
df_graphers['Show breaks between less comparable surveys Checkbox'] = "false"

# %% [markdown]
# ### Grapher views to show breaks in the curves
# Similar to the tables, additional modifications have to be done to process monthly and yearly data properly.

# %%
df_graphers_spells = pd.DataFrame()
j=0

for i in range(len(df_graphers)):
    df_graphers_spells.loc[j, 'title'] = df_graphers['title'][i]
    df_graphers_spells.loc[j, 'ySlugs'] = "consumption_spell_1 consumption_spell_2 consumption_spell_3 consumption_spell_4 consumption_spell_5 consumption_spell_6 income_spell_1 income_spell_2 income_spell_3 income_spell_4 income_spell_5 income_spell_6 income_spell_7"
    df_graphers_spells.loc[j, 'Metric Dropdown'] = df_graphers['Metric Dropdown'][i]
    df_graphers_spells.loc[j, 'Decile Dropdown'] = df_graphers['Decile Dropdown'][i]
    df_graphers_spells.loc[j, 'Aggregation Radio'] = df_graphers['Aggregation Radio'][i]
    df_graphers_spells.loc[j, 'Household survey data type Dropdown'] = df_graphers['Household survey data type Dropdown'][i]
    df_graphers_spells.loc[j, 'tableSlug'] = df_graphers['survey_type'][i] + "_" + df_graphers['ySlugs'][i]
    df_graphers_spells.loc[j, 'subtitle'] = df_graphers['subtitle'][i]
    df_graphers_spells.loc[j, 'note'] = df_graphers['note'][i]
    df_graphers_spells.loc[j, 'sourceDesc'] = df_graphers['sourceDesc'][i]
    df_graphers_spells.loc[j, 'type'] = df_graphers['type'][i]
    df_graphers_spells.loc[j, 'yAxisMin'] = df_graphers['yAxisMin'][i]
    df_graphers_spells.loc[j, 'facet'] = 'entity'
    df_graphers_spells.loc[j, 'selectedFacetStrategy'] = 'entity'
    df_graphers_spells.loc[j, 'hasMapTab'] = "false"
    df_graphers_spells.loc[j, 'tab'] = np.nan
    df_graphers_spells.loc[j, 'mapTargetTime'] = np.nan
    df_graphers_spells.loc[j, 'Show breaks between less comparable surveys Checkbox'] = "true"
    j += 1
    
#Delete spells views for multiple deciles
df_graphers_spells = df_graphers_spells[~(df_graphers_spells['Decile Dropdown'] == 'All deciles')].reset_index(drop=True)

df_graphers_spells.loc[df_graphers_spells['tableSlug'].str.contains("_month"), ['ySlugs']] = "consumption_spell_1_month consumption_spell_2_month consumption_spell_3_month consumption_spell_4_month consumption_spell_5_month consumption_spell_6_month income_spell_1_month income_spell_2_month income_spell_3_month income_spell_4_month income_spell_5_month income_spell_6_month income_spell_7_month"
df_graphers_spells.loc[df_graphers_spells['tableSlug'].str.contains("_year"), ['ySlugs']] = "consumption_spell_1_year consumption_spell_2_year consumption_spell_3_year consumption_spell_4_year consumption_spell_5_year consumption_spell_6_year income_spell_1_year income_spell_2_year income_spell_3_year income_spell_4_year income_spell_5_year income_spell_6_year income_spell_7_year"

#Modify tableSlug to redirect _month and _year to the daily tables
df_graphers_spells['tableSlug'] = df_graphers_spells['tableSlug'].str.removesuffix("_month")
df_graphers_spells['tableSlug'] = df_graphers_spells['tableSlug'].str.removesuffix("_year")
    
df_graphers = pd.concat([df_graphers, df_graphers_spells], ignore_index=True)

# %% [markdown]
# Final adjustments to the graphers table: add `relatedQuestion` link and `defaultView`, and also order decile and metric dropdowns properly

# %%
#Add related question link
df_graphers['relatedQuestionText'] = np.nan
df_graphers['relatedQuestionUrl'] = np.nan
    
#Select one default view
df_graphers.loc[(df_graphers['Decile Dropdown'] == 'All deciles') 
                & (df_graphers['Metric Dropdown'] == "Decile thresholds")
                & (df_graphers['Aggregation Radio'] == "Day") 
                & (df_graphers['Show breaks between less comparable surveys Checkbox'] == "false")
                & (df_graphers['tableSlug'] == "inc_or_cons"), ['defaultView']] = "true"
    
    
#Reorder dropdown menus
#Decile dropdown
decile_dropdown_list = [np.nan,
                        '1 (poorest)',
                        '2',
                        '3',
                        '4',
                        '5',
                        '5 (median)',
                        '6',
                        '7',
                        '8',
                        '9',
                        '9 (richest)',
                        '10 (richest)',
                        'All deciles']

df_graphers_mapping = pd.DataFrame({'decile_dropdown': decile_dropdown_list,})
df_graphers_mapping = df_graphers_mapping.reset_index().set_index('decile_dropdown')
df_graphers['decile_dropdown_aux'] = df_graphers['Decile Dropdown'].map(df_graphers_mapping['index'])

#Metric dropdown
metric_dropdown_list = ["Mean income or expenditure",
                        "Mean income or expenditure, by decile",
                        "Median income or expenditure",
                        "Decile thresholds",
                        "Decile shares"]

df_graphers_mapping = pd.DataFrame({'metric_dropdown': metric_dropdown_list,})
df_graphers_mapping = df_graphers_mapping.reset_index().set_index('metric_dropdown')
df_graphers['metric_dropdown_aux'] = df_graphers['Metric Dropdown'].map(df_graphers_mapping['index'])

#Drop auxiliary variables
df_graphers = df_graphers.sort_values(['metric_dropdown_aux', 'decile_dropdown_aux'], ignore_index=True)
df_graphers = df_graphers.drop(columns=['metric_dropdown_aux', 'decile_dropdown_aux'])

# %% [markdown]
# ## Explorer generation
# Here, the header, tables and graphers dataframes are combined to be shown in for format required for OWID data explorers.

# %%
#Define list of variables to iterate: survey types and the list of variables (the latter for spell tables)
survey_list = list(survey_type['table_name'].unique())
var_list = list(df_spells['master_var'].unique())

#Header is converted into a tab-separated text
header_tsv = df_header.to_csv(sep="\t", header=False)

#Auxiliar variable `survey_type` is dropped and graphers table is converted into a tab-separated text
graphers_tsv = df_graphers.drop(columns=['survey_type'])
graphers_tsv = graphers_tsv.to_csv(sep="\t", index=False)

#This table is indented, to follow explorers' format
graphers_tsv_indented = textwrap.indent(graphers_tsv, "\t")

#The dataframes are combined, including tables which are filtered by survey type and variable
with open(f'data/ppp_2017/final/OWID_internal_upload/explorer_database/across_distribution/grapher.tsv', "w", newline="\n") as f:
    f.write(header_tsv)
    f.write("\ngraphers\n" + graphers_tsv_indented)
    
    for i in survey_list:
        table_tsv = df_tables[df_tables['survey_type'] == i].copy().reset_index(drop=True)
        table_tsv = table_tsv.drop(columns=['survey_type'])
        table_tsv = table_tsv.to_csv(sep="\t", index=False)
        table_tsv_indented = textwrap.indent(table_tsv, "\t")
        f.write("\ntable\t" + "https://raw.githubusercontent.com/owid/notebooks/main/BetterDataDocs/JoeHasell/PIP/data/ppp_2017/final/OWID_internal_upload/explorer_database/" + i + "/poverty_" + i + ".csv\t" + i)
        f.write("\ncolumns\t" + i + "\n\n" + table_tsv_indented)
        
    for var in var_list:
        for i in survey_list:
            table_tsv = df_spells[(df_spells['master_var'] == var) & (df_spells['survey_type'] == i)].copy().reset_index(drop=True)
            table_tsv = table_tsv.drop(columns=['master_var', 'survey_type'])
            table_tsv = table_tsv.to_csv(sep="\t", index=False)
            table_tsv_indented = textwrap.indent(table_tsv, "\t")
            f.write("\ntable\t" + "https://raw.githubusercontent.com/owid/notebooks/main/BetterDataDocs/JoeHasell/PIP/data/ppp_2017/final/OWID_internal_upload/explorer_database/comparability_data/" + i + "/" + var + ".csv\t" + i + "_" + var)
            f.write("\ncolumns\t" + i + "_" + var + "\n\n" + table_tsv_indented)
