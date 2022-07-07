#%%
# Acess keys to write to  our s3 cloud storage
from access_key import KEY_ID, SECRET_KEY 

# boto3  allows us to write data to our s3 cloud storage
import boto3

# A function we have written to help upload our data to our s3 cloud storage
from functions import upload_to_s3

# Set up access for writing files to s3  
session = boto3.session.Session()

client = session.client('s3',
                        endpoint_url="https://joeh.fra1.digitaloceanspaces.com",
                        aws_access_key_id=KEY_ID,
                        aws_secret_access_key=SECRET_KEY)




#%%
import pandas as pd
#%%
raw_csv_url="https://joeh.fra1.digitaloceanspaces.com/pwt/raw_dataframe.csv"
entity_mapping_url= "https://joeh.fra1.digitaloceanspaces.com/pwt/country_standardization_mapping.csv"
entity_name_in_raw='country'
resulting_entity_name='entity'
s3_space_to_save_in='pwt'
as_filename='entities_standardized.csv'

#%%
# Read in raw dataframe
df_raw = pd.read_csv(raw_csv_url)

#%%

df_raw.head()
#%%

    # Read in mapping table which maps PWT names onto OWID names.
df_mapping = pd.read_csv(entity_mapping_url)
#%%
    # Merge in mapping to raw
df_harmonized = pd.merge(df_raw,df_mapping,
left_on=entity_name_in_raw,right_on='Original Name', how='left')
#%%
df_harmonized.head()
#%%    
    # Drop the old entity names column, and the matching column from the mapping file
df_harmonized = df_harmonized.drop(columns=[entity_name_in_raw, 'Original Name'])
#%%    
    # Rename the new entity column
df_harmonized = df_harmonized.rename(columns={'Our World In Data Name': resulting_entity_name})
#%%
    # Move the entity column to front:

    # get a list of columns
cols = list(df_harmonized)
    
    # move the country column to the first in the list of columns
cols.insert(0, cols.pop(cols.index(resulting_entity_name)))
    
    # reorder the columns of the dataframe according to the list
df_harmonized = df_harmonized.loc[:, cols]
#%%

names = df_harmonized[['countrycode', 'country', 'Our World In Data Name']]
names = names.drop_duplicates()
names.head()
len(names.index)
#%%
names.head()
#%%
upload_to_s3(names, 'pwt', 'country_standardization_mapping.csv')

#%%


    # Read in raw dataframe
df_raw = pd.read_csv(raw_csv_url)


    # Read in mapping table which maps PWT names onto OWID names.
df_mapping = pd.read_csv(entity_mapping_url)

    # Merge in mapping to raw
df_harmonized = pd.merge(df_raw,df_mapping,
      left_on=entity_name_in_raw,right_on='Original Name', how='left')
    
    # Drop the old entity names column, and the matching column from the mapping file
    df_harmonized = df_harmonized.drop(columns=[entity_name_in_raw, 'Original Name'])
    
    # Rename the new entity column
    df_harmonized = df_harmonized.rename(columns={'Our World In Data Name': resulting_entity_name})
