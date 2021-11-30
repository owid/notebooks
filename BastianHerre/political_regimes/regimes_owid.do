*****  Stata do-file to create the 'Regimes of the World' data used in several posts on Our World in Data:
*****  Post 1: "The ‘Regimes of the World’ data: how do researchers identify which countries are democracies?"
*****  Post 2: "200 years ago, everyone lacked democratic rights. Now, billions of people have them."
*****  Author: Bastian Herre
*****  November 29, 2021


version 14

clear all
set more off
set varabbrev off

* Set your working directory here:
cd "/Users/bastianherre/Dropbox/Data/"
global project "/Users/bastianherre/Dropbox/Data/"


*** Create master-dataset in which all countries in either V-Dem or OWID population datasets are included, and years included in V-Dem (1789-2020):

* Download V-Dem dataset from https://www.v-dem.net/en/data/data/v-dem-dataset-v111/ and move it into the folder "Coppedge et al. 2021 V-Dem"
* Import V-Dem dataset:
use "Coppedge et al. 2021 V-Dem/V-Dem-CY-Full+Others-v11.1.dta", clear

* Harmonize V-Dem and OWID country names:
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

* Download OWID population data from https://ourworldindata.org/grapher/population and move it into the folder "Our World in Data"
* Merge OWID population into V-Dem data:
sort country_name year
merge 1:1 country_name year using "Our World in Data/population_owid.dta"

* Take a look at unmerged cases:
tab country_name if _merge == 1 & year > 1799 // Unmerged observations in master dataset are from before 1800, are historical countries (e.g. Orange Free State and German Democratic Republic), as well as Kosovo, Palestine/Gaza, Palestine/West Bank, Somaliland, and Zanzibar.
drop _merge

* Only keep one observation per country:
keep country_name
sort country_name
duplicates drop
isid country_name

* Expand to country-year dataset with years 1789 to 2020:
expand 232
bysort country_name: generate year = 1788+_n
label variable year "Year"
tab year

save "Political regimes/master.dta", replace



*** Prepare V-Dem data:

* Import V-Dem dataset again:
use "Coppedge et al. 2021 V-Dem/V-Dem-CY-Full+Others-v11.1.dta", clear

* Keep variables of interest:
keep country_name country_text_id year v2x_regime v2x_polyarchy v2x_elecreg v2xlg_elecreg v2xex_elecreg v2elmulpar_osp v2elfrfair_osp v2x_liberal v2xlg_legcon v2exnamhos v2exnamhog v2ex_hosw v2expathhg v2expathhs v2exaphos v2exaphogp v2cltrnslw_osp v2clacjstm_osp v2clacjstw_osp v2eltype_0 v2eltype_1 v2eltype_4 v2eltype_5 v2eltype_6 v2eltype_7 v2ex_legconhos v2ex_legconhog v2exhoshog v2ex_hogw v2svindep v2lgqstexp v2lgotovst v2lginvstp v2lgoppart

* Drop superfluous observations:
drop if country_name == "Italy" & year == 1861
replace country_name = "Italy" if country_name == "Piedmont-Sardinia" & year == 1861 // Piedmont-Sardinia became Italy during 1861.

* Recode errors in relative power of head of state and head of government variable in line with feedback by Marcus that head of government Mugabe was more powerful than head of state Banana.
replace v2ex_hosw = 0 if country_name == "Zimbabwe" & year >= 1980 & year <= 1986
replace v2ex_hogw = 1 if country_name == "Zimbabwe" & year >= 1980 & year <= 1986

* Recode error in head of state and head of government variables:
list v2exnamhos v2exnamhog v2exhoshog v2ex_hosw v2ex_hogw v2eltype* if country_name == "Russia" & year == 1917
replace v2ex_hosw = 1 if country_name == "Russia" & year == 1917
replace v2ex_hogw = 0 if country_name == "Russia" & year == 1917
* Note: only a head of state (Lenin) listed, so (absent) head of government incorrectly coded as more powerful than head of state; Lenin not appointed by a legislature, but 

list year v2exnamhos v2exnamhog v2exhoshog v2ex_hosw v2ex_hogw v2exaphogp if country_name == "Haiti" & year > 1990 & year < 1995
replace v2exnamhos = "Raoul Cédras" if country_name == "Haiti" & year >= 1991 & year <= 1993
replace v2ex_hosw = 1 if country_name == "Haiti" & year >= 1991 & year <= 1993
replace v2ex_hogw = 0 if country_name == "Haiti" & year >= 1991 & year <= 1993
replace v2exaphogp = 0 if country_name == "Haiti" & year >= 1991 & year <= 1993
* Note: Goemans et al.'s (2009) Archigos dataset, rulers.org, and worldstatesmen.org identify non-elected General Raoul Cédras as the de-facto leader of Haiti from 1991 until 1994.


** Create expanded Regimes of the World indicator:

* Create numeric country identifier:
encode country_name, generate(country_number)

* Declare dataset to be time-series data:
tsset country_number year

* Create indicator for multi-party elections with imputed values between election-years:
generate v2elmulpar_osp_imp = v2elmulpar_osp
replace v2elmulpar_osp_imp = l.v2elmulpar_osp_imp if v2elmulpar_osp_imp == . & v2x_elecreg == 1

* Create indicator for free and fair elections with imputed values between election-years:
generate v2elfrfair_osp_imp = v2elfrfair_osp
replace v2elfrfair_osp_imp = l.v2elfrfair_osp_imp if v2elfrfair_osp_imp == . & v2x_elecreg == 1

* Create indicators for multi-party executive elections, and multi-party executive elections with imputed values between election-years:
generate v2elmulpar_osp_ex = v2elmulpar_osp if v2eltype_6 == 1 | v2eltype_7 == 1
generate v2elmulpar_osp_ex_imp = v2elmulpar_osp_ex
replace v2elmulpar_osp_ex_imp = l.v2elmulpar_osp_ex_imp if v2elmulpar_osp_ex_imp == . & v2xex_elecreg == 1

* Create indicators for multi-party legislative elections, and multi-party legislative elections with imputed values between election-years:
generate v2elmulpar_osp_leg = v2elmulpar_osp if v2eltype_0 == 1 | v2eltype_1 == 1 | v2eltype_4 == 1 | v2eltype_5 == 1 // v2eltype_4 and v2eltype_5 excluded in Marcus Tannenberg and Anna Lührmann's Stata code; included here to align coding with code in V-Dem's data pipeline.
generate v2elmulpar_osp_leg_imp = v2elmulpar_osp_leg
replace v2elmulpar_osp_leg_imp = l.v2elmulpar_osp_leg_imp if v2elmulpar_osp_leg_imp == . & v2xlg_elecreg == 1

* Create indicator for multi-party head of state elections with imputed values between election-years:
generate v2elmulpar_osp_hos_imp = 0 if v2x_elecreg != .
* Note: Marcus Tannenberg does not know why electoral regime used as filter instead of relative power of heads of state and government as filter, as above; Anna Lührmann wrote this code. Using electoral regime as filter for this and all following variables yields identical coding.
replace v2elmulpar_osp_hos_imp = 1 if v2expathhs == 7 & v2xex_elecreg == 1 & v2elmulpar_osp_ex_imp > 1 & v2elmulpar_osp_ex_imp != . // If head of state is directly elected, elections for executive must be multi-party.
replace v2elmulpar_osp_hos_imp = 1 if v2expathhs == 6 & v2xlg_elecreg == 1 & v2elmulpar_osp_leg_imp > 1 & v2elmulpar_osp_leg_imp !=. // If head of state is appointed by legislature, elections for legislature must be multi-party.
* replace v2elmulpar_osp_hos_imp = 1 if v2ex_legconhos == 1 & v2xlg_elecreg == 1 & v2elmulpar_osp_ex_imp > 1 & v2elmulpar_osp_ex_imp != . // If head of state is appointed otherwise, but approval by the legislature is necessary, elections for legislature must be multi-party.
* Why is v2elmulpar_osp_ex_imp and not v2elmulpar_osp_leg_imp used, if this is about legislative elections? This seems to be an error, which is why I use the following code instead:
replace v2elmulpar_osp_hos_imp = 1 if v2ex_legconhos == 1 & v2xlg_elecreg == 1 & v2elmulpar_osp_leg_imp > 1 & v2elmulpar_osp_leg_imp != . // If head of state is appointed otherwise, but approval by the legislature is necessary, elections for legislature must be multi-party.

* Create indicator for multi-party head of government elections with imputed values between election-years:
generate v2elmulpar_osp_hog_imp = 0 if v2x_elecreg != .
replace v2elmulpar_osp_hog_imp = 1 if v2expathhg == 8 & v2xex_elecreg == 1 & v2elmulpar_osp_ex_imp > 1 & v2elmulpar_osp_ex_imp != . // If head of government is directly elected, elections for executive must be multi-party.
replace v2elmulpar_osp_hog_imp = 1 if v2expathhg == 7 & v2xlg_elecreg == 1 & v2elmulpar_osp_leg_imp > 1 & v2elmulpar_osp_leg_imp != . // If head of government is appointed by legislature, elections for legislature must be multi-party.
replace v2elmulpar_osp_hog_imp = 1 if v2expathhg == 6 & v2elmulpar_osp_hos_imp == 1 // If head of government is appointed by the head of state, elections for the head of state must be multi-party.
* replace v2elmulpar_osp_hog_imp = 1 if v2exaphogp == 1 & v2elmulpar_osp_imp != . & v2elmulpar_osp_leg_imp > 1 & v2elmulpar_osp_leg_imp != . // If head of government is appointed otherwise, but approval by the legislature is necessary, elections for legislature must be multi-party.
* Note: Marcus Tannenberg does not know why v2elmulpar_osp_imp used as filter here, and not v2xlg_elecreg; Anna Lührmann may have come up with this fix, as the only five observations coded differently - Cambodia 1973-1974 and Haiti 1992-1994 - in his opinion should be closed autocracies due to no elections being held due to civil war and military rule, respectively.
* But: as described above, Haiti's chief executive is coded incorrectly until 1994, and correcting for that turns the country into a closed autocracy from 1991 to 1993. In 1994 the previously elected president returns, and it is plausible to presume he and his head of government are accountable to the legislature again, making the country an electoral autocracy. And just because a civil war in Cambodia goes on, that does not mean that its chief executive is not accountable to a legislature anymore. I therefore do not use the fix here.
* Yet: I use v2ex_legconhog instead of v2exaphogp to use the variable analogous to v2ex_legconhos above:
replace v2elmulpar_osp_hog_imp = 1 if v2ex_legconhog == 1 & v2xlg_elecreg == 1 & v2elmulpar_osp_leg_imp > 1 & v2elmulpar_osp_leg_imp != . // If head of government is appointed otherwise, but approval by the legislature is necessary, elections for legislature must be multi-party.

* Create indicator for multi-party executive and legislative elections with imputed values between election-years:
generate v2elmulpar_osp_exleg_imp = 0 if v2ex_hosw != .
replace v2elmulpar_osp_exleg_imp = 1 if v2xlg_elecreg == 1 & v2xex_elecreg == 1 & v2elmulpar_osp_ex_imp > 1 & v2elmulpar_osp_ex_imp != . & v2elmulpar_osp_leg_imp > 1 & v2elmulpar_osp_leg_imp != .

* Create indicator for multi-party head of executive elections with imputed values between election-years:
generate v2elmulpar_osp_hoe_imp = 0 if v2ex_hosw != .
replace v2elmulpar_osp_hoe_imp = v2elmulpar_osp_hos_imp if v2ex_hosw <= 1 & v2ex_hosw > 0.5 // If head of state is more powerful than head of government, head of state is the head of the executive.
replace v2elmulpar_osp_hoe_imp = v2elmulpar_osp_hog_imp if v2ex_hosw <= 0.5 // If head of state is as or less powerful than head of government, head of government is the head of the executive.
* Note: Some values of v2ex_hosw are missing, and using v2exhoshog and v2ex_hogw as well improves coverage; Marcus Lührmann agrees with the addition; I therefore add the next two lines:
replace v2elmulpar_osp_hoe_imp = v2elmulpar_osp_hos_imp if v2exhoshog == 1 // If head of state is also head of government, they are the head of the executive.
replace v2elmulpar_osp_hoe_imp = v2elmulpar_osp_hos_imp if v2ex_hogw == 0 // If head of government is less powerful than head of state, head of state must be more powerful than head of government.
* replace v2elmulpar_osp_hoe_imp = 1 if v2elmulpar_osp_exleg_imp == 1
* Note: Marcus Tannenberg does not know why it is assumed that if legislative and executive are elected in multi-party elections, chief of executive is elected in multi-party elections - even if direct coding seems to disagree; Anna Lührmann wrote this code. This leads to regimes under prominent heads of state which came to office in coup d'etats or rebellions to not be classified as closed autocracies. I therefore do not use this line of code; I compare the differences between my coding and the standard RoW coding below.

* Create indicator for minimally free and fair and multi-party elections and minimal features of an electoral democracy otherwise:
generate v2x_polyarchy_dich_row = 0 if v2x_polyarchy != .
replace v2x_polyarchy_dich_row = 1 if v2x_polyarchy > 0.5 & v2x_polyarchy != . & v2elfrfair_osp_imp > 2 & v2elfrfair_osp_imp != . & v2elmulpar_osp_imp > 2 & v2elmulpar_osp_imp != . 

* Create indicator for minimally transparent laws, minimal access to the justice system for men and women, and minimal features of a liberal democracy otherwise:
generate v2x_liberal_dich_row = .
replace v2x_liberal_dich_row = 1 if v2x_liberal > 0.8 & v2x_liberal !=. & v2clacjstm_osp > 3 & v2clacjstm_osp != . & v2clacjstw_osp > 3 & v2clacjstw_osp != . & v2cltrnslw_osp > 3 & v2cltrnslw_osp != .

* Create indicator for Regimes of the World with expanded coverage and minor changes to coding:
gen v2x_regime_owid = .
replace v2x_regime_owid = 3 if v2x_polyarchy_dich_row == 1 & v2x_liberal_dich_row == 1
replace v2x_regime_owid = 2 if v2x_polyarchy_dich_row == 1 & v2x_liberal_dich_row != 1
replace v2x_regime_owid = 1 if v2x_polyarchy_dich_row == 0 & v2elmulpar_osp_hoe_imp == 1 & v2elmulpar_osp_leg_imp > 1
* The line above means that 101 observations are grouped into this category even though v2elmulpar_osp_leg_imp == ., as . is treated as positive infinity; I still follow RoW instead of not coding these observations.
list country_name year if v2x_polyarchy_dich_row == 0 & v2elmulpar_osp_hoe_imp == 1 & v2elmulpar_osp_leg_imp == .
replace v2x_regime_owid = 0 if v2x_polyarchy_dich_row == 0 & (v2elmulpar_osp_hoe_imp == 0 | v2elmulpar_osp_leg_imp <= 1) // Note: = added to v2elmulpar_osp_leg_imp < 1, even if v2elmulpar_osp_leg_imp != 1 for all observations, for possible future iterations.
* These coding rules create seven observations which are coded as electoral democracies even though they have a chief executive who neither meets the criteria for direct or indirect election, nor for being dependent on the legislature.
list country_name year v2x_regime_owid v2x_polyarchy v2elmulpar_osp_hoe_imp if v2x_polyarchy > 0.5 & v2x_polyarchy != . & (v2elmulpar_osp_hoe_imp == 0 | v2elmulpar_osp_leg_imp <= 1) & v2x_regime_owid != 0
* I do not change the coding for these observations because I presume that the criteria for electoral democracy overrule the criteria for distinguishing between electoral and closed autocracies. This also means that I cannot use these criteria alone to code some observations for which only v2x_polyarchy is missing.
* But: if one criteria for electoral democracy is not met, and one criteria for electoral autocracy is not met, this must mean that the country is a closed autocracy:
replace v2x_regime_owid = 0 if (v2elfrfair_osp_imp <= 2 | v2elmulpar_osp_imp <= 2) & (v2elmulpar_osp_hoe_imp == 0 | v2elmulpar_osp_leg_imp <= 1) & v2x_regime_owid == .
* This also means that if one criteria for electoral democracy is not met, yet both criteria for an electoral autocracy is met, it must be an electoral autocracy:
replace v2x_regime_owid = 1 if (v2elfrfair_osp_imp <= 2 | v2elmulpar_osp_imp <= 2) & v2elmulpar_osp_hoe_imp == 1 & v2elmulpar_osp_leg_imp > 1 & v2elmulpar_osp_leg_imp != . & v2x_regime_owid == .

label variable v2x_regime_owid "Regime (Regimes of the World, OWID)"
label define v2x_regime_owid_label 0 "closed autocracy" 1 "electoral autocracy" 2 "electoral democracy" 3 "liberal democracy"
label values v2x_regime_owid v2x_regime_owid_label


** Comparing my and standard RoW coding:

inspect v2x_regime_owid
inspect v2x_polyarchy // Note: Expanded RoW has a slightly larger coverage than the continuous V-Dem measure because some observations are coded without using it.

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


* Harmonize V-Dem and OWID country names:
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


keep country_name year v2x_regime_owid v2svindep v2x_polyarchy v2elfrfair_osp_imp v2elmulpar_osp_imp v2elmulpar_osp_hoe_imp v2elmulpar_osp_leg_imp v2x_liberal_dich_row v2x_liberal v2xlg_legcon v2lgqstexp v2lgotovst v2lginvstp v2lgoppart

save "Political regimes/vdem_temp.dta", replace



*** Add regime dataset to master dataset:

use "Political regimes/master.dta", clear

merge 1:1 country_name year using "Political regimes/vdem_temp.dta"
drop _merge

sort country_name year

** Impute regime data:

* Investigate whether non-independent states have diverse regime types:
tab v2svindep v2x_regime_owid
* Note: Most non-independent states are closed autocracies, but there are some electoral autocracies (and even electoral and liberal democracies: Australia 1858-1899, Iceland 1920-1943, Slovenia 1991). Non-independent states therefore better not be imputed as (closed) autocracies.

tab v2x_regime_owid if v2x_liberal == .
list v2x_regime_owid v2x_liberal_dich_row v2x_liberal v2xlg_legcon v2lgqstexp v2lgotovst v2lginvstp v2lgoppart if country_name == "Australia" & year >= 1895 & year <= 1905
replace v2x_regime_owid = 3 if country_name == "Australia" & year == 1900
* Note: the only case for which a missing value of v2x_liberal matters is Australia in 1900. I manually recode it above because the values in the surrounding year strongly suggest a coding as a liberal democracy.

list if country_name == "Sweden" & year == 1840
replace v2x_regime_owid = 0 if country_name == "Sweden" & year == 1840
* Note: Data (including for v2x_polyarchy) missing without clear reason, history of Sweden does not indicate consequential event; perhaps due to missing data on head of government, who is not listed even though he existed (likely Arvid Mauritz Posse). I manually recode it with the regime type in adjacent years.

* Possible imputations:
list year v2x_regime_owid v2x_polyarchy v2elfrfair_osp_imp v2elmulpar_osp_imp v2elmulpar_osp_hoe_imp v2elmulpar_osp_leg_imp if country_name == "Peru" & year >= 1880 & year <= 1900
* Note: I favor no imputation because of six years of missing data, and even though one criterion for electoral autocracy is not met, the country may have met the criteria for democracy (if unlikely), thereby overriding the former.
list year v2x_regime_owid v2x_polyarchy v2elfrfair_osp_imp v2elmulpar_osp_imp v2elmulpar_osp_hoe_imp v2elmulpar_osp_leg_imp if country_name == "Honduras" & year >= 1910 & year <= 1950
* Note: I favor no imputation because of 12 years of missing data, and the country may have met the criteria for democracy.

keep country_name year v2x_regime_owid

** Impute values for countries or territories and years for which Regimes of the World covers the relevant political entity:
* General notes: I impute for countries or territories without regime data which did not at any point have more than 1 million inhabitants; Wimmer and Min (2006) code status at the end of the year, CShapes 2.0 codes borders at the beginning of the year.

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
* Kazakhstan 1789-1989: imperial power Russia 1730-1990 (Wimmer and Min 2006), part of Russia 1886-1991; not colonized (Ertan et al. 2016).
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
* South Sudan 1789-2010: not listed, but Egypt imperial power of Sudan 1821-1881, mixed rule 1882-1955 (Wimmer and Min 2006), colony of United Kingdom 1898-1955, part of Sudan until 2012 (Cshapes 2.0), colonized by United Kingdom in 1898 (Ertan et al. 2016), independent 1885-1898 (Butcher and Griffiths 2020).
replace country_name_regime_imputed = "Sudan" if country_name == "South Sudan" & year >= 1900 & year <= 2010 // Data for Sudan only available since 1900.
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
* Sudan 1789-1899: Egypt imperial power 1821-1881, mixed rule 1882-1955 (Wimmer and Min 2006), colony of United Kingdom 1898-1955 (CShapes 2.0), colonized by United Kingdom in 1898 (Ertan et al. 2016), independent 1885-1898 (Butcher and Griffiths 2020); in 1886, colony Egypt of United Kingdom covers little of today's Sudan (CShapes 2.0); Egypt invades Sudanese territory in 1820, indigenous forces surrender in 1821, Mahdists capture Khartoum from Egypt and the British in 1885 (Encyclopedia Britannica).
replace country_name_regime_imputed = "Egypt" if country_name == "Sudan" & year >= 1821 & year <= 1884
* Brazil 1824-1825: independent since 1822 (Wimmer and Min 2006, Butcher and Griffiths 2020); I favor no imputation.
* Serbia 1789-1833, 1932-1934: imperial power Turkey 14th century - 1877 (Wimmer and Min 2006); part of the Ottoman Empire (Encyclopedia Britannica); no imperial power 1932-1934 (Wimmer and Min 2006), independent 1932-1934 (Cshapes 2.0); I favor no imputation for later period. 
replace country_name_regime_imputed = "Turkey" if country_name == "Serbia" & year >= 1789 & year <= 1833
* Croatia 1789-1940, 1945-1990: Austria-Hungary imperial power 1699-1917, mixed rule 1918, Yugoslavia 1919-1990 (Wimmer and Min 2006); Austria-Hungary 1886-1918, 1919 partially Hungary and Yugoslavia, 1920-1992 Yugoslavia; I favor no imputation.
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
* Taiwan 1789-1899: part of China 1886-1895, colony by Japan afterwards (CShapes 2.0), imperial power 17th century - 1947 (Wimmer and Min 2006), colonized by Japan 1895-1945 (Ertan et al. 2016).
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


** Merge with V-Dem dataset again, this time on imputing countries:

rename country_name country_name_temp
rename country_name_regime_imputed country_name
rename v2x_regime_owid v2x_regime_owid_temp

sort country_name year
merge m:1 country_name year using "Political regimes/vdem_temp.dta"
drop if _merge == 2

erase "Political regimes/vdem_temp.dta"

rename country_name regime_row_imputed_country_name
rename country_name_temp country_name
rename v2x_regime_owid v2x_regime_owid_imputed
rename v2x_regime_owid_temp v2x_regime_owid

sort country_name year
keep country_name year v2x_regime_owid regime_row_imputed_country_name v2x_regime_owid_imputed
order country_name year v2x_regime_owid regime_row_imputed_country_name v2x_regime_owid_imputed

* Check if there are any observations with imputed regimes even though there is no need for imputation:
list if v2x_regime_owid != . & v2x_regime_owid_imputed != .

* Check if there are any observations with imputed country but without imputed regime:
list if v2x_regime_owid_imputed == . & regime_row_imputed_country_name != ""
replace regime_row_imputed_country_name = "" if v2x_regime_owid_imputed == .

* Reformat variables:
replace v2x_regime_owid = v2x_regime_owid_imputed if v2x_regime_owid == .
drop v2x_regime_owid_imputed

rename v2x_regime_owid regime_row_owid
label values regime_row_owid

generate regime_row_imputed = ""
replace regime_row_imputed = "yes" if regime_row_imputed_country_name != ""
replace regime_row_imputed = "no" if regime_row_imputed_country_name == ""
order regime_row_imputed, after(regime_row_owid)

label variable regime_row_imputed "Regime imputed from another country"
label variable regime_row_imputed_country_name "Name of the country from which regime was imputed"

erase "Political regimes/master.dta"


** Export regime information:

* Keep only countries with at least one year of regime information:

preserve

generate number_years = .
bysort country_name: replace number_years = _N

generate missing_regime = .
replace missing_regime = 1 if regime_row_owid == .

bysort country_name: egen number_years_missing_regime = total(missing_regime)

drop if number_years == number_years_missing_regime
drop number_years missing_regime number_years_missing_regime

save "Political regimes/regimes_owid.dta", replace
export delimited "Political regimes/regimes_owid.csv", replace

restore


** Export regime population information:

* Add population data:
merge 1:1 country_name year using "Our World in Data/population_owid.dta"

* Take a look at unmerged cases:
drop if year < 1800 | year > 2020
tab _merge // Note: no unmatched observations in using dataset between 1789 and 2020.
drop _merge

* Recode Regimes of the World indicator such that it includes a category for when population data is available, but regime data is missing:
replace regime_row_owid = 4 if regime_row_owid == . & population_owid != .
label values regime_row_owid v2x_regime_owid_label
label define v2x_regime_owid_label 4 "no regime data", add
drop if population_owid == .
tab regime_row_owid, m

* Create number of people living in different regimes:

preserve

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


exit
