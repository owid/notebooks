# %%

# %%
# Pandas is a standard package used for data manipulation in python code
import pandas as pd

# This package allows us to save a temporary file, 
# used in the process of uploading data to our s3 cloud storage
import tempfile

# boto3  allows us to write data to our s3 cloud storage
import boto3

# Acess keys to write to  our s3 cloud storage
from access_key import KEY_ID, SECRET_KEY 


# Set up access for writing files to s3  
session = boto3.session.Session()

client = session.client('s3',
                        endpoint_url="https://joeh.fra1.digitaloceanspaces.com",
                        aws_access_key_id=KEY_ID,
                        aws_secret_access_key=SECRET_KEY)




# %%
# A function that uploads a dataframe as csv to particular bucket in s3
def upload_to_s3(df:pd.DataFrame, 
                bucket_name:str, 
                file_name:str):
                
    # I couldn't find a solution for writing to a tempfile csv that worked with the boto3 upload. So
    # I take the roundabout root of creating a temp directory and adding the file to that.
    temp_folder_for_data = tempfile.TemporaryDirectory()

    # Write a csv to the temp folder
    df.to_csv(f'{temp_folder_for_data.name}/write.csv', index=False)
    
    
    # Upload to Digital Ocean – pwt bucket
    client.upload_file(f'{temp_folder_for_data.name}/write.csv',  # Path to local file
                   bucket_name, 
                   file_name, # Name for remote file
                   ExtraArgs={'ACL':'public-read'})  # specify file is public



