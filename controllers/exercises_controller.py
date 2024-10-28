from flask import jsonify

from db import db
from lib.authenticate import auth, auth_admin
from models.exercises import Exercises, exercise_schema, exercises_schema
from util.reflection import populate_object


@auth_admin
def create_exercise(req):
    post_data = req.form if req.form else req.json

    exercise_name = post_data.get('exercise_name')
    exists_query = db.session.query(Exercises).filter(Exercises.exercise_name == exercise_name).first()

    if exists_query:
        return jsonify({'message': f'exercise "{exercise_name}" already exists in the database'}), 400

    if exercise_name == "":
        return jsonify({'message': f'you must enter a name'}), 400

    new_exercise = Exercises.new_exercise_obj()
    populate_object(new_exercise, post_data)

    try:
        db.session.add(new_exercise)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({'message': 'exercise could not be created'}), 400

    return jsonify({'message': 'exercise created', 'result': exercise_schema.dump(new_exercise)}), 201


@auth
def read_exercises(req):
    exercise_query = db.session.query(Exercises).all()

    return jsonify({'message': 'exercises found', 'result': exercises_schema.dump(exercise_query)}), 200


@auth_admin
def update_exercise(req, exercise_id):
    post_data = req.form if req.form else req.json
    exercise_query = db.session.query(Exercises).filter(Exercises.exercise_id == exercise_id).first()

    populate_object(exercise_query, post_data)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({'message': 'exercise could not be updated'}), 400

    return jsonify({'message': 'exercise updated', 'result': exercise_schema.dump(exercise_query)}), 200


@auth_admin
def delete_exercise(req, exercise_id):
    query = db.session.query(Exercises).filter(Exercises.exercise_id == exercise_id).first()

    if not query:
        return jsonify({"message": f"exercise does not exist"}), 400

    try:
        db.session.delete(query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete record"}), 400

    return jsonify({"message": "exercise deleted"}), 200
