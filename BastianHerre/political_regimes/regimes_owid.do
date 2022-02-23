*****  Stata do-file to create the expanded Regimes of the World (RoW) and Varieties of Democracy (V-Dem) data used in several posts on Our World in Data (OWID):
*****  Post 1: "The ‘Regimes of the World’ data: how do researchers identify which countries are democracies?"
*****  Post 2: "200 years ago, everyone lacked democratic rights. Now, billions of people have them"
*****  Post 3: "In most countries, democracy is a recent achievement. Dictatorship is far from a distant memory"
*****  Author: Bastian Herre
*****  February 17, 2022


version 14

clear all
set more off
set varabbrev off

* Set your own working directories here to run the file:
cd "/Users/bastianherre/Dropbox/Data/"
global project "/Users/bastianherre/Dropbox/Data/"



*** Create a master-dataset:

** The master-dataset includes all countries included in either the V-Dem, Boix-Miller-Rosato (BMR) or OWID population dataset, and all years included in V-Dem (1789-2020).
** It allows me to later map the population data onto BMR, RoW and V-Dem data.


** Download V-Dem dataset from https://www.v-dem.net/vdemds.html and move it into the folder "Coppedge et al. 2021 V-Dem"
** Import V-Dem dataset:
use "Coppedge et al. 2021 V-Dem/V-Dem-CY-Full+Others-v11.1.dta", clear

** Harmonize V-Dem and OWID country names:
replace country_name = "Myanmar" if country_name == "Burma/Myanmar"
replace country_name = "Democratic Republic of Congo" if country_name == "Democratic Republic of the Congo"
replace country_name = "Cote d'Ivoire" if country_name == "Ivory Coast"
replace country_name = "Congo" if country_name == "Republic of the Congo"
replace country_name = "Gambia" if country_name == "The Gambia"
replace country_name = "Palestine" if country_name == "Palestine/British Mandate"
replace country_name = "Timor" if country_name == "Timor-Leste"
replace country_name = "United States" if country_name == "United States of America"
replace country_name = "Wuerttemberg" if country_name == "Würtemberg"
replace country_name = "Czechia" if country_name == "Czech Republic"

** Download OWID population data from https://ourworldindata.org/grapher/population and move it into the folder "Our World in Data"
** Merge OWID population into V-Dem data:
sort country_name year
merge 1:1 country_name year using "Our World in Data/population_owid.dta"

** Take a look at unmerged cases:
tab country_name if _merge == 1 & year > 1799 // Unmerged observations in master dataset are from before 1800, are historical countries (e.g. Tuscany and German Democratic Republic), as well as Kosovo, Palestine/Gaza, Palestine/West Bank, Somaliland, and Zanzibar.
drop _merge

** Only keep one observation per country to avoid duplicates in later step:
keep country_name
sort country_name
duplicates drop
isid country_name

save "Political regimes/master_temp.dta", replace


** Download BMR dataset from https://sites.google.com/site/mkmtwo/data?authuser=0 and move it into the folder "Boix, Miller, Rosato 2022 regimes data"
** Import BMR dataset:
use "Boix, Miller, Rosato 2022 regimes data/democracy-v4.0.dta", replace

** Harmonize BMR country names with OWID names:
generate country_name = country
collapse (first) country, by(country_name)
keep country
sort country

export delimited "Boix, Miller, Rosato 2022 regimes data/bmr_countries.csv", replace

* I use the internal country-name-standardizer tool, which creates a file bith BMR's country names and the respective OWID names:

import delimited "Boix, Miller, Rosato 2022 regimes data/bmr_countries_country_standardized.csv", clear varnames(1) // The file is in the GitHub folder.

rename ourworldindataname country_name


** Harmonize remaining incorrectly formatted country names in BMR with OWID names:
replace country_name = "German Democratic Republic" if country_name == "East Germany"
replace country_name = "Micronesia" if country_name == "Micronesia (country)"
replace country_name = "Piedmont-Sardinia" if country_name == "Sardinia"
replace country_name = "Republic of Vietnam" if country_name == "South Vietnam"
replace country_name = "Germany" if country_name == "West Germany"
replace country_name = "Wuerttemberg" if country_name == "Wuerttemburg"
replace country_name = "Yemen" if country_name == "Yemen Arab Republic"
replace country_name = "South Yemen" if country_name == "Yemen People's Republic"


** Save list of original and harmonized BMR country names:
save "Boix, Miller, Rosato 2022 regimes data/bmr_countries.dta", replace


** Only keep one observation per country to avoid duplicates in later step:
keep country_name
tab country_name // Duplicates from countries that changed borders: Ethiopia, Germany, Pakistan, Russia, Serbia, Sudan, Vietnam, and Yemen.
duplicates drop
isid country_name

sort country_name
save "Boix, Miller, Rosato 2022 regimes data/bmr_temp.dta", replace


** Merge BMR into master data:
use "Political regimes/master_temp.dta", clear
merge 1:1 country_name using "Boix, Miller, Rosato 2022 regimes data/bmr_temp.dta"
tab country_name if _merge == 2 // Unmatched countries in BMR are historical countries Central American Union, Czechoslovakia, Great Colombia, Korea, and Orange Free State.
drop _merge
erase "Boix, Miller, Rosato 2022 regimes data/bmr_temp.dta"


** Expand country dataset to country-year dataset with years 1789 to 2020:
expand 232
bysort country_name: generate year = 1788+_n
label variable year "Year"
tab year

save "Political regimes/master.dta", replace



*** Prepare V-Dem data:

** Import V-Dem dataset again:
use "Coppedge et al. 2021 V-Dem/V-Dem-CY-Full+Others-v11.1.dta", clear

** Drop superfluous observations:
drop if country_name == "Italy" & year == 1861
replace country_name = "Italy" if country_name == "Piedmont-Sardinia" & year == 1861 // Piedmont-Sardinia became Italy during 1861.

** Recode errors in relative power of head of state and head of government variable in line with feedback by Marcus that head of government Mugabe was more powerful than head of state Banana.
replace v2ex_hosw = 0 if country_name == "Zimbabwe" & year >= 1980 & year <= 1986
replace v2ex_hogw = 1 if country_name == "Zimbabwe" & year >= 1980 & year <= 1986

** Recode error in head of state and head of government variables:

list v2exnamhos v2exnamhog v2exhoshog v2ex_hosw v2ex_hogw v2eltype* if country_name == "Russia" & year == 1917
replace v2ex_hosw = 1 if country_name == "Russia" & year == 1917
replace v2ex_hogw = 0 if country_name == "Russia" & year == 1917
* Only a head of state (Lenin) listed, so (absent) head of government incorrectly coded as more powerful than head of state; Lenin not appointed by a legislature, but 

list year v2exnamhos v2exnamhog v2exhoshog v2ex_hosw v2ex_hogw v2exaphogp if country_name == "Haiti" & year > 1990 & year < 1995
replace v2exnamhos = "Raoul Cédras" if country_name == "Haiti" & year >= 1991 & year <= 1993
replace v2ex_hosw = 1 if country_name == "Haiti" & year >= 1991 & year <= 1993
replace v2ex_hogw = 0 if country_name == "Haiti" & year >= 1991 & year <= 1993
replace v2exaphogp = 0 if country_name == "Haiti" & year >= 1991 & year <= 1993
* Goemans et al.'s (2009) Archigos dataset, rulers.org, and worldstatesmen.org identify non-elected General Raoul Cédras as the de-facto leader of Haiti from 1991 until 1994.



*** Create expanded Regimes of the World indicator:

** Create numeric country identifier:
encode country_name, generate(country_number)

** Declare dataset to be time-series data:
tsset country_number year

** Create indicator for multi-party elections with imputed values between election-years:
generate v2elmulpar_osp_imp = v2elmulpar_osp
replace v2elmulpar_osp_imp = l.v2elmulpar_osp_imp if v2elmulpar_osp_imp == . & v2x_elecreg == 1

** Create indicator for free and fair elections with imputed values between election-years:
generate v2elfrfair_osp_imp = v2elfrfair_osp
replace v2elfrfair_osp_imp = l.v2elfrfair_osp_imp if v2elfrfair_osp_imp == . & v2x_elecreg == 1

** Create indicators for multi-party executive elections, and multi-party executive elections with imputed values between election-years:
generate v2elmulpar_osp_ex = v2elmulpar_osp if v2eltype_6 == 1 | v2eltype_7 == 1
generate v2elmulpar_osp_ex_imp = v2elmulpar_osp_ex
replace v2elmulpar_osp_ex_imp = l.v2elmulpar_osp_ex_imp if v2elmulpar_osp_ex_imp == . & v2xex_elecreg == 1

** Create indicators for multi-party legislative elections, and multi-party legislative elections with imputed values between election-years:
generate v2elmulpar_osp_leg = v2elmulpar_osp if v2eltype_0 == 1 | v2eltype_1 == 1 | v2eltype_4 == 1 | v2eltype_5 == 1 // v2eltype_4 and v2eltype_5 excluded in Marcus Tannenberg and Anna Lührmann's Stata code; included here to align coding with code in V-Dem's data pipeline.
generate v2elmulpar_osp_leg_imp = v2elmulpar_osp_leg
replace v2elmulpar_osp_leg_imp = l.v2elmulpar_osp_leg_imp if v2elmulpar_osp_leg_imp == . & v2xlg_elecreg == 1

** Create indicator for multi-party head of state elections with imputed values between election-years:
generate v2elmulpar_osp_hos_imp = 0 if v2x_elecreg != .
* Marcus Tannenberg does not know why electoral regime used as filter instead of relative power of heads of state and government as filter, as above; Anna Lührmann wrote this code. Using electoral regime as filter for this and all following variables yields identical coding.
replace v2elmulpar_osp_hos_imp = 1 if v2expathhs == 7 & v2xex_elecreg == 1 & v2elmulpar_osp_ex_imp > 1 & v2elmulpar_osp_ex_imp != . // If head of state is directly elected, elections for executive must be multi-party.
replace v2elmulpar_osp_hos_imp = 1 if v2expathhs == 6 & v2xlg_elecreg == 1 & v2elmulpar_osp_leg_imp > 1 & v2elmulpar_osp_leg_imp !=. // If head of state is appointed by legislature, elections for legislature must be multi-party.
* replace v2elmulpar_osp_hos_imp = 1 if v2ex_legconhos == 1 & v2xlg_elecreg == 1 & v2elmulpar_osp_ex_imp > 1 & v2elmulpar_osp_ex_imp != . // If head of state is appointed otherwise, but approval by the legislature is necessary, elections for legislature must be multi-party.
* It is unclear why v2elmulpar_osp_ex_imp and not v2elmulpar_osp_leg_imp is used, if this is about legislative elections; this seems to be an error, which is why I use the following code instead:
replace v2elmulpar_osp_hos_imp = 1 if v2ex_legconhos == 1 & v2xlg_elecreg == 1 & v2elmulpar_osp_leg_imp > 1 & v2elmulpar_osp_leg_imp != . // If head of state is appointed otherwise, but approval by the legislature is necessary, elections for legislature must be multi-party.

** Create indicator for multi-party head of government elections with imputed values between election-years:
generate v2elmulpar_osp_hog_imp = 0 if v2x_elecreg != .
replace v2elmulpar_osp_hog_imp = 1 if v2expathhg == 8 & v2xex_elecreg == 1 & v2elmulpar_osp_ex_imp > 1 & v2elmulpar_osp_ex_imp != . // If head of government is directly elected, elections for executive must be multi-party.
replace v2elmulpar_osp_hog_imp = 1 if v2expathhg == 7 & v2xlg_elecreg == 1 & v2elmulpar_osp_leg_imp > 1 & v2elmulpar_osp_leg_imp != . // If head of government is appointed by legislature, elections for legislature must be multi-party.
replace v2elmulpar_osp_hog_imp = 1 if v2expathhg == 6 & v2elmulpar_osp_hos_imp == 1 // If head of government is appointed by the head of state, elections for the head of state must be multi-party.

* replace v2elmulpar_osp_hog_imp = 1 if v2exaphogp == 1 & v2elmulpar_osp_imp != . & v2elmulpar_osp_leg_imp > 1 & v2elmulpar_osp_leg_imp != . // If head of government is appointed otherwise, but approval by the legislature is necessary, elections for legislature must be multi-party.
* Marcus Tannenberg does not know why v2elmulpar_osp_imp used as filter here, and not v2xlg_elecreg; Anna Lührmann may have come up with this fix, as the only five observations coded differently - Cambodia 1973-1974 and Haiti 1992-1994 - in his opinion should be closed autocracies due to no elections being held due to civil war and military rule, respectively.
* But: as described above, Haiti's chief executive is coded incorrectly until 1994, and correcting for that turns the country into a closed autocracy from 1991 to 1993. In 1994 the previously elected president returns, and it is plausible to presume he and his head of government are accountable to the legislature again, making the country an electoral autocracy. And just because a civil war in Cambodia goes on, that does not mean that its chief executive is not accountable to a legislature anymore. I therefore do not use the fix here.
* Yet: I use v2ex_legconhog instead of v2exaphogp to use the variable analogous to v2ex_legconhos above:
replace v2elmulpar_osp_hog_imp = 1 if v2ex_legconhog == 1 & v2xlg_elecreg == 1 & v2elmulpar_osp_leg_imp > 1 & v2elmulpar_osp_leg_imp != . // If head of government is appointed otherwise, but approval by the legislature is necessary, elections for legislature must be multi-party.

** Create indicator for multi-party executive and legislative elections with imputed values between election-years:
generate v2elmulpar_osp_exleg_imp = 0 if v2ex_hosw != .
replace v2elmulpar_osp_exleg_imp = 1 if v2xlg_elecreg == 1 & v2xex_elecreg == 1 & v2elmulpar_osp_ex_imp > 1 & v2elmulpar_osp_ex_imp != . & v2elmulpar_osp_leg_imp > 1 & v2elmulpar_osp_leg_imp != .

** Create indicator for multi-party head of executive elections with imputed values between election-years:
generate v2elmulpar_osp_hoe_imp = 0 if v2ex_hosw != .
replace v2elmulpar_osp_hoe_imp = v2elmulpar_osp_hos_imp if v2ex_hosw <= 1 & v2ex_hosw > 0.5 // If head of state is more powerful than head of government, head of state is the head of the executive.
replace v2elmulpar_osp_hoe_imp = v2elmulpar_osp_hog_imp if v2ex_hosw <= 0.5 // If head of state is as or less powerful than head of government, head of government is the head of the executive.

* Some values of v2ex_hosw are missing, and using v2exhoshog and v2ex_hogw as well improves coverage; Marcus Lührmann agrees with the addition; I therefore add the next two lines:
replace v2elmulpar_osp_hoe_imp = v2elmulpar_osp_hos_imp if v2exhoshog == 1 // If head of state is also head of government, they are the head of the executive.
replace v2elmulpar_osp_hoe_imp = v2elmulpar_osp_hos_imp if v2ex_hogw == 0 // If head of government is less powerful than head of state, head of state must be more powerful than head of government.
* replace v2elmulpar_osp_hoe_imp = 1 if v2elmulpar_osp_exleg_imp == 1
* Marcus Tannenberg does not know why it is assumed that if legislative and executive are elected in multi-party elections, chief of executive is elected in multi-party elections - even if direct coding seems to disagree; Anna Lührmann wrote this code. This leads to regimes under prominent heads of state which came to office in coup d'etats or rebellions to not be classified as closed autocracies. I therefore do not use this line of code; I compare the differences between my coding and the standard RoW coding below.

** Create indicator for minimally free and fair and multi-party elections and minimal features of an electoral democracy otherwise:
generate v2x_polyarchy_dich_row = 0 if v2x_polyarchy != .
replace v2x_polyarchy_dich_row = 1 if v2x_polyarchy > 0.5 & v2x_polyarchy != . & v2elfrfair_osp_imp > 2 & v2elfrfair_osp_imp != . & v2elmulpar_osp_imp > 2 & v2elmulpar_osp_imp != . 

** Create indicator for minimally transparent laws, minimal access to the justice system for men and women, and minimal features of a liberal democracy otherwise:
generate v2x_liberal_dich_row = .
replace v2x_liberal_dich_row = 1 if v2x_liberal > 0.8 & v2x_liberal !=. & v2clacjstm_osp > 3 & v2clacjstm_osp != . & v2clacjstw_osp > 3 & v2clacjstw_osp != . & v2cltrnslw_osp > 3 & v2cltrnslw_osp != .

** Create indicator for Regimes of the World with expanded coverage and minor changes to coding:
gen v2x_regime_owid = .
replace v2x_regime_owid = 3 if v2x_polyarchy_dich_row == 1 & v2x_liberal_dich_row == 1
replace v2x_regime_owid = 2 if v2x_polyarchy_dich_row == 1 & v2x_liberal_dich_row != 1
replace v2x_regime_owid = 1 if v2x_polyarchy_dich_row == 0 & v2elmulpar_osp_hoe_imp == 1 & v2elmulpar_osp_leg_imp > 1
* The line above means that 101 observations are grouped into this category even though v2elmulpar_osp_leg_imp == ., as . is treated as positive infinity; I still follow RoW instead of not coding these observations.

list country_name year if v2x_polyarchy_dich_row == 0 & v2elmulpar_osp_hoe_imp == 1 & v2elmulpar_osp_leg_imp == .
replace v2x_regime_owid = 0 if v2x_polyarchy_dich_row == 0 & (v2elmulpar_osp_hoe_imp == 0 | v2elmulpar_osp_leg_imp <= 1) // = added to v2elmulpar_osp_leg_imp < 1, even if v2elmulpar_osp_leg_imp != 1 for all observations, for possible future iterations.
* These coding rules create seven observations which are coded as electoral democracies even though they have a chief executive who neither meets the criteria for direct or indirect election, nor for being dependent on the legislature.

list country_name year v2x_regime_owid v2x_polyarchy v2elmulpar_osp_hoe_imp if v2x_polyarchy > 0.5 & v2x_polyarchy != . & (v2elmulpar_osp_hoe_imp == 0 | v2elmulpar_osp_leg_imp <= 1) & v2x_regime_owid != 0
* I do not change the coding for these observations because I presume that the criteria for electoral democracy overrule the criteria for distinguishing between electoral and closed autocracies. This also means that I cannot use these criteria alone to code some observations for which only v2x_polyarchy is missing.

* But: if one criteria for electoral democracy is not met, and one criteria for electoral autocracy is not met, this must mean that the country is a closed autocracy:
replace v2x_regime_owid = 0 if (v2elfrfair_osp_imp <= 2 | v2elmulpar_osp_imp <= 2) & (v2elmulpar_osp_hoe_imp == 0 | v2elmulpar_osp_leg_imp <= 1) & v2x_regime_owid == .
* This also means that if one criteria for electoral democracy is not met, yet both criteria for an electoral autocracy is met, it must be an electoral autocracy:
replace v2x_regime_owid = 1 if (v2elfrfair_osp_imp <= 2 | v2elmulpar_osp_imp <= 2) & v2elmulpar_osp_hoe_imp == 1 & v2elmulpar_osp_leg_imp > 1 & v2elmulpar_osp_leg_imp != . & v2x_regime_owid == .

** Label indicator for Regimes of the World with expanded coverage and minor changes to coding:
label variable v2x_regime_owid "Regime (Regimes of the World, OWID)"
label define v2x_regime_owid_label 0 "closed autocracy" 1 "electoral autocracy" 2 "electoral democracy" 3 "liberal democracy"
label values v2x_regime_owid v2x_regime_owid_label


** Comparing my and standard RoW coding:

inspect v2x_regime_owid
inspect v2x_polyarchy // Expanded RoW has a slightly larger coverage than the continuous V-Dem measure because some observations are coded without using it.

tab v2x_regime_owid v2x_regime if year >= 1900, m

* Observations own classification identifies as electoral autocracies, whereas RoW identifies them as democracies:
list country_name year if v2x_regime_owid == 1 & v2x_regime == 2
* Papua New Guinea in 2002 and Tanzania in 2010 are coded differently because v2x_polyarchy in Marcus Tannenberg et al.'s input dataset is barely (0.5001598 and 0.5001345) above 0.5, whereas in the official dataset it is rounded to 0.5 and therefore is not above the coding threshold. The same holds for Belgium in 1898, which lies outside of the standard RoW, but which I compared with Johannes von Römer's expanded RoW coding for 1789-2020.
replace v2x_regime_owid = 2 if (country_name == "Tanzania" & year == 2010) | (country_name == "Papua New Guinea" & year == 2002)
replace v2x_regime_owid = 3 if country_name == "Belgium" & year == 1898

* 18 observations own classification identifies as closed autocracies, whereas RoW does not provide data:
list country_name year if v2x_regime_owid == 0 & v2x_regime == . & year >= 1900
* Libya in 1911, 1914, and 1922-1933 can be coded because I use information from v2exhoshog in addition to information from v2ex_hosw to identify head of the executive.
list v2ex_hosw v2exhoshog if v2x_regime_owid == 0 & v2x_regime == . & year >= 1900 & country_name == "Libya"
* Honduras in 1934 and 1935, Kazakhstan in 1990, and Turkmenistan in 1990 can be coded because I use information from the other criteria for democracies and autocracies in the absence of information from v2x_polyarchy:
list v2x_polyarchy v2elfrfair_osp_imp v2elmulpar_osp_imp v2elmulpar_osp_hoe_imp v2elmulpar_osp_leg_imp if v2x_regime_owid == 0 & v2x_regime == . & year >= 1900 & country_name != "Libya"

* 13 observations own classification identifies as electoral autocracies, whereas RoW does not provide data:
list country_name year if v2x_regime_owid == 1 & v2x_regime == . & year >= 1900
* Observations can be coded because I use information from the other criteria for democracies and autocracies in the absence of information from v2x_polyarchy:
list v2x_polyarchy v2elfrfair_osp_imp v2elmulpar_osp_imp v2elmulpar_osp_hoe_imp v2elmulpar_osp_leg_imp if v2x_regime_owid == 1 & v2x_regime == . & year >= 1900

* Observations own classification identifies as closed autocracies, whereas RoW identifies them as electoral autocracies:
list country_name year if v2x_regime_owid == 0 & v2x_regime == 1

* Belgium in 1919 is hard-recoded in RoW code, though Marcus Tannenberg does not know why that happens even if the errors in a previous version of the V-Dem dataset should by now be remedied; after changes to Zimbabwe above, it only continues to make a difference for Belgium in 1919; I keep the recode.
replace v2x_regime_owid = 1 if country_name == "Belgium" & year == 1919

label define v2expathhg 0 "Force" 1 "Foreign power" 2 "Ruling party" 3 "Royal council" 4 "Hereditary succession" 5 "Military" 6 "Head of state" 7 "Legislature" 8 "Directly" 9 "Other"
label values v2expathhg v2expathhg
list country_name year v2elmulpar_osp_exleg_imp v2elmulpar_osp_hoe_imp v2expathhs v2ex_legconhos v2elmulpar_osp_leg_imp if v2x_regime_owid == 0 & v2x_regime == 1 & v2ex_hosw <= 1 & v2ex_hosw > 0.5 & v2ex_legconhos == 0
* 100 observations with multi-party elections for legislature and executive (hence the RoW coding); but which had chief executive which were heads of state that were neither directly or indirectly chosen through multiparty elections, nor were they accountable to a legislature chosen through multi-party elections; I therefore do not recode them.
list country_name year v2exnamhos if v2x_regime_owid < v2x_regime & v2x_regime !=. & v2ex_hosw <= 1 & v2ex_hosw > 0.5
* Examples include many prominent heads of state which came to office in coup d'etats or rebellions, such as Boumedienne (Algeria 1965), Anez (Bolivia 2019), Buyoya (Burundi 1987), Batista (Cuba 1952), Ankrah (Ghana 1966), Khomeini (Iran 1980), Buhari (Nigeria 1983), Jammeh (Gambia 1994), and Eyadema (1967 Togo):

list country_name year v2elmulpar_osp_exleg_imp v2elmulpar_osp_hoe_imp v2expathhs v2ex_legconhos v2elmulpar_osp_leg_imp if v2x_regime_owid == 0 & v2x_regime == 1 & v2ex_hosw <= 1 & v2ex_hosw > 0.5 & v2ex_legconhos != 0
* Nicaragua in 1901 and 1905 with head of state appointed by the legislature, but missing value for v2elmulpar_osp_leg_imp; v2elmulpar_osp_exleg_imp and v2elmulpar_osp_hoe_imp are only not missing because its coding as 0 is based on v2ex_hosw. I leave the coding as is because the coding is the same in adjacent years.

* 37 observations which had multi-party elections for legislature and executive (hence the RoW coding); but which had chief executives which were heads of government that were neither directly or indirectly chosen through multiparty elections, nor were they accountable to a legislature chosen through multi-party elections:
list country_name year v2elmulpar_osp_exleg_imp v2expathhg v2ex_legconhog v2expathhs v2ex_legconhos if v2x_regime_owid == 0 & v2x_regime == 1 & v2elmulpar_osp_exleg_imp == 1 & v2ex_hosw <= 0.5
* Examples include prominent heads of government which came to office in a rebellion or were appointed by a foreign power, such as Castro (Cuba 1959) and Paul Vories McNutt (Philippines 1937):
list country_name year v2exnamhog if v2x_regime_owid < v2x_regime & v2x_regime !=. & v2ex_hosw <= 0.5

* 3 observations coded differently because I use v2ex_legconhog above for consistency, while RoW uses v2exaphogp instead. I defer to RoW coding in this cases. It may be that their data pipeline uses date-specific data which are superior to the year-end data used here. 
list country_name year v2expathhg v2ex_legconhog v2exaphogp if v2x_regime_owid == 0 & v2x_regime == 1 & v2elmulpar_osp_exleg_imp == 0 & v2ex_hosw <= 0.5
replace v2x_regime_owid = 1 if v2x_regime_owid == 0 & v2x_regime == 1 & v2elmulpar_osp_exleg_imp == 0 & v2ex_hosw <= 0.5

* Observations own classification identifies as electoral autocracies, whereas RoW identifies them as closed autocracies:
list country_name year if v2x_regime_owid == 1 & v2x_regime == 0

* 121 observations with chief executives that were heads of state directly or indirectly elected chief executive and at least moderately multi-party elections for legislative, but which are affected by RoW's different standard filter (2elmulpar_osp_ex_imp instead of v2elmulpar_osp_leg_imp) above:
list v2elmulpar_osp_leg_imp v2elmulpar_osp_hoe_imp v2elmulpar_osp_ex_imp v2elmulpar_osp_leg_imp if v2x_regime_owid == 1 & v2x_regime == 0 & v2ex_hosw <= 1 & v2ex_hosw > 0.5

* 3 observations with chief executives that were heads of government directly or indirectly elected chief executive and at least moderately multi-party elections for legislative, but which are affected by RoW's different standard filter (v2elmulpar_osp_imp instead of v2xlg_elecreg) above:
list v2elmulpar_osp_leg_imp v2elmulpar_osp_hoe_imp v2elmulpar_osp_imp v2xlg_elecreg if v2x_regime_owid == 1 & v2x_regime == 0 & v2ex_hosw <= 0.5


** Harmonize V-Dem and OWID country names:
replace country_name = "Myanmar" if country_name == "Burma/Myanmar"
replace country_name = "Democratic Republic of Congo" if country_name == "Democratic Republic of the Congo"
replace country_name = "Cote d'Ivoire" if country_name == "Ivory Coast"
replace country_name = "Congo" if country_name == "Republic of the Congo"
replace country_name = "Gambia" if country_name == "The Gambia"
replace country_name = "Palestine" if country_name == "Palestine/British Mandate"
replace country_name = "Timor" if country_name == "Timor-Leste"
replace country_name = "United States" if country_name == "United States of America"
replace country_name = "Wuerttemberg" if country_name == "Würtemberg"
replace country_name = "Czechia" if country_name == "Czech Republic"



*** Inspect V-Dem democracy indices, their sub-indices, and upper- and lower-bound estimates wherever available:

inspect v2x_polyarchy
inspect v2x_elecoff
inspect v2xel_frefair
inspect v2x_frassoc_thick
inspect v2x_suffr
inspect v2x_freexp_altinf

inspect v2x_polyarchy_codelow
inspect v2xel_frefair_codelow
inspect v2x_frassoc_thick_codelow
inspect v2x_freexp_altinf_codelow

inspect v2x_polyarchy_codehigh
inspect v2xel_frefair_codehigh
inspect v2x_frassoc_thick_codehigh
inspect v2x_freexp_altinf_codehigh

inspect v2x_libdem
inspect v2x_partipdem
inspect v2x_delibdem
inspect v2x_egaldem

inspect v2x_liberal
inspect v2x_partip
inspect v2xdl_delib
inspect v2x_egal

inspect v2xcl_rol
inspect v2x_jucon
inspect v2xlg_legcon

inspect v2x_cspart
inspect v2xdd_dd
inspect v2xel_locelec
inspect v2xel_regelec

inspect v2dlreason
inspect v2dlcommon
inspect v2dlcountr
inspect v2dlconslt
inspect v2dlengage

inspect v2xeg_eqprotec
inspect v2xeg_eqaccess
inspect v2xeg_eqdr

keep country_name year v2x_regime_owid v2elfrfair_osp_imp v2elmulpar_osp_imp v2elmulpar_osp_hoe_imp v2elmulpar_osp_leg_imp v2x_liberal_dich_row v2xlg_legcon v2lgqstexp v2lgotovst v2lginvstp v2lgoppart v2svindep ///
	v2x_polyarchy v2x_elecoff v2xel_frefair v2x_frassoc_thick v2x_suffr v2x_freexp_altinf v2x_polyarchy_codelow v2xel_frefair_codelow v2x_frassoc_thick_codelow v2x_freexp_altinf_codelow v2x_polyarchy_codehigh v2xel_frefair_codehigh v2x_frassoc_thick_codehigh v2x_freexp_altinf_codehigh ///
	v2x_libdem v2x_liberal v2xcl_rol v2x_jucon v2xlg_legcon v2x_libdem_codelow v2x_liberal_codelow v2xcl_rol_codelow v2x_jucon_codelow v2xlg_legcon_codelow v2x_libdem_codehigh v2x_liberal_codehigh v2xcl_rol_codehigh v2x_jucon_codehigh v2xlg_legcon_codehigh ///
	v2x_partipdem v2x_partip v2x_cspart v2xdd_dd v2xel_locelec v2xel_regelec v2x_partipdem_codelow v2x_partip_codelow v2x_cspart_codelow v2xel_locelec_codelow v2xel_regelec_codelow v2x_partipdem_codehigh v2x_partip_codehigh v2x_cspart_codehigh v2xel_locelec_codehigh v2xel_regelec_codehigh ///
	v2x_delibdem v2xdl_delib v2dlreason v2dlcommon v2dlcountr v2dlconslt v2dlengage v2x_delibdem_codelow v2xdl_delib_codelow v2dlreason_codelow v2dlcommon_codelow v2dlcountr_codelow v2dlconslt_codelow v2dlengage_codelow v2x_delibdem_codehigh v2xdl_delib_codehigh v2dlreason_codehigh v2dlcommon_codehigh v2dlcountr_codehigh v2dlconslt_codehigh v2dlengage_codehigh ///
	v2x_egaldem v2x_egal v2xeg_eqprotec v2xeg_eqaccess v2xeg_eqdr v2x_egaldem_codelow v2x_egal_codelow v2xeg_eqprotec_codelow v2xeg_eqaccess_codelow v2xeg_eqdr_codelow v2x_egaldem_codehigh v2x_egal_codehigh v2xeg_eqprotec_codehigh v2xeg_eqaccess_codehigh v2xeg_eqdr_codehigh

save "Political regimes/vdem_temp.dta", replace



*** Add regime dataset to master dataset:

use "Political regimes/master.dta", clear

merge 1:1 country_name year using "Political regimes/vdem_temp.dta"

generate vdem_obs = 1 if _merge == 3
replace vdem_obs = 0 if _merge == 1

label variable vdem_obs "Observation includes information from V-Dem"

drop _merge

erase "Political regimes/master.dta"

sort country_name year



*** Expand V-Dem data by imputing values from other countries:

** Investigate whether non-independent states have diverse regime types:
tab v2svindep v2x_regime_owid
* Most non-independent states are closed autocracies, but there are some electoral autocracies (and even electoral and liberal democracies: Australia 1858-1899, Iceland 1920-1943, Slovenia 1991). Non-independent states therefore better not be imputed as (closed) autocracies.

tab v2x_regime_owid if v2x_liberal == .
list v2x_regime_owid v2x_liberal_dich_row v2x_liberal v2xlg_legcon v2lgqstexp v2lgotovst v2lginvstp v2lgoppart if country_name == "Australia" & year >= 1895 & year <= 1905
replace v2x_regime_owid = 3 if country_name == "Australia" & year == 1900
* The only case for which a missing value of v2x_liberal matters is Australia in 1900. I manually recode it above because the values in the surrounding year strongly suggest a coding as a liberal democracy.

list if country_name == "Sweden" & year == 1840
replace v2x_regime_owid = 0 if country_name == "Sweden" & year == 1840
* Data (including for v2x_polyarchy) missing without clear reason, history of Sweden does not indicate consequential event; perhaps due to missing data on head of government, who is not listed even though he existed (likely Arvid Mauritz Posse). I manually recode it with the regime type in adjacent years.

** Possible imputations:
list year v2x_regime_owid v2x_polyarchy v2elfrfair_osp_imp v2elmulpar_osp_imp v2elmulpar_osp_hoe_imp v2elmulpar_osp_leg_imp if country_name == "Peru" & year >= 1880 & year <= 1900
* I favor no imputation because of six years of missing data, and even though one criterion for electoral autocracy is not met, the country may have met the criteria for democracy (if unlikely), thereby overriding the former.
list year v2x_regime_owid v2x_polyarchy v2elfrfair_osp_imp v2elmulpar_osp_imp v2elmulpar_osp_hoe_imp v2elmulpar_osp_leg_imp if country_name == "Honduras" & year >= 1910 & year <= 1950
* I favor no imputation because of 12 years of missing data, and the country may have met the criteria for democracy.

** Identify the relevant political entity for imputation:
* I identified the following countries and years as candidates for imputation because OWID population data is available, but I was unable to code a regime type.
* I only check candidates with a population of at one point more than 1 million
* Wimmer and Min (2006) code the status of a country at the end of the year, CShapes 2.0 codes its borders at the beginning of the year.

generate country_name_regime_imputed = ""

* Germany 1945-1948: occupied by United States (Cshapes 2.0); I favor no imputation.
* Bangladesh 1789-1970: 1947-1970 imperial power/part of Pakistan (Wimmer and Min 2006, Cshapes 2.0), 1765-1946 imperial power United Kingdom, 1886-1946 part of colony India (Cshapes 2.0), colonized in 1757 (Ertan et al. 2016).
replace country_name_regime_imputed = "Pakistan" if country_name == "Bangladesh" & year >= 1947 & year <= 1970
replace country_name_regime_imputed = "India" if country_name == "Bangladesh" & year >= 1789 & year <= 1946
* Ukraine 1789-1989: 1946-1989 imperial power/part of Russia (Wimmer and Min 2006, Cshapes 2.0), 1921-1945 and 1816-1918 mixed rule (Wimmer and Min 2006).
replace country_name_regime_imputed = "Russia" if country_name == "Ukraine" & year >= 1946 & year <= 1989
* Pakistan 1789-1946: 1839-1946 imperial power United Kingdom (Wimmer and Min 2006), 1886-1947 part of colony India (Cshapes 2.0), colonized in 1849 (Ertan et al. 2016).
replace country_name_regime_imputed = "India" if country_name == "Pakistan" & year >= 1839 & year <= 1946
* Poland 1789-1808, 1868-1917, 1939-1943: no information 1800-1808, 1795-1914 mixed rule (Wimmer and Min 2006), 1939-1943 independent (Cshapes 2.0); I favor no imputation.
* Italy 1789-1860: 1814-1860 part of Austria-Hungary (Wimmer and Min 2006) or Piedmont since 1815 (Butcher and Griffiths 2020).
replace country_name_regime_imputed = "Piedmont-Sardinia" if country_name == "Italy" & year >= 1815 & year <= 1860
* Nigeria 1789-1913: imperial power United Kingdom 1861-1959 (Wimmer and Min 2006), colony of United Kingdom (Cshapes 2.0), colonized by United Kingdom in 1885 (Ertan et al. 2016); I favor no imputation.
* Vietnam 1789-1944: 1861-1953 imperial power France (Wimmer and Min 2006) or 1886-1893 independent and 1894-1954 colonized by France (Cshapes 2.0), colonized by France in 1867 (Ertan et al. 2016), independent 1802-1884 (Butcher and Griffiths 2020); I favor no imputation.
* Uzbekistan 1789-1911, 1921-1989: imperial power Russia 1865-1990 (Wimmer and Min 2006), part of Russia 1886-1991 (Khiva and Bokhara partially as protectorates), not colonized (Ertan et al. 2016), Khiva and Bokhara as independent until -1872 and -1867.
replace country_name_regime_imputed = "Russia" if country_name == "Uzbekistan" & year >= 1865 & year <= 1911
replace country_name_regime_imputed = "Russia" if country_name == "Uzbekistan" & year >= 1921 & year <= 1989
* Kazakhstan 1789-1989: imperial power Russia 1730-1990 (Wimmer and Min 2006), part of Russia 1886-1991 (Cshapes 2.0); not colonized (Ertan et al. 2016).
replace country_name_regime_imputed = "Russia" if country_name == "Kazakhstan" & year >= 1789 & year <= 1989
* Mozambique 1789-1899, 1974-1993: imperial power Portugal 1885-1974 (Wimmer and Min 2006); colony of Portugal 1886-1975 (Cshapes 2.0), colonized by Portugal, approximated as 1750 (Ertan et al. 2016); I favor no imputation.
* Czechia 1789-1917: imperial power Austria-Hungary 16th century-1917 (Wimmer and Min 2006), part of Austria-Hungary since at least 1886 (Cshapes 2.0), Czech part under Austrian control (Encyclopedia Britannica).
replace country_name_regime_imputed = "Austria" if country_name == "Czechia" & year >= 1789 & year <= 1917
* Iran 1789-1899: no imperial onset (Wimmer and Min 2006), independent since at least 1886 (Cshapes 2.0), not colonized (Ertan et al. 2016); I favor no imputation.
* Belarus 1789-1989: imperial power Russia 1795-1990 (Wimmer and Min 2006); 1886-1991 part of Russia (Cshapes 2.0), not mentioned in Ertan et al. (2016), independent since 1991 (Butcher and Griffiths 2020).
replace country_name_regime_imputed = "Russia" if country_name == "Belarus" & year >= 1795 & year <= 1989
* Democratic Republic of Congo 1789-1899: imperial power Belgium 1885-1959 (Wimmer and Min 2006), colonized in 1885 (Ertan et al. 2016); I favor no imputation.
* North Korea 1789-1944: Korea since the 14th century until 1909, imperial power Japan 1910-1944 (Wimmer and Min 2006), independent Korea since at least 1886-1910, colony of Japan -1945 (Cshapes 2.0), not listed (Ertan et al. 2016).
replace country_name_regime_imputed = "South Korea" if country_name == "North Korea" & year >= 1789 & year <= 1910
* Sudan 1789-1899: Egypt imperial power 1821-1881, mixed rule 1882-1955 (Wimmer and Min 2006), colony of United Kingdom 1898-1955 (CShapes 2.0), colonized by United Kingdom in 1898 (Ertan et al. 2016), independent 1885-1898 (Butcher and Griffiths 2020); in 1886, colony Egypt of United Kingdom covers little of today's Sudan (CShapes 2.0); Egypt invades Sudanese territory in 1820, indigenous forces surrender in 1821, Mahdists capture Khartoum from Egypt and the British in 1885 (Encyclopedia Britannica).
replace country_name_regime_imputed = "Egypt" if country_name == "Sudan" & year >= 1821 & year <= 1884
* South Sudan 1789-2010: not listed, but Egypt imperial power of Sudan 1821-1881, mixed rule 1882-1955 (Wimmer and Min 2006), colony of United Kingdom 1898-1955, part of Sudan until 2012 (Cshapes 2.0), colonized by United Kingdom in 1898 (Ertan et al. 2016), independent 1885-1898 (Butcher and Griffiths 2020).
replace country_name_regime_imputed = "Egypt" if country_name == "South Sudan" & year >= 1821 & year <= 1884 // See immediately above.
replace country_name_regime_imputed = "Sudan" if country_name == "South Sudan" & year >= 1900 & year <= 2010
* Ireland 1789-1918: imperial power United Kingdom 11th century-1919 (Wimmer and Min 2006), part of United Kingdom since at least 1886-1922, independent since 1922 (Butcher and Griffiths 2020).
replace country_name_regime_imputed = "United Kingdom" if country_name == "Ireland" & year >= 1789 & year <= 1918
* Azerbaijan 1789-1989: imperial power Russia 1813-1917, 1920-1990 (Wimmer and Min 2006), part of Russia since at least 1886-1991 (Cshapes 2.0) not colonized (Ertan et al. 2016).
replace country_name_regime_imputed = "Russia" if country_name == "Azerbaijan" & year >= 1813 & year <= 1989
* Romania 1789-1830, 1854-1856, 1859-1899: 1688-1858 imperial power Austria-Hungary (Wimmer and Min 2006), independent since at least 1886 (Cshapes 2.0), independent since 1878 (Butcher and Griffiths 2020), Transylvania part of Austria-Hungary, other parts under Ottoman influence; I favor no imputation.
* Austria 1939-1944: imperial power Germany 1938-1944 (Wimmer and Min 2006), independent 1939-1944 (CShapes 2.0), independent 1918-1938 (Butcher and Griffiths 2020); I favor no imputation.
* Philippines 1789-1899: imperial power Spain 16th century-1898, United States 1899-1945 (Wimmer and Min 2006), colony of Spain since at least 1886-1898, colony of United States 1899-1946 (Cshapes 2.0); I favor no imputation.
* Greece 1789-1821, 1918-1919: imperial power Turkey 15th century - 1826, independent 1918-1919 (Wimmer and Min 2006, Cshapes 2.0); independent from 1828 to 1941 (Butcher and Griffiths 2020).
replace country_name_regime_imputed = "Turkey" if country_name == "Greece" & year >= 1789 & year <= 1821
* Tanzania 1789-1914: imperial power/colonized by Germany and United Kingdom (Wimmer and Min 2006, Cshapes 2.0); I favor no imputation. 
* Georgia 1789-1989: imperial power Russia 1801-1918, 1920-1990 (Wimmer and Min 2006), part of Russia since at least 1886-1991, not colonized (Ertan et al. 2016), independent since 1991 (Butcher and Griffiths 2020).
replace country_name_regime_imputed = "Russia" if country_name == "Georgia" & year >= 1801 & year <= 1989
* Slovakia 1789-1992: imperial power Austria-Hungary 16th century-1913, mixed rule 1914-1918, 1919-1992 imperial power Czechoslovakia (Wimmer and Min 2006), part of Austria-Hungary since at least 1886-1918, part of Czechoslovakia 1919-1992 (Cshapes 2.0), Slovak part under Hungarian control (Encyclopedia Britannica).
replace country_name_regime_imputed = "Hungary" if country_name == "Slovakia" & year >= 1789 & year <= 1918
replace country_name_regime_imputed = "Czechia" if country_name == "Slovakia" & year >= 1919 & year <= 1992
* South Africa 1789-1899: imperial power United Kingdom 1814-1909 (Wimmer and Min 2006); (mostly) colonized by United Kingdom 1886-1911 (Cshapes 2.0), colonized by United Kingdom in 1806, earlier also by Dutch settlers (Ertan et al. 2016); I favor no imputation.
* Cameroon 1789-1960: imperial power Germany 1884-1914, mixed rule 1915-1959 (Wimmer and Min 2006), colonized by Germany since at least 1886-1916, occupied by United Kingdom 1916-1919, mandate by France 1919-1959 (Cshapes 2.0); I favor no imputation.
* Tajikistan 1789-1989: imperial power Russia 1921-1990 (Wimmer and Min 2006), part of Russia, part of Russia's protectorate Bokhara 1886-1920, part of Russia 1920-1990 (Cshapes 2.0), independent since 1991, Bokhara independent 1816-1868 (Butcher and Griffiths 2020).
replace country_name_regime_imputed = "Russia" if country_name == "Tajikistan" & year >= 1868 & year <= 1989
* Palestine 1949-2019: no information (Wimmer and Min 2006, Ertan et al. 2016, Butcher and Griffiths 2020). V-Dem includes Gaza and West Bank separately; I therefore favor no imputation.
* Brazil 1824-1825: independent since 1822 (Wimmer and Min 2006, Butcher and Griffiths 2020); I favor no imputation.
* Serbia 1789-1833, 1932-1934: imperial power Turkey 14th century - 1877 (Wimmer and Min 2006); part of the Ottoman Empire (Encyclopedia Britannica); no imperial power 1932-1934 (Wimmer and Min 2006), independent 1932-1934 (Cshapes 2.0); I favor no imputation for later period. 
replace country_name_regime_imputed = "Turkey" if country_name == "Serbia" & year >= 1789 & year <= 1833
* Croatia 1789-1940, 1945-1990: Austria-Hungary imperial power 1699-1917, mixed rule 1918, Yugoslavia 1919-1990 (Wimmer and Min 2006); Austria-Hungary 1886-1918, 1919 partially Hungary and Yugoslavia, 1920-1992 Yugoslavia; I favor no imputation for earlier era.
replace country_name_regime_imputed = "Serbia" if country_name == "Croatia" & year >= 1945 & year <= 1990
* Algeria 1789-1899: imperial power France 1848-1961 (Wimmer and Min 2006), colonized by France since at least 1886-1962 (Cshapes 2.0); I favor no imputation.
* Bosnia and Herzegovina 1789-1991: imperial power Turkey 15th century-1878, Austria-Hungary 1879-1917, Yugoslavia 1918-1990 (Wimmer and Min 2006); occupied by Austria-Hungary since at least 1886-1908, part of Austria-Hungary 1909-1918, part of Yugoslavia 1919-1992 (Cshapes 2.0); Austrian-Hungary occupation while formally still part of Ottoman Empire, not more associated with either Austria or Hungary (Encyclopedia Britannica); I therefore favor no imputation for 1909-1918.
replace country_name_regime_imputed = "Turkey" if country_name == "Bosnia and Herzegovina" & year >= 1789 & year <= 1878
replace country_name_regime_imputed = "Serbia" if country_name == "Bosnia and Herzegovina" & year >= 1919 & year <= 1991
* Moldova 1789-1989: mixed rule 17th century-1939, imperial power Russia 1940-1990 (Wimmer and Min 2006), part of Russia since at least 1886-1919, part of Russia and Romania 1920-1939, part of Russia 1940-1991 (CShapes 2.0, Encyclopedia Britannica).
replace country_name_regime_imputed = "Russia" if country_name == "Moldova" & year >= 1789 & year <= 1919
replace country_name_regime_imputed = "Russia" if country_name == "Moldova" & year >= 1940 & year <= 1989
* Kyrgyzstan 1789-1989: imperial power Russia 1876-1990 (Wimmer and Min 2006), part of Russia since at least 1886-1991 (Cshapes 2.0), not colonized (Ertan et al. 2016), incorporated into Russia in mid-19th century (Encyclopedia Britannica).
replace country_name_regime_imputed = "Russia" if country_name == "Kyrgyzstan" & year >= 1876 & year <= 1989
* Kenya 1789-1899: protectorate of United Kingdom 1889-1920, colony of United Kingom 1921-1963 (CShapes 2.0); imperial power United Kingdom 1895-1962 (Wimmer and Min 2006); I favor no imputation.
* Burkina Faso 1789-1918, 1932-1946: imperial power France 1895-1959 (Wimmer and Min 2006); colony of France 1895-1960 (Cshapes 2.0); colonized by France in 1896 (Ertan et al. 2016); I favor no imputation.
* Sri Lanka 1789-1899: colonized by United Kingdom as Ceylon (Cshapes 2.0); I favor no imputation.
* Belgium 1789-1790, 1796-1829: imperial power Netherlands 1814-1831 (Wimmer and Min 2006), part of Austria - 1794, part of France 1795-1813, part of Netherlands 1814-1831 (Encyclopedia Britannica).
replace country_name_regime_imputed = "France" if country_name == "Belgium" & year >= 1796 & year <= 1813
replace country_name_regime_imputed = "Austria" if country_name == "Belgium" & year >= 1789 & year <= 1790
replace country_name_regime_imputed = "Netherlands" if country_name == "Belgium" & year >= 1814 & year <= 1829
* Lithuania 1940-1989: imperial power Russia 1940-1990 (Wimmer and Min 2006), part of Russia 1940-1991 (CShapes 2.0), independent 1918-1940, 1991- (Butcher and Griffiths 2020).
replace country_name_regime_imputed = "Russia" if country_name == "Lithuania" & year >= 1940 & year <= 1989
* Puerto Rico ..., 1940, 1950-2020: colony of Spain since at least 1886-1898, colony of United States 1899- (CShapes 2.0), colony of Spain since 16th century (Encyclopedia Britannica); I favor no imputation.
* Turkmenistan 1789-1989: imperial power Russia 1897-1990 (Wimmer and Min 2006), (mostly) part of Russia since 1886-1991, part protectorate Khiva 1886-1920 (Cshapes 2.0), not colonized (Ertan et al. 2016), resistance against Russia broken in 1881 (Encyclopedia Britannica).
replace country_name_regime_imputed = "Russia" if country_name == "Turkmenistan" & year >= 1886 & year <= 1989
* Armenia 1789-1989: mixed rule 17th century-1917, 1918-1990 Russia (Wimmer and Min 2006), part of Russia 1886-1991 (Cshapes 2.0); I favor no imputation for early years.
replace country_name_regime_imputed = "Russia" if country_name == "Armenia" & year >= 1918 & year <= 1989
* Uganda 1789-1899: part of Kenya, protectorate of United Kingdom 1892-1894 (CShapes 2.0); own protectorate of United Kingdom 1895-1962; imperial power United Kingdom 1890-1961 (Wimmer and Min 2006); I favor no imputation.
* Iraq 1789-1919: part of Turkey 1886-1920, mandate of United Kingdom 1921-1933 (CShapes 2.0); imperial power Turkey 16th century-1913, imperial power United Kingdom 1914-1931 (Wimmer and Min 2006).
replace country_name_regime_imputed = "Turkey" if country_name == "Iraq" & year >= 1789 & year <= 1919
* Yemen 1851-1917: mixed rule by Turkey and United Kingdom 1849-1918, part of Turkey 1886-1918 (CShapes 2.0), United Kingdom not on CShapes map.
replace country_name_regime_imputed = "Turkey" if country_name == "Yemen" & year >= 1851 & year <= 1917
* Angola 1789-1899: colony of Portugal 1886-1975 (CShapes 2.0); colony of imperial power Portugal 16th century-1974 (Wimmer and Min 2006); I favor no imputation.
* Bulgaria 1789-1877: imperial power Turkey 15th century-1878, independent in 1886 (CShapes 2.0).
replace country_name_regime_imputed = "Turkey" if country_name == "Bulgaria" & year >= 1789 & year <= 1877
* Lithuania 1789-1917: part of Russia 1886-1918 and 1941-1991 (CShapes 2.0), imperial power Russia 1795-1918 (Wimmer and Min 2006).
replace country_name_regime_imputed = "Russia" if country_name == "Lithuania" & year >= 1795  & year <= 1917
* Cambodia 1789-1899: colonized by France 1886-1953 (CShapes 2.0), imperial power France 1857-1952 (Wimmer and Min 2006), colonized in 1863 (Ertan et al. 2016); I favor no imputation.
* Taiwan 1789-1899: part of China 1886-1895, colony of Japan afterwards (CShapes 2.0), imperial power China 17th century - 1947 (Wimmer and Min 2006), colonized by Japan 1895-1945 (Ertan et al. 2016).
replace country_name_regime_imputed = "China" if country_name == "Taiwan" & year >= 1789 & year <= 1894
* Ghana 1789-1901: colonized by United Kingdom 1886-1957 (CShapes 2.0), imperial power Portugal 15th century - 1823, United Kingdom 1874-1956 (Wimmer and Min 2006); I favor no imputation.
* Latvia 1789-1919, 1940-1989: part of Russia 1886-1918 and 1941-1991 (CShapes 2.0), imperial power Russia 1710-1918 and 1940-1990 (Wimmer and Min 2006); I include 1919.
replace country_name_regime_imputed = "Russia" if country_name == "Latvia" & year >= 1789 & year <= 1919
replace country_name_regime_imputed = "Russia" if country_name == "Latvia" & year >= 1940 & year <= 1989
* Mali 1789-1899: colonized by France since 1896 (CShapes 2.0), imperial power France since 1895 (Wimmer and Min 2006); I favor no imputation.
* Syria 1789-1917, 1920-1921: part of Turkey 1886-1920 (CShapes 2.0), imperial power Turkey 1840-1919, France 1920-1943 (Wimmer and Min 2006), colonized by France in 1920 (Ertan et al. 2016), part of of Ottoman Empire 16th century-1830, of Egypt 1831-1839 (Encyclopedia Britannica).
replace country_name_regime_imputed = "Turkey" if country_name == "Syria" & year >= 1789 & year <= 1830
replace country_name_regime_imputed = "Egypt" if country_name == "Syria" & year >= 1831 & year <= 1839
replace country_name_regime_imputed = "Turkey" if country_name == "Syria" & year >= 1840 & year <= 1917
* Malawi 1789-1899: colonized by United Kingdom 1892-1964 (CShapes 2.0), imperial power United Kingdom 1889-1963 (Wimmer and Min 2006); I favor no imputation.
* Netherlands 1811-1812: part of France (Encyclopedia Britannica)
replace country_name_regime_imputed = "France" if country_name == "Netherlands" & year >= 1811 & year <= 1812
* Saudi Arabia 1819-1821: part of Turkey 1886-1919, nothing 1920-1932 (CShapes 2.0), not included (Wimmer and Min 2006), not colonized (Ertan et al. 2016), independent 1816-1818 (Butcher and Griffiths 2020), part of Ottoman Empire (Encyclopedia Britannica).
replace country_name_regime_imputed = "Turkey" if country_name == "Saudi Arabia" & year >= 1819 & year <= 1821
* Malaysia 1789-1899: colonized by United Kingom 1886-1957, imperial power United Kingdom 1795-1956 (Wimmer and Min 2006); I favor no imputation.
* North Macedonia 1789-1990: part of Turkey 1886-1913, part of Serbia 1914-1915, occupied by Austria/Hungary 1916-1918, part of Yugoslavia 1919-1991 (CShapes 2.0); imperial power Turkey 14th century -1913, Yugoslavia 1914-1990 (Wimmer and Min 2006).
replace country_name_regime_imputed = "Turkey" if country_name == "North Macedonia" & year >= 1789 & year <= 1913
replace country_name_regime_imputed = "Serbia" if country_name == "North Macedonia" & year >= 1914 & year <= 1990
* Slovenia 1789-1988: part of Austria-Hungary 1886-1918, of Austria 1919, of Yugoslavia 1920-1992 (CShapes 2.0), imperial power Austria-Hungary 1804-1917, Yugoslavia 1918-1990 (Wimmer and Min 2006), appears more closely affiliated with Austria, as Hungary barely referenced (Encyclopedia Britannica).
replace country_name_regime_imputed = "Serbia" if country_name == "Slovenia" & year >= 1919 & year <= 1988
replace country_name_regime_imputed = "Austria" if country_name == "Slovenia" & year >= 1804 & year <= 1918
* Chad 1789-1919: colonized by France 1900-1960 (CShapes 2.0), imperial power Sudan 1805-1889, France 1890-1959 (Wimmer and Min 2006); I favor no imputation.
* Burundi 1789-1915: imperial power Germany 1890-1922, Belgium 1923-1961 (Wimmer and Min 2006); I favor no imputation.
* Finland 1789-1862: part of Russia 1886-1916 (CShapes 2.0), imperial power Russia 1809-1916 (Wimmer and Min 2006), independence in 1917 (Butcher and Griffiths 2020), part of Sweden 14th century-1808.
replace country_name_regime_imputed = "Sweden" if country_name == "Finland" & year >= 1789 & year <= 1808
replace country_name_regime_imputed = "Russia" if country_name == "Finland" & year >= 1809 & year <= 1862
* Canada 1789-1840: independent since 1886 (CShapes 2.0), imperial power United Kingdom 1763-1866, colonized by Britain and France in 1700 (Ertan et al. 2016); I favor no imputation. 
* Niger 1789-1921: colony of Frange 1896-1960 (CShapes 2.0), imperial power France 1904-1959 (Wimmer and Min 2006); I favor no imputation.
* Madagascar 1789-1816: independent 1886-1896 (CShapes 2.0), imperial power France 1894-1959 (Wimmer and Min 2006), independent 1816-1895 (Butcher and Griffiths 2020), no indication of being part of another country 1789-1816 (Encyclopedia Britannica); I favor no imputation.
* Zambia 1789-1910: colonized by United Kingom 1892-1964 (Cshapes 2.0), imperial power United Kingdom 1890-1963 (Wimmer and Min 2006); I favor no imputation.
* Rwanda 1789-1915: colonized by Germany 1891-1916 (CShapes 2.0), imperial power Germany 1890-1915 (Wimmer and Min 2006); I favor no imputation.
* Estonia 1789-1917, 1940-1989: part of Russia 1886-1918, 1941-1991 (CShapes 2.0), imperial power Russia 1710-1918, 1940-1990 (Wimmer and Min 2006)
replace country_name_regime_imputed = "Russia" if country_name == "Estonia" & year >= 1789 & year <= 1917
replace country_name_regime_imputed = "Russia" if country_name == "Estonia" & year >= 1940 & year <= 1989
* Somalia 1789-1899: colonized by United Kingdom 1886-1961, Italy 1890-1941 (CShapes 2.0), imperial power Turkey 1870-1883, United Kingdom 1884-1888, mixed rule 1889-1941 (Wimmer and Min 2006), occupied by Egypt 1870-1885 (Encyclopedia Britannica); I favor no imputation.
* Guinea 1789-1899: colonized by France 1893-1958 (CShapes 2.0), imperial power France 1849-1957 (Wimmer and Min 2006); I favor no imputation.
* Cote d'Ivoire 1789-1899: colonized by France 1890-1961 (CShapes 2.0), colonized by France 1887-1959 (Wimmer and Min 2006); I favor no imputation.
* Senegal 1789-1903: colonized by France 1886-1961 (CShapes 2.0), imperial power France 1854-1959 (Wimmer and Min 2006); I favor no imputation.
* Laos 1789-1899: part of Thailand 1886-1893, colonized by France 1894-1954 (CShapes 2.0), imperial power Thailand 1778-1889, France 1890-1952 (Wimmer and Min 2006).
replace country_name_regime_imputed = "Thailand" if country_name == "Laos" & year >= 1789 & year <= 1892
* Peru 1789-1820: imperial power Spain 16th century - 1824 (Wimmer and Min 2006), independence in 1821 (Butcher and Griffiths 2020); I favor no imputation.
* Colombia 1789-1809: imperial power Spain 16th century - 1820 (Wimmer and Min 2006), independence in 1819 (Butcher and Griffiths 2020); I favor no imputation.
* Benin 1789-1899: colonized by France 1895-1961 (CShapes 2.0), imperial power 1863-1959 (Wimmer and Min 2006); I favor no imputation.
* Bolivia 1789-1824: imperial power Spain 16th century - 1823 (Wimmer and Min 2006), independence in 1825 (Butcher and Griffiths 2020); I favor no imputation.
* Libya 1912-1913, 1915-1921, 1942-1950: part of Turkey 1886-1912, colonized by Italy 1913-1943, occupied by United Kingdom 1944-1951 (CShapes 2.0), not included (Wimmer and Min 2006), independent 1816-1835 (Butcher and Griffiths 2020); I favor no imputation.
* Israel 1789-1947: part of Turkey 1886-1920, occupied by United Kingdom 1921-1948 (CShapes 2.0), imperial power Turkey 1516-1916, United Kingdom 1917-1947 (Wimmer and Min 2006).
replace country_name_regime_imputed = "Turkey" if country_name == "Israel" & year >= 1789 & year <= 1919
* Sierra Leone 1789-1899: imperial power United Kingdom 1808-1960 (Wimmer and Min 2006), colonized by United Kingdom in 1808/1896 (Ertan et al. 2016); I favor no imputation.
* Zimbabwe 1789-1899: colonized by United Kingdom 1889-1965 (CShapes 2.0), imperial power United Kingdom 1890-1964 (Wimmer and Min 2006); I favor no imputation.
* Papua New Guinea 1789-1899: colonized by United Kingdom 1886-1920 and Germany 1886-1914, Australia 1915-1975 (CShapes 2.0), imperial power United Kingdom 1883-1904, Australia 1905-1974 (Wimmer and Min 2006), colonized by United Kingdom and Germany in 1884 (Ertan et al. 2016); I favor no imputation.
* Central African Republic 1789-1919: colonized by France 1900-1961 (CShapes 2.0), imperial power France 1890-1959 (Wimmer and Min 2006), colonized by France in 1887/1903 (Ertan et al. 2016); I favor no imputation.

** Identify which observations in the dataset do not have any V-Dem information:
* I do not want to impute data for observations where V-Dem coders provide (partial) information, even if the sources above suggest that the country was part of another entity. This is because partial information suggests the remaining missings are not because the country was considered to be part of another country, but for other reasons.
egen nonmissing_values = rownonmiss(country_name year v2x_regime_owid v2elfrfair_osp_imp v2elmulpar_osp_imp v2elmulpar_osp_hoe_imp v2elmulpar_osp_leg_imp v2x_liberal_dich_row v2xlg_legcon v2lgqstexp v2lgotovst v2lginvstp v2lgoppart v2svindep ///
	v2x_polyarchy v2x_elecoff v2xel_frefair v2x_frassoc_thick v2x_suffr v2x_freexp_altinf v2x_polyarchy_codelow v2xel_frefair_codelow v2x_frassoc_thick_codelow v2x_freexp_altinf_codelow v2x_polyarchy_codehigh v2xel_frefair_codehigh v2x_frassoc_thick_codehigh v2x_freexp_altinf_codehigh ///
	v2x_libdem v2x_liberal v2xcl_rol v2x_jucon v2xlg_legcon v2x_libdem_codelow v2x_liberal_codelow v2xcl_rol_codelow v2x_jucon_codelow v2xlg_legcon_codelow v2x_libdem_codehigh v2x_liberal_codehigh v2xcl_rol_codehigh v2x_jucon_codehigh v2xlg_legcon_codehigh ///
	v2x_partipdem v2x_partip v2x_cspart v2xdd_dd v2xel_locelec v2xel_regelec v2x_partipdem_codelow v2x_partip_codelow v2x_cspart_codelow v2xel_locelec_codelow v2xel_regelec_codelow v2x_partipdem_codehigh v2x_partip_codehigh v2x_cspart_codehigh v2xel_locelec_codehigh v2xel_regelec_codehigh ///
	v2x_delibdem v2xdl_delib v2dlreason v2dlcommon v2dlcountr v2dlconslt v2dlengage v2x_delibdem_codelow v2xdl_delib_codelow v2dlreason_codelow v2dlcommon_codelow v2dlcountr_codelow v2dlconslt_codelow v2dlengage_codelow v2x_delibdem_codehigh v2xdl_delib_codehigh v2dlreason_codehigh v2dlcommon_codehigh v2dlcountr_codehigh v2dlconslt_codehigh v2dlengage_codehigh ///
	v2x_egaldem v2x_egal v2xeg_eqprotec v2xeg_eqaccess v2xeg_eqdr v2x_egaldem_codelow v2x_egal_codelow v2xeg_eqprotec_codelow v2xeg_eqaccess_codelow v2xeg_eqdr_codelow v2x_egaldem_codehigh v2x_egal_codehigh v2xeg_eqprotec_codehigh v2xeg_eqaccess_codehigh v2xeg_eqdr_codehigh), strok

generate empty_observation = 1 if nonmissing_values == 2 // The two non-missing values are country and year.


** Rename variables to prepare for merging:

rename country_name country_name_temp
rename country_name_regime_imputed country_name

rename v2x_regime_owid regime_row_owid

rename v2x_polyarchy electdem_vdem_owid
rename v2x_polyarchy_codelow electdem_vdem_owid_low
rename v2x_polyarchy_codehigh electdem_vdem_owid_high

rename v2x_elecoff electoff_vdem_owid

rename v2xel_frefair electfreefair_vdem_owid
rename v2xel_frefair_codelow electfreefair_vdem_owid_low
rename v2xel_frefair_codehigh electfreefair_vdem_owid_high

rename v2x_frassoc_thick freeassoc_vdem_owid
rename v2x_frassoc_thick_codelow freeassoc_vdem_owid_low
rename v2x_frassoc_thick_codehigh freeassoc_vdem_owid_high

rename v2x_suffr suffr_vdem_owid

rename v2x_freexp_altinf freeexpr_vdem_owid
rename v2x_freexp_altinf_codelow freeexpr_vdem_owid_low
rename v2x_freexp_altinf_codehigh freeexpr_vdem_owid_high

/* Work in progress:
rename v2x_libdem
rename v2x_libdem_codelow
rename v2x_libdem_codehigh

rename v2x_liberal
rename v2x_liberal_codelow
rename v2x_liberal_codehigh

rename v2xcl_rol
rename v2xcl_rol_codelow
rename v2xcl_rol_codehigh

rename v2x_jucon
rename v2x_jucon_codelow
rename v2x_jucon_codehigh

rename v2xlg_legcon
rename v2xlg_legcon_codelow
rename v2xlg_legcon_codehigh

rename v2x_partipdem
rename v2x_partipdem_codelow
rename v2x_partipdem_codehigh

rename v2x_partip
rename v2x_partip_codelow
rename v2x_partip_codehigh

rename v2x_cspart
rename v2x_cspart_codelow
rename v2x_cspart_codehigh

rename v2xdd_dd

rename v2xel_locelec
rename v2xel_locelec_codelow
rename v2xel_locelec_codehigh

rename v2xel_regelec
rename v2xel_regelec_codelow
rename v2xel_regelec_codehigh

rename v2x_delibdem
rename v2x_delibdem_codelow
rename v2x_delibdem_codehigh

rename v2xdl_delib
rename v2xdl_delib_codelow
rename v2xdl_delib_codehigh

rename v2dlreason
rename v2dlreason_codelow
rename v2dlreason_codehigh

rename v2dlcommon
rename v2dlcommon_codelow
rename v2dlcommon_codehigh

rename v2dlcountr
rename v2dlcountr_codelow
rename v2dlcountr_codehigh

rename v2dlconslt
rename v2dlconslt_codelow
rename v2dlconslt_codehigh

rename v2dlengage
rename v2dlengage_codelow
rename v2dlengage_codehigh

rename v2x_egaldem
rename v2x_egaldem_codelow
rename v2x_egaldem_codehigh

rename v2x_egal
rename v2x_egal_codelow
rename v2x_egal_codehigh

rename v2xeg_eqprotec
rename v2xeg_eqprotec_codelow
rename v2xeg_eqprotec_codehigh

rename v2xeg_eqaccess
rename v2xeg_eqaccess_codelow
rename v2xeg_eqaccess_codehigh

rename v2xeg_eqdr
rename v2xeg_eqdr_codelow
rename v2xeg_eqdr_codehigh
*/                     
                    

** Merge with V-Dem dataset again, this time on imputing countries:

* I do not merge with the 'merge, update', as in that case some observations will have different non-missing values between the non-imputed and the imputed variables (due to partial V-Dem coverage). I therefore have to use a more manual approach.

sort country_name year
merge m:1 country_name year using "Political regimes/vdem_temp.dta"
drop if _merge == 2
drop _merge

erase "Political regimes/vdem_temp.dta"

rename country_name regime_imputed_country_vdem_owid
rename country_name_temp country_name

** Create variable identifying whether regime data is imputed:
generate regime_imputed_vdem_owid = ""
replace regime_imputed_vdem_owid = "no" if regime_imputed_country_vdem_owid == "" | empty_observation != 1
replace regime_imputed_vdem_owid = "yes" if regime_imputed_country_vdem_owid != "" & empty_observation == 1
order regime_imputed_vdem_owid, before(regime_imputed_country_vdem_owid)

label variable regime_imputed_country_vdem_owid "Name of the country from which V-Dem regime information was imputed"
label variable regime_imputed_vdem_owid "V-Dem regime information imputed from another country"

** Update variable identifying whether observation includes V-Dem information:
replace vdem_obs = 1 if regime_imputed_vdem_owid == "yes"

** Create variable identifying whether country includes V-Dem information:
bysort country_name: egen vdem_country = max(vdem_obs)
label variable vdem_country "Country includes information from V-Dem"

** Add imputed values for variables:
replace regime_row_owid = v2x_regime_owid if regime_imputed_vdem_owid== "yes"

replace electdem_vdem_owid = v2x_polyarchy if regime_imputed_vdem_owid== "yes"

replace electoff_vdem_owid = v2x_elecoff if regime_imputed_vdem_owid== "yes"
replace electfreefair_vdem_owid = v2xel_frefair if regime_imputed_vdem_owid== "yes"
replace freeassoc_vdem_owid = v2x_frassoc_thick if regime_imputed_vdem_owid== "yes"
replace suffr_vdem_owid = v2x_suffr if regime_imputed_vdem_owid== "yes"
replace freeexpr_vdem_owid = v2x_freexp_altinf if regime_imputed_vdem_owid== "yes"

replace electdem_vdem_owid_low = v2x_polyarchy_codelow if regime_imputed_vdem_owid== "yes"
replace electfreefair_vdem_owid_low = v2xel_frefair_codelow if regime_imputed_vdem_owid== "yes"
replace freeassoc_vdem_owid_low = v2x_frassoc_thick_codelow if regime_imputed_vdem_owid== "yes"
replace freeexpr_vdem_owid_low = v2x_freexp_altinf_codelow if regime_imputed_vdem_owid== "yes"

replace electdem_vdem_owid_high = v2x_polyarchy_codehigh if regime_imputed_vdem_owid== "yes"
replace electfreefair_vdem_owid_high = v2xel_frefair_codehigh if regime_imputed_vdem_owid== "yes"
replace freeassoc_vdem_owid_high = v2x_frassoc_thick_codehigh if regime_imputed_vdem_owid== "yes"
replace freeexpr_vdem_owid_high = v2x_freexp_altinf_codehigh if regime_imputed_vdem_owid== "yes"

sort country_name year
keep country_name year vdem_country vdem_obs regime_row_owid electdem_vdem_owid electdem_vdem_owid_low electdem_vdem_owid_high electfreefair_vdem_owid electfreefair_vdem_owid_low electfreefair_vdem_owid_high suffr_vdem_owid electoff_vdem_owid freeexpr_vdem_owid freeexpr_vdem_owid_low freeexpr_vdem_owid_high freeassoc_vdem_owid freeassoc_vdem_owid_low freeassoc_vdem_owid_high regime_imputed_vdem_owid regime_imputed_country_vdem_owid
order country_name year vdem_country vdem_obs regime_row_owid electdem_vdem_owid electdem_vdem_owid_low electdem_vdem_owid_high electfreefair_vdem_owid electfreefair_vdem_owid_low electfreefair_vdem_owid_high suffr_vdem_owid electoff_vdem_owid freeexpr_vdem_owid freeexpr_vdem_owid_low freeexpr_vdem_owid_high freeassoc_vdem_owid freeassoc_vdem_owid_low freeassoc_vdem_owid_high regime_imputed_vdem_owid regime_imputed_country_vdem_owid

** Format variables:

label variable electdem_vdem_owid "Electoral democracy (V-Dem, OWID)"
label variable electdem_vdem_owid_low "Electoral democracy (lower bound, V-Dem, OWID)"
label variable electdem_vdem_owid_high "Electoral democracy (upper bound, V-Dem, OWID)"

label variable electfreefair_vdem_owid "Free and fair elections (V-Dem, OWID)"
label variable electfreefair_vdem_owid_low "Free and fair elections (lower bound, V-Dem, OWID)"
label variable electfreefair_vdem_owid_high "Free and fair elections (upper bound, V-Dem, OWID)"

label variable suffr_vdem_owid "Share of the population with suffrage (V-Dem, OWID)"
label variable electoff_vdem_owid "Elected officials (V-Dem, OWID)"

label variable freeexpr_vdem_owid "Freedom of expression and alternative sources of information (V-Dem, OWID)"
label variable freeexpr_vdem_owid_low "Freedom of expression and alternative sources of information (lower bound, V-Dem, OWID)"
label variable freeexpr_vdem_owid_high "Freedom of expression and alternative sources of information (upper bound, V-Dem, OWID)"

label variable freeassoc_vdem_owid "Freedom of association (V-Dem, OWID)"
label variable freeassoc_vdem_owid_low "Freedom of association (lower bound, V-Dem, OWID)"
label variable freeassoc_vdem_owid_high "Freedom of association (upper bound, V-Dem, OWID)"



*** Create age variables for electoral democracies and liberal democracies:

** Create numeric country identifier:
encode country_name, generate(country_number)

** Declare dataset to be time-series data:
tsset country_number year

** Create variable for age of electoral democracies:
generate electdem_age_row_owid = .
replace electdem_age_row_owid = 0 if regime_row_owid == 0 | regime_row_owid == 1
replace electdem_age_row_owid = 1 if (l.regime_row_owid == 0 | l.regime_row_owid == 1) & (regime_row_owid == 2 | regime_row_owid == 3)
replace electdem_age_row_owid = 1 if l.regime_row_owid == . & (regime_row_owid == 2 | regime_row_owid == 3) // Assume that when previous information is missing, the country was not an electoral democracy.
replace electdem_age_row_owid = l.electdem_age_row_owid + 1 if electdem_age_row_owid == . & (regime_row_owid == 2 | regime_row_owid == 3)
label variable electdem_age_row_owid "Electoral democracy age (Regimes of the World, OWID)"
order electdem_age_row_owid, after(regime_row_owid)

** Create variable for age of liberal democracies:
generate libdem_age_row_owid = .
replace libdem_age_row_owid = 0 if regime_row_owid == 0 | regime_row_owid == 1 | regime_row_owid == 2
replace libdem_age_row_owid = 1 if (l.regime_row_owid == 0 | l.regime_row_owid == 1 | l.regime_row_owid == 2) & regime_row_owid == 3
replace libdem_age_row_owid = 1 if l.regime_row_owid == . & regime_row_owid == 3 // Assume that when previous information is missing, the country was not a liberal democracy.
replace libdem_age_row_owid = l.libdem_age_row_owid + 1 if libdem_age_row_owid == . & regime_row_owid == 3
label variable libdem_age_row_owid "Liberal democracy age (Regimes of the World, OWID)"
order libdem_age_row_owid, after(electdem_age_row_owid)

drop country_number

** Create variable for experience with electoral democracy:
generate electdem_row_owid = .
replace electdem_row_owid = 0 if regime_row_owid == 0 | regime_row_owid == 1
replace electdem_row_owid = 1 if regime_row_owid == 2 | regime_row_owid == 3

generate electdem_exp_row_owid = .
bysort country_name: replace electdem_exp_row_owid = sum(electdem_row_owid) if vdem_country == 1
drop electdem_row_owid

label variable electdem_exp_row_owid "Experience with electoral democracy (Regimes of the World, OWID)"

** Create variable for experience with liberal democracy:
generate libdem_row_owid = .
replace libdem_row_owid = 0 if regime_row_owid == 0 | regime_row_owid == 1 | regime_row_owid == 2
replace libdem_row_owid = 1 if regime_row_owid == 3

generate libdem_exp_row_owid = .
bysort country_name: replace libdem_exp_row_owid = sum(libdem_row_owid) if vdem_country == 1
drop libdem_row_owid

label variable libdem_exp_row_owid "Experience with liberal democracy (Regimes of the World, OWID)"


** Create variable for age group of electoral demcoracies:
generate electdem_age_group_row_owid = .
replace electdem_age_group_row_owid = 0 if regime_row_owid == 0
replace electdem_age_group_row_owid = 1 if regime_row_owid == 1
replace electdem_age_group_row_owid = 2 if electdem_age_row_owid > 0 & electdem_age_row_owid <= 18
replace electdem_age_group_row_owid = 3 if electdem_age_row_owid > 18 & electdem_age_row_owid <= 30
replace electdem_age_group_row_owid = 4 if electdem_age_row_owid > 30 & electdem_age_row_owid <= 60
replace electdem_age_group_row_owid = 5 if electdem_age_row_owid > 60 & electdem_age_row_owid <= 90
replace electdem_age_group_row_owid = 6 if electdem_age_row_owid > 90 & electdem_age_row_owid < .
label variable electdem_age_group_row_owid "Electoral democracy age group (Regimes of the World, OWID)"
label define electdem_age_group_row_owid 0 "closed autocracy" 1"electoral autocracy" 2 "1-18 years" 3 "19-30 years" 4 "31-60 years" 5 "61-90 years" 6 "91+ years"
label values electdem_age_group_row_owid electdem_age_group_row_owid
order electdem_age_group_row_owid, after(electdem_age_row_owid)

** Create variable for age group of liberal democracies:
generate libdem_age_group_row_owid = .
replace libdem_age_group_row_owid = 0 if regime_row_owid == 0
replace libdem_age_group_row_owid = 1 if regime_row_owid == 1
replace libdem_age_group_row_owid = 2 if regime_row_owid == 2
replace libdem_age_group_row_owid = 3 if libdem_age_row_owid > 0 & libdem_age_row_owid <= 18
replace libdem_age_group_row_owid = 4 if libdem_age_row_owid > 18 & libdem_age_row_owid <= 30
replace libdem_age_group_row_owid = 5 if libdem_age_row_owid > 30 & libdem_age_row_owid <= 60
replace libdem_age_group_row_owid = 6 if libdem_age_row_owid > 60 & libdem_age_row_owid <= 90
replace libdem_age_group_row_owid = 7 if libdem_age_row_owid > 90 & libdem_age_row_owid < .
label variable libdem_age_group_row_owid "Liberal democracy age group (Regimes of the World, OWID)"
label define libdem_age_group_row_owid 0 "closed autocracy" 1 "electoral autocracy" 2 "electoral democracy" 3 "1-18 years" 4 "19-30 years" 5 "31-60 years" 6 "61-90 years" 7 "91+ years"
label values libdem_age_group_row_owid libdem_age_group_row_owid
order libdem_age_group_row_owid, after(libdem_age_row_owid)

** Add labels for ages of electoral and liberal democracies to optimize use in the OWID grapher:
tostring electdem_age_row_owid, replace
replace electdem_age_row_owid = "no data" if electdem_age_row_owid == "."
replace electdem_age_row_owid = "closed autocracy" if regime_row_owid == 0
replace electdem_age_row_owid = "electoral autocracy" if regime_row_owid == 1

tostring libdem_age_row_owid, replace
replace libdem_age_row_owid = "no data" if libdem_age_row_owid == "."
replace libdem_age_row_owid = "closed autocracy" if regime_row_owid == 0
replace libdem_age_row_owid = "electoral autocracy" if regime_row_owid == 1
replace libdem_age_row_owid = "electoral democracy" if regime_row_owid == 2

save "Political regimes/master_temp.dta", replace



*** Prepare BMR data:

** Import BMR data again:
use "Boix, Miller, Rosato 2022 regimes data/democracy-v4.0.dta", replace


** Merge with harmonized country names:
merge m:1 country using "Boix, Miller, Rosato 2022 regimes data/bmr_countries.dta"
drop _merge
erase "Boix, Miller, Rosato 2022 regimes data/bmr_countries.dta"


** Identify duplicate observations:
sort country_name year
duplicates tag country_name year, generate(duplicate)
list if duplicate == 1 // duplicates are of Germany/West Germany in 1945 and 1990, and Yugoslavia/Serbia in 1991 and 2006.
drop if ccode == 260 & year == 1945
drop if ccode == 260 & year == 1990
drop if ccode == 345 & year == 1991
drop if ccode == 347 & year == 2006


** Keep variables of interest:
keep country_name year democracy_omitteddata democracy_femalesuffrage // I use 'democracy_omitteddata' instead of 'democracy' because the former codes times of foreign occupation and civil war as missing values instead of continuations of the previous regime type.

order country_name year
sort country_name year

save "Boix, Miller, Rosato 2022 regimes data/bmr.dta", replace



*** Merge BMR with master dataset:

use "Political regimes/master_temp.dta", clear

merge 1:1 country_name year using "Boix, Miller, Rosato 2022 regimes data/bmr.dta"
erase "Political regimes/master_temp.dta"
tab country_name if _merge == 2 // No unmatched countries in BMR (as it should be, as I created a comprehensive list of countries above).

generate bmr_obs = 1 if _merge == 3
replace bmr_obs = 0 if _merge == 1

label variable bmr_obs "Observation includes information from Boix et al. (2013)"

generate regime_bmr_owid = democracy_omitteddata

order bmr_obs, before(regime_bmr_owid)

generate regime_womsuffr_bmr_owid = democracy_femalesuffrage
replace regime_womsuffr_bmr_owid = . if regime_bmr_owid == . // I do this to code times of foreign occupation and civil war as missing values instead of continuations of the previous regime type.

label variable regime_bmr_owid "Regime (BMR, OWID)"
label variable regime_womsuffr_bmr_owid "Regime (with women's suffrage, BMR, OWID)"

generate regime_imputed_bmr_owid = "no" if _merge == 3
drop _merge democracy_omitteddata democracy_femalesuffrage

label variable regime_imputed_bmr_owid "BMR regime information imputed from another country"

** Expand BMR data by imputing data from historical countries:

generate regime_imputed_country_bmr_owid = ""
replace regime_imputed_country_bmr_owid = "Great Colombia" if country_name == "Colombia" & year >= 1821 & year <= 1830
replace regime_imputed_country_bmr_owid = "Central American Union" if country_name == "Costa Rica" & year >= 1824 & year <= 1838
replace regime_imputed_country_bmr_owid = "Czechoslovakia" if country_name == "Czechia" & year >= 1918 & year <= 1992
replace regime_imputed_country_bmr_owid = "Great Colombia" if country_name == "Ecuador" & year >= 1821 & year <= 1830
replace regime_imputed_country_bmr_owid = "Central American Union" if country_name == "El Salvador" & year >= 1824 & year <= 1838
replace regime_imputed_country_bmr_owid = "Central American Union" if country_name == "Guatemala" & year >= 1824 & year <= 1838
replace regime_imputed_country_bmr_owid = "Central American Union" if country_name == "Honduras" & year >= 1824 & year <= 1838
replace regime_imputed_country_bmr_owid = "Central American Union" if country_name == "Nicaragua" & year >= 1824 & year <= 1838
replace regime_imputed_country_bmr_owid = "Korea" if country_name == "North Korea" & year >= 1800 & year <= 1910
replace regime_imputed_country_bmr_owid = "Great Colombia" if country_name == "Panama" & year >= 1821 & year <= 1830
replace regime_imputed_country_bmr_owid = "Czechoslovakia" if country_name == "Slovakia" & year >= 1918 & year <= 1992
replace regime_imputed_country_bmr_owid = "Korea" if country_name == "South Korea" & year >= 1800 & year <= 1910
replace regime_imputed_country_bmr_owid = "Great Colombia" if country_name == "Venezuela" & year >= 1821 & year <= 1830

label variable regime_imputed_country_bmr_owid "Name of the country from which BMR regime information was imputed"


** Merge again, this time on imputed countries:
rename country_name country_name_temp
rename regime_imputed_country_bmr_owid country_name
merge m:1 country_name year using "Boix, Miller, Rosato 2022 regimes data/bmr.dta"
drop if _merge == 2

rename country_name regime_imputed_country_bmr_owid
rename country_name_temp country_name
sort country_name year

replace regime_imputed_bmr_owid = "yes" if _merge == 3

** Update observations including information from BMR:
replace bmr_obs = 1 if regime_imputed_bmr_owid == "yes"

** Create variable identifying whether country includes information from BMR:
bysort country_name: egen bmr_country = max(bmr_obs)
label variable bmr_country "Country includes information from Boix et al. (2013)
order bmr_country, before(bmr_obs)

drop _merge

list country_name year if regime_bmr_owid != . & democracy_omitteddata != . // There is sometimes BMR information for the separate countries at the very end of the historical country; in that case, I do not impute.
replace regime_bmr_owid = democracy_omitteddata if regime_bmr_owid == .
replace regime_womsuffr_bmr_owid = democracy_femalesuffrage if regime_womsuffr_bmr_owid == . & democracy_omitteddata != .
drop democracy_omitteddata democracy_femalesuffrage



*** Create variables for age of BMR democracies:

** Create numeric country identifier:
encode country_name, generate(country_number)

** Declare dataset to be time-series data:
tsset country_number year

** Create variable for age of electoral democracies:
generate electdem_age_bmr_owid = .
replace electdem_age_bmr_owid = 0 if regime_bmr_owid == 0
replace electdem_age_bmr_owid = 1 if l.regime_bmr_owid == 0 & regime_bmr_owid == 1
replace electdem_age_bmr_owid = 1 if l.regime_bmr_owid == . & regime_bmr_owid == 1 // Assume that when previous information is missing, the country was not an electoral democracy.
replace electdem_age_bmr_owid = l.electdem_age_bmr_owid + 1 if electdem_age_bmr_owid == . & regime_bmr_owid == 1
label variable electdem_age_bmr_owid "Electoral democracy age (BMR, OWID)"
order electdem_age_bmr_owid, after(regime_womsuffr_bmr_owid)

drop country_number

** Create variable for experience with electoral democracy:
generate electdem_bmr_owid = .
replace electdem_bmr_owid = 0 if regime_bmr_owid == 0
replace electdem_bmr_owid = 1 if regime_bmr_owid == 1

generate electdem_exp_bmr_owid = .
bysort country_name: replace electdem_exp_bmr_owid = sum(electdem_bmr_owid) if bmr_country == 1
drop electdem_bmr_owid

label variable electdem_exp_bmr_owid "Experience with electoral democracy (BMR, OWID)"


** Create variable for age group of electoral democracies:
generate electdem_age_group_bmr_owid = .
replace electdem_age_group_bmr_owid = 0 if regime_bmr_owid == 0
replace electdem_age_group_bmr_owid = 1 if electdem_age_bmr_owid > 0 & electdem_age_bmr_owid <= 18
replace electdem_age_group_bmr_owid = 2 if electdem_age_bmr_owid > 18 & electdem_age_bmr_owid <= 30
replace electdem_age_group_bmr_owid = 3 if electdem_age_bmr_owid > 30 & electdem_age_bmr_owid <= 60
replace electdem_age_group_bmr_owid = 4 if electdem_age_bmr_owid > 60 & electdem_age_bmr_owid <= 90
replace electdem_age_group_bmr_owid = 5 if electdem_age_bmr_owid > 90 & electdem_age_bmr_owid < .
label variable electdem_age_group_bmr_owid "Electoral democracy age group (BMR, OWID)"
label define electdem_age_group_bmr_owid 0 "non-democracy" 1 "1-18 years" 2 "19-30 years" 3 "31-60 years" 4 "61-90 years" 5 "91+ years"
label values electdem_age_group_bmr_owid electdem_age_group_bmr_owid

** Add labels for ages of BMR democracies to optimize use in the OWID grapher:
tostring electdem_age_bmr_owid, replace
replace electdem_age_bmr_owid = "no data" if electdem_age_bmr_owid == "."
replace electdem_age_bmr_owid = "non-democracy" if regime_bmr_owid == 0

order electdem_age_group_bmr_owid, after(electdem_age_bmr_owid)
order regime_imputed_bmr_owid regime_imputed_country_bmr_owid, after(electdem_age_group_bmr_owid)



*** Create dataset with regime information per country and year:

preserve

** Keep only countries with at least one year of some regime information:
keep if vdem_country == 1 | bmr_country == 1

save "Political regimes/regimes_owid.dta", replace
export delimited "Political regimes/regimes_owid.csv", replace nolabel

restore



*** Create dataset with number per year of people living in different regimes:

preserve

** Add population data:
merge 1:1 country_name year using "Our World in Data/population_owid.dta"

** Take a look at unmerged cases:
drop if year < 1800 | year > 2020
tab _merge // no unmatched observations in using dataset between 1789 and 2020.
drop _merge

** Recode Regimes of the World indicator such that it includes a category for when population data is available, but regime data is missing:
replace regime_row_owid = 4 if regime_row_owid == . & population_owid != .
label values regime_row_owid v2x_regime_owid_label
label define v2x_regime_owid_label 4 "no regime data", add
drop if population_owid == .
tab regime_row_owid, m

** Reduce the infromation to regime per year:
collapse (sum) population_owid, by(year regime_row_owid)

reshape wide population_owid, i(year) j(regime_row_owid)

generate entity_name = "World"
order entity_name, before(year)

rename population_owid0 population_closed_aut
rename population_owid1 population_electoral_aut
rename population_owid2 population_electoral_dem
rename population_owid3 population_liberal_dem
rename population_owid4 population_missing_data

recode population_electoral_dem (. = 0)
recode population_liberal_dem (. = 0)

label variable population_closed_aut "Number of people living in closed autocracies"
label variable population_electoral_aut "Number of people living in electoral autocracies"
label variable population_electoral_dem "Number of people living in electoral democracies"
label variable population_liberal_dem "Number of people living in liberal democracies"
label variable population_missing_data "Number of people living in countries without regime data"

save "Political regimes/regimes_population_owid.dta", replace
export delimited "Political regimes/regimes_population_owid.csv", replace

restore



*** Create dataset with number per year of electoral and liberal democracies in different age groups:

preserve

tabulate electdem_age_group_row_owid, generate(electdem_age_group_row_owid)
tabulate libdem_age_group_row_owid, generate(libdem_age_group_row_owid)
tabulate electdem_age_group_bmr_owid, generate(electdem_age_group_bmr_owid)

collapse (sum) electdem_age_group_row_owid* libdem_age_group_row_owid* electdem_age_group_bmr_owid*, by(year)
drop electdem_age_group_row_owid libdem_age_group_row_owid electdem_age_group_bmr_owid

generate entity_name = "World"
order entity_name, before(year)

rename electdem_age_group_row_owid1 number_closedaut_row_owid
rename electdem_age_group_row_owid2 number_electaut_row_owid
rename electdem_age_group_row_owid3 number_electdem_18_row_owid
rename electdem_age_group_row_owid4 number_electdem_30_row_owid
rename electdem_age_group_row_owid5 number_electdem_60_row_owid
rename electdem_age_group_row_owid6 number_electdem_90_row_owid
rename electdem_age_group_row_owid7 number_electdem_91plus_row_owid

drop libdem_age_group_row_owid1 libdem_age_group_row_owid2
rename libdem_age_group_row_owid3 number_electdem_row_owid
rename libdem_age_group_row_owid4 number_libdem_18_row_owid
rename libdem_age_group_row_owid5 number_libdem_30_row_owid
rename libdem_age_group_row_owid6 number_libdem_60_row_owid
rename libdem_age_group_row_owid7 number_libdem_90_row_owid
rename libdem_age_group_row_owid8 number_libdem_91plus_row_owid

label variable number_closedaut_row_owid "Number of closed autocracies (RoW, OWID)"
label variable number_electaut_row_owid "Number of electoral autocracies (RoW, OWID)"
label variable number_electdem_18_row_owid "Number of electoral democracies aged 1-18 years (RoW, OWID)"
label variable number_electdem_30_row_owid "Number of electoral democracies aged 19-30 years (RoW, OWID)"
label variable number_electdem_60_row_owid "Number of electoral democracies aged 31-60 years (RoW, OWID)"
label variable number_electdem_90_row_owid "Number of electoral democracies aged 61-90 years (RoW, OWID)"
label variable number_electdem_91plus_row_owid "Number of electoral democracies aged 91 years or older (RoW, OWID)"

label variable number_electdem_row_owid "Number of electoral democracies (RoW, OWID)"
label variable number_libdem_18_row_owid "Number of liberal democracies aged 1-18 years (RoW, OWID)"
label variable number_libdem_30_row_owid "Number of liberal democracies aged 19-30 years (RoW, OWID)"
label variable number_libdem_60_row_owid "Number of liberal democracies aged 31-60 years (RoW, OWID)"
label variable number_libdem_90_row_owid "Number of liberal democracies aged 61-90 years (RoW, OWID)"
label variable number_libdem_91plus_row_owid "Number of liberal democracies aged 91 years or older (RoW, OWID)"

rename electdem_age_group_bmr_owid1 number_nondem_bmr_owid
rename electdem_age_group_bmr_owid2 number_electdem_18_bmr_owid
rename electdem_age_group_bmr_owid3 number_electdem_30_bmr_owid
rename electdem_age_group_bmr_owid4 number_electdem_60_bmr_owid
rename electdem_age_group_bmr_owid5 number_electdem_90_bmr_owid
rename electdem_age_group_bmr_owid6 number_electdem_91plus_bmr_owid

label variable number_nondem_bmr_owid "Number of non-democracies (Boix et al. 2013, OWID)"
label variable number_electdem_18_bmr_owid "Number of electoral democracies aged 1-18 years (Boix et al. 2013, OWID)"
label variable number_electdem_30_bmr_owid "Number of electoral democracies aged 19-30 years (Boix et al. 2013, OWID)"
label variable number_electdem_60_bmr_owid "Number of electoral democracies aged 31-60 years (Boix et al. 2013, OWID)"
label variable number_electdem_90_bmr_owid "Number of electoral democracies aged 61-90 years (Boix et al. 2013, OWID)"
label variable number_electdem_91plus_bmr_owid "Number of electoral democracies aged 91 years or older (Boix et al. 2013, OWID)"

save "Political regimes/regimes_number_owid.dta", replace
export delimited "Political regimes/regimes_number_owid.csv", replace

restore



exit
