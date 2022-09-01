
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
# FORMAT COMPARABILTY VAR
# Add 1 to make comparability var run from 1, not from 0
df['survey_comparability'] = df['survey_comparability'] + 1

# Make a more friendly slug for when the data gets pivoted wider
df['survey_comparability'] = 'comparable_spell_' + df['survey_comparability'].astype(int).astype(str)

# %%

for select_var in ['headcount_ratio_190']:

    df_var = df[['Entity', 'Year', select_var, 'survey_comparability']]

    # convert t0 wide
    df_var = pd.pivot(df_var, index=['Entity', 'Year'], columns=['survey_comparability'], values=select_var).reset_index()

    
    # write to csv – one csv per variable in the main dataset
    df_var.to_csv(f'comparability_data/{select_var}.csv', index = False)
# %%
