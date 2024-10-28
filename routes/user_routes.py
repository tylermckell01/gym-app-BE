from flask import Blueprint, request

import controllers

users = Blueprint('users', __name__)


@users.route('/user', methods=['POST'])
def add_user():
    return controllers.add_user(request)


@users.route('/users', methods=['GET'])
def read_all_users():
    return controllers.read_users(request)


@users.route('/user/<id>', methods=['PUT'])
def update_user(id):
    return controllers.update_user_by_id(request, id)


@users.route('/user/delete/<id>', methods=['DELETE'])
def delete_user(id):
    return controllers.delete_user(request, id)
