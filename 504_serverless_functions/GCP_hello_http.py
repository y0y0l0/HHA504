import functions_framework

@functions_framework.http
def hello_http(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'name' in request_json:
        name = request_json['name']
    elif request_args and 'name' in request_args:
        name = request_args['name']
    else:
        name = 'World'
    
    if request_json and 'spo2' in request_json:
        spo2 = request_json['spo2']
    elif request_args and 'spo2' in request_args:
        spo2 = request_args['spo2']
    else:
        spo2 = 'Please enter something'
    """
    response_string = f'Hello {name}! Oxygenation is {oxygen}.'
    return response_string
    """
    spo2 = float(spo2)
    
    if spo2>=92:
        label = 'Normal'
    else: 
        label ='Abbormal Chronic Condition Warning!'
    
    response_string = 'Hello {}!\n\r'.format(name)
    response_string = f'{response_string}Oxygenation value entered: {spo2}.\n\r'
    response_string = f'{response_string}Interpertation: {label}.\n\r'
    return response_string
    
    
    
    
    
    
    