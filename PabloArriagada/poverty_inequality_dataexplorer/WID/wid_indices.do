*This is a code to get WID data for pre-tax and post-tax income inequality


*Gets ppp data to convert to USD
wid, indicators(xlcusp) year(2021) clear 
rename value ppp
tempfile ppp
save "`ppp'"

*Gets average and threshold income for pre tax and post tax (national and disposable) data
wid, indicators(aptinc tptinc adiinc tdiinc acainc tcainc) perc(p0p10 p10p20 p20p30 p30p40 p40p50 p50p60 p60p70 p70p80 p80p90 p90p100 p0p100 p99p100) ages(992) pop(j) clear

*Merge with ppp data to transform monetary values to USD
merge n:1 country using "`ppp'", keep(match)
replace value = value/ppp
drop ppp
drop _merge
tempfile avgthr
save "`avgthr'"

*Gets shares and Gini for pre and post tax income
wid, indicators(sptinc gptinc sdiinc gdiinc scainc gcainc) perc(p0p10 p10p20 p20p30 p30p40 p40p50 p50p60 p60p70 p70p80 p80p90 p90p100 p0p100 p0p40 p0p50 p50p90 p99p100) ages(992) pop(j) clear

*Union with average and threshold income
append using "`avgthr'"

egen varp = concat(percentile variable), punct(_)
egen couy = concat(country year), punct(+)

drop variable percentile country year

reshape wide value, j(varp) i(couy) string

split couy, p(+) destring

rename couy1 country
rename couy2 year

drop couy


rename value* *
rename *sptinc* *share_pretax
rename *gptinc* *gini_pretax
rename *aptinc* *avg_pretax
rename *tptinc* *thr_pretax
rename *sdiinc* *share_posttax_national
rename *gdiinc* *gini_posttax_national
rename *adiinc* *avg_posttax_national
rename *tdiinc* *thr_posttax_national
rename *scainc* *share_posttax_disposable
rename *gcainc* *gini_posttax_disposable
rename *acainc* *avg_posttax_disposable
rename *tcainc* *thr_posttax_disposable


drop p0p100_share*
drop p0p100_thr*


order country year p0p100*gini_pretax p0p100*gini*disposable p0p100*gini*national *share_pretax *share*disposable *share*national *avg_pretax *avg*disposable *avg*national *thr_pretax *thr*disposable *thr*national

export excel using "wid_indices.xlsx", firstrow(variables) replace
save wid_indices, replace
