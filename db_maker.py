from sqlalchemy import create_engine, select, Table, Column, Integer, Float, Date, String, MetaData, ForeignKey
import os


meta = MetaData()
user = os.environ['user']
password = os.environ['password']

stocks = Table('Stocks', meta,
               Column('id_stock', Integer, primary_key=True),
               Column('name', String(250), nullable=False))

tradings = Table('Tradings', meta,
                 Column('id_stock', Integer, ForeignKey("Stocks.id_stock")),
                 Column('id_date', Integer),
                 Column('date', Date),
                 Column('Open', Float),
                 Column('High', Float),
                 Column('Low', Float),
                 Column('Volume', Float))


# Подключаемся к БД и заносим данные
# СУБД+драйвер://юзер:пароль@хост:порт/база
engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@localhost:3306/test_tradings", echo=True)
meta.create_all(engine)
ins = stocks.insert().values(name='APPL')
conn = engine.connect()
ins2 = tradings.insert().values(id_date='1', date='01-01-2015', Open=2.4, High=2.6, Low=2.2, Volume=200)
conn.execute(ins)
conn.execute(ins2)


