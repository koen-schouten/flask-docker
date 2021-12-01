from flask import jsonify, request, abort, Response
from views.utils.get_params import *
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
    api_images_prune.get_params = {"filters": {"default": None ,"type": dict}} 
    parameters = get_HTTP_params(api_images_prune.get_params, request)
    try:
        #pruned_data is a dict containing ImagesDeleted and SpaceReclaimed.
        pruned_data = client.images.prune(**parameters)
        return jsonify(pruned_data)
    except:
        abort(400)
        

def api_images_search():
    api_images_search.get_params = {
        "term": {"default": None ,"type": str},
        "limit": {"default": None ,"type": int}
    } 
    parameters = get_HTTP_params(api_images_search.get_params, request)
    print(parameters)
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
    api_image_tag.get_params = {
        "repository": {"default": None ,"type": str},
        "tag": {"default": None ,"type": str},
        } 
    parameters = get_HTTP_params(api_image_tag.get_params, request)
    print(parameters)
    try:
        image.tag(**parameters)
        return ('', 204)
    except:
        abort(400)
