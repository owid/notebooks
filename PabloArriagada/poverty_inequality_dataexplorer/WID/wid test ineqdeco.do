use wid_pretax_992j_dist, replace

egen country_year = concat(country year)

drop if percentile=="p99p100"
drop if percentile=="p99.9p100"
drop if percentile=="p99.99p100"

gen weight = 0.00001
replace weight = 0.0001 if p < .9999
replace weight = 0.001 if p < .999
replace weight = 0.01 if p < .99

drop if average == .

qui levelsof country_year, local(countries)

qui gen gini = .
qui gen wgini = .
qui gen w2 = .
qui gen w1 = .
qui gen whalf = .
qui gen ede2 = .
qui gen ede1 = .
qui gen edehalf = .
qui gen a2 = .
qui gen a1 = .
qui gen ahalf = .
qui gen ge2 = .
qui gen ge1 = .
qui gen ge0 = .
qui gen gem1 = .
qui gen p75p50 = .
qui gen p25p50 = .
qui gen p10p50 = .
qui gen p90p50 = .
qui gen p75p25 = .
qui gen p90p10 = .
qui gen p95 = .
qui gen p90 = .
qui gen p75 = .
qui gen p50 = .
qui gen p25 = .
qui gen p10 = .
qui gen p5 = .
qui gen max = .
qui gen min = .
qui gen sumw = .
qui gen sd = .
qui gen Var = .
qui gen mean = .


foreach c in `countries' {
	
	qui ineqdeco average [aw = weight] if country_year=="`c'", welfare
	qui replace gini = r(gini) if country_year == "`c'"
	qui replace wgini = r(wgini) if country_year == "`c'"
	qui replace w2 = r(w2) if country_year == "`c'"
	qui replace w1 = r(w1) if country_year == "`c'"
	qui replace whalf = r(whalf) if country_year == "`c'"
	qui replace ede2 = r(ede2) if country_year == "`c'"
	qui replace ede1 = r(ede1) if country_year == "`c'"
	qui replace edehalf = r(edehalf) if country_year == "`c'"
	qui replace a2 = r(a2) if country_year == "`c'"
	qui replace a1 = r(a1) if country_year == "`c'"
	qui replace ahalf = r(ahalf) if country_year == "`c'"
	qui replace ge2 = r(ge2) if country_year == "`c'"
	qui replace ge1 = r(ge1) if country_year == "`c'"
	qui replace ge0 = r(ge0) if country_year == "`c'"
	qui replace gem1 = r(gem1) if country_year == "`c'"
	qui replace p75p50 = r(p75p50) if country_year == "`c'"
	qui replace p25p50 = r(p25p50) if country_year == "`c'"
	qui replace p10p50 = r(p10p50) if country_year == "`c'"
	qui replace p90p50 = r(p90p50) if country_year == "`c'"
	qui replace p75p25 = r(p75p25) if country_year == "`c'"
	qui replace p90p10 = r(p90p10) if country_year == "`c'"
	qui replace p95 = r(p95) if country_year == "`c'"
	qui replace p90 = r(p90) if country_year == "`c'"
	qui replace p75 = r(p75) if country_year == "`c'"
	qui replace p50 = r(p50) if country_year == "`c'"
	qui replace p25 = r(p25) if country_year == "`c'"
	qui replace p10 = r(p10) if country_year == "`c'"
	qui replace p5 = r(p5) if country_year == "`c'"
	qui replace max = r(max) if country_year == "`c'"
	qui replace min = r(min) if country_year == "`c'"
	qui replace sumw = r(sumw) if country_year == "`c'"
	qui replace sd = r(sd) if country_year == "`c'"
	qui replace Var = r(Var) if country_year == "`c'"
	qui replace mean = r(mean) if country_year == "`c'"

}
collapse (min) gini wgini w2 w1 whalf ede2 ede1 edehalf a2 a1 ahalf ge2 ge1 ge0 gem1 p75p50 p25p50 p10p50 p90p50 p75p25 p90p10 p95 p90 p75 p50 p25 p10 p5 max min sumw sd Var mean, by(country_year)


*qui ineqdec0 average [aw = weight] if country_year=="CL2016", welfare
*qui replace gini = r(gini) if country_year == "CL2016"

export delimited using "ineqvariables.csv", replace



