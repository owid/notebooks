*****  This Stata do-file creates a country-year dataset of all countries and regions included in the OWID database
*****  Author: Bastian Herre
*****  June 28, 2022

version 14
clear all
set more off
set varabbrev off


** Set your own working directories here to run the file:
cd "/Users/bastianherre/Dropbox/Data/"
global project "/Users/bastianherre/Dropbox/Data/"

** Download entities list from https://github.com/owid/etl/blob/master/data/reference/countries_regions.csv and move it into the folder "Our World in Data"
** Import entities list:
import delimited "Our World in Data/countries_regions.csv"


** Keep variable of interest:
keep name


** Rename variable:
rename name entity_name


** Expand observations:
expand 233
sort entity_name


** Create year variable:
bysort entity_name: generate year = 1788+_n


** Label variables:
label variable entity_name "Entity name"
label variable year "Year"


** Export data:
export delimited "Our World in Data/owid_entities_expanded.csv", replace
save "Our World in Data/owid_entities_expanded.dta", replace



exit
