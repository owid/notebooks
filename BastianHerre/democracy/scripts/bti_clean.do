*****  This Stata do-file cleans the 2022 democracy dataset by the Bertelsmann Transformation Index (BTI)
*****  Author: Bastian Herre
*****  June 28, 2022

version 14
clear all
set more off
set varabbrev off


** Set your own working directories here to run the file:
cd "/Users/bastianherre/Dropbox/Data/"
global project "/Users/bastianherre/Dropbox/Data/"


** Download BTI dataset from https://bti-project.org/fileadmin/api/content/en/downloads/data/BTI_2006-2022.dta and move it into the folder "Bertelsmann Transformation Index 2022"
** Import BTI dataset:
use "Bertelsmann Transformation Index 2022/BTI_2006-2022.dta", clear


** Keep variables of interest:
keep country year dem_stat stateness pol_part ruleoflaw stab_dem integ cat_dem_stat elect power assembly express separation civ_rights core_stateness pol_sys country_code


** Rename variables of interest:
rename country country_name
rename dem_stat democracy_bti
rename stateness state_bti
rename pol_part political_participation_bti
rename ruleoflaw rule_of_law_bti
rename stab_dem stability_dem_inst_bti
rename integ pol_soc_integr_bti
rename cat_dem_stat regime_bti
rename elect electfreefair_bti
rename power effective_power_bti
rename assembly freeassoc_bti
rename express freeexpr_bti
rename separation sep_power_bti
rename civ_rights civ_rights_bti
rename core_stateness state_basic_bti


** Refine variables of interest:

* Reflect that year of observation is previous year to release:
replace year = year - 1

* Correct regime classification:
tab year regime_bti // Year 2020 looks off, with many fewer hard-line autocracies and many more consolidating democracies.
tab regime_bti pol_sys // Table looks off, as some democracies are classified as hard-line and moderate autocracies, and some defective and consolidating democracies as autocracies.

generate pol_sys_check = .
replace pol_sys_check = 1 if electfreefair_bti >= 6 & electfreefair_bti != . ///
						& effective_power_bti >= 4 & effective_power_bti != . ///
						& freeassoc_bti >= 4 & freeassoc_bti != . ///
						& freeexpr_bti >= 4 & freeexpr_bti != . ///
						& sep_power_bti >= 4 & sep_power_bti != . ///
						& civ_rights_bti >= 4 & civ_rights_bti != . ///
						& state_basic_bti >= 3 & state_basic_bti != .
replace pol_sys_check = 0 if electfreefair_bti < 6 | effective_power_bti < 4 | freeassoc_bti < 4 | freeexpr_bti < 4 | sep_power_bti < 4 | civ_rights_bti < 4 | state_basic_bti < 3
tab pol_sys pol_sys_check, m // Variables match, check successful.
drop pol_sys_check

generate regime_bti_check = .
replace regime_bti_check = 1 if pol_sys == 0 & democracy_bti >= 1 & democracy_bti <= 3.99
replace regime_bti_check = 2 if pol_sys == 0 & democracy_bti >= 4 & democracy_bti <= 10
replace regime_bti_check = 3 if pol_sys == 1 & democracy_bti >= 1 & democracy_bti <= 5.99
replace regime_bti_check = 4 if pol_sys == 1 & democracy_bti >= 6 & democracy_bti <= 7.99
replace regime_bti_check = 5 if pol_sys == 1 & democracy_bti >= 8 & democracy_bti <= 10
tab regime_bti regime_bti_check // Variables do not match, check unsucessful; errors in regime_bti/cat_dem_stat.
tab regime_bti regime_bti_check if year == 2020 // It seems like the scale was accidentally reversed for 2020.
tab regime_bti regime_bti_check if year != 2020
list if regime_bti != regime_bti_check & year != 2020 // It seems there is an additional error for Serbia in 2010, which meets all criteria of a democracy, and should therefore be coded as a consolidating democracy.
drop regime_bti pol_sys

rename regime_bti_check regime_bti

label define regime_bti 1 "hard-line autocracy" 2 "moderate autocracy" 3 "highly defective democracy" 4 "defective democracy" 5 "consolidating democracy"
label values regime_bti regime_bti

replace country_name = "Democratic Republic of Congo" if country_name == "Congo, DR"
replace country_name = "Congo" if country_name == "Congo, Rep."
replace country_name = "Czechia" if country_name == "Czech Republic"
replace country_name = "Cote d'Ivoire" if country_code == "CIV"
replace country_name = "North Macedonia" if country_name == "Macedonia"
replace country_name = "Timor" if country_name == "Timor-Leste"
drop country_code


** Relabel variables of interest:
label variable country_name "Country name"
label variable democracy_bti "Democracy score (BTI)"
label variable regime_bti "Political regime (BTI)"
label variable electfreefair_bti "Free and fair elections (BTI)"
label variable effective_power_bti "Effective power to govern (BTI)"
label variable freeassoc_bti "Freedom of association (BTI)"
label variable freeexpr_bti "Freedom of expression (BTI)"
label variable sep_power_bti "Separation of powers (BTI)"
label variable civ_rights_bti "Civil rights (BTI)"
label variable state_bti "Stateness (BTI)"
label variable state_basic_bti "Basic state functions (BTI)"
label variable political_participation_bti "Political participation (BTI)"
label variable rule_of_law_bti "Rule of law (BTI)"
label variable stability_dem_inst_bti "Stability of democratic institutions (BTI)"
label variable pol_soc_integr_bti "Political and social integration (BTI)"

** Order variables and observations:
order regime_bti democracy_bti, after(year)
order state_basic_bti electfreefair_bti effective_power_bti freeassoc_bti freeexpr_bti sep_power_bti civ_rights_bti, after(regime_bti)
order state_bti political_participation_bti rule_of_law_bti stability_dem_inst_bti pol_soc_integr_bti, after(democracy_bti)
sort country_name year


** Export cleaned BTI data:
save "democracy/datasets/cleaned/bti_cleaned.dta", replace
export delimited "democracy/datasets/cleaned/bti_cleaned.csv", replace nolabel



exit
