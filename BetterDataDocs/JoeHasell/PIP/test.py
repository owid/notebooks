
import pandas as pd

df = pd.DataFrame({"Entity": ['United States', 'United States', 'Kenya', 'Kenya'],
                    "Year": [1990, 2020, 1990, 2020],
                    "headcount_ratio_100": [3, 2, 40, 25]})

is_filled = 'false'
df.to_csv(f'data/poverty_inc_only_filled_{is_filled}.csv')
