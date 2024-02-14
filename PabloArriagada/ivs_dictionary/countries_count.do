/*
COUNTRIES AVAILABLE PER VARIABLE IN INTEGRATED VALUES SURVEY

*/


use Integrated_values_surveys_1981-2021, clear

* Create a string variable called year
decode S002VS, generate(year)

* Replace wave ID with last year of survey
replace year = "1981-1984" if S002VS==1
replace year = "1989-1993" if S002VS==2
replace year = "1994-1998" if S002VS==3 // No EVS
replace year = "1999-2004" if S002VS==4
replace year = "2005-2010" if S002VS==5
replace year = "2010-2014" if S002VS==6 // No EVS
replace year = "2017-2022" if S002VS==7

* There are several S002VS missing (only in EVS), so they are replaced according to the year of survey of EVS
* Note I am not following the same assignment as in the main dataset, because I care about the waves more than different country-year data (see UK 2021 and 2022, for example)
replace year = "1981-1984" if S002VS==. & S002EVS==1
replace year = "1989-1993" if S002VS==. & S002EVS==2
replace year = "1999-2004" if S002VS==. & S002EVS==3
replace year = "2005-2010" if S002VS==. & S002EVS==4
replace year = "2017-2022" if S002VS==. & S002EVS==5

rename S003 country

preserve

local variables_to_use A001 A002 A003 A004

foreach var of varlist _all {
// foreach var in `variables_to_use' {
	drop if missing(`var')
	keep country year
	duplicates drop
	
	collapse (count) country, by (year)
	
	rename country count
	gen var = "`var'"
	
	tempfile `var'_file
	save "``var'_file'"
	
	restore
	preserve
}

ds
local all_vars `r(varlist)'

* Get first var in the group
local first_var : word 1 of `all_vars'
local to_merge: subinstr local all_vars "`first_var'" ""

// local first_var : word 1 of `variables_to_use'
// local to_merge: subinstr local variables_to_use "`first_var'" ""

use ``first_var'_file', clear

foreach var in `to_merge' {
	append using "``var'_file'"
}

* Export as csv
export delimited using "countries_count.csv", datafmt replace


