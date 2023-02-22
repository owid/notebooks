This folder contains various notebooks relating to our use of UCDP and PRIO data - both current and planned.

Two sections are worth separating.

- The `/UCDP_georeferenced` folder contains notebooks that prepare data on conflict deaths and the number of conflicts by country – using fixed country borders (not the coutry entities used in the UCDP data itself). We do not use this data anywhere on OWID currently. But the code is in good shape and everything is working, so it should be a quick job. There is a Readme in that folder that explains things further.

- `Datasets from UCDP and PRIO.Rmd`, in the root directory contains the code I used to produce most of the charts on OWID using UCDP/PRIO data. HOWEVER, I was in the process of restructuring this script when worked stopped and other priorities took over. As things stand the code does not reproduce the final data files contained in `/output`.

Nevertheless, it contains snippets of code and lots of discussion of the different datasets that may be helpful in coming to update the UCDP data. Although, for this purpose of getting to know the data, I would suggest reading an even earlier version of the notebook rendered as HTML, which I have saved here: `older_notebooks/Datasets-from-UCDP-and-PRIO.html`. 

## What is not included here?
NB – This folder does not include scripts used to prepare the UCDP/PRIO data shown in this [comparison of sources chart](https://ourworldindata.org/grapher/conflict-deaths-per-100000-world-various-sources). The data and code used for that is stored in this folder in our old Google Drive storage system: https://drive.google.com/drive/u/1/folders/1zRuTbjcejHIQAIUOT-A6rMZHZ762_rRU.
