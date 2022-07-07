
from standardize_entities import standardize_and_save


standardize_and_save(
    raw_csv_url="https://joeh.fra1.digitaloceanspaces.com/pwt/raw_dataframe.csv",
    entity_mapping_url= "https://joeh.fra1.digitaloceanspaces.com/pwt/country_standardization_mapping.csv",
    entity_name_in_raw='country',
    resulting_entity_name='entity',
    s3_space_to_save_in='pwt',
    as_filename='entities_standardized.csv'
                    )


import prepare_variables

import write_metadata
