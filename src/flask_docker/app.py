from flask import Flask
from views.containers import * 
from views.images import * 

client = docker.from_env()
app = Flask(__name__)

#Container urls
app.add_url_rule('/docker/api/containers/run', view_func=api_containers_run, methods=['POST'])
app.add_url_rule('/docker/api/containers/list', view_func=api_containers_list, methods=['GET'])
app.add_url_rule('/docker/api/containers/get', view_func=api_containers_get, methods=['GET'])
app.add_url_rule('/docker/api/container/<container_id>/id', view_func=api_container_id, methods=['GET'])
app.add_url_rule('/docker/api/container/<container_id>/image', view_func=api_container_image, methods=['GET'])
app.add_url_rule('/docker/api/container/<container_id>/labels', view_func=api_container_labels, methods=['GET'])
app.add_url_rule('/docker/api/container/<container_id>/name', view_func=api_container_name, methods=['GET'])
app.add_url_rule('/docker/api/container/<container_id>/short_id', view_func=api_container_short_id, methods=['GET'])
app.add_url_rule('/docker/api/container/<container_id>/status', view_func=api_container_status, methods=['GET'])
app.add_url_rule('/docker/api/container/<container_id>/diff', view_func=api_container_diff, methods=['GET'])
app.add_url_rule('/docker/api/container/<container_id>/pause', view_func=api_container_pause, methods=['PUT'])
app.add_url_rule('/docker/api/container/<container_id>/unpause', view_func=api_container_unpause, methods=['PUT'])
app.add_url_rule('/docker/api/container/<container_id>/rename', view_func=api_container_rename, methods=['PUT'])
app.add_url_rule('/docker/api/container/<container_id>/start', view_func=api_container_start, methods=['PUT'])
app.add_url_rule('/docker/api/container/<container_id>/stop', view_func=api_container_stop, methods=['PUT'])
app.add_url_rule('/docker/api/container/<container_id>/top', view_func=api_container_top, methods=['GET'])
app.add_url_rule('/docker/api/container/<container_id>/stats', view_func=api_container_stats, methods=['GET'])
app.add_url_rule('/docker/api/container/<container_id>/reload', view_func=api_container_reload, methods=['PUT'])
app.add_url_rule('/docker/api/container/<container_id>/remove', view_func=api_container_remove, methods=['DELETE'])
app.add_url_rule('/docker/api/container/<container_id>/kill', view_func=api_container_kill, methods=['PUT'])
app.add_url_rule('/docker/api/container/<container_id>/logs', view_func=api_container_logs, methods=['GET'])
app.add_url_rule('/docker/api/container/<container_id>/export', view_func=api_container_export, methods=['GET'])

#Image urls
app.add_url_rule('/docker/api/images/list', view_func=api_images_list, methods=['GET'])
app.add_url_rule('/docker/api/images/load', view_func=api_images_load, methods=['POST'])
app.add_url_rule('/docker/api/images/prune', view_func=api_images_prune, methods=['DELETE'])
app.add_url_rule('/docker/api/images/search', view_func=api_images_search, methods=['GET'])
app.add_url_rule('/docker/api/image/<image_id>/attrs', view_func=api_image_attrs, methods=['GET'])
app.add_url_rule('/docker/api/image/<image_id>/id', view_func=api_image_id, methods=['GET'])
app.add_url_rule('/docker/api/image/<image_id>/labels', view_func=api_image_labels, methods=['GET'])
app.add_url_rule('/docker/api/image/<image_id>/short_id', view_func=api_image_short_id, methods=['GET'])
app.add_url_rule('/docker/api/image/<image_id>/tags', view_func=api_image_tags, methods=['GET'])
app.add_url_rule('/docker/api/image/<image_id>/history', view_func=api_image_history, methods=['GET'])
app.add_url_rule('/docker/api/image/<image_id>/reload', view_func=api_image_reload, methods=['PUT'])
app.add_url_rule('/docker/api/image/<image_id>/save', view_func=api_container_image_save, methods=['GET'])
app.add_url_rule('/docker/api/image/<image_id>/tag', view_func=api_image_tag, methods=['PUT'])