*****  This Stata do-file aggregates some of the variables in the LIED dataset
*****  Author: Bastian Herre
*****  September 5, 2023

version 14
clear all
set more off
set varabbrev off


** Set your own working directories here to run the file:
cd "/Users/bastianherre/Dropbox/Data/"
global project "/Users/bastianherre/Dropbox/Data/"


** Aggregate by year to create world aggregates for sums of regime variables:

* Import data:
use "democracy/datasets/refined/lexical_refined.dta", clear

* Create indicator variables for specific regime categories:
tabulate regime_lied, generate(regime_lied)
tabulate electdem_age_group_lied, generate(electdem_age_group_lied)
tabulate polyarchy_age_group_lied, generate(polyarchy_age_group_lied)
tabulate suffrage_lied, generate(suffrage_lied)

* Collapse dataset by year:
collapse (sum) regime_lied* electdem_age_group_lied* polyarchy_age_group_lied* suffrage_lied*, by(year)
drop regime_lied electdem_age_group_lied polyarchy_age_group_lied suffrage_lied

* Create entity identifier:
generate country_name = "World"

* Rename variables:
rename regime_lied1 number_nonelectaut_lied
rename regime_lied2 number_onepaut_lied
rename regime_lied3 number_multipautne_lied
rename regime_lied4 number_multipaut_lied
rename regime_lied5 number_excldem_lied
rename regime_lied6 number_maledem_lied
rename regime_lied7 number_electdem_lied
rename regime_lied8 number_poly_lied

drop electdem_age_group_lied1 electdem_age_group_lied2 electdem_age_group_lied3 electdem_age_group_lied4 electdem_age_group_lied5 electdem_age_group_lied6
rename electdem_age_group_lied7 number_electdem_18_lied
rename electdem_age_group_lied8 number_electdem_30_lied
rename electdem_age_group_lied9 number_electdem_60_lied
rename electdem_age_group_lied10 number_electdem_90_lied
rename electdem_age_group_lied11 number_electdem_91plus_lied

drop polyarchy_age_group_lied1 polyarchy_age_group_lied2 polyarchy_age_group_lied3 polyarchy_age_group_lied4 polyarchy_age_group_lied5 polyarchy_age_group_lied6 polyarchy_age_group_lied7
rename polyarchy_age_group_lied8 number_poly_18_lied
rename polyarchy_age_group_lied9 number_poly_30_lied
rename polyarchy_age_group_lied10 number_poly_60_lied
rename polyarchy_age_group_lied11 number_poly_90_lied

rename suffrage_lied1 number_unisuffrage_none
rename suffrage_lied2 number_unisuffrage_men
rename suffrage_lied3 number_unisuffrage_all

* Temporarily save data:
save "democracy/datasets/final/lexical_aggregated.dta", replace


** Aggregate by year to create world aggregates for population-weighted sums of regime variables:

* Import data:
use "democracy/datasets/refined/lexical_refined.dta", clear

* Add population data:
merge 1:1 country_name year using "Our World in Data/owid_population_cleaned.dta"
tab country_name if _merge == 1 // Unmerged observations are historical countries (Sicily, East Germany) or current countries without population data (Kosovo, Palestine/Gaza, Palestine/West Bank, Somaliland).
drop _merge

* Remove population data for year when regime data is not yet available:
drop if year == 2022

* Recode regime classification such that it includes a category for when population data is available, but regime data is missing:
replace regime_lied = 9 if regime_lied == . & population_owid != .
label values regime_lied regime_lied
label define regime_lied 9 "no regime data", add

replace suffrage_lied = 4 if suffrage_lied == . & population_owid != .
label values suffrage_lied suffrage_lied
label define suffrage_lied 4 "no suffrage data", add
drop if population_owid == .

* Create indicator variables for specific regime categories:
tabulate regime_lied, generate(regime_lied)
tabulate electdem_age_group_lied, generate(electdem_age_group_lied)
tabulate polyarchy_age_group_lied, generate(polyarchy_age_group_lied)
tabulate suffrage_lied, generate(suffrage_lied)

* Collapse dataset by year:
collapse (sum) regime_lied* electdem_age_group_lied* polyarchy_age_group_lied* suffrage_lied* [fweight = population_owid], by(year)
drop regime_lied electdem_age_group_lied polyarchy_age_group_lied suffrage_lied

* Create entity identifier:
generate country_name = "World"

* Rename variables:
rename regime_lied1 pop_nonelectaut_lied
rename regime_lied2 pop_onepaut_lied
rename regime_lied3 pop_multipautne_lied
rename regime_lied4 pop_multipaut_lied
rename regime_lied5 pop_excldem_lied
rename regime_lied6 pop_maledem_lied
rename regime_lied7 pop_electdem_lied
rename regime_lied8 pop_poly_lied
rename regime_lied9 pop_missreg_lied

drop electdem_age_group_lied1 electdem_age_group_lied2 electdem_age_group_lied3 electdem_age_group_lied4 electdem_age_group_lied5 electdem_age_group_lied6
rename electdem_age_group_lied7 pop_electdem_18_lied
rename electdem_age_group_lied8 pop_electdem_30_lied
rename electdem_age_group_lied9 pop_electdem_60_lied
rename electdem_age_group_lied10 pop_electdem_90_lied
rename electdem_age_group_lied11 pop_electdem_91plus_lied

drop polyarchy_age_group_lied1 polyarchy_age_group_lied2 polyarchy_age_group_lied3 polyarchy_age_group_lied4 polyarchy_age_group_lied5 polyarchy_age_group_lied6 polyarchy_age_group_lied7
rename polyarchy_age_group_lied8 pop_poly_18_lied
rename polyarchy_age_group_lied9 pop_poly_30_lied
rename polyarchy_age_group_lied10 pop_poly_60_lied
rename polyarchy_age_group_lied11 pop_poly_90_lied

rename suffrage_lied1 pop_unisuffrage_none
rename suffrage_lied2 pop_unisuffrage_men
rename suffrage_lied3 pop_unisuffrage_all
rename suffrage_lied4 pop_unisuffrage_miss

* Temporarily save data:
save "democracy/datasets/final/lexical_aggregated_popweighted.dta", replace


** Aggregate by year and region to create regional aggregates for sums of regime variables:

* Prepare regional identifiers:
import delimited "Our World in Data/countries_regions_pairs.csv", clear varnames(1)
rename country country_name

* Keep regional identifiers of interest:
tab region
drop if region == "Antarctica"
duplicates tag country_name, generate(duplicate)
list if duplicate == 1
drop if region == "European Union (27)"
duplicates drop // Northern Cyprus still listed twice.
drop duplicate

save "Our World in Data/countries_regions_pairs.dta", replace

* Import data:
use "democracy/datasets/refined/lexical_refined.dta", clear

* Add regional identifiers:
merge m:1 country_name using "Our World in Data/countries_regions_pairs.dta"
tab country_name if _merge == 1
replace region = "Africa" if country_name == "Cape Colony" | country_name == "Natal" | country_name == "Orange Free State" | country_name == "Transvaal"
replace region = "Asia" if country_name == "Palestine/British Mandate" | country_name == "Palestine/Gaza" | country_name == "Palestine/West Bank" |  country_name == "North Vietnam" | country_name == "Ottoman Empire" | country_name == "Tibet"
replace region = "Europe" if country_name == "Brunswick" | country_name == "Hamburg" | country_name == "Hesse-Darmstadt" | country_name == "Hesse-Kassel" | country_name == "Nassau" | country_name == "Oldenburg" | country_name == "Papal States" | country_name == "Prussia" | country_name == "Sardinia" | country_name == "Saxe-Weimar-Eisenach" | country_name == "Sicily"
replace region = "North America" if country_name == "United Provinces of Central America" | country_name == "Newfoundland"
replace region = "South America" if country_name == "Great Colombia"
drop if _merge == 2
drop _merge

* Create indicator variables for specific regime categories:
tabulate regime_lied, generate(regime_lied)
tabulate electdem_age_group_lied, generate(electdem_age_group_lied)
tabulate polyarchy_age_group_lied, generate(polyarchy_age_group_lied)
tabulate suffrage_lied, generate(suffrage_lied)

* Collapse dataset by year:
collapse (sum) regime_lied* electdem_age_group_lied* polyarchy_age_group_lied* suffrage_lied*, by(year region)
drop regime_lied electdem_age_group_lied polyarchy_age_group_lied suffrage_lied

* Create entity identifier:
rename region country_name

* Rename variables:
rename regime_lied1 number_nonelectaut_lied
rename regime_lied2 number_onepaut_lied
rename regime_lied3 number_multipautne_lied
rename regime_lied4 number_multipaut_lied
rename regime_lied5 number_excldem_lied
rename regime_lied6 number_maledem_lied
rename regime_lied7 number_electdem_lied
rename regime_lied8 number_poly_lied

drop electdem_age_group_lied1 electdem_age_group_lied2 electdem_age_group_lied3 electdem_age_group_lied4 electdem_age_group_lied5 electdem_age_group_lied6
rename electdem_age_group_lied7 number_electdem_18_lied
rename electdem_age_group_lied8 number_electdem_30_lied
rename electdem_age_group_lied9 number_electdem_60_lied
rename electdem_age_group_lied10 number_electdem_90_lied
rename electdem_age_group_lied11 number_electdem_91plus_lied

drop polyarchy_age_group_lied1 polyarchy_age_group_lied2 polyarchy_age_group_lied3 polyarchy_age_group_lied4 polyarchy_age_group_lied5 polyarchy_age_group_lied6 polyarchy_age_group_lied7
rename polyarchy_age_group_lied8 number_poly_18_lied
rename polyarchy_age_group_lied9 number_poly_30_lied
rename polyarchy_age_group_lied10 number_poly_60_lied
rename polyarchy_age_group_lied11 number_poly_90_lied

rename suffrage_lied1 number_unisuffrage_none
rename suffrage_lied2 number_unisuffrage_men
rename suffrage_lied3 number_unisuffrage_all

* Temporarily save data:
save "democracy/datasets/final/lexical_aggregated_regions.dta", replace


** Aggregate by year and region to create regional aggregates for population-weighted sums and averages of regime variables:

* Import data:
use "democracy/datasets/refined/lexical_refined.dta", clear

* Add population data:
merge 1:1 country_name year using "Our World in Data/owid_population_cleaned.dta"
tab country_name if _merge == 1 & year >= 1800 // Unmerged observations are historical countries (Sicily, East Germany) or current countries without population data (Kosovo, Palestine/Gaza, Palestine/West Bank, Somaliland).
drop _merge

* Remove population data for year when regime data is not yet available:
drop if year == 2022

* Add regional identifiers:
merge m:1 country_name using "Our World in Data/countries_regions_pairs.dta"
tab country_name if _merge == 1
replace region = "Africa" if country_name == "Cape Colony" | country_name == "Natal" | country_name == "Orange Free State" | country_name == "Transvaal"
replace region = "Asia" if country_name == "Palestine/British Mandate" | country_name == "Palestine/Gaza" | country_name == "Palestine/West Bank" |  country_name == "North Vietnam" | country_name == "Ottoman Empire" | country_name == "Tibet"
replace region = "Europe" if country_name == "Brunswick" | country_name == "Hamburg" | country_name == "Hesse-Darmstadt" | country_name == "Hesse-Kassel" | country_name == "Nassau" | country_name == "Oldenburg" | country_name == "Papal States" | country_name == "Prussia" | country_name == "Sardinia" | country_name == "Saxe-Weimar-Eisenach" | country_name == "Sicily"
replace region = "North America" if country_name == "United Provinces of Central America"
replace region = "South America" if country_name == "Great Colombia"
drop if _merge == 2
drop _merge

* Recode regime classification such that it includes a category for when population data is available, but regime data is missing:
replace regime_lied = 9 if regime_lied == . & population_owid != .
label values regime_lied regime_lied
label define regime_lied 9 "no regime data", add

replace suffrage_lied = 4 if suffrage_lied == . & population_owid != .
label values suffrage_lied suffrage_lied
label define suffrage_lied 4 "no suffrage data", add
drop if population_owid == .

* Create indicator variables for specific regime categories:
tabulate regime_lied, generate(regime_lied)
tabulate electdem_age_group_lied, generate(electdem_age_group_lied)
tabulate polyarchy_age_group_lied, generate(polyarchy_age_group_lied)
tabulate suffrage_lied, generate(suffrage_lied)

* Collapse dataset by year:
collapse (sum) regime_lied* electdem_age_group_lied* polyarchy_age_group_lied* suffrage_lied* [fweight = population_owid], by(year region)
drop regime_lied electdem_age_group_lied polyarchy_age_group_lied suffrage_lied

* Create entity identifier:
rename region country_name

* Rename variables:
rename regime_lied1 pop_nonelectaut_lied
rename regime_lied2 pop_onepaut_lied
rename regime_lied3 pop_multipautne_lied
rename regime_lied4 pop_multipaut_lied
rename regime_lied5 pop_excldem_lied
rename regime_lied6 pop_maledem_lied
rename regime_lied7 pop_electdem_lied
rename regime_lied8 pop_poly_lied
rename regime_lied9 pop_missreg_lied

drop electdem_age_group_lied1 electdem_age_group_lied2 electdem_age_group_lied3 electdem_age_group_lied4 electdem_age_group_lied5 electdem_age_group_lied6
rename electdem_age_group_lied7 pop_electdem_18_lied
rename electdem_age_group_lied8 pop_electdem_30_lied
rename electdem_age_group_lied9 pop_electdem_60_lied
rename electdem_age_group_lied10 pop_electdem_90_lied
rename electdem_age_group_lied11 pop_electdem_91plus_lied

drop polyarchy_age_group_lied1 polyarchy_age_group_lied2 polyarchy_age_group_lied3 polyarchy_age_group_lied4 polyarchy_age_group_lied5 polyarchy_age_group_lied6 polyarchy_age_group_lied7
rename polyarchy_age_group_lied8 pop_poly_18_lied
rename polyarchy_age_group_lied9 pop_poly_30_lied
rename polyarchy_age_group_lied10 pop_poly_60_lied
rename polyarchy_age_group_lied11 pop_poly_90_lied

rename suffrage_lied1 pop_unisuffrage_none
rename suffrage_lied2 pop_unisuffrage_men
rename suffrage_lied3 pop_unisuffrage_all
rename suffrage_lied4 pop_unisuffrage_miss

* Temporarily save data:
save "democracy/datasets/final/lexical_aggregated_popweighted_regions.dta", replace


** Merge different datasets:
use "democracy/datasets/refined/lexical_refined.dta"
merge 1:1 country_name year using "democracy/datasets/final/lexical_aggregated.dta"
drop _merge
merge 1:1 country_name year using "democracy/datasets/final/lexical_aggregated_popweighted.dta"
drop _merge
merge 1:1 country_name year using "democracy/datasets/final/lexical_aggregated_regions.dta"
drop _merge
merge 1:1 country_name year using "democracy/datasets/final/lexical_aggregated_popweighted_regions.dta", update
drop _merge
erase "democracy/datasets/final/lexical_aggregated.dta"
erase "democracy/datasets/final/lexical_aggregated_popweighted.dta"
erase "democracy/datasets/final/lexical_aggregated_regions.dta"
erase "democracy/datasets/final/lexical_aggregated_popweighted_regions.dta"


** Add regional identifiers to final dataset:
merge m:1 country_name using "Our World in Data/countries_regions_pairs.dta"
tab country_name if _merge == 1
replace region = "Africa" if country_name == "Cape Colony" | country_name == "Natal" | country_name == "Orange Free State" | country_name == "Transvaal"
replace region = "Asia" if country_name == "Palestine/British Mandate" | country_name == "Palestine/Gaza" | country_name == "Palestine/West Bank" |  country_name == "North Vietnam" | country_name == "Ottoman Empire" | country_name == "Tibet"
replace region = "Europe" if country_name == "Brunswick" | country_name == "Hamburg" | country_name == "Hesse-Darmstadt" | country_name == "Hesse-Kassel" | country_name == "Nassau" | country_name == "Oldenburg" | country_name == "Papal States" | country_name == "Prussia" | country_name == "Sardinia" | country_name == "Saxe-Weimar-Eisenach" | country_name == "Sicily"
replace region = "North America" if country_name == "United Provinces of Central America"
replace region = "South America" if country_name == "Great Colombia"
drop if _merge == 2
drop _merge


** Label variables:
label variable number_nonelectaut_lied "Number of non-electoral autocracies (LIED)"
label variable number_onepaut_lied "Number of one-party autocracies (LIED)"
label variable number_multipautne_lied "Number of multi-party autocracies without elected executive (LIED)"
label variable number_multipaut_lied "Number of multi-party autocracies (LIED)"
label variable number_excldem_lied "Number of exclusive democracies (LIED)"
label variable number_maledem_lied "Number of male democracies (LIED)"
label variable number_electdem_lied "Number of electoral democracies (LIED)"
label variable number_poly_lied "Number of polyarchies (LIED)"

label variable pop_nonelectaut_lied "People living in non-electoral autocracies (LIED)"
label variable pop_onepaut_lied "People living in one-party autocracies (LIED)"
label variable pop_multipautne_lied "People living in multi-party autocracies without elected executive (LIED)"
label variable pop_multipaut_lied "People living in multi-party autocracies (LIED)"
label variable pop_excldem_lied "People living in exclusive democracies (LIED)"
label variable pop_maledem_lied "People living in male democracies (LIED)"
label variable pop_electdem_lied "People living in electoral democracies (LIED)"
label variable pop_poly_lied "People living inpolyarchies (LIED)"
label variable pop_missreg_lied "People living in countries without regime data (LIED)"

label variable number_electdem_18_lied "Number of electoral democracies aged 1-18 years (LIED)"
label variable number_electdem_30_lied "Number of electoral democracies aged 19-30 years (LIED)"
label variable number_electdem_60_lied "Number of electoral democracies aged 31-60 years (LIED)"
label variable number_electdem_90_lied "Number of electoral democracies aged 61-90 years (LIED)"
label variable number_electdem_91plus_lied "Number of electoral democracies aged 91 years or older (LIED)"

label variable number_poly_18_lied "Number of polyarchies aged 1-18 years (LIED)"
label variable number_poly_30_lied "Number of polyarchies aged 19-30 years (LIED)"
label variable number_poly_60_lied "Number of polyarchies aged 31-60 years (LIED)"
label variable number_poly_90_lied "Number of polyarchies aged 61-90 years (LIED)"

label variable pop_electdem_18_lied "People living in electoral democracies aged 1-18 years (LIED)"
label variable pop_electdem_30_lied "People living in electoral democracies aged 19-30 years (LIED)"
label variable pop_electdem_60_lied "People living in electoral democracies aged 31-60 years (LIED)"
label variable pop_electdem_90_lied "People living in electoral democracies aged 61-90 years (LIED)"
label variable pop_electdem_91plus_lied "People living in electoral democracies aged 91 years or older (LIED)"

label variable pop_poly_18_lied "People living in polyarchies aged 1-18 years (LIED)"
label variable pop_poly_30_lied "People living in polyarchies aged 19-30 years (LIED)"
label variable pop_poly_60_lied "People living in polyarchies aged 31-60 years (LIED)"
label variable pop_poly_90_lied "People living in polyarchies aged 61-90 years (LIED)"

label variable number_unisuffrage_none "Number of countries without universal suffrage (LIED)"
label variable number_unisuffrage_men "Number of countries with universal suffrage for men (LIED)"
label variable number_unisuffrage_all "Number of countries with universal suffrage for men and women (LIED)"

label variable pop_unisuffrage_none "People living in countries without universal suffrage (LIED)"
label variable pop_unisuffrage_men "People living in countries with universal suffrage for men (LIED)"
label variable pop_unisuffrage_all "People living in countries with universal suffrage for men and women (LIED)"
label variable pop_unisuffrage_miss "People living in countries with no data on universal suffrage (LIED)"

label variable region "Region"


** Order observations:
sort country_name year


** Export data:
save "democracy/datasets/final/lexical_final.dta", replace
export delimited "democracy/datasets/final/lexical_final.csv", replace nolabel

describe, replace
keep name varlab
rename name varname
rename varlab varlabel
export delimited "democracy/datasets/final/lexical_final_meta.csv", replace


exit
