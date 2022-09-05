*****  This Stata do-file cleans the Episodes of Regime Transformation (ERT) dataset
*****  Author: Bastian Herre
*****  August 31, 2022

version 14
clear all
set more off
set varabbrev off


** Set your own working directories here to run the file:
cd "/Users/bastianherre/Dropbox/Data/"
global project "/Users/bastianherre/Dropbox/Data/"


** Download data from https://github.com/vdeminstitute/ERT/blob/master/inst/ERT.csv and move it into the folder "Episodes of Regime Transformation v4"
** Import data:
import delimited "Episodes of Regime Transformation v4/ERT.csv", clear varnames(1)


** Keep variables of interest:
keep country_name year reg_type dem_ep aut_ep dem_ep_outcome dem_ep_end_year aut_ep_outcome aut_ep_end_year


** Rename and relabel variables of interest:
rename reg_type regime_dich_ert

label variable country_name "Country name"
label variable year "Year"
label variable regime_dich_ert "Political regime (ERT, dichotomous)"


** Refine country names:
replace country_name = "Myanmar" if country_name == "Burma/Myanmar"
replace country_name = "Democratic Republic of Congo" if country_name == "Democratic Republic of the Congo"
replace country_name = "Cote d'Ivoire" if country_name == "Ivory Coast"
replace country_name = "Congo" if country_name == "Republic of the Congo"
replace country_name = "Gambia" if country_name == "The Gambia"
replace country_name = "Palestine" if country_name == "Palestine/British Mandate"
replace country_name = "Timor" if country_name == "Timor-Leste"
replace country_name = "United States" if country_name == "United States of America"
replace country_name = "Czechia" if country_name == "Czech Republic"
replace country_name = "East Germany" if country_name == "German Democratic Republic"
replace country_name = "Yemen People's Republic" if country_name == "South Yemen"


** Refine dichotomous regime-type variable:
destring regime_dich_ert, force replace
label define regime_dich_ert 0 "autocracy" 1 "democracy"
label values regime_dich_ert regime_dich_ert


** Refine regime-type variable:
tab dem_ep aut_ep
list if dem_ep == 1 & aut_ep == 1

generate regime_ert = 0 if regime_dich_ert == 0 & aut_ep == 1 & dem_ep == 0
replace regime_ert = 1 if regime_dich_ert == 0 & aut_ep == 0 & dem_ep == 0
replace regime_ert = 2 if regime_dich_ert == 0 & aut_ep == 0 & dem_ep == 1
replace regime_ert = 3 if regime_dich_ert == 1 & aut_ep == 1 & dem_ep == 0
replace regime_ert = 4 if regime_dich_ert == 1 & aut_ep == 0 & dem_ep == 0
replace regime_ert = 5 if regime_dich_ert == 1 & aut_ep == 0 & dem_ep == 1
replace regime_ert = . if (regime_dich_ert == 0 & aut_ep == 1 & dem_ep == 1) | (regime_dich_ert == 1 & aut_ep == 1 & dem_ep == 1) // Six observations with simultaneous episodes of democratization and autocratization excluded.
drop dem_ep aut_ep

label variable regime_ert "Political regime (ERT)"
label define regime_ert 0 "hardening autocracy" 1 "stable autocracy" 2 "liberalizing autocracy" 3 "eroding democracy" 4 "stable democracy" 5 "deepening democracy"
label values regime_ert regime_ert
tab regime_ert

generate regime_trich_ert = 0 if regime_ert == 0 | regime_ert == 3
replace regime_trich_ert = 1 if regime_ert == 1 | regime_ert == 4
replace regime_trich_ert = 2 if regime_ert == 2 | regime_ert == 5

label variable regime_trich_ert "Political regime (ERT, trichotomous)"
label define regime_trich_ert 0 "autocratizing regime" 1 "stable regime" 2 "democratizing regime"
label values regime_trich_ert regime_trich_ert
tab regime_trich_ert

** Refine regime-episode-outcome variables:

tab dem_ep_outcome aut_ep_outcome
list if dem_ep_outcome != 0 & aut_ep_outcome != 0

destring aut_ep_end_year, force replace
destring dem_ep_end_year, force replace

generate regime_trep_outcome_ert = 0 if year == aut_ep_end_year & aut_ep_outcome == 5
replace regime_trep_outcome_ert = 1 if year == dem_ep_end_year & dem_ep_outcome == 4
replace regime_trep_outcome_ert = 2 if year == dem_ep_end_year & dem_ep_outcome == 3
replace regime_trep_outcome_ert = 3 if year == dem_ep_end_year & dem_ep_outcome == 2
replace regime_trep_outcome_ert = 4 if year == dem_ep_end_year & dem_ep_outcome == 1
replace regime_trep_outcome_ert = 5 if year == aut_ep_end_year & aut_ep_outcome == 1
replace regime_trep_outcome_ert = 6 if year == aut_ep_end_year & aut_ep_outcome == 2
replace regime_trep_outcome_ert = 7 if year == aut_ep_end_year & aut_ep_outcome == 3
replace regime_trep_outcome_ert = 8 if year == aut_ep_end_year & aut_ep_outcome == 4
replace regime_trep_outcome_ert = 9 if year == dem_ep_end_year & dem_ep_outcome == 5
replace regime_trep_outcome_ert = 10 if year == aut_ep_end_year & aut_ep_outcome == 6
replace regime_trep_outcome_ert = 11 if year == dem_ep_end_year & dem_ep_outcome == 6
replace regime_trep_outcome_ert = . if dem_ep_outcome != 0 & aut_ep_outcome != 0
drop aut_ep_end_year dem_ep_end_year dem_ep_outcome aut_ep_outcome

label variable regime_trep_outcome_ert "Regime episode transformation outcome (ERT)"
label define regime_trep_outcome_ert 0 "hardened autocracy" 1 "reverted autocratic liberalization" 2 "liberalized autocracy" 3 "preempted democratization" 4 "democratization" 5 "democratic breakdown" 6 "preempted democratic breakdown" 7 "diminished democracy" 8 "averted democratic erosion" 9 "deepened democracy" 10 "autocratization episode ongoing" 11 "democratization episode ongoing"
label values regime_trep_outcome_ert regime_trep_outcome_ert

tab regime_trep_outcome_ert

tab regime_trep_outcome_ert regime_ert

sort country_name year


** Export data:
save "democracy/datasets/cleaned/ert_cleaned.dta", replace
export delimited "democracy/datasets/cleaned/ert_cleaned.csv", replace



exit
