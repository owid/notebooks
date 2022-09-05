*****  This Stata do-file aggregates some of the variables in the Episodes of Regime Transformation (ERT) dataset
*****  Author: Bastian Herre
*****  August 31, 2022

version 14
clear all
set more off
set varabbrev off


** Set your own working directories here to run the file:
cd "/Users/bastianherre/Dropbox/Data/"
global project "/Users/bastianherre/Dropbox/Data/"


** Aggregate by year to create world aggregates for sums of regime variables:

* Import data:
use "democracy/datasets/cleaned/ert_cleaned.dta", clear

* Create indicator variables for specific regime categories:
tabulate regime_ert, generate(regime_ert)
tabulate regime_trich_ert, generate(regime_trich_ert)

* Collapse dataset by year:
collapse (sum) regime_ert* regime_trich_ert*, by(year)
drop regime_ert regime_trich_ert

* Create entity identifier:
generate country_name = "World"

* Rename variables:
rename regime_ert1 number_hardaut_ert
rename regime_ert2 number_staut_ert
rename regime_ert3 number_libaut_ert
rename regime_ert4 number_erodem_ert
rename regime_ert5 number_stdem_ert
rename regime_ert6 number_deepdem_ert

rename regime_trich_ert1 number_autreg_ert
rename regime_trich_ert2 number_streg_ert
rename regime_trich_ert3 number_demreg_ert


* Temporarily save data:
save "democracy/datasets/final/ert_aggregated.dta", replace


** Aggregate by year to create world aggregates for population-weighted sums of regime variables:

* Import data:
use "democracy/datasets/cleaned/ert_cleaned.dta", clear

* Add population data:
merge 1:1 country_name year using "Our World in Data/owid_population_cleaned.dta"
tab country_name if _merge == 1 & year >= 1900 // Unmerged observations in master datasets either before 1900, historical countries (Republic of Vietnam, East Germany) or current countries without population data (Kosovo, Palestine/Gaza, Palestine/West Bank, Somaliland).
drop _merge

* Recode regime classification such that it includes a category for when population data is available, but regime data is missing:
replace regime_ert = 6 if regime_ert == . & population_owid != .
label values regime_ert regime_ert
label define regime_ert 6 "no regime data", add

* Create indicator variables for specific regime categories:
tabulate regime_ert, generate(regime_ert)
tabulate regime_trich_ert, generate(regime_trich_ert)

* Collapse dataset by year:
collapse (sum) regime_ert* regime_trich_ert* [fweight = population_owid], by(year)
drop regime_ert regime_trich_ert

* Create entity identifier:
generate country_name = "World"

* Rename variables:
rename regime_ert1 pop_hardaut_ert
rename regime_ert2 pop_staut_ert
rename regime_ert3 pop_libaut_ert
rename regime_ert4 pop_erodem_ert
rename regime_ert5 pop_stdem_ert
rename regime_ert6 pop_deepdem_ert
rename regime_ert7 pop_missreg_ert

rename regime_trich_ert1 pop_autreg_ert
rename regime_trich_ert2 pop_streg_ert
rename regime_trich_ert3 pop_demreg_ert

* Temporarily save data:
save "democracy/datasets/final/ert_aggregated_popweighted.dta", replace


** Aggregate by year and region to create regional aggregates for sums of regime variables:

* Prepare regional identifiers:
import delimited "Our World in Data/countries_regions_pairs.csv", clear varnames(1)
rename country country_name

* Keep regional identifiers of interest:
tab region
drop if region == "Antarctica"
duplicates tag country_name, generate(duplicate)
list if duplicate == 1
drop if region == "European Union (27)"
duplicates drop // Northern Cyprus still listed twice.
drop duplicate

save "Our World in Data/countries_regions_pairs.dta", replace

* Import data:
use "democracy/datasets/cleaned/ert_cleaned.dta", clear

* Add regional identifiers:
merge m:1 country_name using "Our World in Data/countries_regions_pairs.dta"
tab country_name if _merge == 1
replace region = "Europe" if country_name == "Brunswick" | country_name == "Hamburg" | country_name == "Nassau" | country_name == "Oldenburg" | country_name == "Papal States" | country_name == "Piedmont-Sardinia" | country_name == "Saxe-Weimar-Eisenach"
replace region = "Asia" if country_name == "Palestine/Gaza" | country_name == "Palestine/West Bank"
drop if _merge == 2
drop _merge

* Create indicator variables for specific regime categories:
tabulate regime_ert, generate(regime_ert)
tabulate regime_trich_ert, generate(regime_trich_ert)

* Collapse dataset by year:
collapse (sum) regime_ert* regime_trich_ert*, by(year region)
drop regime_ert regime_trich_ert

* Create entity identifier:
rename region country_name

* Rename variables:
rename regime_ert1 number_hardaut_ert
rename regime_ert2 number_staut_ert
rename regime_ert3 number_libaut_ert
rename regime_ert4 number_erodem_ert
rename regime_ert5 number_stdem_ert
rename regime_ert6 number_deepdem_ert

rename regime_trich_ert1 number_autreg_ert
rename regime_trich_ert2 number_streg_ert
rename regime_trich_ert3 number_demreg_ert

* Temporarily save data:
save "democracy/datasets/final/ert_aggregated_regions.dta", replace


** Aggregate by year and region to create regional aggregates for population-weighted sums of regime variables:

* Import data:
use "democracy/datasets/cleaned/ert_cleaned.dta", clear

* Add population data:
merge 1:1 country_name year using "Our World in Data/owid_population_cleaned.dta"
tab country_name if _merge == 1 & year >= 1900 // Unmerged observations in master datasets either before 1900, historical countries (Republic of Vietnam, East Germany) or current countries without population data (Kosovo, Palestine/Gaza, Palestine/West Bank, Somaliland).
drop _merge

* Add regional identifiers:
merge m:1 country_name using "Our World in Data/countries_regions_pairs.dta"
tab country_name if _merge == 1
replace region = "Europe" if country_name == "Brunswick" | country_name == "Hamburg" | country_name == "Nassau" | country_name == "Oldenburg" | country_name == "Papal States" | country_name == "Piedmont-Sardinia" | country_name == "Saxe-Weimar-Eisenach"
replace region = "Asia" if country_name == "Palestine/Gaza" | country_name == "Palestine/West Bank"
drop if _merge == 2
drop _merge

* Recode regime classification such that it includes a category for when population data is available, but regime data is missing:
replace regime_ert = 6 if regime_ert == . & population_owid != .
label values regime_ert regime_ert
label define regime_ert 6 "no regime data", add

* Create indicator variables for specific regime categories:
tabulate regime_ert, generate(regime_ert)
tabulate regime_trich_ert, generate(regime_trich_ert)

* Collapse dataset by year:
collapse (sum) regime_ert* regime_trich_ert* [fweight = population_owid], by(year region)
drop regime_ert regime_trich_ert

* Create entity identifier:
rename region country_name

* Rename variables:
rename regime_ert1 pop_hardaut_ert
rename regime_ert2 pop_staut_ert
rename regime_ert3 pop_libaut_ert
rename regime_ert4 pop_erodem_ert
rename regime_ert5 pop_stdem_ert
rename regime_ert6 pop_deepdem_ert
rename regime_ert7 pop_missreg_ert

rename regime_trich_ert1 pop_autreg_ert
rename regime_trich_ert2 pop_streg_ert
rename regime_trich_ert3 pop_demreg_ert

* Temporarily save data:
save "democracy/datasets/final/ert_aggregated_popweighted_regions.dta", replace


** Merge different datasets:
use "democracy/datasets/cleaned/ert_cleaned.dta"
merge 1:1 country_name year using "democracy/datasets/final/ert_aggregated.dta"
drop _merge
merge 1:1 country_name year using "democracy/datasets/final/ert_aggregated_popweighted.dta"
drop _merge
merge 1:1 country_name year using "democracy/datasets/final/ert_aggregated_regions.dta"
drop _merge
merge 1:1 country_name year using "democracy/datasets/final/ert_aggregated_popweighted_regions.dta", update
drop _merge
erase "democracy/datasets/final/ert_aggregated.dta"
erase "democracy/datasets/final/ert_aggregated_popweighted.dta"
erase "democracy/datasets/final/ert_aggregated_regions.dta"
erase "democracy/datasets/final/ert_aggregated_popweighted_regions.dta"


** Add regional identifiers to final dataset:
merge m:1 country_name using "Our World in Data/countries_regions_pairs.dta"
tab country_name if _merge == 1
replace region = "Europe" if country_name == "Brunswick" | country_name == "Hamburg" | country_name == "Nassau" | country_name == "Oldenburg" | country_name == "Papal States" | country_name == "Piedmont-Sardinia" | country_name == "Saxe-Weimar-Eisenach"
replace region = "Asia" if country_name == "Palestine/Gaza" | country_name == "Palestine/West Bank"
replace region = "World" if country_name == "World"
drop if _merge == 2
drop _merge


** Label variables:
label variable number_hardaut_ert "Number of hardening autocracies (ERT)"
label variable number_staut_ert "Number of stable autocracies (ERT)"
label variable number_libaut_ert "Number of liberalizing autocracies (ERT)"
label variable number_erodem_ert "Number of eroding democracies (ERT)"
label variable number_stdem_ert "Number of stable democracies (ERT)"
label variable number_deepdem_ert "Number of deepening democracies (ERT)"

label variable number_autreg_ert "Number of autocratizing regimes (ERT)"
label variable number_streg_ert "Number of stable regimes (ERT)"
label variable number_demreg_ert "Number of democratizing regimes (ERT)"

label variable pop_hardaut_ert "People living in hardening autocracies (ERT)"
label variable pop_staut_ert "People living in stable autocracies (ERT)"
label variable pop_libaut_ert "People living in liberalizing autocracies (ERT)"
label variable pop_erodem_ert "People living in eroding democracies (ERT)"
label variable pop_stdem_ert "People living in stable democracies (ERT)"
label variable pop_deepdem_ert "People living in deepening democracies (ERT)"
label variable pop_missreg_ert "People living in countries without regime data (ERT)"

label variable pop_autreg_ert "People living in autocratizing regimes (ERT)"
label variable pop_streg_ert "People living in stable regimes (ERT)"
label variable pop_demreg_ert "People living in democratizing regimes (ERT)"

label variable region "Region"


** Keep observations of interest:
drop if year < 1900


** Order observations:
sort country_name year


** Export data:
save "democracy/datasets/final/ert_final.dta", replace
export delimited "democracy/datasets/final/ert_final.csv", replace nolabel

describe, replace
keep name varlab
rename name varname
rename varlab varlabel
export delimited "democracy/datasets/final/ert_final_meta.csv", replace


exit
