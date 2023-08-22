This contains two scripts to generate plots of per-day mortality after birth.

1) England and Wales (1921-2021)

This plot shows data for infants in England and Wales, between 1921 and 2021.

Data comes from the Office for National Statistics, from two files.

The python script generates per-day mortality rates from intervals (e.g. Under 1 day, Between 1 day and 1 week, Between 1 week and 1 month, etc.) and then plots these as dots. It also generates an interpolated line for each year, to connect Age (days) and Mortality, using a log-log space.

2) USA (2017-2020)

This plot shows data for infants in the United States of America, across 2017-2020 (merged).

Data comes from the US Centers for Disease Control and Prevention, via the CDC Wonder.

The python script plots per-day mortality rates over the first 360 days of birth.
