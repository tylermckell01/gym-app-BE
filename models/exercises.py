import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma


from db import db
from .workouts_exercises_xref import workouts_exercises_association_table


class Exercises(db.Model):
    __tablename__ = "Exercises"

    exercise_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    exercise_name = db.Column(db.String(), nullable=False, unique=True)
    muscles_worked = db.Column(db.String())

    workouts = db.relationship("Workouts", secondary=workouts_exercises_association_table, back_populates='exercises')

    def __init__(self, exercise_name, muscles_worked):
        self.exercise_name = exercise_name
        self.muscles_worked = muscles_worked

    def new_exercise_obj():
        return Exercises('', '')


class ExercisesSchema(ma.Schema):
    class Meta:
        fields = ['exercise_name', 'muscles_worked', 'exercise_id', 'workouts']
    workouts = ma.fields.Nested('WorkoutsSchema', many=True, exclude=['exercises'])


exercise_schema = ExercisesSchema()
exercises_schema = ExercisesSchema(many=True)
