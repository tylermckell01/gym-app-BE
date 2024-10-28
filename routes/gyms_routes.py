from flask import Blueprint, request

import controllers

gyms = Blueprint('gyms', __name__)


@gyms.route('/gym', methods=['POST'])
def create_new_gym():
    return controllers.create_gym(request)


@gyms.route('/gyms', methods=['GET'])
def read_all_gyms():
    return controllers.read_gyms(request)


@gyms.route('/gym/<id>', methods=['PUT'])
def update_gym_name_by_id(id):
    return controllers.update_gym_name(request, id)


@gyms.route('/gym/delete/<id>', methods=['DELETE'])
def delete_gym_by_id(id):
    return controllers.delete_gym(request, id)
