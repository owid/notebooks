# Code and datasets on political regimes

This repository contains the code written and datasets created for my projects at Our World In Data which use data on political regimes.


The data are used in the following posts:
- [200 years ago, everyone lacked democratic rights. Now, more than a billion people have them.](https://ourworldindata.org/democratic-rights)
- [The ‘Regimes of the World’ data: how do researchers identify which countries are democracies?](https://ourworldindata.org/regimes-of-the-world-data)
- [In most countries, democracy is a recent achievement. Dictatorship is far from a distant memory](https://ourworldindata.org/democracies-age)

`regimes_owid.csv` and `regimes_owid.dta` include the following variables:
- `country_name`: country name
- `year`: year
- `regime_row_owid`: political regime based on [Lührmann et al. (2018)](https://www.cogitatiopress.com/politicsandgovernance/article/view/1214/0), using data from [V-Dem (v11.1)](https://www.v-dem.net/en/data/data/v-dem-dataset-v111/) and my coding in `regimes_owid.do`; 0 = closed autocracy, 1 = electoral autocracy, 2 = electoral democracy, 3 = liberal democracy.
- `electdem_age_row_owid`: age of electoral democracy, based on `regime_row_owid`
- `electdem_age_group_row_owid`: age group of electoral democracy, based on `electdem_age_row_owid`
- `libdem_age_row_owid`: age of liberal democracy, based on `regime_row_owid`
- `libdem_age_group_row_owid`: age group of liberal democracy, based on `libdem_age_row_owid`
- `electdem_vdem_owid`: electoral democracy, central estimate, using Data from [V-Dem (v11.1)](https://www.v-dem.net/en/data/data/v-dem-dataset-v111/) and my imputations in `regimes_owid.do`
- `electfreefair_vdem_owid`: free and fair elections, central estimate, using Data from [V-Dem (v11.1)](https://www.v-dem.net/en/data/data/v-dem-dataset-v111/) and my imputations in `regimes_owid.do`
- `electfreefair_vdem_owid_low`: free and fair elections, lower bound
- `electfreefair_vdem_owid_high`: free and fair elections, upper bound
- `suffr_vdem_owid`: suffrage, using Data from [V-Dem (v11.1)](https://www.v-dem.net/en/data/data/v-dem-dataset-v111/) and my imputations in `regimes_owid.do`
- `electoff_vdem_owid`: elected officials, using Data from [V-Dem (v11.1)](https://www.v-dem.net/en/data/data/v-dem-dataset-v111/) and my imputations in `regimes_owid.do`
- `freeexpr_vdem_owid`: freedom of expression and alternative sources of information, central estimate, using Data from [V-Dem (v11.1)](https://www.v-dem.net/en/data/data/v-dem-dataset-v111/) and my imputations in `regimes_owid.do`
- `freeexpr_vdem_owid_low`: freedom of expression and alternative sources of information, lower bound
- `freeexpr_vdem_owid_high`: freedom of expression and alternative sources of information, upper bound
- `freeassoc_vdem_owid`: freedom of association, central estimate, using Data from [V-Dem (v11.1)](https://www.v-dem.net/en/data/data/v-dem-dataset-v111/) and my imputations in `regimes_owid.do`
- `freeassoc_vdem_owid_low`: freedom of association, lower bound
- `freeassoc_vdem_owid_high`: freedom of association, upper bound
- `regime_row_imputed`: regime information imputed from another country; 1 = yes, 0 = no.
- `regime_row_imputed_country_name`: name of the country from which regime information was imputed.

`regimes_number_owid.csv` and `regimes_number_owid.dta` include the following variables:
- `entity_name`: entity name
- `year`: Year
- `number_electdem_0`: Number of countries which are not electoral democracies.
- `number_electdem_18`: Number of electoral democracies aged 1-18 years.
- `number_electdem_30`: Number of electoral democracies aged 19-30 years.
- `number_electdem_60`: Number of electoral democracies aged 31-60 years.
- `number_electdem_90`: Number of electoral democracies aged 61-90 years.
- `number_electdem_91plus`: Number of electoral democracies aged 91 years or older.
- `number_libdem_0`: Number of countries which are not liberal democracies.
- `number_electdem_18`: Number of liberal democracies aged 1-18 years.
- `number_electdem_30`: Number of liberal democracies aged 19-30 years.
- `number_electdem_60`: Number of liberal democracies aged 31-60 years.
- `number_electdem_90`: Number of liberal democracies aged 61-90 years.
- `number_electdem_91plus`: Number of liberal democracies aged 91 years or older.

`regimes_population_owid.csv` and `regimes_population_owid.dta` include the following variables:
- `entity_name`: entity name
- `year`: Year
- `population_closed_aut`: number of people living in closed autocracies.
- `population_electoral_aut`: number of people living in electoral autocracies.
- `population_electoral_dem`: number of people living in electoral democracies.
- `population_liberal_dem`: number of people living in liberal democracies.
- `population_missing_data`: number of people living in countries without regime data.