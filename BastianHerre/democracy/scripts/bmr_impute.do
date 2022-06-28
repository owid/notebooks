*****  This Stata do-file expands the countries and years covered by the BMR dataset
*****  Author: Bastian Herre
*****  June 28, 2022

version 14
clear all
set more off
set varabbrev off


** Set your own working directories here to run the file:
cd "/Users/bastianherre/Dropbox/Data/"
global project "/Users/bastianherre/Dropbox/Data/"


** Combine OWID country-year dataset with V-Dem and RoW data:
use "Our World in Data/owid_entities_expanded.dta"

rename entity_name country_name
label variable country_name "Country name"

merge 1:1 country_name year using "democracy/datasets/cleaned/bmr_cleaned.dta"
tab country_name if _merge == 2
sort country_name year


** Create variable indicating which observations include information from BMR:
generate bmr_obs = 1 if _merge == 2 | _merge == 3
replace bmr_obs = 0 if _merge == 1
drop _merge

label variable bmr_obs "Observation includes information from BMR"


** Impute values from historical predecessors:

generate regime_imputed_country_bmr_owid = ""
replace regime_imputed_country_bmr_owid = "Great Colombia" if country_name == "Colombia" & year >= 1821 & year <= 1830
replace regime_imputed_country_bmr_owid = "Central American Union" if country_name == "Costa Rica" & year >= 1824 & year <= 1838
replace regime_imputed_country_bmr_owid = "Czechoslovakia" if country_name == "Czechia" & year >= 1918 & year <= 1992
replace regime_imputed_country_bmr_owid = "Great Colombia" if country_name == "Ecuador" & year >= 1821 & year <= 1830
replace regime_imputed_country_bmr_owid = "Central American Union" if country_name == "El Salvador" & year >= 1824 & year <= 1838
replace regime_imputed_country_bmr_owid = "Central American Union" if country_name == "Guatemala" & year >= 1824 & year <= 1838
replace regime_imputed_country_bmr_owid = "Central American Union" if country_name == "Honduras" & year >= 1824 & year <= 1838
replace regime_imputed_country_bmr_owid = "Central American Union" if country_name == "Nicaragua" & year >= 1824 & year <= 1838
replace regime_imputed_country_bmr_owid = "Korea" if country_name == "North Korea" & year >= 1800 & year <= 1910
replace regime_imputed_country_bmr_owid = "Great Colombia" if country_name == "Panama" & year >= 1821 & year <= 1830
replace regime_imputed_country_bmr_owid = "Czechoslovakia" if country_name == "Slovakia" & year >= 1918 & year <= 1992
replace regime_imputed_country_bmr_owid = "Korea" if country_name == "South Korea" & year >= 1800 & year <= 1910
replace regime_imputed_country_bmr_owid = "Great Colombia" if country_name == "Venezuela" & year >= 1821 & year <= 1830

label variable regime_imputed_country_bmr_owid "Name of the country from which BMR regime information was imputed"


** Merge with BMR dataset again, this time on imputing countries:

rename country_name country_name_temp
rename regime_imputed_country_bmr_owid country_name
sort country_name year

merge m:1 country_name year using "democracy/datasets/cleaned/bmr_cleaned.dta", update
drop if _merge == 2

rename country_name regime_imputed_country_bmr_owid
rename country_name_temp country_name
sort country_name year

rename regime_bmr regime_bmr_owid
rename regime_womsuffr_bmr regime_womsuffr_bmr_owid


** Create variable identifying whether regime data is imputed:
generate regime_imputed_bmr_owid = .
replace regime_imputed_bmr_owid = 0 if _merge != 4
replace regime_imputed_bmr_owid = 1 if _merge == 4
drop _merge

order regime_imputed_bmr_owid, before(regime_imputed_country_bmr_owid)

replace regime_imputed_country_bmr_owid = "" if regime_imputed_bmr_owid == 0

label variable regime_imputed_country_bmr_owid "Name of the country from which BMR regime information was imputed"
label variable regime_imputed_bmr_owid "BMR regime information imputed from another country"


** Update observations including information from BMR:
replace bmr_obs = 1 if regime_imputed_bmr_owid == 1


** Create variable identifying whether country includes information from BMR:
bysort country_name: egen bmr_country = max(bmr_obs)


** Keep countries and years of interest:
drop if bmr_country == 0
drop if bmr_obs == 0
drop bmr_country bmr_obs

drop if year < 1800 | year == 2021


** Export data:
save "democracy/datasets/imputed/bmr_imputed.dta", replace
export delimited "democracy/datasets/imputed/bmr_imputed.csv", replace



exit
