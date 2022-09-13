import pandas as pd
from functions.standardize_entities import *
import subprocess
import time
import sys


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True}
    not_valid = {"no": False, "n": False}
    
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")
        elif choice in valid:
            return valid[choice]
        elif choice in not_valid:
            #sys.exit("Go run that code. Bye!")
            return not_valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")


def run_stata(dofile, answer):
    
    if answer:
    
        print('Querying data from Stata\'s do file...')
        start_time = time.time()

        #Set do-file information
        #Change Stata directory if necessary
        cmd = ["C:\Program Files\Stata14\StataMP-64.exe", "/e", "do", dofile]

        ## Run do-file
        subprocess.call(cmd)

        end_time = time.time()
        elapsed_time = end_time - start_time
        print('Done. Execution time:', elapsed_time, 'seconds')


def load_and_standardize(file):
    print('Loading Stata\'s output and standardizing...')
    start_time = time.time()
    
    #Load the complete Stata output
    #keep_default_na and na_values are included because there is a country labeled NA, Namibia, which becomes null without the parameters
    df_final = pd.read_csv(file,
                           keep_default_na=False,
                           na_values=['-1.#IND', '1.#QNAN', '1.#IND', '-1.#QNAN', '#N/A N/A', '#N/A', 'N/A', 'n/a', '', '#NA', 
                                        'NULL', 'null', 'NaN', '-NaN', 'nan', '-nan', ''])

    #Standardize entities and year
    df_final = standardize_entities(df_final,
                            'data/raw/countries_country_standardized.csv',
                            'country',
                            'Our World In Data Name',
                            'country',
                            'Entity')
    df_final = df_final.rename(columns={'year': 'Year'})

    #Multiply share numbers by 100
    share_cols = df_final.filter(like="share", axis=1).columns
    df_final.loc[:, share_cols] = df_final[share_cols] * 100
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print('Done. Execution time:', elapsed_time, 'seconds')
    
    return df_final


def add_metadata_and_export(df_final, sheet):
    
    print('Changing the names of variables and exporting Grapher\'s dataset...')
    start_time = time.time()
    
    # Specify sheet id and sheet (tab) name for the metadata google sheet 

    sheet_id = '1ntYtYF0NqIW2oXuXl_ZJHvuI7n-bik94BEIOvWHrJAI'
    sheet_name = sheet

    # Read in variable metadata as dataframe
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    df_variable_metadata = pd.read_csv(url)

    # Keep only id vars (country and year) and vars with metadata

    # Select country, year and only those variables with metadata specified
    # in the metadata folder.

    id_vars = ['Entity', 'Year']

    var_list = df_variable_metadata['slug'].tolist()

    var_list = id_vars + var_list 

    df_dataset = df_final[df_final.columns.intersection(var_list)].copy()

    # Replace var names with those defined in the variable metadata ('name')

    # Make a dictionary of var code_names and names
    keys_code_names = df_variable_metadata['slug'].tolist()
    values_names = df_variable_metadata['name'].tolist()
        #pair keys and values with zip
    varnames_dict = dict(zip(keys_code_names, values_names))

    # Rename the columns using the dictionary
    df_dataset = df_dataset.rename(columns=varnames_dict)

    #Export the dataset
    df_dataset.to_csv('data/final/wid_dataset.csv', index=False)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print('Done. Execution time:', elapsed_time, 'seconds')
