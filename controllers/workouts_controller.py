from flask import jsonify

from db import db
from lib.authenticate import auth, auth_admin
from models.workouts import Workouts, workout_schema, workouts_schema
from models.exercises import Exercises
from util.reflection import populate_object


@auth_admin
def create_workout(req):
    post_data = req.form if req.form else req.json

    workout_name = post_data.get('workout_name')
    exists_query = db.session.query(Workouts).filter(Workouts.workout_name == workout_name).first()

    if exists_query:
        return jsonify({'message': f'workout "{workout_name}" already exists in the database'}), 400

    new_workout = Workouts.new_workout_obj()
    populate_object(new_workout, post_data)

    try:
        db.session.add(new_workout)
        db.session.commit()
    except Exception as e:
        print("exception", e)
        db.session.rollback()
        return jsonify({'message': 'workout could not be created'}), 400

    return jsonify({'message': 'workout created', 'result': workout_schema.dump(new_workout)}), 201


@auth
def read_workouts(req):
    workout_query = db.session.query(Workouts).all()

    return jsonify({'message': 'workouts found', 'result': workouts_schema.dump(workout_query)}), 200


@auth
def read_workouts_by_user(req, user_id):
    workout_query = db.session.query(Workouts).filter(Workouts.user_id == user_id).all()
    return jsonify({'message': 'workouts found', 'result': workouts_schema.dump(workout_query)}), 200


@auth_admin
def update_workout_by_id(req, workout_id):
    post_data = req.form if req.form else req.json
    workout_query = db.session.query(Workouts).filter(Workouts.workout_id == workout_id).first()

    populate_object(workout_query, post_data)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({'message': 'workout could not be updated'}), 400

    return jsonify({'message': 'workout updated', 'result': workout_schema.dump(workout_query)}), 200


@auth_admin
def workout_add_exercise(req):
    post_data = req.form if req.form else req.json
    workout_id = post_data.get('workout_id')
    exercise_id = post_data.get('exercise_id')

    workout_query = db.session.query(Workouts).filter(Workouts.workout_id == workout_id).first()
    exercise_query = db.session.query(Exercises).filter(Exercises.exercise_id == exercise_id).first()

    workout_query.exercises.append(exercise_query)
    db.session.commit()

    return jsonify({'message': 'relationship added.', 'workout info': workout_schema.dump(workout_query)}), 200


@auth_admin
def workout_remove_exercise(req):
    post_data = req.form if req.form else req.json
    workout_id = post_data.get('workout_id')
    exercise_id = post_data.get('exercise_id')

    workout_query = db.session.query(Workouts).filter(Workouts.workout_id == workout_id).first()
    exercise_query = db.session.query(Exercises).filter(Exercises.exercise_id == exercise_id).first()

    if workout_query and exercise_query:
        workout_query.exercises.remove(exercise_query)
        db.session.commit()
        return jsonify({'message': 'relationship removed', 'results': workout_schema.dump(workout_query)}), 200
    else:
        return jsonify({'error': 'workout or exercise not found'}), 404


@auth_admin
def delete_workout(req, workout_id):
    query = db.session.query(Workouts).filter(Workouts.workout_id == workout_id).first()

    if not query:
        return jsonify({"message": f"workout by id {workout_id} does not exist"}), 400

    try:
        db.session.delete(query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete record"}), 400

    return jsonify({"message": "workout has been deleted"}), 200
