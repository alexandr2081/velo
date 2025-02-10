import sqlalchemy as sqlal
import sqlalchemy.orm as orm


SqlAlchemyBase = orm.declarative_base()
__factory = None

def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn}")

    engine = sqlal.create_engine(conn, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)

def create_session() -> orm.Session:
    global __factory
    return __factory()

class News(SqlAlchemyBase):
    __tablename__ = 'details'

    id = sqlal.Column(sqlal.Integer, primary_key=True, autoincrement=True)
    title = sqlal.Column(sqlal.String, nullable=True)
    content = sqlal.Column(sqlal.String, nullable=True)
    created_date = sqlal.Column(sqlal.DateTime, default=)
    is_private = sqlal.Column(sqlal.Boolean, default=True)