



# %%
import pandas as pd

# %%
#Main data file
url = "https://joeh.fra1.digitaloceanspaces.com/pwt/entities_standardized_national_accounts.csv"

df_main = pd.read_csv(url)

#%%
df_main.head()

#%%
# National Accounts data file
url = "https://joeh.fra1.digitaloceanspaces.com/pwt/entities_standardized.csv"

df_na = pd.read_csv(url)
#%%
df_na.head()