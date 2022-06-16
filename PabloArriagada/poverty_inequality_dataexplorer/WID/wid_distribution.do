
/*
Use the following letters before different types of income:

a*	average	local currency unit, last year’s prices
b*	inverted Pareto-Lorenz coefficient	no unit
f	female population	fraction (between 0 and 1)
g*	Gini coefficient	Gini coefficient (between 0 and 1)
i	index	no unit
n	population	people
s*	share	fraction (between 0 and 1)
t*	threshold	local currency unit, last year’s prices
m*	total	local currency unit, last year’s prices
p	proportion of women	fraction (between 0 and 1)
w	wealth-to-income ratio or labor/capital share	fraction of national income
r	Top 10/Bottom 50 ratio	no unit
x	exchange rate (market or PPP)	local currency unit per foreign currency
e	Total emissions	Tons of CO2 equivalent emissions
k	Per capita emissions	Tons of CO2 equivalent emissions
l	Average per capita group emissions	Tons of CO2 equivalent per capita emissions

Age:

age code	description
999	The population is comprised of individuals of all ages.
991	The population is comprised of individuals below age 20.
992	The population is comprised of individuals over age 20.
993	The population is comprised of individuals between ages 20 and 39.
994	The population is comprised of individuals between ages 40 and 59.
995	The population is comprised of individuals over age 60.
996	The population is comprised of individuals between ages 20 and 64.
997	The population is comprised of individuals over age 65.
998	The population is comprised of individuals over age 80.
201	The population is comprised of individuals of in the 20 to 24 age group.
251	The population is comprised of individuals of in the 25 to 29 age group.
301	The population is comprised of individuals of in the 30 to 34 age group.
351	The population is comprised of individuals of in the 35 to 39 age group.
401	The population is comprised of individuals of in the 40 to 44 age group.
451	The population is comprised of individuals of in the 45 to 49 age group.
501	The population is comprised of individuals of in the 50 to 54 age group.
551	The population is comprised of individuals of in the 55 to 59 age group.
601	The population is comprised of individuals of in the 60 to 64 age group.
651	The population is comprised of individuals of in the 65 to 69 age group.
701	The population is comprised of individuals of in the 70 to 74 age group.
751	The population is comprised of individuals of in the 75 to 79 age group.
801	The population is comprised of individuals of in the 80 to 84 age group.
851	The population is comprised of individuals of in the 85 to 89 age group.
901	The population is comprised of individuals of in the 90 to 94 age group.
951	The population is comprised of individuals of in the 95 to 99 age group.
111	The population is comprised of individuals over age 99.
001	The population is comprised of individuals of in the 0 to 4 age group.
051	The population is comprised of individuals of in the 5 to 9 age group.
101	The population is comprised of individuals of in the 10 to 14 age group.
151	The population is comprised of individuals of in the 15 to 19 age group.
202	The population is comprised of individuals of in the 20 to 29 age group.
302	The population is comprised of individuals of in the 30 to 39 age group.
402	The population is comprised of individuals of in the 40 to 49 age group.
502	The population is comprised of individuals of in the 50 to 59 age group.
602	The population is comprised of individuals of in the 60 to 69 age group.
702	The population is comprised of individuals of in the 70 to 79 age group.
802	The population is comprised of individuals of in the 80 to 89 age group.
902	The population is comprised of individuals of in the 90 to 99 age group.

Population unit:

unit code	description
i	individuals
j	equal-split adults
m	male
f	female
t	tax unit
e	employed

ptinc: pre-tax national income
diinc: post-tax national income
cainc: 	post-tax disposable income

*/

wid, indicators(xlcusp) year(2017) clear 
rename value ppp
tempfile ppp
save "`ppp'", replace

*wid_pretax_992j_dist
wid, indicators(aptinc tptinc mptinc) perc(p0p1	p1p2	p2p3	p3p4	p4p5	p5p6	p6p7	p7p8	p8p9	p9p10	p10p11	p11p12	p12p13	p13p14	p14p15	p15p16	p16p17	p17p18	p18p19	p19p20	p20p21	p21p22	p22p23	p23p24	p24p25	p25p26	p26p27	p27p28	p28p29	p29p30	p30p31	p31p32	p32p33	p33p34	p34p35	p35p36	p36p37	p37p38	p38p39	p39p40	p40p41	p41p42	p42p43	p43p44	p44p45	p45p46	p46p47	p47p48	p48p49	p49p50	p50p51	p51p52	p52p53	p53p54	p54p55	p55p56	p56p57	p57p58	p58p59	p59p60	p60p61	p61p62	p62p63	p63p64	p64p65	p65p66	p66p67	p67p68	p68p69	p69p70	p70p71	p71p72	p72p73	p73p74	p74p75	p75p76	p76p77	p77p78	p78p79	p79p80	p80p81	p81p82	p82p83	p83p84	p84p85	p85p86	p86p87	p87p88	p88p89	p89p90	p90p91	p91p92	p92p93	p93p94	p94p95	p95p96	p96p97	p97p98	p98p99	p99p99.1	p99.1p99.2	p99.2p99.3	p99.3p99.4	p99.4p99.5	p99.5p99.6	p99.6p99.7	p99.7p99.8	p99.8p99.9	p99.9p99.91	p99.91p99.92	p99.92p99.93	p99.93p99.94	p99.94p99.95	p99.95p99.96	p99.96p99.97	p99.97p99.98	p99.98p99.99	p99.99p99.991	p99.991p99.992	p99.992p99.993	p99.993p99.994	p99.994p99.995	p99.995p99.996	p99.996p99.997	p99.997p99.998	p99.998p99.999	p99.999p100) ages(992) pop(j) exclude clear
merge n:1 country using "`ppp'", keep(match)
replace value = value/ppp
drop ppp
drop _merge
tempfile avgthrtot
save "`avgthrtot'", replace


wid, indicators(bptinc sptinc) perc(p0p1	p1p2	p2p3	p3p4	p4p5	p5p6	p6p7	p7p8	p8p9	p9p10	p10p11	p11p12	p12p13	p13p14	p14p15	p15p16	p16p17	p17p18	p18p19	p19p20	p20p21	p21p22	p22p23	p23p24	p24p25	p25p26	p26p27	p27p28	p28p29	p29p30	p30p31	p31p32	p32p33	p33p34	p34p35	p35p36	p36p37	p37p38	p38p39	p39p40	p40p41	p41p42	p42p43	p43p44	p44p45	p45p46	p46p47	p47p48	p48p49	p49p50	p50p51	p51p52	p52p53	p53p54	p54p55	p55p56	p56p57	p57p58	p58p59	p59p60	p60p61	p61p62	p62p63	p63p64	p64p65	p65p66	p66p67	p67p68	p68p69	p69p70	p70p71	p71p72	p72p73	p73p74	p74p75	p75p76	p76p77	p77p78	p78p79	p79p80	p80p81	p81p82	p82p83	p83p84	p84p85	p85p86	p86p87	p87p88	p88p89	p89p90	p90p91	p91p92	p92p93	p93p94	p94p95	p95p96	p96p97	p97p98	p98p99	p99p99.1	p99.1p99.2	p99.2p99.3	p99.3p99.4	p99.4p99.5	p99.5p99.6	p99.6p99.7	p99.7p99.8	p99.8p99.9	p99.9p99.91	p99.91p99.92	p99.92p99.93	p99.93p99.94	p99.94p99.95	p99.95p99.96	p99.96p99.97	p99.97p99.98	p99.98p99.99	p99.99p99.991	p99.991p99.992	p99.992p99.993	p99.993p99.994	p99.994p99.995	p99.995p99.996	p99.996p99.997	p99.997p99.998	p99.998p99.999	p99.999p100) ages(992) pop(j) exclude clear
append using "`avgthrtot'"

egen couyp = concat(country year percentile), punct(+)
drop country
drop year
drop percentile

reshape wide value, j(variable) i(couyp) string

split couyp, p(+) destring

rename couyp1 country
rename couyp2 year
rename couyp3 percentile

drop couyp

rename valuea* average
rename valueb* inv_paretolorenz
rename values* share
rename valuet* threshold

split percentile, p(p)
destring percentile2, generate(p)
replace p = p/100
drop percentile1
drop percentile2
drop percentile3

sort country year p

order country year percentile p threshold average share inv_paretolorenz

save "wid_pretax_992j_dist.dta", replace
export delimited using "wid_pretax_992j_dist.csv", replace

*wid_posttax_nat_992j_dist
wid, indicators(adiinc tdiinc mdiinc) perc(p0p1	p1p2	p2p3	p3p4	p4p5	p5p6	p6p7	p7p8	p8p9	p9p10	p10p11	p11p12	p12p13	p13p14	p14p15	p15p16	p16p17	p17p18	p18p19	p19p20	p20p21	p21p22	p22p23	p23p24	p24p25	p25p26	p26p27	p27p28	p28p29	p29p30	p30p31	p31p32	p32p33	p33p34	p34p35	p35p36	p36p37	p37p38	p38p39	p39p40	p40p41	p41p42	p42p43	p43p44	p44p45	p45p46	p46p47	p47p48	p48p49	p49p50	p50p51	p51p52	p52p53	p53p54	p54p55	p55p56	p56p57	p57p58	p58p59	p59p60	p60p61	p61p62	p62p63	p63p64	p64p65	p65p66	p66p67	p67p68	p68p69	p69p70	p70p71	p71p72	p72p73	p73p74	p74p75	p75p76	p76p77	p77p78	p78p79	p79p80	p80p81	p81p82	p82p83	p83p84	p84p85	p85p86	p86p87	p87p88	p88p89	p89p90	p90p91	p91p92	p92p93	p93p94	p94p95	p95p96	p96p97	p97p98	p98p99	p99p99.1	p99.1p99.2	p99.2p99.3	p99.3p99.4	p99.4p99.5	p99.5p99.6	p99.6p99.7	p99.7p99.8	p99.8p99.9	p99.9p99.91	p99.91p99.92	p99.92p99.93	p99.93p99.94	p99.94p99.95	p99.95p99.96	p99.96p99.97	p99.97p99.98	p99.98p99.99	p99.99p99.991	p99.991p99.992	p99.992p99.993	p99.993p99.994	p99.994p99.995	p99.995p99.996	p99.996p99.997	p99.997p99.998	p99.998p99.999	p99.999p100) ages(992) pop(j) exclude clear
merge n:1 country using "`ppp'", keep(match)
replace value = value/ppp
drop ppp
drop _merge
tempfile avgthrtot
save "`avgthrtot'", replace

wid, indicators(bdiinc sdiinc) perc(p0p1	p1p2	p2p3	p3p4	p4p5	p5p6	p6p7	p7p8	p8p9	p9p10	p10p11	p11p12	p12p13	p13p14	p14p15	p15p16	p16p17	p17p18	p18p19	p19p20	p20p21	p21p22	p22p23	p23p24	p24p25	p25p26	p26p27	p27p28	p28p29	p29p30	p30p31	p31p32	p32p33	p33p34	p34p35	p35p36	p36p37	p37p38	p38p39	p39p40	p40p41	p41p42	p42p43	p43p44	p44p45	p45p46	p46p47	p47p48	p48p49	p49p50	p50p51	p51p52	p52p53	p53p54	p54p55	p55p56	p56p57	p57p58	p58p59	p59p60	p60p61	p61p62	p62p63	p63p64	p64p65	p65p66	p66p67	p67p68	p68p69	p69p70	p70p71	p71p72	p72p73	p73p74	p74p75	p75p76	p76p77	p77p78	p78p79	p79p80	p80p81	p81p82	p82p83	p83p84	p84p85	p85p86	p86p87	p87p88	p88p89	p89p90	p90p91	p91p92	p92p93	p93p94	p94p95	p95p96	p96p97	p97p98	p98p99	p99p99.1	p99.1p99.2	p99.2p99.3	p99.3p99.4	p99.4p99.5	p99.5p99.6	p99.6p99.7	p99.7p99.8	p99.8p99.9	p99.9p99.91	p99.91p99.92	p99.92p99.93	p99.93p99.94	p99.94p99.95	p99.95p99.96	p99.96p99.97	p99.97p99.98	p99.98p99.99	p99.99p99.991	p99.991p99.992	p99.992p99.993	p99.993p99.994	p99.994p99.995	p99.995p99.996	p99.996p99.997	p99.997p99.998	p99.998p99.999	p99.999p100) ages(992) pop(j) exclude clear
append using "`avgthrtot'"

egen couyp = concat(country year percentile), punct(+)
drop country
drop year
drop percentile

reshape wide value, j(variable) i(couyp) string

split couyp, p(+) destring

rename couyp1 country
rename couyp2 year
rename couyp3 percentile

drop couyp

rename valuea* average
rename valueb* inv_paretolorenz
rename values* share
rename valuet* threshold

split percentile, p(p)
destring percentile2, generate(p)
replace p = p/100
drop percentile1
drop percentile2
drop percentile3

sort country year p

order country year percentile p threshold average share inv_paretolorenz

save "wid_posttax_nat_992j_dist.dta", replace
export delimited using "wid_posttax_nat_992j_dist.csv", replace

*wid_posttax_dis_992j_dist
wid, indicators(acainc tcainc mcainc) perc(p0p1	p1p2	p2p3	p3p4	p4p5	p5p6	p6p7	p7p8	p8p9	p9p10	p10p11	p11p12	p12p13	p13p14	p14p15	p15p16	p16p17	p17p18	p18p19	p19p20	p20p21	p21p22	p22p23	p23p24	p24p25	p25p26	p26p27	p27p28	p28p29	p29p30	p30p31	p31p32	p32p33	p33p34	p34p35	p35p36	p36p37	p37p38	p38p39	p39p40	p40p41	p41p42	p42p43	p43p44	p44p45	p45p46	p46p47	p47p48	p48p49	p49p50	p50p51	p51p52	p52p53	p53p54	p54p55	p55p56	p56p57	p57p58	p58p59	p59p60	p60p61	p61p62	p62p63	p63p64	p64p65	p65p66	p66p67	p67p68	p68p69	p69p70	p70p71	p71p72	p72p73	p73p74	p74p75	p75p76	p76p77	p77p78	p78p79	p79p80	p80p81	p81p82	p82p83	p83p84	p84p85	p85p86	p86p87	p87p88	p88p89	p89p90	p90p91	p91p92	p92p93	p93p94	p94p95	p95p96	p96p97	p97p98	p98p99	p99p99.1	p99.1p99.2	p99.2p99.3	p99.3p99.4	p99.4p99.5	p99.5p99.6	p99.6p99.7	p99.7p99.8	p99.8p99.9	p99.9p99.91	p99.91p99.92	p99.92p99.93	p99.93p99.94	p99.94p99.95	p99.95p99.96	p99.96p99.97	p99.97p99.98	p99.98p99.99	p99.99p99.991	p99.991p99.992	p99.992p99.993	p99.993p99.994	p99.994p99.995	p99.995p99.996	p99.996p99.997	p99.997p99.998	p99.998p99.999	p99.999p100) ages(992) pop(j) exclude clear
merge n:1 country using "`ppp'", keep(match)
replace value = value/ppp
drop ppp
drop _merge
tempfile avgthrtot
save "`avgthrtot'", replace

wid, indicators(bcainc scainc) perc(p0p1	p1p2	p2p3	p3p4	p4p5	p5p6	p6p7	p7p8	p8p9	p9p10	p10p11	p11p12	p12p13	p13p14	p14p15	p15p16	p16p17	p17p18	p18p19	p19p20	p20p21	p21p22	p22p23	p23p24	p24p25	p25p26	p26p27	p27p28	p28p29	p29p30	p30p31	p31p32	p32p33	p33p34	p34p35	p35p36	p36p37	p37p38	p38p39	p39p40	p40p41	p41p42	p42p43	p43p44	p44p45	p45p46	p46p47	p47p48	p48p49	p49p50	p50p51	p51p52	p52p53	p53p54	p54p55	p55p56	p56p57	p57p58	p58p59	p59p60	p60p61	p61p62	p62p63	p63p64	p64p65	p65p66	p66p67	p67p68	p68p69	p69p70	p70p71	p71p72	p72p73	p73p74	p74p75	p75p76	p76p77	p77p78	p78p79	p79p80	p80p81	p81p82	p82p83	p83p84	p84p85	p85p86	p86p87	p87p88	p88p89	p89p90	p90p91	p91p92	p92p93	p93p94	p94p95	p95p96	p96p97	p97p98	p98p99	p99p99.1	p99.1p99.2	p99.2p99.3	p99.3p99.4	p99.4p99.5	p99.5p99.6	p99.6p99.7	p99.7p99.8	p99.8p99.9	p99.9p99.91	p99.91p99.92	p99.92p99.93	p99.93p99.94	p99.94p99.95	p99.95p99.96	p99.96p99.97	p99.97p99.98	p99.98p99.99	p99.99p99.991	p99.991p99.992	p99.992p99.993	p99.993p99.994	p99.994p99.995	p99.995p99.996	p99.996p99.997	p99.997p99.998	p99.998p99.999	p99.999p100) ages(992) pop(j) exclude clear
append using "`avgthrtot'"

egen couyp = concat(country year percentile), punct(+)
drop country
drop year
drop percentile

reshape wide value, j(variable) i(couyp) string

split couyp, p(+) destring

rename couyp1 country
rename couyp2 year
rename couyp3 percentile

drop couyp

rename valuea* average
rename valueb* inv_paretolorenz
rename values* share
rename valuet* threshold

split percentile, p(p)
destring percentile2, generate(p)
replace p = p/100
drop percentile1
drop percentile2
drop percentile3

sort country year p

order country year percentile p threshold average share inv_paretolorenz

save "wid_posttax_dis_992j_dist.dta", replace
export delimited using "wid_posttax_dis_992j_dist.csv", replace


/*
*999, j
wid, indicators(aptinc) perc(p0p1	p1p2	p2p3	p3p4	p4p5	p5p6	p6p7	p7p8	p8p9	p9p10	p10p11	p11p12	p12p13	p13p14	p14p15	p15p16	p16p17	p17p18	p18p19	p19p20	p20p21	p21p22	p22p23	p23p24	p24p25	p25p26	p26p27	p27p28	p28p29	p29p30	p30p31	p31p32	p32p33	p33p34	p34p35	p35p36	p36p37	p37p38	p38p39	p39p40	p40p41	p41p42	p42p43	p43p44	p44p45	p45p46	p46p47	p47p48	p48p49	p49p50	p50p51	p51p52	p52p53	p53p54	p54p55	p55p56	p56p57	p57p58	p58p59	p59p60	p60p61	p61p62	p62p63	p63p64	p64p65	p65p66	p66p67	p67p68	p68p69	p69p70	p70p71	p71p72	p72p73	p73p74	p74p75	p75p76	p76p77	p77p78	p78p79	p79p80	p80p81	p81p82	p82p83	p83p84	p84p85	p85p86	p86p87	p87p88	p88p89	p89p90	p90p91	p91p92	p92p93	p93p94	p94p95	p95p96	p96p97	p97p98	p98p99	p99p99.1	p99.1p99.2	p99.2p99.3	p99.3p99.4	p99.4p99.5	p99.5p99.6	p99.6p99.7	p99.7p99.8	p99.8p99.9	p99.9p99.91	p99.91p99.92	p99.92p99.93	p99.93p99.94	p99.94p99.95	p99.95p99.96	p99.96p99.97	p99.97p99.98	p99.98p99.99	p99.99p99.991	p99.991p99.992	p99.992p99.993	p99.993p99.994	p99.994p99.995	p99.995p99.996	p99.996p99.997	p99.997p99.998	p99.998p99.999	p99.999p100) ages(999) pop(j) metadata clear

merge n:1 country using "`ppp'"
gen value_ppp = value/ppp

save "wid_distribution999j.dta", replace

*992, i
wid, indicators(aptinc) perc(p0p1	p1p2	p2p3	p3p4	p4p5	p5p6	p6p7	p7p8	p8p9	p9p10	p10p11	p11p12	p12p13	p13p14	p14p15	p15p16	p16p17	p17p18	p18p19	p19p20	p20p21	p21p22	p22p23	p23p24	p24p25	p25p26	p26p27	p27p28	p28p29	p29p30	p30p31	p31p32	p32p33	p33p34	p34p35	p35p36	p36p37	p37p38	p38p39	p39p40	p40p41	p41p42	p42p43	p43p44	p44p45	p45p46	p46p47	p47p48	p48p49	p49p50	p50p51	p51p52	p52p53	p53p54	p54p55	p55p56	p56p57	p57p58	p58p59	p59p60	p60p61	p61p62	p62p63	p63p64	p64p65	p65p66	p66p67	p67p68	p68p69	p69p70	p70p71	p71p72	p72p73	p73p74	p74p75	p75p76	p76p77	p77p78	p78p79	p79p80	p80p81	p81p82	p82p83	p83p84	p84p85	p85p86	p86p87	p87p88	p88p89	p89p90	p90p91	p91p92	p92p93	p93p94	p94p95	p95p96	p96p97	p97p98	p98p99	p99p99.1	p99.1p99.2	p99.2p99.3	p99.3p99.4	p99.4p99.5	p99.5p99.6	p99.6p99.7	p99.7p99.8	p99.8p99.9	p99.9p99.91	p99.91p99.92	p99.92p99.93	p99.93p99.94	p99.94p99.95	p99.95p99.96	p99.96p99.97	p99.97p99.98	p99.98p99.99	p99.99p99.991	p99.991p99.992	p99.992p99.993	p99.993p99.994	p99.994p99.995	p99.995p99.996	p99.996p99.997	p99.997p99.998	p99.998p99.999	p99.999p100) ages(992) pop(i) metadata clear

merge n:1 country using "`ppp'"
gen value_ppp = value/ppp

save "wid_distribution992i.dta", replace

*999, i
wid, indicators(aptinc) perc(p0p1	p1p2	p2p3	p3p4	p4p5	p5p6	p6p7	p7p8	p8p9	p9p10	p10p11	p11p12	p12p13	p13p14	p14p15	p15p16	p16p17	p17p18	p18p19	p19p20	p20p21	p21p22	p22p23	p23p24	p24p25	p25p26	p26p27	p27p28	p28p29	p29p30	p30p31	p31p32	p32p33	p33p34	p34p35	p35p36	p36p37	p37p38	p38p39	p39p40	p40p41	p41p42	p42p43	p43p44	p44p45	p45p46	p46p47	p47p48	p48p49	p49p50	p50p51	p51p52	p52p53	p53p54	p54p55	p55p56	p56p57	p57p58	p58p59	p59p60	p60p61	p61p62	p62p63	p63p64	p64p65	p65p66	p66p67	p67p68	p68p69	p69p70	p70p71	p71p72	p72p73	p73p74	p74p75	p75p76	p76p77	p77p78	p78p79	p79p80	p80p81	p81p82	p82p83	p83p84	p84p85	p85p86	p86p87	p87p88	p88p89	p89p90	p90p91	p91p92	p92p93	p93p94	p94p95	p95p96	p96p97	p97p98	p98p99	p99p99.1	p99.1p99.2	p99.2p99.3	p99.3p99.4	p99.4p99.5	p99.5p99.6	p99.6p99.7	p99.7p99.8	p99.8p99.9	p99.9p99.91	p99.91p99.92	p99.92p99.93	p99.93p99.94	p99.94p99.95	p99.95p99.96	p99.96p99.97	p99.97p99.98	p99.98p99.99	p99.99p99.991	p99.991p99.992	p99.992p99.993	p99.993p99.994	p99.994p99.995	p99.995p99.996	p99.996p99.997	p99.997p99.998	p99.998p99.999	p99.999p100) ages(999) pop(i) metadata clear

merge n:1 country using "`ppp'"
gen value_ppp = value/ppp

save "wid_distribution999i.dta", replace

*992, t
wid, indicators(aptinc) perc(p0p1	p1p2	p2p3	p3p4	p4p5	p5p6	p6p7	p7p8	p8p9	p9p10	p10p11	p11p12	p12p13	p13p14	p14p15	p15p16	p16p17	p17p18	p18p19	p19p20	p20p21	p21p22	p22p23	p23p24	p24p25	p25p26	p26p27	p27p28	p28p29	p29p30	p30p31	p31p32	p32p33	p33p34	p34p35	p35p36	p36p37	p37p38	p38p39	p39p40	p40p41	p41p42	p42p43	p43p44	p44p45	p45p46	p46p47	p47p48	p48p49	p49p50	p50p51	p51p52	p52p53	p53p54	p54p55	p55p56	p56p57	p57p58	p58p59	p59p60	p60p61	p61p62	p62p63	p63p64	p64p65	p65p66	p66p67	p67p68	p68p69	p69p70	p70p71	p71p72	p72p73	p73p74	p74p75	p75p76	p76p77	p77p78	p78p79	p79p80	p80p81	p81p82	p82p83	p83p84	p84p85	p85p86	p86p87	p87p88	p88p89	p89p90	p90p91	p91p92	p92p93	p93p94	p94p95	p95p96	p96p97	p97p98	p98p99	p99p99.1	p99.1p99.2	p99.2p99.3	p99.3p99.4	p99.4p99.5	p99.5p99.6	p99.6p99.7	p99.7p99.8	p99.8p99.9	p99.9p99.91	p99.91p99.92	p99.92p99.93	p99.93p99.94	p99.94p99.95	p99.95p99.96	p99.96p99.97	p99.97p99.98	p99.98p99.99	p99.99p99.991	p99.991p99.992	p99.992p99.993	p99.993p99.994	p99.994p99.995	p99.995p99.996	p99.996p99.997	p99.997p99.998	p99.998p99.999	p99.999p100) ages(992) pop(t) metadata clear

merge n:1 country using "`ppp'"
gen value_ppp = value/ppp

save "wid_distribution992t.dta", replace

*999, t
wid, indicators(aptinc) perc(p0p1	p1p2	p2p3	p3p4	p4p5	p5p6	p6p7	p7p8	p8p9	p9p10	p10p11	p11p12	p12p13	p13p14	p14p15	p15p16	p16p17	p17p18	p18p19	p19p20	p20p21	p21p22	p22p23	p23p24	p24p25	p25p26	p26p27	p27p28	p28p29	p29p30	p30p31	p31p32	p32p33	p33p34	p34p35	p35p36	p36p37	p37p38	p38p39	p39p40	p40p41	p41p42	p42p43	p43p44	p44p45	p45p46	p46p47	p47p48	p48p49	p49p50	p50p51	p51p52	p52p53	p53p54	p54p55	p55p56	p56p57	p57p58	p58p59	p59p60	p60p61	p61p62	p62p63	p63p64	p64p65	p65p66	p66p67	p67p68	p68p69	p69p70	p70p71	p71p72	p72p73	p73p74	p74p75	p75p76	p76p77	p77p78	p78p79	p79p80	p80p81	p81p82	p82p83	p83p84	p84p85	p85p86	p86p87	p87p88	p88p89	p89p90	p90p91	p91p92	p92p93	p93p94	p94p95	p95p96	p96p97	p97p98	p98p99	p99p99.1	p99.1p99.2	p99.2p99.3	p99.3p99.4	p99.4p99.5	p99.5p99.6	p99.6p99.7	p99.7p99.8	p99.8p99.9	p99.9p99.91	p99.91p99.92	p99.92p99.93	p99.93p99.94	p99.94p99.95	p99.95p99.96	p99.96p99.97	p99.97p99.98	p99.98p99.99	p99.99p99.991	p99.991p99.992	p99.992p99.993	p99.993p99.994	p99.994p99.995	p99.995p99.996	p99.996p99.997	p99.997p99.998	p99.998p99.999	p99.999p100) ages(999) pop(t) metadata clear

merge n:1 country using "`ppp'"
gen value_ppp = value/ppp

save "wid_distribution999t.dta", replace

*/




*wid, indicators(shweal) perc(p0p1	p1p2	p2p3	p3p4	p4p5	p5p6	p6p7	p7p8	p8p9	p9p10	p10p11	p11p12	p12p13	p13p14	p14p15	p15p16	p16p17	p17p18	p18p19	p19p20	p20p21	p21p22	p22p23	p23p24	p24p25	p25p26	p26p27	p27p28	p28p29	p29p30	p30p31	p31p32	p32p33	p33p34	p34p35	p35p36	p36p37	p37p38	p38p39	p39p40	p40p41	p41p42	p42p43	p43p44	p44p45	p45p46	p46p47	p47p48	p48p49	p49p50	p50p51	p51p52	p52p53	p53p54	p54p55	p55p56	p56p57	p57p58	p58p59	p59p60	p60p61	p61p62	p62p63	p63p64	p64p65	p65p66	p66p67	p67p68	p68p69	p69p70	p70p71	p71p72	p72p73	p73p74	p74p75	p75p76	p76p77	p77p78	p78p79	p79p80	p80p81	p81p82	p82p83	p83p84	p84p85	p85p86	p86p87	p87p88	p88p89	p89p90	p90p91	p91p92	p92p93	p93p94	p94p95	p95p96	p96p97	p97p98	p98p99	p99p99.1	p99.1p99.2	p99.2p99.3	p99.3p99.4	p99.4p99.5	p99.5p99.6	p99.6p99.7	p99.7p99.8	p99.8p99.9	p99.9p99.91	p99.91p99.92	p99.92p99.93	p99.93p99.94	p99.94p99.95	p99.95p99.96	p99.96p99.97	p99.97p99.98	p99.98p99.99	p99.99p99.991	p99.991p99.992	p99.992p99.993	p99.993p99.994	p99.994p99.995	p99.995p99.996	p99.996p99.997	p99.997p99.998	p99.998p99.999	p99.999p100) ages(992) pop(j) metadata clear

