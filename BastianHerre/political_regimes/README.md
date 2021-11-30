# Bastian Herre's code on political regimes

This repository contains the code and datasets for my projects at Our World In Data using data on political regimes.


The data are used in the following posts:
200 years ago, everyone lacked democratic rights. Now, more than a billion people have them.
The ‘Regimes of the World’ data: how do researchers identify which countries are democracies?
[The short history of global living conditions and why it matters that we know it](https://ourworldindata.org/a-history-of-global-living-conditions-in-5-charts)


`regimes.csv` and `regimes.dta` include the following variables:
| Variable                         | Description                                                          |
|:---------------------------------:----------------------------------------------------------------------|
| `country_name`                   | Country name |                                 
| `year     `                      | Year |                           
| `regime_row_owid`                | Political regime based on [Lührmann et al. (2018)](https://www.cogitatiopress.com/politicsandgovernance/article/view/1214/0), using data from [V-Dem (v11.1)](https://www.v-dem.net/en/data/data/v-dem-dataset-v111/) and my coding in `regimes_owid.do`; 0 = closed autocracy, 1 = electoral autocracy, 2 = electoral democracy, 3 = liberal democracy |                   
| `regime_imputed`                 | Regime imputed from another country; 1 = yes, 0 = no. |                        
| `country_name_regime_imputed`    | Name of the country from which regime was imputed |


`regimes_population.csv` and `regimes_population.dta` include the following variables:
| Variable                         | Description                                                          |
|:---------------------------------:----------------------------------------------------------------------|
| `entity`                         | Entity name |                                 
| `year`                           | Year |                           
| `population_closed_aut`          | Number of people living in closed autocracies |                   
| `population_electoral_aut`       | Number of people living in electoral autocracies |                   
| `population_electoral_dem`       | Number of people living in electoral democracies |                   
| `population_liberal_dem`         | Number of people living in liberal democracies |                   
| `population_missing_data`        | Number of people living in countries without regime data |