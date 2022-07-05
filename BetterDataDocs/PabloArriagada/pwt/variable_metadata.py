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


# Create a dictionary for the variable metadata
# This will be a dictionary of dictionaries – one for each variable 
variable_meta = {}


# ---- GDP per capita variables ------

# GDP per capita (expenditure, multiple price benchmarks)
variable_meta['rgdpe_pc'] = {}

variable_meta['rgdpe_pc']['name'] = "GDP per capita (expenditure, multiple price benchmarks)"
variable_meta['rgdpe_pc']['displayName'] = "GDP per capita"
variable_meta['rgdpe_pc']['unitsLong'] = "International-$ at 2017 prices"
variable_meta['rgdpe_pc']['unitsShort'] = "$"
variable_meta['rgdpe_pc']['description'] = "[Long description here]"


# GDP per capita (output, multiple price benchmarks)
variable_meta['rgdpo_pc'] = {}

variable_meta['rgdpo_pc']['name'] = "GDP per capita (output, multiple price benchmarks)"
variable_meta['rgdpo_pc']['displayName'] = "GDP per capita"
variable_meta['rgdpo_pc']['unitsLong'] = "International-$ at 2017 prices"
variable_meta['rgdpo_pc']['unitsShort'] = "$"
variable_meta['rgdpo_pc']['description'] = "[Long description here]"



# GDP per capita (expenditure, single price benchmark)
variable_meta['cgdpe_pc'] = {}

variable_meta['cgdpe_pc']['name'] = "GDP per capita (expenditure, single price benchmark)"
variable_meta['cgdpe_pc']['displayName'] = "GDP per capita"
variable_meta['cgdpe_pc']['unitsLong'] = "International-$ at 2017 prices"
variable_meta['cgdpe_pc']['unitsShort'] = "$"
variable_meta['cgdpe_pc']['description'] = "[Long description here]"


# GDP per capita (expenditure, single price benchmark)
variable_meta['cgdpo_pc'] = {}

variable_meta['cgdpo_pc']['name'] = "GDP per capita (output, single price benchmark)"
variable_meta['cgdpo_pc']['displayName'] = "GDP per capita"
variable_meta['cgdpo_pc']['unitsLong'] = "International-$ at 2017 prices"
variable_meta['cgdpo_pc']['unitsShort'] = "$"
variable_meta['cgdpo_pc']['description'] = "[Long description here]"


# GDP per capita (using national accounts growth rates)
variable_meta['rgdpna_pc'] = {}

variable_meta['rgdpna_pc']['name'] = "GDP per capita (using national accounts growth rates)"
variable_meta['rgdpna_pc']['displayName'] = "GDP per capita"
variable_meta['rgdpna_pc']['unitsLong'] = "International-$ at 2017 prices"
variable_meta['rgdpna_pc']['unitsShort'] = "$"
variable_meta['rgdpna_pc']['description'] = "[Long description here]"



# ---- Absolute GDP variables ------

# GDP (expenditure, multiple price benchmarks)
variable_meta['rgdpe'] = {}

variable_meta['rgdpe']['name'] = "GDP (expenditure, multiple price benchmarks)"
variable_meta['rgdpe']['displayName'] = "GDP"
variable_meta['rgdpe']['unitsLong'] = "International-$ at 2017 prices"
variable_meta['rgdpe']['unitsShort'] = "$"
variable_meta['rgdpe']['description'] = "[Long description here]"


# GDP (output, multiple price benchmarks)
variable_meta['rgdpo'] = {}

variable_meta['rgdpo']['name'] = "GDP (output, multiple price benchmarks)"
variable_meta['rgdpo']['displayName'] = "GDP"
variable_meta['rgdpo']['unitsLong'] = "International-$ at 2017 prices"
variable_meta['rgdpo']['unitsShort'] = "$"
variable_meta['rgdpo']['description'] = "[Long description here]"



# GDP (expenditure, single price benchmark)
variable_meta['cgdpe'] = {}

variable_meta['cgdpe']['name'] = "GDP (expenditure, single price benchmark)"
variable_meta['cgdpe']['displayName'] = "GDP"
variable_meta['cgdpe']['unitsLong'] = "International-$ at 2017 prices"
variable_meta['cgdpe']['unitsShort'] = "$"
variable_meta['cgdpe']['description'] = "[Long description here]"


# GDP (expenditure, single price benchmark)
variable_meta['cgdpo'] = {}

variable_meta['cgdpo']['name'] = "GDP (output, single price benchmark)"
variable_meta['cgdpo']['displayName'] = "GDP"
variable_meta['cgdpo']['unitsLong'] = "International-$ at 2017 prices"
variable_meta['cgdpo']['unitsShort'] = "$"
variable_meta['cgdpo']['description'] = "[Long description here]"


# GDP (using national accounts growth rates)
variable_meta['rgdpna'] = {}

variable_meta['rgdpna']['name'] = "GDP (using national accounts growth rates)"
variable_meta['rgdpna']['displayName'] = "GDP"
variable_meta['rgdpna']['unitsLong'] = "International-$ at 2017 prices"
variable_meta['rgdpna']['unitsShort'] = "$"
variable_meta['rgdpna']['description'] = "[Long description here]"




# --- Employment and labour productivity variables ––––

# Annual working hours per worker



# --- Components of GDP variables ––––


# Labour share

# JH comment: let's present the following as a stacked area chart

# Share of household consumption

# Share of gross capital formation

# Share of Government consumption

# Share of residual trade and statistical discrepancy




# --- Trade variables––––

# Share of exports 

# Share of imports

# Trade openness (ratio of exports plus imports to GDP)




# --- Total Factor Productivity variables ––––



# --- Other variables ––––




#Convert dictionary to dataframe
df = pd.DataFrame.from_dict(variable_meta, orient='index')

# Write to s3
upload_to_s3(df, 'pwt', 'dataset_meta.csv')

# %%