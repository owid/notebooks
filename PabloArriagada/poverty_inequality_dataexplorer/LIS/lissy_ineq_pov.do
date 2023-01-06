/*
LIS COMMANDS FOR OUR WORLD IN DATA
This program calculates poverty and inequality estimates and percentiles for three incomes:
dhi: Disposable household income, which is toal income minus taxes and social security contributions
dhci: Disposable household cash income, which is dhi minus the total value of goods and services (fringe benefits, home production, in-kind benefits and transfers)
mi: Market income, the sum of factor income (labor plus capital income), private income (private cash transfers and in-kind goods and services, not involving govt) and private pensions
*/

*
/* SETTINGS
----------------------------------------------------------------------------------------------------------- 
Select data to extract:
1. Poverty and inequality metrics
2. Percentiles
*/
global menu_option = 1

*Select the income variable to get percentiles (dhi, dhci, mi). menu_option has to be 2 to extract data
global perc_vars dhi

*Select the dataset to extract. "all" for the entire LIS data, "test" for test data, small [from(2015) to(2020) iso2(cl uk)]
global dataset = "all"

*Select if values should be converted to PPPs (1 = yes, 0 = no) and the PPP version (2017 or 2011)
global ppp_values = 1
global ppp_year = 2017

*-------------------------------------------------------------------------------------------------------------


program define make_variables
	gen miss_comp = 0
	quietly replace miss_comp=1 if dhi==. | dhci==. | hifactor==. | hiprivate==. | hi33==.
	quietly drop if miss_comp==1
	gen mi = hifactor + hiprivate + hi33
	foreach var in dhi dhci mi {
		gen e`var'_b = `var'
		replace e`var'_b = 0 if `var'<0
		* Apply top and bottom codes / outlier detection
		gen e`var'_log=log(e`var'_b)
		* keep negatives and 0 in the overall distribution of non-missing dhi
		replace e`var'_log=0 if e`var'_log==. & e`var'_b!=.
		* detect interquartile range
		cap drop iqr
		cap drop upper_bound
		cap drop lower_bound
		qui sum e`var'_log [w=hwgt],de
		gen iqr=r(p75)-r(p25)
		* detect upper bound for extreme values
		gen upper_bound=r(p75) + (iqr * 3)
		gen lower_bound=r(p25) - (iqr * 3)
		* top code income at upper bound for extreme values
		replace e`var'_b=exp(upper_bound) if e`var'_b>exp(upper_bound)
		* bottom code income at lower bound for extreme values
		replace e`var'_b=exp(lower_bound) if e`var'_b<exp(lower_bound)
		replace e`var'_b = (e`var'_b/(nhhmem^0.5))
	}
	quietly sum edhi_b [w=hwgt*nhhmem], de
	*Why edhi_b and not e`var'_b???
	*LIS methodology always uses (equivalized) household disposable income for the relative poverty line
	global povline_40 = r(p50)*0.4
	global povline_50 = r(p50)*0.5
	global povline_60 = r(p50)*0.6
end

*Use PPP data
if "$ppp_values" == "1" {
	use $myincl/ppp_$ppp_year.dta
	tempfile ppp
	save "`ppp'"
}

*Selects the entire dataset or a small one for testing
if "$dataset" == "all" {
	qui lissydata, lis
}
else if "$dataset" == "test" {
qui lissydata, lis from(2015) to(2020) iso2(cl uk)
}

/*Trying ways to incorporate PPP deflator (from WID code)

*Merge with ppp data have
merge n:1 country using "`ppp'", keep(match)
replace value = value/ppp
drop ppp
drop _merge
tempfile avgthr
save "`avgthr'"

*Union with average and threshold income
append using "`avgthr'"

*/

* Gets countries and the first country in the group
local countries "${selected}"
local first_country : word 1 of `countries'

* Option 1 is to get poverty and inequality variables
if "$menu_option" == "1" {
	foreach ccyy in `countries' {
		quietly use dhi dhci hifactor hiprivate hi33 hwgt nhhmem grossnet using $`ccyy'h, clear
		quietly make_variables
		foreach var in dhi dhci mi {
			*Identify observations below (relative) poverty lines
			quietly gen byte poor_40_`var'=(e`var'_b<$povline_40)
			quietly gen byte poor_50_`var'=(e`var'_b<$povline_50)
			quietly gen byte poor_60_`var'=(e`var'_b<$povline_60)
			*Calculate and store gini for equivalized income
			quietly ineqdec0 e`var'_b [w=hwgt*nhhmem]
			local gini_`var' : di %9.3f r(gini)
			
			*Calculate the proportion of individuals in poverty
			quietly sum poor_40_`var' [w=hwgt*nhhmem]
			local povrate_40_`var' : di %9.2f r(mean)*100
			quietly sum poor_50_`var' [w=hwgt*nhhmem]
			local povrate_50_`var' : di %9.2f r(mean)*100
			quietly sum poor_60_`var' [w=hwgt*nhhmem]
			local povrate_60_`var' : di %9.2f r(mean)*100
		}
	*Print dataset header
	if "`ccyy'" == "`first_country'" di "dataset,gini_dhi,gini_dhci,gini_mi,povrate_40_dhi,povrate_50_dhi,povrate_60_dhi,povrate_40_dhci,povrate_50_dhci,povrate_60_dhci,povrate_40_mi,povrate_50_mi,povrate_60_mi"
	*Print poverty and inequality estimates for each country, year and income
	di "`ccyy',`gini_dhi',`gini_dhci',`gini_mi',`povrate_40_dhi',`povrate_50_dhi',`povrate_60_dhi',`povrate_40_dhci',`povrate_50_dhci',`povrate_60_dhci',`povrate_40_mi',`povrate_50_mi',`povrate_60_mi'"
	}
}

* Option 2 is to get the percentiles of each income distribution
else if "$menu_option" == "2" {
	foreach ccyy in `countries' {
		quietly use dhi dhci hifactor hiprivate hi33 hwgt nhhmem grossnet using $`ccyy'h, clear
		quietly make_variables
		foreach var in $perc_vars {
			*Estimate all the percentiles
			_pctile e`var'_b [aw=hwgt*nhhmem], nq(100)
			*Print dataset header
			if "`ccyy'" == "`first_country'" di "dataset,variable,percentile,value"
			*Print percentiles for each country, year, and income
			forvalues j = 1/99 {
				local p`j' = r(r`j')
				di "`ccyy',`var',`j',`p`j''"
			}
		}
	}
}
