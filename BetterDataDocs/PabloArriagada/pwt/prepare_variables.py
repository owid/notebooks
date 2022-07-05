# %%

# %%
# Pandas is a standard package used for data manipulation in python code
import pandas as pd

# boto3  allows us to write data to our s3 cloud storage
import boto3

# Keys for accessing s3
from joes_key import KEY_ID, SECRET_KEY 

# A function we have written to help upload our data to our s3 cloud storage
from functions import upload_to_s3


# Note, we should grab this from the etl instead when it's ready
from variable_metadata import variable_meta


# %%
# Set up access for writing files to s3  
session = boto3.session.Session()

client = session.client('s3',
                        endpoint_url="https://joeh.fra1.digitaloceanspaces.com",
                        aws_access_key_id=KEY_ID,
                        aws_secret_access_key=SECRET_KEY)




# ------- LOAD –––––––––

# %%
# Load the 'harmonized' data (i.e with standardized country names)
# – For the time being, this is stored in Joe's Digital Ocean account.

url = 'https://joeh.fra1.digitaloceanspaces.com/pwt/harmonized.csv'

df = pd.read_csv(url)




# ------- RUN –––––––––

# –––– Construct absolute GDP variables –––––
#The original data is given in millions of dollars.
# We multiply the variable by 1,000,000 to give the figures in dollars.
df['rgdpe'] = df['rgdpe']*1000000
df['rgdpo'] = df['rgdpo']*1000000
df['cgdpe'] = df['cgdpe']*1000000
df['cgdpo'] = df['cgdpo']*1000000
df['rgdpna'] = df['rgdpna']*1000000


# –––– Construct GDP per capita variables –––––
# GDP per capita is GDP divided by popultion (both are given in millions)
df['rgdpe_pc'] = df['rgdpe']/df['pop']
df['rgdpo_pc'] = df['rgdpo']/df['pop']
df['cgdpe_pc'] = df['cgdpe']/df['pop']
df['cgdpo_pc'] = df['cgdpo']/df['pop']
df['rgdpna_pc'] = df['rgdpna']/df['pop']




# %%
# --- Employment and labour productivity variables ––––


# %%
# --- Components of GDP variables ––––





# %%
# --- Trade variables––––



# %%
# --- Total Factor Productivity variables ––––


# %%
# --- Other variables ––––





# %%
# –––––––– UPLOAD –––––––––––––

# %%
# Select country, year and only those variables with metadata specified
# in the metadata folder.

id_vars = ['country', 'year']

var_list = list(variable_meta.keys())

var_list = id_vars + var_list 

df_final = df[df.columns.intersection(var_list)]


# TODO: replace names as defined in the variable metadata


# %%
df_final.head()


# %%
upload_to_s3(df_final, 'pwt', 'final.csv')


# %%
