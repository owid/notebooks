
subject : loop test



lissydata, lis from(1980) to(2020)
local ccyy "${selected}"

foreach c in `ccyy' {
	dis "`c'" as text

	qui cap lissyuse, lis ccyy(`c') hvars(did hid hwgt nhhmem dhi)

	* select only records if dhi filled
	qui drop if dhi==. 

	***Bottom and top coding / outlier detection***
	* create disposable household income in logs 
	qui gen dhi_log=log(dhi)
	* keep negatives and 0 in the overall distribution of non-missing dhi
	qui replace dhi_log=0 if dhi_log==. & dhi!=. 
	* detect interquartile range
	qui sum dhi_log [w=hwgt],de
	qui gen iqr=r(p75)-r(p25)
	* detect upper bound for extreme values
	qui gen upper_bound=r(p75) + (iqr * 3)
	qui gen lower_bound=r(p25) - (iqr * 3)
	* top code income at upper bound for extreme values
	qui replace dhi=exp(upper_bound) if dhi>exp(upper_bound) 
	* bottom code income at lower bound for extreme values
	qui replace dhi=exp(lower_bound) if dhi<exp(lower_bound) 

	* create equivalised income, set equivalence scale as square root of household members
	qui generate ey=(dhi/(nhhmem^0.5))

	* create person weight as hwgt times number of household members
	qui generate pwt=hwgt*nhhmem

	_pctile ey [aw=pwt], nq(100)
	dis r(r1)
}
