*****  Stata do-file to create the press-freedom data used in the following chart on Our World in Data (OWID):
*****  https://ourworldindata.org/grapher/press-freedom-fh
*****  Author: Bastian Herre
*****  April 8, 2022


version 14

clear all
set more off
set varabbrev off


** Set your own working directories here to run the file:
cd "/Users/bastianherre/Dropbox/Data/"
global project "/Users/bastianherre/Dropbox/Data/"


** Download dataset from https://freedomhouse.org/sites/default/files/2020-02/FOTP1980-FOTP2017_Public-Data.xlsx and move it into the folder "Freedom House 2017 freedom of the world".

** Import Freedom of the press dataset:
import excel "Freedom House 2017 Freedom of the Press/FOTP1980-FOTP2017_Public-Data.xlsx", sheet("Data") clear


** Drop rows that are not observations:
drop in 1/3


** Give variables meaning- and useful names:
rename A country_name
rename B y1979p
rename C y1979b
rename D y1980p
rename E y1980b
rename F y1982p
rename G y1982b // Treat January 1981 to August 1982 as 1982.
rename H y1983p
rename I y1983b // Treat August 1982 to November 1983 as 1983.
rename J y1984p
rename K y1984b
rename L y1985p
rename M y1985b
rename N y1986p
rename O y1986b
rename P y1987p
rename Q y1987b
rename R y1988
rename S y1989
rename T y1990
rename U y1991
rename V y1992
rename AF y1993
rename AP y1994
rename AZ y1995
rename BJ y1996
rename BT y1997
rename CD y1998
rename CN y1999
rename CX y2000
rename DC y2001
rename DH y2002
rename DM y2003
rename DR y2004
rename DW y2005
rename EB y2006
rename EG y2007
rename EL y2008
rename EQ y2009
rename EV y2010
rename FA y2011
rename FF y2012
rename FK y2013
rename FP y2014
rename FU y2015
rename FZ y2016


** Drop now-superfluous rows that are not observations:
drop in 1/2


** Create aggregate score across print and broadcast media by using the lower classification of the two categories:
generate y1979 = ""
replace y1979 = "-" if y1979p == "-" | y1979b == "-"
replace y1979 = "NF" if y1979 != "-" & (y1979p == "NF" | y1979b == "NF")
replace y1979 = "PF" if y1979 != "-" & y1979 != "NF" & (y1979p == "PF" | y1979b == "PF")
replace y1979 = "F" if y1979p == "F" & y1979b == "F"

generate y1980 = ""
replace y1980 = "-" if y1980p == "-" | y1980b == "-"
replace y1980 = "NF" if y1980 != "-" & (y1980p == "NF" | y1980b == "NF")
replace y1980 = "PF" if y1980 != "-" & y1980 != "NF" & (y1980p == "PF" | y1980b == "PF")
replace y1980 = "F" if y1980p == "F" & y1980b == "F"

generate y1982 = ""
replace y1982 = "-" if y1982p == "-" | y1982b == "-"
replace y1982 = "NF" if y1982 != "-" & (y1982p == "NF" | y1982b == "NF")
replace y1982 = "PF" if y1982 != "-" & y1982 != "NF" & (y1982p == "PF" | y1982b == "PF")
replace y1982 = "F" if y1982p == "F" & y1982b == "F"

generate y1983 = ""
replace y1983 = "-" if y1983p == "-" | y1983b == "-"
replace y1983 = "NF" if y1983 != "-" & (y1983p == "NF" | y1983b == "NF")
replace y1983 = "PF" if y1983 != "-" & y1983 != "NF" & (y1983p == "PF" | y1983b == "PF")
replace y1983 = "F" if y1983p == "F" & y1983b == "F"

generate y1984 = ""
replace y1984 = "-" if y1984p == "-" | y1984b == "-"
replace y1984 = "NF" if y1984 != "-" & (y1984p == "NF" | y1984b == "NF")
replace y1984 = "PF" if y1984 != "-" & y1984 != "NF" & (y1984p == "PF" | y1984b == "PF")
replace y1984 = "F" if y1984p == "F" & y1984b == "F"

generate y1985 = ""
replace y1985 = "-" if y1985p == "-" | y1985b == "-"
replace y1985 = "NF" if y1985 != "-" & (y1985p == "NF" | y1985b == "NF")
replace y1985 = "PF" if y1985 != "-" & y1985 != "NF" & (y1985p == "PF" | y1985b == "PF")
replace y1985 = "F" if y1985p == "F" & y1985b == "F"

generate y1986 = ""
replace y1986 = "-" if y1986p == "-" | y1986b == "-"
replace y1986 = "NF" if y1986 != "-" & (y1986p == "NF" | y1986b == "NF")
replace y1986 = "PF" if y1986 != "-" & y1986 != "NF" & (y1986p == "PF" | y1986b == "PF")
replace y1986 = "F" if y1986p == "F" & y1986b == "F"

generate y1987 = ""
replace y1987 = "-" if y1987p == "-" | y1987b == "-"
replace y1987 = "NF" if y1987 != "-" & (y1987p == "NF" | y1987b == "NF")
replace y1987 = "PF" if y1987 != "-" & y1987 != "NF" & (y1987p == "PF" | y1987b == "PF")
replace y1987 = "F" if y1987p == "F" & y1987b == "F"


** Keep variables of remaining interest:
keep country_name y1979 y1980 y1982 y1983 y1984 y1985 y1986 y1987 y1988 y1990 y1991 y1992 y1993 y1994 y1995 y1996 y1997 y1998 y1999 y2000 y2001 y2002 y2003 y2004 y2005 y2006 y2007 y2008 y2009 y2010 y2011 y2012 y2013 y2014 y2015 y2016


** Create dataset with country-year observations:
reshape long y, i(country_name) j(year)
rename y press_freedom_fh_owid_temp


** Create numeric version of classification:
generate press_freedom_fh_owid = .
replace press_freedom_fh_owid = 0 if press_freedom_fh_owid_temp == "NF"
replace press_freedom_fh_owid = 1 if press_freedom_fh_owid_temp == "PF"
replace press_freedom_fh_owid = 2 if press_freedom_fh_owid_temp == "F"
drop if press_freedom_fh_owid == .
drop press_freedom_fh_owid_temp


** Format country names:
replace country_name = "Congo" if country_name == "Congo (Brazzaville)"
replace country_name = "Democratic Republic of Congo" if country_name == "Congo (Kinshasa)"
replace country_name = "Northern Cyprus" if country_name == "Cyprus (Turkish)"
replace country_name = "Czechia" if country_name == "Czech Republic"
replace country_name = "Germany" if country_name == "Germany, West"
replace country_name = "German Democratic Republic" if country_name == "Germany, East"
replace country_name = "Sao Tome and Principe" if country_name == "São Tomé and Príncipe"
replace country_name = "Timor" if country_name == "Timor-Leste"
replace country_name = "Yemen" if country_name == "Yemen, North"
replace country_name = "South Yemen" if country_name == "Yemen, South"
replace country_name = "West Bank and Gaza Strip" if country_name == "Israeli-Occupied Territories and Palestinian Authority"
replace country_name = "West Bank and Gaza Strip" if country_name == "West Bank and Gaza Strip"
replace country_name = "North Macedonia" if country_name == "Macedonia"
replace country_name = "Cote d'Ivoire" if country_name == "Côte d'Ivoire"
replace country_name = "Gambia" if country_name == "The Gambia"
replace country_name = "Eswatini" if country_name == "Swaziland"


** Replace country names of historical countries with the largest constituent country that exists today:
replace country_name = "Czechia" if country_name == "Czechoslovakia"
replace country_name = "Russia" if country_name == "USSR"
replace country_name = "Serbia" if country_name == "Yugoslavia"


** Label variables:
label variable country_name "Country name"
label variable year "Year"
label variable press_freedom_fh_owid "Press freedom status (Freedom House, OWID)"

** Order variables and sort observations:
order country_name year press_freedom_fh_owid
sort country_name year


* Export data:
save "Freedom House 2017 Freedom of the Press/press_freedom_fh_owid.dta", replace
export delimited "Freedom House 2017 Freedom of the Press/press_freedom_fh_owid.csv", replace



exit
