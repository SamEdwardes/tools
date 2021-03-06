'''
TITLE: Combine CSV & XLSX
DESCRIPTION: combine all csv and xlsx files in same directory as script into one or multiple csv files
---
AUTHOR: Sam Edwardes
DATE: 2019-05-07
NOTES:
    The script will find all csv files and load into a dataframe.
    The script will also find each excel file, and load each sheet into a dataframe.
    The script will then combine dataframes with the same headers into one dataframe.
    THe script will then output each combined dataframe into a csv file.
'''

import pandas as pd
import numpy as np
import os
import itertools

# user input defualt
export_results = False

# create an empty list for the dataframes
df_list = []
df_file_list = []
df_tab_list = []

# loop through each file in the same directory as script and import dataframe
for file in os.listdir():
    if ".csv" in file:
        temp_df = pd.read_csv(filepath_or_buffer=file, sep=",")
        temp_df["se.source.file"] = file
        temp_df["se.source.tab"] = np.NaN
        df_list.append(temp_df)
        df_file_list.append(file)
        df_tab_list.append(np.NaN)
        del temp_df
    elif ".xlsx" in file:
        temp_xls = pd.ExcelFile(file)
        for sheet in temp_xls.sheet_names:
            temp_df = pd.read_excel(temp_xls, sheet)
            temp_df["se.source.file"] = file
            temp_df["se.source.tab"] = sheet
            df_list.append(temp_df)
            df_file_list.append(file)
            df_tab_list.append(sheet)
            del temp_df
        del temp_xls
    else:
        continue

# clean the headers of each dataframe
for df in df_list:
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

# get a list that contains a list of column names for each df
df_columns_list = []
for df in df_list:
    df_columns_list.append(list(df.columns))

# remove duplicate items from list
df_columns_list.sort()
df_columns_list = (list(df_columns_list for df_columns_list,_ in itertools.groupby(df_columns_list)))

# iterate through unique headers, combining dataframes when they match the header
df_final_list = []
for cols in df_columns_list:
    temp_df_list = []
    for df in df_list:
        if list(df.columns) == cols:
            temp_df_list.append(df)
        else:
            continue
    df_final_list.append(pd.concat(temp_df_list))
    del temp_df_list

# print results
print("\n###############\nRESULTS\n###############")
print("\n" + str(len(df_list))+" dataframes were identified: ")
df_dict = {"file.name": df_file_list, "tab.name": df_tab_list}
print(pd.DataFrame(data=df_dict))
print("\nThe dataframes were combined into " + str(len(df_final_list)) + " unique dataframes:\n")
for df in df_final_list:
    print(df.head())
    print("\n")

# ask for user input
user_input_export_results = input('Do you want to export the results? (y/n): ')
if user_input_export_results.lower().strip()[0] == 'y':
    export_results = True
else:
    export_results = False

# print original dataframes
print("\n\n###############\nORIGINAL DATA FRAMES\n###############")
for df in df_list:
    print("\n")
    print(df.head())

# export dataframes to csv
iteration = 1
if export_results:
    for df in df_final_list:
        file_name = "combined_" + str(iteration) + ".csv"
        print()
        iteration = iteration + 1
        df.to_csv(file_name, index=False)
    print("\n\n###############\nEXPORT STATUS\n###############")
    print("\nProgram complete: reuslts exported")
else:
    print("\n\n###############\nEXPORT STATUS\n###############")
    print("\nProgram complete: results not exported")

#keep the window open until the user presses enter
input('\nPress any key to close the program.')
