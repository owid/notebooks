*****  Stata do-file to create the nuclear-weapons-stockpiles data used in the following chart on Our World in Data (OWID):
*****  https://ourworldindata.org/grapher/nuclear-warhead-stockpiles
*****  Author: Bastian Herre
*****  September 5, 2022


version 14

clear all
set more off
set varabbrev off


** Set your own working directories here to run the file:
cd "/Users/bastianherre/Dropbox/Data/"
global project "/Users/bastianherre/Dropbox/Data/nuclear_weapons"


** Download dataset from https://fas.org/issues/nuclear-weapons/status-world-nuclear-forces/ and move it into the folder "Nuclear weapons/Federation of American Scientists 2022 nuclear weapons stockpiles".
** Import data:
import delimited "Federation of American Scientists 2022 nuclear weapons stockpiles/nuclear_weapons_stockpiles_raw.csv"


** Keep variables of interest:
drop totalinventories


** Rename and label variables:
rename ÿþyear year

rename china nuclear_weapons_stockpile1
rename france nuclear_weapons_stockpile2
rename india nuclear_weapons_stockpile3
rename israel nuclear_weapons_stockpile4
rename northkorea nuclear_weapons_stockpile5
rename pakistan nuclear_weapons_stockpile6
rename russia nuclear_weapons_stockpile7
rename southafrica nuclear_weapons_stockpile8
rename uk nuclear_weapons_stockpile10
rename us nuclear_weapons_stockpile11

label variable year "Year"

** Create country-year dataset:
reshape long nuclear_weapons_stockpile, i(year) j(country_number)
label variable nuclear_weapons_stockpile "Nuclear warhead stockpile (Federation of American Scientists 2022)"

generate country_name = "China" if country_number == 1
replace country_name = "France" if country_number == 2
replace country_name = "India" if country_number == 3
replace country_name = "Israel" if country_number == 4
replace country_name = "North Korea" if country_number == 5
replace country_name = "Pakistan" if country_number == 6
replace country_name = "Russia" if country_number == 7
replace country_name = "South Africa" if country_number == 8
replace country_name = "World" if country_number == 9
replace country_name = "United Kingdom" if country_number == 10
replace country_name = "United States" if country_number == 11
label variable country_name "Country name"
drop country_number


** Refine variables:
replace nuclear_weapons_stockpile = 0 if nuclear_weapons_stockpile == .


** Order variables and observations:
order country_name year nuclear_weapons_stockpile
sort country_name year


** Export data:
save "Federation of American Scientists 2022 nuclear weapons stockpiles/nuclear_weapons_stockpiles.dta", replace
export delimited "Federation of American Scientists 2022 nuclear weapons stockpiles/nuclear_weapons_stockpiles.csv", replace



exit
