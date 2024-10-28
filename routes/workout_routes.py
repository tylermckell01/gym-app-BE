from flask import Blueprint, request

import controllers

workout = Blueprint('workout', __name__)


@workout.route('/workout', methods=['POST'])
def create_new_workout():
    return controllers.create_workout(request)


@workout.route('/workouts', methods=['GET'])
def read_all_workouts():
    return controllers.read_workouts(request)


@workout.route('/workouts/<id>', methods=["GET"])
def read_workouts_by_user(id):
    return controllers.read_workouts_by_user(request, id)


@workout.route('/workout/<id>', methods=['PUT'])
def update_workout(id):
    return controllers.update_workout_by_id(request, id)


@workout.route('/workout/exercise', methods=['POST'])
def add_xref():
    return controllers.workout_add_exercise(request)


@workout.route('/workout/exercise', methods=['DELETE'])
def delete_xref():
    return controllers.workout_remove_exercise(request)


@workout.route('/workout/delete/<id>', methods=['DELETE'])
def delete_workout_by_id(id):
    return controllers.delete_workout(request, id)
