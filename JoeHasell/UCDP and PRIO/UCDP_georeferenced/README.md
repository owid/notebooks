This folder contains three notebooks that do the following:

- `join_UCDP_datasets.ipynb` combines two UCDP datasets of georeferenced conflict events: the official, main dataset and also the 'candidate' dataset that includes more recent events where a full assessment is yet to be made by UCDP.  
- `ucdp_country_extract.ipynb` assigns countries to the events contained in the UCDP data, using the Natural Earth shape files to define country borders. This is needed because the country entities coded in the original data relate to shifting boundaries.
- `Aggregate.ipynb` aggregates over events to get number of deaths and number of conflicts by country, year, and conflict-type. 
