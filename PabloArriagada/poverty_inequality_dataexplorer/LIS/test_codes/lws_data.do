//////////////////////////////////////////////////////////////////////////// 
//																 		  // 
//	This program computes distributional statistics from LWS and LIS	  // 
// 						Author: Ignacio Flores (2021)					  //
//																 		  // 
////////////////////////////////////////////////////////////////////////////

//Prepare command (execution at the end)
//////////////////////////////////////////////////////////////////
global execute ///
	ineqstats_lissy summarize, weight(hpopwgt) edad(0) ///
		ccyy() decomp(han haf has) liab(hln hlr) ///
		hvars(hpopwgt han haf has hln hlr) pvars(ppopwgt age) ///
		database(lws) //test 
//////////////////////////////////////////////////////////////////
	
//define program 
cap program drop ineqstats_lissy
program define ineqstats_lissy
	version 11 
	syntax name [, weight(string) EDad(real 0)  ///
		CCyy(string) BCKTavgs TEST LIABilities(string)] ///
		DEComp(string) HVARs(string) ///
		DATAbase(string) PVARs(string) 
		
	*-----------------------------------------------------------------------
	*PART 0: Check inputs
	*---------------------------------- -------------------------------------
	
	//Choice of database 
	if ("`database'" == "") {
		di as text "You must choose a database (LIS or LWS)"
		exit 1
	}
	if ("`database'" != "" & inlist("`database'", "lws", "lis")) {
		local database `database'
		local dname = upper("`database'")
		di as text "Extracting information from `dname' at $S_TIME"
	}
	
	//Weights
	if ("`weight'" == "") {
		local weight "ppopwgt"
		display as text "Weight: `weight' (default)"
	} 
	else {
		
	} 
	
	//Decomposition
	if ("`decomp'" != "") {
	}
	else{
		display as text "You must define total wealth/income components"
		exit 1
	}
	
	//Decompositions and extensions 
	foreach w in `decomp' `liabilities' {
		local decomp_working "`decomp_working' `w'"
	}
	
	*select countries 
	if ("`ccyy'") == "" & "`test'" == "" {
		lissydata, `database' from(1980) to(2020) 
		local ccyy "${selected}"
		di as text "ccyy() was left empty, retrieve all (default)"
	}

	if "`test'" == "test" {
		local ccyy xx17 zz98
	}
	*---------------------------------------------------------------------------
	*PART 1: Summary statistics 
	*---------------------------------------------------------------------------
	
	// Loopy over all country-years 
	foreach c in `ccyy' {
		
		//split country and year 
		local yr = substr("`c'", 3, 2)
		if `yr' < 50 local `c'year = `yr' + 2000
		if `yr' > 50 local `c'year = `yr' + 1900
		local `c'iso2 = upper(substr("`c'", 1, 2))
	
		// Open data
		clear
		
		*decide to open real or testing dataset
		if "`test'" == "" {
			qui cap lissyuse, ///
				`database' ccyy(`c') pvars(`pvars') hvars(`hvars')	
		}
		if "`test'" != "" {
			qui set obs 2000 
			foreach v in `pvars' `hvars' {
				qui gen `v' = runiform()
			}
			qui gen inum = 1 
		}
		if "`database'" == "lws" {
			qui keep if inum == 1
			if "`liabilities'" != "" {
				foreach v in `liabilities' {
					qui replace `v' = -`v'
				}
			}
		} 
	
		//continue only if file exists
		cap assert _N == 0
		if _rc != 0 {
			
			*check existence of variables independently (for debugging) 
			foreach var in `decomp_working' age `weight' {
				cap confirm variable `var', exact
				if _rc == 0 {
					*check if 
					sum `var', meanonly
					local m_`c'_`period'_`var' = r(mean) 
					if inlist("`m_`c'_`period'_`var''", ".", "0") {
						local misvar_`c'_`period' "`misvar_`c'_`period'' `var'"
					}
				}
				else di as text "  variable `var' not found"
			}
	
			//check all variables exist 
			cap confirm variable `decomp_working' age `weight', exact
			if (_rc == 0 /*& "`misvar_`c'_`period''" == ""*/) { 
			
				tempvar ftile ftile_clean freq F fy cumfy L d_eq ///
					p1 p2 bckt_size cum_weight wy freq_t10 F_t10 ///
					auxinc smooth_income bckt_pop
				
				// Keep adults only
				qui drop if age < `edad'
				
				*recast weight if necessary
				cap assert int(`weight') == `weight' 
				if _rc != 0 {
					di as text "weights contained decimals" _continue
					di as text ", integers now"
					qui replace `weight' = round(`weight')
				}
				
				// Get total income/wealth and average
				if ("`decomp_working'" != "") {
					//display as text "`decomp_working'"
					tempname inc_`c'_`period'
					qui egen `inc_`c'_`period'' = ///
						rowtotal(`decomp_working')
				}
				qui sum `inc_`c'_`period'' [w=`weight']
				local avg_main = r(mean)	
				
				//write cdf down 
				qui sum	`weight', meanonly
				local poptot = r(sum)
				sort `inc_`c'_`period''
				quietly	gen `freq' = `weight' / `poptot'
				quietly	gen `F' = sum(`freq'[_n - 1])
				
				//increase resolution of top 1%
				qui expand `weight' + 1 if `F' >= 0.99, gen(checker)
				qui keep if checker == 1 | `F' < 0.99
				qui replace `weight' = 1 if checker == 1
				qui sort `inc_`c'_`period''
				quietly	replace `freq' = `weight' / `poptot'
				quietly	replace `F' = sum(`freq'[_n - 1])	
			
				*check pop is the same now 
				qui sum `weight', meanonly
				local newpop = r(sum)
				assert `poptot' - `newpop' == 0 
					
				*Estimate gini
				quietly	gen `fy'= `freq' * `inc_`c'_`period''
				quietly	gen `cumfy' = sum(`fy')
				qui sum `cumfy', meanonly
				local cumfy_max = r(max)
				quietly	gen `L' = `cumfy' / `cumfy_max'
				qui gen `d_eq' = (`F' - `L') * `weight' / `poptot'
				qui sum	`d_eq', meanonly
				local d_eq_tot = r(sum)
				local gini = `d_eq_tot'*2
				
				// Classify obs in 127 g-percentiles
				cap qui egen `ftile' = cut(`F'), ///
					at(0(0.01)0.99 0.991(0.001)0.999 ///
					0.9991(0.0001)0.9999 0.99991(0.00001)0.99999 1)
				
				//keep going if only if it doesn't fail 
				if _rc == 0 {
					
					*fill last obs 
					qui replace `ftile' = 0.99999 if missing(`ftile')
					
					//gather info to check consistency 
					qui sum `inc_`c'_`period'' [w = `weight'], meanonly 
					local suminc = r(sum)	
					qui sum `inc_`c'_`period'' [w = `weight'] ///
						if `F' >= 0.99, meanonly 
					local top1_check_`c'_`period' = r(sum)/`suminc' * 100
				
					// Estimate top average 
					gsort -`F'
					qui gen `wy' = `inc_`c'_`period'' * `weight'
					cap drop topavg
					qui gen topavg = sum(`wy') / sum(`weight')
					
					*topaverages decomposition 
					foreach v in `decomp_working' {
						tempvar wy_`v'
						qui gen `wy_`v'' = `v' * `weight'
						qui gen topavg_`v' = ///
							sum(`wy_`v'') / sum(`weight')
					}
					sort `F'

					//composition 
					foreach v in `decomp_working' {
						//prepare lines bracket composition 
						local lst_coll`c'`period' "`lst_coll`c'`period'' bckt_avg_`v' = `v'"
					}
					
					//count adult population 
					qui sum `weight' if age >= `edad'
					local adpop_`c'_`period' = r(sum)
					
					
					// Collapse to 127 percentiles 
					qui collapse (min) thr = `inc_`c'_`period'' ///
						(mean) bckt_avg = `inc_`c'_`period'' ///
						`lst_coll`c'`period'' ///
						(max) bckt_max = `inc_`c'_`period'' ///
						(min) `ftile_clean' = `F' ///
						bckt_min = `inc_`c'_`period'' ///
						(sum) bckt_sum_tot = `inc_`c'_`period'' ///
						(rawsum) wgts = `weight' [w = `weight'], ///
						by (`ftile')
					
					*save for later 
					tempfile collapsed_form
					qui save `collapsed_form'	
					
					if _rc == 0 {
						
						// build 127 percentiles again from scratch
						clear
						qui set obs 127
						*qui set obs 100
						qui gen `ftile_clean' = (_n - 1)/100 in 1/100
						qui replace `ftile_clean' ///
							= (99 + (_n - 100)/10)/100 in 101/109
						qui replace `ftile_clean' ///
							= (99.9 + (_n - 109)/100)/100 in 110/118
						qui replace `ftile_clean' ///
							= (99.99 + (_n - 118)/1000)/100 in 119/127
							
						*append clean cuts 	
						qui append using `collapsed_form'
						qui gsort `ftile_clean' -`ftile'
						
						*put composition variables in percentages 
						foreach x in sex categ firm {
							foreach z in ``x'vars' {
								qui replace `z' = `z' / wgts 
							}
						}
					
						*interpolate data 
						qui ds bckt_max bckt_min wgts ///
							`ftile_clean' `ftile' , not 
						foreach var in `r(varlist)' {
							qui ipolate `var' `ftile_clean', ///
								gen(ip_`var') 
							qui drop `var'
								qui rename ip_`var' `var'	
						}	
						
						*keep clean cuts 
						qui keep if missing(`ftile')
						qui drop `ftile'
						qui rename `ftile_clean' `ftile'
						qui replace `ftile' = ///
							round(`ftile' * 100000)	
					
						*get bracket population shares 
						qui gsort -`ftile' 
						qui gen `bckt_pop' = `ftile'[_n-1] - `ftile' 
						qui replace `bckt_pop' = 1 ///
							if `ftile' == 99999	
						qui gen sum_pop = sum(`bckt_pop')	
						
						*make bracket averages consistent with totavg
						qui sum bckt_avg [w = `bckt_pop'], meanonly
						local ipol_avg = r(mean)
						qui replace bckt_avg = ///
							bckt_avg * `avg_main' / `ipol_avg'
						qui replace thr = ///
							thr * `avg_main' / `ipol_avg'	
						*di as text "ratio: " ///
						*	`avg_main' / `ipol_avg' * 100
				
						*gen vars to enforce consistency of composition
						tempvar tot_decomp ratio_decom 
						qui egen `tot_decomp' = rowtotal(bckt_avg_*)
						qui gen `ratio_decom' = ///
							bckt_avg / `tot_decomp'		
						
						*loop over variables
						qui ds thr bckt_sum_tot sum_pop __* ///
							`sexvars' `categvars' `firmvars' ///
							  wgts `ratio_decom', not 
						foreach v in `r(varlist)' {
							
							*enforce consistency of components 
							local ext2 = ///
								subinstr("`v'", "bckt_avg", "", .) 
							
							if !inlist("`v'", "bckt_avg") {
								qui replace `v' = `v' * `ratio_decom' ///
								if `ratio_decom' > 0 ///
								& !missing(`ratio_decom')
							}
							
							*compute top averages	
							qui gen fy`ext2' = `v' * `bckt_pop' 
							qui gen sum_fy`ext2' = sum(fy`ext2')
							qui gen topavg`ext2' = ///
								sum_fy`ext2' / sum_pop
							
							*get general average 
							qui sum topavg`ext2' if `ftile' == 0 
							local avg`ext2' = r(sum)
							
							*get top shares 
							qui gen topsh`ext2' ///
								= topavg`ext2' / `avg`ext2'' * ///
								(sum_pop / 100000 )
							assert topsh`ext2'[127] == 1 | ///
								missing(topsh`ext2'[127]) 
							*get bracket shares 
							qui gen s`ext2' = `v' / `avg`ext2'' * ///
								(`bckt_pop'  / 100000)
							qui sum s`ext2', meanonly 
							local xyz = r(sum)
							qui assert round(`xyz'*10^5) == 10^5 ///
								if "`xyz'" != "0"
							
						}	
							
						*go back to decimals 
						qui replace `ftile' = `ftile' / 100000
						qui replace `bckt_pop' = `bckt_pop' / 100000
						
						*sort 
						sort `ftile'
						qui gen ftile = `ftile'	
						
						*clean
						qui rename topsh topshare
						
						//What share of total income by item?
						foreach v in `decomp_working' {
							qui local sh_`v'_`c'_`period' = ///
								topavg_`v'[1] / topavg[1] 
						}
						
						// Total average  
						qui gen average = .
						qui replace average = `avg_main' in 1		
						
						// Inverted beta coefficient
						qui gen b = topavg/thr		
						
						// Fractile
						qui rename ftile p
						
						// Year
						qui gen ccyy = "`c'" in 1	
						
						// Write Gini
						qui gen gini = `gini' in 1
						
						if "`bcktavg'" != ""{
							local addvars bckt_sum_tot bckt_sum_*
						} 
						
						// Order and save	
						order ccyy gini average p thr ///
							bckt_avg s  topavg topshare b topavg_* ///
							topsh* `addvars' ///
							`sexvars' `categvars' `firmvars'
						
						keep ccyy gini average p thr ///
							bckt_avg s topavg topshare b ///
							topavg_* topsh* `addvars' ///
							`sexvars' `categvars' `firmvars'
						tempname mat_sum
						mkmat gini average p thr bckt_avg s topavg ///
							topshare b topavg_*, matrix(`mat_sum')
						mkmat gini average p thr bckt_avg s topavg ///
							topshare b topavg_*, matrix(_mat_sum)	
							
						//check consistency of all variables 
						assert bckt_avg >= thr	if bckt_avg > 0
						*assert ///
						*	round(average[1] / topavg[1] * 10^5) ==10^5
						qui sum s, meanonly 
						assert round(r(sum) * 10^5) == 10^5
						
						*di as text "country-sheet " _continue
						*di as text "`c' `period' saved at $S_TIME"
						
						//Fetch some summary stats for 1ry panel
						local b50_sh_`c'_`period' = 1 - topshare[51]
						local m40_sh_`c'_`period' = ///
							topshare[51] - topshare[91]
						local t10_sh_`c'_`period' = topshare[91]
						local t1_sh_`c'_`period' = topshare[100]
						local gini_`c'_`period' = gini[1]
						local average_`c'_`period' = average[1]
						
				
						if (abs(`t1_sh_`c'_`period'' * ///
							100-`top1_check_`c'_`period'') > 0.1) {
							di as text "top one should be " ///
								`top1_check_`c'_`period''
							di as text "top one is: " ///
								`t1_sh_`c'_`period'' * 100
							di as text "diff in ppts (`c'): " ///
								`t1_sh_`c'_`period''* ///
								100 - `top1_check_`c'_`period''
						}
						
						//Data for 2ry summary stats (composition)
						local it_test = 1 
						local it_test2 = 1 
						foreach v in `decomp_working' {
							local b50c_`v'_`c'`period' = ///
								(1 - topsh_`v'[51]) * ///
								`sh_`v'_`c'_`period'' ///
								/ `b50_sh_`c'_`period''
							local m40c_`v'_`c'`period' = ///
								(topsh_`v'[51] - topsh_`v'[91]) * ///
								 `sh_`v'_`c'_`period'' / ///
								`m40_sh_`c'_`period''
							local t10c_`v'_`c'`period' = ///
								topsh_`v'[91] * ///
								`sh_`v'_`c'_`period'' ///
								/ `t10_sh_`c'_`period''
							local t1c_`v'_`c'`period' = ///
								topsh_`v'[100] * ///
								`sh_`v'_`c'_`period'' ///
								/ `t1_sh_`c'_`period''
								
							if `it_test2' == 1 local test_tots2_`c'`period' `sh_`v'_`c'_`period''
							else local test_tots2_`c'`period' `test_tots2_`c'`period'' + `sh_`v'_`c'_`period''
							if `it_test2' == 1 local it_test2 = 0
							
							*check consistency (sum of components by group)
							foreach g in b50 m40 t10 t1 {
								if "``g'c_`v'_`c'`period''" != "." {
									if `it_test' == 1 local `g'test_`c'`period' ``g'c_`v'_`c'`period''	
									if `it_test' != 1 local `g'test_`c'`period' ``g'test_`c'`period'' + ``g'c_`v'_`c'`period''
									if `it_test' == 1 local it_test = 0 
								}
							}	
						}
					}		
					
					else {
						display as error "There was a problem with " _continue
						display as error "`c' `period' (skipped)"
					}
				
				}
				
				else {
					display as error "There was a problem with " _continue
					display as error "`c' `period' (skipped)"
				}
			}
			else {
				di as error "Missing variables " _continue 
				di as error "in `c' `period': skip" 
			}	
			if "`misvar_`c'_`period''" != "" {
				di as error "`c' `period' missing or empty variables: `misvar_`c'_`period''"
			}
		}
	}
	
	//Summarize main info for all countries
	clear
	local sumvars gini average adpop b50_sh m40_sh t10_sh t1_sh
	local compgrp tot b50 m40 t10 t1 
	local nobs = wordcount("`ccyy'") 
	local ncomp = wordcount("`compgrp'") * wordcount("`decomp_working'") * `nobs'
	local nvars = wordcount("`sumvars'") * `nobs'
	local nobs =  `nvars' + `ncomp'
	set obs `nobs'

	//Generate empty vars
	foreach v in country year variable value {
		if inlist("`v'", "country", "variable") qui gen `v' = ""
		if inlist("`v'", "year", "value")  qui gen `v' = .
	}
	
	//Fill primary variables
	local iter = 1 
	foreach c in `ccyy' {	
		foreach v in `sumvars' {
			if ("``v'_`c'_`period''" != "") {
				qui replace country = "``c'iso2'" in `iter'
				qui replace year = ``c'year' in `iter'
				qui replace variable = "`v'" in `iter'
				qui replace value = ``v'_`c'_`period'' in `iter'
			}
			local iter = `iter' + 1	
		}
	}
	
	//Fill composition variables 
	foreach c in `ccyy' {
		foreach group in `compgrp' {
			foreach v in `decomp_working' {
				if ("`sh_`v'_`c'_`period''" != "") {
					if "`group'" != "tot" local x ``group'c_`v'_`c'`period''
					if "`group'" == "tot" local x `sh_`v'_`c'_`period''
					qui replace country ="``c'iso2'" in `iter'
					qui replace year = ``c'year' in `iter'
					qui replace variable = "`group'_`v'" in `iter'
					qui replace value = `x' in `iter'	
					local iter = `iter' + 1	
				} 
			}
		}	
	}	
		
	//keep data points in memory 
	qui gen n = _n
	local vbls country year variable value 
	local N = _N
	forvalues n = 1/`N' {
		foreach v in `vbls' {
			if inlist("`v'", "country", "variable") {
				qui levelsof `v' if n == `n', clean local(scl_`v'_`n')
				scal scl_`v'_`n' = "`scl_`v'_`n''"
			}
			if inlist("`v'", "year", "value") {
				quietly sum `v' if n == `n' 
				scal scl_`v'_`n' = r(max)
			}
		}
	}

	//display as csv 
	forvalues n = 1/`N' {
		if `n' == 1 {
			local linelength = 55
			//Prepare display table with summary info 
			display as text "{hline `linelength'}"
			display as text "INEQSTATS-LISSY Results"
			display as text "{hline `linelength'}"
			di as text "Settings: "
			di as text "Extracted from `dname' database"		
			display as text "Weight used: `weight'"
			display as text "Income/wealth components: `decomp_working'"
			display as text "{hline `linelength'}"

			//Display csv 
			di as result ///
				"{bf:<<<<<<<<<<<<<<<< CSV file starts here >>>>>>>>>>>>>>>>>}"
			di as text "country, year, variable, value"
		} 
		di as text scl_country_`n' "," scl_year_`n' "," ///
			scl_variable_`n' "," scl_value_`n'
		if `n' == _N {
			di as result ///
				"{bf:<<<<<<<<<<<<<<<< CSV file ends here >>>>>>>>>>>>>>>>>>>}"
			display as text "{hline `linelength'}"
		}
	}
	
end	

//Execute program 
$execute
 
