from flask import json

def get_HTTP_params(get_param_dict, request):
    if request.method == 'GET':
        return get_params_from_HTTP_GET(get_param_dict, request)
    elif request.method in ['POST', 'PUT', 'DELETE']:
        if request.is_json:
            return get_params_from_json(get_param_dict, request)
        else:
            return get_params_from_HTTP_POST(get_param_dict, request)

def get_params_from_HTTP_GET(get_param_dict, request):
    parameters = {}
    for param_name, datatype_info in get_param_dict.items():
        parameter = request.args.get(key=param_name, default=datatype_info["default"], type=json.loads)
        parameters[param_name] = parameter
    return parameters


def get_params_from_HTTP_POST(get_param_dict, request):
    parameters = {}
    for param_name, datatype_info in get_param_dict.items():
        parameter = request.form.get(key=param_name, default=datatype_info["default"], type=json.loads)
        parameters[param_name] = parameter
    return parameters

def get_params_from_json(get_param_dict, request):
    json_params = request.get_json()
    parameters = {}
    for param_name, datatype_info in get_param_dict.items():
        if param_name in json_params:
            parameters[param_name] = json_params[parameters]
        else:
            parameters[param_name] = datatype_info["default"]
    return parameters