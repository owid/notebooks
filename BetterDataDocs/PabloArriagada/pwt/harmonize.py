
# --------- SET UP -----------
# Here we provide details of which libraries and packages we use to prepare the data


# %%
# Pandas is a standard package used for data manipulation in python code
import pandas as pd

# boto3  allows us to write data to our s3 cloud storage
import boto3


# Acess keys to write to  our s3 cloud storage
from joes_key import ENDPOINT, KEY_ID, SECRET_KEY 

# A function we have written to help upload our data to our s3 cloud storage
from functions import upload_to_s3


# Set up access for writing files to s3  
session = boto3.session.Session()

client = session.client('s3',
                        endpoint_url="https://{}.digitaloceanspaces.com".format(ENDPOINT),
                        aws_access_key_id=KEY_ID,
                        aws_secret_access_key=SECRET_KEY)




# ------- RUN –––––––––

# %%
# Load the 'Walden' data (for the time being in Joe's s3) 

url = 'https://joeh.fra1.digitaloceanspaces.com/pwt/pwt100-original.xlsx'

df_original = pd.read_excel(url, sheet_name='Data')


# %%
# Standardize country names
mapping_filename = 'country_standardization_mapping.csv'
entity_varname = 'country'
# %%
# Read in mapping csv – This needs to be two columns headed 'Original Name' and 'Our World In Data Name'
df_mapping = pd.read_csv(mapping_filename)

# %%
# Merge in the mapping to the main df
df_harmonized = pd.merge(df_original,df_mapping,
    left_on=entity_varname,right_on='Original Name', how='left')
    
# Drop the old entity names column, and the matching column from the mapping file
df_harmonized = df_harmonized.drop(columns=[entity_varname, 'Original Name'])
    
# Rename the new entity col as specefied in the args
df_harmonized = df_harmonized.rename(columns={'Our World In Data Name': entity_varname})
    
# Move entity variable to first column
# get a list of columns
cols = list(df_harmonized)
    
# move the column to head of list using index, pop and insert
cols.insert(0, cols.pop(cols.index(entity_varname)))
    
# use loc to reorder
df_harmonized = df_harmonized.loc[:, cols]


# %%
upload_to_s3(df_harmonized, 'pwt', 'harmonized.csv')


# %%