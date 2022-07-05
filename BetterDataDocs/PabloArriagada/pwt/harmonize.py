# %% [markdown]
"""
# How does Our World in Data prepare data from the Penn World Tables?
"""
# %% [markdown]
"""
### About this document
This script is part of a series documenting how we prepare the data 
provided in the Penn World Tables for use in our website and charts.

<br>

We make these scripts available in two formats: as scripts stored 
[here in GitHub](https://docs.google.com/document/d/1VDWq2JggspDPyFjLg47DsIqNuFXAaE4SO8_CeMLMqVk/edit), 
and as notebooks published in Google Colabs.

<br>

If you have this open as a notebook, for instance in 
Google Colabs, you can run the code below and also edit it to explore the data.


"""
# %% [markdown]
"""
### Data preparation steps

* **Step 1. Standardize country names**   ([Open in Colabs](https://docs.google.com/document/d/1VDWq2JggspDPyFjLg47DsIqNuFXAaE4SO8_CeMLMqVk/edit) – [View in Github](https://docs.google.com/document/d/1VDWq2JggspDPyFjLg47DsIqNuFXAaE4SO8_CeMLMqVk/edit))
<br>
In this notebook we document how we load the original raw data file and standardize
the country names.
<br>
* Step 2. Write metadata   ([Open in Colabs](https://docs.google.com/document/d/1VDWq2JggspDPyFjLg47DsIqNuFXAaE4SO8_CeMLMqVk/edit) – [View in Github](https://docs.google.com/document/d/1VDWq2JggspDPyFjLg47DsIqNuFXAaE4SO8_CeMLMqVk/edit))
* Step 3. Prepare and transform variables   ([Open in Colabs](https://docs.google.com/document/d/1VDWq2JggspDPyFjLg47DsIqNuFXAaE4SO8_CeMLMqVk/edit) – [View in Github](https://docs.google.com/document/d/1VDWq2JggspDPyFjLg47DsIqNuFXAaE4SO8_CeMLMqVk/edit))
"""

# %% [markdown]
"""
## Set up and permissions

This section needs to be run in order to load packages used.
<br>
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
# # Load data and standardize country names
#
# ## Load original data file

# %%
# Load the original raw data file as a pandas dataframe. 
# (For the time being, this is in Joe's own Digital Ocean account).

url = 'https://joeh.fra1.digitaloceanspaces.com/pwt/pwt100-original.xlsx'

df_original = pd.read_excel(url, sheet_name='Data')

# %% [markdown]
# Here is the first few rows of the data:
# %%
df_original.head()

# %% [markdown]
# # Standardize country names

# %% [markdown]
# We adjust the country names to align with our standardized set of names. This makes it 
# possible for us compare data across different datasets.

# %%
# Read in mapping table which maps PWT names onto OWID names.
#Pablo: Is there a "standardization of standardizing countries"? Because using a file like this would also require to
#go to the tool in https://owid.cloud/admin/standardize in the first place

url = 'https://joeh.fra1.digitaloceanspaces.com/pwt/country_standardization_mapping.csv'

df_mapping = pd.read_csv(url)


# %% [markdown]
# Here is the first few rows of the mapping table:
# %%
df_mapping.head()

# %%
# Merge in the mapping to the main dataframe and tidy


# Merge
df_harmonized = pd.merge(df_original,df_mapping,
    left_on='country',right_on='Original Name', how='left')
    
# Drop the old entity names column, and the matching column from the mapping file
df_harmonized = df_harmonized.drop(columns=['country', 'Original Name'])
    
# Rename the new entity column
df_harmonized = df_harmonized.rename(columns={'Our World In Data Name': 'country'})

# Move the country column to front:

# get a list of columns
cols = list(df_harmonized)
    
# move the country column to the first in the list of columns
cols.insert(0, cols.pop(cols.index('country')))
    
# reorder the columns of the dataframe according to the list
df_harmonized = df_harmonized.loc[:, cols]

# %% [markdown]
# Here is the first few rows of the data after swapping the country names:
# %%
df_harmonized.head()


# %% [markdown]
# # Upload prepared data to our database
"""
This section is for internal purposes, and will not run unless you have the right permissions.
"""
# %%
if s3access:
    upload_to_s3(df_harmonized, 'pwt', 'harmonized.csv')
else:
    print("No write access")

# %%
