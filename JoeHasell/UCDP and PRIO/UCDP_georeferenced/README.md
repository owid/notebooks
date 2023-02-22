
This folder contains notebooks that prepare UCDP's georeferenced data on conflict *events* into data on conflict deaths and the number of conflicts *by country and year*. It uses a different set of country entities than that provided as standard in the dataset. The reson for doing this is that the countries provided in the original data represent entities whose borders shift over time. i.e. 'Sudan' covers a different geographical area depending on the year.

See https://github.com/owid/owid-issues/issues/165 for further discussion.
 
Note that the data work is basically done. However:
    - Contrary to the current code, I would recommend **not** including the UCDP *candidate* event dataset, and relying only the main 'official' GED dataset.
    - It could all do with sense checking and careful code review/a re-write. Fiona wrote the tricky notebook that maps the country shape files. I wrote ththe other two notebooks when I was just starting out with python, copying and pasting a lot from Fiona's. The pipeline should be seen as a draft.
    - There may well be new version of the GED data.
    - The data in this pipeline was downloaded manually. But there is also an API that might be more amenable to use.


## About the pipeline
This folder contains three notebooks that do the following:

- `join_UCDP_datasets.ipynb` combines two UCDP datasets of georeferenced conflict events: the official, main dataset and also the 'candidate' dataset that includes more recent events where a full assessment is yet to be made by UCDP.  
- `ucdp_country_extract.ipynb` assigns countries to the events contained in the UCDP data, using the Natural Earth shape files to define country borders. This is needed because the country entities coded in the original data relate to shifting boundaries.
- `Aggregate.ipynb` aggregates over events to get number of deaths and number of conflicts by country, year, and conflict-type. 
