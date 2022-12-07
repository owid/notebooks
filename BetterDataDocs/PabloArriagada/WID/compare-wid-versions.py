# +
import pandas as pd

wid_2021 = pd.read_csv('data/raw/wid_indices_992j_2021.csv',
                           keep_default_na=False,
                           na_values=['-1.#IND', '1.#QNAN', '1.#IND', '-1.#QNAN', '#N/A N/A', '#N/A', 'N/A', 'n/a', '', '#NA', 
                                        'NULL', 'null', 'NaN', '-NaN', 'nan', '-nan', ''])
wid_2022 = pd.read_csv('data/raw/wid_indices_992j.csv',
                           keep_default_na=False,
                           na_values=['-1.#IND', '1.#QNAN', '1.#IND', '-1.#QNAN', '#N/A N/A', '#N/A', 'N/A', 'n/a', '', '#NA', 
                                        'NULL', 'null', 'NaN', '-NaN', 'nan', '-nan', ''])
# -

merge = pd.merge(wid_2021[['country', 'year']], wid_2022[['country', 'year']], how='outer', indicator=True)
merge

merge.to_csv('data/raw/compare_wid_updates.csv', index=False)

merge._merge.value_counts()


