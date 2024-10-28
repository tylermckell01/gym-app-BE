from flask import jsonify

from db import db
from lib.authenticate import auth, auth_admin
from models.gyms import Gyms, gym_schema, gyms_schema
from util.reflection import populate_object


@auth_admin
def create_gym(req):
    post_data = req.form if req.form else req.json

    gym_name = post_data.get('gym_name')
    exists_query = db.session.query(Gyms).filter(Gyms.gym_name == gym_name).first()

    if gym_name == "":
        return jsonify({'message': f'you must enter a name'}), 400

    if exists_query:
        return jsonify({'message': f'gym "{gym_name}" already exists in the database'}), 400

    new_gym = Gyms.new_gym_obj()
    populate_object(new_gym, post_data)

    try:
        db.session.add(new_gym)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'gym could not be created'}), 400

    return jsonify({'message': 'gym created', 'result': gym_schema.dump(new_gym)}), 201


@auth
def read_gyms(req):
    gym_query = db.session.query(Gyms).all()

    return jsonify({'message': 'gyms found', 'result': gyms_schema.dump(gym_query)}), 200


@auth_admin
def update_gym_name(req, gym_id):
    post_data = req.form if req.form else req.json
    gym_query = db.session.query(Gyms).filter(Gyms.gym_id == gym_id).first()

    populate_object(gym_query, post_data)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({'message': 'gym could not be updated'}), 400

    return jsonify({'message': 'gym updated', 'result': gym_schema.dump(gym_query)}), 200


@auth_admin
def delete_gym(req, gym_id):
    query = db.session.query(Gyms).filter(Gyms.gym_id == gym_id).first()

    if not query:
        return jsonify({"message": f"that gym does not exist"}), 400

    try:
        db.session.delete(query)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"message": "unable to delete record"}), 400

    return jsonify({"message": "gym deleted"}), 200
