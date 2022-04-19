from sqlalchemy import create_engine, select, Table, Column, Integer, Float, Date, String, MetaData, ForeignKey
import loader
import os


meta = MetaData()
user = os.environ['user']
password = os.environ['password']

stocks = Table(
    'Stocks', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(32)),
    Column('from_date', Date),
    Column('to_date', Date)
)

database = Table(
    'Database', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(32)),
    Column('from_dt', Date),
    Column('till_dt', Date)
)

tradings = Table(
    'Tradings', meta,
    Column('id', Integer, primary_key=True),
    Column('id_st', Integer, ForeignKey('Database.id')),
    Column('date', Date),
    Column('Open', Float),
    Column('High', Float),
    Column('Low', Float),
    Column('Volume', Float)
)

# Подключаемся к БД и заносим данные
# СУБД+драйвер://юзер:пароль@хост:порт/база
def connect_to_db():
    engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@localhost:3306/test_tradings", echo=True)
    meta.create_all(engine)
    return engine.connect()


def update_list_of_stocks():
    conn = connect_to_db()
    delete = stocks.delete()
    conn.execute(delete)
    dict_stocks = loader.form_dict_of_stocks()
    for x in dict_stocks:
        ins_stock = stocks.insert().values(name=x, from_date=dict_stocks[x][0], to_date=dict_stocks[x][1])
        conn.execute(ins_stock)


def add_to_db(name, from_date, to_date):
    pass








