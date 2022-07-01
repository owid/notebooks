use wid_pretax_992j_dist, replace

drop if percentile=="p99p100"
drop if percentile=="p99.9p100"
drop if percentile=="p99.99p100"

gen weight = 0.00001
replace weight = 0.0001 if p < .9999
replace weight = 0.001 if p < .999
replace weight = 0.01 if p < .99

ineqdeco average [aw = weight] if country=="CL" & year==2016
ineqdeco average [fw = weight] if country=="CL" & year==2016
ineqdeco average [pw = weight] if country=="CL" & year==2016
ineqdeco average [iw = weight] if country=="CL" & year==2016
