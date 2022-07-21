# %%
import pandas as pd

import numpy as np

from standardize_entities_and_save_from_df import standardize_and_save


# %%
id_vars = ['country_name', 'reporting_year','reporting_level','welfare_type']

# %%
# Key vars data
is_filled = "true"

# Import 'constructed' key vars (after GPinter alignment)

df_constructed = pd.read_csv(f'data/intermediate/key_vars/filled_{is_filled}/key_vars_after_Gpinter.csv')

# %%

df_constructed = df_constructed.rename(columns={
    "gini": "gini_constructed",
    "sh_decile_1": "shares_decile_1_constructed",
    "sh_decile_2": "shares_decile_2_constructed",
    "sh_decile_3": "shares_decile_3_constructed",
    "sh_decile_4": "shares_decile_4_constructed",
    "sh_decile_5": "shares_decile_5_constructed",
    "sh_decile_6": "shares_decile_6_constructed",
    "sh_decile_7": "shares_decile_7_constructed",
    "sh_decile_8": "shares_decile_8_constructed",
    "sh_decile_9": "shares_decile_9_constructed",
    "sh_decile_10": "shares_decile_10_constructed",
    "avg_decile_1": "average_daily_decile_1",
    "avg_decile_2": "average_daily_decile_2",
    "avg_decile_3": "average_daily_decile_3",
    "avg_decile_4": "average_daily_decile_4",
    "avg_decile_5": "average_daily_decile_5",
    "avg_decile_6": "average_daily_decile_6",
    "avg_decile_7": "average_daily_decile_7",
    "avg_decile_8": "average_daily_decile_8",
    "avg_decile_9": "average_daily_decile_9",
    "avg_decile_10": "average_daily_decile_10",
    "thresh_decile_1": "threshold_decile_1",
    "thresh_decile_2": "threshold_decile_2",
    "thresh_decile_3": "threshold_decile_3",
    "thresh_decile_4": "threshold_decile_4",
    "thresh_decile_5": "threshold_decile_5",
    "thresh_decile_6": "threshold_decile_6",
    "thresh_decile_7": "threshold_decile_7",
    "thresh_decile_8": "threshold_decile_8",
    "thresh_decile_9": "threshold__decile_9"
    })


# %%
# Import standard key vars from API output
df_original = pd.read_csv("data/API_output/example_response_filled.csv")

# %%

df_original = df_original.rename(columns={
    "median": "median_original",
    "gini": "gini_original",
    "decile1": "shares_decile_1_original",
    "decile2": "shares_decile_2_original",
    "decile3": "shares_decile_3_original",
    "decile4": "shares_decile_4_original",
    "decile5": "shares_decile_5_original",
    "decile6": "shares_decile_6_original",
    "decile7": "shares_decile_7_original",
    "decile8": "shares_decile_8_original",
    "decile9": "shares_decile_9_original",
    "decile10": "shares_decile_10_original"
        })

# %%
# Merge constructed data into original
df_original = df_original.merge(df_constructed, how = 'left')


# %%
# Add 'final' vars
df_original["gini"] = np.where(
        pd.isna(df_original["gini_constructed"]), 
        df_original["gini_constructed"], 
        df_original["gini_original"]) 

for d in range(1,10):
        
    varname = f"shares_decile_{d}"

    df_original[varname] = np.where(
            pd.isna(df_original[f"{varname}_constructed"]), 
            df_original[f"{varname}_constructed"], 
            df_original[f"{varname}_original"]) 


# %%
# Grab top 1% share from percentile data
# Import standard key vars from API output
df_percentiles = pd.read_csv(f'data/intermediate/percentiles/filled_{is_filled}/percentiles_after_Gpinter.csv')

# %%

select_cols = id_vars
select_cols.append("share_in_bracket")



just_topshares = df_percentiles[df_percentiles["p"]==0.99][select_cols]

# %%
just_topshares[just_topshares[id_vars].duplicated()].head()
# %%
df_original = df_original.merge(just_topshares,
    how = 'left')


# %%
df_original = df_original.rename(columns={
    "share_in_bracket": "shares_top_1pc"
    })

# %%
# Standadize country names and write to S3
#df_original.to_csv(f'data/clean/main_data/filled_{is_filled}/main_data.csv', index=False)

standardize_and_save(
    orig_df = df_original,
    entity_mapping_url = "https://joeh.fra1.digitaloceanspaces.com/PIP/country_mapping.csv",
    mapping_varname_raw ='Original Name',
    mapping_vaname_owid = 'Our World In Data Name',
    data_varname_old = 'country_name',
    data_varname_new = 'entity',
    s3_space_to_save_in = 'PIP',
    as_filename = "main_data.csv"
    )

# %%
