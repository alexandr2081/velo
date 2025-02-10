import json
import sqlalchemy as sqlal # type: ignore
from .db_session import SqlAlchemyBase


class Detail(SqlAlchemyBase):
    __tablename__ = 'details'

    id = sqlal.Column(sqlal.Integer, primary_key=True, autoincrement=True)
    type = sqlal.Column(sqlal.SMALLINT)
    name = sqlal.Column(sqlal.String, unique=True)
    price = sqlal.Column(sqlal.Integer)
    descript = sqlal.Column(sqlal.String)
    weight = sqlal.Column(sqlal.SMALLINT)
    material = sqlal.Column(sqlal.SMALLINT)
    color = sqlal.Column(sqlal.SMALLINT)
    manufacture = sqlal.Column(sqlal.SMALLINT)
    img = sqlal.Column(sqlal.String, nullable=True)
    img_velo = sqlal.Column(sqlal.String, nullable=True)
    available = sqlal.Column(sqlal.SMALLINT)
    level = sqlal.Column(sqlal.SMALLINT)
    param = sqlal.Column(sqlal.String, nullable=True)

    def __str__(self):
        with open('./static/chars.json', 'r', encoding='utf-8') as ch, open('./static/types.json', 'r', encoding='utf-8') as ty:
            ch, ty, lam = json.load(ch), list(json.load(ty).keys())[self.type], lambda x, y, z: list(x[y].keys())[z]
            return "{" + """"id": "{}", "type": "{}", "name": "{}", "price": "{}", "descript": "{}", "weight": "{}", "material": "{}", "color": "{}", "manufacture": "{}", "img": "{}", "img_": "{}", "available": "{}", "level": "{}", "param": {}""".format(
                self.id, ty, self.name, self.price, self.descript, self.weight, lam(ch, "material", self.material), ch["color"][self.color],
                lam(ch, "manufacture", self.manufacture), self.img, self.img_velo, self.available, lam(ch, "level", self.level), self.param.split("~")).replace("\'", '"') + "}"
