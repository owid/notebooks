This contains a script to generate three charts to show how cancer mortality varies with age:

1. Death rates from each cancer, by age
2. Relative share of cancer deaths from each cancer, by age
3. Number of deaths from each cancer, by age

The dataset I (Saloni) saved is from 2018 to 2022 and can be downloaded from the CDC Wonder database at: https://wonder.cdc.gov/controller/saved/D158/D406F321

You can update the chart with new data from the CDC Wonder database here: https://wonder.cdc.gov/ using the following steps:

- Go to Underlying cause of death -> group by: single-year age group, ICD-10 113 Cause List
- In section 6, click ICD-10 113 Cause list
- Highlight #Malignant neoplasms until #In situ neoplasms
- Download and save to data_folder

The output plot is also available in the folder.

Note: Categories are not shown when the total number of deaths per single-year age group was less than 10, according to CDC Wonder's terms of use.

**Update log**
- 9 May 2025: I identified a coding error in the data on lymphatic and blood cancers and corrected it.
  - The error meant that the category 'lymphatic and blood cancers' wrongly included the category lymphoid and blood cancers `(C81-C96)`, plus its subcategories aside from leukemia — i.e. lymphoid and blood cancers `(C81, C82–C85, C88, C90, C96)`. This meant that it was double counting many cases.
  - In the correction, I removed the lymphoid and blood cancers category `(C81-C96)` while keeping the non-leukemia subcategories `(C81, C82–C85, C88, C90, C96)`.
  - This error greatly changed the share of cancers in the lymphatic and blood cancers category shown in the chart.
