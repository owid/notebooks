*****  This Stata do-file expands the countries and years covered by the V-Dem and RoW data
*****  Author: Bastian Herre
*****  June 28, 2022

version 14
clear all
set more off
set varabbrev off


** Set your own working directories here to run the file:
cd "/Users/bastianherre/Dropbox/Data/"
global project "/Users/bastianherre/Dropbox/Data/"


** Combine OWID country-year dataset with V-Dem and RoW data:
use "Our World in Data/owid_entities_expanded.dta"

rename entity_name country_name
label variable country_name "Country name"

merge 1:1 country_name year using "democracy/datasets/cleaned/vdem_row_cleaned.dta"
tab country_name if _merge == 2
sort country_name year


** Create variable indicating which observations include information from V-Dem:
generate vdem_obs = 1 if _merge == 2 | _merge == 3
replace vdem_obs = 0 if _merge == 1
drop _merge


** Impute values from adjacent years:

list year regime_row_owid regime_redux_row_owid regime_amb_row_owid if country_name  == "Australia" & year >= 1895 & year <= 1905
replace regime_row_owid = 3 if country_name == "Australia" & year == 1900
replace regime_redux_row_owid = 2 if country_name == "Australia" & year == 1900
replace regime_amb_row_owid = 8 if country_name == "Australia" & year == 1900
* Data missing without clear reason, history of Australia does not indicate consequential event. I recode it because the values in the surrounding year strongly suggest a coding as a liberal democracy.

list year regime_row_owid regime_amb_row_owid if country_name == "Sweden" & year >= 1835 & year <= 1845
replace regime_row_owid = 0 if country_name == "Sweden" & year == 1840
replace regime_redux_row_owid = 0 if country_name == "Sweden" & year == 1840
replace regime_amb_row_owid = 0 if country_name == "Sweden" & year == 1840
* Data (including for v2x_polyarchy) missing without clear reason, history of Sweden does not indicate consequential event; perhaps due to missing data on head of government, who is not listed even though he existed (likely Arvid Mauritz Posse). I recode it with the regime type in adjacent years.

** Possible imputations:
list year regime_row_owid electdem_vdem electmulpar_row electmulpar_hoe_row_owid electmulpar_leg_row electfreefair_row if country_name == "Peru" & year >= 1880 & year <= 1900
* I favor no imputation because of six years of missing data, and even though one criterion for electoral autocracy is not met, the country may have met the criteria for democracy (if unlikely), thereby overriding the former.
list year regime_row_owid electdem_vdem electmulpar_row electmulpar_hoe_row_owid electmulpar_leg_row electfreefair_row if country_name == "Honduras" & year >= 1910 & year <= 1950
* I favor no imputation because of 12 years of missing data, and the country may have met the criteria for democracy.


** Impute values from historical predecessors:
* I identified the following countries and years as candidates for imputation because OWID population data is available, but V-Dem did not provide regime data.
* I only check candidates with a population of at one point more than 1 million
* Among the sources I used, Wimmer and Min (2006) code the status of a country at the end of the year, CShapes 2.0 codes its borders at the beginning of the year.

generate country_name_regime_imputed = ""

* Germany 1945-1948: occupied by United States (Cshapes 2.0); I favor no imputation.
* Bangladesh 1789-1970: 1947-1970 imperial power/part of Pakistan (Wimmer and Min 2006, Cshapes 2.0), 1765-1946 imperial power United Kingdom, 1886-1946 part of colony India (Cshapes 2.0), colonized in 1757 (Ertan et al. 2016).
replace country_name_regime_imputed = "Pakistan" if country_name == "Bangladesh" & year >= 1947 & year <= 1970
replace country_name_regime_imputed = "India" if country_name == "Bangladesh" & year >= 1789 & year <= 1946
* Ukraine 1789-1989: 1946-1989 imperial power/part of Russia (Wimmer and Min 2006, Cshapes 2.0), 1921-1945 and 1816-1918 mixed rule (Wimmer and Min 2006).
replace country_name_regime_imputed = "Russia" if country_name == "Ukraine" & year >= 1946 & year <= 1989
* Pakistan 1789-1946: 1839-1946 imperial power United Kingdom (Wimmer and Min 2006), 1886-1947 part of colony India (Cshapes 2.0), colonized in 1849 (Ertan et al. 2016).
replace country_name_regime_imputed = "India" if country_name == "Pakistan" & year >= 1839 & year <= 1946
* Poland 1789-1808, 1868-1917, 1939-1943: no information 1800-1808, 1795-1914 mixed rule (Wimmer and Min 2006), 1939-1943 independent (Cshapes 2.0); I favor no imputation.
* Italy 1789-1860: 1814-1860 part of Austria-Hungary (Wimmer and Min 2006) or Piedmont since 1815 (Butcher and Griffiths 2020).
replace country_name_regime_imputed = "Piedmont-Sardinia" if country_name == "Italy" & year >= 1815 & year <= 1860
* Nigeria 1789-1913: imperial power United Kingdom 1861-1959 (Wimmer and Min 2006), colony of United Kingdom (Cshapes 2.0), colonized by United Kingdom in 1885 (Ertan et al. 2016); I favor no imputation.
* Vietnam 1789-1944: 1861-1953 imperial power France (Wimmer and Min 2006) or 1886-1893 independent and 1894-1954 colonized by France (Cshapes 2.0), colonized by France in 1867 (Ertan et al. 2016), independent 1802-1884 (Butcher and Griffiths 2020); I favor no imputation.
* Uzbekistan 1789-1911, 1921-1989: imperial power Russia 1865-1990 (Wimmer and Min 2006), part of Russia 1886-1991 (Khiva and Bokhara partially as protectorates), not colonized (Ertan et al. 2016), Khiva and Bokhara as independent until -1872 and -1867.
replace country_name_regime_imputed = "Russia" if country_name == "Uzbekistan" & year >= 1865 & year <= 1911
replace country_name_regime_imputed = "Russia" if country_name == "Uzbekistan" & year >= 1921 & year <= 1989
* Kazakhstan 1789-1989: imperial power Russia 1730-1990 (Wimmer and Min 2006), part of Russia 1886-1991 (Cshapes 2.0); not colonized (Ertan et al. 2016).
replace country_name_regime_imputed = "Russia" if country_name == "Kazakhstan" & year >= 1789 & year <= 1989
* Mozambique 1789-1899, 1974-1993: imperial power Portugal 1885-1974 (Wimmer and Min 2006); colony of Portugal 1886-1975 (Cshapes 2.0), colonized by Portugal, approximated as 1750 (Ertan et al. 2016); I favor no imputation.
* Czechia 1789-1917: imperial power Austria-Hungary 16th century-1917 (Wimmer and Min 2006), part of Austria-Hungary since at least 1886 (Cshapes 2.0), Czech part under Austrian control (Encyclopedia Britannica).
replace country_name_regime_imputed = "Austria" if country_name == "Czechia" & year >= 1789 & year <= 1917
* Iran 1789-1899: no imperial onset (Wimmer and Min 2006), independent since at least 1886 (Cshapes 2.0), not colonized (Ertan et al. 2016); I favor no imputation.
* Belarus 1789-1989: imperial power Russia 1795-1990 (Wimmer and Min 2006); 1886-1991 part of Russia (Cshapes 2.0), not mentioned in Ertan et al. (2016), independent since 1991 (Butcher and Griffiths 2020).
replace country_name_regime_imputed = "Russia" if country_name == "Belarus" & year >= 1795 & year <= 1989
* Democratic Republic of Congo 1789-1899: imperial power Belgium 1885-1959 (Wimmer and Min 2006), colonized in 1885 (Ertan et al. 2016); I favor no imputation.
* North Korea 1789-1944: Korea since the 14th century until 1909, imperial power Japan 1910-1944 (Wimmer and Min 2006), independent Korea since at least 1886-1910, colony of Japan -1945 (Cshapes 2.0), not listed (Ertan et al. 2016).
replace country_name_regime_imputed = "South Korea" if country_name == "North Korea" & year >= 1789 & year <= 1910
* Sudan 1789-1899: Egypt imperial power 1821-1881, mixed rule 1882-1955 (Wimmer and Min 2006), colony of United Kingdom 1898-1955 (CShapes 2.0), colonized by United Kingdom in 1898 (Ertan et al. 2016), independent 1885-1898 (Butcher and Griffiths 2020); in 1886, colony Egypt of United Kingdom covers little of today's Sudan (CShapes 2.0); Egypt invades Sudanese territory in 1820, indigenous forces surrender in 1821, Mahdists capture Khartoum from Egypt and the British in 1885 (Encyclopedia Britannica).
replace country_name_regime_imputed = "Egypt" if country_name == "Sudan" & year >= 1821 & year <= 1884
* South Sudan 1789-2010: not listed, but Egypt imperial power of Sudan 1821-1881, mixed rule 1882-1955 (Wimmer and Min 2006), colony of United Kingdom 1898-1955, part of Sudan until 2012 (Cshapes 2.0), colonized by United Kingdom in 1898 (Ertan et al. 2016), independent 1885-1898 (Butcher and Griffiths 2020).
replace country_name_regime_imputed = "Egypt" if country_name == "South Sudan" & year >= 1821 & year <= 1884 // See immediately above.
replace country_name_regime_imputed = "Sudan" if country_name == "South Sudan" & year >= 1900 & year <= 2010
* Ireland 1789-1918: imperial power United Kingdom 11th century-1919 (Wimmer and Min 2006), part of United Kingdom since at least 1886-1922, independent since 1922 (Butcher and Griffiths 2020).
replace country_name_regime_imputed = "United Kingdom" if country_name == "Ireland" & year >= 1789 & year <= 1918
* Azerbaijan 1789-1989: imperial power Russia 1813-1917, 1920-1990 (Wimmer and Min 2006), part of Russia since at least 1886-1991 (Cshapes 2.0) not colonized (Ertan et al. 2016).
replace country_name_regime_imputed = "Russia" if country_name == "Azerbaijan" & year >= 1813 & year <= 1989
* Romania 1789-1830, 1854-1856, 1859-1899: 1688-1858 imperial power Austria-Hungary (Wimmer and Min 2006), independent since at least 1886 (Cshapes 2.0), independent since 1878 (Butcher and Griffiths 2020), Transylvania part of Austria-Hungary, other parts under Ottoman influence; I favor no imputation.
* Austria 1939-1944: imperial power Germany 1938-1944 (Wimmer and Min 2006), independent 1939-1944 (CShapes 2.0), independent 1918-1938 (Butcher and Griffiths 2020); I favor no imputation.
* Philippines 1789-1899: imperial power Spain 16th century-1898, United States 1899-1945 (Wimmer and Min 2006), colony of Spain since at least 1886-1898, colony of United States 1899-1946 (Cshapes 2.0); I favor no imputation.
* Greece 1789-1821, 1918-1919: imperial power Turkey 15th century - 1826, independent 1918-1919 (Wimmer and Min 2006, Cshapes 2.0); independent from 1828 to 1941 (Butcher and Griffiths 2020).
replace country_name_regime_imputed = "Turkey" if country_name == "Greece" & year >= 1789 & year <= 1821
* Tanzania 1789-1914: imperial power/colonized by Germany and United Kingdom (Wimmer and Min 2006, Cshapes 2.0); I favor no imputation. 
* Georgia 1789-1989: imperial power Russia 1801-1918, 1920-1990 (Wimmer and Min 2006), part of Russia since at least 1886-1991, not colonized (Ertan et al. 2016), independent since 1991 (Butcher and Griffiths 2020).
replace country_name_regime_imputed = "Russia" if country_name == "Georgia" & year >= 1801 & year <= 1989
* Slovakia 1789-1992: imperial power Austria-Hungary 16th century-1913, mixed rule 1914-1918, 1919-1992 imperial power Czechoslovakia (Wimmer and Min 2006), part of Austria-Hungary since at least 1886-1918, part of Czechoslovakia 1919-1992 (Cshapes 2.0), Slovak part under Hungarian control (Encyclopedia Britannica).
replace country_name_regime_imputed = "Hungary" if country_name == "Slovakia" & year >= 1789 & year <= 1918
replace country_name_regime_imputed = "Czechia" if country_name == "Slovakia" & year >= 1919 & year <= 1992
* South Africa 1789-1899: imperial power United Kingdom 1814-1909 (Wimmer and Min 2006); (mostly) colonized by United Kingdom 1886-1911 (Cshapes 2.0), colonized by United Kingdom in 1806, earlier also by Dutch settlers (Ertan et al. 2016); I favor no imputation.
* Cameroon 1789-1960: imperial power Germany 1884-1914, mixed rule 1915-1959 (Wimmer and Min 2006), colonized by Germany since at least 1886-1916, occupied by United Kingdom 1916-1919, mandate by France 1919-1959 (Cshapes 2.0); I favor no imputation.
* Tajikistan 1789-1989: imperial power Russia 1921-1990 (Wimmer and Min 2006), part of Russia, part of Russia's protectorate Bokhara 1886-1920, part of Russia 1920-1990 (Cshapes 2.0), independent since 1991, Bokhara independent 1816-1868 (Butcher and Griffiths 2020).
replace country_name_regime_imputed = "Russia" if country_name == "Tajikistan" & year >= 1868 & year <= 1989
* Palestine 1949-2019: no information (Wimmer and Min 2006, Ertan et al. 2016, Butcher and Griffiths 2020). V-Dem includes Gaza and West Bank separately; I therefore favor no imputation.
* Brazil 1824-1825: independent since 1822 (Wimmer and Min 2006, Butcher and Griffiths 2020); I favor no imputation.
* Serbia 1789-1833, 1932-1934: imperial power Turkey 14th century - 1877 (Wimmer and Min 2006); part of the Ottoman Empire (Encyclopedia Britannica); no imperial power 1932-1934 (Wimmer and Min 2006), independent 1932-1934 (Cshapes 2.0); I favor no imputation for later period. 
replace country_name_regime_imputed = "Turkey" if country_name == "Serbia" & year >= 1789 & year <= 1833
* Croatia 1789-1940, 1945-1990: Austria-Hungary imperial power 1699-1917, mixed rule 1918, Yugoslavia 1919-1990 (Wimmer and Min 2006); Austria-Hungary 1886-1918, 1919 partially Hungary and Yugoslavia, 1920-1992 Yugoslavia; I favor no imputation for earlier era.
replace country_name_regime_imputed = "Serbia" if country_name == "Croatia" & year >= 1945 & year <= 1990
* Algeria 1789-1899: imperial power France 1848-1961 (Wimmer and Min 2006), colonized by France since at least 1886-1962 (Cshapes 2.0); I favor no imputation.
* Bosnia and Herzegovina 1789-1991: imperial power Turkey 15th century-1878, Austria-Hungary 1879-1917, Yugoslavia 1918-1990 (Wimmer and Min 2006); occupied by Austria-Hungary since at least 1886-1908, part of Austria-Hungary 1909-1918, part of Yugoslavia 1919-1992 (Cshapes 2.0); Austrian-Hungary occupation while formally still part of Ottoman Empire, not more associated with either Austria or Hungary (Encyclopedia Britannica); I therefore favor no imputation for 1909-1918.
replace country_name_regime_imputed = "Turkey" if country_name == "Bosnia and Herzegovina" & year >= 1789 & year <= 1878
replace country_name_regime_imputed = "Serbia" if country_name == "Bosnia and Herzegovina" & year >= 1919 & year <= 1991
* Moldova 1789-1989: mixed rule 17th century-1939, imperial power Russia 1940-1990 (Wimmer and Min 2006), part of Russia since at least 1886-1919, part of Russia and Romania 1920-1939, part of Russia 1940-1991 (CShapes 2.0, Encyclopedia Britannica).
replace country_name_regime_imputed = "Russia" if country_name == "Moldova" & year >= 1789 & year <= 1919
replace country_name_regime_imputed = "Russia" if country_name == "Moldova" & year >= 1940 & year <= 1989
* Kyrgyzstan 1789-1989: imperial power Russia 1876-1990 (Wimmer and Min 2006), part of Russia since at least 1886-1991 (Cshapes 2.0), not colonized (Ertan et al. 2016), incorporated into Russia in mid-19th century (Encyclopedia Britannica).
replace country_name_regime_imputed = "Russia" if country_name == "Kyrgyzstan" & year >= 1876 & year <= 1989
* Kenya 1789-1899: protectorate of United Kingdom 1889-1920, colony of United Kingom 1921-1963 (CShapes 2.0); imperial power United Kingdom 1895-1962 (Wimmer and Min 2006); I favor no imputation.
* Burkina Faso 1789-1918, 1932-1946: imperial power France 1895-1959 (Wimmer and Min 2006); colony of France 1895-1960 (Cshapes 2.0); colonized by France in 1896 (Ertan et al. 2016); I favor no imputation.
* Sri Lanka 1789-1899: colonized by United Kingdom as Ceylon (Cshapes 2.0); I favor no imputation.
* Belgium 1789-1790, 1796-1829: imperial power Netherlands 1814-1831 (Wimmer and Min 2006), part of Austria - 1794, part of France 1795-1813, part of Netherlands 1814-1831 (Encyclopedia Britannica).
replace country_name_regime_imputed = "France" if country_name == "Belgium" & year >= 1796 & year <= 1813
replace country_name_regime_imputed = "Austria" if country_name == "Belgium" & year >= 1789 & year <= 1790
replace country_name_regime_imputed = "Netherlands" if country_name == "Belgium" & year >= 1814 & year <= 1829
* Lithuania 1940-1989: imperial power Russia 1940-1990 (Wimmer and Min 2006), part of Russia 1940-1991 (CShapes 2.0), independent 1918-1940, 1991- (Butcher and Griffiths 2020).
replace country_name_regime_imputed = "Russia" if country_name == "Lithuania" & year >= 1940 & year <= 1989
* Puerto Rico ..., 1940, 1950-2021: colony of Spain since at least 1886-1898, colony of United States 1899- (CShapes 2.0), colony of Spain since 16th century (Encyclopedia Britannica); I favor no imputation.
* Turkmenistan 1789-1989: imperial power Russia 1897-1990 (Wimmer and Min 2006), (mostly) part of Russia since 1886-1991, part protectorate Khiva 1886-1920 (Cshapes 2.0), not colonized (Ertan et al. 2016), resistance against Russia broken in 1881 (Encyclopedia Britannica).
replace country_name_regime_imputed = "Russia" if country_name == "Turkmenistan" & year >= 1886 & year <= 1989
* Armenia 1789-1989: mixed rule 17th century-1917, 1918-1990 Russia (Wimmer and Min 2006), part of Russia 1886-1991 (Cshapes 2.0); I favor no imputation for early years.
replace country_name_regime_imputed = "Russia" if country_name == "Armenia" & year >= 1918 & year <= 1989
* Uganda 1789-1899: part of Kenya, protectorate of United Kingdom 1892-1894 (CShapes 2.0); own protectorate of United Kingdom 1895-1962; imperial power United Kingdom 1890-1961 (Wimmer and Min 2006); I favor no imputation.
* Iraq 1789-1919: part of Turkey 1886-1920, mandate of United Kingdom 1921-1933 (CShapes 2.0); imperial power Turkey 16th century-1913, imperial power United Kingdom 1914-1931 (Wimmer and Min 2006).
replace country_name_regime_imputed = "Turkey" if country_name == "Iraq" & year >= 1789 & year <= 1919
* Yemen 1851-1917: mixed rule by Turkey and United Kingdom 1849-1918, part of Turkey 1886-1918 (CShapes 2.0), United Kingdom not on CShapes map.
replace country_name_regime_imputed = "Turkey" if country_name == "Yemen" & year >= 1851 & year <= 1917
* Angola 1789-1899: colony of Portugal 1886-1975 (CShapes 2.0); colony of imperial power Portugal 16th century-1974 (Wimmer and Min 2006); I favor no imputation.
* Bulgaria 1789-1877: imperial power Turkey 15th century-1878, independent in 1886 (CShapes 2.0).
replace country_name_regime_imputed = "Turkey" if country_name == "Bulgaria" & year >= 1789 & year <= 1877
* Lithuania 1789-1917: part of Russia 1886-1918 and 1941-1991 (CShapes 2.0), imperial power Russia 1795-1918 (Wimmer and Min 2006).
replace country_name_regime_imputed = "Russia" if country_name == "Lithuania" & year >= 1795  & year <= 1917
* Cambodia 1789-1899: colonized by France 1886-1953 (CShapes 2.0), imperial power France 1857-1952 (Wimmer and Min 2006), colonized in 1863 (Ertan et al. 2016); I favor no imputation.
* Taiwan 1789-1899: part of China 1886-1895, colony of Japan afterwards (CShapes 2.0), imperial power China 17th century - 1947 (Wimmer and Min 2006), colonized by Japan 1895-1945 (Ertan et al. 2016).
replace country_name_regime_imputed = "China" if country_name == "Taiwan" & year >= 1789 & year <= 1894
* Ghana 1789-1901: colonized by United Kingdom 1886-1957 (CShapes 2.0), imperial power Portugal 15th century - 1823, United Kingdom 1874-1956 (Wimmer and Min 2006); I favor no imputation.
* Latvia 1789-1919, 1940-1989: part of Russia 1886-1918 and 1941-1991 (CShapes 2.0), imperial power Russia 1710-1918 and 1940-1990 (Wimmer and Min 2006); I include 1919.
replace country_name_regime_imputed = "Russia" if country_name == "Latvia" & year >= 1789 & year <= 1919
replace country_name_regime_imputed = "Russia" if country_name == "Latvia" & year >= 1940 & year <= 1989
* Mali 1789-1899: colonized by France since 1896 (CShapes 2.0), imperial power France since 1895 (Wimmer and Min 2006); I favor no imputation.
* Syria 1789-1917, 1920-1921: part of Turkey 1886-1920 (CShapes 2.0), imperial power Turkey 1840-1919, France 1920-1943 (Wimmer and Min 2006), colonized by France in 1920 (Ertan et al. 2016), part of of Ottoman Empire 16th century-1830, of Egypt 1831-1839 (Encyclopedia Britannica).
replace country_name_regime_imputed = "Turkey" if country_name == "Syria" & year >= 1789 & year <= 1830
replace country_name_regime_imputed = "Egypt" if country_name == "Syria" & year >= 1831 & year <= 1839
replace country_name_regime_imputed = "Turkey" if country_name == "Syria" & year >= 1840 & year <= 1917
* Malawi 1789-1899: colonized by United Kingdom 1892-1964 (CShapes 2.0), imperial power United Kingdom 1889-1963 (Wimmer and Min 2006); I favor no imputation.
* Netherlands 1811-1812: part of France (Encyclopedia Britannica)
replace country_name_regime_imputed = "France" if country_name == "Netherlands" & year >= 1811 & year <= 1812
* Saudi Arabia 1819-1821: part of Turkey 1886-1919, nothing 1920-1932 (CShapes 2.0), not included (Wimmer and Min 2006), not colonized (Ertan et al. 2016), independent 1816-1818 (Butcher and Griffiths 2020), part of Ottoman Empire (Encyclopedia Britannica).
replace country_name_regime_imputed = "Turkey" if country_name == "Saudi Arabia" & year >= 1819 & year <= 1821
* Malaysia 1789-1899: colonized by United Kingom 1886-1957, imperial power United Kingdom 1795-1956 (Wimmer and Min 2006); I favor no imputation.
* North Macedonia 1789-1990: part of Turkey 1886-1913, part of Serbia 1914-1915, occupied by Austria/Hungary 1916-1918, part of Yugoslavia 1919-1991 (CShapes 2.0); imperial power Turkey 14th century -1913, Yugoslavia 1914-1990 (Wimmer and Min 2006).
replace country_name_regime_imputed = "Turkey" if country_name == "North Macedonia" & year >= 1789 & year <= 1913
replace country_name_regime_imputed = "Serbia" if country_name == "North Macedonia" & year >= 1914 & year <= 1990
* Slovenia 1789-1988: part of Austria-Hungary 1886-1918, of Austria 1919, of Yugoslavia 1920-1992 (CShapes 2.0), imperial power Austria-Hungary 1804-1917, Yugoslavia 1918-1990 (Wimmer and Min 2006), appears more closely affiliated with Austria, as Hungary barely referenced (Encyclopedia Britannica).
replace country_name_regime_imputed = "Serbia" if country_name == "Slovenia" & year >= 1919 & year <= 1988
replace country_name_regime_imputed = "Austria" if country_name == "Slovenia" & year >= 1804 & year <= 1918
* Chad 1789-1919: colonized by France 1900-1960 (CShapes 2.0), imperial power Sudan 1805-1889, France 1890-1959 (Wimmer and Min 2006); I favor no imputation.
* Burundi 1789-1915: imperial power Germany 1890-1922, Belgium 1923-1961 (Wimmer and Min 2006); I favor no imputation.
* Finland 1789-1862: part of Russia 1886-1916 (CShapes 2.0), imperial power Russia 1809-1916 (Wimmer and Min 2006), independence in 1917 (Butcher and Griffiths 2020), part of Sweden 14th century-1808.
replace country_name_regime_imputed = "Sweden" if country_name == "Finland" & year >= 1789 & year <= 1808
replace country_name_regime_imputed = "Russia" if country_name == "Finland" & year >= 1809 & year <= 1862
* Canada 1789-1840: independent since 1886 (CShapes 2.0), imperial power United Kingdom 1763-1866, colonized by Britain and France in 1700 (Ertan et al. 2016); I favor no imputation. 
* Niger 1789-1921: colony of Frange 1896-1960 (CShapes 2.0), imperial power France 1904-1959 (Wimmer and Min 2006); I favor no imputation.
* Madagascar 1789-1816: independent 1886-1896 (CShapes 2.0), imperial power France 1894-1959 (Wimmer and Min 2006), independent 1816-1895 (Butcher and Griffiths 2020), no indication of being part of another country 1789-1816 (Encyclopedia Britannica); I favor no imputation.
* Zambia 1789-1910: colonized by United Kingom 1892-1964 (Cshapes 2.0), imperial power United Kingdom 1890-1963 (Wimmer and Min 2006); I favor no imputation.
* Rwanda 1789-1915: colonized by Germany 1891-1916 (CShapes 2.0), imperial power Germany 1890-1915 (Wimmer and Min 2006); I favor no imputation.
* Estonia 1789-1917, 1940-1989: part of Russia 1886-1918, 1941-1991 (CShapes 2.0), imperial power Russia 1710-1918, 1940-1990 (Wimmer and Min 2006)
replace country_name_regime_imputed = "Russia" if country_name == "Estonia" & year >= 1789 & year <= 1917
replace country_name_regime_imputed = "Russia" if country_name == "Estonia" & year >= 1940 & year <= 1989
* Somalia 1789-1899: colonized by United Kingdom 1886-1961, Italy 1890-1941 (CShapes 2.0), imperial power Turkey 1870-1883, United Kingdom 1884-1888, mixed rule 1889-1941 (Wimmer and Min 2006), occupied by Egypt 1870-1885 (Encyclopedia Britannica); I favor no imputation.
* Guinea 1789-1899: colonized by France 1893-1958 (CShapes 2.0), imperial power France 1849-1957 (Wimmer and Min 2006); I favor no imputation.
* Cote d'Ivoire 1789-1899: colonized by France 1890-1961 (CShapes 2.0), colonized by France 1887-1959 (Wimmer and Min 2006); I favor no imputation.
* Senegal 1789-1903: colonized by France 1886-1961 (CShapes 2.0), imperial power France 1854-1959 (Wimmer and Min 2006); I favor no imputation.
* Laos 1789-1899: part of Thailand 1886-1893, colonized by France 1894-1954 (CShapes 2.0), imperial power Thailand 1778-1889, France 1890-1952 (Wimmer and Min 2006).
replace country_name_regime_imputed = "Thailand" if country_name == "Laos" & year >= 1789 & year <= 1892
* Peru 1789-1820: imperial power Spain 16th century - 1824 (Wimmer and Min 2006), independence in 1821 (Butcher and Griffiths 2020); I favor no imputation.
* Colombia 1789-1809: imperial power Spain 16th century - 1820 (Wimmer and Min 2006), independence in 1819 (Butcher and Griffiths 2020); I favor no imputation.
* Benin 1789-1899: colonized by France 1895-1961 (CShapes 2.0), imperial power 1863-1959 (Wimmer and Min 2006); I favor no imputation.
* Bolivia 1789-1824: imperial power Spain 16th century - 1823 (Wimmer and Min 2006), independence in 1825 (Butcher and Griffiths 2020); I favor no imputation.
* Libya 1912-1913, 1915-1921, 1942-1950: part of Turkey 1886-1912, colonized by Italy 1913-1943, occupied by United Kingdom 1944-1951 (CShapes 2.0), not included (Wimmer and Min 2006), independent 1816-1835 (Butcher and Griffiths 2020); I favor no imputation.
* Israel 1789-1947: part of Turkey 1886-1920, occupied by United Kingdom 1921-1948 (CShapes 2.0), imperial power Turkey 1516-1916, United Kingdom 1917-1947 (Wimmer and Min 2006).
replace country_name_regime_imputed = "Turkey" if country_name == "Israel" & year >= 1789 & year <= 1919
* Sierra Leone 1789-1899: imperial power United Kingdom 1808-1960 (Wimmer and Min 2006), colonized by United Kingdom in 1808/1896 (Ertan et al. 2016); I favor no imputation.
* Zimbabwe 1789-1899: colonized by United Kingdom 1889-1965 (CShapes 2.0), imperial power United Kingdom 1890-1964 (Wimmer and Min 2006); I favor no imputation.
* Papua New Guinea 1789-1899: colonized by United Kingdom 1886-1920 and Germany 1886-1914, Australia 1915-1975 (CShapes 2.0), imperial power United Kingdom 1883-1904, Australia 1905-1974 (Wimmer and Min 2006), colonized by United Kingdom and Germany in 1884 (Ertan et al. 2016); I favor no imputation.
* Central African Republic 1789-1919: colonized by France 1900-1961 (CShapes 2.0), imperial power France 1890-1959 (Wimmer and Min 2006), colonized by France in 1887/1903 (Ertan et al. 2016); I favor no imputation.


** Identify which observations in the dataset do not have any V-Dem information:
* I do not want to impute data for observations where V-Dem coders provide (partial) information, even if the sources above suggest that the country was part of another entity. This is because partial information suggests the remaining missings are not because the country was considered to be part of another country, but for other reasons.
egen nonmissing_values = rownonmiss(country_name year regime_row_owid regime_redux_row_owid regime_amb_row_owid electmulpar_row electmulpar_high_row electmulpar_low_row electmulpar_leg_row electmulpar_leg_high_row electmulpar_leg_low_row electmulpar_hoe_row_owid electmulpar_hoe_high_row_owid electmulpar_hoe_low_row_owid electfreefair_row electfreefair_high_row electfreefair_low_row electdem_dich_row_owid electdem_dich_high_row_owid electdem_dich_low_row_owid accessjust_m_row accessjust_m_high_row accessjust_m_low_row accessjust_w_row accessjust_w_high_row accessjust_w_low_row transplaws_row transplaws_high_row transplaws_low_row lib_dich_row lib_dich_high_row lib_dich_low_row ///
	electdem_vdem electdem_vdem_low electdem_vdem_high libdem_vdem libdem_vdem_low libdem_vdem_high participdem_vdem participdem_vdem_low participdem_vdem_high delibdem_vdem delibdem_vdem_low delibdem_vdem_high egaldem_vdem egaldem_vdem_low egaldem_vdem_high ///
	freeexpr_vdem freeexpr_vdem_low freeexpr_vdem_high freeassoc_vdem freeassoc_vdem_low freeassoc_vdem_high suffr_vdem electfreefair_vdem electfreefair_vdem_low electfreefair_vdem_high electoff_vdem ///
	lib_vdem lib_vdem_low lib_vdem_high civlib_vdem civlib_vdem_low civlib_vdem_high judicial_constr_vdem judicial_constr_vdem_low judicial_constr_vdem_high legis_constr_vdem legis_constr_vdem_low legis_constr_vdem_high ///
	particip_vdem particip_vdem_low particip_vdem_high civsoc_particip_vdem civsoc_particip_vdem_low civsoc_particip_vdem_high dirpop_vote_vdem locelect_vdem locelect_vdem_low locelect_vdem_high regelect_vdem regelect_vdem_low regelect_vdem_high ///
	delib_vdem delib_vdem_low delib_vdem_high justified_polch_vdem justified_polch_vdem_low justified_polch_vdem_high justcomgd_polch_vdem justcomgd_polch_vdem_low justcomgd_polch_vdem_high counterarg_polch_vdem counterarg_polch_vdem_low counterarg_polch_vdem_high elitecons_polch_vdem elitecons_polch_vdem_low elitecons_polch_vdem_high soccons_polch_vdem soccons_polch_vdem_low soccons_polch_vdem_high ///
	egal_vdem egal_vdem_low egal_vdem_high equal_rights_vdem equal_rights_vdem_low equal_rights_vdem_high equal_access_vdem equal_access_vdem_low equal_access_vdem_high equal_res_vdem equal_res_vdem_low equal_res_vdem_high ///
	turnout_vdem goveffective_vdem_wbgi), strok

generate empty_observation = 1 if nonmissing_values == 2 // The two non-missing values are country and year.                    
                    

** Merge with V-Dem dataset again, this time on imputing countries:

rename country_name country_name_temp
rename country_name_regime_imputed country_name
sort country_name year

* I do not merge with the 'merge, update', as in that case some observations will have different non-missing values between the non-imputed and the imputed variables (due to partial V-Dem coverage). I therefore have to use a more manual approach.

rename electmulpar_hoe_high_row_owid electmulpar_hoe_h_row_owid
rename electmulpar_hoe_low_row_owid electmulpar_hoe_l_row_owid
foreach var of varlist regime_row_owid regime_redux_row_owid regime_amb_row_owid electmulpar_row electmulpar_high_row electmulpar_low_row electmulpar_leg_row electmulpar_leg_high_row electmulpar_leg_low_row electmulpar_hoe_row_owid electmulpar_hoe_h_row_owid electmulpar_hoe_l_row_owid electfreefair_row electfreefair_high_row electfreefair_low_row electdem_dich_row_owid electdem_dich_high_row_owid electdem_dich_low_row_owid accessjust_m_row accessjust_m_high_row accessjust_m_low_row accessjust_w_row accessjust_w_high_row accessjust_w_low_row transplaws_row transplaws_high_row transplaws_low_row lib_dich_row lib_dich_high_row lib_dich_low_row ///
	electdem_vdem electdem_vdem_low electdem_vdem_high libdem_vdem libdem_vdem_low libdem_vdem_high participdem_vdem participdem_vdem_low participdem_vdem_high delibdem_vdem delibdem_vdem_low delibdem_vdem_high egaldem_vdem egaldem_vdem_low egaldem_vdem_high ///
	freeexpr_vdem freeexpr_vdem_low freeexpr_vdem_high freeassoc_vdem freeassoc_vdem_low freeassoc_vdem_high suffr_vdem electfreefair_vdem electfreefair_vdem_low electfreefair_vdem_high electoff_vdem ///
	lib_vdem lib_vdem_low lib_vdem_high civlib_vdem civlib_vdem_low civlib_vdem_high judicial_constr_vdem judicial_constr_vdem_low judicial_constr_vdem_high legis_constr_vdem legis_constr_vdem_low legis_constr_vdem_high ///
	particip_vdem particip_vdem_low particip_vdem_high civsoc_particip_vdem civsoc_particip_vdem_low civsoc_particip_vdem_high dirpop_vote_vdem locelect_vdem locelect_vdem_low locelect_vdem_high regelect_vdem regelect_vdem_low regelect_vdem_high ///
	delib_vdem delib_vdem_low delib_vdem_high justified_polch_vdem justified_polch_vdem_low justified_polch_vdem_high justcomgd_polch_vdem justcomgd_polch_vdem_low justcomgd_polch_vdem_high counterarg_polch_vdem counterarg_polch_vdem_low counterarg_polch_vdem_high elitecons_polch_vdem elitecons_polch_vdem_low elitecons_polch_vdem_high soccons_polch_vdem soccons_polch_vdem_low soccons_polch_vdem_high ///
	egal_vdem egal_vdem_low egal_vdem_high equal_rights_vdem equal_rights_vdem_low equal_rights_vdem_high equal_access_vdem equal_access_vdem_low equal_access_vdem_high equal_res_vdem equal_res_vdem_low equal_res_vdem_high ///
	turnout_vdem goveffective_vdem_wbgi {
rename `var' `var'_owid
}

merge m:1 country_name year using "democracy/datasets/cleaned/vdem_row_cleaned.dta"
drop if _merge == 2
drop _merge

rename country_name regime_imputed_country_vdem_owid
rename country_name_temp country_name


** Create variable identifying whether regime data is imputed:
generate regime_imputed_vdem_owid = .
replace regime_imputed_vdem_owid = 0 if regime_imputed_country_vdem_owid == "" | empty_observation != 1
replace regime_imputed_vdem_owid = 1 if regime_imputed_country_vdem_owid != "" & empty_observation == 1
order regime_imputed_vdem_owid, before(regime_imputed_country_vdem_owid)

replace regime_imputed_country_vdem_owid = "" if regime_imputed_vdem_owid == 0

label variable regime_imputed_country_vdem_owid "Name of the country from which V-Dem regime information was imputed"
label variable regime_imputed_vdem_owid "V-Dem regime information imputed from another country"


** Update variable identifying whether observation includes V-Dem information:
replace vdem_obs = 1 if regime_imputed_vdem_owid == 1


** Create variable identifying whether country includes V-Dem information:
bysort country_name: egen vdem_country = max(vdem_obs)


** Add imputed values for variables:

rename electmulpar_hoe_high_row_owid electmulpar_hoe_h_row_owid
rename electmulpar_hoe_low_row_owid electmulpar_hoe_l_row_owid
foreach var of varlist regime_row_owid regime_redux_row_owid regime_amb_row_owid electmulpar_row electmulpar_high_row electmulpar_low_row electmulpar_leg_row electmulpar_leg_high_row electmulpar_leg_low_row electmulpar_hoe_row_owid electmulpar_hoe_h_row_owid electmulpar_hoe_l_row_owid electfreefair_row electfreefair_high_row electfreefair_low_row electdem_dich_row_owid electdem_dich_high_row_owid electdem_dich_low_row_owid accessjust_m_row accessjust_m_high_row accessjust_m_low_row accessjust_w_row accessjust_w_high_row accessjust_w_low_row transplaws_row transplaws_high_row transplaws_low_row lib_dich_row lib_dich_high_row lib_dich_low_row ///
	electdem_vdem electdem_vdem_low electdem_vdem_high libdem_vdem libdem_vdem_low libdem_vdem_high participdem_vdem participdem_vdem_low participdem_vdem_high delibdem_vdem delibdem_vdem_low delibdem_vdem_high egaldem_vdem egaldem_vdem_low egaldem_vdem_high ///
	freeexpr_vdem freeexpr_vdem_low freeexpr_vdem_high freeassoc_vdem freeassoc_vdem_low freeassoc_vdem_high suffr_vdem electfreefair_vdem electfreefair_vdem_low electfreefair_vdem_high electoff_vdem ///
	lib_vdem lib_vdem_low lib_vdem_high civlib_vdem civlib_vdem_low civlib_vdem_high judicial_constr_vdem judicial_constr_vdem_low judicial_constr_vdem_high legis_constr_vdem legis_constr_vdem_low legis_constr_vdem_high ///
	particip_vdem particip_vdem_low particip_vdem_high civsoc_particip_vdem civsoc_particip_vdem_low civsoc_particip_vdem_high dirpop_vote_vdem locelect_vdem locelect_vdem_low locelect_vdem_high regelect_vdem regelect_vdem_low regelect_vdem_high ///
	delib_vdem delib_vdem_low delib_vdem_high justified_polch_vdem justified_polch_vdem_low justified_polch_vdem_high justcomgd_polch_vdem justcomgd_polch_vdem_low justcomgd_polch_vdem_high counterarg_polch_vdem counterarg_polch_vdem_low counterarg_polch_vdem_high elitecons_polch_vdem elitecons_polch_vdem_low elitecons_polch_vdem_high soccons_polch_vdem soccons_polch_vdem_low soccons_polch_vdem_high ///
	egal_vdem egal_vdem_low egal_vdem_high equal_rights_vdem equal_rights_vdem_low equal_rights_vdem_high equal_access_vdem equal_access_vdem_low equal_access_vdem_high equal_res_vdem equal_res_vdem_low equal_res_vdem_high ///
	turnout_vdem goveffective_vdem_wbgi {
replace `var'_owid = `var' if regime_imputed_vdem_owid == 1
}
 
drop nonmissing_values empty_observation regime_row_owid regime_redux_row_owid regime_amb_row_owid electmulpar_row electmulpar_high_row electmulpar_low_row electmulpar_leg_row electmulpar_leg_high_row electmulpar_leg_low_row electmulpar_hoe_row_owid electmulpar_hoe_h_row_owid electmulpar_hoe_l_row_owid electfreefair_row electfreefair_high_row electfreefair_low_row electdem_dich_row_owid electdem_dich_high_row_owid electdem_dich_low_row_owid accessjust_m_row accessjust_m_high_row accessjust_m_low_row accessjust_w_row accessjust_w_high_row accessjust_w_low_row transplaws_row transplaws_high_row transplaws_low_row lib_dich_row lib_dich_high_row lib_dich_low_row electdem_vdem electdem_vdem_low electdem_vdem_high libdem_vdem libdem_vdem_low libdem_vdem_high participdem_vdem participdem_vdem_low participdem_vdem_high delibdem_vdem delibdem_vdem_low delibdem_vdem_high egaldem_vdem egaldem_vdem_low egaldem_vdem_high freeexpr_vdem freeexpr_vdem_low freeexpr_vdem_high freeassoc_vdem freeassoc_vdem_low freeassoc_vdem_high suffr_vdem electfreefair_vdem electfreefair_vdem_low electfreefair_vdem_high electoff_vdem lib_vdem lib_vdem_low lib_vdem_high civlib_vdem civlib_vdem_low civlib_vdem_high judicial_constr_vdem judicial_constr_vdem_low judicial_constr_vdem_high legis_constr_vdem legis_constr_vdem_low legis_constr_vdem_high particip_vdem particip_vdem_low particip_vdem_high civsoc_particip_vdem civsoc_particip_vdem_low civsoc_particip_vdem_high dirpop_vote_vdem locelect_vdem locelect_vdem_low locelect_vdem_high regelect_vdem regelect_vdem_low regelect_vdem_high delib_vdem delib_vdem_low delib_vdem_high justified_polch_vdem justified_polch_vdem_low justified_polch_vdem_high justcomgd_polch_vdem justcomgd_polch_vdem_low justcomgd_polch_vdem_high counterarg_polch_vdem counterarg_polch_vdem_low counterarg_polch_vdem_high elitecons_polch_vdem elitecons_polch_vdem_low elitecons_polch_vdem_high soccons_polch_vdem soccons_polch_vdem_low soccons_polch_vdem_high turnout_vdem egal_vdem egal_vdem_low egal_vdem_high equal_rights_vdem equal_rights_vdem_low equal_rights_vdem_high equal_access_vdem equal_access_vdem_low equal_access_vdem_high equal_res_vdem equal_res_vdem_low equal_res_vdem_high goveffective_vdem_wbgi

rename regime_row_owid_owid regime_row_owid
rename regime_redux_row_owid_owid regime_redux_row_owid
rename regime_amb_row_owid_owid regime_amb_row_owid

rename electmulpar_hoe_row_owid_owid electmulpar_hoe_row_owid
rename electmulpar_hoe_h_row_owid_owid electmulpar_hoe_high_row_owid 
rename electmulpar_hoe_l_row_owid_owid electmulpar_hoe_low_row_owid

rename electdem_dich_row_owid_owid electdem_dich_row_owid
rename electdem_dich_high_row_owid_owid electdem_dich_high_row_owid
rename electdem_dich_low_row_owid_owid electdem_dich_low_row_owid

** Keep countries and observations of interest:
drop if vdem_country == 0
drop if vdem_obs == 0
drop vdem_country vdem_obs


** Export data:
save "democracy/datasets/imputed/vdem_row_imputed.dta", replace
export delimited "democracy/datasets/imputed/vdem_row_imputed.csv", replace



exit
