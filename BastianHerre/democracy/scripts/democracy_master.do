*****  This Stata do-file creates the democracy data used in Our World in Data (OWID)'s Democracy Data Explorer, as well as in many charts and several articles across our site.
*****  Author: Bastian Herre
*****  June 28, 2022


** Set your working directory here:
cd "/Users/bastianherre/Dropbox/Data/"
global project "/Users/bastianherre/Dropbox/Data/"


** Clean datasets:
do "democracy/scripts/vdem_row_clean"
do "democracy/scripts/lied_clean.do"
do "democracy/scripts/bmr_clean.do"
do "democracy/scripts/polity_clean.do"
do "democracy/scripts/fh_clean.do"
do "democracy/scripts/bti_clean.do"
do "democracy/scripts/eiu_clean.do"


** Impute datasets:
do "democracy/scripts/owid_entities_expand"
do "democracy/scripts/vdem_row_impute"
do "democracy/scripts/bmr_impute"


** Refine datasets:
do "democracy/scripts/vdem_row_refine"
do "democracy/scripts/lied_refine"
do "democracy/scripts/bmr_refine"
do "democracy/scripts/polity_refine"


** Aggregate datasets:
do "democracy/scripts/owid_population_clean.do"
do "democracy/scripts/vdem_row_aggregate.do"
do "democracy/scripts/lied_aggregate.do"
do "democracy/scripts/lied_aggregate.do"
do "democracy/scripts/polity_aggregate.do"
do "democracy/scripts/fh_aggregate.do"
do "democracy/scripts/bti_aggregate.do"
do "democracy/scripts/eiu_aggregate.do"


exit
