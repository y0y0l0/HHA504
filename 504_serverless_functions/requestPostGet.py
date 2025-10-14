import requests
url = "https://python504-307314263527.europe-west1.run.app"
## if post normal
#r = requests.post(url, json={"SpO2": 95, "Pulse": 65})
## if post abnormal respiratory
#r = requests.post(url, json={"SpO2": 90, "Pulse": 65})
## if post abnormal heart rate
r = requests.post(url, json={"SpO2": 95, "Pulse": 125})
## if get 
#r = requests.get(url)
print(r.status_code, r.json())