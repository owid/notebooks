# # World Inequality Database indicators
# The [World Inequality Database (WID.world)](https://wid.world/wid-world/) aims to provide open and convenient access to the most extensive available database on the historical evolution of the world distribution of income and wealth, both within countries and between countries. The dataset addresses some of the main limitations household surveys produce in national statistics of this kind: under-coverage at the top of the distribution due to non-response (the richest tend to not answer this kind of surveys or omit their income) or measurement error (the richest underreport their income for convenience or not actually knowing an exact figure if all their activities are added). The problem is handled with the combination of fiscal and national accounts data along household surveys based on the work of the leading researchers in the area: Anthony B. Atkinson, Thomas Piketty, Emmanuel Saez, Facundo Alvaredo, Gabriel Zucman, and hundreds of others. The initiative is based in the Paris School of Economics (as the [World Inequality Lab](https://inequalitylab.world/)) and compiles the World Inequality Report, a yearly publication about how inequality has evolved until the last year.
#
# Besides income and wealth distribution data, the WID has recently added carbon emissions to generate carbon inequality indices. It also offers decomposed stats on national income. The data can be obtained from the website and by R and Stata commands.

# Three income distributions are considered:
# - **Pretax income distribution** `ptinc`, which includes social insurance benefits (and remove corresponding contributions), but exclude other forms of redistribution (income tax, social assistance benefits, etc.).
# - **Post-tax national income distribution** `diinc`, which includes both in-kind and in-cash redistribution.
# - **Post-tax disposable income distribution** `cainc`, which excludes in-kind transfers (because the distribution of in-kind transfers requires a lot of assumptions).
#
# These distributions are the main DINA (distributional national accounts) income variables available at WID. DINA income concepts are distributed income concepts that are consistent with national accounts aggregates. The precise definitions are outlined in the [DINA guidelines](https://wid.world/es/news-article/2020-distributional-national-accounts-guidelines-dina-4/) and country-specific papers. 
#
# All of these distributions are generated using equal-split adults (j) as the population unit, meaning that the unit is the individual, but that income or wealth is distributed equally among all household members. The age group is individuals over age 20 (992, adult population), which excludes children (with 0 income in most of the cases). Extrapolations and interpolations are excluded from these files, as WID discourages its use at the level of individual countries (see the `exclude` description at `help wid` in Stata). More information about the variables and definitions can be found on [WID's codes dictionary](https://wid.world/codes-dictionary/).
#
# The variables processed in this notebook come from commands given in the `wid` function in Stata. These commands are located in the `wid_indices.do` file from this same folder. Selecting 'yes' in the code will execute this code and generate the most recent data from WID. Both `.csv` and `.dta` files are available for analysis in `data/raw/`.

from create_dataset_functions import *
import time

# ## Question: Do you want to run the WID query in Stata? (~10 minutes)
# Choosing `yes` will run the Stata code first to get the most recent data. Choosing `no` will process data which was previously extracted from the Stata's do file.

# +
print('WARNING: If a full update is needed, first you have to run a Stata\'s query in a do file.')
print('It usually takes about 10 minutes to execute.')

question = "Do you want to run this do file?"
answer = query_yes_no(question)
# -

# ## Run the do file
# This section runs the `wid_indices.do` file in Stata (if `yes` was selected). You can change Stata's directory if you have it installed somewhere else (just change the `stata_dir` path).

start_time = time.time()
dofile = "wid_indices.do"
stata_dir = "C:\Program Files\Stata14\StataMP-64.exe"
run_stata(dofile, stata_dir, answer)

# ## Load Stata's output and standardize
# This step takes Stata's output, changes entities names to OWID standard, renames `year` to `Year` and multiplies shares variables by 100

file = 'data/raw/wid_indices_992j.csv'
df_final = load_and_standardize(file)

# ## Reformat and export dataset
# Variables are renamed for more human-readable columns to be uploaded in Grapher as a dataset.

add_metadata_and_export(df_final, 'wid_pretax')
#add_metadata_and_export(df_final, 'wid_posttax_dis')
#add_metadata_and_export(df_final, 'wid_posttax_nat')

# ## Create special dataset to compare long-run share of top 1%
# This is a to create a faceted chart to compare the evolution of the income share for the top 1% in English-speaking countries vs. Continental Europe + Japan.

create_faceted_dataset(df_final)
#create_faceted_dataset_temp() #Until WID updates long-run data

end_time = time.time()
elapsed_time = end_time - start_time
print(f'The files were created in {elapsed_time} seconds :)')
print('Update the pretax WID dataset with data/final/wid_pretax.csv')
#print('Update the post-tax disposable WID dataset with data/final/wid_posttax_dis.csv')
#print('Update the post-tax national WID dataset with data/final/wid_posttax_nat.csv')
print('Update the English vs. Europe/Japan dataset with data/final/wid_faceted.csv')
