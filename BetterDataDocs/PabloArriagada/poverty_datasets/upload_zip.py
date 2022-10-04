from functions.upload import *

upload_to_s3(path='OWID_datasets_Poverty.zip',
            bucket_name = 'OWID_datasets',
            file_name = 'OWID_datasets_Poverty.zip')


