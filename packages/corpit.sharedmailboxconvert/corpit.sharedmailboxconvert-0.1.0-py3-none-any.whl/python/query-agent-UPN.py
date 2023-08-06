#Dependencies
import re
import os
import pandas as pd
import csv
import tkinter as tk
from tkinter import filedialog

#Promp the user for a .csv file from Jira Filter with all fields
root = tk.Tk()
root.withdraw()

PATH= filedialog.askopenfilename()


#Declare a Regex statement
#Declare Regex compiler
emailRegex = re.compile(r'''(
    [a-zA-Z0-9._%+-]+
    @
    [a-zA-Z0-9.-]+
    (\.[a-zA-Z]{2,4})
    )''', re.VERBOSE)


#Pull in csv
init_df = pd.read_csv(PATH)

#pull out Series Description
description_series = init_df.Description


#We need to filter out rows that have a "reactivate" and a "deactivation"
reactivate_description_series = description_series[description_series.str.contains('Reacti')]
deactivate_description_series = description_series[description_series.str.contains('Deactiv')]


#Regex Email pull into an Array
def find_email_regex(in_series):
    matches = []
    for items in in_series:
        for groups in emailRegex.findall(items):
            matches.append(groups[0])
    return matches

#TODO: remove duplicates
#TODO: move check duplicates earlier to catch duplicates and create a report.

#Create .csv files for each type, reactivate and activate
def create_output_csv():
    to_csv_react = pd.DataFrame(find_email_regex(reactivate_description_series), columns = ["UserPrincipalName"])
    to_csv_deact = pd.DataFrame(find_email_regex(deactivate_description_series), columns = ["UserPrincipalName"])
    to_csv_react.to_csv("AWSReactivationList.csv", index =False, header="UserPrincipalName")
    to_csv_deact.to_csv("AWSDeactivationList.csv", index =False, header="UserPrincipalName")
    
create_output_csv()

#Check for duplicates and print a .csv
duplicate_check_deactiv = pd.DataFrame(find_email_regex(deactivate_description_series), columns = ["UserPrincipalName"])
duplicate_check_deactiv.value_counts().sort_values(ascending=False)

duplicate_check_deactiv.value_counts().sort_values(ascending=False).to_csv("Duplicates.csv")