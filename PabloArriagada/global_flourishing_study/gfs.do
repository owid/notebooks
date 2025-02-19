use gfs_all_countries_wave1, clear


* Define questions CONTENT HAPPY LIFE_SAT MENTAL_HEALTH PHYSICAL_HLTH WORRY_SAFETY EXPENSES
global questions CONTENT HAPPY LIFE_SAT MENTAL_HEALTH PHYSICAL_HLTH WORRY_SAFETY EXPENSES

* Keep COUNTRY, WAVE and $questions
keep COUNTRY WAVE ANNUAL_WEIGHT1 STRATA PSU $questions

* Preserve dataset in these conditions
preserve

collapse (mean) $questions [w=ANNUAL_WEIGHT1], by (COUNTRY WAVE)

* Export as csv
export delimited using "gfs_collapse.csv", datafmt replace

restore
preserve


* Combine country and wave
egen country_wave = concat(COUNTRY WAVE), punct("-")

* Create the unique values of country_wave
quietly levelsof country_wave, local(surveys) clean

* Define first survey listed
local first_survey : word 1 of `surveys'

* Define survey
svyset PSU [pweight = ANNUAL_WEIGHT1], strata(STRATA)

foreach survey in `surveys' {
	* If we are in the first country of the list print the title
	if "`survey'" == "`first_survey'" {
		di "survey,CONTENT,HAPPY,LIFE_SAT,MENTAL_HEALTH,PHYSICAL_HLTH,WORRY_SAFETY,EXPENSES"
	}
	foreach question in $questions {
		* Calculate mean
		qui svy: mean `question' if country_wave == "`survey'"
		
		* Save matrix of estimates
		matrix b = e(b)
		
		* Display value of matrix
		local `question': di b[1,1]
	}
	
	* Print results by survey
	di "`survey',`CONTENT',`HAPPY',`LIFE_SAT',`MENTAL_HEALTH',`PHYSICAL_HLTH',`WORRY_SAFETY',`EXPENSES'"
}
