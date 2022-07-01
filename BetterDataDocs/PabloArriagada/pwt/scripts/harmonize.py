
# --------- SET UP -----------
# %%
import pandas as pd

# boto3  allows us to write data to our s3 cloud storage
import boto3

# Keys for accessing s3
from joes_key import ENDPOINT, KEY_ID, SECRET_KEY 

# Set up access for writing files to s3  
session = boto3.session.Session()

client = session.client('s3',
                        endpoint_url="https://{}.digitaloceanspaces.com".format(ENDPOINT),
                        aws_access_key_id=KEY_ID,
                        aws_secret_access_key=SECRET_KEY)



# --------- FUNCTIONS ------------
# %%
# A function that swaps old for new entity names, as specified in a entity /
# name mapping csv. You specify the varname of the entity var in the original 
# dataframe (this will also be the name of the standardized entities variable)  
def standardize_entities(df:pd.DataFrame, \
                        mapping_filename:str, \
                        entity_varname:str):

    # Read in mapping csv – This needs to be two columns headed 'Original Name' and 'Our World In Data Name'
    df_mapping = pd.read_csv(mapping_filename)

    # Merge in the mapping to the main df
    df_harmonized = pd.merge(df,df_mapping,left_on=entity_varname,right_on='Original Name', how='left')
    
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

    return df_harmonized



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





# ------- RUN –––––––––

# %%
# Load the 'Walden' data (for the time being in Joe's s3) 

url = 'https://joeh.fra1.digitaloceanspaces.com/pwt/pwt100-original.xlsx'

df_original = pd.read_excel(url, sheet_name='Data')


# %%
# Standardize country names
df_harmonized = standardize_entities(df_original,
    'country_standardization_mapping.csv',
    'country'
    )



# %%
upload_to_s3(df_harmonized, 'pwt', 'harmonized.csv')


# %%