*****  This Stata do-file aggregates some of the variables in the Democracy-Index 2022 dataset by the EIU
*****  Author: Bastian Herre
*****  February 1, 2023

version 14
clear all
set more off
set varabbrev off


** Set your own working directories here to run the file:
cd "/Users/bastianherre/Dropbox/Data/"
global project "/Users/bastianherre/Dropbox/Data/"


** Aggregate by year to create world aggregates for sums and averages of regime variables:

* Import data:
use "democracy/datasets/cleaned/eiu_cleaned.dta", replace

* Create indicator variables for specific regime categories:
tabulate regime_eiu, generate(regime_eiu)

* Collapse dataset by year:
collapse (sum) regime_eiu* (mean) democracy_eiu, by(year)
drop regime_eiu

* Create entity identifier:
generate country_name = "World"

* Rename variables:
rename regime_eiu1 number_autreg_eiu
rename regime_eiu2 number_hybreg_eiu
rename regime_eiu3 number_flawdem_eiu
rename regime_eiu4 number_fulldem_eiu

* Temporarily save data:
save "democracy/datasets/final/eiu_aggregated.dta", replace


** Aggregate by year to create world aggregates for population-weighted sums and averages of regime variables:

* Import data:
use "democracy/datasets/cleaned/eiu_cleaned.dta", replace

* Add population data:
merge 1:1 country_name year using "Our World in Data/owid_population_cleaned.dta"
tab country_name if _merge == 1 // No unmerged observations.
drop _merge

* Recode regime classification such that it includes a category for when population data is available, but regime data is missing:
replace regime_eiu = 5 if regime_eiu == . & population_owid != .
label values regime_eiu regime_eiu
label define regime_eiu 5 "no regime data", add
drop if population_owid == .

* Create indicator variables for specific regime categories:
tabulate regime_eiu, generate(regime_eiu)

* Collapse dataset by year:
collapse (sum) regime_eiu* (mean) democracy_eiu [fweight = population_owid], by(year)
drop regime_eiu

* Create entity identifier:
generate country_name = "World"

* Rename variables:
rename regime_eiu1 pop_autreg_eiu
rename regime_eiu2 pop_hybreg_eiu
rename regime_eiu3 pop_flawdem_eiu
rename regime_eiu4 pop_fulldem_eiu
rename regime_eiu5 pop_missreg_eiu

rename democracy_eiu popw_democracy_eiu

* Temporarily save data:
save "democracy/datasets/final/eiu_aggregated_popweighted.dta", replace


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
use "democracy/datasets/cleaned/eiu_cleaned.dta", replace

* Add regional identifiers:
merge m:1 country_name using "Our World in Data/countries_regions_pairs.dta"
tab country_name if _merge == 1
drop if _merge == 2
drop _merge

* Create indicator variables for specific regime categories:
tabulate regime_eiu, generate(regime_eiu)

* Collapse dataset by year:
collapse (sum) regime_eiu* (mean) democracy_eiu, by(year region)
drop regime_eiu

* Create entity identifier:
rename region country_name

* Rename variables:
rename regime_eiu1 number_autreg_eiu
rename regime_eiu2 number_hybreg_eiu
rename regime_eiu3 number_flawdem_eiu
rename regime_eiu4 number_fulldem_eiu

* Temporarily save data:
save "democracy/datasets/final/eiu_aggregated_regions.dta", replace


** Aggregate by year and region to create regional aggregates for population-weighted sums and averages of regime variables:

* Import data:
use "democracy/datasets/cleaned/eiu_cleaned.dta", replace

* Add population data:
merge 1:1 country_name year using "Our World in Data/owid_population_cleaned.dta"
tab country_name if _merge == 1 & year >= 1800 // No unmerged observations.
drop _merge

* Add regional identifiers:
merge m:1 country_name using "Our World in Data/countries_regions_pairs.dta"
drop if _merge == 2
drop _merge

* Recode regime classification such that it includes a category for when population data is available, but regime data is missing:
replace regime_eiu = 5 if regime_eiu == . & population_owid != .
label values regime_eiu regime_eiu
label define regime_eiu 5 "no regime data", add
drop if population_owid == .

* Create indicator variables for specific regime categories:
tabulate regime_eiu, generate(regime_eiu)

* Collapse dataset by year:
collapse (sum) regime_eiu* (mean) democracy_eiu [fweight = population_owid], by(year region)
drop regime_eiu

* Create entity identifier:
rename region country_name

* Rename variables:
rename regime_eiu1 pop_autreg_eiu
rename regime_eiu2 pop_hybreg_eiu
rename regime_eiu3 pop_flawdem_eiu
rename regime_eiu4 pop_fulldem_eiu
rename regime_eiu5 pop_missreg_eiu

rename democracy_eiu popw_democracy_eiu

* Temporarily save data:
save "democracy/datasets/final/eiu_aggregated_popweighted_regions.dta", replace


** Merge different datasets:
use "democracy/datasets/cleaned/eiu_cleaned.dta", replace
merge 1:1 country_name year using "democracy/datasets/final/eiu_aggregated.dta"
drop _merge
merge 1:1 country_name year using "democracy/datasets/final/eiu_aggregated_popweighted.dta"
drop _merge
merge 1:1 country_name year using "democracy/datasets/final/eiu_aggregated_regions.dta"
drop _merge
merge 1:1 country_name year using "democracy/datasets/final/eiu_aggregated_popweighted_regions.dta", update
drop _merge
erase "democracy/datasets/final/eiu_aggregated.dta"
erase "democracy/datasets/final/eiu_aggregated_popweighted.dta"
erase "democracy/datasets/final/eiu_aggregated_regions.dta"
erase "democracy/datasets/final/eiu_aggregated_popweighted_regions.dta"


** Keep years of interest:
keep if year == 2006 | year == 2008 | year >= 2010


** Add regional identifiers to final dataset:
merge m:1 country_name using "Our World in Data/countries_regions_pairs.dta"
tab country_name if _merge == 1
drop if _merge == 2
drop _merge


** Label variables:
label variable number_autreg_eiu "Number of authoritarian regimes (EIU)"
label variable number_hybreg_eiu "Number of hybrid regime (EIU)"
label variable number_flawdem_eiu "Number of flawed democracies (EIU)"
label variable number_fulldem_eiu "Number of full democracies (EIU)"

label variable pop_autreg_eiu "People living in authoritarian regimes (EIU)"
label variable pop_hybreg_eiu "People living in hybrid regimes (EIU)"
label variable pop_flawdem_eiu "People living in flawed democracies (EIU)"
label variable pop_fulldem_eiu "People living in full democracies (EIU)"
* label variable pop_missreg_eiu "People living in countries without regime data (EIU)"

label variable popw_democracy_eiu "Democracy (EIU, population-weighted)"

label variable region "Region"


** Order observations:
sort country_name year


** Export data:
save "democracy/datasets/final/eiu_final.dta", replace
export delimited "democracy/datasets/final/eiu_final.csv", replace nolabel

describe, replace
keep name varlab
rename name varname
rename varlab varlabel
export delimited "democracy/datasets/final/eiu_final_meta.csv", replace


exit
