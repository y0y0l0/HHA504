### Serverless Functions Overview
This project utilizes serverless functions to handle backend logic and API requests. Serverless functions allow you to run code without managing servers, providing scalability and ease of deployment.
## Video Recordings:
## Learning Goal:
- Create a serverless function that handles HTTP requests and responses.
## Steps to Create a Serverless Function:
1. **Set Up Your Environment**: Ensure you have a serverless framework or platform set up (GCP and Azure).
2. **Create a New Function**: Use the platform's CLI or dashboard to create a new serverless function.
3. **Write Your Code**: Implement the logic for your function. This will evaluate HTTP requests and return appropriate responses.
4. **Deploy the Function**: Use the platform's deployment tools to deploy your function to the cloud.
5. **Test the Function**: Use tools like Postman or curl to send HTTP requests to your function and verify the responses.
Patient SpO2 and Pulse Rate Evaluation Function:
# Python (requests):
```
match spo2_val:
        # Classify based on SpO2 and Pulse values
        # Note: Pulse normal range is 60-100 bpm for adults
        # Source: https://www.heart.org/en/health-topics/high-blood-pressure/the-facts-about-high-blood-pressure/understanding-blood-pressure-readings
        # Note: SpO2 normal range is 95-100%
        # Source: https://www.verywellhealth.com/what-is-a-normal-spo2-level-914823
        # Note: SpO2 below 92% is considered low and may require medical attention
        # Source: https://www.mayoclinic.org/tests-procedures/pulse-oximetry/about/pac-20384743
        # Note: SpO2 below 90% is considered very low and requires immediate medical attention
        #   Source: https://www.cdc.gov/coronavirus/2019-ncov/hcp/clinical-guidance/critical-care.html
        # Note: Pulse below 60 bpm (bradycardia) or above 100 bpm (tachycardia) may indicate an abnormal heart rate
        # Source: https://www.heart.org/en/health-topics/arrhythmia/about-arrhythmia
        # Note: Pulse below 50 bpm or above 120 bpm is considered more severe and may require medical attention
        # Source: https://www.heart.org/en/health-topics/arrhythmia/about-arrhythmia
        case _ if spo2_val >= 95 and (pulse_val < 60 or pulse_val > 100):
            status = "Abnormal Heart Rate Warning!"
        case _ if spo2_val >= 95 and (pulse_val < 20 or pulse_val > 120):
            status = "Abnormal Severe Heart Rate Warning!"
        case _ if spo2_val >= 95 and pulse_val >= 60 and pulse_val <= 100:
            status = "normal"
        case _ if spo2_val < 95 and (pulse_val < 60 or pulse_val > 100):
            status = "Abnormal Chronic Condition Warning!"
        case _ if spo2_val < 95 and pulse_val >= 60 and pulse_val <= 100:
            status = "Abnormal Respiratory Warning!"
        case _ if spo2_val < 92 and pulse_val >= 60 and pulse_val <= 100:
            status = "Abnormal Severe Respiratory Warning!"
        case _ if spo2_val < 90 and pulse_val >= 60 and pulse_val <= 100:
            status = "Abnormal Critical Respiratory Warning!"
    category = "Normal" if status == "normal" else "Abnormal"
```
# Expected Output:
- If SpO2 is 95 or below: "abnormal SpO2 Level"
- If Pulse is below 60 or above 100: "Abnormal Pulse Rate"
- If both SpO2 and Pulse are within normal ranges: "Normal"

# Example usage:        
## Request Example Code Snippet:
```
import requests
url = "https://python504-307314263527.europe-west1.run.app"
## if post normal
r = requests.post(url, json={"SpO2": 95, "Pulse": 65})
## if post abnormal respiratory
r = requests.post(url, json={"SpO2": 90, "Pulse": 65})
## if post abnormal heart rate
r = requests.post(url, json={"SpO2": 95, "Pulse": 125})
## if get 
r = requests.get(url)
print(r.status_code, r.json())
```
# Response Example:
```
POST normal
200 
{
    'SpO2': 95.0, 
    'Pulse': 62.0, 
    'status': 'normal', 
    'category': 'Normal'
}

POST abnormal respiratory
200 
{
    'SpO2': 90.0, 
    'Pulse': 65.0, 
    'status': 'Abnormal Respiratory Warning!', 
    'category': 'Abnormal'
}

POST abnormal heart rate
200 
{
    'SpO2': 95.0, 
    'Pulse': 125.0, 
    'status': 'Abnormal Heart Rate Warning!', 
    'category': 'Abnormal'
}

GET
400
{
    "error": "Both 'SpO2' and 'Pulse' are required."
}
```
# Recording Requirements Recording Requirements (2–4 minutes)
Brief intro (name, which two clouds you chose).
Show your repository and where the cloud‑specific code lives.
Show the live endpoint(s) and execute a POST request with two examples (one normal, one abnormal).
Show where to find logs or monitoring in each cloud’s portal.
Mention any gotchas (permissions, runtime version, cold starts).
Upload the recording and place a shareable link in your README.