import sqlalchemy as sqlal
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlal.Column(sqlal.Integer, primary_key=True, autoincrement=True)
    name = sqlal.Column(sqlal.String)
    email = sqlal.Column(sqlal.String, unique=True)
    hashed_password = sqlal.Column(sqlal.String)
    builds = sqlal.orm.relationship("Build", back_populates='user')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
