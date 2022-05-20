from sqlalchemy import Column, Integer, Float, Date, Boolean, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy_utils import database_exists, create_database
import datetime
import os
import loader

base = declarative_base()


class Stock(base):
    __tablename__ = 'stocks'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    begin_date = Column(Date)
    end_date = Column(Date)

    def __init__(self, name, begin_date, end_date):
        self.name = name
        self.begin_date = begin_date
        self.end_date = end_date

    def __repr__(self):
        return f"<Stocks(name={self.name}, " \
               f"begin_date={self.begin_date}," \
               f" end_date={self.end_date})>"


class Database(base):
    __tablename__ = 'database'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    from_date = Column(Date)
    till_date = Column(Date)

    def __init__(self, name, from_date, till_date):
        self.name = name
        self.from_date = from_date
        self.till_date = till_date

    def __repr_(self):
        return f"Database(name={self.name}, " \
               f"from_date={self.from_date}, " \
               f"till_date={self.till_date})"


class Trading(base):
    __tablename__ = 'tradings'

    id = Column(Integer, primary_key=True)
    id_st = Column(Integer, ForeignKey('database.id'))
    all_period_st = Column(Boolean)
    date = Column(Date)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    volume = Column(Integer)

    def __init__(self, id_st, all_period_st, date, open, high, low, volume):
        self.id_st = id_st
        self.all_period_st = all_period_st
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.volume = volume

    def __repr__(self):
        return f"Tradings(id_st={self.id_st}," \
               f" all_period_st={self.all_period_st}, " \
               f"date={self.date}," \
               f" open={self.open}," \
               f" high={self.high}," \
               f" low={self.low}," \
               f" volume={self.volume})"


user = os.environ['user']
password = os.environ['password']
path = os.environ['path']
name_of_db = 'test'

# Подключаемся к БД
# СУБД+драйвер://юзер:пароль@хост:порт/база
connection_string = f'mysql+pymysql://{user}:{password}@localhost:3306/{name_of_db}'
engine = create_engine(connection_string, echo=True)
# Session = sessionmaker(bind=engine, autoflush=False)
session = Session(bind=engine, autoflush=False)

base.metadata.create_all(engine)


def create_db():
    base.metadata.create_all(engine)


def update_list_of_stocks():
    dict_stocks = loader.form_dict_of_stocks()
    engine.execute('TRUNCATE TABLE stocks')
    for x in dict_stocks:
        session.add(Stock(name=x, begin_date=dict_stocks[x][0], end_date=dict_stocks[x][1]))
        session.commit()


def query_current_list_stocks():
    return


def get_current_list_stocks():
    result = session.query(Stock.name).all()
    mas = []
    for i in range(len(result)):
        x = str(result[i])
        x = x[2:-3]
        mas.append(x)
    return mas


def get_begin_end_date(name_of_stock: str):
    begin = session.query(Stock).filter_by(name=name_of_stock).all()
    '''for i in range(len(result)):
        result[i] = result[i].isoformat()'''
    print(type(begin))
    print(len(begin))
    mas = begin[0].__dict__
    return [mas['begin_date'], mas['end_date']]


def add_to_db(name: str, from_date: datetime.date, to_date: datetime.date):
    list = loader.download_stock(name, from_date, to_date)














