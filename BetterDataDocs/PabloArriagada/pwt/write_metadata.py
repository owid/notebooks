# Currently this is step is redundant (I'm saving a csv in Google sheets in s3).

# The point is just to demo the idea that metadata authored in 
# google sheets can then be added to the database.

# %%
import pandas as pd

# Acess keys to write to  our s3 cloud storage
from joes_key import KEY_ID, SECRET_KEY 

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


# Read in metadata from google sheet

# %%
# Specify sheet id and sheet (tab) name for the metadata google sheet 
sheet_id = '1gbk8lBc4ZTjzE94pG8vgFX1Ta5baIQhpdD158GhPJsc'
var_meta_sheetname = 'variable_metadata'
data_meta_sheetname = 'dataset_metadata'

# Read in variable metadata as dataframe
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={var_meta_sheetname}'
df_variable_metadata = pd.read_csv(url)

# Read in dataset metadata as dataframe
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={data_meta_sheetname}'
df_dataset_metadata = pd.read_csv(url)

# Write both to s3
upload_to_s3(df_variable_metadata, 'pwt', 'variable_metadata.csv')
upload_to_s3(df_dataset_metadata, 'pwt', 'dataset_metadata.csv')