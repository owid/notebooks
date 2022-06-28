*****  This Stata do-file cleans the Freedom-in-the-World (2022) dataset:
*****  Author: Bastian Herre
*****  June 28, 2022


version 14

clear all
set more off
set varabbrev off


** Set your own working directories here to run the file:
cd "/Users/bastianherre/Dropbox/Data/"
global project "/Users/bastianherre/Dropbox/Data/"


** Download dataset from https://freedomhouse.org/sites/default/files/2022-03/Country_and_Territory_Ratings_and_Statuses_FIW_1973-2022%20.xlsx and move it into the folder "Freedom in the World 2022":


** Import Freedom House territory dataset:
import excel "Freedom in the World 2022/Country_and_Territory_Ratings_and_Statuses_FIW_1973-2022 .xlsx", sheet("Territory Ratings, Statuses")

** Drop rows that are not observations:
drop in 1/3


** Give variables meaning- and useful names:
rename A country_name
label variable country_name "Country name"

rename B y1972_pr
rename C y1972_cl
rename D y1972_st
rename E y1973_pr
rename F y1973_cl
rename G y1973_st
rename H y1974_pr
rename I y1974_cl
rename J y1974_st
rename K y1975_pr
rename L y1975_cl
rename M y1975_st
rename N y1976_pr
rename O y1976_cl
rename P y1976_st
rename Q y1977_pr
rename R y1977_cl
rename S y1977_st
rename T y1978_pr
rename U y1978_cl
rename V y1978_st
rename W y1979_pr
rename X y1979_cl
rename Y y1979_st
rename Z y1980_pr
rename AA y1980_cl
rename AB y1980_st
rename AC y1982_pr // Consider January 1981 to August 1982 as 1982. Set tolerance in charts to 1.
rename AD y1982_cl
rename AE y1982_st
rename AF y1983_pr // Consider August 1982 to November 1983 as 1983.
rename AG y1983_cl
rename AH y1983_st
rename AI y1984_pr
rename AJ y1984_cl
rename AK y1984_st
rename AL y1985_pr
rename AM y1985_cl
rename AN y1985_st
rename AO y1986_pr
rename AP y1986_cl
rename AQ y1986_st
rename AR y1987_pr
rename AS y1987_cl
rename AT y1987_st
rename AU y1988_pr
rename AV y1988_cl
rename AW y1988_st
rename AX y1989_pr
rename AY y1989_cl
rename AZ y1989_st
rename BA y1990_pr
rename BB y1990_cl
rename BC y1990_st
rename BD y1991_pr
rename BE y1991_cl
rename BF y1991_st
rename BG y1992_pr
rename BH y1992_cl
rename BI y1992_st
rename BJ y1993_pr
rename BK y1993_cl
rename BL y1993_st
rename BM y1994_pr
rename BN y1994_cl
rename BO y1994_st
rename BP y1995_pr
rename BQ y1995_cl
rename BR y1995_st
rename BS y1996_pr
rename BT y1996_cl
rename BU y1996_st
rename BV y1997_pr
rename BW y1997_cl
rename BX y1997_st
rename BY y1998_pr
rename BZ y1998_cl
rename CA y1998_st
rename CB y1999_pr
rename CC y1999_cl
rename CD y1999_st
rename CE y2000_pr
rename CF y2000_cl
rename CG y2000_st
rename CH y2001_pr
rename CI y2001_cl
rename CJ y2001_st
rename CK y2002_pr
rename CL y2002_cl
rename CM y2002_st
rename CN y2003_pr
rename CO y2003_cl
rename CP y2003_st
rename CQ y2004_pr
rename CR y2004_cl
rename CS y2004_st
rename CT y2005_pr
rename CU y2005_cl
rename CV y2005_st
rename CW y2006_pr
rename CX y2006_cl
rename CY y2006_st
rename CZ y2007_pr
rename DA y2007_cl
rename DB y2007_st
rename DC y2008_pr
rename DD y2008_cl
rename DE y2008_st
rename DF y2009_pr
rename DG y2009_cl
rename DH y2009_st
rename DI y2010_pr
rename DJ y2010_cl
rename DK y2010_st
rename DL y2011_pr
rename DM y2011_cl
rename DN y2011_st
rename DO y2012_pr
rename DP y2012_cl
rename DQ y2012_st
rename DR y2013_pr
rename DS y2013_cl
rename DT y2013_st
rename DU y2014_pr
rename DV y2014_cl
rename DW y2014_st
rename DX y2015_pr
rename DY y2015_cl
rename DZ y2015_st
rename EA y2016_pr
rename EB y2016_cl
rename EC y2016_st
rename ED y2017_pr
rename EE y2017_cl
rename EF y2017_st
rename EG y2018_pr
rename EH y2018_cl
rename EI y2018_st
rename EJ y2019_pr
rename EK y2019_cl
rename EL y2019_st
rename EM y2020_pr
rename EN y2020_cl
rename EO y2020_st
rename EP y2021_pr
rename EQ y2021_cl
rename ER y2021_st


** Generate variable indicating whether an entity is a country or not, i.e. a territory:
generate country_fh = 0


** Rename Kosovo to avoid duplicate with Kosovo in country dataset:
replace country_name = "Kosovo (territory)" if country_name == "Kosovo"


** Temporarily save dataset:
save "democracy/datasets/cleaned/fh_territories.dta", replace


** Import Freedom House country dataset:
import excel "Freedom in the World 2022/Country_and_Territory_Ratings_and_Statuses_FIW_1973-2022 .xlsx", sheet("Country Ratings, Statuses ") clear


** Drop rows that are not observations:
drop in 1/3


** Give variables meaning- and useful names:
rename A country_name
label variable country_name "Country name"

rename B y1972_pr
rename C y1972_cl
rename D y1972_st
rename E y1973_pr
rename F y1973_cl
rename G y1973_st
rename H y1974_pr
rename I y1974_cl
rename J y1974_st
rename K y1975_pr
rename L y1975_cl
rename M y1975_st
rename N y1976_pr
rename O y1976_cl
rename P y1976_st
rename Q y1977_pr
rename R y1977_cl
rename S y1977_st
rename T y1978_pr
rename U y1978_cl
rename V y1978_st
rename W y1979_pr
rename X y1979_cl
rename Y y1979_st
rename Z y1980_pr
rename AA y1980_cl
rename AB y1980_st
rename AC y1982_pr // Consider January 1981 to August 1982 as 1982. Set tolerance in charts to 1.
rename AD y1982_cl
rename AE y1982_st
rename AF y1983_pr // Consider August 1982 to November 1983 as 1983.
rename AG y1983_cl
rename AH y1983_st
rename AI y1984_pr
rename AJ y1984_cl
rename AK y1984_st
rename AL y1985_pr
rename AM y1985_cl
rename AN y1985_st
rename AO y1986_pr
rename AP y1986_cl
rename AQ y1986_st
rename AR y1987_pr
rename AS y1987_cl
rename AT y1987_st
rename AU y1988_pr
rename AV y1988_cl
rename AW y1988_st
rename AX y1989_pr
rename AY y1989_cl
rename AZ y1989_st
rename BA y1990_pr
rename BB y1990_cl
rename BC y1990_st
rename BD y1991_pr
rename BE y1991_cl
rename BF y1991_st
rename BG y1992_pr
rename BH y1992_cl
rename BI y1992_st
rename BJ y1993_pr
rename BK y1993_cl
rename BL y1993_st
rename BM y1994_pr
rename BN y1994_cl
rename BO y1994_st
rename BP y1995_pr
rename BQ y1995_cl
rename BR y1995_st
rename BS y1996_pr
rename BT y1996_cl
rename BU y1996_st
rename BV y1997_pr
rename BW y1997_cl
rename BX y1997_st
rename BY y1998_pr
rename BZ y1998_cl
rename CA y1998_st
rename CB y1999_pr
rename CC y1999_cl
rename CD y1999_st
rename CE y2000_pr
rename CF y2000_cl
rename CG y2000_st
rename CH y2001_pr
rename CI y2001_cl
rename CJ y2001_st
rename CK y2002_pr
rename CL y2002_cl
rename CM y2002_st
rename CN y2003_pr
rename CO y2003_cl
rename CP y2003_st
rename CQ y2004_pr
rename CR y2004_cl
rename CS y2004_st
rename CT y2005_pr
rename CU y2005_cl
rename CV y2005_st
rename CW y2006_pr
rename CX y2006_cl
rename CY y2006_st
rename CZ y2007_pr
rename DA y2007_cl
rename DB y2007_st
rename DC y2008_pr
rename DD y2008_cl
rename DE y2008_st
rename DF y2009_pr
rename DG y2009_cl
rename DH y2009_st
rename DI y2010_pr
rename DJ y2010_cl
rename DK y2010_st
rename DL y2011_pr
rename DM y2011_cl
rename DN y2011_st
rename DO y2012_pr
rename DP y2012_cl
rename DQ y2012_st
rename DR y2013_pr
rename DS y2013_cl
rename DT y2013_st
rename DU y2014_pr
rename DV y2014_cl
rename DW y2014_st
rename DX y2015_pr
rename DY y2015_cl
rename DZ y2015_st
rename EA y2016_pr
rename EB y2016_cl
rename EC y2016_st
rename ED y2017_pr
rename EE y2017_cl
rename EF y2017_st
rename EG y2018_pr
rename EH y2018_cl
rename EI y2018_st
rename EJ y2019_pr
rename EK y2019_cl
rename EL y2019_st
rename EM y2020_pr
rename EN y2020_cl
rename EO y2020_st
rename EP y2021_pr
rename EQ y2021_cl
rename ER y2021_st


** Keep variables and observations of interest:
keep country_name y*
keep if country_name != ""


** Generate variable indicating whether an entity is a country or not, i.e. a territory:
generate country_fh = 1
label variable country_fh "Entity considered a country by Freedom House"


** Append dataset with territories:
append using "democracy/datasets/cleaned/fh_territories.dta"
erase "democracy/datasets/cleaned/fh_territories.dta"

** Create dataset with country-year-category observations:
reshape long y, i(country_name) j(year_category) string
rename y score


** Create year and category variables:
split year_category, p("_")
rename year_category1 year
rename year_category2 category
drop year_category


** Format year variable:
destring year, replace
label variable year "Year"


** Create dataset with country-year observations:
reshape wide score, i(country_name year) j(category) string


** Format variables:
rename scorecl civlibs_fh
rename scorepr polrights_fh
rename scorest regime_fh

order country_name year regime_fh polrights_fh civlibs_fh

label variable regime_fh "Political regime (Freedom House)"
label variable polrights_fh "Political rights rating (Freedom House)"
label variable civlibs_fh "Civil liberties rating (Freedom House)"

tab regime_fh
tab polrights_fh
tab civlibs_fh


** Replace scores for South Africa in 1972, where separate scores were given for white and black population, with the scores for the black population:
replace regime_fh = "NF" if regime_fh == "F (NF)"
replace polrights_fh = "5" if polrights_fh == "2(5)"
replace civlibs_fh = "6" if civlibs_fh == "3(6)"


** Reconcile Kosovo as territory with Kosovo as country:
drop if country_name == "Kosovo (territory)" & (year < 1993 | year > 2008)
drop if country_name == "Kosovo" & year > 1992 & year < 2009
replace country_name = "Kosovo" if country_name == "Kosovo (territory)"
sort country_name year


** Create numeric version of variables:
replace regime_fh = "0" if regime_fh == "NF"
replace regime_fh = "1" if regime_fh == "PF"
replace regime_fh = "2" if regime_fh == "F"
destring regime_fh, replace ignore("-")

label define regime_fh 0 "not free" 1 "partly free" 2 "free"
label values regime_fh regime_fh

destring polrights_fh, replace ignore("-")
destring civlibs_fh, replace ignore("-")


** Format country names:
replace country_name = "Cape Verde" if country_name == "Cabo Verde"


** Temporarily save dataset:
save "democracy/datasets/cleaned/fh.dta", replace


** Download dataset from https://freedomhouse.org/sites/default/files/2022-02/Aggregate_Category_and_Subcategory_Scores_FIW_2003-2022.xlsx and move it into the folder "Freedom in the World 2022":


** Import Freedom House subcategory dataset:
import excel "Freedom in the World 2022/Aggregate_Category_and_Subcategory_Scores_FIW_2003-2022.xlsx", sheet("FIW06-22") clear firstrow


** Recode edition year such that it becomes observation year:
replace Edition = Edition - 1
rename Edition year


** Rename and label variables of interest:
rename CountryTerritory country_name
rename A electprocess_fh
rename PR polrights_score_fh
rename CL civlibs_score_fh

label variable electprocess_fh "Electoral process (Freedom House)"
label variable polrights_score_fh "Political rights score (Freedom House)"
label variable civlibs_score_fh "Civil liberties score (Freedom House)"


** Keep variables of interest:
keep country_name year electprocess_fh polrights_score_fh civlibs_score_fh


** Create indicator for electoral democracy:
generate electdem_fh = 0 if electprocess_fh != . & polrights_score_fh != . & civlibs_score_fh != .
replace electdem_fh = 1 if electdem_fh == 0 & electprocess_fh >= 7 & polrights_score_fh >= 20 & civlibs_score_fh >= 30

label variable electdem_fh "Electoral democracy (Freedom House)"

order electdem_fh, after(year)


** Format country names:
replace country_name = "Cape Verde" if country_name == "Cabo Verde"
replace country_name = "Israeli-Occupied Territories" if country_name == "Israeli Occupied Territories"
replace country_name = "Palestinian Authority-Administered Territories" if country_name == "Palestinian Authority Administered Territories"
replace country_name = "North Macedonia" if country_name == "Macedonia"
replace country_name = "Eswatini" if country_name == "Swaziland"


** Merge with long-term dataset:
sort country_name year
merge 1:1 country_name year using "democracy/datasets/cleaned/fh.dta"
* Only unmatched observations in long-term dataset, as it should be.
drop _merge
erase "democracy/datasets/cleaned/fh.dta"

** Order variables:
order regime_fh polrights_fh civlibs_fh, after(year)


** Format country names:
replace country_name = "Congo" if country_name == "Congo (Brazzaville)"
replace country_name = "Democratic Republic of Congo" if country_name == "Congo (Kinshasa)"
replace country_name = "Czechia" if country_name == "Czech Republic"
replace country_name = "East Germany" if country_name == "Germany, E. " 
replace country_name = "Saint Kitts and Nevis" if country_name == "St. Kitts and Nevis"
replace country_name = "Saint Lucia" if country_name == "St. Lucia"
replace country_name = "Saint Vincent and the Grenadines" if country_name == "St. Vincent and the Grenadines"
replace country_name = "Republic of Vietnam" if country_name == "Vietnam, S."
replace country_name = "Yemen People's Republic" if country_name == "Yemen, S."
replace country_name = "North Vietnam" if country_name == "Vietnam, N."
replace country_name = "West Germany" if country_name == "Germany, W. "
replace country_name = "Yemen Arab Republic" if country_name == "Yemen, N."
replace country_name = "Micronesia (country)" if country_name == "Micronesia"
replace country_name = "Gambia" if country_name == "The Gambia"
replace country_name = "Timor" if country_name == "Timor-Leste"

sort country_name year




** Format country names and eliminate duplicate observations:
*** This could be considered imputation, and should perhaps be left for imputation do-file.


drop if country_name == "Yemen" & regime_fh == .
drop if country_name == "Germany" & regime_fh == .
drop if country_name == "Vietnam" & regime_fh == .


sort country_name


** Export datasets:
save "democracy/datasets/cleaned/fh_cleaned.dta", replace
export delimited "democracy/datasets/cleaned/fh_cleaned.csv", replace nolabel



exit
