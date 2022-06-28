*****  This Stata do-file cleans the Lexical Index of Electoral Democracy (LIED) dataset
*****  Author: Bastian Herre
*****  June 28, 2022


version 14

clear all
set more off
set varabbrev off


** Set your own working directories here to run the file:
cd "/Users/bastianherre/Dropbox/Data/"
global project "/Users/bastianherre/Dropbox/Data/"

* Download dataset from https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/WPKNIT and move it into the folder "Lexical Index of Electoral Democracy v6.4":

** Import Lexical Index-dataset:
import excel "Lexical Index of Electoral Democracy v6.4/LIED_6.4.xlsx", firstrow clear


** Keep variables of interest:
keep countryn year male_suffrage female_suffrage executive_elections legislative_elections multiparty_legislative_election competitive_elections political_liberties lexical_index lexical_index_plus
* Note: vdem-variable for V-Dem country code not included because of missing values.


** Rename variables of interest:
rename countryn country_name
rename executive_elections exelec_lied
rename legislative_elections legelec_lied
rename multiparty_legislative_election opposition_lied
rename competitive_elections competition_lied
rename political_liberties poliberties_lied
rename lexical_index regime_redux_lied
rename lexical_index_plus regime_lied
rename male_suffrage male_suffrage_lied
rename female_suffrage female_suffrage_lied


** Label variables of interest:
label variable country_name "Country name"
label variable year "Year"
label variable exelec_lied "Executive elections (Lexical Index)"
label variable legelec_lied "Legislative elections (Lexical Index)"
label variable opposition_lied "Political opposition (Lexical Index)"
label variable competition_lied "Competitive elections (Lexical Index)"
label variable poliberties_lied "Political liberties (Lexical Index)"
label variable male_suffrage_lied "Universal suffrage for men (Lexical Index)"
label variable female_suffrage_lied "Universal suffrage for women (Lexical Index)"
label variable regime_lied "Regime (Lexical Index)"


** Label values of variables of interest:
label define regime_lied 0 "non-electoral autocracy" 1 "one-party autocracy" 2 "multi-party autocracy without elected executive" 3 "multi-party autocracy" 4 "exclusive democracy" 5 "male democracy" 6 "electoral democracy" 7 "polyarchy"
label values regime_lied regime_lied
label values regime_redux_lied regime_lied

** Refine variables:
tab legelec_lied
tab opposition_lied // There should only be scores of 0 or 1.
list country_name year regime_lied if legelec_lied == 2 | opposition_lied == 2 // Regime coding indicates that the variables should be coded as 1.
replace opposition_lied = 1 if opposition_lied == 2
replace legelec_lied = 1 if legelec_lied == 2

duplicates drop


** Refine country names:
replace country_name = "Papal States" if country_name == "Papal states, the"
replace country_name = "Saint Kitts and Nevis" if country_name == "St. Kitts and Nevis"
replace country_name = "Saint Lucia" if country_name == "St. Lucia"
replace country_name = "Saint Vincent and the Grenadines" if country_name == "St. Vincent and the Grenadines"
replace country_name = "Great Colombia" if country_name == "Gran Colombia"
replace country_name = "Mecklenburg Schwerin" if country_name == "Mecklenburg-Schwerin"
replace country_name = "North Macedonia" if country_name == "Macedonia"
replace country_name = "Congo" if country_name == "Congo Brazzaville"
replace country_name = "Democratic Republic of Congo" if country_name == "Congo, Democratic Republic"
replace country_name = "Czechia" if country_name == "Czech Republic"
replace country_name = "Timor" if country_name == "East Timor"
replace country_name = "North Korea" if country_name == "Korea, North"
replace country_name = "South Korea" if country_name == "Korea, South"
replace country_name = "Republic of Vietnam" if country_name == "Vietnam, South"
replace country_name = "Eswatini" if country_name == "Swaziland"
replace country_name = "Western Sahara" if country_name == "Sahrawi"
replace country_name = "East Germany" if country_name == "Germany, East"
replace country_name = "West Germany" if country_name == "Germany, West"
replace country_name = "United Korea" if country_name == "Korea"
replace country_name = "Micronesia (country)" if country_name == "Micronesia"
replace country_name = "Serbia and Montenegro" if country_name == "Serbia-Montenegro"
replace country_name = "Yemen People's Republic" if country_name == "Yemen, South"
replace country_name = "North Vietnam" if country_name == "Vietnam, North"
replace country_name = "Wuerttemburg" if country_name == "Wuerttemberg"
replace country_name = "Yemen Arab Republic" if country_name == "Yemen, North"


** Order variables and observations:
order country_name year regime_lied regime_redux_lied exelec_lied legelec_lied opposition_lied competition_lied male_suffrage_lied female_suffrage_lied poliberties_lied
sort country_name year


** Export datasets:
save "democracy/datasets/cleaned/lied_cleaned.dta", replace
export delimited "democracy/datasets/cleaned/lied_cleaned.csv", replace nolabel



exit
