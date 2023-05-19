
This folder contains notebooks that prepare UCDP's georeferenced data on conflict *events* into data on conflict deaths and the number of conflicts, by *region* (UCDP-definitions), *year* and *type of violence*. 

## About the pipeline
This folder contains two notebooks that do the following:

- `import_and_tidy.ipynb` reads in the data and makes some small changes based on sense-checks.  
- `UCDP_region_aggregation.ipynb` aggregates over events to get number of deaths and number of conflicts by region, year, and conflict-type. 

Data is read in and saved to respective subfolders of `/data`. 

The final data uploaded to grapher (via fasttrack) is in `data/output`.