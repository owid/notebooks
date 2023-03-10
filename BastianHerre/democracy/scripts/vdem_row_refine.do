*****  This Stata do-file refines the variables in the V-Dem and RoW data
*****  Author: Bastian Herre
*****  March 1, 2023

version 14
clear all
set more off
set varabbrev off


** Set your own working directories here to run the file:
cd "/Users/bastianherre/Dropbox/Data/"
global project "/Users/bastianherre/Dropbox/Data/"


** Import data:
use "democracy/datasets/imputed/vdem_row_imputed.dta"


** Create numeric country identifier:
encode country_name, generate(country_number)


** Declare dataset to be time-series data:
tsset country_number year


** Create variable for age of electoral democracies:
generate electdem_age_row_owid = .
replace electdem_age_row_owid = 0 if regime_row_owid == 0 | regime_row_owid == 1
replace electdem_age_row_owid = 1 if (l.regime_row_owid == 0 | l.regime_row_owid == 1) & (regime_row_owid == 2 | regime_row_owid == 3)
replace electdem_age_row_owid = 1 if l.regime_row_owid == . & (regime_row_owid == 2 | regime_row_owid == 3) // Assume that when previous information is missing, the country was not an electoral democracy.
replace electdem_age_row_owid = l.electdem_age_row_owid + 1 if electdem_age_row_owid == . & (regime_row_owid == 2 | regime_row_owid == 3)
label variable electdem_age_row_owid "Electoral democracy age (Regimes of the World, OWID)"
order electdem_age_row_owid, after(regime_row_owid)


** Create variable for age of liberal democracies:
generate libdem_age_row_owid = .
replace libdem_age_row_owid = 0 if regime_row_owid == 0 | regime_row_owid == 1 | regime_row_owid == 2
replace libdem_age_row_owid = 1 if (l.regime_row_owid == 0 | l.regime_row_owid == 1 | l.regime_row_owid == 2) & regime_row_owid == 3
replace libdem_age_row_owid = 1 if l.regime_row_owid == . & regime_row_owid == 3 // Assume that when previous information is missing, the country was not a liberal democracy.
replace libdem_age_row_owid = l.libdem_age_row_owid + 1 if libdem_age_row_owid == . & regime_row_owid == 3
label variable libdem_age_row_owid "Liberal democracy age (Regimes of the World, OWID)"
order libdem_age_row_owid, after(electdem_age_row_owid)

drop country_number


** Create variable for experience with electoral democracy:
generate electdem_row_owid = .
replace electdem_row_owid = 0 if regime_row_owid == 0 | regime_row_owid == 1
replace electdem_row_owid = 1 if regime_row_owid == 2 | regime_row_owid == 3

generate electdem_exp_row_owid = .
bysort country_name: replace electdem_exp_row_owid = sum(electdem_row_owid) if regime_row_owid != .
drop electdem_row_owid

label variable electdem_exp_row_owid "Experience with electoral democracy (Regimes of the World, OWID)"


** Create variable for experience with liberal democracy:
generate libdem_row_owid = .
replace libdem_row_owid = 0 if regime_row_owid == 0 | regime_row_owid == 1 | regime_row_owid == 2
replace libdem_row_owid = 1 if regime_row_owid == 3

generate libdem_exp_row_owid = .
bysort country_name: replace libdem_exp_row_owid = sum(libdem_row_owid) if regime_row_owid != .
drop libdem_row_owid

label variable libdem_exp_row_owid "Experience with liberal democracy (Regimes of the World, OWID)"


** Create variable for age group of electoral demcoracies:
generate electdem_age_group_row_owid = .
replace electdem_age_group_row_owid = 0 if regime_row_owid == 0
replace electdem_age_group_row_owid = 1 if regime_row_owid == 1
replace electdem_age_group_row_owid = 2 if electdem_age_row_owid > 0 & electdem_age_row_owid <= 18
replace electdem_age_group_row_owid = 3 if electdem_age_row_owid > 18 & electdem_age_row_owid <= 30
replace electdem_age_group_row_owid = 4 if electdem_age_row_owid > 30 & electdem_age_row_owid <= 60
replace electdem_age_group_row_owid = 5 if electdem_age_row_owid > 60 & electdem_age_row_owid <= 90
replace electdem_age_group_row_owid = 6 if electdem_age_row_owid > 90 & electdem_age_row_owid < .
label variable electdem_age_group_row_owid "Electoral democracy age group (Regimes of the World, OWID)"
label define electdem_age_group_row_owid 0 "closed autocracy" 1"electoral autocracy" 2 "1-18 years" 3 "19-30 years" 4 "31-60 years" 5 "61-90 years" 6 "91+ years"
label values electdem_age_group_row_owid electdem_age_group_row_owid
order electdem_age_group_row_owid, after(electdem_age_row_owid)


** Create variable for age group of liberal democracies:
generate libdem_age_group_row_owid = .
replace libdem_age_group_row_owid = 0 if regime_row_owid == 0
replace libdem_age_group_row_owid = 1 if regime_row_owid == 1
replace libdem_age_group_row_owid = 2 if regime_row_owid == 2
replace libdem_age_group_row_owid = 3 if libdem_age_row_owid > 0 & libdem_age_row_owid <= 18
replace libdem_age_group_row_owid = 4 if libdem_age_row_owid > 18 & libdem_age_row_owid <= 30
replace libdem_age_group_row_owid = 5 if libdem_age_row_owid > 30 & libdem_age_row_owid <= 60
replace libdem_age_group_row_owid = 6 if libdem_age_row_owid > 60 & libdem_age_row_owid <= 90
replace libdem_age_group_row_owid = 7 if libdem_age_row_owid > 90 & libdem_age_row_owid < .
label variable libdem_age_group_row_owid "Liberal democracy age group (Regimes of the World, OWID)"
label define libdem_age_group_row_owid 0 "closed autocracy" 1 "electoral autocracy" 2 "electoral democracy" 3 "1-18 years" 4 "19-30 years" 5 "31-60 years" 6 "61-90 years" 7 "91+ years"
label values libdem_age_group_row_owid libdem_age_group_row_owid
order libdem_age_group_row_owid, after(libdem_age_row_owid)


** Add labels for ages of electoral and liberal democracies to optimize use in the OWID grapher:
tostring electdem_age_row_owid, replace
replace electdem_age_row_owid = "no data" if electdem_age_row_owid == "."
replace electdem_age_row_owid = "closed autocracy" if regime_row_owid == 0
replace electdem_age_row_owid = "electoral autocracy" if regime_row_owid == 1

tostring libdem_age_row_owid, replace
replace libdem_age_row_owid = "no data" if libdem_age_row_owid == "."
replace libdem_age_row_owid = "closed autocracy" if regime_row_owid == 0
replace libdem_age_row_owid = "electoral autocracy" if regime_row_owid == 1
replace libdem_age_row_owid = "electoral democracy" if regime_row_owid == 2


** Create variable for women's political representation:
generate wom_parl_gr_vdem_owid = .
replace wom_parl_gr_vdem_owid = 0 if wom_parl_vdem_owid == 0
replace wom_parl_gr_vdem_owid = 1 if wom_parl_vdem_owid > 0 & wom_parl_vdem_owid < 10
replace wom_parl_gr_vdem_owid = 2 if wom_parl_vdem_owid >= 10 & wom_parl_vdem_owid < 20
replace wom_parl_gr_vdem_owid = 3 if wom_parl_vdem_owid >= 20 & wom_parl_vdem_owid < 30
replace wom_parl_gr_vdem_owid = 4 if wom_parl_vdem_owid >= 30 & wom_parl_vdem_owid < 40
replace wom_parl_gr_vdem_owid = 5 if wom_parl_vdem_owid >= 40 & wom_parl_vdem_owid < .
label variable wom_parl_gr_vdem_owid "Women's political representation (grouped, V-Dem, OWID)"
label define wom_parl_gr_vdem_owid 0 "no women" 1 "0-10% women" 2 "10%-20% women" 3 "20%-30% women" 4 "30%-40% women" 5 "40%+ women"


** Export data:
save "democracy/datasets/refined/vdem_row_refined.dta", replace
export delimited "democracy/datasets/refined/vdem_row_refined.csv", replace nolabel



exit
