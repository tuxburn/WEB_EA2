from flask import request, jsonify, Blueprint
from db import (
    add_module, get_modules, get_module, update_module, delete_module,
    add_sensor_to_module, get_sensor, update_sensor, delete_sensor
)

routes = Blueprint('routes', __name__)

# Rutas para módulos

@routes.route('/modulos/', methods=['POST'])
def create_module():
    module = request.json
    result = add_module(module)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result), 201

@routes.route('/modulos/', methods=['GET'])
def get_all_modules():
    modules = get_modules()
    return jsonify(modules), 200

@routes.route('/modulos/<modulo_id>', methods=['GET'])
def get_single_module(modulo_id):
    result = get_module(modulo_id)
    if "error" in result:
        return jsonify(result), 404
    return jsonify(result), 200

@routes.route('/modulos/<modulo_id>', methods=['PUT'])
def update_single_module(modulo_id):
    data = request.json
    result = update_module(modulo_id, data)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result), 200

@routes.route('/modulos/<modulo_id>', methods=['DELETE'])
def delete_single_module(modulo_id):
    result = delete_module(modulo_id)
    if "error" in result:
        return jsonify(result), 404
    return jsonify(result), 200

# Rutas para sensores en un módulo

@routes.route('/modulos/<modulo_id>/sensores', methods=['POST'])
def create_sensor_in_module(modulo_id):
    sensor = request.json
    result = add_sensor_to_module(modulo_id, sensor)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result), 201

@routes.route('/modulos/<modulo_id>/sensores/<sensor_id>', methods=['GET'])
def get_sensor_in_module(modulo_id, sensor_id):
    result = get_sensor(modulo_id, sensor_id)
    if "error" in result:
        return jsonify(result), 404
    return jsonify(result), 200

@routes.route('/modulos/<modulo_id>/sensores/<sensor_id>', methods=['PUT'])
def update_sensor_in_module(modulo_id, sensor_id):
    data = request.json
    result = update_sensor(modulo_id, sensor_id, data)
    if "error" in result:
        return jsonify(result), 500
    return jsonify(result), 200

@routes.route('/modulos/<modulo_id>/sensores/<sensor_id>', methods=['DELETE'])
def delete_sensor_in_module(modulo_id, sensor_id):
    result = delete_sensor(modulo_id, sensor_id)
    if "error" in result:
        return jsonify(result), 404
    return jsonify(result), 200
