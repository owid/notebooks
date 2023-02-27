qui lissydata, lis

local countries "${selected}"
di "`countries'"
di "${selected}"

use $myincl/ppp_2017.dta, clear
sum

*Create yy variable, a year variable with two digits
gen yy = year
tostring yy, replace
replace yy = substr(yy,-2,.)

*Combine iso2 and yy to create ccyy, a country-year variable as the one identifying datasets
egen ccyy = concat(iso2 yy)

*Get distinct values of ccyy and call it countries_with_ppp
qui levelsof ccyy, local(countries_with_ppp) clean

*Define an empty countries_without_ppp global macro
global countries_without_ppp

*Check countries in the income datasets not in PPP dataset
foreach c in `countries' {
	if !strpos("`countries_with_ppp'", "`c'") {
		global countries_without_ppp $countries_without_ppp `c'
	}
}

di "$countries_without_ppp"
