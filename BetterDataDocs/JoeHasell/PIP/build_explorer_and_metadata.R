




# The final function -  build_OWID_controls - is built by nesting two other functions 
  # iteratively (like Russian dolls). Collectively, the work to multiply up the controls
  # specified in the control_stubs sheet across the values givin the Aux sheets


# 1. This function takes a dataframe (`df_block`) and within it replaces a set of key words 
  # for a set of values. The key words and replacement values are specified by `sheet_name` 
  # (string) and `replacements_row` (a 1 row dataframe). The key words are strings, 
  # constructed as "[`sheet_name`$`column_header`]", where `column_header` is each of the 
  # variable names in `replacements_row`. The replacement values are the corresponding values 
  # of `replacements_row`.
myReplaceFun<- function(df_block, sheet_name, replacements_row){
  
  # Replace any NAs with empty strings
  replacements_row[is.na(replacements_row)]<- ""
  
  # Backslashes for regex special character escapes
  search_for_strs<- paste0("\\[", sheet_name, "\\$", names(replacements_row), "\\]")
  
  replace_with_strs<- as.vector(t(replacements_row))
  
  replace_vector_over_col <- function(x) (str_replace_all(x, setNames(replace_with_strs,search_for_strs)))
  
  df_block_replaced<- df_block %>% 
    mutate(across(everything(), replace_vector_over_col))
  
  return(df_block_replaced)
}

  # # Test this function
  # df_block<- data.frame(col1 = c("headcount_ratio_[abs_povline$slug_suffix]","headcount_[abs_povline$slug_suffix]"),
  #                     col2 = c("$[abs_povline$text] a day","$[abs_povline$text] a day"))
  # 
  # sheet_name<- "abs_povline"
  # 
  # replacements_row<- data.frame("text" = "1",
  #                             "slug_suffix" = "1_00",
  #                             "math" = "1")
  # 
  # 
  # 
  # print(myReplaceFun(df_block = df_block,
  #                  sheet_name = sheet_name,
  #                  replacements_row = replacements_row))



# 2. This function splits a dataframe (`df_replacements_rows`, where each row is a 
  # replacements_row in myReplaceFun) into a list of dataframes by row, applies the 
  # myReplaceFun on each of those rows, and then aggregates the resulting list back 
  # into a single dataframe. The arguments `df_block` and `sheet_name` are passed to 
  # myReplaceFun for all rows.
applymyReplaceFunRowwise<- function(df_block, sheet_name, df_replacements_rows){
  
  list_replacements_rows<- split(df_replacements_rows, seq(nrow(df_replacements_rows)))
  
  list_replaced_df_blocks<- lapply(list_replacements_rows, myReplaceFun, df_block = df_block, sheet_name = sheet_name)
  
  df_replaced_df_blocks<- bind_rows(list_replaced_df_blocks)
  
  return(df_replaced_df_blocks)
  
}  


  ## Test this function
  # df_block<- data.frame(col1 = c("headcount_ratio_[abs_povline$slug_suffix]","headcount_[abs_povline$slug_suffix]"), 
  #                     col2 = c("$[abs_povline$text] a day","$[abs_povline$text] a day"))
  # 
  # sheet_name<- "abs_povline"
  # 
  # df_replacements_rows<- data.frame("text" = c("1", "2"),
  #                                 "slug_suffix" = c("1_00", "2_00"),
  #                                 "math" = c("1", "2"))
  # 
  # 
  # 
  # print(applymyReplaceFunRowwise(df_block = df_block,
  #                              sheet_name = sheet_name,
  #                              df_replacements_rows = df_replacements_rows))








##### Main function

# Specify special sheet names (the sheets that do not contain Aux control options)
special_sheets<- list()

special_sheets[["explorer_sheetname"]]<- "explorer_sheet_main"
special_sheets[["graphers_stubs_sheetname"]]<- "grapher_stubs_main"
special_sheets[["table_stubs_sheetname"]]<- "table_stubs_main"
special_sheets[["global_controls_sheetname"]]<- "global_controls_main"

special_sheets[["codebook_stubs_sheetname"]]<- "codebook_metadata_stubs"


special_sheets[["codebook_print_sheetname"]]<- "codebook_metadata_auto"



aux_sheet_pattern<- "AUX_" #The string in the workbook sheetnames that calls a 
                            #sheet out as being an 'Aux sheet' -  i.e. a sheet
                            #where the various values of the placeholders are
                            #given



# This is the function
build_OWID_controls<- function(gsheets_id){
  
  # Authorise access to google sheets
  gs4_auth()
  
  # Clear current contents
  range_clear(
    ss = gsheets_id,
    sheet = special_sheets[["explorer_sheetname"]],
    range = NULL,
    reformat = TRUE)
  
  
  # Print progress status
  print("Multiplying up the controls")
  
  
  # Make a vector of the names of the other sheets (these are the Aux sheets, which will 
    # be used to multiply-up the control stubs, replacing the various combination of values 
    # contained in the Aux sheets)
  aux_sheets<- sheet_names(gsheets_id)
  aux_sheets<-aux_sheets[grepl(aux_sheet_pattern, aux_sheets)]
  
  stubs_multiplied<- list()
  
  # grab global controls as specified in workbook
  global_controls<- read_sheet(gsheets_id, sheet = special_sheets[["global_controls_sheetname"]])
  
  last_row<- 0
  
  range_write(
    ss = gsheets_id,
    data = global_controls,
    sheet = special_sheets[["explorer_sheetname"]],
    range = cell_limits(c(last_row + 1, 1), c(NA, NA)),
    col_names = FALSE,
    reformat = FALSE
  )
  
  last_row<- last_row + nrow(global_controls) # keep track of the last row printed in the google sheet
  
  
  # For both grapher and table stubs...
  for(stubs_sheet in c("graphers", "table", "codebook")){
    
    # Pull in the stubs from gsheets
    stubs<- read_sheet(gsheets_id, sheet = special_sheets[[paste0(stubs_sheet,"_stubs_sheetname")]])
    
    # The first step in multiplying up the stubs is to convert the dataframe of 
    # control stubs to a list of rows.
    running_list<- split(stubs, seq(nrow(stubs)))
    
    
    # Now lets run applymyReplaceFunRowwise iteratively. In the first iteration, it runs 
    # across the list containing the control stubs. The output of this first iteration is 
    # a list of (multirow) dataframes which is the control stubs multiplied up by only one 
    # set of Aux values. Further iterations then run across this list of dataframes, which 
    # itself outputs a list of dataframes. And so on, for each Aux sheet.
    
    for(aux_sheet in aux_sheets){
      
      df_replacements_rows<- read_sheet(gsheets_id, sheet = aux_sheet, trim_ws = FALSE)
      
      running_list<- lapply(running_list, applymyReplaceFunRowwise, sheet_name = aux_sheet, df_replacements_rows =  df_replacements_rows)
      
    }
    
    
    # collapse the output into a single df
    controls_multiplied_up<- bind_rows(running_list)
    
    # drop any duplicate rows. This is a key step in the function: Duplicates will be created
    # where a control stub row doesn't make use of all Aux sheets.
    controls_multiplied_up<-  controls_multiplied_up %>% distinct()
    
    #Add to list
    stubs_multiplied[[stubs_sheet]]<- controls_multiplied_up
    
  }
  
    
    # Print progress status
    print(paste0("Overwriting explorer sheet - graphers"))

    # Write the word 'graphers' or  in the right place
    print_col<- 1
    
    range_write(
            ss = gsheets_id,
            data = as.data.frame('graphers'),  #range_write requires dataframe input
            sheet = special_sheets[["explorer_sheetname"]],
            range = cell_limits(c(last_row + 2, print_col), c(NA, NA)), #NB print in first column
            col_names = FALSE,
            reformat = FALSE
          )

    
    last_row<- last_row + 2 # keep track of the last row printed in the google sheet
    
    

    # Print the controls one row down, and from second column
    print_col<- 2
      
    range_write(
            ss = gsheets_id,
            data = stubs_multiplied[['graphers']],
            sheet = special_sheets[["explorer_sheetname"]],
            range = cell_limits(c(last_row +1, print_col), c(NA, NA)),
            col_names = TRUE,
            reformat = FALSE
          )
    
    last_row<- last_row + nrow(stubs_multiplied[['graphers']]) + 1 # keep track of the last row printed in the google sheet
    

    
    # Print progress status
    print("Overwriting explorer sheet - table controls")
    
    
    # Grab tables sheet from workbook
    table_list<- unique(stubs_multiplied[['table']]$tableSlug)
    
    
  
    # make a list of the table controls dataframes that the loop below will produce
    # table_controls<- list()
    
    # for each table
    for (tab in table_list){
      
      
      # Print progress status
      print(paste0("Overwriting explorer sheet - table controls: ", tab))
      
      # Filter the controls for the rows matching this table slug and drop the tableSlug column from the table controls 
      df_table_controls_this_table<- stubs_multiplied[['table']] %>%
        filter(tableSlug == tab)
      
      #grab table link
      table_link<- df_table_controls_this_table %>%
        select(table_link) %>%
        unique() %>%
        as.character()
      
      #unselect the columns that aren't printed
      df_table_controls_this_table<- df_table_controls_this_table %>%
        select(-c(tableSlug, table_link))
      
      
      
      # table link and header for table cols

        # build a dataframe that contains the right text
        table_header<- data.frame(col1 = c("table", "columns"),
                                  col2 = c(table_link, tab),
                                  col3 = c(tab, ""))


         # print the table link and header
         print_col<- 1

         range_write(
                    ss = gsheets_id,
                    data = table_header,
                    sheet = special_sheets[["explorer_sheetname"]],
                    range = cell_limits(c(last_row + 2, print_col), c(NA, NA)),
                    col_names = FALSE,
                    reformat = FALSE
                  )

         last_row<- last_row + nrow(table_header) + 2 # keep track of the last row printed in the google sheet
         
         
      # print table controls
      print_col<- 2

      range_write(
              ss = gsheets_id,
              data = df_table_controls_this_table,
              sheet = special_sheets[["explorer_sheetname"]],
              range = cell_limits(c(last_row+1, print_col), c(NA, NA)),
              col_names = TRUE,
              reformat = FALSE
                     )
      
      
         last_row<- last_row + nrow(df_table_controls_this_table) + 1 # keep track of the last row printed in the google sheet
         
      
      #Add controls to list   
      # table_controls[[this_tableSlug]]<- df_table_controls_this_table
      
    }
    

  
  # Write codebook(s) to directory
  # Multiple codebooks -  one for each tableSlug
    
    # Make list of table names used in the prepared codebook controls
    table_list<- unique(stubs_multiplied[['codebook']]$tableSlug)
    
    for (tab in table_list){
      
      # Filter for the rows matching this table slug 
      df_codebook_controls_this_table<- stubs_multiplied[['codebook']] %>%
        filter(tableSlug == tab) 
        
      # write admin metadata as csv
      fp<- paste0("data/ppp_2017/final/OWID_internal_upload/explorer_database/", tab, "/variable_metadata.csv")
      
      write.csv(df_codebook_controls_this_table, fp)
      
      # keep only codebook vars and write to csv in public download folder
      df_codebook_controls_this_table<- df_codebook_controls_this_table %>%
        select(slug, description) %>%
        rename(varname = slug)
      
      # write codebook metadata to directory
      fp<- paste0("data/ppp_2017/final/PIP_data_public_download/full_dataset/", tab, "/codebook.csv")
      
      write.csv(df_codebook_controls_this_table, fp)
      
    }
    
    
}

# Run main function

# Load packages
library(tidyverse)
library(googlesheets4)


gsheets_id<- "1bVOaDcnDoF0M_zK3uof0dIH-Z4OUDxqM7QO3B9jzRbk"

return_list<- build_OWID_controls(gsheets_id)


