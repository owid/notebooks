*****  This Stata do-file cleans the Boix-Miller-Rosato (BMR) democracy dataset
*****  Author: Bastian Herre
*****  June 28, 2022

version 14
clear all
set more off
set varabbrev off


** Set your own working directories here to run the file:
cd "/Users/bastianherre/Dropbox/Data/"
global project "/Users/bastianherre/Dropbox/Data/"


** Download data from https://sites.google.com/site/mkmtwo/data?authuser=0 and move it into the folder "Boix-Miller-Rosato v4"
** Import data:
use "Boix-Miller-Rosato v4/democracy-v4.0.dta", replace


** Harmonize BMR country names with OWID names:
generate country_name = country
collapse (first) country, by(country_name)
preserve
keep country
sort country
export delimited "democracy/datasets/cleaned/bmr_countries.csv", replace
restore

* I use the OWID-internal country-name-standardizer tool, which creates a file bith BMR's country names and the respective OWID names:

import delimited "democracy/datasets/cleaned/supplement/bmr_countries_standardized.csv", clear varnames(1) // The file is in the GitHub folder.
erase "democracy/datasets/cleaned/bmr_countries.csv"

rename ourworldindataname country_name

** Harmonize remaining incorrectly formatted country names:
replace country_name = "Piedmont-Sardinia" if country_name == "Sardinia"
replace country_name = "Republic of Vietnam" if country_name == "South Vietnam"

replace country_name = "North Vietnam" if country == "VIETNAM, NORTH"
replace country_name = "Yugoslavia" if country == "YUGOSLAVIA"
replace country_name = "United Korea" if country == "KOREA"


** Save list of original and harmonized BMR country names:
save "democracy/datasets/cleaned/bmr_countries_standardized.dta", replace


** Import BMR data again:
use "Boix-Miller-Rosato v4/democracy-v4.0.dta", replace


** Merge with harmonized country names:
merge m:1 country using "democracy/datasets/cleaned/bmr_countries_standardized.dta"
drop _merge
erase "democracy/datasets/cleaned/bmr_countries_standardized.dta"


** Identify duplicate observations:
sort country_name year
duplicates tag country_name year, generate(duplicate)
list if duplicate == 1 // duplicates are of Germany/West Germany in 1945 and 1990, and Yugoslavia/Serbia in 1991 and 2006.
drop if ccode == 260 & year == 1945
drop if ccode == 260 & year == 1990
drop if ccode == 345 & year == 1991
drop if ccode == 347 & year == 2006


** Keep variables of interest:
keep country_name year democracy_omitteddata democracy_femalesuffrage // I use 'democracy_omitteddata' instead of 'democracy' because the former codes times of foreign occupation and civil war as missing values instead of continuations of the previous regime type.


** Rename variables of interest:
rename democracy_omitteddata regime_bmr
rename democracy_femalesuffrage regime_womsuffr_bmr


** Relabel variables of interest:
label variable country_name "Country name"
label variable year "Year"
label variable regime_bmr "Political regime (BMR)"
label variable regime_womsuffr_bmr "Political regime (with women's suffrage, BMR)"


** Order variables and observations:
order country_name year
sort country_name year


** Export data:
save "democracy/datasets/cleaned/bmr_cleaned.dta", replace
export delimited "democracy/datasets/cleaned/bmr_cleaned.csv", replace



exit
