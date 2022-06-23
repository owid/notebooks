*****  Stata do-file to create the human-rights-protection data used in the following chart on Our World in Data (OWID):
*****  https://ourworldindata.org/grapher/human-rights-protection
*****  Author: Bastian Herre
*****  April 8, 2022


version 14

clear all
set more off
set varabbrev off

** Set your own working directories here to run the file:
cd "/Users/bastianherre/Dropbox/Data/"
global project "/Users/bastianherre/Dropbox/Data/"


** Download dataset from https://dataverse.harvard.edu/dataverse/HumanRightsScores.
** Import data:
import delimited using "/Users/bastianherre/Dropbox/Data/Fariss, Kenwick, Reuning 2020 human rights protection/HumanRightsProtectionScores_v4.01.csv", stringcols(25)
* I import theta_mean as a string so as not to lose the leading zeros before the period.


** Keep variables of interest:
keep country_name cow year theta_mean


** Rename and label variables:
rename theta_mean human_rights_protection
label variable country_name "Country name"
label variable year "Year"
label variable human_rights_protection "Human rights protection (Fariss et al. 2020)"


** Refine variables:
replace country_name = "Antigua and Barbuda" if country_name=="Antigua & Barbuda"
replace country_name = "Bosnia and Herzegovina" if country_name=="Bosnia & Herzegovina"
replace country_name = "Congo" if country_name=="Congo - Brazzaville"
replace country_name = "Democratic Republic of Congo" if country_name=="Congo - Kinshasa"
replace country_name = "Cote d'Ivoire" if cow == 437
drop if country_name=="German Federal Republic" & year == 1990
replace country_name = "Germany" if country_name=="German Federal Republic"
replace country_name = "Micronesia" if country_name=="Micronesia (Federated States of)"
replace country_name = "Myanmar" if country_name=="Myanmar (Burma)"
replace country_name = "Saint Kitts and Nevis" if country_name=="St. Kitts & Nevis"
replace country_name = "Saint Lucia" if country_name=="St. Lucia"
replace country_name = "Saint Vincent and the Grenadines" if country_name=="St. Vincent & Grenadines"
replace country_name = "Sao Tome and Principe" if cow == 403
replace country_name = "Timor" if country_name=="Timor-Leste"
replace country_name = "Trinidad and Tobago" if country_name=="Trinidad & Tobago"
drop if country_name=="Yemen" & year == 1990
replace country_name = "Yemen" if country_name=="Yemen Arab Republic"
replace country_name = "Serbia" if country_name=="Yugoslavia"
drop cow


** Order variables and observations:
order country_name year human_rights_protection
sort country_name year


** Export data:
save "/Users/bastianherre/Dropbox/Data/Human Rights/human_rights_protection.dta", replace
export delimited "/Users/bastianherre/Dropbox/Data/Human Rights/human_rights_protection.csv", replace


exit
