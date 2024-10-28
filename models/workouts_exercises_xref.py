from db import db

workouts_exercises_association_table = db.Table(
    "WorkoutsExercisesAssociation",
    db.Model.metadata,
    db.Column("workout_id", db.ForeignKey("Workouts.workout_id", ondelete='CASCADE'), primary_key=True),
    db.Column("exercise_id", db.ForeignKey("Exercises.exercise_id", ondelete='CASCADE'), primary_key=True)
)
