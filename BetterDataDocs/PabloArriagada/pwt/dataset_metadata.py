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


# Create a 'dictionary' (an array whose elements are named) for the dataset metadata
# This will end up in e.g. our database, 'Sources' tab etc.

#Pablo: Wouldn't it be better to have both dataset and variables' metadata together? Because this will be a very short script anyway

dataset_meta = {}

dataset_meta_fields = ['name', 'sourceName', 'link', 'description', 'dateRetrieved']

# Add dataset metadata to dictionary
dataset_meta['name'] = "Penn World Tables version 10.0"
dataset_meta['sourceName'] = "Penn World Tables"
dataset_meta['link'] = "https://www.rug.nl/ggdc/productivity/pwt"
dataset_meta['description'] = "PWT version 10.0 is a database with information \
on relative levels of income, output, input and productivity, covering 183 \
countries between 1950 and 2019."
dataset_meta['dateRetrieved'] = "dd/mm/2022"


# Convert dictionary to dataframe 
df = pd.DataFrame(dataset_meta, index=[0])

# Write to s3
upload_to_s3(df, 'pwt', 'dataset_meta.csv')


# %%
