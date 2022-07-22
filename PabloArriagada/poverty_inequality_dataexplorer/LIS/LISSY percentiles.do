program define make_variables
gen miss_comp = 0
quietly replace miss_comp=1 if dhi==. | hifactor==. | hi33==. | hpub_i==. | hpub_u==. | hpub_a==. | hiprivate==. | hxitsc==.
quietly drop if miss_comp==1
sum dhi [w=hwgt], de
*gen mi = hifactor + hiprivate + hi33
*gen siti = hifactor + hiprivate + hi33 + hpub_i + hpub_u - hxitsc
*gen sa = hifactor + hiprivate + hi33 + hpub_a
foreach var in dhi {
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
*global povline = r(p50)*0.5
end

qui lissydata, lis from(1980) to(2020)
*qui lissydata, lis from(1980) to(2020) iso2(cl uk)
*qui lissydata, lis from(2015) to(2020) iso2(cl uk)
local countries "${selected}"

foreach ccyy in `countries' {
	quietly use dhi hifactor hi33 hpublic hpub_a hpub_i hpub_u hiprivate hxitsc hwgt nhhmem grossnet using $`ccyy'h, clear
	quietly make_variables
	foreach var in dhi {
		*quietly gen byte poor`var'=(e`var'_b<$povline)
		*Calculate and store gini, relative poverty rate
		*quietly ineqdec0 e`var'_b [w=hwgt*nhhmem]
		*local gini`var' : di %9.3f r(gini)
		*quietly sum poor`var' [w=hwgt*nhhmem]
		*local povrate`var' : di %9.2f r(mean)*100
		_pctile e`var'_b [aw=hwgt*nhhmem], nq(100)
		forvalues j = 1/100 {
			local p`j' = r(r`j')
		}
	}
/*Output gini and poverty rate measures as comma separated values. If this is the first country being computed, output a line of column headers first. */
if "`ccyy'" == "at87" di "dataset,p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16, p17, p18, p19, p20, p21, p22, p23, p24, p25, p26, p27, p28, p29, p30, p31, p32, p33, p34, p35, p36, p37, p38, p39, p40, p41, p42, p43, p44, p45, p46, p47, p48, p49, p50, p51, p52, p53, p54, p55, p56, p57, p58, p59, p60, p61, p62, p63, p64, p65, p66, p67, p68, p69, p70, p71, p72, p73, p74, p75, p76, p77, p78, p79, p80, p81, p82, p83, p84, p85, p86, p87, p88, p89, p90, p91, p92, p93, p94, p95, p96, p97, p98, p99, p100"
di "`ccyy',`p1',`p2',`p3',`p4',`p5',`p6',`p7',`p8',`p9',`p10',`p11',`p12',`p13',`p14',`p15',`p16',`p17',`p18',`p19',`p20',`p21',`p22',`p23',`p24',`p25',`p26',`p27',`p28',`p29',`p30',`p31',`p32',`p33',`p34',`p35',`p36',`p37',`p38',`p39',`p40',`p41',`p42',`p43',`p44',`p45',`p46',`p47',`p48',`p49',`p50',`p51',`p52',`p53',`p54',`p55',`p56',`p57',`p58',`p59',`p60',`p61',`p62',`p63',`p64',`p65',`p66',`p67',`p68',`p69',`p70',`p71',`p72',`p73',`p74',`p75',`p76',`p77',`p78',`p79',`p80',`p81',`p82',`p83',`p84',`p85',`p86',`p87',`p88',`p89',`p90',`p91',`p92',`p93',`p94',`p95',`p96',`p97',`p98',`p99',`p100'"
}
