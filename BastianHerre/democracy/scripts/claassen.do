*****  This Stata do-file cleans Claassen's data on citizens' support of and satisfaction with democracy.
*****  Author: Bastian Herre
*****  August 4, 2022

version 14
clear all
set more off
set varabbrev off


** Set your own working directories here to run the file:
cd "/Users/bastianherre/Dropbox/Data/"
global project "/Users/bastianherre/Dropbox/Data/"


** Download data from chrisclaassen.com/docs/dem_mood_v4.csv and move it into the folder "Claassen 2022"
** Import data:
import delimited "Claassen 2022/dem_mood_v4.csv", clear varnames(1)


** Keep variables of interest:
keep country year supdem supdem_u95 supdem_l95


** Rename and label variables:
rename country country_name
rename supdem democracy_support_claassen
rename supdem_u95 democracy_support_high_claassen
rename supdem_l95 democracy_support_low_claassen

label variable country_name "Country name"
label variable year "Year"
label variable democracy_support_claassen "Citizen support for democracy (Claassen)"
label variable democracy_support_high_claassen "Citizen support for democracy (upper bound, Claassen)"
label variable democracy_support_low_claassen "Citizen support for democracy (lower bound, Claassen)"


** Refine variables:
replace country_name = "North Macedonia" if country_name == "Macedonia"
replace country_name = "United States" if country_name == "United States of America"


** Order observations:
sort country_name year


** Export data:
save "Claassen 2022/claassen_support.dta", replace
export delimited "Claassen 2022/claassen_support.csv", replace

describe, replace
keep name varlab
rename name varname
rename varlab varlabel
export delimited "Claassen 2022/claassen_support_meta.csv", replace



** Download data from chrisclaassen.com/docs/satis_est_v2.csv and move it into the folder "Claassen 2022"
** Import data:
import delimited "Claassen 2022/satis_est_v2.csv", clear varnames(1)


** Keep variables of interest:
keep country year satis satis_u95 satis_l95


** Rename and label variables:
rename country country_name
rename satis democracy_satisf_claassen
rename satis_u95 democracy_satisf_high_claassen
rename satis_l95 democracy_satisf_low_claassen

label variable country_name "Country name"
label variable year "Year"
label variable democracy_satisf_claassen "Citizen satisfaction with democracy (Claassen)"
label variable democracy_satisf_high_claassen "Citizen satisfaction with democracy (upper bound, Claassen)"
label variable democracy_satisf_low_claassen "Citizen satisfaction with democracy (lower bound, Claassen)"


** Refine variables:
replace country_name = "North Macedonia" if country_name == "Macedonia"
replace country_name = "United States" if country_name == "United States of America"


** Order observations:
sort country_name year


** Export data:
save "Claassen 2022/claassen_satisfaction.dta", replace
export delimited "Claassen 2022/claassen_satisfaction.csv", replace

describe, replace
keep name varlab
rename name varname
rename varlab varlabel
export delimited "Claassen 2022/claassen_satisfaction_meta.csv", replace



exit
