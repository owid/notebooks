This folder contains R scripts needed to recreate a heatmap of measles case rates in the US, by state and year. You can see the chart [here](https://ourworldindata.org/measles-vaccines-save-lives#the-introduction-of-the-measles-vaccine-led-to-a-substantial-decline-in-cases).

Data comes from [Project Tycho](https://zenodo.org/records/11452259) and various reports by the U.S. Centers for Disease Control and Prevention.

The data used in the chart is available [here](https://catalog.ourworldindata.org/external/health/latest/measles_state_level/measles.csv), and     each data point is annotated with the source of that data point.

Where needed, the reported measles cases were normalized by the population of the state in that year using the U.S. State population data from FRED. This was downloaded using the FRED API; the code used to do this is available [here](https://github.com/owid/etl/blob/master/snapshots/demography/2025-01-23/us_state_population.py), although you will need to set up a FRED API key to run it. Guidance is available [here](https://fred.stlouisfed.org/docs/api/fred/).
