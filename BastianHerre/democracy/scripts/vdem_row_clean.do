*****  This Stata do-file cleans the democracy dataset by the Varieties of Democracy (V-Dem) project, including the Regimes of the World (RoW) data
*****  Author: Bastian Herre
*****  June 28, 2022

version 14
clear all
set more off
set varabbrev off


** Set your own working directories here to run the file:
cd "/Users/bastianherre/Dropbox/Data/"
global project "/Users/bastianherre/Dropbox/Data/"


** Download V-Dem dataset from https://www.v-dem.net/vdemds.html and move it into the folder "Varieties of Democracy v12"
** Import V-Dem dataset:
use "Varieties of Democracy v12/V-Dem-CY-Full+Others-v12.dta", clear


** Keep variables of interest:
keep country_name year v2x_regime v2x_regime_amb v2elmulpar_osp v2elmulpar_osp_codehigh v2elmulpar_osp_codelow v2elfrfair_osp v2elfrfair_osp_codehigh v2elfrfair_osp_codelow v2x_elecreg v2xex_elecreg v2xlg_elecreg v2eltype* v2exnamhos v2exhoshog v2expathhs v2exnamhog v2expathhg v2ex_hosw v2ex_hogw v2ex_legconhog v2ex_legconhos v2exaphogp v2cltrnslw_osp v2cltrnslw_osp_codehigh v2cltrnslw_osp_codelow v2clacjstm_osp v2clacjstm_osp_codehigh v2clacjstm_osp_codelow v2clacjstw_osp v2clacjstw_osp_codehigh v2clacjstw_osp_codelow ///
	v2x_polyarchy v2x_elecoff v2xel_frefair v2x_frassoc_thick v2x_suffr v2x_freexp_altinf v2x_polyarchy_codelow v2xel_frefair_codelow v2x_frassoc_thick_codelow v2x_freexp_altinf_codelow v2x_polyarchy_codehigh v2xel_frefair_codehigh v2x_frassoc_thick_codehigh v2x_freexp_altinf_codehigh ///
	v2x_libdem v2x_liberal v2xcl_rol v2x_jucon v2xlg_legcon v2x_libdem_codelow v2x_liberal_codelow v2xcl_rol_codelow v2x_jucon_codelow v2xlg_legcon_codelow v2x_libdem_codehigh v2x_liberal_codehigh v2xcl_rol_codehigh v2x_jucon_codehigh v2xlg_legcon_codehigh ///
	v2x_partipdem v2x_partip v2x_cspart v2xdd_dd v2xel_locelec v2xel_regelec v2x_partipdem_codelow v2x_partip_codelow v2x_cspart_codelow v2xel_locelec_codelow v2xel_regelec_codelow v2x_partipdem_codehigh v2x_partip_codehigh v2x_cspart_codehigh v2xel_locelec_codehigh v2xel_regelec_codehigh ///
	v2x_delibdem v2xdl_delib v2dlreason v2dlcommon v2dlcountr v2dlconslt v2dlengage v2x_delibdem_codelow v2xdl_delib_codelow v2dlreason_codelow v2dlcommon_codelow v2dlcountr_codelow v2dlconslt_codelow v2dlengage_codelow v2x_delibdem_codehigh v2xdl_delib_codehigh v2dlreason_codehigh v2dlcommon_codehigh v2dlcountr_codehigh v2dlconslt_codehigh v2dlengage_codehigh ///
	v2x_egaldem v2x_egal v2xeg_eqprotec v2xeg_eqaccess v2xeg_eqdr v2x_egaldem_codelow v2x_egal_codelow v2xeg_eqprotec_codelow v2xeg_eqaccess_codelow v2xeg_eqdr_codelow v2x_egaldem_codehigh v2x_egal_codehigh v2xeg_eqprotec_codehigh v2xeg_eqaccess_codehigh v2xeg_eqdr_codehigh ///
	v2eltrnout e_wbgi_gee

** Drop superfluous observations:
drop if country_name == "Italy" & year == 1861
replace country_name = "Italy" if country_name == "Piedmont-Sardinia" & year == 1861 // Piedmont-Sardinia became Italy during 1861.


** Correct errors in head of state and head of government variables:

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


** Create expanded and refined Regimes of the World indicator:

* Create numeric country identifier:
encode country_name, generate(country_number)

* Declare dataset to be time-series data:
tsset country_number year

* Create indicators for multi-party elections with imputed values between election-years:
generate v2elmulpar_osp_imp = v2elmulpar_osp
replace v2elmulpar_osp_imp = l.v2elmulpar_osp_imp if v2elmulpar_osp_imp == . & v2x_elecreg == 1

generate v2elmulpar_osp_high_imp = v2elmulpar_osp_codehigh
replace v2elmulpar_osp_high_imp = l.v2elmulpar_osp_high_imp if v2elmulpar_osp_high_imp == . & v2x_elecreg == 1

generate v2elmulpar_osp_low_imp = v2elmulpar_osp_codelow
replace v2elmulpar_osp_low_imp = l.v2elmulpar_osp_low_imp if v2elmulpar_osp_low_imp == . & v2x_elecreg == 1

* Create indicators for free and fair elections with imputed values between election-years:
generate v2elfrfair_osp_imp = v2elfrfair_osp
replace v2elfrfair_osp_imp = l.v2elfrfair_osp_imp if v2elfrfair_osp_imp == . & v2x_elecreg == 1

generate v2elfrfair_osp_high_imp = v2elfrfair_osp
replace v2elfrfair_osp_high_imp = l.v2elfrfair_osp_high_imp if v2elfrfair_osp_high_imp == . & v2x_elecreg == 1

generate v2elfrfair_osp_low_imp = v2elfrfair_osp
replace v2elfrfair_osp_low_imp = l.v2elfrfair_osp_low_imp if v2elfrfair_osp_low_imp == . & v2x_elecreg == 1

* Create indicators for multi-party executive elections, and multi-party executive elections with imputed values between election-years:
generate v2elmulpar_osp_ex = v2elmulpar_osp if v2eltype_6 == 1 | v2eltype_7 == 1
generate v2elmulpar_osp_ex_imp = v2elmulpar_osp_ex
replace v2elmulpar_osp_ex_imp = l.v2elmulpar_osp_ex_imp if v2elmulpar_osp_ex_imp == . & v2xex_elecreg == 1

generate v2elmulpar_osp_ex_high = v2elmulpar_osp_codehigh if v2eltype_6 == 1 | v2eltype_7 == 1
generate v2elmulpar_osp_ex_high_imp = v2elmulpar_osp_ex_high
replace v2elmulpar_osp_ex_high_imp = l.v2elmulpar_osp_ex_high_imp if v2elmulpar_osp_ex_high_imp == . & v2xex_elecreg == 1

generate v2elmulpar_osp_ex_low = v2elmulpar_osp_codelow if v2eltype_6 == 1 | v2eltype_7 == 1
generate v2elmulpar_osp_ex_low_imp = v2elmulpar_osp_ex_low
replace v2elmulpar_osp_ex_low_imp = l.v2elmulpar_osp_ex_low_imp if v2elmulpar_osp_ex_low_imp == . & v2xex_elecreg == 1

* Create indicators for multi-party legislative elections, and multi-party legislative elections with imputed values between election-years:
generate v2elmulpar_osp_leg = v2elmulpar_osp if v2eltype_0 == 1 | v2eltype_1 == 1 | v2eltype_4 == 1 | v2eltype_5 == 1 // v2eltype_4 and v2eltype_5 excluded in Marcus Tannenberg and Anna Lührmann's Stata code; included here to align coding with code in V-Dem's data pipeline.
generate v2elmulpar_osp_leg_imp = v2elmulpar_osp_leg
replace v2elmulpar_osp_leg_imp = l.v2elmulpar_osp_leg_imp if v2elmulpar_osp_leg_imp == . & v2xlg_elecreg == 1

generate v2elmulpar_osp_leg_high = v2elmulpar_osp_codehigh if v2eltype_0 == 1 | v2eltype_1 == 1 | v2eltype_4 == 1 | v2eltype_5 == 1 // v2eltype_4 and v2eltype_5 excluded in Marcus Tannenberg and Anna Lührmann's Stata code; included here to align coding with code in V-Dem's data pipeline.
generate v2elmulpar_osp_leg_high_imp = v2elmulpar_osp_leg_high
replace v2elmulpar_osp_leg_high_imp = l.v2elmulpar_osp_leg_high_imp if v2elmulpar_osp_leg_high_imp == . & v2xlg_elecreg == 1

generate v2elmulpar_osp_leg_low = v2elmulpar_osp_codelow if v2eltype_0 == 1 | v2eltype_1 == 1 | v2eltype_4 == 1 | v2eltype_5 == 1 // v2eltype_4 and v2eltype_5 excluded in Marcus Tannenberg and Anna Lührmann's Stata code; included here to align coding with code in V-Dem's data pipeline.
generate v2elmulpar_osp_leg_low_imp = v2elmulpar_osp_leg_low
replace v2elmulpar_osp_leg_low_imp = l.v2elmulpar_osp_leg_low_imp if v2elmulpar_osp_leg_low_imp == . & v2xlg_elecreg == 1

* Create indicators for multi-party head of state elections with imputed values between election-years:
generate v2elmulpar_osp_hos_imp = 0 if v2x_elecreg != .
* Marcus Tannenberg does not know why electoral regime used as filter instead of relative power of heads of state and government as filter, as above; Anna Lührmann wrote this code. Using electoral regime as filter for this and all following variables yields identical coding.
replace v2elmulpar_osp_hos_imp = 1 if v2expathhs == 7 & v2xex_elecreg == 1 & v2elmulpar_osp_ex_imp > 1 & v2elmulpar_osp_ex_imp != . // If head of state is directly elected, elections for executive must be multi-party.
replace v2elmulpar_osp_hos_imp = 1 if v2expathhs == 6 & v2xlg_elecreg == 1 & v2elmulpar_osp_leg_imp > 1 & v2elmulpar_osp_leg_imp !=. // If head of state is appointed by legislature, elections for legislature must be multi-party.
* replace v2elmulpar_osp_hos_imp = 1 if v2ex_legconhos == 1 & v2xlg_elecreg == 1 & v2elmulpar_osp_ex_imp > 1 & v2elmulpar_osp_ex_imp != . // If head of state is appointed otherwise, but approval by the legislature is necessary, elections for legislature must be multi-party.
* It is unclear why v2elmulpar_osp_ex_imp and not v2elmulpar_osp_leg_imp is used, if this is about legislative elections; this seems to be an error, which is why I use the following code instead:
replace v2elmulpar_osp_hos_imp = 1 if v2ex_legconhos == 1 & v2xlg_elecreg == 1 & v2elmulpar_osp_leg_imp > 1 & v2elmulpar_osp_leg_imp != . // If head of state is appointed otherwise, but approval by the legislature is necessary, elections for legislature must be multi-party.

generate v2elmulpar_osp_hos_high_imp = 0 if v2x_elecreg != .
replace v2elmulpar_osp_hos_high_imp = 1 if v2expathhs == 7 & v2xex_elecreg == 1 & v2elmulpar_osp_ex_high_imp > 1 & v2elmulpar_osp_ex_high_imp != . // If head of state is directly elected, elections for executive must be multi-party.
replace v2elmulpar_osp_hos_high_imp = 1 if v2expathhs == 6 & v2xlg_elecreg == 1 & v2elmulpar_osp_leg_high_imp > 1 & v2elmulpar_osp_leg_high_imp !=. // If head of state is appointed by legislature, elections for legislature must be multi-party.
replace v2elmulpar_osp_hos_high_imp = 1 if v2ex_legconhos == 1 & v2xlg_elecreg == 1 & v2elmulpar_osp_leg_high_imp > 1 & v2elmulpar_osp_leg_high_imp != . // If head of state is appointed otherwise, but approval by the legislature is necessary, elections for legislature must be multi-party.

generate v2elmulpar_osp_hos_low_imp = 0 if v2x_elecreg != .
replace v2elmulpar_osp_hos_low_imp = 1 if v2expathhs == 7 & v2xex_elecreg == 1 & v2elmulpar_osp_ex_low_imp > 1 & v2elmulpar_osp_ex_low_imp != . // If head of state is directly elected, elections for executive must be multi-party.
replace v2elmulpar_osp_hos_low_imp = 1 if v2expathhs == 6 & v2xlg_elecreg == 1 & v2elmulpar_osp_leg_low_imp > 1 & v2elmulpar_osp_leg_low_imp !=. // If head of state is appointed by legislature, elections for legislature must be multi-party.
replace v2elmulpar_osp_hos_low_imp = 1 if v2ex_legconhos == 1 & v2xlg_elecreg == 1 & v2elmulpar_osp_leg_low_imp > 1 & v2elmulpar_osp_leg_low_imp != . // If head of state is appointed otherwise, but approval by the legislature is necessary, elections for legislature must be multi-party.

* Create indicators for multi-party head of government elections with imputed values between election-years:
generate v2elmulpar_osp_hog_imp = 0 if v2x_elecreg != .
replace v2elmulpar_osp_hog_imp = 1 if v2expathhg == 8 & v2xex_elecreg == 1 & v2elmulpar_osp_ex_imp > 1 & v2elmulpar_osp_ex_imp != . // If head of government is directly elected, elections for executive must be multi-party.
replace v2elmulpar_osp_hog_imp = 1 if v2expathhg == 7 & v2xlg_elecreg == 1 & v2elmulpar_osp_leg_imp > 1 & v2elmulpar_osp_leg_imp != . // If head of government is appointed by legislature, elections for legislature must be multi-party.
replace v2elmulpar_osp_hog_imp = 1 if v2expathhg == 6 & v2elmulpar_osp_hos_imp == 1 // If head of government is appointed by the head of state, elections for the head of state must be multi-party.

* replace v2elmulpar_osp_hog_imp = 1 if v2exaphogp == 1 & v2elmulpar_osp_imp != . & v2elmulpar_osp_leg_imp > 1 & v2elmulpar_osp_leg_imp != . // If head of government is appointed otherwise, but approval by the legislature is necessary, elections for legislature must be multi-party.
* Marcus Tannenberg does not know why v2elmulpar_osp_imp used as filter here, and not v2xlg_elecreg; Anna Lührmann may have come up with this fix, as the only five observations coded differently - Cambodia 1973-1974 and Haiti 1992-1994 - in his opinion should be closed autocracies due to no elections being held due to civil war and military rule, respectively.
* But: as described above, Haiti's chief executive is coded incorrectly until 1994, and correcting for that turns the country into a closed autocracy from 1991 to 1993. In 1994 the previously elected president returns, and it is plausible to presume he and his head of government are accountable to the legislature again, making the country an electoral autocracy. And just because a civil war in Cambodia goes on, that does not mean that its chief executive is not accountable to a legislature anymore. I therefore do not use the fix here.
* Yet: I use v2ex_legconhog instead of v2exaphogp to use the variable analogous to v2ex_legconhos above:
replace v2elmulpar_osp_hog_imp = 1 if v2ex_legconhog == 1 & v2xlg_elecreg == 1 & v2elmulpar_osp_leg_imp > 1 & v2elmulpar_osp_leg_imp != . // If head of government is appointed otherwise, but approval by the legislature is necessary, elections for legislature must be multi-party.

generate v2elmulpar_osp_hog_high_imp = 0 if v2x_elecreg != .
replace v2elmulpar_osp_hog_high_imp = 1 if v2expathhg == 8 & v2xex_elecreg == 1 & v2elmulpar_osp_ex_high_imp > 1 & v2elmulpar_osp_ex_high_imp != . // If head of government is directly elected, elections for executive must be multi-party.
replace v2elmulpar_osp_hog_high_imp = 1 if v2expathhg == 7 & v2xlg_elecreg == 1 & v2elmulpar_osp_leg_high_imp > 1 & v2elmulpar_osp_leg_high_imp != . // If head of government is appointed by legislature, elections for legislature must be multi-party.
replace v2elmulpar_osp_hog_high_imp = 1 if v2expathhg == 6 & v2elmulpar_osp_hos_high_imp == 1 // If head of government is appointed by the head of state, elections for the head of state must be multi-party.

replace v2elmulpar_osp_hog_high_imp = 1 if v2ex_legconhog == 1 & v2xlg_elecreg == 1 & v2elmulpar_osp_leg_high_imp > 1 & v2elmulpar_osp_leg_high_imp != . // If head of government is appointed otherwise, but approval by the legislature is necessary, elections for legislature must be multi-party.

generate v2elmulpar_osp_hog_low_imp = 0 if v2x_elecreg != .
replace v2elmulpar_osp_hog_low_imp = 1 if v2expathhg == 8 & v2xex_elecreg == 1 & v2elmulpar_osp_ex_low_imp > 1 & v2elmulpar_osp_ex_low_imp != . // If head of government is directly elected, elections for executive must be multi-party.
replace v2elmulpar_osp_hog_low_imp = 1 if v2expathhg == 7 & v2xlg_elecreg == 1 & v2elmulpar_osp_leg_low_imp > 1 & v2elmulpar_osp_leg_low_imp != . // If head of government is appointed by legislature, elections for legislature must be multi-party.
replace v2elmulpar_osp_hog_low_imp = 1 if v2expathhg == 6 & v2elmulpar_osp_hos_low_imp == 1 // If head of government is appointed by the head of state, elections for the head of state must be multi-party.

replace v2elmulpar_osp_hog_low_imp = 1 if v2ex_legconhog == 1 & v2xlg_elecreg == 1 & v2elmulpar_osp_leg_low_imp > 1 & v2elmulpar_osp_leg_low_imp != . // If head of government is appointed otherwise, but approval by the legislature is necessary, elections for legislature must be multi-party.

* Create indicators for multi-party executive and legislative elections with imputed values between election-years:
generate v2elmulpar_osp_exleg_imp = 0 if v2ex_hosw != .
replace v2elmulpar_osp_exleg_imp = 1 if v2xlg_elecreg == 1 & v2xex_elecreg == 1 & v2elmulpar_osp_ex_imp > 1 & v2elmulpar_osp_ex_imp != . & v2elmulpar_osp_leg_imp > 1 & v2elmulpar_osp_leg_imp != .

generate v2elmulpar_osp_exleg_high_imp = 0 if v2ex_hosw != .
replace v2elmulpar_osp_exleg_high_imp = 1 if v2xlg_elecreg == 1 & v2xex_elecreg == 1 & v2elmulpar_osp_ex_high_imp > 1 & v2elmulpar_osp_ex_high_imp != . & v2elmulpar_osp_leg_high_imp > 1 & v2elmulpar_osp_leg_high_imp != .

generate v2elmulpar_osp_exleg_low_imp = 0 if v2ex_hosw != .
replace v2elmulpar_osp_exleg_low_imp = 1 if v2xlg_elecreg == 1 & v2xex_elecreg == 1 & v2elmulpar_osp_ex_low_imp > 1 & v2elmulpar_osp_ex_low_imp != . & v2elmulpar_osp_leg_low_imp > 1 & v2elmulpar_osp_leg_low_imp != .

* Create indicator for multi-party head of executive elections with imputed values between election-years:
generate v2elmulpar_osp_hoe_imp = 0 if v2ex_hosw != .
replace v2elmulpar_osp_hoe_imp = v2elmulpar_osp_hos_imp if v2ex_hosw <= 1 & v2ex_hosw > 0.5 // If head of state is more powerful than head of government, head of state is the head of the executive.
replace v2elmulpar_osp_hoe_imp = v2elmulpar_osp_hog_imp if v2ex_hosw <= 0.5 // If head of state is as or less powerful than head of government, head of government is the head of the executive.

* Some values of v2ex_hosw are missing, and using v2exhoshog and v2ex_hogw as well improves coverage; Marcus Lührmann agrees with the addition; I therefore add the next two lines:
replace v2elmulpar_osp_hoe_imp = v2elmulpar_osp_hos_imp if v2exhoshog == 1 // If head of state is also head of government, they are the head of the executive.
replace v2elmulpar_osp_hoe_imp = v2elmulpar_osp_hos_imp if v2ex_hogw == 0 // If head of government is less powerful than head of state, head of state must be more powerful than head of government.
* replace v2elmulpar_osp_hoe_imp = 1 if v2elmulpar_osp_exleg_imp == 1
* Marcus Tannenberg does not know why it is assumed that if legislative and executive are elected in multi-party elections, chief of executive is elected in multi-party elections - even if direct coding seems to disagree; Anna Lührmann wrote this code. This leads to regimes under prominent heads of state which came to office in coup d'etats or rebellions to not be classified as closed autocracies. I therefore do not use this line of code; I compare the differences between my coding and the standard RoW coding below.

generate v2elmulpar_osp_hoe_high_imp = 0 if v2ex_hosw != .
replace v2elmulpar_osp_hoe_high_imp = v2elmulpar_osp_hos_high_imp if v2ex_hosw <= 1 & v2ex_hosw > 0.5 // If head of state is more powerful than head of government, head of state is the head of the executive.
replace v2elmulpar_osp_hoe_high_imp = v2elmulpar_osp_hog_high_imp if v2ex_hosw <= 0.5 // If head of state is as or less powerful than head of government, head of government is the head of the executive.

replace v2elmulpar_osp_hoe_high_imp = v2elmulpar_osp_hos_high_imp if v2exhoshog == 1 // If head of state is also head of government, they are the head of the executive.
replace v2elmulpar_osp_hoe_high_imp = v2elmulpar_osp_hos_high_imp if v2ex_hogw == 0 // If head of government is less powerful than head of state, head of state must be more powerful than head of government.

generate v2elmulpar_osp_hoe_low_imp = 0 if v2ex_hosw != .
replace v2elmulpar_osp_hoe_low_imp = v2elmulpar_osp_hos_low_imp if v2ex_hosw <= 1 & v2ex_hosw > 0.5 // If head of state is more powerful than head of government, head of state is the head of the executive.
replace v2elmulpar_osp_hoe_low_imp = v2elmulpar_osp_hog_low_imp if v2ex_hosw <= 0.5 // If head of state is as or less powerful than head of government, head of government is the head of the executive.

replace v2elmulpar_osp_hoe_low_imp = v2elmulpar_osp_hos_low_imp if v2exhoshog == 1 // If head of state is also head of government, they are the head of the executive.
replace v2elmulpar_osp_hoe_low_imp = v2elmulpar_osp_hos_low_imp if v2ex_hogw == 0 // If head of government is less powerful than head of state, head of state must be more powerful than head of government.

* Create dichotomous indicators for classification criteria:
generate v2x_polyarchy_dich = .
replace v2x_polyarchy_dich = 0 if v2x_polyarchy >= 0 & v2x_polyarchy <= 0.5
replace v2x_polyarchy_dich = 1 if v2x_polyarchy > 0.5 & v2x_polyarchy <= 1 // relative to V-Dem/RoW, = added to v2elmulpar_osp_leg_imp < 1, even if v2elmulpar_osp_leg_imp != 1 for all observations, for possible future iterations.

generate v2x_polyarchy_high_dich = .
replace v2x_polyarchy_high_dich = 0 if v2x_polyarchy_codehigh >= 0 & v2x_polyarchy_codehigh <= 0.5
replace v2x_polyarchy_high_dich = 1 if v2x_polyarchy_codehigh > 0.5 & v2x_polyarchy_codehigh <= 1 // relative to V-Dem/RoW, = added to v2elmulpar_osp_leg_imp < 1, even if v2elmulpar_osp_leg_imp != 1 for all observations, for possible future iterations.

generate v2x_polyarchy_low_dich = .
replace v2x_polyarchy_low_dich = 0 if v2x_polyarchy_codelow >= 0 & v2x_polyarchy_codelow <= 0.5
replace v2x_polyarchy_low_dich = 1 if v2x_polyarchy_codelow > 0.5 & v2x_polyarchy_codelow <= 1 // relative to V-Dem/RoW, = added to v2elmulpar_osp_leg_imp < 1, even if v2elmulpar_osp_leg_imp != 1 for all observations, for possible future iterations.

generate v2elfrfair_osp_imp_dich = .
replace v2elfrfair_osp_imp_dich = 0 if v2elfrfair_osp_imp <= 2
replace v2elfrfair_osp_imp_dich = 1 if v2elfrfair_osp_imp > 2 & v2elfrfair_osp_imp < .

generate v2elfrfair_osp_high_imp_dich = .
replace v2elfrfair_osp_high_imp_dich = 0 if v2elfrfair_osp_high_imp <= 2
replace v2elfrfair_osp_high_imp_dich = 1 if v2elfrfair_osp_high_imp > 2 & v2elfrfair_osp_high_imp < .

generate v2elfrfair_osp_low_imp_dich = .
replace v2elfrfair_osp_low_imp_dich = 0 if v2elfrfair_osp_low_imp <= 2
replace v2elfrfair_osp_low_imp_dich = 1 if v2elfrfair_osp_low_imp > 2 & v2elfrfair_osp_low_imp < .

generate v2elmulpar_osp_imp_dich = .
replace v2elmulpar_osp_imp_dich = 0 if v2elmulpar_osp_imp <= 2
replace v2elmulpar_osp_imp_dich = 1 if v2elmulpar_osp_imp > 2 & v2elmulpar_osp_imp < .

generate v2elmulpar_osp_high_imp_dich = .
replace v2elmulpar_osp_high_imp_dich = 0 if v2elmulpar_osp_high_imp <= 2
replace v2elmulpar_osp_high_imp_dich = 1 if v2elmulpar_osp_high_imp > 2 & v2elmulpar_osp_high_imp < .

generate v2elmulpar_osp_low_imp_dich = .
replace v2elmulpar_osp_low_imp_dich = 0 if v2elmulpar_osp_low_imp <= 2
replace v2elmulpar_osp_low_imp_dich = 1 if v2elmulpar_osp_low_imp > 2 & v2elmulpar_osp_low_imp < .

generate v2x_liberal_dich = .
replace v2x_liberal_dich = 0 if v2x_liberal >= 0 & v2x_liberal <= 0.8
replace v2x_liberal_dich = 1 if v2x_liberal > 0.8 & v2x_liberal <= 1

generate v2x_liberal_high_dich = .
replace v2x_liberal_high_dich = 0 if v2x_liberal_codehigh >= 0 & v2x_liberal_codehigh <= 0.8
replace v2x_liberal_high_dich = 1 if v2x_liberal_codehigh > 0.8 & v2x_liberal_codehigh <= 1

generate v2x_liberal_low_dich = .
replace v2x_liberal_low_dich = 0 if v2x_liberal_codelow >= 0 & v2x_liberal_codelow <= 0.8
replace v2x_liberal_low_dich = 1 if v2x_liberal_codelow > 0.8 & v2x_liberal_codelow <= 1

generate v2clacjstm_osp_dich = .
replace v2clacjstm_osp_dich = 0 if v2clacjstm_osp <= 3
replace v2clacjstm_osp_dich = 1 if v2clacjstm_osp > 3 & v2clacjstm_osp < .

generate v2clacjstm_osp_high_dich = .
replace v2clacjstm_osp_high_dich = 0 if v2clacjstm_osp_codehigh <= 3
replace v2clacjstm_osp_high_dich = 1 if v2clacjstm_osp_codehigh > 3 & v2clacjstm_osp_codehigh < .

generate v2clacjstm_osp_low_dich = .
replace v2clacjstm_osp_low_dich = 0 if v2clacjstm_osp_codelow <= 3
replace v2clacjstm_osp_low_dich = 1 if v2clacjstm_osp_codelow > 3 & v2clacjstm_osp_codelow < .

generate v2clacjstw_osp_dich = .
replace v2clacjstw_osp_dich = 0 if v2clacjstw_osp <= 3
replace v2clacjstw_osp_dich = 1 if v2clacjstw_osp > 3 & v2clacjstw_osp < .

generate v2clacjstw_osp_high_dich = .
replace v2clacjstw_osp_high_dich = 0 if v2clacjstw_osp_codehigh <= 3
replace v2clacjstw_osp_high_dich = 1 if v2clacjstw_osp_codehigh > 3 & v2clacjstw_osp_codehigh < .

generate v2clacjstw_osp_low_dich = .
replace v2clacjstw_osp_low_dich = 0 if v2clacjstw_osp_codelow <= 3
replace v2clacjstw_osp_low_dich = 1 if v2clacjstw_osp_codelow > 3 & v2clacjstw_osp_codelow < .

generate v2cltrnslw_osp_dich = .
replace v2cltrnslw_osp_dich = 0 if v2cltrnslw_osp <= 3
replace v2cltrnslw_osp_dich = 1 if v2cltrnslw_osp > 3 & v2cltrnslw_osp < .

generate v2cltrnslw_osp_high_dich = .
replace v2cltrnslw_osp_high_dich = 0 if v2cltrnslw_osp_codehigh <= 3
replace v2cltrnslw_osp_high_dich = 1 if v2cltrnslw_osp_codehigh > 3 & v2cltrnslw_osp_codehigh < .

generate v2cltrnslw_osp_low_dich = .
replace v2cltrnslw_osp_low_dich = 0 if v2cltrnslw_osp_codelow <= 3
replace v2cltrnslw_osp_low_dich = 1 if v2cltrnslw_osp_codelow > 3 & v2cltrnslw_osp_codelow < .

generate v2elmulpar_osp_leg_imp_dich = .
replace v2elmulpar_osp_leg_imp_dich = 0 if v2elmulpar_osp_leg_imp <= 1
replace v2elmulpar_osp_leg_imp_dich = 1 if v2elmulpar_osp_leg_imp > 1 & v2elmulpar_osp_leg_imp < . // relative to V-Dem/RoW, I added v2elmulpar_osp_leg_imp < ., as otherwise v2elmulpar_osp_leg_imp_dich = 1 if v2elmulpar_osp_leg_imp > 1.
tab v2elmulpar_osp_leg_imp_dich

generate v2elmulpar_osp_leg_high_imp_dich = .
replace v2elmulpar_osp_leg_high_imp_dich = 0 if v2elmulpar_osp_leg_high_imp <= 1
replace v2elmulpar_osp_leg_high_imp_dich = 1 if v2elmulpar_osp_leg_high_imp > 1 & v2elmulpar_osp_leg_high_imp < . // relative to V-Dem/RoW, I added v2elmulpar_osp_leg_imp < ., as otherwise v2elmulpar_osp_leg_imp_dich = 1 if v2elmulpar_osp_leg_imp > 1.
tab v2elmulpar_osp_leg_high_imp_dich

generate v2elmulpar_osp_leg_low_imp_dich = .
replace v2elmulpar_osp_leg_low_imp_dich = 0 if v2elmulpar_osp_leg_low_imp <= 1
replace v2elmulpar_osp_leg_low_imp_dich = 1 if v2elmulpar_osp_leg_low_imp > 1 & v2elmulpar_osp_leg_low_imp < . // relative to V-Dem/RoW, I added v2elmulpar_osp_leg_imp < ., as otherwise v2elmulpar_osp_leg_imp_dich = 1 if v2elmulpar_osp_leg_imp > 1.
tab v2elmulpar_osp_leg_low_imp_dich

* Create indicators for Regimes of the World with expanded coverage and minor changes to coding:
generate regime_row_owid = .
replace regime_row_owid = 3 if (v2elfrfair_osp_imp_dich == 1 & v2elmulpar_osp_imp_dich == 1 & v2x_polyarchy_dich == 1) & (v2x_liberal_dich == 1 & v2clacjstm_osp_dich == 1 & v2clacjstw_osp_dich == 1 & v2cltrnslw_osp_dich == 1)
replace regime_row_owid = 2 if (v2elfrfair_osp_imp_dich == 1 & v2elmulpar_osp_imp_dich == 1 & v2x_polyarchy_dich == 1) & (v2x_liberal_dich == 0 | v2clacjstm_osp_dich == 0 | v2clacjstw_osp_dich == 0 | v2cltrnslw_osp_dich == 0) // relative to V-Dem/RoW, the liberal-democracy conditions have to be = 0 , not != 1, as otherwise missing data, i.e. positive infinity is also included.
replace regime_row_owid = 1 if (v2elfrfair_osp_imp_dich == 0 | v2elmulpar_osp_imp_dich == 0 | v2x_polyarchy_dich == 0) & (v2elmulpar_osp_hoe_imp == 1 & v2elmulpar_osp_leg_imp_dich == 1)
replace regime_row_owid = 0 if (v2elfrfair_osp_imp_dich == 0 | v2elmulpar_osp_imp_dich == 0 | v2x_polyarchy_dich == 0) & (v2elmulpar_osp_hoe_imp == 0 | v2elmulpar_osp_leg_imp_dich == 0)
* These coding rules allow for some observations being coded as electoral democracies even though they have a chief executive who neither meets the criteria for direct or indirect election, nor for being dependent on the legislature.
* I do not change the coding for these observations because I presume that the criteria for electoral democracy overrule the criteria for distinguishing between electoral and closed autocracies. This also means that I cannot use these criteria alone to code some observations for which only v2x_polyarchy_dich is missing.

* But: if one criteria for electoral democracy is not met, and one criteria for electoral autocracy is not met, this must mean that the country is a closed autocracy:
replace regime_row_owid = 0 if (v2elfrfair_osp_imp_dich == 0 | v2elmulpar_osp_imp_dich == 0 | v2x_polyarchy_dich == 0) & (v2elmulpar_osp_hoe_imp == 0 | v2elmulpar_osp_leg_imp_dich == 0) & regime_row_owid == .
* This also means that if one criteria for electoral democracy is not met, yet both criteria for an electoral autocracy is met, it must be an electoral autocracy:
replace regime_row_owid = 1 if (v2elfrfair_osp_imp_dich == 0 | v2elmulpar_osp_imp_dich == 0 | v2x_polyarchy_dich == 0) & v2elmulpar_osp_hoe_imp == 1 & v2elmulpar_osp_leg_imp_dich == 1 & regime_row_owid == .

* Label indicator for Regimes of the World with expanded coverage and minor changes to coding:
label variable regime_row_owid "Political regime (RoW, OWID)"
label define regime_row_owid 0 "closed autocracy" 1 "electoral autocracy" 2 "electoral democracy" 3 "liberal democracy"
label values regime_row_owid regime_row_owid


** Compare our and standard RoW coding:
tab regime_row_owid v2x_regime if year >= 1900, m

* Observations own classification identifies as electoral autocracies, whereas RoW identifies them as electoral democracies:
list country_name year if regime_row_owid == 1 & v2x_regime == 2
list v2x_polyarchy if regime_row_owid == 1 & v2x_regime == 2
* Observations are coded differently because v2x_polyarchy in V-Dem's input dataset is barely above 0.5, whereas in the released dataset it is rounded to 0.5 and therefore is not above the coding threshold (conversation with Marcus Tannenberg and Johannes von Römer).
replace regime_row_owid = 2 if regime_row_owid == 1 & v2x_regime == 2

* Observations own classification identifies as electoral democracies, whereas RoW identifies them as liberal democracies:
list country_name year if regime_row_owid == 2 & v2x_regime == 3
list v2x_liberal v2clacjstm_osp v2clacjstw_osp v2cltrnslw_osp if regime_row_owid == 2 & v2x_regime == 3
* Observations most likely coded differently because v2cltrnslw_osp in V-Dem's input dataset is barely above 3, whereas in the released dataset it is rounded to 3 and therefore is not above the coding threshold.
replace regime_row_owid = 3 if regime_row_owid == 2 & v2x_regime == 3

* 18 observations own classification identifies as closed autocracies, whereas RoW does not provide data:
list country_name year if regime_row_owid == 0 & v2x_regime == . & year >= 1900
* Libya in 1911, 1914, and 1922-1933 can be coded because I use information from v2exhoshog in addition to information from v2ex_hosw to identify head of the executive.
list v2ex_hosw v2exhoshog if regime_row_owid == 0 & v2x_regime == . & year >= 1900 & country_name == "Libya"
* Honduras in 1934 and 1935, Kazakhstan in 1990, and Turkmenistan in 1990 can be coded because I use information from the other criteria for democracies and autocracies in the absence of information from v2x_polyarchy:
list v2x_polyarchy v2elfrfair_osp_imp_dich v2elmulpar_osp_imp_dich v2elmulpar_osp_hoe_imp v2elmulpar_osp_leg_imp_dich if regime_row_owid == 0 & v2x_regime == . & year >= 1900 & country_name != "Libya"

* 13 observations own classification identifies as electoral autocracies, whereas RoW does not provide data:
list country_name year if regime_row_owid == 1 & v2x_regime == . & year >= 1900
* Observations can be coded because I use information from the other criteria for democracies and autocracies in the absence of information from v2x_polyarchy:
list v2x_polyarchy v2elfrfair_osp_imp_dich v2elmulpar_osp_imp_dich v2elmulpar_osp_hoe_imp v2elmulpar_osp_leg_imp_dich if regime_row_owid == 1 & v2x_regime == . & year >= 1900

* Observations own classification identifies as closed autocracies, whereas RoW identifies them as electoral autocracies:
list country_name year if regime_row_owid == 0 & v2x_regime == 1

* Belgium in 1919 is hard-recoded in RoW code, though Marcus Tannenberg does not know why that happens even if the errors in a previous version of the V-Dem dataset should by now be remedied; it only continues to make a difference for Belgium in 1919; I keep the recode.
replace regime_row_owid = 1 if country_name == "Belgium" & year == 1919

label define v2expathhg 0 "Force" 1 "Foreign power" 2 "Ruling party" 3 "Royal council" 4 "Hereditary succession" 5 "Military" 6 "Head of state" 7 "Legislature" 8 "Directly" 9 "Other"
label values v2expathhg v2expathhg
list country_name year v2elmulpar_osp_exleg_imp v2elmulpar_osp_hoe_imp v2expathhs v2ex_legconhos v2elmulpar_osp_leg_imp if regime_row_owid == 0 & v2x_regime == 1 & v2ex_hosw <= 1 & v2ex_hosw > 0.5 & v2ex_legconhos == 0
* 100 observations with multi-party elections for legislature and executive (hence the RoW coding); but which had chief executive which were heads of state that were neither directly or indirectly chosen through multiparty elections, nor were they accountable to a legislature chosen through multi-party elections; I therefore do not recode them.
list country_name year v2exnamhos if regime_row_owid < v2x_regime & v2x_regime !=. & v2ex_hosw <= 1 & v2ex_hosw > 0.5
* Examples include many prominent heads of state which came to office in coup d'etats or rebellions, such as Boumedienne (Algeria 1965), Anez (Bolivia 2019), Buyoya (Burundi 1987), Batista (Cuba 1952), Ankrah (Ghana 1966), Khomeini (Iran 1980), Buhari (Nigeria 1983), Jammeh (Gambia 1994), and Eyadema (1967 Togo):

list country_name year v2elmulpar_osp_exleg_imp v2elmulpar_osp_hoe_imp v2expathhs v2ex_legconhos v2elmulpar_osp_leg_imp_dich if regime_row_owid == 0 & v2x_regime == 1 & v2ex_hosw <= 1 & v2ex_hosw > 0.5 & v2ex_legconhos != 0
* Nicaragua in 1901 and 1905 with head of state appointed by the legislature, but missing value for v2elmulpar_osp_leg_imp; v2elmulpar_osp_exleg_imp and v2elmulpar_osp_hoe_imp are only not missing because its coding as 0 is based on v2ex_hosw. I leave the coding as is because the coding is the same in adjacent years.

* 37 observations which had multi-party elections for legislature and executive (hence the RoW coding); but which had chief executives which were heads of government that were neither directly or indirectly chosen through multiparty elections, nor were they accountable to a legislature chosen through multi-party elections:
list country_name year v2elmulpar_osp_exleg_imp v2expathhg v2ex_legconhog v2expathhs v2ex_legconhos if regime_row_owid == 0 & v2x_regime == 1 & v2elmulpar_osp_exleg_imp == 1 & v2ex_hosw <= 0.5
* Examples include prominent heads of government which came to office in a rebellion or were appointed by a foreign power, such as Castro (Cuba 1959) and Paul Vories McNutt (Philippines 1937):
list country_name year v2exnamhog if regime_row_owid < v2x_regime & v2x_regime !=. & v2ex_hosw <= 0.5

* 3 observations coded differently because I use v2ex_legconhog above for consistency, while RoW uses v2exaphogp instead. I defer to RoW coding in these cases. It may be that their data pipeline uses date-specific data which are superior to the year-end data used here. 
list country_name year v2expathhg v2ex_legconhog v2exaphogp if regime_row_owid == 0 & v2x_regime == 1 & v2elmulpar_osp_exleg_imp == 0 & v2ex_hosw <= 0.5
replace regime_row_owid = 1 if regime_row_owid == 0 & v2x_regime == 1 & v2elmulpar_osp_exleg_imp == 0 & v2ex_hosw <= 0.5

* Observations own classification identifies as electoral autocracies, whereas RoW identifies them as closed autocracies:
list country_name year if regime_row_owid == 1 & v2x_regime == 0

* 120 observations with chief executives that were heads of state directly or indirectly elected chief executive and at least moderately multi-party elections for legislative, but which are affected by RoW's different standard filter (2elmulpar_osp_ex_imp instead of v2elmulpar_osp_leg_imp) above:
list v2elmulpar_osp_leg_imp_dich v2elmulpar_osp_hoe_imp v2elmulpar_osp_ex_imp v2elmulpar_osp_leg_imp if regime_row_owid == 1 & v2x_regime == 0 & v2ex_hosw <= 1 & v2ex_hosw > 0.5

* 3 observations with chief executives that were heads of government directly or indirectly elected chief executive and at least moderately multi-party elections for legislative, but which are affected by RoW's different standard filter (v2elmulpar_osp_imp instead of v2xlg_elecreg) above:
list v2elmulpar_osp_leg_imp v2elmulpar_osp_hoe_imp v2elmulpar_osp_imp v2xlg_elecreg if regime_row_owid == 1 & v2x_regime == 0 & v2ex_hosw <= 0.5

* 83 observations which RoW identifies as electoral autocracies, but which own classification identifies as missing:
list v2x_elecreg v2elfrfair_osp_imp_dich v2elmulpar_osp_imp_dich v2x_polyarchy_dich v2elmulpar_osp_hoe_imp v2elmulpar_osp_leg_imp_dich v2eltype_0 v2eltype_1 v2eltype_4 v2eltype_5 if regime_row_owid == . & v2x_regime == 1 // All observations have missing values for multi-party legislative elections, sometimes also for free and fair as well as multi-party elections in general. One could say that if v2x_electreg == 0 — or v2eltype_0/1/4/5 are all zero — this means that were no (multi-party legislative) elections - but this would make these regimes closed autocracies, not electoral autociraces. So this better stay as is.

* 1 observation which RoW identifies as closed autocracy, but which own classification identifies as missing:
list v2elfrfair_osp_imp_dich v2elmulpar_osp_imp_dich v2x_polyarchy_dich v2elmulpar_osp_hoe_imp v2elmulpar_osp_leg_imp_dich if regime_row_owid == . & v2x_regime == 0
list country_name year if regime_row_owid == . & v2x_regime == 0 // Slovakia in 1993 had not held legislative elections yet. This can stay as is.

* 1 observation which RoW identifies as electoral democracy, but which own classification identifies as missing:
list v2elfrfair_osp_imp_dich v2elmulpar_osp_imp_dich v2x_polyarchy_dich v2x_liberal_dich v2clacjstm_osp_dich v2clacjstw_osp_dich v2cltrnslw_osp_dich if regime_row_owid == . & v2x_regime == 2
list country_name year if regime_row_owid == . & v2x_regime == 2 // I impute Australia in 1900 in later script.

** Finalize expanded and refined Regimes of the World indicator with ambiguous categories:

generate regime_amb_row_owid = .
replace regime_amb_row_owid = 9 if regime_row_owid == 3
replace regime_amb_row_owid = 8 if regime_row_owid == 3 & (v2elfrfair_osp_low_imp_dich == 0 | v2elmulpar_osp_low_imp_dich == 0 | v2x_polyarchy_low_dich == 0 | v2x_liberal_low_dich == 0 | v2clacjstm_osp_low_dich == 0 | v2clacjstw_osp_low_dich == 0 | v2cltrnslw_osp_low_dich == 0)
replace regime_amb_row_owid = 6 if regime_row_owid == 2
replace regime_amb_row_owid = 7 if regime_row_owid == 2 & (v2elfrfair_osp_high_imp_dich == 1 & v2elmulpar_osp_high_imp_dich == 1 & v2x_polyarchy_high_dich == 1) & (v2x_liberal_high_dich == 1 & v2clacjstm_osp_high_dich == 1 & v2clacjstw_osp_high_dich == 1 & v2cltrnslw_osp_high_dich == 1)
replace regime_amb_row_owid = 5 if regime_row_owid == 2 & (v2elfrfair_osp_low_imp_dich == 0 | v2elmulpar_osp_low_imp_dich == 0 | v2x_polyarchy_low_dich == 0)
replace regime_amb_row_owid = 3 if regime_row_owid == 1
replace regime_amb_row_owid = 4 if regime_row_owid == 1 & (v2elfrfair_osp_high_imp_dich == 1 & v2elmulpar_osp_high_imp_dich == 1 & v2x_polyarchy_high_dich == 1)
replace regime_amb_row_owid = 2 if regime_row_owid == 1 & (v2elmulpar_osp_hoe_low_imp == 0 | v2elmulpar_osp_leg_low_imp_dich == 0)
replace regime_amb_row_owid = 0 if regime_row_owid == 0
replace regime_amb_row_owid = 1 if regime_row_owid == 0 & (v2elmulpar_osp_hoe_high_imp == 1 & v2elmulpar_osp_leg_high_imp_dich == 1)

* Label indicator for Regimes of the World with expanded coverage and minor changes to coding:
label variable regime_amb_row_owid "Political regime, including ambiguous categories (RoW, OWID)"
label define regime_amb_row_owid 0 "closed autocracy" 1 "closed autocracy, maybe electoral" 2 "electoral autocracy, maybe closed" 3 "electoral autocracy" 4 "electoral autocracy, maybe electoral democracy" 5 "electoral democracy, maybe electoral autocracy" 6 "electoral democracy" 7 "electoral democracy, maybe liberal" 8 "liberal democracy, maybe electoral" 9 "liberal democracy"
label values regime_amb_row_owid regime_amb_row_owid


** Compare our and standard RoW ambiguous coding:
tab regime_amb_row_owid v2x_regime_amb if year >= 1900, m
tab regime_amb_row_owid v2x_regime_amb if year >= 1900 & regime_row_owid == v2x_regime, m // Setting aside the observations reviewed above.
* Because the variables closely match each other, and the differences in the coding rules are difficult to track for the ambiguous classification which depends on even more variables than the simplified one, I presume that the remaining differences are due to the different coding rules or the rougher rounding of numbers in the released dataset, and I therefore do not make any changes to them.


** Drop now superfluous variables:
drop country_number v2x_regime v2x_regime_amb v2x_elecreg v2xex_elecreg v2xlg_elecreg v2eltype* v2elmulpar_osp v2elfrfair_osp v2elmulpar_osp_imp v2elmulpar_osp_leg_imp v2elfrfair_osp_imp v2exnamhos v2exhoshog v2expathhs v2exnamhog v2exaphogp v2ex_hogw v2expathhg v2ex_hosw v2ex_legconhog v2ex_legconhos v2elmulpar_osp_ex v2elmulpar_osp_ex_imp v2elmulpar_osp_leg v2elmulpar_osp_hos_imp v2elmulpar_osp_hog_imp v2elmulpar_osp_exleg_imp v2cltrnslw_osp v2clacjstm_osp v2clacjstw_osp v2elmulpar_osp_codehigh v2elmulpar_osp_codelow v2elfrfair_osp_codehigh v2elfrfair_osp_codelow v2elmulpar_osp_high_imp v2elmulpar_osp_low_imp v2elfrfair_osp_high_imp v2elfrfair_osp_low_imp v2elmulpar_osp_ex_high v2elmulpar_osp_ex_high_imp v2elmulpar_osp_ex_low v2elmulpar_osp_ex_low_imp v2elmulpar_osp_leg_high v2elmulpar_osp_leg_high_imp v2elmulpar_osp_leg_low v2elmulpar_osp_leg_low_imp v2elmulpar_osp_hos_high_imp v2elmulpar_osp_hos_low_imp v2elmulpar_osp_hog_high_imp v2elmulpar_osp_hog_low_imp v2elmulpar_osp_exleg_high_imp v2elmulpar_osp_exleg_low_imp v2cltrnslw_osp_codehigh v2cltrnslw_osp_codelow v2clacjstm_osp_codehigh v2clacjstm_osp_codelow v2clacjstw_osp_codehigh v2clacjstw_osp_codelow


** Create reduced version of political regimes, only distinguishing between closed autocracies, electoral autocracies, and electoral democracies (including liberal democracies):
generate regime_redux_row_owid = regime_row_owid
recode regime_redux_row_owid (3=2)
order regime_redux_row_owid, after(regime_row_owid)
label values regime_redux_row_owid regime_row_owid
label variable regime_redux_row_owid "Political regime (Regimes of the World, reduced, OWID)"


** Rename variables of interest:
rename v2x_polyarchy_dich electdem_dich_row_owid  // _owid suffix to reflect that I coded the variable slightly differently than Lührmann et al.
rename v2x_polyarchy_high_dich electdem_dich_high_row_owid
rename v2x_polyarchy_low_dich electdem_dich_low_row_owid

rename v2elfrfair_osp_imp_dich electfreefair_row
rename v2elfrfair_osp_high_imp_dich electfreefair_high_row
rename v2elfrfair_osp_low_imp_dich electfreefair_low_row

rename v2elmulpar_osp_imp_dich electmulpar_row
rename v2elmulpar_osp_high_imp_dich electmulpar_high_row
rename v2elmulpar_osp_low_imp_dich electmulpar_low_row

rename v2x_liberal_dich lib_dich_row
rename v2x_liberal_high_dich lib_dich_high_row
rename v2x_liberal_low_dich lib_dich_low_row

rename v2clacjstm_osp_dich accessjust_m_row
rename v2clacjstm_osp_high_dich accessjust_m_high_row
rename v2clacjstm_osp_low_dich accessjust_m_low_row

rename v2clacjstw_osp_dich accessjust_w_row
rename v2clacjstw_osp_high_dich accessjust_w_high_row
rename v2clacjstw_osp_low_dich accessjust_w_low_row

rename v2cltrnslw_osp_dich transplaws_row
rename v2cltrnslw_osp_high_dich transplaws_high_row
rename v2cltrnslw_osp_low_dich transplaws_low_row

rename v2elmulpar_osp_hoe_imp electmulpar_hoe_row_owid // _owid suffix to reflect that I coded the variable slightly differently than Lührmann et al.
rename v2elmulpar_osp_hoe_high_imp electmulpar_hoe_high_row_owid
rename v2elmulpar_osp_hoe_low_imp electmulpar_hoe_low_row_owid

rename v2elmulpar_osp_leg_imp_dich electmulpar_leg_row
rename v2elmulpar_osp_leg_high_imp_dich electmulpar_leg_high_row
rename v2elmulpar_osp_leg_low_imp_dich electmulpar_leg_low_row

rename v2x_polyarchy electdem_vdem
rename v2x_polyarchy_codelow electdem_vdem_low
rename v2x_polyarchy_codehigh electdem_vdem_high

rename v2x_elecoff electoff_vdem

rename v2xel_frefair electfreefair_vdem
rename v2xel_frefair_codelow electfreefair_vdem_low
rename v2xel_frefair_codehigh electfreefair_vdem_high

rename v2x_frassoc_thick freeassoc_vdem
rename v2x_frassoc_thick_codelow freeassoc_vdem_low
rename v2x_frassoc_thick_codehigh freeassoc_vdem_high

rename v2x_suffr suffr_vdem

rename v2x_freexp_altinf freeexpr_vdem
rename v2x_freexp_altinf_codelow freeexpr_vdem_low
rename v2x_freexp_altinf_codehigh freeexpr_vdem_high

rename v2x_libdem libdem_vdem
rename v2x_libdem_codelow libdem_vdem_low
rename v2x_libdem_codehigh libdem_vdem_high

rename v2x_liberal lib_vdem
rename v2x_liberal_codelow lib_vdem_low
rename v2x_liberal_codehigh lib_vdem_high

rename v2xcl_rol civlib_vdem
rename v2xcl_rol_codelow civlib_vdem_low
rename v2xcl_rol_codehigh civlib_vdem_high

rename v2x_jucon judicial_constr_vdem
rename v2x_jucon_codelow judicial_constr_vdem_low
rename v2x_jucon_codehigh judicial_constr_vdem_high

rename v2xlg_legcon legis_constr_vdem
rename v2xlg_legcon_codelow legis_constr_vdem_low
rename v2xlg_legcon_codehigh legis_constr_vdem_high

rename v2x_partipdem participdem_vdem
rename v2x_partipdem_codelow participdem_vdem_low
rename v2x_partipdem_codehigh participdem_vdem_high

rename v2x_partip particip_vdem
rename v2x_partip_codelow particip_vdem_low
rename v2x_partip_codehigh particip_vdem_high

rename v2x_cspart civsoc_particip_vdem
rename v2x_cspart_codelow civsoc_particip_vdem_low
rename v2x_cspart_codehigh civsoc_particip_vdem_high

rename v2xdd_dd dirpop_vote_vdem

rename v2xel_locelec locelect_vdem
rename v2xel_locelec_codelow locelect_vdem_low
rename v2xel_locelec_codehigh locelect_vdem_high

rename v2xel_regelec regelect_vdem
rename v2xel_regelec_codelow regelect_vdem_low
rename v2xel_regelec_codehigh regelect_vdem_high

rename v2x_delibdem delibdem_vdem
rename v2x_delibdem_codelow delibdem_vdem_low
rename v2x_delibdem_codehigh delibdem_vdem_high

rename v2xdl_delib delib_vdem
rename v2xdl_delib_codelow delib_vdem_low
rename v2xdl_delib_codehigh delib_vdem_high

rename v2dlreason justified_polch_vdem
rename v2dlreason_codelow justified_polch_vdem_low
rename v2dlreason_codehigh justified_polch_vdem_high

rename v2dlcommon justcomgd_polch_vdem
rename v2dlcommon_codelow justcomgd_polch_vdem_low
rename v2dlcommon_codehigh justcomgd_polch_vdem_high

rename v2dlcountr counterarg_polch_vdem
rename v2dlcountr_codelow counterarg_polch_vdem_low
rename v2dlcountr_codehigh counterarg_polch_vdem_high

rename v2dlconslt elitecons_polch_vdem
rename v2dlconslt_codelow elitecons_polch_vdem_low
rename v2dlconslt_codehigh elitecons_polch_vdem_high

rename v2dlengage soccons_polch_vdem
rename v2dlengage_codelow soccons_polch_vdem_low
rename v2dlengage_codehigh soccons_polch_vdem_high

rename v2x_egaldem egaldem_vdem
rename v2x_egaldem_codelow egaldem_vdem_low
rename v2x_egaldem_codehigh egaldem_vdem_high

rename v2x_egal egal_vdem
rename v2x_egal_codelow egal_vdem_low
rename v2x_egal_codehigh egal_vdem_high

rename v2xeg_eqprotec equal_rights_vdem
rename v2xeg_eqprotec_codelow equal_rights_vdem_low
rename v2xeg_eqprotec_codehigh equal_rights_vdem_high

rename v2xeg_eqaccess equal_access_vdem
rename v2xeg_eqaccess_codelow equal_access_vdem_low
rename v2xeg_eqaccess_codehigh equal_access_vdem_high

rename v2xeg_eqdr equal_res_vdem
rename v2xeg_eqdr_codelow equal_res_vdem_low
rename v2xeg_eqdr_codehigh equal_res_vdem_high

rename v2eltrnout turnout_vdem
rename e_wbgi_gee goveffective_vdem_wbgi


** Label variables of interest:
label variable electdem_dich_row_owid "Electoral democracy (RoW, OWID)"
label variable electdem_dich_high_row_owid "Electoral democracy (upper bound, RoW, OWID)"
label variable electdem_dich_low_row_owid "Electoral democracy (lower bound, RoW, OWID)"

label variable electfreefair_row "Free and fair elections (RoW)"
label variable electfreefair_high_row "Free and fair elections (upper bound, RoW)"
label variable electfreefair_low_row "Free and fair elections (lower bound, RoW)"

label variable electmulpar_row "Multiparty elections (RoW)"
label variable electmulpar_high_row "Multiparty elections (upper bound, RoW)"
label variable electmulpar_low_row "Multiparty elections (lower bound, RoW)"

label variable lib_dich_row "Liberal political institutions (RoW)"
label variable lib_dich_high_row "Liberal political institutions (upper bound, RoW)"
label variable lib_dich_low_row "Liberal political institutions (lower bound, RoW)"

label variable accessjust_m_row "Access to justice for men (RoW)"
label variable accessjust_m_high_row "Access to justice for men (upper bound, RoW)"
label variable accessjust_m_low_row "Access to justice for men (lower bound, RoW)"

label variable accessjust_w_row "Access to justice for women (RoW)"
label variable accessjust_w_high_row "Access to justice for women (upper bound, RoW)"
label variable accessjust_w_low_row "Access to justice for women (lower bound, RoW)"

label variable transplaws_row "Transparent laws (RoW)"
label variable transplaws_high_row "Transparent laws (upper bound, RoW)"
label variable transplaws_low_row "Transparent laws (lower bound, RoW)"

label variable electmulpar_hoe_row_owid "Multiparty elections for chief executive (RoW, OWID)"
label variable electmulpar_hoe_high_row_owid "Multiparty elections for chief executive (upper bound, RoW, OWID)"
label variable electmulpar_hoe_low_row_owid "Multiparty elections for chief executive (lower bound, RoW, OWID)"

label variable electmulpar_leg_row "Multiparty elections for legislature (RoW)"
label variable electmulpar_leg_high_row "Multiparty elections for legislature (upper bound, RoW)"
label variable electmulpar_leg_low_row "Multiparty elections for legislature (lower bound, RoW)"

label variable electdem_vdem "Electoral democracy (V-Dem)"
label variable electdem_vdem_low "Electoral democracy (lower bound, V-Dem)"
label variable electdem_vdem_high "Electoral democracy (upper bound, V-Dem)"

label variable electfreefair_vdem "Free and fair elections (V-Dem, OWID)"
label variable electfreefair_vdem_low "Free and fair elections (lower bound, V-Dem)"
label variable electfreefair_vdem_high "Free and fair elections (upper bound, V-Dem)"

label variable suffr_vdem "Share of adults with suffrage (V-Dem)"

label variable electoff_vdem "Elected officials (V-Dem)"

label variable freeexpr_vdem "Freedom of expression and alternative sources of information (V-Dem)"
label variable freeexpr_vdem_low "Freedom of expression and alternative sources of information (lower bound, V-Dem)"
label variable freeexpr_vdem_high "Freedom of expression and alternative sources of information (upper bound, V-Dem)"

label variable freeassoc_vdem "Freedom of association (V-Dem)"
label variable freeassoc_vdem_low "Freedom of association (lower bound, V-Dem)"
label variable freeassoc_vdem_high "Freedom of association (upper bound, V-Dem)"

label variable libdem_vdem "Liberal democracy (V-Dem)"
label variable libdem_vdem_low "Liberal democracy (lower bound, V-Dem)"
label variable libdem_vdem_high "Liberal democracy (upper bound, V-Dem)"

label variable lib_vdem "Liberal political institutions (V-Dem)"
label variable lib_vdem_low "Liberal political institutions (lower bound, V-Dem)"
label variable lib_vdem_high "Liberal political institutions (upper bound, V-Dem)"

label variable civlib_vdem "Civil liberties (V-Dem)"
label variable civlib_vdem_low "Civil liberties (lower bound, V-Dem)"
label variable civlib_vdem_high "Civil liberties (upper bound, V-Dem)"

label variable judicial_constr_vdem "Judicial constraints on the executive (V-Dem)"
label variable judicial_constr_vdem_low "Judicial constraints on the executive (lower bound, V-Dem)"
label variable judicial_constr_vdem_high  "Judicial constraints on the executive (upper bound, V-Dem)"

label variable legis_constr_vdem "Legislative constraints on the executive (V-Dem)"
label variable legis_constr_vdem_low "Legislative constraints on the executive (lower bound, V-Dem)"
label variable legis_constr_vdem_high "Legislative constraints on the executive (upper bound, V-Dem)"

label variable participdem_vdem "Participatory democracy (V-Dem)"
label variable participdem_vdem_low "Participatory democracy (lower bound, V-Dem)"
label variable participdem_vdem_high "Participatory democracy (upper bound, V-Dem)"

label variable particip_vdem "Participatory political institutions (V-Dem)"
label variable particip_vdem_low "Participatory political institutions (lower bound, V-Dem)"
label variable particip_vdem_high "Participatory political institutions (upper bound, V-Dem)"

label variable civsoc_particip_vdem "Civil society participation (V-Dem)"
label variable civsoc_particip_vdem_low "Civil society participation (lower bound, V-Dem)"
label variable civsoc_particip_vdem_high "Civil society participation (upper bound, V-Dem)"

label variable dirpop_vote_vdem "Extent of direct popular votes (V-Dem)"

label variable locelect_vdem "Elected local governments (V-Dem)"
label variable locelect_vdem_low "Elected local governments (lower bound, V-Dem)"
label variable locelect_vdem_high "Elected local governments (upper bound, V-Dem)"

label variable regelect_vdem "Elected regional governments (V-Dem)"
label variable regelect_vdem_low "Elected regional governments (lower bound, V-Dem)"
label variable regelect_vdem_high "Elected regional governments (upper bound, V-Dem)"

label variable egaldem_vdem "Egalitarian democracy (V-Dem)"
label variable egaldem_vdem_low "Egalitarian democracy (lower bound, V-Dem)"
label variable egaldem_vdem_high "Egalitarian democracy (upper bound, V-Dem)"

label variable egal_vdem "Egalitarian political institutions (V-Dem)"
label variable egal_vdem_low "Egalitarian political institutions (lower bound, V-Dem)"
label variable egal_vdem_high "Egalitarian political institutions (upper bound, V-Dem)"

label variable equal_rights_vdem "Equal rights protection (V-Dem)"
label variable equal_rights_vdem_low "Equal rights protection (lower bound, V-Dem)"
label variable equal_rights_vdem_high "Equal rights protection (upper bound, V-Dem)"

label variable equal_access_vdem "Equal access to power (V-Dem)"
label variable equal_access_vdem_low "Equal access to power (lower bound, V-Dem)"
label variable equal_access_vdem_high "Equal access to power (upper bound, V-Dem)"

label variable equal_res_vdem "Equal resource distribution (V-Dem)"
label variable equal_res_vdem_low "Equal resource distribution (lower bound, V-Dem)"
label variable equal_res_vdem_high "Equal resource distribution (upper bound, V-Dem)"

label variable delibdem_vdem "Deliberative democracy (V-Dem)"
label variable delibdem_vdem_low "Deliberative democracy (lower bound, V-Dem)"
label variable delibdem_vdem_high "Deliberative democracy (upper bound, V-Dem)"

label variable delib_vdem "Deliberative political institutions (V-Dem)"
label variable delib_vdem_low "Deliberative political institutions (lower bound, V-Dem)"
label variable delib_vdem_high "Deliberative political institutions (upper bound, V-Dem)"

label variable justified_polch_vdem "Justified political positions (V-Dem)"
label variable justified_polch_vdem_low "Justified political positions (lower bound, V-Dem)"
label variable justified_polch_vdem_high "Justified political positions (upper bound, V-Dem)"

label variable justcomgd_polch_vdem "Common good justifications (V-Dem)"
label variable justcomgd_polch_vdem_low "Common good justifications (lower bound, V-Dem)"
label variable justcomgd_polch_vdem_high "Common good justifications (upper bound, V-Dem)"

label variable counterarg_polch_vdem "Respect for counterarguments (V-Dem)"
label variable counterarg_polch_vdem_low "Respect for counterarguments (lower bound, V-Dem)"
label variable counterarg_polch_vdem_high "Respect for counterarguments (upper bound, V-Dem)"

label variable elitecons_polch_vdem "Elite consultation (V-Dem)"
label variable elitecons_polch_vdem_low "Elite consultation  (lower bound, V-Dem)"
label variable elitecons_polch_vdem_high "Elite consultation  (upper bound, V-Dem)"

label variable soccons_polch_vdem "Engaged society (V-Dem)"
label variable soccons_polch_vdem_low "Engaged society (lower bound, V-Dem)"
label variable soccons_polch_vdem_high "Engaged society (upper bound, V-Dem)"


label variable turnout_vdem "Voter turnout (V-Dem)"
label variable goveffective_vdem_wbgi "Government effectiveness (World Bank Governance Indicators, V-Dem)"


** Refine variables of interest:
replace country_name = "Myanmar" if country_name == "Burma/Myanmar"
replace country_name = "Democratic Republic of Congo" if country_name == "Democratic Republic of the Congo"
replace country_name = "Cote d'Ivoire" if country_name == "Ivory Coast"
replace country_name = "Congo" if country_name == "Republic of the Congo"
replace country_name = "Gambia" if country_name == "The Gambia"
replace country_name = "Palestine" if country_name == "Palestine/British Mandate"
replace country_name = "Timor" if country_name == "Timor-Leste"
replace country_name = "United States" if country_name == "United States of America"
replace country_name = "Wuerttemburg" if country_name == "Würtemberg"
replace country_name = "Czechia" if country_name == "Czech Republic"
replace country_name = "East Germany" if country_name == "German Democratic Republic"
replace country_name = "Hesse Electoral" if country_name == "Hesse-Kassel"
replace country_name = "Hesse Grand Ducal" if country_name == "Hesse-Darmstadt"
replace country_name = "Yemen People's Republic" if country_name == "South Yemen"

replace suffr_vdem = suffr_vdem * 100


** Order variables and observations:
order country_name year regime_row_owid regime_amb_row_owid electmulpar*_row electmulpar_hoe*_row_owid electmulpar_leg*_row electfreefair*_row electdem_dich*_row_owid accessjust_m*_row accessjust_w*_row transplaws*_row lib_dich*_row
order justified_polch_vdem justified_polch_vdem_low justified_polch_vdem_high justcomgd_polch_vdem justcomgd_polch_vdem_low justcomgd_polch_vdem_high counterarg_polch_vdem counterarg_polch_vdem_low counterarg_polch_vdem_high elitecons_polch_vdem elitecons_polch_vdem_low elitecons_polch_vdem_high soccons_polch_vdem soccons_polch_vdem_low soccons_polch_vdem_high, after(delib_vdem_high)
order turnout_vdem, after(soccons_polch_vdem_high)

sort country_name year


** Export data:
save "democracy/datasets/cleaned/vdem_row_cleaned.dta", replace
export delimited "democracy/datasets/cleaned/vdem_row_cleaned.csv", replace



exit
