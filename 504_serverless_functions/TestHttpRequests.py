import requests
import os
from dotenv import load_dotenv
#load_dotenv()
load_dotenv()


# GCP Testing
gcp_url = "https://python504-307314263527.europe-west1.run.app"
## if post normal
r = requests.post(gcp_url, json={"SpO2": 95, "Pulse": 65})
print("GCP Normal Test: ",r.status_code, r.json())
## if post abnormal respiratory
r = requests.post(gcp_url, json={"SpO2": 82, "Pulse": 70})
print("GCP Abnormal Respiratory Test: ",r.status_code, r.json())
## if post abnormal heart rate
r = requests.post(gcp_url, json={"SpO2": 95, "Pulse": 125})
print("GCP Abnormal Heart Rate Test: ",r.status_code, r.json())
## if post abnormal heart rate and respiratory rate
r = requests.post(gcp_url, json={"SpO2": 80, "Pulse": 125})
print("GCP Abnormal Heart and Respiratory Rate Test: ",r.status_code, r.json())
## if get 
r = requests.get(gcp_url)
print("GCP GET Test: ",r.status_code, r.json())

# Azure Testing
azure_url = "https://python-serverless-gcffbjdngbgcbmg4.westus3-01.azurewebsites.net/api/http_trigger1?"+os.getenv("azure_master_key")
## if post missing vitals
r = requests.post(azure_url, json={"name":"Hagrid"})
print("Azure Missing Vitals Test: \n",r.status_code, r.reason, r.text)
## if post normal
r = requests.post(azure_url, json={"name":"Harry Potter","spo2": 95, "pulse": 65})
print("Azure Normal Test: \n",r.status_code, r.reason, r.text)
## if post abnormal respiratory
r = requests.post(azure_url, json={"name":"Hermione Granger","spo2": 15, "pulse": 77})
print("Azure Abnormal Respiratory Test: \n",r.status_code, r.reason, r.text)
## if post abnormal heart rate
r = requests.post(azure_url, json={"name":"Neville Longbottom","spo2": 97, "pulse": 127})
print("Azure Abnormal Heart Rate Test: \n",r.status_code, r.reason, r.text)
## if post abnormal heart and respiratory rate
r = requests.post(azure_url, json={"name":"Ron Weasley","spo2": 56, "pulse": 20})
print("Azure Abnormal Heart and Respiratory Rate Test: \n",r.status_code, r.reason, r.text)
## if get 
r = requests.get(azure_url)
print("Azure GET Test: \n",r.status_code, r.reason, r.text)