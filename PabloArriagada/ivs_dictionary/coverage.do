/*
COVERAGE OF IVS BY WAVE
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

keep country year

* Define waves
global ivs_waves "1981-1984" "1989-1993" "1994-1998" "1999-2004" "2005-2010" "2010-2014" "2017-2022"

preserve


duplicates drop
	
collapse (count) country, by (year)
	

* Export as csv
export delimited using "coverage.csv", datafmt replace
