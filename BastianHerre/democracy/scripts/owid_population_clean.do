*****  This Stata do-file cleans the population dataset by Our World in Data
*****  Author: Bastian Herre
*****  March 8, 2023

version 14
clear all
set more off
set varabbrev off


** Set your own working directories here to run the file:
cd "/Users/bastianherre/Dropbox/Data/"
global project "/Users/bastianherre/Dropbox/Data/"


** Download population dataset from https://owid.cloud/admin/variables/525709 and move it into the folder "Our World in Data"
** Import data:
import delimited "/Users/bastianherre/Dropbox/Data/Our World in Data/population.csv"


** Keep variables of interest:
keep entity year population


** Keep observations of interest:
drop if year < 1800 | year > 2022 // I am interested only in the period with annual data (>= 1800) and up to the current year (<= 2022)


** Rename variables:
rename entity country_name
rename population population_owid


** Label variables:
label variable country_name "Country name"
label variable population_owid "Population (OWID)"


** Keep observations of interest:
drop if country_name == "Africa" | country_name == "Asia" | country_name == "Europe" | country_name == "North America" | country_name == "South America" | country_name == "Oceania" | country_name == "World"
drop if country_name == "Africa (UN)" | country_name == "Asia (UN)" | country_name == "Europe (UN)" | country_name == "European Union (27)" | country_name == "High-income countries" | country_name == "Northern America (UN)" | country_name == "Latin America and the Caribbean (UN)" | country_name == "Low-income countries" | country_name == "Lower-middle-income countries" | country_name == "Oceania (UN)" | country_name == "Upper-middle-income countries" | country_name == "World"


** Sort observations:
sort country_name year


** Export data:
save "Our World in Data/owid_population_cleaned.dta", replace
export delimited "Our World in Data/owid_population_cleaned.csv", replace



exit
