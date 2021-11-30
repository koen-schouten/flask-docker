from flask import Flask, jsonify, request, abort, json, Response
from utils import *
import docker

client = docker.from_env()
app = Flask(__name__)

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
    parameters = get_HTTP_params(api_containers_list.get_params, request)
    try:
        containers = client.containers.list(**parameters)
    except:
        abort(400)
    return jsonify([container.attrs for container in containers])


@app.route("/docker/api/containers/get", methods=['GET'])
def api_containers_get():
    api_containers_get.get_params = {"container_id": {"default": None ,"type": str}}
    
    parameters = get_HTTP_params(api_containers_get.get_params, request)
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
def api_container_status(container_id):
    container = get_docker_container_from_id(container_id) 
    return jsonify(container.status)

@app.route("/docker/api/container/<container_id>/diff", methods=['GET'])
def api_container_diff(container_id):
    container = get_docker_container_from_id(container_id) 
    return jsonify(container.diff())


@app.route("/docker/api/container/<container_id>/pause", methods=['PUT'])
def api_container_pause(container_id):
    container = get_docker_container_from_id(container_id) 
    try:
        container.pause()
    except:
        abort(400)
    return ('', 204)


@app.route("/docker/api/container/<container_id>/unpause", methods=['PUT'])
def api_container_unpause(container_id):
    container = get_docker_container_from_id(container_id)
    try:
        container.unpause()
    except:
        abort(400)
    return ('', 204)


@app.route("/docker/api/container/<container_id>/rename", methods=['PUT'])
def api_container_rename(container_id):
    container = get_docker_container_from_id(container_id)
    api_container_rename.get_params = {"name": {"default": None ,"type": str}}

    parameters = request.get_json()

    try:
        container.rename(**parameters)
    except:
        abort(400)
    return ('', 204)


@app.route("/docker/api/container/<container_id>/start", methods=['PUT'])
def api_container_start(container_id):
    container = get_docker_container_from_id(container_id)
    try:
        container.start()
    except:
        abort(400)
    return ('', 204)


@app.route("/docker/api/container/<container_id>/stop", methods=['PUT'])
def api_container_stop(container_id):
    container = get_docker_container_from_id(container_id)
    try:
        container.stop()
    except:
        abort(400)
    return ('', 204)

@app.route("/docker/api/container/<container_id>/top", methods=['GET'])
def api_container_top(container_id):
    container = get_docker_container_from_id(container_id)
    api_container_top.get_params = {"ps_args": {"default": None ,"type": str}}
    parameters = get_HTTP_params(api_container_top.get_params, request)
    return jsonify(container.top(**parameters))


@app.route("/docker/api/container/<container_id>/stats", methods=['GET'])
def api_container_stats(container_id):
    container = get_docker_container_from_id(container_id)
    return jsonify(container.stats(decode=False, stream=False))


@app.route("/docker/api/container/<container_id>/reload", methods=['PUT'])
def api_container_reload(container_id):
    container = get_docker_container_from_id(container_id)
    try:
        container.reload()
    except:
        abort(400)
    return ('', 204)


@app.route("/docker/api/container/<container_id>/remove", methods=['DELETE'])
def api_container_remove(container_id):
    container = get_docker_container_from_id(container_id)
    api_container_remove.get_params = {"v": {"default": False ,"type": bool},
                                      "link ": {"default": False ,"type": str},
                                      "force ": {"default": False ,"type": str}  
                                      } 
    parameters = get_HTTP_params(api_container_stop.get_params, request)
    try:
        container.remove(**parameters)
    except:
        abort(400)
    return ('', 204)


@app.route("/docker/api/container/<container_id>/kill", methods=['PUT'])
def api_container_kill(container_id):
    container = get_docker_container_from_id(container_id)
    api_container_kill.get_params = {"signal": {"default": None ,"type": int}} 
    parameters = get_HTTP_params(api_container_kill.get_params, request)
    print(parameters)
    try:
        container.kill(**parameters)
    except:
        abort(400)
    return ('', 204)


@app.route("/docker/api/container/<container_id>/logs", methods=['GET'])
def api_container_logs(container_id):
    container = get_docker_container_from_id(container_id)
    return Response(container.logs().decode("utf-8"), mimetype="text/plain")


@app.route("/docker/api/container/<container_id>/export", methods=['GET'])
def api_container_export(container_id):
    container = get_docker_container_from_id(container_id)
    print("test")
    return Response(container.export(), 
                    mimetype='application/octet-stream', 
                    headers=[('Content-Length', str()),
                            ('Content-Disposition', "attachment; filename=export.tar") ],)