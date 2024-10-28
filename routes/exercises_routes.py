from flask import Blueprint, request

import controllers

exercises = Blueprint('exercises', __name__)


@exercises.route('/exercise', methods=['POST'])
def create_new_exercise():
    return controllers.create_exercise(request)


@exercises.route('/exercises', methods=['GET'])
def read_all_exercises():
    return controllers.read_exercises(request)


@exercises.route('/exercise/<id>', methods=['PUT'])
def update_exercise_by_id(id):
    return controllers.update_exercise(request, id)


@exercises.route('/exercise/delete/<id>', methods=['DELETE'])
def delete_exercise_by_id(id):
    return controllers.delete_exercise(request, id)
