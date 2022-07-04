use wid_pretax_992j_dist, replace

egen country_year = group(country year)

drop if percentile=="p99p100"
drop if percentile=="p99.9p100"
drop if percentile=="p99.99p100"

gen weight = 0.00001
replace weight = 0.0001 if p < .9999
replace weight = 0.001 if p < .999
replace weight = 0.01 if p < .99

*ineqdec0 average [aw = weight], bygroup(country_year) welfare
ineqdec0 average [aw = weight] if country=="CL" & year==2016, welfare
ineqdeco average [pw = weight] if country=="CL" & year==2016
ineqdeco average [iw = weight] if country=="CL" & year==2016

return list
