*****  This Stata do-file refines the variables in the Polity 5 dataset
*****  Author: Bastian Herre
*****  June 28, 2022

version 14
clear all
set more off
set varabbrev off


** Set your own working directories here to run the file:
cd "/Users/bastianherre/Dropbox/Data/"
global project "/Users/bastianherre/Dropbox/Data/"


** Import data:
use "democracy/datasets/cleaned/polity_cleaned.dta"


** Create numeric country identifier:
encode country_name, generate(country_number)


** Declare dataset to be time-series data:
tsset country_number year


** Create alternative version of democracy index with only positive values:
generate democracy_recod_polity = democracy_polity + 10

label variable democracy_recod_polity "Democracy (Polity, recoded 0-20)"


** Create variable for age of democracies:
generate dem_age_polity = .
replace dem_age_polity = 0 if regime_polity == 0 | regime_polity == 1
replace dem_age_polity = 1 if (l.regime_polity == 0 | l.regime_polity == 1) & regime_polity == 2
replace dem_age_polity = 1 if l.regime_polity == . & regime_polity == 2 // Assume that when previous information is missing, the country was not a democracy.
replace dem_age_polity = l.dem_age_polity + 1 if dem_age_polity == . & regime_polity == 2
label variable dem_age_polity "Democracy age (Polity)"
order dem_age_polity, after(regime_polity)

drop country_number


** Create variable for experience with democracy:
generate dem_polity = .
replace dem_polity = 0 if regime_polity == 0 | regime_polity == 1
replace dem_polity = 1 if regime_polity == 2

generate dem_exp_polity = .
bysort country_name: replace dem_exp_polity = sum(dem_polity) if regime_polity != .
drop dem_polity

label variable dem_exp_polity "Experience with democracy (Polity)"


** Create variable for age group of demcoracies:
generate dem_age_group_polity = .
replace dem_age_group_polity = 0 if regime_polity == 0
replace dem_age_group_polity = 1 if regime_polity == 1
replace dem_age_group_polity = 2 if dem_age_polity > 0 & dem_age_polity <= 18
replace dem_age_group_polity = 3 if dem_age_polity > 18 & dem_age_polity <= 30
replace dem_age_group_polity = 4 if dem_age_polity > 30 & dem_age_polity <= 60
replace dem_age_group_polity = 5 if dem_age_polity > 60 & dem_age_polity <= 90
replace dem_age_group_polity = 6 if dem_age_polity > 90 & dem_age_polity < .
label variable dem_age_group_polity "Democracy age group (Polity)"
label define dem_age_group_polity 0 "autocracy" 1 "anocracy" 2 "1-18 years" 3 "19-30 years" 4 "31-60 years" 5 "61-90 years" 6 "91+ years"
label values dem_age_group_polity dem_age_group_polity
order dem_age_group_polity, after(dem_age_polity)


** Add labels for age of democracies to optimize use in the OWID grapher:
tostring dem_age_polity, replace
replace dem_age_polity = "no data" if dem_age_polity == "."
replace dem_age_polity = "autocracy" if regime_polity == 0
replace dem_age_polity = "anocracy" if regime_polity == 1


** Export data:
save "democracy/datasets/refined/polity_refined.dta", replace
export delimited "democracy/datasets/refined/polity_refined.csv", replace nolabel



exit
