import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db


class Gyms(db.Model):
    __tablename__ = 'Gyms'

    gym_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    gym_name = db.Column(db.String(), nullable=False, unique=True)

    def __init__(self, gym_name):
        self.gym_name = gym_name

    def new_gym_obj():
        return Gyms('')


class GymsSchema(ma.Schema):
    class Meta:
        fields = ['gym_id', 'gym_name', 'workouts']


gym_schema = GymsSchema()
gyms_schema = GymsSchema(many=True)
