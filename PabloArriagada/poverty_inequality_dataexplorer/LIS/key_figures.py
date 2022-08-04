# # Using Key Figures from LIS

# This notebook compares the data from the Key Figures Module of LIS

import pandas as pd
from pathlib import Path
import numpy as np
import plotly.express as px
import plotly.io as pio

# +
file = Path('data/access-key-workbook.xlsx')
kf_excel = pd.read_excel(file, sheet_name='Key Figures as of 12-Jun-2022')
kf_excel = kf_excel.rename(columns={"LIS Dataset_x000D_\n": "LIS Dataset", "Wave_x000D_\n": "Wave"})
kf_excel.drop(kf_excel.index[648:652], axis=0, inplace=True)

cols = kf_excel.columns.drop(['LIS Dataset', 'Wave'])
kf_excel[cols] = kf_excel[cols].apply(pd.to_numeric, errors='coerce')


file = Path('data/key_figures_search.xlsx')
kf_search = pd.read_excel(file, sheet_name='Sheet1')

cols = kf_search.columns.drop(['DATASET(S)'])
kf_search[cols] = kf_search[cols].apply(pd.to_numeric, errors='coerce')
# -

kf_excel

kf_search

kf_excel.columns

kf_search.columns

# +
kf_excel['entity_year'] = kf_excel['LIS Dataset'].str.split('-').apply(lambda x: x[1])
kf_excel['year'] = kf_excel['entity_year'].str[-4:]
kf_excel['year'] = kf_excel['year'].apply(pd.to_numeric, errors='coerce')
kf_excel['entity'] = kf_excel['entity_year'].str[:-5]

kf_search['entity'] = kf_search['DATASET(S)'].str[:2]
kf_search['year'] = kf_search['DATASET(S)'].str[2:]
# -

kf_excel

kf_search[['GINI']].describe()

kf_excel[['Gini Coefficient']].describe()

kf_search[['ATK5']].describe()

kf_excel[['Atkinson Coefficient (epsilon=0.5)']].describe()

# +
cols_excel = kf_excel.columns.drop(['LIS Dataset', 'Wave', 'entity', 'year'])
cols_search = kf_search.columns.drop(['DATASET(S)', 'entity', 'year'])

hola = kf_excel[cols_excel].where(kf_excel[cols_excel].values==kf_search[cols_search].values).notna()
# -

kf_excel['Gini Coefficient'].isin(kf_search['GINI']).value_counts()

hola['Gini Coefficient'].value_counts()

fig = px.line(kf_excel, x="year", y="Gini Coefficient", color="entity", title='Inequality according to LIS')
fig.show()

fig = px.histogram(kf_excel, x="year", marginal="box", title="<b>Distribution of years in LIS</b>")
fig.show()

kf_count = kf_excel.groupby(['year']).size()
kf_count


