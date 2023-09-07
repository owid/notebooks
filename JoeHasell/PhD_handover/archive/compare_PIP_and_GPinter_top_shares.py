
#%%
import pandas as pd
import plotly.express as px

#%%
# Load GPinter estimated data and original PIP top shares
fp = "data/manipulation/pip_estimated_top1_shares.csv"
estimated_shares = pd.read_csv(fp)

fp = "data/manipulation/pip_clean_top1_shares.csv"
pip_shares = pd.read_csv(fp)

#%%
# Merge 
compare = pd.merge(pip_shares, estimated_shares, how = 'outer')

compare['top1_share_gpinter'] = compare['top1_share_gpinter']*100

compare['diff'] = compare['Top 1pc share'] - compare['top1_share_gpinter']

# compare.head()

# fig = px.scatter(compare, x='Top 1pc share', y="top1_share_gpinter")
# fig.show()

fig = px.scatter(compare,x="top1_share_gpinter", y = 'diff', color = 'country')
fig.show()
# %%
