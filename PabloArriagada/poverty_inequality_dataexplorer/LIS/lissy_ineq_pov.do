program define make_variables
	gen miss_comp = 0
	quietly replace miss_comp=1 if dhci==. | dhci==. | hitotal==.
	quietly drop if miss_comp==1
	*sum dhi [w=hwgt], de
	foreach var in dhi dhci hitotal {
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
	global povline_40 = r(p50)*0.4
	global povline_50 = r(p50)*0.5
	global povline_60 = r(p50)*0.6
end

qui lissydata, lis
*qui lissydata, lis from(1980) to(2020)
*qui lissydata, lis from(1980) to(2020) iso2(cl uk)
*qui lissydata, lis from(2015) to(2020) iso2(cl uk)
local countries "${selected}"

foreach ccyy in `countries' {
	quietly use dhi dhci hitotal hwgt nhhmem grossnet using $`ccyy'h, clear
	quietly make_variables
	foreach var in dhi dhci hitotal {
		quietly gen byte poor_40_`var'=(e`var'_b<$povline_40)
		quietly gen byte poor_50_`var'=(e`var'_b<$povline_50)
		quietly gen byte poor_60_`var'=(e`var'_b<$povline_60)
		*Calculate and store gini, relative poverty rate
		quietly ineqdec0 e`var'_b [w=hwgt*nhhmem]
		local gini_`var' : di %9.3f r(gini)
		quietly sum poor_40_`var' [w=hwgt*nhhmem]
		local povrate_40_`var' : di %9.2f r(mean)*100
		quietly sum poor_50_`var' [w=hwgt*nhhmem]
		local povrate_50_`var' : di %9.2f r(mean)*100
		quietly sum poor_60_`var' [w=hwgt*nhhmem]
		local povrate_60_`var' : di %9.2f r(mean)*100
	}
/*Output gini and poverty rate measures as comma separated values. If this is the first country being computed, output a line of column headers first. */
if "`ccyy'" == "at87" di "dataset,gini_dhi,gini_dhci,gini_hitotal,povrate_40_dhi,povrate_50_dhi,povrate_60_dhi,povrate_40_dhci,povrate_50_dhci,povrate_60_dhci,povrate_40_hitotal,povrate_50_hitotal,povrate_60_hitotal"
di "`ccyy',`gini_dhi',`gini_dhci',`gini_hitotal',`povrate_40_dhi',`povrate_50_dhi',`povrate_60_dhi',`povrate_40_dhci',`povrate_50_dhci',`povrate_60_dhci',`povrate_40_hitotal',`povrate_50_hitotal',`povrate_60_hitotal'"
}
