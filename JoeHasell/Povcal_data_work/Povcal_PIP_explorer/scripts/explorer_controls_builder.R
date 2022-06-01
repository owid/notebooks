





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
  
  # Backslashes for regex special character escapes
  search_for_strs<- paste0("\\[", sheet_name, "\\$", names(replacements_row), "\\]")
  
  replace_with_strs<- as.vector(t(replacements_row))
  
  replace_vector_over_col <- function(x) (str_replace_all(x, setNames(replace_with_strs,search_for_strs)))
  
  df_block_replaced<- df_block %>% 
    mutate(across(everything(), replace_vector_over_col))
  
  return(df_block_replaced)
}

  ## Test this function
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

special_sheets[["explorer_sheetname"]]<- "explorer_controls"
special_sheets[["control_stub_sheetname"]]<- "control_stubs"
special_sheets[["global_controls_sheetname"]]<- "global_controls"
special_sheets[["graphers_columns_sheetname"]]<- "graphers_columns"
special_sheets[["table_columns_sheetname"]]<- "table_columns"
special_sheets[["tables_sheetname"]]<- "tables"

aux_sheet_pattern<- "AUX_" #The string in the workbook sheetnames that calls a 
                            #sheet out as being an 'Aux sheet' -  i.e. a sheet
                            #where the various values of the placeholders are
                            #given


# Specify the set of column headers

# This is the function
build_OWID_controls<- function(gsheets_id){
  
  # Print progress status
  print("Multiplying up the controls")
  
  # Authorise access to google sheets
  gs4_auth()
  
  
  # Pull in the control stubs
  
  control_stubs<- read_sheet(gsheets_id, sheet = special_sheets[["control_stub_sheetname"]])
  
  
  
  # Make a vector of the names of the other sheets (these are the Aux sheets, which will 
    # be used to multiply-up the control stubs, replacing the various combination of values 
    # contained in the Aux sheets)
  aux_sheets<- sheet_names(gsheets_id)
  aux_sheets<-aux_sheets[grepl(aux_sheet_pattern, aux_sheets)]
  
  
  # The first step in multiplying up the control stubs is to convert the dataframe of 
    # control stubs to a list of rows.
  running_list<- split(control_stubs, seq(nrow(control_stubs)))
  
  
  
  # Now lets run applymyReplaceFunRowwise iteratively. In the first iteration, it runs 
    # across the list containing the control stubs. The output of this first iteration is 
    # a list of (multirow) dataframes which is the control stubs multiplied up by only one 
    # set of Aux values. Further iterations then run across this list of dataframes, which 
    # itself outputs a list of dataframes. And so on, for each Aux sheet.
  
  for(aux_sheet in aux_sheets){
    
    df_replacements_rows<- read_sheet(gsheets_id, sheet = aux_sheet)
    
    running_list<- lapply(running_list, applymyReplaceFunRowwise, sheet_name = aux_sheet, df_replacements_rows =  df_replacements_rows)
    
  }
  
  
  # collapse the output into a single df
  controls_multiplied_up<- bind_rows(running_list)
  
  
  # drop any duplicate rows. This is a key step in the function: Duplicates will be created
    # where a control stub row doesn't make use of all Aux sheets.
  controls_multiplied_up<-  controls_multiplied_up %>% distinct()
  
  
  ## Write to final controls google sheet
  
  # Clear current contents
  range_clear(
    ss = gsheets_id, 
    sheet = special_sheets[["explorer_sheetname"]], 
    range = NULL, 
    reformat = TRUE)
  

  
  # initial global controls
  
    # Print progress status
    print("Overwriting explorer sheet - Global controls")
  
    # grab global controls as specified in workbook 
    global_controls<- read_sheet(gsheets_id, sheet = special_sheets[["global_controls_sheetname"]])
  
  range_write(
    ss = gsheets_id,
    data = global_controls,
    sheet = special_sheets[["explorer_sheetname"]],
    range = cell_limits(c(1, 1), c(NA, NA)),
    col_names = FALSE,
    reformat = FALSE
  )
    

    # Write grapher rows

      # Print progress status
      print("Overwriting explorer sheet - Global 'graphers' controls")

      # Write the word 'graphers' in the right place
      print_row<- nrow(global_controls) + 2 #The row to print "graphers" on = the number of controls + a gap
      print_col<- 1
        
        range_write(
          ss = gsheets_id,
          data = as.data.frame("graphers"),  #range_write requires dataframe input (I transpose here to flip the vector to rows)
          sheet = special_sheets[["explorer_sheetname"]],
          range = cell_limits(c(print_row, 1), c(NA, NA)), #NB print in first column
          col_names = FALSE,
          reformat = FALSE
        )


      # Print the grapher columns in the next row
        
        # Grab the grapher columns as specified in workbook 
        graphers_columns<- read_sheet(gsheets_id, sheet = special_sheets[["graphers_columns_sheetname"]])
       
        # Select the grapher columns from the controls and rename to final names
        df_grapher_controls<- controls_multiplied_up %>%
          select(all_of(graphers_columns$names_in_this_workbook)) #This also orders the columns
        
        # rename columns to final explorer names
        names(df_grapher_controls)<- graphers_columns$final_explorer_names #Note names vector is in same order

        # Print the controls one row down, and from second column
        print_row<- print_row + 1
        print_col<- 2
        range_write(
          ss = gsheets_id,
          data = df_grapher_controls,
          sheet = special_sheets[["explorer_sheetname"]],
          range = cell_limits(c(print_row, print_col), c(NA, NA)), 
          col_names = TRUE,
          reformat = FALSE
        )
    
        
      # Write table controls 
        
        # Print progress status
        print("Overwriting explorer sheet - table controls")
        
        # Grab tables sheet from workbook
        tables<- read_sheet(gsheets_id, sheet = special_sheets[["tables_sheetname"]])
        
        # Grab table columns sheet from workbook
        table_columns<- read_sheet(gsheets_id, sheet = special_sheets[["table_columns_sheetname"]])
        
        
        
        # specify starting print row (the length of the two blocks printed so far, plus header and gap)
        print_row<- nrow(global_controls) + nrow(df_grapher_controls) + 5 
 
        # for each table
        for (i in 1:nrow(tables)){
          
          this_tableSlug<- as.character(tables[i,"tableSlug"])
          
          # Print progress status
          print(paste0("Overwriting explorer sheet - table controls: ", this_tableSlug))
          
          # Filter the controls for the rows matching this table slug
          df_table_controls_this_table<- controls_multiplied_up %>%
            filter(tableSlug == this_tableSlug)
          
          # Select the table columns from the controls and rename to final names
          df_table_controls_this_table<- df_table_controls_this_table %>%
            select(all_of(table_columns$names_in_this_workbook)) #This also orders the columns
          
          # rename columns to final explorer names
          names(df_table_controls_this_table)<- table_columns$final_explorer_names #Note names vector is in same order
          
          # table link and header

            # build a dataframe that contains the right text
            table_header<- tables[i,]
             
            table_header<- rbind(table_header, table_header) %>%
              mutate(first_col = c("table", "columns")) %>%
              select(first_col, links, tableSlug)
            
            table_header[2,2]<- this_tableSlug
            table_header[2,3]<- ""
            
              
            # print the table link and header
            print_col<- 1
            
            range_write(
              ss = gsheets_id,
              data = table_header,
              sheet = special_sheets[["explorer_sheetname"]],
              range = cell_limits(c(print_row, print_col), c(NA, NA)),
              col_names = FALSE,
              reformat = FALSE
            )
          
          
          # print table controls
            print_row<- print_row + 2 # Increment print row
            print_col<- 2
          
            range_write(
              ss = gsheets_id,
              data = df_table_controls_this_table,
              sheet = special_sheets[["explorer_sheetname"]],
              range = cell_limits(c(print_row, print_col), c(NA, NA)),
              col_names = TRUE,
              reformat = FALSE
            )
          
        # Increment print row
        print_row<- print_row + nrow(df_table_controls_this_table) + 2
          
        }
        
      
  }
  
  



# # Test main function
# 
# # Load packages
# library(tidyverse)
# library(googlesheets4)
# 
# gsheets_id<- "1-65yg7odNc6wym6VxXc5Sj0Dt0A9QPaL8mfzUhc1yHE"
# 
# build_OWID_controls(gsheets_id)


