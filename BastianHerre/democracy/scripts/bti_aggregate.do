*****  This Stata do-file aggregates some of the variables in 2022 democracy dataset by the BTI
*****  Author: Bastian Herre
*****  June 28, 2022

version 14
clear all
set more off
set varabbrev off


** Set your own working directories here to run the file:
cd "/Users/bastianherre/Dropbox/Data/"
global project "/Users/bastianherre/Dropbox/Data/"


** Aggregate by year to create world aggregates for sums and averages of regime variables:

* Import data:
use "democracy/datasets/cleaned/bti_cleaned.dta", clear

* Create indicator variables for specific regime categories:
tabulate regime_bti, generate(regime_bti)

* Collapse dataset by year:
collapse (sum) regime_bti* (mean) democracy_bti, by(year)
drop regime_bti

* Create entity identifier:
generate country_name = "World"

* Rename variables:
rename regime_bti1 number_hardaut_bti
rename regime_bti2 number_modaut_bti
rename regime_bti3 number_hdefdem_bti
rename regime_bti4 number_defdem_bti
rename regime_bti5 number_consdem_bti

* Temporarily save data:
save "democracy/datasets/final/bti_aggregated.dta", replace


** Aggregate by year to create world aggregates for population-weighted sums and averages of regime variables:

* Import data:
use "democracy/datasets/cleaned/bti_cleaned.dta", clear

* Add population data:
merge 1:1 country_name year using "Our World in Data/owid_population_cleaned.dta"
tab country_name if _merge == 1 // Unmerged observations is a country without population data (Kosovo).
drop _merge

* Recode regime classification such that it includes a category for when population data is available, but regime data is missing:
replace regime_bti = 6 if regime_bti == . & population_owid != .
label values regime_bti regime_bti
label define regime_bti 6 "no regime data", add
drop if population_owid == .

* Create indicator variables for specific regime categories:
tabulate regime_bti, generate(regime_bti)

* Collapse dataset by year:
collapse (sum) regime_bti* (mean) democracy_bti [fweight = population_owid], by(year)
drop regime_bti

* Create entity identifier:
generate country_name = "World"

* Rename variables:
rename regime_bti1 pop_hardaut_bti
rename regime_bti2 pop_modaut_bti
rename regime_bti3 pop_hdefdem_bti
rename regime_bti4 pop_defdem_bti
rename regime_bti5 pop_consdem_bti
rename regime_bti6 pop_missreg_bti

rename democracy_bti popw_democracy_bti

* Temporarily save data:
save "democracy/datasets/final/bti_aggregated_popweighted.dta", replace


** Aggregate by year and region to create regional aggregates for sums and averages of regime variables:

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
use "democracy/datasets/cleaned/bti_cleaned.dta", clear

* Add regional identifiers:
merge m:1 country_name using "Our World in Data/countries_regions_pairs.dta"
tab country_name if _merge == 1
drop if _merge == 2
drop _merge

* Create indicator variables for specific regime categories:
tabulate regime_bti, generate(regime_bti)

* Collapse dataset by year:
collapse (sum) regime_bti* (mean) democracy_bti, by(year region)
drop regime_bti

* Create entity identifier:
rename region country_name

* Rename variables:
rename regime_bti1 number_hardaut_bti
rename regime_bti2 number_modaut_bti
rename regime_bti3 number_hdefdem_bti
rename regime_bti4 number_defdem_bti
rename regime_bti5 number_consdem_bti

* Temporarily save data:
save "democracy/datasets/final/bti_aggregated_regions.dta", replace


** Aggregate by year and region to create regional aggregates for population-weighted sums and averages of regime variables:

* Import data:
use "democracy/datasets/cleaned/bti_cleaned.dta", clear

* Add population data:
merge 1:1 country_name year using "Our World in Data/owid_population_cleaned.dta"
tab country_name if _merge == 1 & year >= 1800 // Unmerged observations is a country without population data (Kosovo).
drop _merge

* Add regional identifiers:
merge m:1 country_name using "Our World in Data/countries_regions_pairs.dta"
drop if _merge == 2
drop _merge

* Recode regime classification such that it includes a category for when population data is available, but regime data is missing:
replace regime_bti = 6 if regime_bti == . & population_owid != .
label values regime_bti regime_bti
label define regime_bti 6 "no regime data", add
drop if population_owid == .

* Create indicator variables for specific regime categories:
tabulate regime_bti, generate(regime_bti)

* Collapse dataset by year:
collapse (sum) regime_bti* (mean) democracy_bti [fweight = population_owid], by(year region)
drop regime_bti

* Create entity identifier:
rename region country_name

* Rename variables:
rename regime_bti1 pop_hardaut_bti
rename regime_bti2 pop_modaut_bti
rename regime_bti3 pop_hdefdem_bti
rename regime_bti4 pop_defdem_bti
rename regime_bti5 pop_consdem_bti
rename regime_bti6 pop_missreg_bti

rename democracy_bti popw_democracy_bti

* Temporarily save data:
save "democracy/datasets/final/bti_aggregated_popweighted_regions.dta", replace


** Merge different datasets:
use "democracy/datasets/cleaned/bti_cleaned.dta"
merge 1:1 country_name year using "democracy/datasets/final/bti_aggregated.dta"
drop _merge
merge 1:1 country_name year using "democracy/datasets/final/bti_aggregated_popweighted.dta"
drop _merge
merge 1:1 country_name year using "democracy/datasets/final/bti_aggregated_regions.dta"
drop _merge
merge 1:1 country_name year using "democracy/datasets/final/bti_aggregated_popweighted_regions.dta", update
drop _merge
erase "democracy/datasets/final/bti_aggregated.dta"
erase "democracy/datasets/final/bti_aggregated_popweighted.dta"
erase "democracy/datasets/final/bti_aggregated_regions.dta"
erase "democracy/datasets/final/bti_aggregated_popweighted_regions.dta"


** Keep years of interest:
keep if year == 2005 | year == 2007 | year == 2009 | year == 2011 | year == 2013 | year == 2015 | year == 2017 | year == 2019 | year == 2021


** Add regional identifiers to final dataset:
merge m:1 country_name using "Our World in Data/countries_regions_pairs.dta"
tab country_name if _merge == 1
drop if _merge == 2
drop _merge


** Label variables:
label variable number_hardaut_bti "Number of hard autocracies (BTI)"
label variable number_modaut_bti "Number of moderate autocracies (BTI)"
label variable number_hdefdem_bti "Number of highly defective democracies (BTI)"
label variable number_defdem_bti "Number of defective democracies (BTI)"
label variable number_consdem_bti "Number of consolidating democracies (BTI)"

label variable pop_hardaut_bti "People living in hard autocracies (BTI)"
label variable pop_modaut_bti "People living in moderate autocracies (BTI)"
label variable pop_hdefdem_bti "People living in highly defective democracies (BTI)"
label variable pop_defdem_bti "People living in defective democracies (BTI)"
label variable pop_consdem_bti "People living in consolidating democracies (BTI)"
label variable pop_missreg_bti "People living in countries without regime data (BTI)"

label variable popw_democracy_bti "Democracy score (BTI, population-weighted)"

label variable region "Region"


** Order observations:
sort country_name year


** Export data:
save "democracy/datasets/final/bti_final.dta", replace
export delimited "democracy/datasets/final/bti_final.csv", replace nolabel

describe, replace
keep name varlab
rename name varname
rename varlab varlabel
export delimited "democracy/datasets/final/bti_final_meta.csv", replace


exit
