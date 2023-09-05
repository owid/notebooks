*****  Stata do-file to create the nuclear-weapons-inventories data used in the following chart on Our World in Data (OWID):
*****  https://ourworldindata.org/grapher/nuclear-warhead-inventories
*****  Author: Bastian Herre
*****  August 21, 2023


version 14

clear all
set more off
set varabbrev off


** Set your own working directories here to run the file:
cd "/Users/bastianherre/Dropbox/Data/"
global project "/Users/bastianherre/Dropbox/Data/"


** Download dataset from https://fas.org/issues/nuclear-weapons/status-world-nuclear-forces/ and move it into the folder "Nuclear weapons/Federation of American Scientists 2022 nuclear weapons stockpiles".
** Import 2022 data:
import delimited "Federation of American Scientists 2023 nuclear weapons inventories/nuclear_weapons_inventories_2022_raw.csv"


** Keep variables of interest:
drop sumdeployedstrategicdeployedstra


** Rename variables:
rename ÿþcountry country_name
rename deployednonstrategic nuclear_weapons_depl_nonstrat
rename deployedstrategic nuclear_weapons_depl_strat
rename reservenondeployed nuclear_weapons_reserve_nondepl
rename retired nuclear_weapons_retired
rename totalinventory nuclear_weapons_inventory


** Refine variables:
generate year = 2022

replace nuclear_weapons_retired = 0 if nuclear_weapons_retired == .
replace nuclear_weapons_retired = (nuclear_weapons_inventory - nuclear_weapons_depl_nonstrat - nuclear_weapons_depl_strat - nuclear_weapons_reserve_nondepl - nuclear_weapons_retired) if country_name == "United Kingdom" // In other data by FAS the UK has 180 stockpiled warheads; so the difference must be retired warheads.


** Temporarily save the data:
save "Federation of American Scientists 2023 nuclear weapons inventories/nuclear_weapons_inventories_temp.dta", replace


** Import 2023 data:
import delimited "Federation of American Scientists 2023 nuclear weapons inventories/nuclear_weapons_inventories_2023_raw.csv", clear


** Keep observations of interest:
drop in 6

** Refine observations of interest:
destring russia, force replace
destring unitedstates, force replace


** Transpose data:
xpose, varname clear
drop in 1


** Rename variables:
rename _varname country_name
rename v1 nuclear_weapons_retired
rename v2 nuclear_weapons_reserve_nondepl
rename v3 nuclear_weapons_depl_nonstrat
rename v4 nuclear_weapons_depl_strat
rename v5 nuclear_weapons_inventory


** Refine variables:
generate year = 2023

replace country_name = "Russia" if country_name == "russia"
replace country_name = "United States" if country_name == "unitedstates"
replace country_name = "China" if country_name == "china"
replace country_name = "France" if country_name == "france"
replace country_name = "United Kingdom" if country_name == "unitedkingdom"
replace country_name = "Pakistan" if country_name == "pakistan"
replace country_name = "India" if country_name == "india"
replace country_name = "Israel" if country_name == "israel"
replace country_name = "North Korea" if country_name == "northkorea"

replace nuclear_weapons_retired = 0 if nuclear_weapons_retired == .


** Combine 2022 and 2023 data:
append using "Federation of American Scientists 2023 nuclear weapons inventories/nuclear_weapons_inventories_temp.dta"
erase "Federation of American Scientists 2023 nuclear weapons inventories/nuclear_weapons_inventories_temp.dta"


** Label variables:
label variable country_name "Country name"
label variable year "Year"
label variable nuclear_weapons_depl_nonstrat "Deployed nonstrategic nuclear warheads (Federation of American Scientists 2022)"
label variable nuclear_weapons_depl_strat "Deployed strategic nuclear warheads (Federation of American Scientists 2022)"
label variable nuclear_weapons_reserve_nondepl "Nondeployed reserve nuclear warheads (Federation of American Scientists 2022)"
label variable nuclear_weapons_retired "Retired nuclear warheads (Federation of American Scientists 2022)"
label variable nuclear_weapons_inventory "Nuclear warheads inventory (Federation of American Scientists 2022)"


** Order variables and observations:
order country_name year nuclear_weapons_depl_strat nuclear_weapons_depl_nonstrat
sort country_name year


** Export data:
save "Federation of American Scientists 2023 nuclear weapons inventories/nuclear_weapons_inventories.dta", replace
export delimited "Federation of American Scientists 2023 nuclear weapons inventories/nuclear_weapons_inventories.csv", replace

describe, replace
keep name varlab
rename name varname
rename varlab varlabel
export delimited "Federation of American Scientists 2023 nuclear weapons inventories/nuclear_weapons_inventories_meta.csv", replace



exit
