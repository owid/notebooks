*****  This Stata do-file refines the variables in the LIED dataset
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
use "democracy/datasets/cleaned/lied_cleaned.dta"


** Create numeric country identifier:
encode country_name, generate(country_number)


** Declare dataset to be time-series data:
tsset country_number year


** Create variable for age of electoral democracies:
generate electdem_age_lied = .
replace electdem_age_lied = 0 if regime_lied == 0 | regime_lied == 1 | regime_lied == 2 | regime_lied == 3 | regime_lied == 4 | regime_lied == 5
replace electdem_age_lied = 1 if (l.regime_lied == 0 | l.regime_lied == 1 | l.regime_lied == 2 | l.regime_lied == 3 | l.regime_lied == 4 | l.regime_lied == 5) & (regime_lied == 6 | regime_lied == 7)
replace electdem_age_lied = 1 if l.regime_lied == . & (regime_lied == 6 | regime_lied == 7) // Assume that when previous information is missing, the country was not an electoral democracy.
replace electdem_age_lied = l.electdem_age_lied + 1 if electdem_age_lied == . & (regime_lied == 6 | regime_lied == 7)
label variable electdem_age_lied "Electoral democracy age (LIED)"
order electdem_age_lied, after(regime_lied)


** Create variable for age of polyarchies:
generate polyarchy_age_lied = .
replace polyarchy_age_lied = 0 if regime_lied == 0 | regime_lied == 1 | regime_lied == 2 | regime_lied == 3 | regime_lied == 4 | regime_lied == 5 | regime_lied == 6
replace polyarchy_age_lied = 1 if (l.regime_lied == 0 | l.regime_lied == 1 | l.regime_lied == 2 | l.regime_lied == 3 | l.regime_lied == 4 | l.regime_lied == 5 | l.regime_lied == 6) & regime_lied == 7
replace polyarchy_age_lied = 1 if l.regime_lied == . & regime_lied == 7 // Assume that when previous information is missing, the country was not a polyarchy.
replace polyarchy_age_lied = l.polyarchy_age_lied + 1 if polyarchy_age_lied == . & regime_lied == 7
label variable polyarchy_age_lied "Polyarchy age (LIED)"
order polyarchy_age_lied, after(electdem_age_lied)

drop country_number


** Create variable for experience with electoral democracy:
generate electdem_lied = .
replace electdem_lied = 0 if regime_lied == 0 | regime_lied == 1 | regime_lied == 2 | regime_lied == 3 | regime_lied == 4 | regime_lied == 5
replace electdem_lied = 1 if regime_lied == 6 | regime_lied == 7

generate electdem_exp_lied = .
bysort country_name: replace electdem_exp_lied = sum(electdem_lied) if regime_lied != .
drop electdem_lied

label variable electdem_exp_lied "Experience with electoral democracy (LIED)"


** Create variable for experience with polyarchy:
generate polyarchy_lied = .
replace polyarchy_lied = 0 if regime_lied == 0 | regime_lied == 1 | regime_lied == 2 | regime_lied == 3 | regime_lied == 4 | regime_lied == 5 | regime_lied == 6
replace polyarchy_lied = 1 if regime_lied == 7

generate polyarchy_exp_lied = .
bysort country_name: replace polyarchy_exp_lied = sum(polyarchy_lied) if regime_lied != .
drop polyarchy_lied

label variable polyarchy_exp_lied "Experience with polyarchy (LIED)"


** Create variable for age group of electoral demcoracies:
generate electdem_age_group_lied = .
replace electdem_age_group_lied = 0 if regime_lied == 0
replace electdem_age_group_lied = 1 if regime_lied == 1
replace electdem_age_group_lied = 2 if regime_lied == 2
replace electdem_age_group_lied = 3 if regime_lied == 3
replace electdem_age_group_lied = 4 if regime_lied == 4
replace electdem_age_group_lied = 5 if regime_lied == 5
replace electdem_age_group_lied = 6 if electdem_age_lied > 0 & electdem_age_lied <= 18
replace electdem_age_group_lied = 7 if electdem_age_lied > 18 & electdem_age_lied <= 30
replace electdem_age_group_lied = 8 if electdem_age_lied > 30 & electdem_age_lied <= 60
replace electdem_age_group_lied = 9 if electdem_age_lied > 60 & electdem_age_lied <= 90
replace electdem_age_group_lied = 10 if electdem_age_lied > 90 & electdem_age_lied < .
label variable electdem_age_group_lied "Electoral democracy age group (Regimes of the World, OWID)"
label define electdem_age_group_lied 0 "non-electoral autocracy" 1 "one-party autocracy" 2 "multi-party autocracy without elected executive" 3 "multi-party autocracy" 4 "exclusive democracy" 5 "male democracy" 6 "1-18 years" 7 "19-30 years" 8 "31-60 years" 9 "61-90 years" 10 "91+ years"
label values electdem_age_group_lied electdem_age_group_lied
order electdem_age_group_lied, after(electdem_age_lied)


** Create variable for age group of polyarchies:
generate polyarchy_age_group_lied = .
replace polyarchy_age_group_lied = 0 if regime_lied == 0
replace polyarchy_age_group_lied = 1 if regime_lied == 1
replace polyarchy_age_group_lied = 2 if regime_lied == 2
replace polyarchy_age_group_lied = 3 if regime_lied == 3
replace polyarchy_age_group_lied = 4 if regime_lied == 4
replace polyarchy_age_group_lied = 5 if regime_lied == 5
replace polyarchy_age_group_lied = 6 if regime_lied == 6
replace polyarchy_age_group_lied = 7 if polyarchy_age_lied > 0 & polyarchy_age_lied <= 18
replace polyarchy_age_group_lied = 8 if polyarchy_age_lied > 18 & polyarchy_age_lied <= 30
replace polyarchy_age_group_lied = 9 if polyarchy_age_lied > 30 & polyarchy_age_lied <= 60
replace polyarchy_age_group_lied = 10 if polyarchy_age_lied > 60 & polyarchy_age_lied <= 90
replace polyarchy_age_group_lied = 11 if polyarchy_age_lied > 90 & polyarchy_age_lied < .
label variable polyarchy_age_group_lied "Polyarchy age group (Regimes of the World, OWID)"
label define polyarchy_age_group_lied 0 "non-electoral autocracy" 1 "one-party autocracy" 2 "multi-party autocracy without elected executive" 3 "multi-party autocracy" 4 "exclusive democracy" 5 "male democracy" 6 "electoral democracy" 7 "1-18 years" 8 "19-30 years" 9 "31-60 years" 10 "61-90 years" 11 "91+ years"
label values polyarchy_age_group_lied polyarchy_age_group_lied
order polyarchy_age_group_lied, after(polyarchy_age_lied)


** Add labels for ages of electoral democracies and polyarchies to optimize use in the OWID grapher:
tostring electdem_age_lied, replace
replace electdem_age_lied = "no data" if electdem_age_lied == "."
replace electdem_age_lied = "non-electoral autocracy" if regime_lied == 0
replace electdem_age_lied = "one-party autocracy" if regime_lied == 1
replace electdem_age_lied = "multi-party autocracy without elected executive" if regime_lied == 2
replace electdem_age_lied = "multi-party autocracy" if regime_lied == 3
replace electdem_age_lied = "exclusive democracy" if regime_lied == 4
replace electdem_age_lied = "male democracy" if regime_lied == 5

tostring polyarchy_age_lied, replace
replace polyarchy_age_lied = "no data" if polyarchy_age_lied == "."
replace polyarchy_age_lied = "non-electoral autocracy" if regime_lied == 0
replace polyarchy_age_lied = "one-party autocracy" if regime_lied == 1
replace polyarchy_age_lied = "multi-party autocracy without elected executive" if regime_lied == 2
replace polyarchy_age_lied = "multi-party autocracy" if regime_lied == 3
replace polyarchy_age_lied = "exclusive democracy" if regime_lied == 4
replace polyarchy_age_lied = "male democracy" if regime_lied == 5
replace polyarchy_age_lied = "electoral democracy" if regime_lied == 6


** Export data:
save "democracy/datasets/refined/lied_refined.dta", replace
export delimited "democracy/datasets/refined/lied_refined.csv", replace nolabel



exit
