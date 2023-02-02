*****  This Stata do-file cleans the Democracy-Index 2021 dataset by the Economist Intelligence Unit (EIU)
*****  Author: Bastian Herre
*****  February 2, 2023

version 14
clear all
set more off
set varabbrev off


** Set your own working directories here to run the file:
cd "/Users/bastianherre/Dropbox/Data/"
global project "/Users/bastianherre/Dropbox/Data/"


** Export EIU dataset 2021 from https://www.eiu.com/n/campaigns/democracy-index-2021/ into the file "eiu_2021.xlsx" move it into the folder "EIU 2022 Democracy Index"
** Import EIU 2021 dataset:
import excel "EIU 2022 Democracy Index/eiu_2021.xlsx", clear firstrow



** Keep variables of interest:
drop rank_eiu

destring democracy_eiu elect_freefair_eiu funct_gov_eiu pol_part_eiu dem_culture_eiu civlib_eiu, replace


** Add year identifier:
generate year = 2021


* Refine country names:
replace country_name = "Bosnia and Herzegovina" if country_name == "Bosnia and Hercegovina"
replace country_name = "Congo" if country_name == "Congo (Brazzaville)"
replace country_name = "Cape Verde" if country_name == "Cabo Verde"
replace country_name = "Czechia" if country_name == "Czech Republic"
replace country_name = "Cote d'Ivoire" if country_name == "Côte d'Ivoire"
replace country_name = "Kyrgyzstan" if country_name == "Kyrgyz Republic"
replace country_name = "Timor" if country_name == "Timor-Leste"
replace country_name = "United States" if country_name == "United States of America"

sort country_name year


** Export cleaned EIU 2021 data:
save "democracy/datasets/cleaned/eiu_2021.dta", replace


** Export EIU dataset 2022 from https://www.eiu.com/n/campaigns/democracy-index-2022/ into the file "eiu_2022.xlsx" move it into the folder "EIU 2022 Democracy Index"
** Import EIU 2022 dataset:
import excel "EIU 2022 Democracy Index/eiu_2022.xlsx", clear firstrow



** Keep variables of interest:
drop rank_eiu


** Add year identifier:
generate year = 2022


* Refine country names:
replace country_name = "Bosnia and Herzegovina" if country_name == "Bosnia and Hercegovina"
replace country_name = "Congo" if country_name == "Congo (Brazzaville)"
replace country_name = "Cape Verde" if country_name == "Cabo Verde"
replace country_name = "Czechia" if country_name == "Czech Republic"
replace country_name = "Cote d'Ivoire" if country_name == "Côte d’Ivoire"
replace country_name = "Kyrgyzstan" if country_name == "Kyrgyz Republic"
replace country_name = "Timor" if country_name == "Timor-Leste"
replace country_name = "United States" if country_name == "United States of America"

sort country_name year


** Export cleaned EIU 2022 data:
save "democracy/datasets/cleaned/eiu_2022.dta", replace


** Download EIU dataset 2006-2020 from gapminder — http://www.gapm.io/dxlsdemocrix — and move it into the folder "EIU 2021 Democracy Index"
** Import EIU 2006-2020 dataset:
import excel "EIU 2022 Democracy Index/_EIU-Democracy Indices - Dataset - v4.xlsx", clear firstrow sheet("data-for-countries-etc-by-year")


** Keep observations of interest:
drop if name == ""


** Keep variables of interest:
keep name time DemocracyindexEIU ElectoralpluralismindexEIU GovernmentindexEIU PoliticalparticipationindexEI PoliticalcultureindexEIU CivillibertiesindexEIU


** Keep years of interest: (gapminder interpolates years for 2007 and 2009)
drop if time == 2007 | time == 2009


** Rename variables of interest:
rename name country_name
rename time year
rename DemocracyindexEIU democracy_eiu
rename ElectoralpluralismindexEIU elect_freefair_eiu
rename GovernmentindexEIU funct_gov_eiu
rename PoliticalparticipationindexEI pol_part_eiu
rename PoliticalcultureindexEIU dem_culture_eiu
rename CivillibertiesindexEIU civlib_eiu


** Refine variables of interest:

replace democracy_eiu = democracy_eiu / 10 //  gapminder multiplies all values by ten.
replace elect_freefair_eiu = elect_freefair_eiu / 10
replace funct_gov_eiu = funct_gov_eiu / 10
replace pol_part_eiu = pol_part_eiu / 10
replace dem_culture_eiu = dem_culture_eiu / 10
replace civlib_eiu = civlib_eiu / 10

replace country_name = "Democratic Republic of Congo" if country_name == "Congo, Dem. Rep."
replace country_name = "Congo" if country_name == "Congo, Rep."
replace country_name = "Czechia" if country_name == "Czech Republic"
replace country_name = "Hong Kong" if country_name == "Hong Kong, China"
replace country_name = "Kyrgyzstan" if country_name == "Kyrgyz Republic"
replace country_name = "Laos" if country_name == "Lao"
replace country_name = "North Macedonia" if country_name == "Macedonia, FYR"
replace country_name = "Slovakia" if country_name == "Slovak Republic"
replace country_name = "Eswatini" if country_name == "Swaziland"
replace country_name = "Timor" if country_name == "Timor-Leste"


** Add missing observations:

insobs 1
replace country_name = "Algeria" if country_name == ""

insobs 1
replace country_name = "Iran" if country_name == ""

insobs 1
replace country_name = "Lithuania" if country_name == ""

insobs 1
replace country_name = "Ukraine" if country_name == ""

replace year = 2020 if year == .

replace democracy_eiu = 3.77 if country_name == "Algeria" & year == 2020
replace democracy_eiu = 2.20 if country_name == "Iran" & year == 2020
replace democracy_eiu = 7.13 if country_name == "Lithuania" & year == 2020
replace democracy_eiu = 5.81 if country_name == "Ukraine" & year == 2020

replace elect_freefair_eiu = 3.08 if country_name == "Algeria" & year == 2020
replace elect_freefair_eiu = 0.00 if country_name == "Iran" & year == 2020
replace elect_freefair_eiu = 9.58 if country_name == "Lithuania" & year == 2020
replace elect_freefair_eiu = 8.25 if country_name == "Ukraine" & year == 2020

replace funct_gov_eiu = 2.50 if country_name == "Algeria" & year == 2020
replace funct_gov_eiu = 2.50 if country_name == "Iran" & year == 2020
replace funct_gov_eiu = 6.07 if country_name == "Lithuania" & year == 2020
replace funct_gov_eiu = 2.71 if country_name == "Ukraine" & year == 2020

replace pol_part_eiu = 4.44 if country_name == "Algeria" & year == 2020
replace pol_part_eiu = 3.89 if country_name == "Iran" & year == 2020
replace pol_part_eiu = 5.56 if country_name == "Lithuania" & year == 2020
replace pol_part_eiu = 7.22 if country_name == "Ukraine" & year == 2020

replace dem_culture_eiu = 5.00 if country_name == "Algeria" & year == 2020
replace dem_culture_eiu = 3.13 if country_name == "Iran" & year == 2020
replace dem_culture_eiu = 5.63 if country_name == "Lithuania" & year == 2020
replace dem_culture_eiu = 5.00 if country_name == "Ukraine" & year == 2020

replace civlib_eiu = 3.82 if country_name == "Algeria" & year == 2020
replace civlib_eiu = 1.47 if country_name == "Iran" & year == 2020
replace civlib_eiu = 8.82 if country_name == "Lithuania" & year == 2020
replace civlib_eiu = 5.88 if country_name == "Ukraine" & year == 2020


** Merge with EIU 2021 data:
append using "democracy/datasets/cleaned/eiu_2021.dta"
erase "democracy/datasets/cleaned/eiu_2021.dta"


** Merge with EIU 2022 data:
append using "democracy/datasets/cleaned/eiu_2022.dta"
erase "democracy/datasets/cleaned/eiu_2022.dta"


** Create regime identifier:
generate regime_eiu = .
replace regime_eiu = 0 if democracy_eiu >= 0 & democracy_eiu <= 4
replace regime_eiu = 1 if democracy_eiu > 4 & democracy_eiu <= 6
replace regime_eiu = 2 if democracy_eiu > 6 & democracy_eiu <= 8
replace regime_eiu = 3 if democracy_eiu > 8 & democracy_eiu <= 10

label define regime_eiu 0 "authoritarian regime" 1 "hybrid regime" 2 "flawed democracy" 3 "full democracy"
label values regime_eiu regime_eiu


** Relabel variables of interest:
label variable country_name "Country name"
label variable year "Year"
label variable regime_eiu "Regime (EIU)"
label variable democracy_eiu "Democracy score (EIU)"
label variable elect_freefair_eiu "Free and fair elections (EIU)"
label variable funct_gov_eiu "Functioning government (EIU)"
label variable pol_part_eiu "Political participation (EIU)"
label variable dem_culture_eiu "Democratic culture (EIU)"
label variable civlib_eiu "Civil liberties (EIU)"


** Order variables and observations:
order regime_eiu, after(year)
sort country_name year


** Export cleaned EIU data:
save "democracy/datasets/cleaned/eiu_cleaned.dta", replace
export delimited "democracy/datasets/cleaned/eiu_cleaned.csv", replace nolabel



exit
