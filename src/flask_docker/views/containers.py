from flask import jsonify, request, abort, Response
from views.utils.get_params import *
from views.http_params import http_params_dict
import docker

client = docker.from_env()

"""
Helper function to get a docker container from container_id
"""
def get_docker_container_from_id(container_id):
    try:
        container = client.containers.get(container_id)
    except:
        abort(404)
    return container

def calculate_container_cpu_percent(stats_dict):
    cpu_count = len(stats_dict["cpu_stats"]["cpu_usage"]["percpu_usage"])
    cpu_percent = 0.0
    cpu_delta = float(stats_dict["cpu_stats"]["cpu_usage"]["total_usage"]) - \
                float(stats_dict["precpu_stats"]["cpu_usage"]["total_usage"])
    system_delta = float(stats_dict["cpu_stats"]["system_cpu_usage"]) - \
                   float(stats_dict["precpu_stats"]["system_cpu_usage"])
    if system_delta > 0.0:
        cpu_percent = cpu_delta / system_delta * 100.0 * cpu_count
    return cpu_percent

#-----------------------------------------------------------------------------#   
#Containers View functions
#-----------------------------------------------------------------------------#  

def api_containers_run():
    parameters = get_HTTP_params(http_params_dict["api_containers_run"], request)
    try:
        container = client.containers.run(**parameters)
    except:
        abort(400)
        
    #If detach is True, a Container object is returned.
    print(parameters)
    if parameters["detach"]:    
        return container.attrs
    else:
        return ('', 204)


def api_containers_list():
    parameters = get_HTTP_params(http_params_dict["api_containers_list"], request)
    try:
        containers = client.containers.list(**parameters)
    except:
        abort(400)
    return jsonify([container.attrs for container in containers])


def api_containers_get():
    api_containers_get.get_params = {"container_id": {"default": None ,"type": str}}
    
    parameters = get_HTTP_params(api_containers_get.get_params, request)
    print(parameters)

    try:
        container = client.containers.get(**parameters)
    except:
        abort(400)
    return jsonify(container.attrs)



#-----------------------------------------------------------------------------#   
#Container View functions
#-----------------------------------------------------------------------------#  
def api_container_id(container_id):
    container = get_docker_container_from_id(container_id) 
    return jsonify(container.id)

def api_container_image(container_id):
    container = get_docker_container_from_id(container_id) 
    return jsonify(container.image.attrs)

def api_container_labels(container_id):
    container = get_docker_container_from_id(container_id) 
    return jsonify(container.labels)

def api_container_name(container_id):
    container = get_docker_container_from_id(container_id) 
    return jsonify(container.name)

def api_container_short_id(container_id):
    container = get_docker_container_from_id(container_id) 
    return jsonify(container.short_id)

def api_container_status(container_id):
    container = get_docker_container_from_id(container_id) 
    return jsonify(container.status)

def api_container_diff(container_id):
    container = get_docker_container_from_id(container_id) 
    return jsonify(container.diff())


def api_container_pause(container_id):
    container = get_docker_container_from_id(container_id) 
    try:
        container.pause()
    except:
        abort(400)
    return ('', 204)


def api_container_unpause(container_id):
    container = get_docker_container_from_id(container_id)
    try:
        container.unpause()
    except:
        abort(400)
    return ('', 204)


def api_container_rename(container_id):
    container = get_docker_container_from_id(container_id)
    parameters = get_HTTP_params(http_params_dict["api_container_rename"], request)
    try:
        container.rename(**parameters)
    except:
        abort(400)
    return ('', 204)


def api_container_start(container_id):
    container = get_docker_container_from_id(container_id)
    try:
        container.start()
    except:
        abort(400)
    return ('', 204)


def api_container_stop(container_id):
    container = get_docker_container_from_id(container_id)
    try:
        container.stop()
    except:
        abort(400)
    return ('', 204)

def api_container_top(container_id):
    container = get_docker_container_from_id(container_id)
    parameters = get_HTTP_params(http_params_dict["api_container_top"], request)
    return jsonify(container.top(**parameters))


def api_container_stats(container_id):
    container = get_docker_container_from_id(container_id)
    return jsonify(container.stats(decode=False, stream=False))


def api_container_cpu_usage(container_id):
    container = get_docker_container_from_id(container_id)
    stats_dict = container.stats(decode=False, stream=False)
    cpu_percent = calculate_container_cpu_percent(stats_dict)
    return jsonify(cpu_percent)


def api_container_reload(container_id):
    container = get_docker_container_from_id(container_id)
    try:
        container.reload()
    except:
        abort(400)
    return ('', 204)


def api_container_remove(container_id):
    container = get_docker_container_from_id(container_id)
    parameters = get_HTTP_params(http_params_dict["api_container_stop"], request)
    try:
        container.remove(**parameters)
    except:
        abort(400)
    return ('', 204)


def api_container_kill(container_id):
    container = get_docker_container_from_id(container_id)
    parameters = get_HTTP_params(http_params_dict["api_container_kill"], request)
    try:
        container.kill(**parameters)
    except:
        abort(400)
    return ('', 204)


def api_container_logs(container_id):
    container = get_docker_container_from_id(container_id)
    return Response(container.logs().decode("utf-8"), mimetype="text/plain")


def api_container_export(container_id):
    container = get_docker_container_from_id(container_id)
    return Response(container.export(), 
                    mimetype='application/octet-stream', 
                    headers=[('Content-Length', str()),
                            ('Content-Disposition', f"attachment; filename={container.id}.tar") ],)
