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
1. Poverty and inequality metrics (mean, gini, relative poverty)
2. Percentile thresholds and shares
3. Additional inequality metrics (generalized entropy, Atkinson)
*/
global menu_option = 1

*Select if the code extracts income (1) or consumption (0)
global income = 1

*Select if the code extracts equivalized (1) or per capita (0) aggregation
global equivalized = 1

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
	quietly replace miss_comp=1 if dhi==. | dhci==. | hifactor==. | hiprivate==. | hi33==. | hcexp==.
	quietly drop if miss_comp==1
	gen mi = hifactor + hiprivate + hi33
	foreach var in dhi dhci mi hcexp {
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

* Gets the data
foreach ccyy in `countries' {
	quietly use dhi dhci hifactor hiprivate hi33 hcexp hwgt hpopwgt nhhmem grossnet iso2 year using $`ccyy'h, clear
	*Merge with PPP data to get deflator
	if "$ppp_values" == "1" {
		quietly merge n:1 iso2 year using "`ppp'", keep(match) nogenerate keepusing(lisppp)
	}
	quietly make_variables
	* Option 1 is to get poverty and inequality variables
	if "$menu_option" == "1" {
		foreach var in dhi dhci mi hcexp {
			*Identify observations below (relative) poverty lines
			quietly gen byte poor_40_`var'=(e`var'_b<$povline_40)
			quietly gen byte poor_50_`var'=(e`var'_b<$povline_50)
			quietly gen byte poor_60_`var'=(e`var'_b<$povline_60)
			*Calculate and store gini for equivalized income
			quietly ineqdec0 e`var'_b [w=hwgt*nhhmem]
			local gini_`var' : di %9.3f r(gini)
			
			*Get mean income
			local mean_`var': di r(mean)
			
			*Calculate the proportion of individuals in poverty
			quietly sum poor_40_`var' [w=hwgt*nhhmem]
			local povrate_40_`var' : di %9.2f r(mean)*100
			quietly sum poor_50_`var' [w=hwgt*nhhmem]
			local povrate_50_`var' : di %9.2f r(mean)*100
			quietly sum poor_60_`var' [w=hwgt*nhhmem]
			local povrate_60_`var' : di %9.2f r(mean)*100
		}
		*Print dataset header
		if "`ccyy'" == "`first_country'" di "dataset,pop,mean_dhi,mean_dhci,mean_mi,mean_hcexp,gini_dhi,gini_dhci,gini_mi,gini_hcexp,povrate_40_dhi,povrate_50_dhi,povrate_60_dhi,povrate_40_dhci,povrate_50_dhci,povrate_60_dhci,povrate_40_mi,povrate_50_mi,povrate_60_mi,povrate_40_hcexp,povrate_50_hcexp,povrate_60_hcexp"
		*Print poverty and inequality estimates for each country, year and income
		di "`ccyy',$pop,`mean_dhi',`mean_dhci',`mean_mi',`mean_hcexp',`gini_dhi',`gini_dhci',`gini_mi',`gini_hcexp',`povrate_40_dhi',`povrate_50_dhi',`povrate_60_dhi',`povrate_40_dhci',`povrate_50_dhci',`povrate_60_dhci',`povrate_40_mi',`povrate_50_mi',`povrate_60_mi',`povrate_40_hcexp',`povrate_50_hcexp',`povrate_60_hcexp'"
	}
	* Option 2 is to get the percentiles and shares of the income distribution
	else if "$menu_option" == "2" {
		foreach var in $perc_vars {
			*Estimate percentile shares
			qui sumdist e`var'_b [w=hwgt*nhhmem], ngp(10)
			*Print dataset header
			if "`ccyy'" == "`first_country'" di "dataset,variable,percentile,thr,share"
			*Print percentile thresholds and shares for each country, year, and income
			forvalues j = 1/10 {
				local thr`j': di %16.2f r(q`j')
				local s`j': di %9.4f r(sh`j')*100
				di "`ccyy',`var',`j',`thr`j'',`s`j''"
			}
		}
	}
	* Option 3 is to get additional inequality variables
	else if "$menu_option" == "3" {
		foreach var in dhi dhci mi {
			*Calculate inequality metrics (ineqdec0 only estimates ge2, indeqdeco calculates them all)
			quietly ineqdeco e`var'_b [w=hwgt*nhhmem]
			
			*Get generalized entropy inequality index
			local gem1_`var': di %9.3f r(gem1)
			local ge0_`var': di %9.3f r(ge0)
			local ge1_`var': di %9.3f r(ge1)
			local ge2_`var': di %9.3f r(ge2)
			
			*Get Atkinson inequality index
			local ahalf_`var': di %9.3f r(ahalf)
			local a1_`var': di %9.3f r(a1)
			local a2_`var': di %9.3f r(a2)
		}
		*Print dataset header
		if "`ccyy'" == "`first_country'" di "dataset,gem1_dhi,gem1_dhci,gem1_mi,ge0_dhi,ge0_dhci,ge0_mi,ge1_dhi,ge1_dhci,ge1_mi,ge2_dhi,ge2_dhci,ge2_mi,ahalf_dhi,ahalf_dhci,ahalf_mi,a1_dhi,a1_dhci,a1_mi,a2_dhi,a2_dhci,a2_mi"
		*Print inequality estimates for each country, year and income
		di "`ccyy',`gem1_dhi',`gem1_dhci',`gem1_mi',`ge0_dhi',`ge0_dhci',`ge0_mi',`ge1_dhi',`ge1_dhci',`ge1_mi',`ge2_dhi',`ge2_dhci',`ge2_mi',`ahalf_dhi',`ahalf_dhci',`ahalf_mi',`a1_dhi',`a1_dhci',`a1_mi',`a2_dhi',`a2_dhci',`a2_mi'"
	}
	
	* Option 4 is to get additional poverty variables
	else if "$menu_option" == "4" {
		foreach var in dhi dhci mi {
			forvalues pct = 40(10)60 {
				*Calculate poverty metrics (ineqdec0 only estimates ge2, indeqdeco calculates them all)
				quietly povdeco e`var'_b [w=hwgt*nhhmem], pline(${povline_`pct'})
				
				*fgt0 is headcount ratio
				*local fgt0_`var'_`pct': di %9.2f r(fgt0)
				local fgt1_`var'_`pct': di %9.2f r(fgt1) *100
				local fgt2_`var'_`pct': di %9.4f r(fgt2)
				
				local meanpoor_`var'_`pct': di %9.2f r(meanpoor)
				local meangappoor_`var'_`pct': di %9.2f r(meangappoor)
			}
			
			*quietly poverty e`var'_b [w=hwgt*nhhmem], line($povline_40)
			
			/*
			Saved Results
			-------------

				S_1  = total number of observations in the data
				S_2  = number of observations used to compute the indices
				S_3  = weighted number of observations
				S_4  = value of the poverty line
				S_5  = weighted number of observations identified as poor

			(the following results are only available if the measure has been requested)
				S_6  = headcount ratio [FGT(0)]     
				S_7  = aggregate poverty gap
				S_8  = poverty gap ratio [FGT(1)]
				S_9  = income gap ratio 
				S_10 = Watts index
				S_11 = FGT(0.5)
				S_12 = FGT(1.5)
				S_13 = FGT(2)
				S_14 = FGT(2.5)
				S_15 = FGT(3)
				S_16 = FGT(3.5)
				S_17 = FGT(4)
				S_18 = FGT(4.5)
				S_19 = FGT(5)
				S_20 = Clark et al. index (0.10)
				S_21 = Clark et al. index (0.25)
				S_22 = Clark et al. index (0.5)
				S_23 = Clark et al. index (0.75)
				S_24 = Clark et al. index (0.90)
				S_25 = Sen index
				S_26 = Thon index
				S_27 = Takayama index

			
			*/
		}
		*Print dataset header
		if "`ccyy'" == "`first_country'" di "dataset,fgt1_dhi_40,fgt1_dhci_40,fgt1_mi_40,fgt1_dhi_50,fgt1_dhci_50,fgt1_mi_50,fgt1_dhi_60,fgt1_dhci_60,fgt1_mi_60,fgt2_dhi_40,fgt2_dhci_40,fgt2_mi_40,fgt2_dhi_50,fgt2_dhci_50,fgt2_mi_50,fgt2_dhi_60,fgt2_dhci_60,fgt2_mi_60,meanpoor_dhi_40,meanpoor_dhci_40,meanpoor_mi_40,meanpoor_dhi_50,meanpoor_dhci_50,meanpoor_mi_50,meanpoor_dhi_60,meanpoor_dhci_60,meanpoor_mi_60,meangappoor_dhi_40,meangappoor_dhci_40,meangappoor_mi_40,meangappoor_dhi_50,meangappoor_dhci_50,meangappoor_mi_50,meangappoor_dhi_60,meangappoor_dhci_60,meangappoor_mi_60"
		*Print inequality estimates for each country, year and income
		di "`ccyy',`fgt1_dhi_40',`fgt1_dhci_40',`fgt1_mi_40',`fgt1_dhi_50',`fgt1_dhci_50',`fgt1_mi_50',`fgt1_dhi_60',`fgt1_dhci_60',`fgt1_mi_60',`fgt2_dhi_40',`fgt2_dhci_40',`fgt2_mi_40',`fgt2_dhi_50',`fgt2_dhci_50',`fgt2_mi_50',`fgt2_dhi_60',`fgt2_dhci_60',`fgt2_mi_60',`meanpoor_dhi_40',`meanpoor_dhci_40',`meanpoor_mi_40',`meanpoor_dhi_50',`meanpoor_dhci_50',`meanpoor_mi_50',`meanpoor_dhi_60',`meanpoor_dhci_60',`meanpoor_mi_60',`meangappoor_dhi_40',`meangappoor_dhci_40',`meangappoor_mi_40',`meangappoor_dhi_50',`meangappoor_dhci_50',`meangappoor_mi_50',`meangappoor_dhi_60',`meangappoor_dhci_60',`meangappoor_mi_60'"
	}
}
