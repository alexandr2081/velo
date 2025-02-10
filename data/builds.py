import sqlalchemy as sqlal
from .db_session import SqlAlchemyBase


class Build(SqlAlchemyBase):
    __tablename__ = 'builds'

    id = sqlal.Column(sqlal.Integer, primary_key=True, autoincrement=True)
    name = sqlal.Column(sqlal.String)
    details = sqlal.Column(sqlal.String, nullable=True)
    
    is_open = sqlal.Column(sqlal.Boolean)
    user_name = sqlal.Column(sqlal.String, sqlal.ForeignKey("users.name"), nullable=True)
    user = sqlal.orm.relationship('User')

    def __str__(self):
        return "{" + '''"id": "{}", "name": "{}", "details": {}, "is_open": "{}", "user_name": "{}"'''.format(
            self.id, self.name, self.details.split(), self.is_open, self.user_name).replace("\'", '"') + "}"
