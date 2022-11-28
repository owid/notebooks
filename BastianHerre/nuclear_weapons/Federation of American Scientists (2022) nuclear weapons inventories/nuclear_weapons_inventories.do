*****  Stata do-file to create the nuclear-weapons-inventories data used in the following chart on Our World in Data (OWID):
*****  https://ourworldindata.org/grapher/nuclear-warhead-inventories
*****  Author: Bastian Herre
*****  October 26, 2022


version 14

clear all
set more off
set varabbrev off


** Set your own working directories here to run the file:
cd "/Users/bastianherre/Dropbox/Data/"
global project "/Users/bastianherre/Dropbox/Data/"


** Download dataset from https://fas.org/issues/nuclear-weapons/status-world-nuclear-forces/ and move it into the folder "Nuclear weapons/Federation of American Scientists 2022 nuclear weapons stockpiles".
** Import data:
import delimited "Federation of American Scientists 2022 nuclear weapons inventories/nuclear_weapons_inventories_2022_raw.csv"


** Keep variables of interest:
drop sumdeployedstrategicdeployedstra


** Rename and label variables:
rename ÿþcountry country_name
rename deployednonstrategic nuclear_weapons_depl_nonstrat
rename deployedstrategic nuclear_weapons_depl_strat
rename reservenondeployed nuclear_weapons_reserve_nondepl
rename retired nuclear_weapons_retired
rename totalinventory nuclear_weapons_inventory

label variable country_name "Country name"
label variable nuclear_weapons_depl_nonstrat "Deployed nonstrategic nuclear warheads (Federation of American Scientists 2022)"
label variable nuclear_weapons_depl_strat "Deployed strategic nuclear warheads (Federation of American Scientists 2022)"
label variable nuclear_weapons_reserve_nondepl "Nondeployed reserve nuclear warheads (Federation of American Scientists 2022)"
label variable nuclear_weapons_retired "Retired nuclear warheads (Federation of American Scientists 2022)"
label variable nuclear_weapons_inventory "Nuclear warheads inventory (Federation of American Scientists 2022)"


** Refine variables:
generate year = 2022
label variable year "Year"

replace nuclear_weapons_retired = 0 if nuclear_weapons_retired == .
replace nuclear_weapons_retired = (nuclear_weapons_inventory - nuclear_weapons_depl_nonstrat - nuclear_weapons_depl_strat - nuclear_weapons_reserve_nondepl - nuclear_weapons_retired) if country_name == "United Kingdom" // In other data by FAS the UK has 180 stockpiled warheads; so the difference must be retired warheads.


** Order variables and observations:
order country_name year nuclear_weapons_depl_strat nuclear_weapons_depl_nonstrat


** Export data:
save "nuclear_weapons/Federation of American Scientists (2022) nuclear weapons inventories/nuclear_weapons_inventories.dta", replace
export delimited "nuclear_weapons/Federation of American Scientists (2022) nuclear weapons inventories/nuclear_weapons_inventories.csv", replace

describe, replace
keep name varlab
rename name varname
rename varlab varlabel
export delimited "nuclear_weapons/Federation of American Scientists (2022) nuclear weapons inventories/nuclear_weapons_inventories_meta.csv", replace



exit
