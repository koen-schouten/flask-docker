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

def get_docker_container_from_id(container_id):
    try:
        container = client.containers.get(container_id)
    except:
        abort(404)
    return container

@app.route("/docker/api/container/<container_id>/id", methods=['GET'])
def api_container_id(container_id):
    container = get_docker_container_from_id(container_id) 
    return jsonify(container.id)

@app.route("/docker/api/container/<container_id>/image", methods=['GET'])
def api_container_image(container_id):
    container = get_docker_container_from_id(container_id) 
    return jsonify(container.image.attrs)

@app.route("/docker/api/container/<container_id>/labels", methods=['GET'])
def api_container_labels(container_id):
    container = get_docker_container_from_id(container_id) 
    return jsonify(container.labels)

@app.route("/docker/api/container/<container_id>/name", methods=['GET'])
def api_container_name(container_id):
    container = get_docker_container_from_id(container_id) 
    return jsonify(container.name)

@app.route("/docker/api/container/<container_id>/short_id", methods=['GET'])
def api_container_short_id(container_id):
    container = get_docker_container_from_id(container_id) 
    return jsonify(container.short_id)

@app.route("/docker/api/container/<container_id>/status", methods=['GET'])
def api_container_short_status(container_id):
    container = get_docker_container_from_id(container_id) 
    return jsonify(container.status)

@app.route("/docker/api/container/<container_id>/diff", methods=['GET'])
def api_container_short_diff(container_id):
    container = get_docker_container_from_id(container_id) 
    return jsonify(container.diff())


@app.route("/docker/api/container/<container_id>/pause", methods=['PUT'])
def api_container_short_pause(container_id):
    container = get_docker_container_from_id(container_id) 
    try:
        container.pause()
    except:
        abort(400)
    return ('', 204)


@app.route("/docker/api/container/<container_id>/unpause", methods=['PUT'])
def api_container_short_unpause(container_id):
    container = get_docker_container_from_id(container_id)
    try:
        container.unpause()
    except:
        abort(400)
    return ('', 204)