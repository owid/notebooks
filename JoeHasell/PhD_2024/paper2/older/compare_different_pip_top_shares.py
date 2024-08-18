#%%
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt



# COMPARE TOP 10% SHARES

#%% Grab top10 share from 'key indicators' dataset
# Load the main dataset prepared by Pablo
fp = "https://catalog.ourworldindata.org/explorers/poverty_inequality/latest/poverty_inequality_export/keyvars.feather"
df = pd.read_feather(fp)

df_key_vars = df[df['series_code']=='p90p100Share_pip_disposable_perCapita']

df_key_vars = df_key_vars[['country', 'year', 'pipreportinglevel', 'pipwelfare', 'value']]
df_key_vars['value'] = df_key_vars['value'] / 100

#%% Load data for China etc. that I summed from rural and urban percentile shares
fp = "data/top_pip_shares_comparison/china_etc_top10shares.csv"
df_china_etc_aggregated = pd.read_csv(fp)
df_china_etc_aggregated['pipreportinglevel']='national'

#%% Load data I summed up from the main percentile file (i.e. China etc. are only present as rural and urban)
fp = "data/top_pip_shares_comparison/main_perc_top10shares.csv"
df_main_perc = pd.read_csv(fp)


#%% Load data I aggregated from the thousand bins dataset (older verion of the PIP database)
fp = "data/top_pip_shares_comparison/thou_bin_top10shares.csv"
df_thou_bin = pd.read_csv(fp)
df_thou_bin['pipreportinglevel']='national'
df_thou_bin['pipwelfare']='none_assigned'


#%% MERGE ALL THE DATA TOGETHER (NB thou bin data doesn't have welfare column)

# Concatenate the DataFrames vertically with keys
concatenated_df = pd.concat([df_key_vars, df_china_etc_aggregated, df_main_perc, df_thou_bin], keys=['direct_pip', 'my_aggregation', 'main_perc', 'thou_bin'])

# Reset the index to make the keys a separate column
concatenated_df.reset_index(level=0, inplace=True)

# Rename the 'level_0' column to 'key'
concatenated_df.rename(columns={'level_0': 'key'}, inplace=True)

# Reset the index to make it sequential
concatenated_df.reset_index(drop=True, inplace=True)

# Add a ID col that combines reporting level, welfare, and 'df'
concatenated_df['series_id'] = concatenated_df['key'] + ' (' + concatenated_df['pipreportinglevel'] + '_' + concatenated_df['pipwelfare'] + ')' 

#%% PLOT TO COMPARE

#%%
def save_comparison_plot(country):
    # Select data
    df = concatenated_df[concatenated_df['country']==country]

    df = df[df['pipreportinglevel']=='national']
    df = df[df['key'].isin(['direct_pip', 'my_aggregation', 'thou_bin'])]

    # Create the line plot
    plt.figure(figsize=(10, 6))  # Adjust the figure size if needed
    sns.lineplot(data=df, x='year', y='value', hue='key', marker='o')

    # Set plot title and labels
    plt.title(f'Comparison of top 10pc share from source – {country}')
    plt.xlabel('Year')
    plt.ylabel('Value')

    # Show the plot
    plt.legend(title='series_id')  # Add legend with title
    plt.grid(True)  # Add grid


    # Save the plot as an SVG file
    plt.savefig(f'plots/compare_top_10_share_{country}.svg', format='svg')

    plt.show()

#%% Save comparison plots for China, India and Indonesia
save_comparison_plot('China')
save_comparison_plot('India')
save_comparison_plot('Indonesia')


############################################
############################################


# COMPARE TOP 1% SHARES

# Only available in my own aggregation of the urban/rural data and
# in the thousand bins data


#%% Load data for China etc. that I summed from rural and urban percentile shares
fp = "data/top_pip_shares_comparison/china_etc_top1shares.csv"
df_china_etc_aggregated = pd.read_csv(fp)
df_china_etc_aggregated['pipreportinglevel']='national'

#%% Load data I aggregated from the thousand bins dataset (older verion of the PIP database)
fp = "data/top_pip_shares_comparison/thou_bin_top1shares.csv"
df_thou_bin = pd.read_csv(fp)
df_thou_bin['pipreportinglevel']='national'
df_thou_bin['pipwelfare']='none_assigned'



#%% MERGE ALL THE DATA TOGETHER (NB thou bin data doesn't have welfare column)

# Concatenate the DataFrames vertically with keys
concatenated_df = pd.concat([df_china_etc_aggregated, df_thou_bin], keys=['my_aggregation', 'thou_bin'])

# Reset the index to make the keys a separate column
concatenated_df.reset_index(level=0, inplace=True)

# Rename the 'level_0' column to 'key'
concatenated_df.rename(columns={'level_0': 'key'}, inplace=True)

# Reset the index to make it sequential
concatenated_df.reset_index(drop=True, inplace=True)

# Add a ID col that combines reporting level, welfare, and 'df'
concatenated_df['series_id'] = concatenated_df['key'] + ' (' + concatenated_df['pipreportinglevel'] + '_' + concatenated_df['pipwelfare'] + ')' 

#%% PLOT TO COMPARE

#%%
def save_comparison_plot(country):
    # Select data
    df = concatenated_df[concatenated_df['country']==country]

    df = df[df['pipreportinglevel']=='national']
    df = df[df['key'].isin(['direct_pip', 'my_aggregation', 'thou_bin'])]

    # Create the line plot
    plt.figure(figsize=(10, 6))  # Adjust the figure size if needed
    sns.lineplot(data=df, x='year', y='value', hue='key', marker='o')

    # Set plot title and labels
    plt.title(f'Comparison of top 1pc share from source – {country}')
    plt.xlabel('Year')
    plt.ylabel('Value')

    # Show the plot
    plt.legend(title='series_id')  # Add legend with title
    plt.grid(True)  # Add grid


    # Save the plot as an SVG file
    plt.savefig(f'plots/compare_top_1_share_{country}.svg', format='svg')

    plt.show()

#%% Save comparison plots for China, India and Indonesia
save_comparison_plot('China')
save_comparison_plot('India')
save_comparison_plot('Indonesia')



#%%