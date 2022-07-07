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

# %%
# Load packages

# Pandas is a standard package used for data manipulation in python code
import pandas as pd
               

# %%
# Load the original raw data file as a pandas dataframe. 
# (For the time being, this is in Joe's own Digital Ocean account).

url = 'https://joeh.fra1.digitaloceanspaces.com/pwt/pwt100-original.xlsx'

df = pd.read_excel(url, sheet_name='Data')

# %% [markdown]
# Here is the first few rows of the data:
# %%
df.head()



# %% [markdown]
# Here we save it as a csv to our s3 storage.
upload_to_s3(df, 'pwt', 'raw_dataframe.csv')
