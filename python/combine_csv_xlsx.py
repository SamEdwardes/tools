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

# TODO check why test3.xlsx sheet 2 is showing up in two final dataframes (its b/c how we are filtering...)
# user input
export_results = True

# create an empty list for the dataframes
df_list = []

# loop through each file in the same directory as script and import dataframe
for file in os.listdir():
    if ".csv" in file:
        temp_df = pd.read_csv(filepath_or_buffer=file, sep=",")
        temp_df["se.source.file"] = file
        temp_df["se.source.tab"] = np.NaN
        df_list.append(temp_df)
        del temp_df
    elif ".xlsx" in file:
        temp_xls = pd.ExcelFile(file)
        for sheet in temp_xls.sheet_names:
            temp_df = pd.read_excel(temp_xls, sheet)
            temp_df["se.source.file"] = file
            temp_df["se.source.tab"] = sheet
            df_list.append(temp_df)
            del temp_df
        del temp_xls
    else:
        continue

# clean the headers of each dataframe
for df in df_list:
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

# stack all df on top of each other
df_all = (pd.concat(df_list))

# get a list that contains a list of column names for each df
df_columns_list = []
for df in df_list:
    df_columns_list.append(list(df.columns))

# remove duplicate items from list
df_columns_list.sort()
df_columns_list = (list(df_columns_list for df_columns_list,_ in itertools.groupby(df_columns_list)))

# filter all df for each unique set of column names
df_final_list = []
for cols in df_columns_list:
    df_final_list.append(df_all[cols].dropna(thresh=len(cols)-1).reset_index(drop=True))

# print final results
print("\n###############\nFINAL DATA FRAMES\n###############")
for df in df_final_list:
    print("\n")
    print(df)
print("\n###############\nALL DATA FRAMES\n###############")
print(df_all)
print("\n###############\nORIGINAL DATA FRAMES\n###############")
for df in df_list:
    print("\n")
    print(df)

# export dataframes to csv
iteration = 1
if export_results:
    for df in df_final_list:
        file_name = "combined_" + str(iteration) + ".csv"
        print()
        iteration = iteration + 1
        df.to_csv(file_name, index=False)
    print("\nProgram complete: reuslts exported")
else:
    print("\nProgram complete: results not exported")


    print()




