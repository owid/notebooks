*****  Stata do-file to create the nuclear-weapons-tests data used in the following chart on Our World in Data (OWID):
*****  https://ourworldindata.org/grapher/number-of-nuclear-weapons-tests
*****  Author: Bastian Herre
*****  April 8, 2022


version 14

clear all
set more off
set varabbrev off


** Set your own working directories here to run the file:
cd "/Users/bastianherre/Dropbox/Data/"
global project "/Users/bastianherre/Dropbox/Data/"


** Download dataset from https://www.armscontrol.org/factsheets/nucleartesttally and move it into the folder "Reporters sans Frontieres 2022 World Press Freedom Index".
** Import data:
import excel "Arms Control Association 2020 nuclear weapons tests/nuclear_weapons_tests_states_wide.xlsx", firstrow


** Rename variables:
rename Year year
rename UnitedStates nuclear_weapons_tests1
rename Russia nuclear_weapons_tests2
rename UnitedKingdom nuclear_weapons_tests3
rename France nuclear_weapons_tests4
rename China nuclear_weapons_tests5
rename India nuclear_weapons_tests6
rename Pakistan nuclear_weapons_tests7
rename NorthKorea nuclear_weapons_tests8


** Create country-year dataset:
reshape long nuclear_weapons_tests, i(year) j(country_number)


** Label variables:
label variable nuclear_weapons_tests "Number of nuclear weapons tests (Arms Control Association)"


** Refine variables:
generate country_name = "United States" if country_number == 1
replace country_name = "Russia" if country_number == 2
replace country_name = "United Kingdom" if country_number == 3
replace country_name = "France" if country_number == 4
replace country_name = "China" if country_number == 5
replace country_name = "India" if country_number == 6
replace country_name = "Pakistan" if country_number == 7
replace country_name = "North Korea" if country_number == 8
label variable country_name "Country name"
drop country_number


** Order variables and observations:
order country_name year nuclear_weapons_tests
sort country_name year


** Export data:
save "Arms Control Association 2020 nuclear weapons tests/nuclear_weapons_tests_states.dta", replace
export delimited "Arms Control Association 2020 nuclear weapons tests/nuclear_weapons_tests_states.csv", replace



exit

