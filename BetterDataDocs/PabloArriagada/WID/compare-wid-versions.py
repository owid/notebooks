# +
import pandas as pd

wid_2021 = pd.read_csv('data/raw/wid_indices_992j_2021.csv')
wid_2022 = pd.read_csv('data/raw/wid_indices_992j.csv')
# -

merge = pd.merge(wid_2021[['country', 'year']], wid_2022[['country', 'year']], how='outer', indicator=True)
merge

merge.to_csv('data/raw/compare_wid_updates.csv', index=False)


