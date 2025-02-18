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
