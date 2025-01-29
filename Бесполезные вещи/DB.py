import sqlalchemy as sqlal # type: ignore


class DB:
    def __init__(self):
        self.engine = sqlal.create_engine('sqlite:///VeloData.db')
        self.conn = self.engine.connect()
        metadata = sqlal.MetaData()
        self.details = sqlal.Table('details', metadata, sqlal.Column('det_id', sqlal.Integer, primary_key=True),
                            sqlal.Column('det_type', sqlal.Text), sqlal.Column('det_name', sqlal.Text),
                            sqlal.Column('det_price', sqlal.Integer), sqlal.Column('det_description', sqlal.Text),
                            sqlal.Column('det_weight', sqlal.Integer), sqlal.Column('det_material', sqlal.Integer),
                            sqlal.Column('det_size', sqlal.Text), sqlal.Column('det_color', sqlal.Text),
                            sqlal.Column('det_manufacture', sqlal.Text), sqlal.Column('det_parameter', sqlal.Text))
        metadata.create_all(self.engine)
        self.conn.close()

    def det_db(self, det, filter, req):
        conn = self.engine.connect()
        if filter == '':
            select_type_que = sqlal.select([self.details]).where(self.details.columns.dt_type=='Вилка')
            select_all_res = conn.execute(select_type_que).fetchall()
        conn.close()
        return select_all_res

    def update_det_db(self, det_id, type, new):
        conn = self.engine.connect()
        update_que = sqlal.update(self.details).where(self.details.columns.det_id==id).values(type=new)
        conn.execute(update_que)
        conn.close()

    def del_det_db(self, det_id):
        conn = self.engine.connect()
        del_que = sqlal.delete(self.details).where(self.details.columns.det_id==det_id)
        conn.execute(del_que)
        conn.close()

    def new_det_db(self, A):
#        conn = self.engine.connect()
        in_que = self.details.insert().values(A)
        self.conn.execute(in_que)
        self.conn.commit()
        self.conn.close()

D = DB
a = input('Вводи параметры в порядке Тип!Имя!Цена!Описание!Вес!Материал!Размер!Цвет!Производитель!ДопПараметры\n')
S, n, ABC = [], {}, ('det_type', 'det_name', 'det_price', 'det_description', 'det_weight', 'det_material', 'det_size',
              'det_color', 'det_manufacture', 'det_parameter')

while a != '':
    for i in range(len(a.split('!'))):
        n[ABC[i]] = a.split('!')[i]
    S.append(n)
    a, n = input(), {}
print(S)
D.new_det_db(D, S)
#Рама!Stern energy 1.0!7000!Рама велосипеда Stern energy 1.0!7000!Аллюминий!1500*100*1000!Синий!Stern!Под прямую вилку, задняя ось эксцентрик, тормоза дисковые