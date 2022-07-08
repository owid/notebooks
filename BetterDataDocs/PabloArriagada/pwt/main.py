
print("Making dataframes...")
import make_dataframe

print("Standardizing entity names...")
from standardize_entities import standardize_and_save

print("Standardizing entity names in main data file...")
# Standardize entity names in main data file
standardize_and_save(
    raw_csv_url="https://joeh.fra1.digitaloceanspaces.com/pwt/raw_dataframe.csv",
    entity_mapping_url= "https://joeh.fra1.digitaloceanspaces.com/pwt/country_name_mapping.csv",
    mapping_varname_raw = 'country',
    mapping_vaname_owid = "Our World In Data Name",
    data_varname_old='country',
    data_varname_new='entity',
    s3_space_to_save_in='pwt',
    as_filename='entities_standardized.csv'
                    )

print("Standardizing entity names in national accounts data file...")
#Standardize entity names in national accounts data file
standardize_and_save(
    raw_csv_url="https://joeh.fra1.digitaloceanspaces.com/pwt/raw_dataframe_national_accounts.csv",
    entity_mapping_url= "https://joeh.fra1.digitaloceanspaces.com/pwt/country_name_mapping_national_accounts.csv",
    mapping_varname_raw = 'country',
    mapping_vaname_owid = "Our World In Data Name",
    data_varname_old='countrycode',
    data_varname_new='entity',
    s3_space_to_save_in='pwt',
    as_filename='entities_standardized_national_accounts.csv'
                    )

print("Preparing variables...")
import prepare_variables

print("Writing metadata...")
import write_metadata


