*****  Stata do-file to create the press-freedom data used in the following chart on Our World in Data (OWID):
*****  https://ourworldindata.org/grapher/press-freedom-rsf
*****  Author: Bastian Herre
*****  April 8, 2022


version 14

clear all
set more off
set varabbrev off


** Set your own working directories here to run the file:
cd "/Users/bastianherre/Dropbox/Data/"
global project "/Users/bastianherre/Dropbox/Data/"


** Download dataset for 2013 from https://rsf.org/sites/default/files/ranking2013.csv and move it into the folder "Reporters sans Frontieres 2022 World Press Freedom Index".
** Import data:
import delimited "Reporters sans Frontieres 2022 World Press Freedom Index/ranking2013.csv", delimiter(";")


** Keep variables of interest:
keep en_country overallsco~2016 // Despite the variable name, this is not 2016 data — these values differ from the values for 2016 from the dataset below.


** Rename variables of interest:
rename en_country country_name
rename overallsco~2016 press_freedom_score_rsf


** Refine variables of interest"
generate year = 2013


** Order variables and observations:
order country_name year
sort country_name year


** Export data:
save "Reporters sans Frontieres 2022 World Press Freedom Index/press_freedom_rsf_2013.dta", replace


** Download 2014-ongoing dataset from GitHub repository (which we received from Nalini Chella-Lepetit, Head of the World Press Freedom Index) and move it into the folder "Reporters sans Frontieres 2022 World Press Freedom Index".
** Import data:
import delimited "Reporters sans Frontieres 2022 World Press Freedom Index/RSF_WorldPressFreedomIndex_2014-2021.csv", delimiter(";") clear


** Keep variables of interest:
drop iso rank


** Rename variables of interest:
rename ïyear year
rename country country_name
rename score press_freedom_score_rsf


** Combine 2013 and 2014- datasets:
append using "Reporters sans Frontieres 2022 World Press Freedom Index/press_freedom_rsf_2013.dta"
erase "Reporters sans Frontieres 2022 World Press Freedom Index/press_freedom_rsf_2013.dta"

** Refine variables of interest:
destring press_freedom_score_rsf, replace dpcomma

generate press_freedom_status_rsf = .
replace press_freedom_status_rsf = 0 if press_freedom_score_rsf >= 0 & press_freedom_score_rsf <= 15
replace press_freedom_status_rsf = 1 if press_freedom_score_rsf >= 15.01 & press_freedom_score_rsf <= 25
replace press_freedom_status_rsf = 2 if press_freedom_score_rsf >= 25.01 & press_freedom_score_rsf <= 35
replace press_freedom_status_rsf = 3 if press_freedom_score_rsf >= 35.01 & press_freedom_score_rsf <= 55
replace press_freedom_status_rsf = 4 if press_freedom_score_rsf >= 55.01 & press_freedom_score_rsf <= 100

label define press_freedom_status_rsf 0 "good" 1 "satisfactory" 2 "problematic" 3 "difficult" 4 "very serious"
label values press_freedom_status_rsf press_freedom_status_rsf

* Compare calculated values with labels in 2014- dataset:
tab press_freedom_status_rsf situation, m // Labels match.
drop situation

replace country_name = "Myanmar" if country_name == "Burma"
replace country_name = "Brunei" if country_name == "Brunei Darussalam"
replace country_name = "Cape Verde" if country_name == "Cap-Vert"
replace country_name = "Czechia" if country_name == "Czech Republic"
replace country_name = "Northern Cyprus" if country_name == "Cyprus North"
replace country_name = "Democratic Republic of Congo" if country_name == "DR Congo"
replace country_name = "North Korea" if country_name == "Democratic People's Republic of Korea"
replace country_name = "Timor" if country_name == "East Timor"
replace country_name = "Iran" if country_name == "Islamic Republic of Iran"
replace country_name = "Cote d'Ivoire" if country_name == "Ivory Coast"
replace country_name = "Laos" if country_name == "Lao People's Democratic Republic"
replace country_name = "North Macedonia" if country_name == "Republic of Macedonia"
replace country_name = "Congo" if country_name == "Republic of the Congo"
replace country_name = "Russia" if country_name == "Russian Federation"
replace country_name = "Syria" if country_name == "Syrian Arab Republic"
replace country_name = "Democratic Republic of Congo" if country_name == "The Democratic Republic Of The Congo"
replace country_name = "Eastern Caribbean States" if country_name == "OECS"


** Label variables of interest:
label variable year "Year"
label variable country_name "Country name"
label variable press_freedom_score_rsf "World press freedom index score (Reporters sans Frontieres)"
label variable press_freedom_status_rsf "World press freedom index status (Reporters sans Frontieres)"


** Order variables and observations:
order country_name year press_freedom_score_rsf press_freedom_status_rsf
sort country_name year


** Export data:
save "Reporters sans Frontieres 2022 World Press Freedom Index/press_freedom_rsf.dta", replace
export delimited "Reporters sans Frontieres 2022 World Press Freedom Index/press_freedom_rsf.csv", replace nolabel



exit
