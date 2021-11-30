# Code and datasets on political regimes

This repository contains the code written and datasets created for my projects at Our World In Data which use data on political regimes.


The data are used in the following posts:
- 200 years ago, everyone lacked democratic rights. Now, more than a billion people have them.
- The ‘Regimes of the World’ data: how do researchers identify which countries are democracies?
- [The short history of global living conditions and why it matters that we know it.](https://ourworldindata.org/a-history-of-global-living-conditions-in-5-charts)


`regimes_owid.csv` and `regimes_owid.dta` include the following variables:
- `country_name`: country name
- `year`: year
- `regime_row_owid`: political regime based on [Lührmann et al. (2018)](https://www.cogitatiopress.com/politicsandgovernance/article/view/1214/0), using data from [V-Dem (v11.1)](https://www.v-dem.net/en/data/data/v-dem-dataset-v111/) and my coding in `regimes_owid.do`; 0 = closed autocracy, 1 = electoral autocracy, 2 = electoral democracy, 3 = liberal democracy.
- `regime_row_imputed`: regime imputed from another country; 1 = yes, 0 = no.
- `regime_row_imputed_country_name`: name of the country from which regime was imputed.


`regimes_population_owid.csv` and `regimes_population_owid.dta` include the following variables:
- `entity_name`: entity name
- `year`: Year
- `population_closed_aut`: number of people living in closed autocracies.
- `population_electoral_aut`: number of people living in electoral autocracies.
- `population_electoral_dem`: number of people living in electoral democracies.
- `population_liberal_dem`: number of people living in liberal democracies.
- `population_missing_data`: number of people living in countries without regime data.