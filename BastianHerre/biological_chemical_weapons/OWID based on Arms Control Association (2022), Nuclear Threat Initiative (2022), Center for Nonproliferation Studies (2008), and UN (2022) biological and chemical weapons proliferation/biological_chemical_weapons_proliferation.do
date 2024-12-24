*****  Stata do-file to create the biological-chemical-weapons-proliferation data used in several charts on Our World in Data (OWID)'s biological-and-chemical-weapons page:
*****  
*****  Author: Bastian Herre
*****  November 14, 2024


version 14

clear all
set more off
set varabbrev off


** Set your own working directories here to run the file:
cd "/Users/bastianherre/Dropbox/Data/biological_chemical_weapons/OWID based on Arms Control Association (2022), Nuclear Threat Initiative (2022), Center for Nonproliferation Studies (2008), and UN (2022) biological and chemical weapons proliferation/"


** Download dataset from GitHub repository (which we primarily created from https://www.armscontrol.org/factsheets/cbwprolif, https://www.nti.org/countries/, https://nonproliferation.org/wp-content/uploads/2016/03/2008-Chemical-and-Biological-Weapons_-Possession-and-Programs-Past-and-Present.pdf, https://treaties.unoda.org/t/bwc, and https://treaties.unoda.org/t/cwc) and move it into the folder "Arms Control Association 2022 biological and chemical weapons proliferation".
** Import data:
import excel "biological_chemical_weapons_proliferation_raw.xlsx", firstrow

** Generate numerical variables of interest:
tab bioweapons_status_current
generate bioweapons_status_current_num = 0 if bioweapons_status_current == "neither pursues nor possesses"
replace bioweapons_status_current_num = 1 if bioweapons_status_current == "allegedly pursues"

tab bioweapons_status_hist
generate bioweapons_status_hist_num = 0 if bioweapons_status_hist == "neither pursued nor possessed"
replace bioweapons_status_hist_num = 1 if bioweapons_status_hist == "allegedly pursued"
replace bioweapons_status_hist_num = 2 if bioweapons_status_hist == "pursued"
replace bioweapons_status_hist_num = 3 if bioweapons_status_hist == "allegedly possessed"
replace bioweapons_status_hist_num = 4 if bioweapons_status_hist == "possessed"
replace bioweapons_status_hist_num = 5 if bioweapons_status_hist == "used"

tab chemweapons_status_current
generate chemweapons_status_current_num = 0 if chemweapons_status_current == "neither pursues nor possesses"
replace chemweapons_status_current_num = 1 if chemweapons_status_current == "allegedly pursues"
replace chemweapons_status_current_num = 2 if chemweapons_status_current == "possesses"
replace chemweapons_status_current_num = 3 if chemweapons_status_current == "allegedly recently used"
replace chemweapons_status_current_num = 4 if chemweapons_status_current == "recently used"

tab chemweapons_status_hist
generate chemweapons_status_hist_num = 0 if chemweapons_status_hist == "neither pursued nor possessed"
replace chemweapons_status_hist_num = 1 if chemweapons_status_hist == "pursued"
replace chemweapons_status_hist_num = 2 if chemweapons_status_hist == "allegedly possessed"
replace chemweapons_status_hist_num = 3 if chemweapons_status_hist == "possessed"
replace chemweapons_status_hist_num = 4 if chemweapons_status_hist == "allegedly used"
replace chemweapons_status_hist_num = 5 if chemweapons_status_hist == "used"

** Create world aggregates:


* Temporarily save dataset:
save "biological_chemical_weapons_proliferation_temp.dta", replace

* Create indicator variables for specific regime categories:
tabulate bioweapons_status_current_num, generate(bioweapons_status_current_num)
tabulate bioweapons_status_hist_num, generate(bioweapons_status_hist_num)
tabulate chemweapons_status_current_num, generate(chemweapons_status_current_num)
tabulate chemweapons_status_hist_num, generate(chemweapons_status_hist_num)

* Collapse dataset:
collapse (sum) bioweapons_status_current_num* bioweapons_status_hist_num* chemweapons_status_current_num* chemweapons_status_hist_num*
drop bioweapons_status_current_num bioweapons_status_hist_num chemweapons_status_current_num chemweapons_status_hist_num

* Create entity identifier:
generate country_name = "World"
generate year = 2022

* Rename variables:
rename bioweapons_status_current_num1 num_bioweapons_curr_neither
rename bioweapons_status_current_num2 num_bioweapons_curr_allepur

rename bioweapons_status_hist_num1 num_bioweapons_hist_neither
rename bioweapons_status_hist_num2 num_bioweapons_hist_allepur
rename bioweapons_status_hist_num3 num_bioweapons_hist_pur
rename bioweapons_status_hist_num4 num_bioweapons_hist_alleposs
rename bioweapons_status_hist_num5 num_bioweapons_hist_poss
rename bioweapons_status_hist_num6 num_bioweapons_hist_use

rename chemweapons_status_current_num1 num_chemweapons_curr_neither
rename chemweapons_status_current_num2 num_chemweapons_curr_allepur
rename chemweapons_status_current_num3 num_chemweapons_curr_poss
rename chemweapons_status_current_num4 num_chemweapons_curr_alleuse
rename chemweapons_status_current_num5 num_chemweapons_curr_use

rename chemweapons_status_hist_num1 num_chemweapons_hist_neither
rename chemweapons_status_hist_num2 num_chemweapons_hist_pur
rename chemweapons_status_hist_num3 num_chemweapons_hist_alleposs
rename chemweapons_status_hist_num4 num_chemweapons_hist_poss
rename chemweapons_status_hist_num5 num_chemweapons_hist_alleuse
rename chemweapons_status_hist_num6 num_chemweapons_hist_use

* Temporarily save data:
save "biological_chemical_weapons_proliferation_aggregated.dta", replace

* Merge datasets:
use "biological_chemical_weapons_proliferation_temp.dta"
merge 1:1 country_name using "biological_chemical_weapons_proliferation_aggregated.dta"
drop _merge
erase "biological_chemical_weapons_proliferation_temp.dta"
erase "biological_chemical_weapons_proliferation_aggregated.dta"


** Label variables:
label variable country_name "Country name"
label variable year "Year"

label variable bioweapons_status_current "Current country position towards bioweapons (OWID based on ACA, NTI, and CNS)"
label variable bioweapons_status_current_num "Current country position towards bioweapons (numerical)"
label variable bioweapons_status_hist "Past country position towards bioweapons (OWID based on ACA, NTI, and CNS)"
label variable bioweapons_status_hist_num "Past country position towards bioweapons (numerical)"
label variable chemweapons_status_current "Current country pos. towards chemical weapons (OWID based on ACA, NTI, and CNS)"
label variable chemweapons_status_current_num "Current country position towards chemical weapons (numerical)"
label variable chemweapons_status_hist "Past country position towards chemical weapons (OWID based on ACA, NTI, and CNS)"
label variable chemweapons_status_hist_num "Past country position towards chemical weapons (numerical)"

label variable num_bioweapons_curr_neither "Number of countries neither pursuing nor possessing bioweapons"
label variable num_bioweapons_curr_allepur "Number of countries allegedly pursuing bioweapons"
label variable num_bioweapons_hist_neither "Number of countries that neither pursued nor possessed bioweapons"
label variable num_bioweapons_hist_allepur "Number of countries that allegedly pursued bioweapons"
label variable num_bioweapons_hist_pur "Number of countries that pursued bioweapons"
label variable num_bioweapons_hist_alleposs "Number of countries that allegedly possessed bioweapons"
label variable num_bioweapons_hist_poss "Number of countries that possessed bioweapons"
label variable num_bioweapons_hist_use "Number of countries that used bioweapons in the past"
label variable num_chemweapons_curr_neither "Number of countries neither pursuing nor possessing chemical weapons"
label variable num_chemweapons_curr_allepur "Number of countries allegedly pursuing chemical weapons"
label variable num_chemweapons_curr_poss "Number of countries possessing chemical weapons"
label variable num_chemweapons_curr_alleuse "Number of countries that recently allegedly used chemical weapons"
label variable num_chemweapons_curr_use "Number of countries that recently used chemical weapons"
label variable num_chemweapons_hist_neither "Number of countries that neither pursued nor possessed chemical weapons"
label variable num_chemweapons_hist_pur "Number of countries that pursued chemical weapons"
label variable num_chemweapons_hist_alleposs "Number of countries that allegedly possessed chemical weapons"
label variable num_chemweapons_hist_poss "Number of countries that possessed chemical weapons"
label variable num_chemweapons_hist_alleuse "Number of countries that allegedly used chemical weapons"
label variable num_chemweapons_hist_use "Number of countries that used chemical weapons"


** Order variables:
order country_name year bioweapons_status_current bioweapons_status_current_num bioweapons_status_hist bioweapons_status_hist_num chemweapons_status_current chemweapons_status_current_num chemweapons_status_hist chemweapons_status_hist_num


** Export data:
save "biological_chemical_weapons_proliferation_owid.dta", replace
export delimited "biological_chemical_weapons_proliferation_owid.csv", replace nolabel

describe, replace
keep name varlab
rename name varname
rename varlab varlabel
export delimited "biological_chemical_weapons_proliferation_owid_meta.csv", replace



exit
