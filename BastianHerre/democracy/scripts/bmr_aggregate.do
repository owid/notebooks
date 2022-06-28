*****  This Stata do-file aggregates some of the variables in the BMR dataset
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
use "democracy/datasets/refined/bmr_refined.dta", clear

* Only aggregate countries without imputed values:
replace regime_bmr_owid = . if regime_imputed_bmr_owid == 1
replace regime_womsuffr_bmr_owid = . if regime_imputed_bmr_owid == 1
replace dem_age_group_bmr_owid = . if regime_imputed_bmr_owid == 1
replace dem_ws_age_group_bmr_owid = . if regime_imputed_bmr_owid == 1

* Create indicator variables for specific regime categories:
tabulate regime_bmr_owid, generate(regime_bmr_owid)
tabulate regime_womsuffr_bmr_owid, generate(regime_womsuffr_bmr_owid)
tabulate dem_age_group_bmr_owid, generate(dem_age_group_bmr_owid)
tabulate dem_ws_age_group_bmr_owid, generate(dem_ws_age_group_bmr_owid)

* Collapse dataset by year:
collapse (sum) regime_bmr_owid* regime_womsuffr_bmr_owid* dem_age_group_bmr_owid* dem_ws_age_group_bmr_owid*, by(year)
drop regime_bmr_owid regime_womsuffr_bmr_owid dem_age_group_bmr_owid dem_ws_age_group_bmr_owid

* Create entity identifier:
generate country_name = "World"

* Rename variables:
rename regime_bmr_owid1 number_nondem_bmr_owid
rename regime_bmr_owid2 number_dem_bmr_owid

rename regime_womsuffr_bmr_owid1 number_nondem_womsuffr_bmr_owid
rename regime_womsuffr_bmr_owid2 number_dem_womsuffr_bmr_owid

drop dem_age_group_bmr_owid1
rename dem_age_group_bmr_owid2 number_dem_18_bmr_owid
rename dem_age_group_bmr_owid3 number_dem_30_bmr_owid
rename dem_age_group_bmr_owid4 number_dem_60_bmr_owid
rename dem_age_group_bmr_owid5 number_dem_90_bmr_owid
rename dem_age_group_bmr_owid6 number_dem_91plus_bmr_owid

drop dem_ws_age_group_bmr_owid1
rename dem_ws_age_group_bmr_owid2 number_dem_ws_18_bmr_owid
rename dem_ws_age_group_bmr_owid3 number_dem_ws_30_bmr_owid
rename dem_ws_age_group_bmr_owid4 number_dem_ws_60_bmr_owid
rename dem_ws_age_group_bmr_owid5 number_dem_ws_90_bmr_owid
rename dem_ws_age_group_bmr_owid6 number_dem_ws_91plus_bmr_owid

* Temporarily save data:
save "democracy/datasets/final/bmr_aggregated.dta", replace


** Aggregate by year to create world aggregates for population-weighted sums of regime variables:

* Import data:
use "democracy/datasets/refined/bmr_refined.dta", clear

* Add population data:
merge 1:1 country_name year using "Our World in Data/owid_population_cleaned.dta"
tab country_name if _merge == 1 & year >= 1800 // Unmerged observations in master datasets either before 1800, historical countries (East Germany, Soviet Union) or current countries without population data (Kosovo).
drop _merge
drop if year == 2021

* Recode regime classification such that it includes a category for when population data is available, but regime data is missing:
replace regime_bmr_owid = 2 if regime_bmr_owid == . & population_owid != .
label values regime_bmr_owid regime_bmr_owid
label define regime_bmr_owid 0 "nondemocracy" 1 "democracy" 2 "no regime data", add
drop if population_owid == .

replace regime_womsuffr_bmr_owid = 2 if regime_womsuffr_bmr_owid == . & population_owid != .
label values regime_womsuffr_bmr_owid regime_bmr_owid

* Here, I also aggregate countries with imputed values — because people matter here, not countries.

* Create indicator variables for specific regime categories:
tabulate regime_bmr_owid, generate(regime_bmr_owid)
tabulate regime_womsuffr_bmr_owid, generate(regime_womsuffr_bmr_owid)
tabulate dem_age_group_bmr_owid, generate(dem_age_group_bmr_owid)
tabulate dem_ws_age_group_bmr_owid, generate(dem_ws_age_group_bmr_owid)

* Collapse dataset by year:
collapse (sum) regime_bmr_owid* regime_womsuffr_bmr_owid* dem_age_group_bmr_owid* dem_ws_age_group_bmr_owid* [fweight = population_owid], by(year)
drop regime_bmr_owid regime_womsuffr_bmr_owid dem_age_group_bmr_owid dem_ws_age_group_bmr_owid

* Create entity identifier:
generate country_name = "World"

* Rename variables:
rename regime_bmr_owid1 pop_nondem_bmr_owid
rename regime_bmr_owid2 pop_dem_bmr_owid
rename regime_bmr_owid3 pop_missreg_bmr_owid

drop regime_womsuffr_bmr_owid3
rename regime_womsuffr_bmr_owid1 pop_nondem_womsuffr_bmr_owid
rename regime_womsuffr_bmr_owid2 pop_dem_womsuffr_bmr_owid

drop dem_age_group_bmr_owid1
rename dem_age_group_bmr_owid2 pop_dem_18_bmr_owid
rename dem_age_group_bmr_owid3 pop_dem_30_bmr_owid
rename dem_age_group_bmr_owid4 pop_dem_60_bmr_owid
rename dem_age_group_bmr_owid5 pop_dem_90_bmr_owid
rename dem_age_group_bmr_owid6 pop_dem_91plus_bmr_owid

drop dem_ws_age_group_bmr_owid1
rename dem_ws_age_group_bmr_owid2 pop_dem_ws_18_bmr_owid
rename dem_ws_age_group_bmr_owid3 pop_dem_ws_30_bmr_owid
rename dem_ws_age_group_bmr_owid4 pop_dem_ws_60_bmr_owid
rename dem_ws_age_group_bmr_owid5 pop_dem_ws_90_bmr_owid
rename dem_ws_age_group_bmr_owid6 pop_dem_ws_91plus_bmr_owid

* Temporarily save data:
save "democracy/datasets/final/bmr_aggregated_popweighted.dta", replace


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
use "democracy/datasets/refined/bmr_refined.dta", clear

* Add regional identifiers:
merge m:1 country_name using "Our World in Data/countries_regions_pairs.dta"
tab country_name if _merge == 1
replace region = "Africa" if country_name == "Orange Free State"
replace region = "Asia" if country_name == "North Vietnam"
replace region = "North America" if country_name == "Central American Union"
replace region = "South America" if country_name == "Great Colombia"
replace region = "Europe" if country_name == "Papal States" | country_name == "Piedmont-Sardinia"
drop if _merge == 2
drop _merge

* Only aggregate countries without imputed values:
replace regime_bmr_owid = . if regime_imputed_bmr_owid == 1
replace regime_womsuffr_bmr_owid = . if regime_imputed_bmr_owid == 1
replace dem_age_group_bmr_owid = . if regime_imputed_bmr_owid == 1
replace dem_ws_age_group_bmr_owid = . if regime_imputed_bmr_owid == 1

tabulate regime_bmr_owid, generate(regime_bmr_owid)
tabulate regime_womsuffr_bmr_owid, generate(regime_womsuffr_bmr_owid)
tabulate dem_age_group_bmr_owid, generate(dem_age_group_bmr_owid)
tabulate dem_ws_age_group_bmr_owid, generate(dem_ws_age_group_bmr_owid)

* Collapse dataset by year:
collapse (sum) regime_bmr_owid* regime_womsuffr_bmr_owid* dem_age_group_bmr_owid* dem_ws_age_group_bmr_owid*, by(year region)
drop regime_bmr_owid regime_womsuffr_bmr_owid dem_age_group_bmr_owid dem_ws_age_group_bmr_owid

* Create entity identifier:
rename region country_name

* Rename variables:
rename regime_bmr_owid1 number_nondem_bmr_owid
rename regime_bmr_owid2 number_dem_bmr_owid

rename regime_womsuffr_bmr_owid1 number_nondem_womsuffr_bmr_owid
rename regime_womsuffr_bmr_owid2 number_dem_womsuffr_bmr_owid

drop dem_age_group_bmr_owid1
rename dem_age_group_bmr_owid2 number_dem_18_bmr_owid
rename dem_age_group_bmr_owid3 number_dem_30_bmr_owid
rename dem_age_group_bmr_owid4 number_dem_60_bmr_owid
rename dem_age_group_bmr_owid5 number_dem_90_bmr_owid
rename dem_age_group_bmr_owid6 number_dem_91plus_bmr_owid

drop dem_ws_age_group_bmr_owid1
rename dem_ws_age_group_bmr_owid2 number_dem_ws_18_bmr_owid
rename dem_ws_age_group_bmr_owid3 number_dem_ws_30_bmr_owid
rename dem_ws_age_group_bmr_owid4 number_dem_ws_60_bmr_owid
rename dem_ws_age_group_bmr_owid5 number_dem_ws_90_bmr_owid
rename dem_ws_age_group_bmr_owid6 number_dem_ws_91plus_bmr_owid

* Temporarily save data:
save "democracy/datasets/final/bmr_aggregated_regions.dta", replace


** Aggregate by year and region to create regional aggregates for population-weighted sums of regime variables:

* Import data:
use "democracy/datasets/refined/bmr_refined.dta", clear

* Add population data:
merge 1:1 country_name year using "Our World in Data/owid_population_cleaned.dta"
tab country_name if _merge == 1 & year >= 1800 // Unmerged observations in master datasets either before 1800, historical countries (East Germany, Soviet Union) or current countries without population data (Kosovo).
drop _merge
drop if year == 2021

* Add regional identifiers:
merge m:1 country_name using "Our World in Data/countries_regions_pairs.dta"
tab country_name if _merge == 1
replace region = "Africa" if country_name == "Orange Free State"
replace region = "Asia" if country_name == "North Vietnam"
replace region = "North America" if country_name == "Central American Union"
replace region = "South America" if country_name == "Great Colombia"
replace region = "Europe" if country_name == "Papal States" | country_name == "Piedmont-Sardinia"
drop if _merge == 2
drop _merge

* Recode regime classification such that it includes a category for when population data is available, but regime data is missing:
replace regime_bmr_owid = 2 if regime_bmr_owid == . & population_owid != .
label values regime_bmr_owid regime_bmr_owid
label define regime_bmr_owid 0 "nondemocracy" 1 "democracy" 2 "no regime data", add
drop if population_owid == .

replace regime_womsuffr_bmr_owid = 2 if regime_womsuffr_bmr_owid == . & population_owid != .
label values regime_womsuffr_bmr_owid regime_bmr_owid

* Here, I also aggregate countries with imputed values — because people matter, not countries.

* Create indicator variables for specific regime categories:
tabulate regime_bmr_owid, generate(regime_bmr_owid)
tabulate regime_womsuffr_bmr_owid, generate(regime_womsuffr_bmr_owid)
tabulate dem_age_group_bmr_owid, generate(dem_age_group_bmr_owid)
tabulate dem_ws_age_group_bmr_owid, generate(dem_ws_age_group_bmr_owid)

* Collapse dataset by year:
collapse (sum) regime_bmr_owid* regime_womsuffr_bmr_owid* dem_age_group_bmr_owid* dem_ws_age_group_bmr_owid* [fweight = population_owid], by(year region)
drop regime_bmr_owid regime_womsuffr_bmr_owid dem_age_group_bmr_owid dem_ws_age_group_bmr_owid

* Create entity identifier:
rename region country_name

* Rename variables:
rename regime_bmr_owid1 pop_nondem_bmr_owid
rename regime_bmr_owid2 pop_dem_bmr_owid
rename regime_bmr_owid3 pop_missreg_bmr_owid

drop regime_womsuffr_bmr_owid3
rename regime_womsuffr_bmr_owid1 pop_nondem_womsuffr_bmr_owid
rename regime_womsuffr_bmr_owid2 pop_dem_womsuffr_bmr_owid

drop dem_age_group_bmr_owid1
rename dem_age_group_bmr_owid2 pop_dem_18_bmr_owid
rename dem_age_group_bmr_owid3 pop_dem_30_bmr_owid
rename dem_age_group_bmr_owid4 pop_dem_60_bmr_owid
rename dem_age_group_bmr_owid5 pop_dem_90_bmr_owid
rename dem_age_group_bmr_owid6 pop_dem_91plus_bmr_owid

drop dem_ws_age_group_bmr_owid1
rename dem_ws_age_group_bmr_owid2 pop_dem_ws_18_bmr_owid
rename dem_ws_age_group_bmr_owid3 pop_dem_ws_30_bmr_owid
rename dem_ws_age_group_bmr_owid4 pop_dem_ws_60_bmr_owid
rename dem_ws_age_group_bmr_owid5 pop_dem_ws_90_bmr_owid
rename dem_ws_age_group_bmr_owid6 pop_dem_ws_91plus_bmr_owid

* Temporarily save data:
save "democracy/datasets/final/bmr_aggregated_popweighted_regions.dta", replace


** Merge different datasets:
use "democracy/datasets/refined/bmr_refined.dta"
merge 1:1 country_name year using "democracy/datasets/final/bmr_aggregated.dta"
drop _merge
merge 1:1 country_name year using "democracy/datasets/final/bmr_aggregated_popweighted.dta"
drop _merge
merge 1:1 country_name year using "democracy/datasets/final/bmr_aggregated_regions.dta"
drop _merge
merge 1:1 country_name year using "democracy/datasets/final/bmr_aggregated_popweighted_regions.dta", update
drop _merge
erase "democracy/datasets/final/bmr_aggregated.dta"
erase "democracy/datasets/final/bmr_aggregated_popweighted.dta"
erase "democracy/datasets/final/bmr_aggregated_regions.dta"
erase "democracy/datasets/final/bmr_aggregated_popweighted_regions.dta"


** Add regional identifiers to final dataset:
merge m:1 country_name using "Our World in Data/countries_regions_pairs.dta"
tab country_name if _merge == 1
replace region = "Africa" if country_name == "Orange Free State"
replace region = "Asia" if country_name == "North Vietnam"
replace region = "North America" if country_name == "Central American Union"
replace region = "South America" if country_name == "Great Colombia"
replace region = "Europe" if country_name == "Papal States" | country_name == "Piedmont-Sardinia"
replace region = "World" if country_name == "World"
drop if _merge == 2
drop _merge


** Label variables:
label variable number_nondem_bmr_owid "Number of nondemocracies (BMR)"
label variable number_dem_bmr_owid "Number of democracies (BMR)"

label variable number_nondem_womsuffr_bmr_owid "Number of nondemocracies, including women's suffrage (BMR)"
label variable number_dem_womsuffr_bmr_owid "Number of democracies, including women's suffrage (BMR)"

label variable pop_nondem_bmr_owid "People living in nondemocracies (BMR)"
label variable pop_dem_bmr_owid "People living in of democracies (BMR)"
label variable pop_missreg_bmr_owid "People living in countries without regime data (BMR)"

label variable pop_nondem_womsuffr_bmr_owid "People living in nondemocracies, including women's suffrage (BMR)"
label variable pop_dem_womsuffr_bmr_owid "People living in of democracies, including women's suffrage (BMR)"

label variable number_dem_18_bmr_owid "Number of democracies aged 1-18 years (BMR)"
label variable number_dem_30_bmr_owid "Number of democracies aged 19-30 years (BMR)"
label variable number_dem_60_bmr_owid "Number of democracies aged 31-60 years (BMR)"
label variable number_dem_90_bmr_owid "Number of democracies aged 61-90 years (BMR)"
label variable number_dem_91plus_bmr_owid "Number of democracies aged 91 years or older (BMR)"

label variable number_dem_ws_18_bmr_owid "Number of democracies (incl. women's suffrage) aged 1-18 years (BMR)"
label variable number_dem_ws_30_bmr_owid "Number of democracies (incl. women's suffrage) aged 19-30 years (BMR)"
label variable number_dem_ws_60_bmr_owid "Number of democracies (incl. women's suffrage) aged 31-60 years (BMR)"
label variable number_dem_ws_90_bmr_owid "Number of democracies (incl. women's suffrage) aged 61-90 years (BMR)"
label variable number_dem_ws_91plus_bmr_owid "Number of democracies (incl. women's suffrage) aged 91 years or older (BMR)"

label variable pop_dem_18_bmr_owid "People living in democracies aged 1-18 years (BMR)"
label variable pop_dem_30_bmr_owid "People living in democracies aged 19-30 years (BMR)"
label variable pop_dem_60_bmr_owid "People living in democracies aged 31-60 years (BMR)"
label variable pop_dem_90_bmr_owid "People living in democracies aged 61-90 years (BMR)"
label variable pop_dem_91plus_bmr_owid "People living in democracies aged 91 years or older (BMR)"

label variable pop_dem_ws_18_bmr_owid "People living in democracies (incl. women's suffrage) aged 1-18 years (BMR)"
label variable pop_dem_ws_30_bmr_owid "People living in democracies (incl. women's suffrage) aged 19-30 years (BMR)"
label variable pop_dem_ws_60_bmr_owid "People living in democracies (incl. women's suffrage) aged 31-60 years (BMR)"
label variable pop_dem_ws_90_bmr_owid "People living in democracies (incl. women's suffrage) aged 61-90 years (BMR)"
label variable pop_dem_ws_91plus_bmr_owid "People living in democracies (incl. women's suffrage) aged 91 years or older (BMR)"

label variable region "Region"


** Order observations:
sort country_name year


** Export data:
save "democracy/datasets/final/bmr_final.dta", replace
export delimited "democracy/datasets/final/bmr_final.csv", replace nolabel

describe, replace
keep name varlab
rename name varname
rename varlab varlabel
export delimited "democracy/datasets/final/bmr_final_meta.csv", replace


exit
