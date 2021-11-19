from flask import Flask, jsonify, request, abort, json
import docker

client = docker.from_env()
app = Flask(__name__)

def recursively_build_json(val):
    if isinstance(val, list):
        new_val = [recursively_build_json(item) for item in val]
    elif type(val) is dict:
        new_val = {key:recursively_build_json(value) for (key,value) in val.items()}
    elif hasattr(val, '_asdict'):
        new_val = {key:recursively_build_json(value) for (key,value) in val._asdict().items()}
    else:
        new_val = val
    return new_val


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/docker/api/containers/list", methods=['GET'])
def api_containers_list():
    api_containers_list.get_params = {"all": {"default": False ,"type": bool},
                                      "since": {"default": None ,"type": str},
                                      "before": {"default": None ,"type": str},
                                      "limit": {"default": None ,"type": str},
                                      "filters": {"default": None ,"type": dict},
                                      "sparse": {"default": False ,"type": bool},
                                      "ignore_removed": {"default": False ,"type": bool}
                                      }
    
    parameters = {}
    for param_name, datatype_info in api_containers_list.get_params.items():
        parameter = request.args.get(key=param_name, default=datatype_info["default"], type=json.loads)
        parameters[param_name] = parameter

    try:
        containers = client.containers.list(**parameters)
    except:
        abort(400)
    return jsonify([container.attrs for container in containers])