use Integrated_values_surveys_1981-2021, clear

preserve

uselabel
drop trunc
* Export as csv
export delimited using "value_labels.csv", datafmt replace

restore

preserve

desc, replace
keep if vallab != "" //keep variables that have value labels
* Export as csv
export delimited using "variable_labels.csv", datafmt replace

restore

