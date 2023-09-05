*****  This Stata do-file prepares the monadic version of the Strategic Nuclear Forces Dataset by Kyungwon Suh for analysis
*****  Author: Bastian Herre
*****  September 5, 2023

version 14
clear all
set more off
set varabbrev off


** Set your own working directories here to run the file:
cd "/Users/bastianherre/Dropbox/Data/"
global project "/Users/bastianherre/Dropbox/Data/"


** Download V-Dem dataset from https://www.v-dem.net/vdemds.html and move it into the folder "Varieties of Democracy v12"
** Import V-Dem dataset:
import excel "Suh 2022 strategic nuclear forces/snforce_monadic.xlsx", firstrow clear


** Keep variables of interest:
drop monadicCMP


** Rename variables of interest:
rename warheads nuclear_warheads_stockpile
rename monadicdnuke nuclear_warheads_firststrike
rename monadicEMT nuclwarh_firststr_yield


** Label variables of interest:
label variable nuclear_warheads_stockpile "Stockpiled nuclear warheads"
label variable nuclear_warheads_firststrike "Strategic nuclear warheads deliverable in first strike"
label variable nuclwarh_firststr_yield "Megatons of nuclear warheads deliverable in first strike"


** Replace variable with country codes with variable for country names:
generate country_name = ""
replace country_name = "United States" if ccode == 2
replace country_name = "United Kingdom" if ccode == 200
replace country_name = "France" if ccode == 220
replace country_name = "Russia" if ccode == 365
replace country_name = "South Africa" if ccode == 560
replace country_name = "Israel" if ccode == 666
replace country_name = "China" if ccode == 710
replace country_name = "India" if ccode == 750
replace country_name = "Pakistan" if ccode == 770
drop ccode


** Create additional variable of interest:
generate nuclwarh_firststr_area = nuclwarh_firststr_yield * 51.7

label variable nuclwarh_firststr_area "Destroyable area by nuclear weapons deliverable in first strike (in km2)"


** Order variables and observations:
order country_name, before(year)
sort country_name year


** Export data:
save "Suh 2022 strategic nuclear forces/nuclear_weapons_forces.dta", replace
export delimited "Suh 2022 strategic nuclear forces/nuclear_weapons_forces.csv", replace

describe, replace
keep name varlab
rename name varname
rename varlab varlabel
export delimited "Suh 2022 strategic nuclear forces/nuclear_weapons_forces_meta.csv", replace



exit
