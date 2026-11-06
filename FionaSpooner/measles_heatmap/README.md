This folder contains R scripts needed to recreate a heatmap of measles case rates in the US, by state and year. You can see the chart [here](https://ourworldindata.org/measles-vaccines-save-lives#the-introduction-of-the-measles-vaccine-led-to-a-substantial-decline-in-cases).

Data comes from [Project Tycho](https://zenodo.org/records/11452259) and various reports by the U.S. Centers for Disease Control and Prevention.

The data used in the chart is available [here](https://catalog.ourworldindata.org/external/health/latest/measles_state_level/measles.csv), and each data point is annotated with the source of that data point.

Where needed, the reported measles cases were normalized by the population of the state in that year using the U.S. State population data from FRED. The code used to download this is available [here](https://github.com/owid/etl/blob/master/snapshots/demography/2026-11-06/us_state_population.py).

The latest years come from the preliminary counts on the CDC's [Measles Cases and Outbreaks](https://www.cdc.gov/measles/data-research/index.html) page, which can still be revised; the chart's footnote lists them. These count cases in the year the rash began, while earlier years mostly count them in the year they were reported. To plot a local copy of the data instead of the published file, set the `MEASLES_DATA` environment variable to its path.
