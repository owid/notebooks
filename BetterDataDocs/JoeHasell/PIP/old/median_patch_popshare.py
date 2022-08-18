# %%
# 

start_time = time.time()

df_query = pip_query_country(
                    popshare_or_povline = "povline", 
                    value = 1.9, 
                    fill_gaps="false")

median_list = []

for i in range(len(df_query)):
    if np.isnan(df_query['median'][i]):
        df_popshare = pip_query_country(popshare_or_povline = "popshare",
                                        country_code = df_query['country_code'][i],
                                        year = df_query['reporting_year'][i],
                                        welfare_type = df_query['welfare_type'][i],
                                        reporting_level = df_query['reporting_level'][i],
                                        value = 0.5,
                                        fill_gaps="false")
        try:
            median_value = df_popshare['poverty_line'][0]
            median_list.append(median_value)
        
        except:
            median_list.append(np.nan)
        
        
    else:
        median_value = df_query['median'][i]
        median_list.append(median_value)
               

df_query['median2'] = median_list
df_query = df_query.rename(columns={'country_name': 'Entity',
                                    'reporting_year': 'Year'})
null_median = (df_query['median'].isnull()).sum()
null_median2 = (df_query['median2'].isnull()).sum()
print(f'Before patching: {null_median} nulls for median')
print(f'After patching: {null_median2} nulls for median')

df_final = pd.merge(df_final, df_query[['Entity', 'Year', 'welfare_type', 'reporting_level', 'median2']], 
                       how='left', 
                       on=['Entity', 'Year', 'welfare_type', 'reporting_level'], 
                       validate='many_to_one')
df_final['median_ratio'] = df_final['median'] / df_final['median2']
median_ratio_median = (df_final['median_ratio']).median()
median_ratio_min = (df_final['median_ratio']).min()
median_ratio_max = (df_final['median_ratio']).max()

if median_ratio_median == 1 and median_ratio_min == 1 and median_ratio_max == 1:
    print(f'Patch successful.')
    print(f'Ratio between old and new variable: Median = {median_ratio_median}, Min = {median_ratio_min}, Max = {median_ratio_max}')
else:
    print(f'Patch changed some median values. Please check for errors.')
    print(f'Ratio between old and new variable: Median = {median_ratio_median}, Min = {median_ratio_min}, Max = {median_ratio_max}')

df_final.drop(columns=['median', 'median_ratio'], inplace=True)
df_final.rename(columns={'median2': 'median'}, inplace=True)


end_time = time.time()
elapsed_time = end_time - start_time
print('Execution time:', elapsed_time, 'seconds')
