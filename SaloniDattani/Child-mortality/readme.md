This is a script to generate a plot of per-day mortality after birth, in infants in England and Wales.

Data comes from the Office for National Statistics, from two files.

The python script generates per-day mortality rates from intervals (e.g. Under 1 day, Between 1 day and 1 week, Between 1 week and 1 month, etc.) and then plots these as dots. It also generates an interpolated line for each year, to connect Age (days) and Mortality, using a log-log space.
