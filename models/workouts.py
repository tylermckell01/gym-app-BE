import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db
from .workouts_exercises_xref import workouts_exercises_association_table


class Workouts(db.Model):
    __tablename__ = "Workouts"

    workout_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workout_name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    length = db.Column(db.Float(), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Users.user_id"), nullable=False)

    exercises = db.relationship("Exercises", secondary=workouts_exercises_association_table, back_populates='workouts')
    user = db.relationship("Users", back_populates='workouts')

    def __init__(self, workout_name, description, length, user_id):
        self.workout_name = workout_name
        self.description = description
        self.length = length
        self.user_id = user_id

    def new_workout_obj():
        return Workouts('', '', 0, '')


class WorkoutsSchema(ma.Schema):
    class Meta:
        fields = ['workout_id', 'workout_name', 'description', 'length', 'gym', 'exercises', 'user']
    user = ma.fields.Nested("UsersSchema", exclude=['workouts'])
    exercises = ma.fields.Nested('ExercisesSchema', many=True, exclude=['workouts'])


workout_schema = WorkoutsSchema()
workouts_schema = WorkoutsSchema(many=True)
