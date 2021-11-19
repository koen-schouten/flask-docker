from flask import Flask, jsonify, request, abort, json
import docker

client = docker.from_env()
app = Flask(__name__)

def get_params_from_HTTP_get(get_param_dict, request):
    parameters = {}
    for param_name, datatype_info in get_param_dict.items():
        parameter = request.args.get(key=param_name, default=datatype_info["default"], type=json.loads)
        parameters[param_name] = parameter
    return parameters


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
    parameters = get_params_from_HTTP_get(api_containers_list.get_params, request)
    try:
        containers = client.containers.list(**parameters)
    except:
        abort(400)
    return jsonify([container.attrs for container in containers])


@app.route("/docker/api/containers/get", methods=['GET'])
def api_containers_get():
    api_containers_get.get_params = {"container_id": {"default": None ,"type": str}}
    
    parameters = get_params_from_HTTP_get(api_containers_get.get_params, request)
    print(parameters)

    try:
        container = client.containers.get(**parameters)
    except:
        abort(400)
    return jsonify(container.attrs)