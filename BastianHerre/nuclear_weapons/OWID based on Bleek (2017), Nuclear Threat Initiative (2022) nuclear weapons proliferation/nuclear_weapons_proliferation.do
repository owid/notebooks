*****  Stata do-file to create the nuclear-weapons-proliferation data used in the following charts on Our World in Data (OWID):
*****  https://ourworldindata.org/grapher/country-position-nuclear-weapons
*****  https://ourworldindata.org/grapher/nuclear-weapons-proliferation
*****  Author: Bastian Herre
*****  April 8, 2022


version 14

clear all
set more off
set varabbrev off


** Set your own working directories here to run the file:
cd "/Users/bastianherre/Dropbox/Data/"
global project "/Users/bastianherre/Dropbox/Data/"


** Download dataset from GitHub repository (which we digitized from https://www.belfercenter.org/sites/default/files/files/publication/When%20Did%20%28and%20Didn%27t%29%20States%20Proliferate%3F_1.pdf) and move it into the folder "Bleek 2017 nuclear weapons proliferation".
** Import data:
import excel "Bleek 2017 nuclear weapons proliferation/nuclear_weapons_proliferation_raw.xlsx", firstrow


** Rename variables:
rename Country country_name
rename Explore nuclear_weapons_exploration
rename Pursue nuclear_weapons_pursuit
rename Acquire nuclear_weapons_acquisition


** Refine variables:
label variable country_name "Country name"
replace country_name = "Algeria" if country_name == "Algerla"
replace country_name = "Australia" if country_name == "Australla"
replace country_name = "West Germany" if country_name == "Germany, West"
replace country_name = "North Korea" if country_name == "Korea, North"
replace country_name = "Russia" if country_name == "Russla"
replace country_name = "Syria" if country_name == "Syrla"
replace country_name = "Taiwan" if country_name == "Talwan"
replace country_name = "Serbia" if country_name == "Yugoslavia"


** Create country-year dataset:
sort country_name


split nuclear_weapons_exploration, p("-" ",")
destring nuclear_weapons_exploration*, replace

replace nuclear_weapons_exploration2 = nuclear_weapons_exploration2 + 1900 if nuclear_weapons_exploration2 < 100
replace nuclear_weapons_exploration3 = nuclear_weapons_exploration3 + 1900 if nuclear_weapons_exploration3 < 100
replace nuclear_weapons_exploration4 = nuclear_weapons_exploration4 + 1900 if nuclear_weapons_exploration4 < 100
drop nuclear_weapons_exploration

rename nuclear_weapons_exploration1 nuclear_weapons_explore_start1
rename nuclear_weapons_exploration2 nuclear_weapons_explore_end1
rename nuclear_weapons_exploration3 nuclear_weapons_explore_start2
rename nuclear_weapons_exploration4 nuclear_weapons_explore_end2

replace nuclear_weapons_explore_end1 = 2022 if nuclear_weapons_explore_end1 == .
replace nuclear_weapons_explore_end2 = 2022 if nuclear_weapons_explore_end2 == . & nuclear_weapons_explore_start2 != .


split nuclear_weapons_pursuit, p("-" ",")
destring nuclear_weapons_pursuit*, replace

replace nuclear_weapons_pursuit2 = nuclear_weapons_pursuit2 + 1900 if nuclear_weapons_pursuit2 < 100
replace nuclear_weapons_pursuit2 = 2007 if nuclear_weapons_pursuit2 == 1907
replace nuclear_weapons_pursuit3 = nuclear_weapons_pursuit3 + 1900 if nuclear_weapons_pursuit3 < 100
replace nuclear_weapons_pursuit4 = nuclear_weapons_pursuit4 + 1900 if nuclear_weapons_pursuit4 < 100
replace nuclear_weapons_pursuit5 = nuclear_weapons_pursuit5 + 1900 if nuclear_weapons_pursuit5 < 100
drop nuclear_weapons_pursuit

rename nuclear_weapons_pursuit1 nuclear_weapons_pursue_start1
rename nuclear_weapons_pursuit2 nuclear_weapons_pursue_end1
rename nuclear_weapons_pursuit3 nuclear_weapons_pursue_start2
rename nuclear_weapons_pursuit4 nuclear_weapons_pursue_end2
rename nuclear_weapons_pursuit5 nuclear_weapons_pursue_start3
generate nuclear_weapons_pursue_end3 = .

replace nuclear_weapons_pursue_end1 = 2022 if nuclear_weapons_pursue_end1 == . & nuclear_weapons_pursue_start1 != .
replace nuclear_weapons_pursue_end2 = 2022 if nuclear_weapons_pursue_end2 == . & nuclear_weapons_pursue_start2 != .
replace nuclear_weapons_pursue_end3 = 2022 if nuclear_weapons_pursue_end3 == . & nuclear_weapons_pursue_start3 != .


split nuclear_weapons_acquisition, p("-" ",")
destring nuclear_weapons_acquisition*, replace

replace nuclear_weapons_acquisition2 = nuclear_weapons_acquisition2 + 1900 if nuclear_weapons_acquisition2 < 100
drop nuclear_weapons_acquisition

rename nuclear_weapons_acquisition1 nuclear_weapons_acquire_start1
rename nuclear_weapons_acquisition2 nuclear_weapons_acquire_end1

replace nuclear_weapons_acquire_end1 = 2022 if nuclear_weapons_acquire_end1 == . & nuclear_weapons_acquire_start1 != .

save "/Users/bastianherre/Dropbox/Data/Nuclear weapons/nuclear_weapons_proliferation_temp.dta", replace


** Add countries which did not considers nuclear weapons:

* Download dataset with list of independent states from http://ksgleditsch.com/data-4.html and move it into the folder "Gleditsch, Ward 1999 independent states".
* Import data:
import delimited "/Users/bastianherre/Dropbox/Data/Gleditsch, Ward 1999 independent states/iisystem.txt", clear

* Keep variables of interest:
drop v1

* Rename variables:
rename v2 iso3code
rename v3 country_name
rename v4 start
rename v5 end

* Label variables:
label variable country_name "Country name"
label variable start "Start of independence"
label variable end "End of independence"

save "/Users/bastianherre/Dropbox/Data/Gleditsch, Ward 1999 independent states/iisystem_temp.dta", replace

* Download dataset with list of microstates from http://ksgleditsch.com/data-4.html and move it into the folder "Gleditsch, Ward 1999 independent states".
* Import data:
import delimited "/Users/bastianherre/Dropbox/Data/Gleditsch, Ward 1999 independent states/microstatessystem.txt", clear

* Keep variables of interest:
drop v1

* Rename variables:
rename v2 iso3code
rename v3 country_name
rename v4 start
rename v5 end

* Label variables:
label variable country_name "Country name"
label variable start "Start of independence"
label variable end "End of independence"

save "/Users/bastianherre/Dropbox/Data/Gleditsch, Ward 1999 independent states/microstatessystem_temp.dta", replace

* Combine datasets:
use "/Users/bastianherre/Dropbox/Data/Gleditsch, Ward 1999 independent states/iisystem_temp.dta", clear
append using "/Users/bastianherre/Dropbox/Data/Gleditsch, Ward 1999 independent states/microstatessystem_temp.dta"

erase "/Users/bastianherre/Dropbox/Data/Gleditsch, Ward 1999 independent states/iisystem_temp.dta"
erase "/Users/bastianherre/Dropbox/Data/Gleditsch, Ward 1999 independent states/microstatessystem_temp.dta"

* Create country-year dataset:
split start, p(:) destring
drop start start1 start2
rename start3 startyear

split end, p(:) destring
drop end end1 end2
rename end3 endyear

replace endyear = 2022 if endyear == 2017

keep if endyear > 1938 & endyear < .

* Refine variables:
replace country_name="Burkina Faso" if country_name=="Burkina Faso (Upper Volta)"
replace country_name="Myanmar" if country_name=="Myanmar (Burma)"
replace country_name="Cambodia" if country_name=="Cambodia (Kampuchea)"
replace country_name="Democratic Republic of Congo" if country_name=="Congo, Democratic Republic of (Zaire)"
replace country_name="Iran" if country_name=="Iran (Persia)"
replace country_name="Cote d'Ivoire" if iso3code=="CDI"
replace country_name="Republic of Vietnam" if country_name=="Vietnam, Republic of"
replace country_name="Congo" if country_name=="Congo"
replace country_name="Russia" if country_name=="Russia (Soviet Union)"
replace country_name="Sao Tome and Principe" if country_name=="São Tomé and Principe"
replace country_name="South Korea" if country_name=="Korea, Republic of"
replace country_name="South Yemen" if country_name=="Yemen, People's Republic of"
replace country_name="Suriname" if country_name=="Surinam"
replace country_name="The Gambia" if country_name=="Gambia"
replace country_name="Turkey" if country_name=="Turkey (Ottoman Empire)"
replace country_name="Yemen" if country_name=="Yemen (Arab Republic of Yemen)"
replace country_name="Zimbabwe" if country_name=="Zimbabwe (Rhodesia)"
replace country_name="Belarus" if country_name=="Belarus (Byelorussia)"
replace country_name="Bosnia and Herzegovina" if country_name=="Bosnia-Herzegovina"
replace country_name="Czechia" if country_name=="Czechoslovakia"
replace country_name="Czechia" if country_name=="Czech Republic"
replace country_name="Germany" if country_name=="German Federal Republic"
replace country_name="Italy" if country_name=="Italy/Sardinia"
replace country_name="North Korea" if country_name=="Korea, People's Republic of"
replace country_name="Kyrgyzstan" if country_name=="Kyrgyz Republic"
replace country_name="North Macedonia" if country_name=="Macedonia (Former Yugoslav Republic of)"
replace country_name="Romania" if country_name=="Rumania"
replace country_name="Sri Lanka" if country_name=="Sri Lanka (Ceylon)"
replace country_name="Tanzania" if country_name=="Tanzania/Tanganyika"
replace country_name="Vietnam" if country_name=="Vietnam, Democratic Republic of"
replace country_name="Serbia" if country_name=="Yugoslavia"
replace country_name="Timor" if country_name=="East Timor"
replace country_name="United States" if country_name=="United States of America"
replace country_name="Samoa" if country_name=="Samoa/Western Samoa"
drop iso3code

drop if country_name=="Czechia" & startyear == 1918
drop if country_name=="Serbia" & startyear == 1918
drop if country_name=="Estonia" & startyear == 1918
drop if country_name=="Latvia" & startyear == 1918
drop if country_name=="Lithuania" & startyear == 1918
drop if country_name=="Germany (Prussia)"

save "/Users/bastianherre/Dropbox/Data/Gleditsch, Ward 1999 independent states/gw_temp.dta", replace

* Combine datasets with countries that at least considered nuclear weapons with those that did not:
merge 1:1 country_name using "/Users/bastianherre/Dropbox/Data/Nuclear weapons/nuclear_weapons_proliferation_temp.dta"
drop _merge

erase "/Users/bastianherre/Dropbox/Data/Nuclear weapons/nuclear_weapons_proliferation_temp.dta"

expand 85
sort country_name

generate year = .
replace year = 1938 if country_name[_n-1] != country_name
replace year = year[_n-1] + 1 if country_name[_n-1] == country_name

* Label variables:
label variable year "Year"
order country_name year

* Refine variables:
drop if country_name == "West Germany" & (year < 1946 | year > 1989)
drop if country_name == "Germany" & year > 1945 & year < 1990
replace country_name = "Germany" if country_name == "West Germany"
sort country_name year

drop if endyear < 2022 & startyear > year
drop if endyear < 2022 & endyear < year
drop startyear endyear


** Generate variables of interest:
generate nuclear_weapons_consideration = .
replace nuclear_weapons_consideration = 1 if nuclear_weapons_explore_start1 == year | nuclear_weapons_explore_start2 == year
bysort country_name: replace nuclear_weapons_consideration = 0 if nuclear_weapons_explore_end1[_n-1] == year[_n-1] | nuclear_weapons_explore_end2[_n-1] == year[_n-1]
bysort country_name: replace nuclear_weapons_consideration = 1 if nuclear_weapons_consideration[_n-1] == 1 & nuclear_weapons_consideration != 0
recode nuclear_weapons_consideration (.=0)
drop nuclear_weapons_explore*
label variable nuclear_weapons_consideration "Country at least considers acquiring nuclear weapons"

generate nuclear_weapons_pursuit = .
replace nuclear_weapons_pursuit = 1 if nuclear_weapons_pursue_start1 == year | nuclear_weapons_pursue_start2 == year | nuclear_weapons_pursue_start3 == year
bysort country_name: replace nuclear_weapons_pursuit = 0 if nuclear_weapons_pursue_end1[_n-1] == year[_n-1] | nuclear_weapons_pursue_end2[_n-1] == year[_n-1] | nuclear_weapons_pursue_end3[_n-1] == year[_n-1]
bysort country_name: replace nuclear_weapons_pursuit = 1 if nuclear_weapons_pursuit[_n-1] == 1 & nuclear_weapons_pursuit != 0
recode nuclear_weapons_pursuit (.=0)
drop nuclear_weapons_pursue*
label variable nuclear_weapons_pursuit "Country at least pursues nuclear weapons"

generate nuclear_weapons_possession = .
replace nuclear_weapons_possession = 1 if nuclear_weapons_acquire_start1 == year
bysort country_name: replace nuclear_weapons_possession = 0 if nuclear_weapons_acquire_end1[_n-1] == year[_n-1]
bysort country_name: replace nuclear_weapons_possession = 1 if nuclear_weapons_possession[_n-1] == 1 & nuclear_weapons_possession != 0
recode nuclear_weapons_possession (.=0)
drop nuclear_weapons_acquire*
label variable nuclear_weapons_possession "Country has nuclear weapons"

tab nuclear_weapons_consideration nuclear_weapons_pursuit
list country_name year if nuclear_weapons_consideration == 0 & nuclear_weapons_pursuit == 1
tab nuclear_weapons_pursuit nuclear_weapons_possession

generate nuclear_weapons_status = 0
replace nuclear_weapons_status = 1 if nuclear_weapons_consideration == 1
replace nuclear_weapons_status = 2 if nuclear_weapons_pursuit == 1
replace nuclear_weapons_status = 3 if nuclear_weapons_possession == 1
label variable nuclear_weapons_status "Country behavior on nuclear weapons"
label define nuclear_weapons_status 0 "does not consider" 1 "considers" 2 "pursues" 3 "possesses"
label values nuclear_weapons_status nuclear_weapons_status

replace nuclear_weapons_consideration = 0 if nuclear_weapons_pursuit == 1
replace nuclear_weapons_pursuit = 0 if nuclear_weapons_possession == 1


** Order variables:
order country_name year nuclear_weapons_status


** Export data:
save "/Users/bastianherre/Dropbox/Data/Nuclear weapons/nuclear_weapons_proliferation_owid.dta", replace
export delimited "/Users/bastianherre/Dropbox/Data/Nuclear weapons/nuclear_weapons_proliferation_owid.csv", replace nolabel


** Create dataset with total number of different states by year:

preserve

* Keep countries that at least considered nuclear weapons after 1938:
drop if nuclear_weapons_consideration == 0 & nuclear_weapons_pursuit == 0 & nuclear_weapons_possession == 0 & year != 1938

tabulate nuclear_weapons_status, generate(nuclear_weapons_status)

* Create global dataset:
collapse (sum) nuclear_weapons_status*, by(year)
drop nuclear_weapons_status

generate entity_name = "World"
order entity_name, before(year)

* Keep variables of interest:
drop nuclear_weapons_status1

* Rename variables:
rename nuclear_weapons_status2 number_nuclweap_consideration
rename nuclear_weapons_status3 number_nuclweap_pursuit
rename nuclear_weapons_status4 number_nuclweap_possession

* Label variables:
label variable number_nuclweap_consideration "Number of countries considering acquiring nuclear weapons"
label variable number_nuclweap_consideration "Number of countries pursuing nuclear weapons"
label variable number_nuclweap_consideration "Number of countries possessing nuclear weapons"

* Export data:
save "/Users/bastianherre/Dropbox/Data/Nuclear weapons/nuclear_weapons_proliferation_total_owid.dta", replace
export delimited "/Users/bastianherre/Dropbox/Data/Nuclear weapons/nuclear_weapons_proliferation_total_owid.csv", replace


exit
