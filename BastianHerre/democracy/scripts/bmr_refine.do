*****  This Stata do-file refines the variables in the BMR dataset
*****  Author: Bastian Herre
*****  April 22, 2022

version 14
clear all
set more off
set varabbrev off


** Set your own working directories here to run the file:
cd "/Users/bastianherre/Dropbox/Data/"
global project "/Users/bastianherre/Dropbox/Data/"


** Import data:
use "democracy/datasets/imputed/bmr_imputed.dta"


** Refine regime variable capturing women's suffrage:
replace regime_womsuffr_bmr_owid = . if regime_bmr_owid == . // I do this to code times of foreign occupation and civil war as missing values instead of continuations of the previous regime type.

** Create numeric country identifier:
encode country_name, generate(country_number)


** Declare dataset to be time-series data:
tsset country_number year


** Create variable for age of democracies:
generate dem_age_bmr_owid = .
replace dem_age_bmr_owid = 0 if regime_bmr_owid == 0
replace dem_age_bmr_owid = 1 if l.regime_bmr_owid == 0 & regime_bmr_owid == 1
replace dem_age_bmr_owid = 1 if l.regime_bmr_owid == . & regime_bmr_owid == 1 // Assume that when previous information is missing, the country was not an electoral democracy.
replace dem_age_bmr_owid = l.dem_age_bmr_owid + 1 if dem_age_bmr_owid == . & regime_bmr_owid == 1
label variable dem_age_bmr_owid "Democracy age (BMR, OWID)"
order dem_age_bmr_owid, after(regime_bmr_owid)


** Create variable for age of democracies with women's suffrage:
generate dem_ws_age_bmr_owid = .
replace dem_ws_age_bmr_owid = 0 if regime_womsuffr_bmr_owid == 0
replace dem_ws_age_bmr_owid = 1 if l.regime_womsuffr_bmr_owid == 0 & regime_womsuffr_bmr_owid == 1
replace dem_ws_age_bmr_owid = 1 if l.regime_womsuffr_bmr_owid == . & regime_womsuffr_bmr_owid == 1 // Assume that when previous information is missing, the country was not an electoral democracy.
replace dem_ws_age_bmr_owid = l.dem_ws_age_bmr_owid + 1 if dem_ws_age_bmr_owid == . & regime_womsuffr_bmr_owid == 1
label variable dem_ws_age_bmr_owid "Democracy age, including women's suffrage (BMR, OWID)"
order dem_ws_age_bmr_owid, after(regime_womsuffr_bmr_owid)

drop country_number


** Create variable for experience with democracy:
generate dem_exp_bmr_owid = .
bysort country_name: replace dem_exp_bmr_owid = sum(regime_bmr_owid) if regime_bmr_owid != .

label variable dem_exp_bmr_owid "Experience with democracy (BMR, OWID)"


** Create variable for experience with democracy with women's suffrage:
generate dem_ws_exp_bmr_owid = .
bysort country_name: replace dem_ws_exp_bmr_owid = sum(regime_womsuffr_bmr_owid) if regime_womsuffr_bmr_owid != .

label variable dem_ws_exp_bmr_owid "Experience with democracy, including women's suffrage (BMR, OWID)"


** Create variable for age group of democracies:
generate dem_age_group_bmr_owid = .
replace dem_age_group_bmr_owid = 0 if regime_bmr_owid == 0
replace dem_age_group_bmr_owid = 1 if dem_age_bmr_owid > 0 & dem_age_bmr_owid <= 18
replace dem_age_group_bmr_owid = 2 if dem_age_bmr_owid > 18 & dem_age_bmr_owid <= 30
replace dem_age_group_bmr_owid = 3 if dem_age_bmr_owid > 30 & dem_age_bmr_owid <= 60
replace dem_age_group_bmr_owid = 4 if dem_age_bmr_owid > 60 & dem_age_bmr_owid <= 90
replace dem_age_group_bmr_owid = 5 if dem_age_bmr_owid > 90 & dem_age_bmr_owid < .
label variable dem_age_group_bmr_owid "Democracy age group (BMR, OWID)"
label define dem_age_group_bmr_owid 0 "non-democracy" 1 "1-18 years" 2 "19-30 years" 3 "31-60 years" 4 "61-90 years" 5 "91+ years"
label values dem_age_group_bmr_owid dem_age_group_bmr_owid
order dem_age_group_bmr_owid, after(dem_age_bmr_owid)


** Create variable for age group of democracies with women's suffrage:
generate dem_ws_age_group_bmr_owid = .
replace dem_ws_age_group_bmr_owid = 0 if regime_womsuffr_bmr_owid == 0
replace dem_ws_age_group_bmr_owid = 1 if dem_ws_age_bmr_owid > 0 & dem_ws_age_bmr_owid <= 18
replace dem_ws_age_group_bmr_owid = 2 if dem_ws_age_bmr_owid > 18 & dem_ws_age_bmr_owid <= 30
replace dem_ws_age_group_bmr_owid = 3 if dem_ws_age_bmr_owid > 30 & dem_ws_age_bmr_owid <= 60
replace dem_ws_age_group_bmr_owid = 4 if dem_ws_age_bmr_owid > 60 & dem_ws_age_bmr_owid <= 90
replace dem_ws_age_group_bmr_owid = 5 if dem_ws_age_bmr_owid > 90 & dem_ws_age_bmr_owid < .
label variable dem_ws_age_group_bmr_owid "Democracy age group, including women's suffrage (BMR, OWID)"
label values dem_ws_age_group_bmr_owid dem_age_group_bmr_owid
order dem_ws_age_group_bmr_owid, after(dem_ws_age_bmr_owid)


** Add labels for ages of BMR democracies to optimize use in the OWID grapher:
tostring dem_age_bmr_owid, replace
replace dem_age_bmr_owid = "no data" if dem_age_bmr_owid == "."
replace dem_age_bmr_owid = "non-democracy" if regime_bmr_owid == 0

tostring dem_ws_age_bmr_owid, replace
replace dem_ws_age_bmr_owid = "no data" if dem_ws_age_bmr_owid == "."
replace dem_ws_age_bmr_owid = "non-democracy" if regime_womsuffr_bmr_owid == 0

** Export data:
save "democracy/datasets/refined/bmr_refined.dta", replace
export delimited "democracy/datasets/refined/bmr_refined.csv", replace



exit
