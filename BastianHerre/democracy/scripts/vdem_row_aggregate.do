*****  This Stata do-file aggregates some of the variables of the V-Dem and RoW data
*****  Author: Bastian Herre
*****  October 25, 2022

version 14
clear all
set more off
set varabbrev off


** Set your own working directories here to run the file:
cd "/Users/bastianherre/Dropbox/Data/"
global project "/Users/bastianherre/Dropbox/Data/"


** Aggregate by year to create world aggregates for sums and averages of regime variables:

* Import data:
use "democracy/datasets/refined/vdem_row_refined.dta", clear

* Only aggregate countries without imputed values:
replace regime_row_owid = . if regime_imputed_vdem_owid == 1
replace regime_amb_row_owid = . if regime_imputed_vdem_owid == 1
replace electdem_age_group_row_owid = . if regime_imputed_vdem_owid == 1
replace libdem_age_group_row_owid = . if regime_imputed_vdem_owid == 1

* Create indicator variables for specific regime categories:
tabulate regime_row_owid, generate(regime_row_owid)
tabulate regime_amb_row_owid, generate(regime_amb_row_owid)
tabulate electdem_age_group_row_owid, generate(electdem_age_group_row_owid)
tabulate libdem_age_group_row_owid, generate(libdem_age_group_row_owid)

* Collapse dataset by year:
collapse (sum) regime_row_owid* regime_amb_row_owid* electdem_age_group_row_owid* libdem_age_group_row_owid* ///
	(mean) electdem_vdem_owid electdem_vdem_low_owid electdem_vdem_high_owid libdem_vdem_owid libdem_vdem_low_owid libdem_vdem_high_owid participdem_vdem_owid participdem_vdem_low_owid participdem_vdem_high_owid delibdem_vdem_owid delibdem_vdem_low_owid delibdem_vdem_high_owid egaldem_vdem_owid egaldem_vdem_low_owid egaldem_vdem_high_owid ///
	civ_libs_vdem_owid civ_libs_vdem_high_owid civ_libs_vdem_low_owid phys_integr_libs_vdem_owid phys_integr_libs_vdem_high_owid phys_integr_libs_vdem_low_owid pol_libs_vdem_owid pol_libs_vdem_high_owid pol_libs_vdem_low_owid priv_libs_vdem_owid priv_libs_vdem_high_owid priv_libs_vdem_low_owid, by(year)
drop regime_row_owid regime_amb_row_owid electdem_age_group_row_owid libdem_age_group_row_owid

* Create entity identifier:
generate country_name = "World"

* Rename variables:
rename regime_row_owid1 number_closedaut_row_owid
rename regime_row_owid2 number_electaut_row_owid
rename regime_row_owid3 number_electdem_row_owid
rename regime_row_owid4 number_libdem_row_owid

rename regime_amb_row_owid1 number_closedaut_amb_row_owid
rename regime_amb_row_owid2 number_closedaut_h_amb_row_owid
rename regime_amb_row_owid3 number_electaut_l_amb_row_owid
rename regime_amb_row_owid4 number_electaut_amb_row_owid
rename regime_amb_row_owid5 number_electaut_h_amb_row_owid
rename regime_amb_row_owid6 number_electdem_l_amb_row_owid
rename regime_amb_row_owid7 number_electdem_amb_row_owid
rename regime_amb_row_owid8 number_electdem_h_amb_row_owid
rename regime_amb_row_owid9 number_libdem_l_amb_row_owid
rename regime_amb_row_owid10 number_libdem_amb_row_owid

drop electdem_age_group_row_owid1 electdem_age_group_row_owid2
rename electdem_age_group_row_owid3 number_electdem_18_row_owid
rename electdem_age_group_row_owid4 number_electdem_30_row_owid
rename electdem_age_group_row_owid5 number_electdem_60_row_owid
rename electdem_age_group_row_owid6 number_electdem_90_row_owid
rename electdem_age_group_row_owid7 number_electdem_91plus_row_owid

drop libdem_age_group_row_owid1 libdem_age_group_row_owid2 libdem_age_group_row_owid3
rename libdem_age_group_row_owid4 number_libdem_18_row_owid
rename libdem_age_group_row_owid5 number_libdem_30_row_owid
rename libdem_age_group_row_owid6 number_libdem_60_row_owid
rename libdem_age_group_row_owid7 number_libdem_90_row_owid
rename libdem_age_group_row_owid8 number_libdem_91plus_row_owid

* Temporarily save data:
save "democracy/datasets/final/vdem_row_aggregated.dta", replace


** Aggregate by year to create world aggregates for population-weighted sums and averages of regime variables:

* Import data:
use "democracy/datasets/refined/vdem_row_refined.dta", clear

* Add population data:
merge 1:1 country_name year using "Our World in Data/owid_population_cleaned.dta"
tab country_name if _merge == 1 & year >= 1800 // Unmerged observations in master datasets either before 1800, historical countries (Two Sicilies, East Germany) or current countries without population data (Kosovo, Palestine/Gaza, Palestine/West Bank, Somaliland).
drop _merge

* Recode regime classification such that it includes a category for when population data is available, but regime data is missing:
replace regime_row_owid = 4 if regime_row_owid == . & population_owid != .
label values regime_row_owid regime_row_owid
label define regime_row_owid 4 "no regime data", add

replace regime_amb_row_owid = 10 if regime_amb_row_owid == . & population_owid != .
label values regime_amb_row_owid regime_row_owid
label define regime_amb_row_owid 10 "no regime data", add
drop if population_owid == .

* Here, I also aggregate countries with imputed values — because people matter here, not countries.

* Create indicator variables for specific regime categories:
tabulate regime_row_owid, generate(regime_row_owid)
tabulate regime_amb_row_owid, generate(regime_amb_row_owid)
tabulate electdem_age_group_row_owid, generate(electdem_age_group_row_owid)
tabulate libdem_age_group_row_owid, generate(libdem_age_group_row_owid)

* Collapse dataset by year:
collapse (sum) regime_row_owid* regime_amb_row_owid* electdem_age_group_row_owid* libdem_age_group_row_owid* ///
	(mean) electdem_vdem_owid electdem_vdem_low_owid electdem_vdem_high_owid libdem_vdem_owid libdem_vdem_low_owid libdem_vdem_high_owid participdem_vdem_owid participdem_vdem_low_owid participdem_vdem_high_owid delibdem_vdem_owid delibdem_vdem_low_owid delibdem_vdem_high_owid egaldem_vdem_owid egaldem_vdem_low_owid egaldem_vdem_high_owid ///
	civ_libs_vdem_owid civ_libs_vdem_high_owid civ_libs_vdem_low_owid phys_integr_libs_vdem_owid phys_integr_libs_vdem_high_owid phys_integr_libs_vdem_low_owid pol_libs_vdem_owid pol_libs_vdem_high_owid pol_libs_vdem_low_owid priv_libs_vdem_owid priv_libs_vdem_high_owid priv_libs_vdem_low_owid [fweight = population_owid], by(year)
drop regime_row_owid regime_amb_row_owid regime_amb_row_owid11 electdem_age_group_row_owid libdem_age_group_row_owid

* Create entity identifier:
generate country_name = "World"

* Rename variables:
rename regime_row_owid1 pop_closedaut_row_owid
rename regime_row_owid2 pop_electaut_row_owid
rename regime_row_owid3 pop_electdem_row_owid
rename regime_row_owid4 pop_libdem_row_owid
rename regime_row_owid5 pop_missreg_row_owid

rename regime_amb_row_owid1 pop_closedaut_amb_row_owid
rename regime_amb_row_owid2 pop_closedaut_h_amb_row_owid
rename regime_amb_row_owid3 pop_electaut_l_amb_row_owid
rename regime_amb_row_owid4 pop_electaut_amb_row_owid
rename regime_amb_row_owid5 pop_electaut_h_amb_row_owid
rename regime_amb_row_owid6 pop_electdem_l_amb_row_owid
rename regime_amb_row_owid7 pop_electdem_amb_row_owid
rename regime_amb_row_owid8 pop_electdem_h_amb_row_owid
rename regime_amb_row_owid9 pop_libdem_l_amb_row_owid
rename regime_amb_row_owid10 pop_libdem_amb_row_owid

drop electdem_age_group_row_owid1 electdem_age_group_row_owid2
rename electdem_age_group_row_owid3 pop_electdem_18_row_owid
rename electdem_age_group_row_owid4 pop_electdem_30_row_owid
rename electdem_age_group_row_owid5 pop_electdem_60_row_owid
rename electdem_age_group_row_owid6 pop_electdem_90_row_owid
rename electdem_age_group_row_owid7 pop_electdem_91plus_row_owid

drop libdem_age_group_row_owid1 libdem_age_group_row_owid2 libdem_age_group_row_owid3
rename libdem_age_group_row_owid4 pop_libdem_18_row_owid
rename libdem_age_group_row_owid5 pop_libdem_30_row_owid
rename libdem_age_group_row_owid6 pop_libdem_60_row_owid
rename libdem_age_group_row_owid7 pop_libdem_90_row_owid
rename libdem_age_group_row_owid8 pop_libdem_91plus_row_owid

rename electdem_vdem_owid popw_electdem_vdem_owid
rename electdem_vdem_low_owid popw_electdem_l_vdem_owid
rename electdem_vdem_high_owid popw_electdem_h_vdem_owid

rename libdem_vdem_owid popw_libdem_vdem_owid
rename libdem_vdem_low_owid popw_libdem_l_vdem_owid
rename libdem_vdem_high_owid popw_libdem_h_vdem_owid

rename participdem_vdem_owid popw_participdem_vdem_owid
rename participdem_vdem_low_owid popw_participdem_l_vdem_owid
rename participdem_vdem_high_owid popw_participdem_h_vdem_owid

rename delibdem_vdem_owid popw_delibdem_vdem_owid
rename delibdem_vdem_low_owid popw_delibdem_l_vdem_owid
rename delibdem_vdem_high_owid popw_delibdem_h_vdem_owid

rename egaldem_vdem_owid popw_egaldem_vdem_owid
rename egaldem_vdem_low_owid popw_egaldem_l_vdem_owid
rename egaldem_vdem_high_owid popw_egaldem_h_vdem_owid

rename civ_libs_vdem_owid popw_civ_libs_vdem_owid
rename civ_libs_vdem_high_owid popw_civ_libs_vdem_high_owid
rename civ_libs_vdem_low_owid popw_civ_libs_vdem_low_owid

rename phys_integr_libs_vdem_owid popw_physinteg_libs_vdem_owid
rename phys_integr_libs_vdem_high_owid popw_physinteg_libs_vdem_h_owid
rename phys_integr_libs_vdem_low_owid popw_physinteg_libs_vdem_l_owid

rename pol_libs_vdem_owid popw_pol_libs_vdem_owid
rename pol_libs_vdem_high_owid popw_pol_libs_vdem_high_owid
rename pol_libs_vdem_low_owid popw_pol_libs_vdem_low_owid

rename priv_libs_vdem_owid popw_priv_libs_vdem_owid
rename priv_libs_vdem_high_owid popw_priv_libs_vdem_high_owid
rename priv_libs_vdem_low_owid popw_priv_libs_vdem_low_owid


* Temporarily save data:
save "democracy/datasets/final/vdem_row_aggregated_popweighted.dta", replace


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
use "democracy/datasets/refined/vdem_row_refined.dta", clear

* Add regional identifiers:
merge m:1 country_name using "Our World in Data/countries_regions_pairs.dta"
tab country_name if _merge == 1
replace region = "Europe" if country_name == "Brunswick" | country_name == "Hamburg" | country_name == "Nassau" | country_name == "Oldenburg" | country_name == "Papal States" | country_name == "Piedmont-Sardinia" | country_name == "Saxe-Weimar-Eisenach"
replace region = "Asia" if country_name == "Palestine/Gaza" | country_name == "Palestine/West Bank"
drop if _merge == 2
drop _merge

* Only aggregate countries without imputed values:
replace regime_row_owid = . if regime_imputed_vdem_owid == 1
replace regime_amb_row_owid = . if regime_imputed_vdem_owid == 1
replace electdem_age_group_row_owid = . if regime_imputed_vdem_owid == 1
replace libdem_age_group_row_owid = . if regime_imputed_vdem_owid == 1

* Create indicator variables for specific regime categories:
tabulate regime_row_owid, generate(regime_row_owid)
tabulate regime_amb_row_owid, generate(regime_amb_row_owid)
tabulate electdem_age_group_row_owid, generate(electdem_age_group_row_owid)
tabulate libdem_age_group_row_owid, generate(libdem_age_group_row_owid)

* Collapse dataset by year:
collapse (sum) regime_row_owid* regime_amb_row_owid* electdem_age_group_row_owid* libdem_age_group_row_owid* ///
	(mean) electdem_vdem_owid electdem_vdem_low_owid electdem_vdem_high_owid libdem_vdem_owid libdem_vdem_low_owid libdem_vdem_high_owid participdem_vdem_owid participdem_vdem_low_owid participdem_vdem_high_owid delibdem_vdem_owid delibdem_vdem_low_owid delibdem_vdem_high_owid egaldem_vdem_owid egaldem_vdem_low_owid egaldem_vdem_high_owid ///
	civ_libs_vdem_owid civ_libs_vdem_high_owid civ_libs_vdem_low_owid phys_integr_libs_vdem_owid phys_integr_libs_vdem_high_owid phys_integr_libs_vdem_low_owid pol_libs_vdem_owid pol_libs_vdem_high_owid pol_libs_vdem_low_owid priv_libs_vdem_owid priv_libs_vdem_high_owid priv_libs_vdem_low_owid, by(year region)
drop regime_row_owid regime_amb_row_owid electdem_age_group_row_owid libdem_age_group_row_owid

* Create entity identifier:
rename region country_name

* Rename variables:
rename regime_row_owid1 number_closedaut_row_owid
rename regime_row_owid2 number_electaut_row_owid
rename regime_row_owid3 number_electdem_row_owid
rename regime_row_owid4 number_libdem_row_owid

rename regime_amb_row_owid1 number_closedaut_amb_row_owid
rename regime_amb_row_owid2 number_closedaut_h_amb_row_owid
rename regime_amb_row_owid3 number_electaut_l_amb_row_owid
rename regime_amb_row_owid4 number_electaut_amb_row_owid
rename regime_amb_row_owid5 number_electaut_h_amb_row_owid
rename regime_amb_row_owid6 number_electdem_l_amb_row_owid
rename regime_amb_row_owid7 number_electdem_amb_row_owid
rename regime_amb_row_owid8 number_electdem_h_amb_row_owid
rename regime_amb_row_owid9 number_libdem_l_amb_row_owid
rename regime_amb_row_owid10 number_libdem_amb_row_owid

drop electdem_age_group_row_owid1 electdem_age_group_row_owid2
rename electdem_age_group_row_owid3 number_electdem_18_row_owid
rename electdem_age_group_row_owid4 number_electdem_30_row_owid
rename electdem_age_group_row_owid5 number_electdem_60_row_owid
rename electdem_age_group_row_owid6 number_electdem_90_row_owid
rename electdem_age_group_row_owid7 number_electdem_91plus_row_owid

drop libdem_age_group_row_owid1 libdem_age_group_row_owid2 libdem_age_group_row_owid3
rename libdem_age_group_row_owid4 number_libdem_18_row_owid
rename libdem_age_group_row_owid5 number_libdem_30_row_owid
rename libdem_age_group_row_owid6 number_libdem_60_row_owid
rename libdem_age_group_row_owid7 number_libdem_90_row_owid
rename libdem_age_group_row_owid8 number_libdem_91plus_row_owid

* Temporarily save data:
save "democracy/datasets/final/vdem_row_aggregated_regions.dta", replace


** Aggregate by year and region to create regional aggregates for population-weighted sums and averages of regime variables:

* Import data:
use "democracy/datasets/refined/vdem_row_refined.dta", clear

* Add population data:
merge 1:1 country_name year using "Our World in Data/owid_population_cleaned.dta"
tab country_name if _merge == 1 & year >= 1800 // Unmerged observations in master datasets either before 1800, historical countries (Two Sicilies, East Germany) or current countries without population data (Kosovo, Palestine/Gaza, Palestine/West Bank, Somaliland).
drop _merge

* Add regional identifiers:
merge m:1 country_name using "Our World in Data/countries_regions_pairs.dta"
tab country_name if _merge == 1
replace region = "Europe" if country_name == "Brunswick" | country_name == "Hamburg" | country_name == "Nassau" | country_name == "Oldenburg" | country_name == "Papal States" | country_name == "Piedmont-Sardinia" | country_name == "Saxe-Weimar-Eisenach"
replace region = "Asia" if country_name == "Palestine/Gaza" | country_name == "Palestine/West Bank"
drop if _merge == 2
drop _merge

* Recode regime classification such that it includes a category for when population data is available, but regime data is missing:
replace regime_row_owid = 4 if regime_row_owid == . & population_owid != .
label values regime_row_owid regime_row_owid
label define regime_row_owid 4 "no regime data", add

replace regime_amb_row_owid = 10 if regime_amb_row_owid == . & population_owid != .
label values regime_amb_row_owid regime_row_owid
label define regime_amb_row_owid 10 "no regime data", add
drop if population_owid == .

* Here, I also aggregate countries with imputed values — because people matter, not countries.

* Create indicator variables for specific regime categories:
tabulate regime_row_owid, generate(regime_row_owid)
tabulate regime_amb_row_owid, generate(regime_amb_row_owid)
tabulate electdem_age_group_row_owid, generate(electdem_age_group_row_owid)
tabulate libdem_age_group_row_owid, generate(libdem_age_group_row_owid)

* Collapse dataset by year:
collapse (sum) regime_row_owid* regime_amb_row_owid* electdem_age_group_row_owid* libdem_age_group_row_owid* ///
	(mean) electdem_vdem_owid electdem_vdem_low_owid electdem_vdem_high_owid libdem_vdem_owid libdem_vdem_low_owid libdem_vdem_high_owid participdem_vdem_owid participdem_vdem_low_owid participdem_vdem_high_owid delibdem_vdem_owid delibdem_vdem_low_owid delibdem_vdem_high_owid egaldem_vdem_owid egaldem_vdem_low_owid egaldem_vdem_high_owid ///
	civ_libs_vdem_owid civ_libs_vdem_high_owid civ_libs_vdem_low_owid phys_integr_libs_vdem_owid phys_integr_libs_vdem_high_owid phys_integr_libs_vdem_low_owid pol_libs_vdem_owid pol_libs_vdem_high_owid pol_libs_vdem_low_owid priv_libs_vdem_owid priv_libs_vdem_high_owid priv_libs_vdem_low_owid [fweight = population_owid], by(year region)
drop regime_row_owid regime_amb_row_owid regime_amb_row_owid11 electdem_age_group_row_owid libdem_age_group_row_owid

* Create entity identifier:
rename region country_name

* Rename variables:
rename regime_row_owid1 pop_closedaut_row_owid
rename regime_row_owid2 pop_electaut_row_owid
rename regime_row_owid3 pop_electdem_row_owid
rename regime_row_owid4 pop_libdem_row_owid
rename regime_row_owid5 pop_missreg_row_owid

rename regime_amb_row_owid1 pop_closedaut_amb_row_owid
rename regime_amb_row_owid2 pop_closedaut_h_amb_row_owid
rename regime_amb_row_owid3 pop_electaut_l_amb_row_owid
rename regime_amb_row_owid4 pop_electaut_amb_row_owid
rename regime_amb_row_owid5 pop_electaut_h_amb_row_owid
rename regime_amb_row_owid6 pop_electdem_l_amb_row_owid
rename regime_amb_row_owid7 pop_electdem_amb_row_owid
rename regime_amb_row_owid8 pop_electdem_h_amb_row_owid
rename regime_amb_row_owid9 pop_libdem_l_amb_row_owid
rename regime_amb_row_owid10 pop_libdem_amb_row_owid

drop electdem_age_group_row_owid1 electdem_age_group_row_owid2
rename electdem_age_group_row_owid3 pop_electdem_18_row_owid
rename electdem_age_group_row_owid4 pop_electdem_30_row_owid
rename electdem_age_group_row_owid5 pop_electdem_60_row_owid
rename electdem_age_group_row_owid6 pop_electdem_90_row_owid
rename electdem_age_group_row_owid7 pop_electdem_91plus_row_owid

drop libdem_age_group_row_owid1 libdem_age_group_row_owid2 libdem_age_group_row_owid3
rename libdem_age_group_row_owid4 pop_libdem_18_row_owid
rename libdem_age_group_row_owid5 pop_libdem_30_row_owid
rename libdem_age_group_row_owid6 pop_libdem_60_row_owid
rename libdem_age_group_row_owid7 pop_libdem_90_row_owid
rename libdem_age_group_row_owid8 pop_libdem_91plus_row_owid

rename electdem_vdem_owid popw_electdem_vdem_owid
rename electdem_vdem_low_owid popw_electdem_l_vdem_owid
rename electdem_vdem_high_owid popw_electdem_h_vdem_owid

rename libdem_vdem_owid popw_libdem_vdem_owid
rename libdem_vdem_low_owid popw_libdem_l_vdem_owid
rename libdem_vdem_high_owid popw_libdem_h_vdem_owid

rename participdem_vdem_owid popw_participdem_vdem_owid
rename participdem_vdem_low_owid popw_participdem_l_vdem_owid
rename participdem_vdem_high_owid popw_participdem_h_vdem_owid

rename delibdem_vdem_owid popw_delibdem_vdem_owid
rename delibdem_vdem_low_owid popw_delibdem_l_vdem_owid
rename delibdem_vdem_high_owid popw_delibdem_h_vdem_owid

rename egaldem_vdem_owid popw_egaldem_vdem_owid
rename egaldem_vdem_low_owid popw_egaldem_l_vdem_owid
rename egaldem_vdem_high_owid popw_egaldem_h_vdem_owid

rename civ_libs_vdem_owid popw_civ_libs_vdem_owid
rename civ_libs_vdem_high_owid popw_civ_libs_vdem_high_owid
rename civ_libs_vdem_low_owid popw_civ_libs_vdem_low_owid

rename phys_integr_libs_vdem_owid popw_physinteg_libs_vdem_owid
rename phys_integr_libs_vdem_high_owid popw_physinteg_libs_vdem_h_owid
rename phys_integr_libs_vdem_low_owid popw_physinteg_libs_vdem_l_owid

rename pol_libs_vdem_owid popw_pol_libs_vdem_owid
rename pol_libs_vdem_high_owid popw_pol_libs_vdem_high_owid
rename pol_libs_vdem_low_owid popw_pol_libs_vdem_low_owid

rename priv_libs_vdem_owid popw_priv_libs_vdem_owid
rename priv_libs_vdem_high_owid popw_priv_libs_vdem_high_owid
rename priv_libs_vdem_low_owid popw_priv_libs_vdem_low_owid

* Temporarily save data:
save "democracy/datasets/final/vdem_row_aggregated_popweighted_regions.dta", replace


** Merge different datasets:
use "democracy/datasets/refined/vdem_row_refined.dta"
merge 1:1 country_name year using "democracy/datasets/final/vdem_row_aggregated.dta"
drop _merge
merge 1:1 country_name year using "democracy/datasets/final/vdem_row_aggregated_popweighted.dta"
drop _merge
merge 1:1 country_name year using "democracy/datasets/final/vdem_row_aggregated_regions.dta"
drop _merge
merge 1:1 country_name year using "democracy/datasets/final/vdem_row_aggregated_popweighted_regions.dta", update
drop _merge
erase "democracy/datasets/final/vdem_row_aggregated.dta"
erase "democracy/datasets/final/vdem_row_aggregated_popweighted.dta"
erase "democracy/datasets/final/vdem_row_aggregated_regions.dta"
erase "democracy/datasets/final/vdem_row_aggregated_popweighted_regions.dta"


** Add regional identifiers to final dataset:
merge m:1 country_name using "Our World in Data/countries_regions_pairs.dta"
tab country_name if _merge == 1
replace region = "Europe" if country_name == "Brunswick" | country_name == "Hamburg" | country_name == "Nassau" | country_name == "Oldenburg" | country_name == "Papal States" | country_name == "Piedmont-Sardinia" | country_name == "Saxe-Weimar-Eisenach"
replace region = "Asia" if country_name == "Palestine/Gaza" | country_name == "Palestine/West Bank"
replace region = "World" if country_name == "World"
drop if _merge == 2
drop _merge


** Label variables:
label variable number_closedaut_row_owid "Number of closed autocracies (RoW, OWID)"
label variable number_electaut_row_owid "Number of electoral autocracies (RoW, OWID)"
label variable number_electdem_row_owid "Number of electoral democracies (RoW, OWID)"
label variable number_libdem_row_owid "Number of liberal democracies (RoW, OWID)"

label variable pop_closedaut_row_owid "People living in closed autocracies (RoW, OWID)"
label variable pop_electaut_row_owid "People living in electoral autocracies (RoW, OWID)"
label variable pop_electdem_row_owid "People living in electoral democracies (RoW, OWID)"
label variable pop_libdem_row_owid "People living in liberal democracies (RoW, OWID)"
label variable pop_missreg_row_owid "People living in countries without regime data (RoW, OWID)"

label variable number_closedaut_amb_row_owid "Number of closed autocracies (ambig. RoW, OWID)"
label variable number_closedaut_h_amb_row_owid "Number of closed, maybe electoral, autocracies (ambig. RoW, OWID)"
label variable number_electaut_l_amb_row_owid "Number of electoral, maybe closed, autocracies (ambig. RoW, OWID)"
label variable number_electaut_amb_row_owid "Number of electoral autocracies (ambig. RoW, OWID)"
label variable number_electaut_h_amb_row_owid "Number of electoral autocracies that may be electoral democracies (ambig. RoW, OWID)"
label variable number_electdem_l_amb_row_owid "Number of electoral democracies that may be electoral autocracies (ambig. RoW, OWID)"
label variable number_electdem_amb_row_owid "Number of electoral democracies (ambig. RoW, OWID)"
label variable number_electdem_h_amb_row_owid "Number of electoral, maybe liberal, democracies (ambig. RoW, OWID)"
label variable number_libdem_l_amb_row_owid "Number of liberal, maybe electoral, democracies (ambig. RoW, OWID)"
label variable number_libdem_amb_row_owid "Number of liberal democracies (ambig. RoW, OWID)"

label variable pop_closedaut_amb_row_owid "People living in closed autocracies (ambig. RoW, OWID)"
label variable pop_closedaut_h_amb_row_owid "People living in closed, maybe electoral, autocracies (ambig. RoW, OWID)"
label variable pop_electaut_l_amb_row_owid "People living in electoral, maybe closed, autocracies (ambig. RoW, OWID)"
label variable pop_electaut_amb_row_owid "People living in electoral autocracies (ambig. RoW, OWID)"
label variable pop_electaut_h_amb_row_owid "People living in electoral autocracies that may be electoral democracies (ambig. RoW, OWID)"
label variable pop_electdem_l_amb_row_owid "People living in electoral democracies that may be electoral autocracies (ambig. RoW, OWID)"
label variable pop_electdem_amb_row_owid "People living in electoral democracies (ambig. RoW, OWID)"
label variable pop_electdem_h_amb_row_owid "People living in electoral, maybe liberal, democracies (ambig. RoW, OWID)"
label variable pop_libdem_l_amb_row_owid "People living in liberal, maybe electoral, democracies (ambig. RoW, OWID)"
label variable pop_libdem_amb_row_owid "People living in liberal democracies (ambig. RoW, OWID)"

label variable number_electdem_18_row_owid "Number of electoral democracies aged 1-18 years (RoW, OWID)"
label variable number_electdem_30_row_owid "Number of electoral democracies aged 19-30 years (RoW, OWID)"
label variable number_electdem_60_row_owid "Number of electoral democracies aged 31-60 years (RoW, OWID)"
label variable number_electdem_90_row_owid "Number of electoral democracies aged 61-90 years (RoW, OWID)"
label variable number_electdem_91plus_row_owid "Number of electoral democracies aged 91 years or older (RoW, OWID)"

label variable number_libdem_18_row_owid "Number of liberal democracies aged 1-18 years (RoW, OWID)"
label variable number_libdem_30_row_owid "Number of liberal democracies aged 19-30 years (RoW, OWID)"
label variable number_libdem_60_row_owid "Number of liberal democracies aged 31-60 years (RoW, OWID)"
label variable number_libdem_90_row_owid "Number of liberal democracies aged 61-90 years (RoW, OWID)"
label variable number_libdem_91plus_row_owid "Number of liberal democracies aged 91 years or older (RoW, OWID)"

label variable pop_electdem_18_row_owid "People living in electoral democracies aged 1-18 years (RoW, OWID)"
label variable pop_electdem_30_row_owid "People living in electoral democracies aged 19-30 years (RoW, OWID)"
label variable pop_electdem_60_row_owid "People living in electoral democracies aged 31-60 years (RoW, OWID)"
label variable pop_electdem_90_row_owid "People living in electoral democracies aged 61-90 years (RoW, OWID)"
label variable pop_electdem_91plus_row_owid "People living in electoral democracies aged 91 years or older (RoW, OWID)"

label variable pop_libdem_18_row_owid "People living in liberal democracies aged 1-18 years (RoW, OWID)"
label variable pop_libdem_30_row_owid "People living in liberal democracies aged 19-30 years (RoW, OWID)"
label variable pop_libdem_60_row_owid "People living in liberal democracies aged 31-60 years (RoW, OWID)"
label variable pop_libdem_90_row_owid "People living in liberal democracies aged 61-90 years (RoW, OWID)"
label variable pop_libdem_91plus_row_owid "People living in liberal democracies aged 91 years or older (RoW, OWID)"

label variable popw_electdem_vdem_owid "Electoral democracy (V-Dem, population-weighted)"
label variable popw_electdem_l_vdem_owid "Electoral democracy (lower bound, pop-weighted, V-Dem)"
label variable popw_electdem_h_vdem_owid "Electoral democracy (upper bound, pop-weighted, V-Dem)"

label variable popw_libdem_vdem_owid "Liberal democracy (V-Dem, population-weighted)"
label variable popw_libdem_l_vdem_owid "Liberal democracy (lower bound, pop-weighted, V-Dem)"
label variable popw_libdem_h_vdem_owid "Liberal democracy (upper bound, pop-weighted, V-Dem)"

label variable popw_participdem_vdem_owid "Participatory democracy (V-Dem, population-weighted)"
label variable popw_participdem_l_vdem_owid "Participatory democracy (lower bound, pop-weighted, V-Dem)"
label variable popw_participdem_h_vdem_owid "Participatory democracy (upper bound, pop-weighted, V-Dem)"

label variable popw_delibdem_vdem_owid "Deliberative democracy (V-Dem, population-weighted)"
label variable popw_delibdem_l_vdem_owid "Deliberative democracy (lower bound, pop-weighted, V-Dem)"
label variable popw_delibdem_h_vdem_owid "Deliberative democracy (upper bound, pop-weighted, V-Dem)"

label variable popw_egaldem_vdem_owid "Egalitarian democracy (V-Dem, population-weighted)"
label variable popw_egaldem_l_vdem_owid "Egalitarian democracy (lower bound, pop-weighted, V-Dem)"
label variable popw_egaldem_h_vdem_owid "Egalitarian democracy (upper bound, pop-weighted, V-Dem)"

label variable popw_civ_libs_vdem_owid "Civil liberties (V-Dem, population-weighted)"
label variable popw_civ_libs_vdem_low_owid "Civil liberties (lower bound, pop-weighted, V-Dem)"
label variable popw_civ_libs_vdem_high_owid "Civil liberties (upper bound, pop-weighted, V-Dem)"

label variable popw_physinteg_libs_vdem_owid "Physical integrity liberties (V-Dem, population-weighted)"
label variable popw_physinteg_libs_vdem_l_owid "Physical integrity liberties (lower bound, pop-weighted, V-Dem)"
label variable popw_physinteg_libs_vdem_h_owid "Physical integrity liberties (upper bound, pop-weighted, V-Dem)"

label variable popw_pol_libs_vdem_owid "Political civil liberties (V-Dem, population-weighted)"
label variable popw_pol_libs_vdem_low_owid "Political civil liberties (lower bound, pop-weighted, V-Dem)"
label variable popw_pol_libs_vdem_high_owid "Political civil liberties (upper bound, pop-weighted, V-Dem)"

label variable popw_priv_libs_vdem_owid "Private civil liberties (V-Dem, population-weighted)"
label variable popw_priv_libs_vdem_low_owid "Private civil liberties (lower bound, pop-weighted, V-Dem)"
label variable popw_priv_libs_vdem_high_owid "Private civil liberties (upper bound, pop-weighted, V-Dem)"

label variable region "Region"


** Order observations:
sort country_name year


** Export data:
save "democracy/datasets/final/vdem_row_final.dta", replace
export delimited "democracy/datasets/final/vdem_row_final.csv", replace nolabel

describe, replace
keep name varlab
rename name varname
rename varlab varlabel
export delimited "democracy/datasets/final/vdem_row_final_meta.csv", replace


exit
