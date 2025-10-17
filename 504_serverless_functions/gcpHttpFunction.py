import json
import functions_framework

@functions_framework.http
def hello_http(request):
    """HTTP Cloud Function.
    Expects JSON with 'SpO2' and 'Pulse' (or query params as fallback).
    Returns a JSON classification of SpO2 and Pulse rate.
    """
    # Prefer JSON body; fall back to query parameters for convenience
    data = request.get_json(silent=True) or {}
    args = request.args or {}

    spo2 = data.get("SpO2", args.get("SpO2"))
    pulse = data.get("Pulse", args.get("Pulse"))

    # Presence check
    if spo2 is None:
        return (
            json.dumps({"error": " 'SpO2' is a required field."}),
            400,
            {"Content-Type": "application/json"},
        )
     # Presence check
    if pulse is None:
        return (
            json.dumps({"error": " 'Pulse' is a required field."}),
            400,
            {"Content-Type": "application/json"},
        )
    # Type/convert check
    try:
        spo2_val = float(spo2)
    except (TypeError, ValueError):
        return (
            json.dumps({"error": "'SpO2' must be numbers."}),
            400,
            {"Content-Type": "application/json"},
        )
    try:
        pulse_val = float(pulse)
    except (TypeError, ValueError):
        return (
            json.dumps({"error": "'Pulse' must be numbers."}),
            400,
            {"Content-Type": "application/json"},
        )
    # Validate SpO2 range (0-100)
    if spo2_val < 0 or spo2_val >= 100:
            return (
                json.dumps({"error": "'SpO2' must be between 0 and 100."}),
                400,
                {"Content-Type": "application/json"},
            )
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

    payload = {
        "SpO2": spo2_val,
        "Pulse": pulse_val,
        "status": status,
        "category": category,
    }

    return json.dumps(payload), 200, {"Content-Type": "application/json"}