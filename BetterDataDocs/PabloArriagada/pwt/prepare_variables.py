
# %% [markdown]
"""
# How does Our World in Data prepare data from the Penn World Tables?
"""
# %% [markdown]
"""
### About this document
This script is part of a series documenting how we prepare the data 
provided in the Penn World Tables for use in our website and charts.


We make these scripts available in two formats: as scripts stored 
[here in GitHub](https://docs.google.com/document/d/1VDWq2JggspDPyFjLg47DsIqNuFXAaE4SO8_CeMLMqVk/edit), 
and as notebooks published in Google Colabs.

If you have this open as a notebook, for instance in 
Google Colabs, you can run the code below and also edit it to explore the data.


"""
# %% [markdown]
"""
### Data preparation steps

* Step 1. Standardize country names   ([Open in Colabs](https://docs.google.com/document/d/1VDWq2JggspDPyFjLg47DsIqNuFXAaE4SO8_CeMLMqVk/edit) – [View in Github](https://docs.google.com/document/d/1VDWq2JggspDPyFjLg47DsIqNuFXAaE4SO8_CeMLMqVk/edit))
* **Step 2. Write metadata**   ([Open in Colabs](https://docs.google.com/document/d/1VDWq2JggspDPyFjLg47DsIqNuFXAaE4SO8_CeMLMqVk/edit) – [View in Github](https://docs.google.com/document/d/1VDWq2JggspDPyFjLg47DsIqNuFXAaE4SO8_CeMLMqVk/edit))
<br>
In this notebook we document how the data series we show 
in our charts are derived from the data available in the 
Penn World Tables.
<br>
* Step 3. Prepare and transform variables   ([Open in Colabs](https://docs.google.com/document/d/1VDWq2JggspDPyFjLg47DsIqNuFXAaE4SO8_CeMLMqVk/edit) – [View in Github](https://docs.google.com/document/d/1VDWq2JggspDPyFjLg47DsIqNuFXAaE4SO8_CeMLMqVk/edit))
"""

# %% [markdown]
"""
## Set up and permissions

This section needs to be run in order to load packages used.


If you are viewing this in Colabs, it will also install any packages not pre-installed 
in this environment.
<br>
In addition, we run code to allow us (the Our World in Data team) to 
upload data to our database once it's been prepared. Unless you are running this with the
corrent access keys, code blocks relating to data uploads will not run.
"""

# %%
#@title Run set up

# Test if this script is running on Google Colab, by trying to load a colab-specific package.

try:
  import google.colab
  IN_COLAB = True
except:
  IN_COLAB = False


# If this is in Colabs, install any needed packages
#if IN_COLAB:
# None to install



# If the correct access keys are in place, set up a s3 client and session 
# to be able to upload to our database.

s3access = True

try:
        # Acess keys to write to  our s3 cloud storage
        from joes_key import KEY_ID, SECRET_KEY 

        # boto3  allows us to write data to our s3 cloud storage
        import boto3

        # A function we have written to help upload our data to our s3 cloud storage
        from functions import upload_to_s3

        # Load variable metadata (– only the subset of variables with 
        # metadata will be uploaded to s3)
        from variable_metadata import variable_meta, df_variable_meta

        # Set up access for writing files to s3  
        session = boto3.session.Session()

        client = session.client('s3',
                        endpoint_url="https://joeh.fra1.digitaloceanspaces.com",
                        aws_access_key_id=KEY_ID,
                        aws_secret_access_key=SECRET_KEY)

except:
        s3access = False
        print("No write access")


# Load packages

# Pandas is a standard package used for data manipulation in python code
import pandas as pd
               


# %% [markdown]
# # Load data

# %%
# Loading the 'harmonized' data (i.e with standardized country names)
# – For the time being, this is stored in Joe's Digital Ocean account.

url = 'https://joeh.fra1.digitaloceanspaces.com/pwt/harmonized.csv'

df = pd.read_csv(url)

# %% [markdown]
# Here is the first few rows of the data:
# %%
df.head()


# %% [markdown]
# # Prepapre variables for Our World in Data

# %% [markdown]
# ## Absolute GDP variables
# The original data is given in millions of dollars.<br>
# We multiply the variable by 1,000,000 to give the figures in dollars.
# %%
df['rgdpe'] = df['rgdpe']*1000000
df['rgdpo'] = df['rgdpo']*1000000
df['cgdpe'] = df['cgdpe']*1000000
df['cgdpo'] = df['cgdpo']*1000000
df['rgdpna'] = df['rgdpna']*1000000

# %% [markdown]
# ## GDP per capita variables
# Penn World Tables do not directly provide GDP per capita. We calculate
# these by dividing GDP by the population figures they provide (both
# given in millions).
# %%
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





# %% [markdown]
# # Upload prepared data to our database

"""
This section is for internal purposes, and will not run unless you have the right permissions.
"""
# %%
if s3access:
   
    # Select country, year and only those variables with metadata specified
    # in the metadata folder.

    id_vars = ['country', 'year']

    var_list = list(variable_meta.keys())

    var_list = id_vars + var_list 

    df_final = df[df.columns.intersection(var_list)]

else:
    print("No write access")

# %%
# Replace var names with those defined as 'name' in the variable metadata
if s3access:
    # Make a dictionary mapping current column names to 'name'
    varnames_dict = df_variable_meta['name'].to_dict()

    # Rename the columns using the dictionary
    # NB:This generates a warning, but produces the right output. I didn't figure out a better way yet.
    df_final.rename(columns=varnames_dict, inplace=True)

else:
    print("No write access")
# %%
#The final data looks like this
#df_final.head()

# %%
# Write data as csv to s3
if s3access:    
    upload_to_s3(df_final, 'pwt', 'final.csv')

else:
    print("No write access")

# %%
