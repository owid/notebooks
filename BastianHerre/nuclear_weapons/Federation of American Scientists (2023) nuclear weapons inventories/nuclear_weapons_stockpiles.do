*****  Stata do-file to create the nuclear-weapons-stockpiles data used in the following chart on Our World in Data (OWID):
*****  https://ourworldindata.org/grapher/nuclear-warhead-stockpiles
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
** Import data:
import delimited "Federation of American Scientists 2023 nuclear weapons inventories/nuclear_weapons_stockpiles_raw.csv"


** Rename and label variables:
rename ÿþyear year
rename measurenames country_name
rename measurevalues nuclear_weapons_stockpile

label variable year "Year"
label variable country_name "Country name"
label variable nuclear_weapons_stockpile "Nuclear warhead stockpile (Federation of American Scientists 2022)"


** Refine variables:
replace country_name = "World" if country_name == "Total  Inventories"
replace country_name = "United Kingdom" if country_name == "UK"
replace country_name = "United States" if country_name == "US"

replace nuclear_weapons_stockpile = 0 if nuclear_weapons_stockpile == .


** Order variables and observations:
order country_name year nuclear_weapons_stockpile
sort country_name year


** Export data:
save "Federation of American Scientists 2023 nuclear weapons inventories/nuclear_weapons_stockpiles.dta", replace
export delimited "Federation of American Scientists 2023 nuclear weapons inventories/nuclear_weapons_stockpiles.csv", replace

describe, replace
keep name varlab
rename name varname
rename varlab varlabel
export delimited "Federation of American Scientists 2023 nuclear weapons inventories/nuclear_weapons_stockpiles_meta.csv", replace


exit
