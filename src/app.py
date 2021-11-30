from flask import Flask, jsonify, request, abort, Response
from utils import *
import docker

client = docker.from_env()
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
#-----------------------------------------------------------------------------#   
#Containers
#-----------------------------------------------------------------------------# 
@app.route("/docker/api/containers/run", methods=['POST'])
def api_containers_run():
    api_containers_run.get_params = {
        "image": {"default": None ,"type": str},
        "command": {"default": None ,"type": str},
        "auto_remove": {"default": None ,"type": bool},
        "blkio_weight_device": {"default": None ,"type": dict},
        "blkio_weight": {"default": None ,"type": int},
        "cap_add": {"default": None ,"type": str},
        "cap_drop": {"default": None ,"type": str},
        "cgroup_parent": {"default": None ,"type": str},
        "cpu_count": {"default": None ,"type": int},
        "cpu_percent": {"default": None ,"type": int},
        "cpu_period": {"default": None ,"type": int},
        "cpu_quota": {"default": None ,"type": int},
        "cpu_rt_period": {"default": None ,"type": int},
        "cpu_rt_runtime": {"default": None ,"type": int},
        "cpu_shares": {"default": None ,"type": int},
        "cpuset_cpus": {"default": None ,"type": int},
        "cpuset_mems": {"default": None ,"type": str},
        "detach": {"default": True ,"type": bool},
        "device_cgroup_rules": {"default": None ,"type": list},
        "device_read_bps": {"default": None ,"type": dict},
        "device_read_iops": {"default": None ,"type": int},
        "device_write_bps": {"default": None ,"type": int},
        "device_write_iops": {"default": None ,"type": int},
        "devices": {"default": None ,"type": list},
        "dns": {"default": None ,"type": list},
        "dns_opt": {"default": None ,"type": list},
        "dns_search": {"default": None ,"type": list},
        "domainname": {"default": None ,"type": str},
        "entrypoint": {"default": None ,"type": str},
        "environment": {"default": None ,"type": dict},
        "extra_hosts": {"default": None ,"type": dict},
        "healthcheck": {"default": None ,"type": dict},
        "hostname": {"default": None ,"type": str},
        "init": {"default": None ,"type": bool},
        "init_path": {"default": None ,"type": str},
        "ipc_mode": {"default": None ,"type": str},
        "isolation": {"default": None ,"type": str},
        "kernel_memory": {"default": None ,"type": int},
        "labels": {"default": None ,"type": dict},
        "links": {"default": None ,"type": dict},
        #"log_config": {"default": None ,"type": logConfic},
        "lxc_conf": {"default": None ,"type": dict},
        "mac_address": {"default": None ,"type": str},
        "mem_limit": {"default": None ,"type": int},
        "mem_reservation": {"default": None ,"type": int},
        "mem_swappiness": {"default": None ,"type": int},
        "memswap_limit": {"default": None ,"type": str},
        "mounts": {"default": None ,"type": list},
        "name": {"default": None ,"type": str},
        "nano_cpus": {"default": None ,"type": int},
        "network": {"default": None ,"type": str},
        "network_disabled": {"default": None ,"type": bool},
        "network_mode": {"default": None ,"type": str},
        "oom_kill_disable": {"default": None ,"type": bool},
        "oom_score_adj": {"default": None ,"type": int},
        "pid_mode": {"default": None ,"type": str},
        "pids_limit": {"default": None ,"type": int},       
        "platform": {"default": None ,"type": str}, 
        "pids_limit": {"default": None ,"type": int},         
        "ports": {"default": None ,"type": dict}, 
        "privileged": {"default": None ,"type": bool},
        "publish_all_ports": {"default": None ,"type": bool},
        "read_only": {"default": None ,"type": bool},
        "remove": {"default": False ,"type": bool},       
        "restart_policy": {"default": None ,"type": dict}, 
        "runtime": {"default": None ,"type": str},         
        "security_opt": {"default": None ,"type": list}, 
        "shm_size": {"default": None ,"type": str},
        "stdin_open": {"default": None ,"type": bool},      
        "stdout": {"default": True ,"type": bool},      
        "stderr": {"default": False ,"type": bool},      
        "stop_signal": {"default": None ,"type": str},      
        "storage_opt": {"default": None ,"type": dict},   
        "stream": {"default": False ,"type": bool},      
        "sysctls": {"default": None ,"type": dict},      
        "tmpfs": {"default": None ,"type": dict},                                                    
        "tty": {"default": None ,"type": bool},      
        "ulimits": {"default": None ,"type": list},      
        "use_config_proxy": {"default": None ,"type": bool},      
        "user": {"default": None ,"type": str},      
        "userns_mode": {"default": None ,"type": str},                                      
        "uts_mode": {"default": None ,"type": str},      
        "version": {"default": None ,"type": str},
        "volume_driver": {"default": None ,"type": str},
        "volumes": {"default": None ,"type": dict},
        "volumes_from": {"default": None ,"type": list},
        "working_dir": {"default": None ,"type": str},                
    }
    
    parameters = get_HTTP_params(api_containers_run.get_params, request)
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

#-----------------------------------------------------------------------------#   
#Container
#-----------------------------------------------------------------------------#  
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
                                      "link": {"default": False ,"type": str},
                                      "force": {"default": False ,"type": str}  
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
    return Response(container.export(), 
                    mimetype='application/octet-stream', 
                    headers=[('Content-Length', str()),
                            ('Content-Disposition', "attachment; filename=export.tar") ],)

#-----------------------------------------------------------------------------#   
#Images
#-----------------------------------------------------------------------------#   

@app.route("/docker/api/images/list", methods=['GET'])
def api_images_list():
    image_list = client.images.list()
    return jsonify([image.attrs for image in image_list])


def get_docker_image_from_name(name):
    try:
        image = client.images.get(name)
    except:
        abort(404)
    return image

#-----------------------------------------------------------------------------#   
#Image
#-----------------------------------------------------------------------------#   
@app.route("/docker/api/image/<image_id>/attrs", methods=['GET'])
def api_image_attrs(image_id):
    image = get_docker_image_from_name(image_id) 
    return jsonify(image.attrs)


@app.route("/docker/api/image/<image_id>/id", methods=['GET'])
def api_image_id(image_id):
    image = get_docker_image_from_name(image_id) 
    return jsonify(image.id)


@app.route("/docker/api/image/<image_id>/labels", methods=['GET'])
def api_image_labels(image_id):
    image = get_docker_image_from_name(image_id) 
    return jsonify(image.labels)


@app.route("/docker/api/image/<image_id>/short_id", methods=['GET'])
def api_image_short_id(image_id):
    image = get_docker_image_from_name(image_id) 
    return jsonify(image.short_id)


@app.route("/docker/api/image/<image_id>/tags", methods=['GET'])
def api_image_short_tags(image_id):
    image = get_docker_image_from_name(image_id) 
    return jsonify(image.tags)


@app.route("/docker/api/image/<image_id>/history", methods=['GET'])
def api_image_short_history(image_id):
    image = get_docker_image_from_name(image_id) 
    return jsonify(image.history())


@app.route("/docker/api/image/<image_id>/reload", methods=['PUT'])
def api_image_short_reload(image_id):
    image = get_docker_image_from_name(image_id) 
    try:
        image.reload()
        return ('', 204)
    except:
        abort(400)
        

@app.route("/docker/api/image/<image_id>/save", methods=['GET'])
def api_container_image_save(image_id):
    image = get_docker_image_from_name(image_id)
    return Response(image.save(), 
                    mimetype='application/octet-stream', 
                    headers=[('Content-Length', str()),
                            ('Content-Disposition', "attachment; filename=image.tar") ],)

