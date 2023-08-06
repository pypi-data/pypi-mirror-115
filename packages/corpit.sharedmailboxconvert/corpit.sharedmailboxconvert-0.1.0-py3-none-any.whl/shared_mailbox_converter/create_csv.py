#Importing modules
import requests
from requests.auth import HTTPBasicAuth
import json
import csv
import pandas as pd
import os
import xml.etree.ElementTree as ET

#Directory Paths
root_path = os.path.dirname(os.path.realpath(__file__))
output_path = root_path + "//output//"
os.chdir(output_path)

#config file for auth key
tree = ET.parse('config_jira.xml')
root = tree.getroot()
username = root.find('username').text
password = root.find('password').text

#Authenticate
auth = HTTPBasicAuth(username, password)

def get_issues_from_filter(filter_id):

    url = "https://assuranceiq.atlassian.net/rest/api/3/filter/" + str(filter_id)
    
    headers = {
        "Accept": "application/json"
    }

    response = requests.request(
       "GET",
       url,
       headers=headers,
       auth=auth
    )

    filter_object = json.loads(response.text)

    return filter_object["searchUrl"]

def get_issues(temp_url):

    url = temp_url

    headers = {
       "Accept": "application/json"
    }

    response = requests.request(
        "GET",
        url,
        headers=headers,
        auth=auth
    )

    #print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
    temp_dict = json.loads(response.text)
    #get_issues(temp)
    
    temp_arr = []
    #print(type(temp_dict["issues"]))
    for items in temp_dict["issues"]:
        issue_key = items["key"]
        temp_arr.append(issue_key)
        
    return temp_arr

def get_descriptions(issue_key):
    url = "https://assuranceiq.atlassian.net/rest/api/3/issue/" + issue_key
    
    headers = {
        "Accept": "application/json"
    }

    response = requests.request(
       "GET",
       url,
       headers=headers,
       auth=auth
    )
    
   
    
    issue = json.loads(response.text)
    content = issue["fields"]["description"]["content"][0]["content"][0]["text"]
    wrapper = json.loads(content)
    
    descriptions = wrapper["body"]
    return descriptions

def organize_data(test_input):
    temp_list = []
    return_df = pd.DataFrame()
    #def organize_csv
    for item in test_input:
        user_id = item["userIdentifier"]
        user_email = item["email"]
        user_status = item["userStatus"]
        temp_dict =  {"userIdentifier": user_id,
                     "email" : user_email,
                      "userStatus": user_status
                     }
        temp_list.append(temp_dict)
    return_df = pd.DataFrame(temp_list)
        
        
    return return_df


# def process_output(ticket_number):
#     deactive_series = pd.DataFrame(organize_data(get_descriptions(ticket_number))[0], name = "email")
#     #reactive_series = pd.Series(organize_data(get_descriptions(ticket_number))[1], name = "email")
    
#     return deactive_series, reactive_series


issues = get_issues(get_issues_from_filter(10364))

for issue in issues:
    organize_data(get_descriptions(issue)).to_csv(issue + ".csv", index = False)
    #process_output(issue)[1].to_csv(issue + "reactive_series.csv", header = "email", index = False)
