*****  This Stata do-file aggregates some of the variables in Polity 5 dataset
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
use "democracy/datasets/refined/polity_refined.dta", clear

* Only keep years with comprehensive coverage:
drop if year < 1800 | year > 2018

* Create indicator variables for specific regime categories:
tabulate regime_polity, generate(regime_polity)
tabulate dem_age_group_polity, generate(dem_age_group_polity)

* Collapse dataset by year:
collapse (sum) regime_polity* dem_age_group_polity* (mean) democracy_polity democracy_recod_polity, by(year)
drop regime_polity dem_age_group_polity

* Create entity identifier:
generate country_name = "World"

* Rename variables:
rename regime_polity1 number_aut_polity
rename regime_polity2 number_ano_polity
rename regime_polity3 number_dem_polity

drop dem_age_group_polity1 dem_age_group_polity2
rename dem_age_group_polity3 number_dem_18_polity
rename dem_age_group_polity4 number_dem_30_polity
rename dem_age_group_polity5 number_dem_60_polity
rename dem_age_group_polity6 number_dem_90_polity
rename dem_age_group_polity7 number_dem_91plus_polity

* Temporarily save data:
save "democracy/datasets/final/polity_aggregated.dta", replace


** Aggregate by year to create world aggregates for population-weighted sums and averages of regime variables:

* Import data:
use "democracy/datasets/refined/polity_refined.dta", clear

* Add population data:
merge 1:1 country_name year using "Our World in Data/owid_population_cleaned.dta"
tab country_name if _merge == 1 // Unmerged observations are historical countries (Two Sicilies, East Germany) or current countries without population data (Kosovo).
drop _merge

* Only keep years with comprehensive coverage:
drop if year < 1800 | year > 2018

* Recode regime classification such that it includes a category for when population data is available, but regime data is missing:
replace regime_polity = 3 if regime_polity == . & population_owid != .
label values regime_polity regime_polity
label define regime_polity 3 "no regime data", add
drop if population_owid == .

* Create indicator variables for specific regime categories:
tabulate regime_polity, generate(regime_polity)
tabulate dem_age_group_polity, generate(dem_age_group_polity)

* Collapse dataset by year:
collapse (sum) regime_polity* dem_age_group_polity* (mean) democracy_polity [fweight = population_owid], by(year)
drop regime_polity dem_age_group_polity

* Create entity identifier:
generate country_name = "World"

* Rename variables:
rename regime_polity1 pop_aut_polity
rename regime_polity2 pop_ano_polity
rename regime_polity3 pop_dem_polity
rename regime_polity4 pop_missreg_polity

drop dem_age_group_polity1 dem_age_group_polity2
rename dem_age_group_polity3 pop_dem_18_polity
rename dem_age_group_polity4 pop_dem_30_polity
rename dem_age_group_polity5 pop_dem_60_polity
rename dem_age_group_polity6 pop_dem_90_polity
rename dem_age_group_polity7 pop_dem_91plus_polity

rename democracy_polity popw_democracy_polity

* Temporarily save data:
save "democracy/datasets/final/polity_aggregated_popweighted.dta", replace


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
use "democracy/datasets/refined/polity_refined.dta", clear

* Only keep years with comprehensive coverage:
drop if year < 1800 | year > 2018

* Add regional identifiers:
merge m:1 country_name using "Our World in Data/countries_regions_pairs.dta"
tab country_name if _merge == 1
replace region = "Africa" if country_name == "Orange Free State"
replace region = "Asia" if country_name == "North Vietnam"
replace region = "Europe" if country_name == "Papal States" | country_name == "Sardinia" | country_name == "Prussia"
replace region = "North America" if country_name == "United Province of Canada"
replace region = "South America" if country_name == "Great Colombia"
drop if _merge == 2
drop _merge

* Create indicator variables for specific regime categories:
tabulate regime_polity, generate(regime_polity)
tabulate dem_age_group_polity, generate(dem_age_group_polity)

* Collapse dataset by year:
collapse (sum) regime_polity* dem_age_group_polity* (mean) democracy_polity democracy_recod_polity, by(year region)
drop regime_polity dem_age_group_polity

* Create entity identifier:
rename region country_name

* Rename variables:
rename regime_polity1 number_aut_polity
rename regime_polity2 number_ano_polity
rename regime_polity3 number_dem_polity

drop dem_age_group_polity1 dem_age_group_polity2
rename dem_age_group_polity3 number_dem_18_polity
rename dem_age_group_polity4 number_dem_30_polity
rename dem_age_group_polity5 number_dem_60_polity
rename dem_age_group_polity6 number_dem_90_polity
rename dem_age_group_polity7 number_dem_91plus_polity

* Temporarily save data:
save "democracy/datasets/final/polity_aggregated_regions.dta", replace


** Aggregate by year and region to create regional aggregates for population-weighted sums and averages of regime variables:

* Import data:
use "democracy/datasets/refined/polity_refined.dta", clear

* Add population data:
merge 1:1 country_name year using "Our World in Data/owid_population_cleaned.dta"
tab country_name if _merge == 1 & year >= 1800 // Unmerged observations are historical countries (Two Sicilies, East Germany) or current countries without population data (Kosovo).
drop _merge

* Only keep years with comprehensive coverage:
drop if year < 1800 | year > 2018

* Add regional identifiers:
merge m:1 country_name using "Our World in Data/countries_regions_pairs.dta"
tab country_name if _merge == 1
replace region = "Africa" if country_name == "Orange Free State"
replace region = "Asia" if country_name == "North Vietnam"
replace region = "Europe" if country_name == "Papal States" | country_name == "Sardinia" | country_name == "Prussia"
replace region = "North America" if country_name == "United Province of Canada"
replace region = "South America" if country_name == "Great Colombia"
drop if _merge == 2
drop _merge

* Recode regime classification such that it includes a category for when population data is available, but regime data is missing:
replace regime_polity = 3 if regime_polity == . & population_owid != .
label values regime_polity regime_polity
label define regime_polity 3 "no regime data", add
drop if population_owid == .

* Create indicator variables for specific regime categories:
tabulate regime_polity, generate(regime_polity)
tabulate dem_age_group_polity, generate(dem_age_group_polity)

* Collapse dataset by year:
collapse (sum) regime_polity* dem_age_group_polity* (mean) democracy_polity [fweight = population_owid], by(year region)
drop regime_polity dem_age_group_polity

* Create entity identifier:
rename region country_name

* Rename variables:
rename regime_polity1 pop_aut_polity
rename regime_polity2 pop_ano_polity
rename regime_polity3 pop_dem_polity
rename regime_polity4 pop_missreg_polity

drop dem_age_group_polity1 dem_age_group_polity2
rename dem_age_group_polity3 pop_dem_18_polity
rename dem_age_group_polity4 pop_dem_30_polity
rename dem_age_group_polity5 pop_dem_60_polity
rename dem_age_group_polity6 pop_dem_90_polity
rename dem_age_group_polity7 pop_dem_91plus_polity

rename democracy_polity popw_democracy_polity

* Temporarily save data:
save "democracy/datasets/final/polity_aggregated_popweighted_regions.dta", replace


** Merge different datasets:
use "democracy/datasets/refined/polity_refined.dta"
merge 1:1 country_name year using "democracy/datasets/final/polity_aggregated.dta"
drop _merge
merge 1:1 country_name year using "democracy/datasets/final/polity_aggregated_popweighted.dta"
drop _merge
merge 1:1 country_name year using "democracy/datasets/final/polity_aggregated_regions.dta"
drop _merge
merge 1:1 country_name year using "democracy/datasets/final/polity_aggregated_popweighted_regions.dta", update
drop _merge
erase "democracy/datasets/final/polity_aggregated.dta"
erase "democracy/datasets/final/polity_aggregated_popweighted.dta"
erase "democracy/datasets/final/polity_aggregated_regions.dta"
erase "democracy/datasets/final/polity_aggregated_popweighted_regions.dta"


** Add regional identifiers to final dataset:
merge m:1 country_name using "Our World in Data/countries_regions_pairs.dta"
tab country_name if _merge == 1
replace region = "Africa" if country_name == "Orange Free State"
replace region = "Asia" if country_name == "North Vietnam"
replace region = "Europe" if country_name == "Papal States" | country_name == "Sardinia" | country_name == "Prussia"
replace region = "North America" if country_name == "United Province of Canada"
replace region = "South America" if country_name == "Great Colombia"
drop if _merge == 2
drop _merge


** Label variables:
label variable number_aut_polity "Number of autocracies (Polity)"
label variable number_ano_polity "Number of anocracies (Polity)"
label variable number_dem_polity "Number of democracies (Polity)"

label variable pop_aut_polity "People living in autocracies (Polity)"
label variable pop_ano_polity "People living in anocracies (Polity)"
label variable pop_dem_polity "People living in democracies (Polity)"
label variable pop_missreg_polity "People living in countries without regime data (Polity)"

label variable number_dem_18_polity "Number of democracies aged 1-18 years (Polity)"
label variable number_dem_30_polity "Number of democracies aged 19-30 years (Polity)"
label variable number_dem_60_polity "Number of democracies aged 31-60 years (Polity)"
label variable number_dem_90_polity "Number of democracies aged 61-90 years (Polity)"
label variable number_dem_91plus_polity "Number of democracies aged 91 years or older (Polity)"

label variable pop_dem_18_polity "People living in democracies aged 1-18 years (Polity)"
label variable pop_dem_30_polity "People living in democracies aged 19-30 years (Polity)"
label variable pop_dem_60_polity "People living in democracies aged 31-60 years (Polity)"
label variable pop_dem_90_polity "People living in democracies aged 61-90 years (Polity)"
label variable pop_dem_91plus_polity "People living in democracies aged 91 years or older (Polity)"

label variable popw_democracy_polity "Democracy (Polity, population-weighted)"

label variable region "Region"


** Order observations:
sort country_name year


** Export data:
save "democracy/datasets/final/polity_final.dta", replace
export delimited "democracy/datasets/final/polity_final.csv", replace nolabel

describe, replace
keep name varlab
rename name varname
rename varlab varlabel
export delimited "democracy/datasets/final/polity_final_meta.csv", replace


exit
