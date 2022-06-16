*This is a code to get WID data to compare pretax data with different filters
*Trying i, j, t and e for population unit
*Trying 992, 996 and 999 as ages groups

set more off

*Gets ppp data to convert to USD
wid, indicators(xlcusp) year(2017) clear 
rename value ppp
tempfile ppp
save "`ppp'"

*Gets average and threshold income for pre tax and post tax (nat and dis) data
wid, indicators(aptinc tptinc) perc(p0p10 p10p20 p20p30 p30p40 p40p50 p50p60 p60p70 p70p80 p80p90 p90p100 p0p100 p99p100 p99.9p100 p99.99p100 p99.999p100) ages(999) pop(e) exclude clear

*Merge with ppp data to transform monetary values to USD
merge n:1 country using "`ppp'", keep(match)
replace value = value/ppp
drop ppp
drop _merge
tempfile avgthr
save "`avgthr'"

*Gets shares and Gini for pre and post tax income
wid, indicators(sptinc gptinc) perc(p0p10 p10p20 p20p30 p30p40 p40p50 p50p60 p60p70 p70p80 p80p90 p90p100 p0p100 p0p40 p0p50 p50p90 p99p100 p99.9p100 p99.99p100 p99.999p100) ages(999) pop(e) exclude clear

*Union with average and threshold income
append using "`avgthr'"

egen varp = concat(percentile variable), punct(_)
egen couy = concat(country year), punct(+)

drop variable percentile country year

replace varp = subinstr(varp, ".", "_", .) 

reshape wide value, j(varp) i(couy) string

split couy, p(+) destring

rename couy1 country
rename couy2 year

drop couy


rename value* *
rename *_s* *_share
rename *_g* *_gini
rename *_a* *_average
rename *_t* *_threshold

drop p0p100_share*
drop p0p100_thr*

order country year *gini* *share* *threshold* *average*

sort country year

export delimited using "pretax_999e.csv", replace
