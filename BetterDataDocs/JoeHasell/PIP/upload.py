# %%
# ACCESS TO STORAGE ----

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


import pandas as pd


# Grab the prepped percentile data
df = pd.read_csv('clean_data/percentiles_filled.csv')

# %% 
# Here we save it as a csv to our s3 storage.
upload_to_s3(df, 'PIP', 'percentiles_filled.csv')
