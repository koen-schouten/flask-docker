from flask import jsonify, request, abort, Response
from views.utils.get_params import *
from views.http_params import http_params_dict
import docker

client = docker.from_env()

"""
Helper function to get docker image from image_name
"""
def get_docker_image_from_name(name):
    try:
        image = client.images.get(name)
    except:
        abort(404)
    return image

#-----------------------------------------------------------------------------#   
#Images View functions
#-----------------------------------------------------------------------------#   

def api_images_list():
    image_list = client.images.list()
    return jsonify([image.attrs for image in image_list])


def api_images_load():
    if len(request.files) == 1:
        #files.items[0] is a tuple (filename, file) so therefore [1] at the end
        file = next(iter(request.files.items()))[1]
        #client.images.load(file) returns an image list. 
        #There is only one image so therefore the [0] at the end.
        image = client.images.load(file)[0]
        return jsonify(image.attrs)
    abort(400)
    

def api_images_prune():
    parameters = get_HTTP_params(http_params_dict["api_images_prune"], request)
    try:
        #pruned_data is a dict containing ImagesDeleted and SpaceReclaimed.
        pruned_data = client.images.prune(**parameters)
        return jsonify(pruned_data)
    except:
        abort(400)
        

def api_images_search():
    parameters = get_HTTP_params(http_params_dict["api_images_search"], request)
    try:
        image_list = client.images.search(**parameters)
        return jsonify(image_list)
    except:
        abort(400)
 
   
#-----------------------------------------------------------------------------#   
#Image View functions
#-----------------------------------------------------------------------------#   
def api_image_attrs(image_id):
    image = get_docker_image_from_name(image_id) 
    return jsonify(image.attrs)


def api_image_id(image_id):
    image = get_docker_image_from_name(image_id) 
    return jsonify(image.id)


def api_image_labels(image_id):
    image = get_docker_image_from_name(image_id) 
    return jsonify(image.labels)


def api_image_short_id(image_id):
    image = get_docker_image_from_name(image_id) 
    return jsonify(image.short_id)


def api_image_tags(image_id):
    image = get_docker_image_from_name(image_id) 
    return jsonify(image.tags)


def api_image_history(image_id):
    image = get_docker_image_from_name(image_id) 
    return jsonify(image.history())


def api_image_reload(image_id):
    image = get_docker_image_from_name(image_id) 
    try:
        image.reload()
        return ('', 204)
    except:
        abort(400)
        

def api_container_image_save(image_id):
    image = get_docker_image_from_name(image_id)
    return Response(image.save(), 
                    mimetype='application/octet-stream', 
                    headers=[('Content-Length', str()),
                            ('Content-Disposition', f"attachment; filename={image.id}.tar") ],)
    

def api_image_tag(image_id):
    image = get_docker_image_from_name(image_id) 
    parameters = get_HTTP_params(http_params_dict("api_image_tag"), request)
    try:
        image.tag(**parameters)
        return ('', 204)
    except:
        abort(400)
