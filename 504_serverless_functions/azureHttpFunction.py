import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="http_trigger1")
def http_trigger1(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    spo2 = req.params.get('spo2')
    pulse = req.params.get('pulse')
    category ='unknown'
    status= 'None'
    try:
        req_body = req.get_json()
    except Exception:
        req_body = {}
    else:
        name = req_body.get('name')
        spo2 = req_body.get('spo2')
        pulse = req_body.get('pulse')

    payload = {
            "name": name,
            "spo2": spo2,
            "pulse": pulse,
            "status": status,
            "category": category
        }
    if name is None and spo2 is None and pulse is None:
        status = "'Name', 'Spo2', and 'Pulse' are required fields in the request body for a personalized response."
        message = status
        payload["status"] = status
        logging.info(message)
        return func.HttpResponse(message+"\n\n"+str(payload),status_code=400)
    if name is not None and spo2 is None and pulse is None:
        status = "Hello {name}, 'Spo2' and 'Pulse' are required fields in the request body for a personalized response.".format(name=name)
        message = status
        payload["status"] = status
        logging.info(message)
        return func.HttpResponse(message+"\n\n"+str(payload),status_code=400)
    if name is None:
         status = "'Name' is a required field in the request body for a personalized response."
         message = status
         payload["status"] = status
         logging.info(message)
         return func.HttpResponse(message+"\n\n"+str(payload),status_code=400)
    if name is not None and spo2 is None:
        status = "Hello {name}, 'SpO2' is a required field in the request body for a personalized response.".format(name=name)
        message = status
        payload["status"] = status
        logging.info(message)
        return func.HttpResponse(message+"\n\n"+str(payload),status_code=400)
    if name is not None and pulse is None:
        status = "Hello {name}, 'Pulse' is a required field in the request body for a personalized response.".format(name=name)
        message = status
        payload["status"] = status
        logging.info(message)
        return func.HttpResponse(message+"\n\n"+str(payload),status_code=400)
    if name is None and spo2 is None:
        status = "'SpO2' is a required field in the request body for a personalized response."
        message = status
        payload["status"] = status
        logging.info(message)
        return func.HttpResponse(message+"\n\n"+str(payload),status_code=400)
    if name is None and pulse is None:
        status = "'Pulse' is a required field in the request body for a personalized response."
        message = status
        payload["status"] = status
        logging.info(message)
        return func.HttpResponse(message+"\n\n"+str(payload),status_code=400)
    if name is not None and spo2 and pulse:
        # Type/convert check
        try:
            spo2_val = float(spo2)
        except (TypeError, ValueError):
            status = "'SpO2' must be numbers."
            message = status
            payload["status"] = status
            logging.info(message)
            return func.HttpResponse(message+"\n\n"+str(payload),status_code=400)
        try:
            pulse_val = float(pulse)
        except (TypeError, ValueError):
            status = "'Pulse' must be numbers."
            message = status
            payload["status"] = status
            logging.info(message)
            return func.HttpResponse(message+"\n\n"+str(payload),status_code=400)
    # Validate SpO2 range (0-100)
    if spo2_val < 0 or spo2_val >= 100:
            status = "'SpO2' must be between 0 and 100."
            message = status
            payload["status"] = status
            logging.info(message)
            return func.HttpResponse(message+"\n\n"+str(payload),status_code=400)
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
        case _ if spo2_val >= 95 and (pulse_val <= 60 or pulse_val > 100):
            status = "Abnormal Heart Rate Warning"
        case _ if spo2_val >= 95 and (pulse_val <= 20 or pulse_val > 120):
            status = "Abnormal Severe Heart Rate Warning"
        case _ if spo2_val >= 95 and pulse_val >= 60 and pulse_val <= 100:
            status = "normal"
        case _ if spo2_val < 95 and (pulse_val < 60 or pulse_val > 100):
            status = "Abnormal Chronic Condition Warning"
        case _ if spo2_val < 95 and pulse_val >= 60 and pulse_val <= 100:
            status = "Abnormal Respiratory Warning"
        case _ if spo2_val < 92 and pulse_val >= 60 and pulse_val <= 100:
            status = "Abnormal Severe Respiratory Warning"
        case _ if spo2_val < 90 and pulse_val >= 60 and pulse_val <= 100:
            status = "Abnormal Critical Respiratory Warning"
    category = "Normal" if status == "normal" else "Abnormal"
    payload["status"] = status
    payload["category"] = category
    message = "Hello, {name}. Your oxigenation is {spo2} with pulse rate of {pulse}. Your report status is {category}. Please review {status} status with your healthcare provider.".format(name=name, spo2=spo2, pulse=pulse, category=category, status=status)
    logging.info(message)
    return func.HttpResponse(message+"\n\n"+str(payload), status_code=200)
