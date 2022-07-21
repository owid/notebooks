Because the pipeline uses a mix of .pyy and .r scripts and 
because some of the steps take a long time to execute,
I cannot make a 'main.py' script to implement the pipeline.

Instead here I give instructions as to the order in which to
execute the scripts in the root directory.

1) percentiles_request.py
2) headcounts_request (this strand of the pipeline hasn't been made yet – to come)
3) construct_vars_with_gpinter.r
4) prep_main_data_file.py
5) prep_percentiles_data_file.py (not yet done)



To do:

- Extend prep_main_data_file.py to also produce non-filled main data.

- Prepare final percentile csv (filled and non filled)