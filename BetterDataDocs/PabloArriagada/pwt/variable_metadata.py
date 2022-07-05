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
variable_meta['avh'] = {}

variable_meta['avh']['name'] = "Annual working hours per worker"
variable_meta['avh']['displayName'] = "Annual working hours"
variable_meta['avh']['unitsLong'] = "Hours"
variable_meta['avh']['unitsShort'] = "h"
variable_meta['avh']['description'] = "[Long description here]"


# Number of workers
variable_meta['emp'] = {}

variable_meta['emp']['name'] = "Number of people in work"
variable_meta['emp']['displayName'] = "Number of people in work"
variable_meta['emp']['unitsLong'] = "People in work"
variable_meta['emp']['unitsShort'] = "h"
variable_meta['emp']['description'] = "[Long description here]"

#Productivity
variable_meta['productivity'] = {}

variable_meta['productivity']['name'] = "Productivity: output per hour worked"
variable_meta['productivity']['displayName'] = "Productivity: output per hour worked"
variable_meta['productivity']['unitsLong'] = "Constant 2011 international-$ per hour"
variable_meta['productivity']['unitsShort'] = "$/h"
variable_meta['productivity']['description'] = "[Long description here]"


# --- Components of GDP variables ––––


# Labour share
variable_meta['labsh'] = {}

variable_meta['labsh']['name'] = "Share of labour compensation in GDP"
variable_meta['labsh']['displayName'] = "Share of labour compensation in GDP"
variable_meta['labsh']['unitsLong'] = "%"
variable_meta['labsh']['unitsShort'] = "%"
variable_meta['labsh']['description'] = "[Long description here – Note that this is a 'NA-based' measure using current national prices.]"


# Share of household consumption
variable_meta['csh_c'] = {}

variable_meta['csh_c']['name'] = "Share of household consumption in GDP"
variable_meta['csh_c']['displayName'] = "Share of household consumption in GDP"
variable_meta['csh_c']['unitsLong'] = "%"
variable_meta['csh_c']['unitsShort'] = "%"
variable_meta['csh_c']['description'] = "[Long description here]"

# Share of gross capital formation
variable_meta['csh_i'] = {}

variable_meta['csh_i']['name'] = "Share of gross capital formation in GDP"
variable_meta['csh_i']['displayName'] = "Share of gross capital formation in GDP"
variable_meta['csh_i']['unitsLong'] = "%"
variable_meta['csh_i']['unitsShort'] = "%"
variable_meta['csh_i']['description'] = "[Long description here]"

# Share of Government consumption
variable_meta['csh_g'] = {}

variable_meta['csh_g']['name'] = "Share of labour compensation in GDP"
variable_meta['csh_g']['displayName'] = "Share of labour compensation in GDP"
variable_meta['csh_g']['unitsLong'] = "%"
variable_meta['csh_g']['unitsShort'] = "%"
variable_meta['csh_g']['description'] = "[Long description here]"

# Share of residual trade and statistical discrepancy
variable_meta['csh_r'] = {}

variable_meta['csh_r']['name'] = "Share of labour compensation in GDP"
variable_meta['csh_r']['displayName'] = "Share of labour compensation in GDP"
variable_meta['csh_r']['unitsLong'] = "%"
variable_meta['csh_r']['unitsShort'] = "%"
variable_meta['csh_r']['description'] = "[Long description here]"



# --- Trade variables––––

# Share of exports 

# Share of imports

# Trade openness (ratio of exports plus imports to GDP)




# --- Total Factor Productivity variables ––––



# --- Other variables ––––




#Convert dictionary to dataframe
df_variable_meta = pd.DataFrame.from_dict(variable_meta, orient='index')

# Write to s3
upload_to_s3(df_variable_meta, 'pwt', 'dataset_meta.csv')

# %%