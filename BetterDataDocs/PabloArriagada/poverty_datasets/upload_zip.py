from functions.upload import *
import shutil
from pathlib import Path


# +
# # # copy subdirectory example
# parent_dir = Path().parent
# from_directory = parent_dir / "JoeHasell/PIP/data/ppp_2017/final/PIP_data_public_download/full_dataset"
# to_directory = "World Bank Poverty and Inequality Platform (PIP)"

# #copy_tree(from_directory, to_directory)
# shutil.copytree(from_directory, to_directory)
# -

upload_to_s3(path='OWID_datasets_Poverty.zip',
            bucket_name = 'OWID_datasets',
            file_name = 'OWID_datasets_Poverty.zip')


