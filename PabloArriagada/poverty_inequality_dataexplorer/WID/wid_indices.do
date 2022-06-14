*This is a code to get WID data for pre-tax and post-tax income inequality

set more off

*Gets ppp data to convert to USD
wid, indicators(xlcusp) year(2021) clear 
rename value ppp
tempfile ppp
save "`ppp'"

*Gets average and threshold income for pre tax and post tax (nat and dis) data
wid, indicators(aptinc tptinc adiinc tdiinc acainc tcainc) perc(p0p10 p10p20 p20p30 p30p40 p40p50 p50p60 p60p70 p70p80 p80p90 p90p100 p0p100 p99p100 p99.9p100 p99.99p100 p99.999p100) ages(992) pop(j) clear

*Merge with ppp data to transform monetary values to USD
merge n:1 country using "`ppp'", keep(match)
replace value = value/ppp
drop ppp
drop _merge
tempfile avgthr
save "`avgthr'"

*Gets shares and Gini for pre and post tax income
wid, indicators(sptinc gptinc sdiinc gdiinc scainc gcainc) perc(p0p10 p10p20 p20p30 p30p40 p40p50 p50p60 p60p70 p70p80 p80p90 p90p100 p0p100 p0p40 p0p50 p50p90 p99p100 p99.9p100 p99.99p100 p99.999p100) ages(992) pop(j) clear

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
rename *sptinc* *share_pretax
rename *gptinc* *gini_pretax
rename *aptinc* *avg_pretax
rename *tptinc* *thr_pretax
rename *sdiinc* *share_posttax_nat
rename *gdiinc* *gini_posttax_nat
rename *adiinc* *avg_posttax_nat
rename *tdiinc* *thr_posttax_nat
rename *scainc* *share_posttax_dis
rename *gcainc* *gini_posttax_dis
rename *acainc* *avg_posttax_dis
rename *tcainc* *thr_posttax_dis


drop p0p100_share*
drop p0p100_thr*

gen palma_ratio_pretax = p90p100_share_pretax / p0p40_share_pretax
*As there is not p0p40 share for posttax:
gen palma_ratio_posttax_nat = p90p100_share_posttax_nat / (p0p50_share_posttax_nat - p40p50_share_posttax_nat) 
gen palma_ratio_posttax_dis = p90p100_share_posttax_dis / (p0p50_share_posttax_dis - p40p50_share_posttax_dis)

gen s90_s10_ratio_pretax = p90p100_share_pretax / p0p10_share_pretax
gen s90_s10_ratio_posttax_nat = p90p100_share_posttax_nat / p0p10_share_posttax_nat
gen s90_s10_ratio_posttax_dis = p90p100_share_posttax_dis / p0p10_share_posttax_dis

gen s80_s20_ratio_pretax = (p80p90_share_pretax + p90p100_share_pretax) / (p0p10_share_pretax + p10p20_share_pretax)
gen s80_s20_ratio_posttax_nat = (p80p90_share_posttax_nat + p90p100_share_posttax_nat) / (p0p10_share_posttax_nat + p10p20_share_posttax_nat)
gen s80_s20_ratio_posttax_dis = (p80p90_share_posttax_dis + p90p100_share_posttax_dis) / (p0p10_share_posttax_dis + p10p20_share_posttax_dis)

gen s90_s50_ratio_pretax = p90p100_share_pretax / p0p50_share_pretax
gen s90_s50_ratio_posttax_nat = p90p100_share_posttax_nat / p0p50_share_posttax_nat
gen s90_s50_ratio_posttax_dis = p90p100_share_posttax_dis / p0p50_share_posttax_dis

gen p90_p10_ratio_pretax = p90p100_thr_pretax / p10p20_thr_pretax
gen p90_p10_ratio_posttax_nat = p90p100_thr_posttax_nat / p10p20_thr_posttax_nat
gen p90_p10_ratio_posttax_dis = p90p100_thr_posttax_dis / p10p20_thr_posttax_dis

gen p90_p50_ratio_pretax = p90p100_thr_pretax / p50p60_thr_pretax
gen p90_p50_ratio_posttax_nat = p90p100_thr_posttax_nat / p50p60_thr_posttax_nat
gen p90_p50_ratio_posttax_dis = p90p100_thr_posttax_dis / p50p60_thr_posttax_dis



order country year *gini_pretax *gini*dis *gini*nat *_ratio*pretax *_ratio*dis *_ratio*nat *share_pretax *share*dis *share*nat *avg_pretax *avg*dis *avg*nat *thr_pretax *thr*dis *thr*nat

export excel using "wid_indices.xlsx", firstrow(variables) replace
save wid_indices, replace
