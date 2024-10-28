import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID
from db import db


class Users(db.Model):
    __tablename__ = "Users"

    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    role = db.Column(db.String(), nullable=False)
    active = db.Column(db.Boolean(), default=True)

    auth = db.relationship("AuthTokens", back_populates="user")
    workouts = db.relationship("Workouts", back_populates="user", cascade="all")

    def __init__(self, first_name, last_name, email, password, role, active):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.role = role
        self.active = active

    def get_new_user():
        return Users('', '', '', '', '', True)


class UsersSchema(ma.Schema):
    class Meta:
        fields = ['user_id', 'first_name', 'last_name', 'role', 'email', 'active', 'workouts']
    workouts = ma.fields.Nested('WorkoutsSchema', many=True, exclude=['user'])


user_schema = UsersSchema()
users_schema = UsersSchema(many=True)
