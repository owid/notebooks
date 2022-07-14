#%%
import pandas as pd
#%%
file = 'https://raw.githubusercontent.com/owid/notebooks/main/PabloArriagada/poverty_inequality_dataexplorer/WID/wid_pretax_992j_dist.csv'
df = pd.read_csv(file, keep_default_na=False,
                         na_values=['-1.#IND', '1.#QNAN', '1.#IND', '-1.#QNAN', '#N/A N/A', '#N/A', 'N/A', 'n/a', '', '#NA', 
                                    'NULL', 'null', 'NaN', '-NaN', 'nan', '-nan', ''])




# %%

keep_percentiles = ['p0p1', 'p1p2', 'p2p3', 'p3p4', 'p4p5', 'p5p6', 'p6p7', 'p7p8',
       'p8p9', 'p9p10', 'p10p11', 'p11p12', 'p12p13', 'p13p14', 'p14p15',
       'p15p16', 'p16p17', 'p17p18', 'p18p19', 'p19p20', 'p20p21',
       'p21p22', 'p22p23', 'p23p24', 'p24p25', 'p25p26', 'p26p27',
       'p27p28', 'p28p29', 'p29p30', 'p30p31', 'p31p32', 'p32p33',
       'p33p34', 'p34p35', 'p35p36', 'p36p37', 'p37p38', 'p38p39',
       'p39p40', 'p40p41', 'p41p42', 'p42p43', 'p43p44', 'p44p45',
       'p45p46', 'p46p47', 'p47p48', 'p48p49', 'p49p50', 'p50p51',
       'p51p52', 'p52p53', 'p53p54', 'p54p55', 'p55p56', 'p56p57',
       'p57p58', 'p58p59', 'p59p60', 'p60p61', 'p61p62', 'p62p63',
       'p63p64', 'p64p65', 'p65p66', 'p66p67', 'p67p68', 'p68p69',
       'p69p70', 'p70p71', 'p71p72', 'p72p73', 'p73p74', 'p74p75',
       'p75p76', 'p76p77', 'p77p78', 'p78p79', 'p79p80', 'p80p81',
       'p81p82', 'p82p83', 'p83p84', 'p84p85', 'p85p86', 'p86p87',
       'p87p88', 'p88p89', 'p89p90', 'p90p91', 'p91p92', 'p92p93',
       'p93p94', 'p94p95', 'p95p96', 'p96p97', 'p97p98', 'p98p99',
       'p99p100']


df = df[df['percentile'].isin(keep_percentiles)]

# %%
url = 'https://raw.githubusercontent.com/owid/notebooks/main/JoeHasell/Povcal_data_work/Global_distribution/gpinter/data/WID/original/WID%20regions_country_standardized.csv'

df_mapping = pd.read_csv(url)
# %%
