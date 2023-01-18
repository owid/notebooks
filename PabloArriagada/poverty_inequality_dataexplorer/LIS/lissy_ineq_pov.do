/*
LIS COMMANDS FOR OUR WORLD IN DATA
This program calculates poverty and inequality estimates and percentiles for three incomes:
dhi: Disposable household income, which is total income minus taxes and social security contributions
dhci: Disposable household cash income, which is dhi minus the total value of goods and services (fringe benefits, home production, in-kind benefits and transfers)
mi: Market income, the sum of factor income (labor plus capital income), private income (private cash transfers and in-kind goods and services, not involving goverment) and private pensions
*/

*
/* SETTINGS
----------------------------------------------------------------------------------------------------------- 
Select data to extract:
1. Population, mean, median, gini and relative poverty variables
2. Absolute poverty variables
3. Decile thresholds and shares

*/
global menu_option = 1

*Select if the code extracts income (1) or consumption (0)
global income = 1

*Select if the code extracts equivalized (1) or per capita (0) aggregation
global equivalized = 1

*Select the variables to extract
global inc_cons_vars dhi dhci mi hcexp

*Select the dataset to extract. "all" for the entire LIS data, "test" for test data, small [from(2015) to(2020) iso2(cl uk)]
global dataset = "all"

*Select if values should be converted to PPPs (1 = yes, 0 = no) and the PPP version (2017 or 2011)
global ppp_values = 1
global ppp_year = 2017

*Define absolute poverty lines (cents)
global abs_povlines 100 215 365 685 1000 2000 3000 4000

*Set the maximum character limit per line
set linesize 255

*-------------------------------------------------------------------------------------------------------------

program define make_variables
	gen miss_comp = 0
	quietly replace miss_comp=1 if dhi==. | dhci==. | hifactor==. | hiprivate==. | hi33==. | hcexp==.
	quietly drop if miss_comp==1
	gen mi = hifactor + hiprivate + hi33
	foreach var in dhi dhci mi hcexp {
	
		quietly sum `var'
		local max_`var' = r(max)
		
		if `max_`var'' > 0 {
			*Use raw income variable
			gen e`var'_b = `var'
			
			if "$ppp_values" == "1" {
				*Convert variable into int-$ at ppp_year prices
				replace e`var'_b = e`var'_b / lisppp
			}
			
			*Replace negative values for zeros
			replace e`var'_b = 0 if `var'<0
			* Apply top and bottom codes / outlier detection
			gen e`var'_log=log(e`var'_b)
			* keep negatives and 0 in the overall distribution of non-missing income
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
			
			* If equivalization is selected, the household income is divided by the LIS equivalence scale (squared root of the number of household members)
			if "$equivalized" == "1" {
				replace e`var'_b = (e`var'_b/(nhhmem^0.5))
			}
			
			*If equivalization is not selected, the household income is divided by the number of household members
			else if "$equivalized" == "0" {
				replace e`var'_b = (e`var'_b/(nhhmem))
			}
		}
		
		else {
		
		gen e`var'_b = .
		
		}
	}
	quietly sum edhi_b [w=hwgt*nhhmem], de
	*Why edhi_b and not e`var'_b???
	*LIS methodology always uses (equivalized) household disposable income for the relative poverty line
	global povline_40 = r(p50)*0.4
	global povline_50 = r(p50)*0.5
	global povline_60 = r(p50)*0.6
	
	*Get total population
	quietly sum nhhmem [w=hpopwgt]
	global pop: di %10.0f r(sum)
end

*Use PPP data
if "$ppp_values" == "1" {
	use $myincl/ppp_$ppp_year.dta
	
	tempfile ppp
	save "`ppp'"
}

*Define program to convert to PPP, to use in multiple instances and because some datasets do not have deflator (se76, tw)
program define convert_ppp
	if iso2 != "tw" | (iso2 != "se" & year == 1967)
		quietly merge n:1 iso2 year using "`ppp'", keep(match) nogenerate keepusing(lisppp)
		foreach var in $inc_cons_vars {
			replace e`var'_b = e`var'_b / lisppp
		}
	}
	else
		foreach var in $inc_cons_vars {
			replace e`var'_b = .
		}
end

*Selects the entire dataset or a small one for testing
if "$dataset" == "all" {
	qui lissydata, lis
}
else if "$dataset" == "test" {
qui lissydata, lis from(2015) to(2020) iso2(cl uk)
}

* Gets countries and the first country in the group
local countries "${selected}"
local first_country : word 1 of `countries'

*Gets first income/consumption variable in inc_cons_vars
local first_inc_cons : word 1 of $inc_cons_vars

* Gets the data
foreach ccyy in `countries' {
	quietly use dhi dhci hifactor hiprivate hi33 hcexp hwgt hpopwgt nhhmem grossnet iso2 year using $`ccyy'h, clear
	*Merge with PPP data to get deflator
	if "$ppp_values" == "1" {
		quietly merge n:1 iso2 year using "`ppp'", keep(match) nogenerate keepusing(lisppp)
	}
	quietly make_variables
	
	* Option 1 is to get population, mean, median, gini and relative poverty variables
	if "$menu_option" == "1" {
		foreach var in $inc_cons_vars {
			
			quietly sum e`var'_b
			local n_`var' = r(N)
			
			if `n_`var'' > 0 {
			
				*For 40, 50, 60 (% of median)
				forvalues pct = 40(10)60 {
					*Calculate poverty metrics
					quietly povdeco e`var'_b [w=hwgt*nhhmem], pline(${povline_`pct'})
					
					*fgt0 is headcount ratio
					local fgt0_`var'_`pct': di %9.2f r(fgt0) *100
					local fgt1_`var'_`pct': di %9.2f r(fgt1) *100
					local fgt2_`var'_`pct': di %9.4f r(fgt2)
					
					local meanpoor_`var'_`pct': di %9.2f r(meanpoor)
					local meangap_`var'_`pct': di %9.2f r(meangappoor)
				}
				
				*Calculate and store gini for equivalized income
				quietly ineqdec0 e`var'_b [w=hwgt*nhhmem]
				local gini_`var' : di %9.3f r(gini)
				
				*Get mean and median income
				local mean_`var': di %9.2f r(mean)
				local median_`var': di %9.2f r(p50)
			}
			
			else {
				
				*For 40, 50, 60 (% of median)
				forvalues pct = 40(10)60 {
					
					*fgt0 is headcount ratio
					local fgt0_`var'_`pct' = .
					local fgt1_`var'_`pct' = .
					local fgt2_`var'_`pct' = .
					
					local meanpoor_`var'_`pct' = .
					local meangap_`var'_`pct' = .
				}
				
				local gini_`var' = .
				
				*Get mean and median income
				local mean_`var' = .
				local median_`var' = .
			}

			*Print dataset header
			if "`ccyy'" == "`first_country'" & "`var'" == "`first_inc_cons'" di "dataset,variable,eq,pop,mean,median,gini,fgt0_40,fgt0_50,fgt0_60,fgt1_40,fgt1_50,fgt1_60,fgt2_40,fgt2_50,fgt2_60,meanpoor_40,meanpoor_50,meanpoor_60,meangap_40,meangap_50,meangap_60"
			*Print percentile thresholds and shares for each country, year, and income
			di "`ccyy',`var',$equivalized,$pop,`mean_`var'',`median_`var'',`gini_`var'',`fgt0_`var'_40',`fgt0_`var'_50',`fgt0_`var'_60',`fgt1_`var'_40',`fgt1_`var'_50',`fgt1_`var'_60',`fgt2_`var'_40',`fgt2_`var'_50',`fgt2_`var'_60',`meanpoor_`var'_40',`meanpoor_`var'_50',`meanpoor_`var'_60',`meangap_`var'_40',`meangap_`var'_50',`meangap_`var'_60'"
		}
	}
	
	* Option 2 is to get absolute poverty variables
	else if "$menu_option" == "2" {
		foreach var in $inc_cons_vars {
			
			quietly sum e`var'_b
			local n_`var' = r(N)
			
			foreach pline in $abs_povlines {
			
				if `n_`var'' > 0 {
			
					*Calculate poverty metrics
					local pline_year = `pline'/100*365
					quietly povdeco e`var'_b [w=hwgt*nhhmem], pline(`pline_year')
					
					*fgt0 is headcount ratio
					local fgt0_`var'_`pline': di %9.2f r(fgt0) *100
					local fgt1_`var'_`pline': di %9.2f r(fgt1) *100
					local fgt2_`var'_`pline': di %9.4f r(fgt2)
					
					local meanpoor_`var'_`pline': di %9.2f r(meanpoor)
					local meangap_`var'_`pline': di %9.2f r(meangappoor)
				}
				
				else {
				
					local fgt0_`var'_`pline' = .
					local fgt1_`var'_`pline' = .
					local fgt2_`var'_`pline' = .
					
					local meanpoor_`var'_`pline' = .
					local meangap_`var'_`pline' = .
				
				}
				
				*Print dataset header
				if "`ccyy'" == "`first_country'" & "`var'" == "`first_inc_cons'" di "dataset,variable,eq,povline,fgt0,fgt1,fgt2,meanpoor,meangap"
				*Print percentile thresholds and shares for each country, year, and income
				di "`ccyy',`var',$equivalized,`pline',`fgt0_`var'_`pline'',`fgt1_`var'_`pline'',`fgt2_`var'_`pline'',`meanpoor_`var'_`pline'',`meangap_`var'_`pline''"
				
			}
		}
	}

	* Option 3 is to get the deciles thresholds and shares of the income distribution
	else if "$menu_option" == "3" {
		foreach var in $inc_cons_vars {
		
			quietly sum e`var'_b
			local n_`var' = r(N)
			
			*Print dataset header
			if "`ccyy'" == "`first_country'" & "`var'" == "`first_inc_cons'" di "dataset,variable,eq,percentile,thr,share"
			
			if `n_`var'' > 0 {
			
				*Estimate percentile shares
				qui sumdist e`var'_b [w=hwgt*nhhmem], ngp(10)
				*Print percentile thresholds and shares for each country, year, and income
				forvalues j = 1/10 {
					local thr`j': di %16.2f r(q`j')
					local s`j': di %9.4f r(sh`j')*100
					di "`ccyy',`var',$equivalized,`j',`thr`j'',`s`j''"
				}
			}
			
			else {
			
				*Print percentile thresholds and shares for each country, year, and income
				forvalues j = 1/10 {
					local thr`j' = .
					local s`j' = .
					di "`ccyy',`var',$equivalized,`j',`thr`j'',`s`j''"
				}
			
			}
		}
	}
}
