
#%%
import pandas as pd



#%%
fp = '/Users/joehasell/Documents/OWID/notebooks/BetterDataDocs/JoeHasell/PIP/data/poverty_inc_or_cons.csv'
df_orig = pd.read_csv(fp)

df = df_orig
#%%
#select_country = 'Kenya'
#df = df_orig[df_orig['Entity']== select_country]

# %%
# drop regions where survey coverage = nan
df = df[df['survey_comparability'].notna()]

#%%
df['survey_comparability'] = 'comparable_spell_' + df['survey_comparability'].astype(int).astype(str)

# %%
select_var = 'headcount_ratio_190'

df = df[['Entity', 'Year', select_var, 'survey_comparability']]
# %%
# convert t0 wide
df = pd.pivot(df, index=['Entity', 'Year'], columns=['survey_comparability'], values=select_var).reset_index()



# %%
# write to csv
df.to_csv("test_of_show_breaks.csv", index = False)
# %%
