*****  This Stata do-file aggregates some of the variables in the Freedom-of-the-World dataset
*****  Author: Bastian Herre
*****  June 28, 2022

version 14
clear all
set more off
set varabbrev off


** Set your own working directories here to run the file:
cd "/Users/bastianherre/Dropbox/Data/"
global project "/Users/bastianherre/Dropbox/Data/"


** Aggregate by year to create world aggregates for sums of regime variables:

* Import data:
use "democracy/datasets/cleaned/fh_cleaned.dta", clear

* Create indicator variables for specific regime categories:
tabulate regime_fh, generate(regime_fh)
tabulate electdem_fh, generate(electdem_fh)

* Collapse dataset by year:
collapse (sum) regime_fh* electdem_fh*, by(year)
drop regime_fh electdem_fh

* Create entity identifier:
generate country_name = "World"

* Rename variables:
rename regime_fh1 number_notfree_fh
rename regime_fh2 number_partlyfree_fh
rename regime_fh3 number_free_fh

rename electdem_fh1 number_nonelectdem_fh
rename electdem_fh2 number_electdem_fh

* Temporarily save data:
save "democracy/datasets/final/fh_aggregated.dta", replace


** Aggregate by year to create world aggregates for population-weighted sums of regime variables:

* Import data:
use "democracy/datasets/cleaned/fh_cleaned.dta", clear

* Add population data:
merge 1:1 country_name year using "Our World in Data/owid_population_cleaned.dta"
tab country_name if _merge == 1 // Unmerged observations are historical countries (e.g. Czechoslovakia, East Germany) or current countries without population data (e.g. Israeli-Occupied Territories, Kosovo).
drop _merge

* Recode regime classification such that it includes a category for when population data is available, but regime data is missing:
replace regime_fh = 3 if regime_fh == . & population_owid != .
label values regime_fh regime_fh
label define regime_fh 3 "no regime data", add

replace electdem_fh = 2 if electdem_fh == . & population_owid != .
label values electdem_fh electdem_fh
label define electdem_fh 2 "no regime data", add

drop if population_owid == .

* Create indicator variables for specific regime categories:
tabulate regime_fh, generate(regime_fh)
tabulate electdem_fh, generate(electdem_fh)

* Collapse dataset by year:
collapse (sum) regime_fh* electdem_fh* [fweight = population_owid], by(year)
drop regime_fh electdem_fh

* Create entity identifier:
generate country_name = "World"

* Rename variables:
rename regime_fh1 pop_notfree_fh
rename regime_fh2 pop_partlyfree_fh
rename regime_fh3 pop_free_fh
rename regime_fh4 pop_missreg_fh

rename electdem_fh1 pop_nonelectdem_fh
rename electdem_fh2 pop_electdem_fh
rename electdem_fh3 pop_missdem_fh

* Temporarily save data:
save "democracy/datasets/final/fh_aggregated_popweighted.dta", replace


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
use "democracy/datasets/cleaned/fh_cleaned.dta", clear

* Add regional identifiers:
merge m:1 country_name using "Our World in Data/countries_regions_pairs.dta"
tab country_name if _merge == 1
replace region = "Asia" if country_name == "Chechnya" | country_name == "Gaza Strip" | country_name == "Indian Kashmir" | country_name == "Israeli-Occupied Territories" | country_name == "Kurdistan" | country_name == "North Vietnam" | country_name == "Pakistani Kashmir" | country_name == "Palestinian Authority-Administered Territories" | country_name == "Tibet" | country_name == "West Bank" | country_name == "West Bank and Gaza Strip" | country_name == "West Papua"
replace region = "Europe" if country_name == "Crimea" | country_name == "Eastern Donbas" | country_name == "Northern Ireland"
drop if _merge == 2
drop _merge

* Create indicator variables for specific regime categories:
tabulate regime_fh, generate(regime_fh)
tabulate electdem_fh, generate(electdem_fh)

* Collapse dataset by year:
collapse (sum) regime_fh* electdem_fh*, by(year region)
drop regime_fh electdem_fh

* Create entity identifier:
rename region country_name

* Rename variables:
rename regime_fh1 number_notfree_fh
rename regime_fh2 number_partlyfree_fh
rename regime_fh3 number_free_fh

rename electdem_fh1 number_nonelectdem_fh
rename electdem_fh2 number_electdem_fh

* Temporarily save data:
save "democracy/datasets/final/fh_aggregated_regions.dta", replace


** Aggregate by year and region to create regional aggregates for population-weighted sums of regime variables:

* Import data:
use "democracy/datasets/cleaned/fh_cleaned.dta", clear

* Add population data:
merge 1:1 country_name year using "Our World in Data/owid_population_cleaned.dta"
tab country_name if _merge == 1 // Unmerged observations are historical countries (e.g. Czechoslovakia, East Germany) or current countries without population data (e.g. Israeli-Occupied Territories, Kosovo).
drop _merge

* Add regional identifiers:
merge m:1 country_name using "Our World in Data/countries_regions_pairs.dta"
tab country_name if _merge == 1
replace region = "Asia" if country_name == "Chechnya" | country_name == "Gaza Strip" | country_name == "Indian Kashmir" | country_name == "Israeli-Occupied Territories" | country_name == "Kurdistan" | country_name == "North Vietnam" | country_name == "Pakistani Kashmir" | country_name == "Palestinian Authority-Administered Territories" | country_name == "Tibet" | country_name == "West Bank" | country_name == "West Bank and Gaza Strip" | country_name == "West Papua"
replace region = "Europe" if country_name == "Crimea" | country_name == "Eastern Donbas" | country_name == "Northern Ireland"
drop if _merge == 2
drop _merge

* Recode regime classification such that it includes a category for when population data is available, but regime data is missing:
replace regime_fh = 3 if regime_fh == . & population_owid != .
label values regime_fh regime_fh
label define regime_fh 3 "no regime data", add

replace electdem_fh = 2 if electdem_fh == . & population_owid != .
label values electdem_fh electdem_fh
label define electdem_fh 2 "no regime data", add

drop if population_owid == .

* Create indicator variables for specific regime categories:
tabulate regime_fh, generate(regime_fh)
tabulate electdem_fh, generate(electdem_fh)

* Collapse dataset by year:
collapse (sum) regime_fh* electdem_fh* [fweight = population_owid], by(year region)
drop regime_fh electdem_fh

* Create entity identifier:
rename region country_name

* Rename variables:
rename regime_fh1 pop_notfree_fh
rename regime_fh2 pop_partlyfree_fh
rename regime_fh3 pop_free_fh
rename regime_fh4 pop_missreg_fh

rename electdem_fh1 pop_nonelectdem_fh
rename electdem_fh2 pop_electdem_fh
rename electdem_fh3 pop_missdem_fh

* Temporarily save data:
save "democracy/datasets/final/fh_aggregated_popweighted_regions.dta", replace


** Merge different datasets:
use "democracy/datasets/cleaned/fh_cleaned.dta"
merge 1:1 country_name year using "democracy/datasets/final/fh_aggregated.dta"
drop _merge
merge 1:1 country_name year using "democracy/datasets/final/fh_aggregated_popweighted.dta"
drop _merge
merge 1:1 country_name year using "democracy/datasets/final/fh_aggregated_regions.dta"
drop _merge
merge 1:1 country_name year using "democracy/datasets/final/fh_aggregated_popweighted_regions.dta", update
drop _merge
erase "democracy/datasets/final/fh_aggregated.dta"
erase "democracy/datasets/final/fh_aggregated_popweighted.dta"
erase "democracy/datasets/final/fh_aggregated_regions.dta"
erase "democracy/datasets/final/fh_aggregated_popweighted_regions.dta"


** Add regional identifiers to final dataset:
merge m:1 country_name using "Our World in Data/countries_regions_pairs.dta"
tab country_name if _merge == 1
replace region = "Asia" if country_name == "Chechnya" | country_name == "Gaza Strip" | country_name == "Indian Kashmir" | country_name == "Israeli-Occupied Territories" | country_name == "Kurdistan" | country_name == "North Vietnam" | country_name == "Pakistani Kashmir" | country_name == "Palestinian Authority-Administered Territories" | country_name == "Tibet" | country_name == "West Bank" | country_name == "West Bank and Gaza Strip" | country_name == "West Papua"
replace region = "Europe" if country_name == "Crimea" | country_name == "Eastern Donbas" | country_name == "Northern Ireland"
drop if _merge == 2
drop _merge


** Label variables:
label variable number_notfree_fh "Number of not-free countries (Freedom House)"
label variable number_partlyfree_fh "Number of partly-free countries (Freedom House)"
label variable number_free_fh "Number of free countries (Freedom House)"

label variable pop_notfree_fh "People living in not-free countries (Freedom House)"
label variable pop_partlyfree_fh "People living in partly-free countries (Freedom House)"
label variable pop_free_fh "People living in free countries (Freedom House)"
label variable pop_missreg_fh "People living in countries without regime data (Freedom House)"

label variable number_nonelectdem_fh "Number of not-electoral democracies (Freedom House)"
label variable number_electdem_fh "Number of electoral democracies (Freedom House)"

label variable pop_nonelectdem_fh "People living in not-electoral democracies (Freedom House)"
label variable pop_electdem_fh "People living in not-electoral democracies (Freedom House)"
label variable pop_missdem_fh "People living in countries without democracy data (Freedom House)"

label variable region "Region"


** Clear variables before they are included:
replace number_electdem_fh = . if year < 2005
replace number_nonelectdem_fh = . if year < 2005

replace pop_missdem_fh = . if year < 2005
replace pop_electdem_fh = . if year < 2005
replace pop_nonelectdem_fh = . if year < 2005

replace pop_missreg_fh = . if year < 1972 | year == 1981
replace pop_notfree_fh = . if year < 1972 | year == 1981
replace pop_partlyfree_fh = . if year < 1972 | year == 1981
replace pop_free_fh = . if year < 1972 | year == 1981


** Order observations:
sort country_name year


** Export data:
save "democracy/datasets/final/fh_final.dta", replace
export delimited "democracy/datasets/final/fh_final.csv", replace nolabel

describe, replace
keep name varlab
rename name varname
rename varlab varlabel
export delimited "democracy/datasets/final/fh_final_meta.csv", replace


exit
