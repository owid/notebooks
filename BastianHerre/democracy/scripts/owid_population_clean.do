*****  This Stata do-file cleans the population dataset by Our World in Data
*****  Author: Bastian Herre
*****  June 28, 2022

version 14
clear all
set more off
set varabbrev off


** Set your own working directories here to run the file:
cd "/Users/bastianherre/Dropbox/Data/"
global project "/Users/bastianherre/Dropbox/Data/"


** Download V-Dem dataset from https://ourworldindata.org/grapher/population and move it into the folder "Our World in Data"
** Import data:
import delimited "/Users/bastianherre/Dropbox/Data/Our World in Data/population.csv"


** Keep variables of interest:
keep entity year populationhistoricalestimates


** Keep observations of interest:
drop if year < 1800 | year > 2021 // I am interested only in the period with annual data (>= 1800) and up to current data (<= 2021)


** Rename variables:
rename entity country_name
rename populationhistoricalestimates population_owid


** Label variables:
label variable country_name "Country name"
label variable population_owid "Population (OWID)"


** Keep observations of interest:
drop if country_name == "Africa" | country_name == "Asia" | country_name == "Europe" | country_name == "North America" | country_name == "South America" | country_name == "Oceania" | country_name == "World"


** Sort observations:
sort country_name year


** Export data:
save "Our World in Data/owid_population_cleaned.dta", replace
export delimited "Our World in Data/owid_population_cleaned.csv", replace



exit
