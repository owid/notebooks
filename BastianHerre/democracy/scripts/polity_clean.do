*****  This Stata do-file cleans the Polity 5 dataset
*****  Author: Bastian Herre
*****  June 28, 2022


version 14

clear all
set more off
set varabbrev off


** Set your own working directories here to run the file:
cd "/Users/bastianherre/Dropbox/Data/"
global project "/Users/bastianherre/Dropbox/Data/"


** Download dataset from http://www.systemicpeace.org/inscr/p5v2018.xls and move it into the folder "Polity 5 2021":


** Import Freedom House territory dataset:
import excel "Polity 5 2021/p5v2018-2.xls", firstrow


** Keep variables of interest:
keep country year polity2 xrcomp xropen xconst parreg parcomp ccode


** Rename and relabel variables of interest:

rename country country_name
label variable country_name "Country name"

label variable year "Year"

rename polity2 democracy_polity
label variable democracy_polity "Democracy (Polity)"

rename xrcomp exec_reccomp_polity
label variable exec_reccomp_polity "Competitiveness of executive recruitment (Polity)"

rename xropen exec_recopen_polity
label variable exec_recopen_polity "Openness of executive recruitment (Polity)"

rename xconst exec_constr_polity
label variable exec_constr_polity "Constraints on the executive (Polity)"

rename parreg polpart_reg_polity
label variable polpart_reg_polity "Regulation of political participation (Polity)"

rename parcomp polpart_comp_polity
label variable polpart_comp_polity "Competitiveness of political participation (Polity)"


** Recode values of polity score in line with rules on page 17 of: Marshall, Monty G., and Ted Robert Gurr. 2020. Polity 5: Political Regime Characteristics and Transitions, 1800-2018. Dataset Users' Manual. 
replace democracy_polity = . if democracy_polity == -66
replace democracy_polity = . if democracy_polity == -88 & country_name == "Belgium" & year == 1830


** Refine indicators:
recode exec_reccomp_polity exec_recopen_polity exec_constr_polity polpart_reg_polity polpart_comp_polity (-88 = .) (-77 = .) (-66 = .)

label define exec_reccomp_polity 0 "power seized" 1 "elite selection" 2 "dual or transitional" 3 "election"
label values exec_reccomp_polity exec_reccomp_polity

label define exec_recopen_polity 0 "power seized" 1 "hereditary succession" 2 "dual, chief minister designated" 3 "dual, chief minister elected" 4 "open"
label values exec_recopen_polity exec_recopen_polity

label define exec_constr_polity 1 "unconstrained" 3 "slight to moderate"  5 "substantial" 7 "executive parity or subordination"
label values exec_constr_polity exec_constr_polity

label define polpart_reg_polity 1 "unregulated" 2 "multiple identities" 3 "sectarian" 4 "restricted" 5 "unrestricted and stable"
label values polpart_reg_polity polpart_reg_polity

label define polpart_comp_polity 0 "unregulated" 1 "repressed" 2 "suppressed" 3 "factional" 4 "transitional" 5 "competitive"
label values polpart_comp_polity polpart_comp_polity


** Generate regime variables as per the (conventional) rules here: https://www.systemicpeace.org/polityproject.html
generate regime_polity = .
replace regime_polity = 0 if democracy_polity >= -10 & democracy_polity <= -6
replace regime_polity = 1 if democracy_polity >= -5 & democracy_polity <= 5
replace regime_polity = 2 if democracy_polity >= 6 & democracy_polity <= 10

label variable regime_polity "Political regime (Polity)"
label define regime_polity 0 "autocracy" 1 "anocracy" 2 "democracy"
label values regime_polity regime_polity

order regime_polity, after(democracy_polity)


** Delete duplicate observations:
drop if country_name == "Ethiopia" & year == 1993 & ccode == 530 // Eritrea separates during 1993, I keep the entity at the end of the year.
drop if country_name == "Yugoslavia" & year == 1991 & ccode == 345 // Yugoslavia splits during 1991, I keep the entity at the end of the year.
drop if country_name == "Sudan" & year == 2011 // South Sudan separates during 2011, I keep the entity at the end of the year.
drop ccode

** Format country names:
replace country_name = "Bosnia and Herzegovina" if country_name == "Bosnia"
replace country_name = "Congo" if country_name == "Congo Brazzaville"
replace country_name = "Democratic Republic of Congo" if country_name == "Congo Kinshasa"
replace country_name = "Congo" if country_name == "Congo-Brazzaville"
replace country_name = "Cote d'Ivoire" if country_name == "Cote D'Ivoire"
replace country_name = "Czechia" if country_name == "Czech Republic"
replace country_name = "East Germany" if country_name == "Germany East"
replace country_name = "West Germany" if country_name == "Germany West"
replace country_name = "Cote d'Ivoire" if country_name == "Ivory Coast"
replace country_name = "North Korea" if country_name == "Korea North"
replace country_name = "South Korea" if country_name == "Korea South"
replace country_name = "North Macedonia" if country_name == "Macedonia"
replace country_name = "Myanmar" if country_name == "Myanmar (Burma)"
replace country_name = "Slovakia" if country_name == "Slovak Republic"
replace country_name = "Republic of Vietnam" if country_name == "South Vietnam"
replace country_name = "Sudan" if country_name == "Sudan-North"
replace country_name = "Eswatini" if country_name == "Swaziland"
replace country_name = "Timor" if country_name == "Timor Leste"
replace country_name = "United Arab Emirates" if country_name == "UAE"
replace country_name = "United Province of Canada" if country_name == "United Province CA"
replace country_name = "United States" if country_name == "United States                   "
replace country_name = "North Vietnam" if country_name == "Vietnam North"
replace country_name = "Wuerttemberg" if country_name == "Wuerttemburg"
replace country_name = "Yemen Arab Republic" if country_name == "Yemen North"
replace country_name = "Yemen People's Republic" if country_name == "Yemen South"
replace country_name = "United Korea" if country_name == "Korea"
replace country_name = "Wuerttemburg" if country_name == "Wuerttemberg"
replace country_name = "Great Colombia" if country_name == "Gran Colombia"


** Export datasets:
save "democracy/datasets/cleaned/polity_cleaned.dta", replace
export delimited "democracy/datasets/cleaned/polity_cleaned.csv", replace nolabel



exit
