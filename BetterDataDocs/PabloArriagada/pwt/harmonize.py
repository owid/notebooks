# %% [markdown]
"""
# How does Our World in Data prepare data from the Penn World Tables?
"""
# %% [markdown]
"""
### About this document
This script is part of a series documenting how we prepare the data 
provided in the Penn World Tables for use in our website and charts.

<br><br>

We make these scripts available in two formats: as scripts stored 
[here in GitHub](https://docs.google.com/document/d/1VDWq2JggspDPyFjLg47DsIqNuFXAaE4SO8_CeMLMqVk/edit), 
and as notebooks published in Google Colabs.

<br><br>

If you have this open as a notebook, for instance in 
Google Colabs, you can run the code below and also edit it to explore the data.



"""
# %% [markdown]
"""
### Data preparation steps

* **Step 1) Standardize country names**   (Current document) – [View in GitHub](https://docs.google.com/document/d/1VDWq2JggspDPyFjLg47DsIqNuFXAaE4SO8_CeMLMqVk/edit)
<br>
*In this notebook we document how we load the original raw data file and standardize
the country names.*
<br><br>
* Step 2) Write metadata   ([Open in Colabs](https://docs.google.com/document/d/1VDWq2JggspDPyFjLg47DsIqNuFXAaE4SO8_CeMLMqVk/edit) – [View in Github](https://docs.google.com/document/d/1VDWq2JggspDPyFjLg47DsIqNuFXAaE4SO8_CeMLMqVk/edit))
* Step 3) Prepare and transform variables   ([Open in Colabs](https://docs.google.com/document/d/1VDWq2JggspDPyFjLg47DsIqNuFXAaE4SO8_CeMLMqVk/edit) – [View in Github](https://docs.google.com/document/d/1VDWq2JggspDPyFjLg47DsIqNuFXAaE4SO8_CeMLMqVk/edit))

"""



# %% [markdown]
"""
## Set up and permissions

In this section we load any modules or packages we need to run the code.
<br><br>
Prior to this, we run a check to see whether you are viewing this in Google Colabs and, if so, 
install any needed packages.
<br><br>
This section also includes code to allow us (the Our World in Data team) to 
upload data to our database once it's been prepared. The code below first checks whether you have 
the right permissions to upload to our database, and, if not, sections of the code below related to 
this will not run. This should not affect your ability 
to run the rest of the code or add/edit cells to explore the data.
"""

# %% [markdown]
# Check if in Colabs, and if so install needed packages. 
# %%
# Test if notebook is running on Google Colab, by trying to load a colab-specific package.

try:
  import google.colab
  IN_COLAB = True
except:
  IN_COLAB = False

# %%
# Install needed packages
#if IN_COLAB:
# None to install


# %% [markdown]
# Set up to upload data our database, if correct permissions

# %%
# Check permissions, bu
s3access = True

try:
        # Acess keys to write to  our s3 cloud storage
        from joes_key import ENDPOINT, KEY_ID, SECRET_KEY 

        # boto3  allows us to write data to our s3 cloud storage
        import boto3

        # A function we have written to help upload our data to our s3 cloud storage
        from functions import upload_to_s3


        # Set up access for writing files to s3  
        session = boto3.session.Session()

        client = session.client('s3',
                        endpoint_url="https://{}.digitaloceanspaces.com".format(ENDPOINT),
                        aws_access_key_id=KEY_ID,
                        aws_secret_access_key=SECRET_KEY)

except:
        print("This notebook is not able to write prepared data to our cloud storage. Steps in the code relating to this will not be run.")
        s3access = False

# %% [markdown]
# Load packages.

 # %%
# Pandas is a standard package used for data manipulation in python code
import pandas as pd
               



# ------- RUN –––––––––

# %%
# Load the 'Walden' data (for the time being in Joe's s3) 

url = 'https://joeh.fra1.digitaloceanspaces.com/pwt/pwt100-original.xlsx'

df_original = pd.read_excel(url, sheet_name='Data')


# %%
# Standardize country names

# %%
# Read in mapping csv – This needs to be two columns headed 'Original Name' and 'Our World In Data Name'
url = 'https://joeh.fra1.digitaloceanspaces.com/pwt/country_standardization_mapping.csv'

df_mapping = pd.read_csv(url)

# %%
# Merge in the mapping to the main df
df_harmonized = pd.merge(df_original,df_mapping,
    left_on='country',right_on='Original Name', how='left')
    
# Drop the old entity names column, and the matching column from the mapping file
df_harmonized = df_harmonized.drop(columns=['country', 'Original Name'])
    
# Rename the new entity col as specefied in the args
df_harmonized = df_harmonized.rename(columns={'Our World In Data Name': 'country'})
    
# Move entity variable to first column
# get a list of columns
cols = list(df_harmonized)
    
# move the column to head of list using index, pop and insert
cols.insert(0, cols.pop(cols.index('country')))
    
# use loc to reorder
df_harmonized = df_harmonized.loc[:, cols]


# %%
if s3access:
    upload_to_s3(df_harmonized, 'pwt', 'harmonized.csv')


# %%