from sqlalchemy import Column, Integer, Float, Date, Boolean, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import delete
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
    all_period = Column(Boolean)
    from_date = Column(Date)
    till_date = Column(Date)

    def __init__(self, name, all_period, from_date, till_date):
        self.name = name
        self.all_period = all_period
        self.from_date = from_date
        self.till_date = till_date

    def __repr_(self):
        return f"Database(name={self.name}, " \
               f"all_period={self.all_period}" \
               f"from_date={self.from_date}, " \
               f"till_date={self.till_date})"


class Trading(base):
    __tablename__ = 'tradings'

    id = Column(Integer, primary_key=True)
    name_st = Column(String(100))
    all_period_st = Column(Boolean)
    date = Column(Date)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)

    def __init__(self, name_st, all_period_st, date, open, high, low, close):
        self.name_st = name_st
        self.all_period_st = all_period_st
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.close = close

    def __repr__(self):
        return f"Tradings(name_st={self.name_st}," \
               f" all_period_st={self.all_period_st}, " \
               f"date={self.date}," \
               f" open={self.open}," \
               f" high={self.high}," \
               f" low={self.low}," \
               f" close={self.close},"


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


def create_db():
    base.metadata.create_all(engine)


def delete_tables():
    session.commit()
    Trading.__table__.drop(engine, checkfirst=True)
    Database.__table__.drop(engine, checkfirst=True)


def update_list_of_stocks():
    dict_stocks = loader.form_dict_of_stocks()
    for x in dict_stocks:
        session.add(Stock(name=x, begin_date=dict_stocks[x][0], end_date=dict_stocks[x][1]))
        session.commit()


def truncate_table_stocks():
    stocks = session.query(Stock).where(Stock.id > 0)
    stocks.delete()


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
    mas = begin[0].__dict__
    # return [datetime.datetime.strptime(mas['begin_date'], '%Y-%m-%d'),
    #         datetime.datetime.strptime(mas['end_date'], '%Y-%m-%d')]
    return [mas['begin_date'], mas['end_date']]


def get_current_list_database():
    result = session.query(Database).all()
    mas = []
    for x in result:
        q = x.__dict__
        lst = list()
        lst.append(q['id'])
        lst.append(q['name'])
        lst.append(q['all_period'])
        lst.append(q['from_date'].isoformat())
        lst.append(q['till_date'].isoformat())
        mas.append(lst)
    return mas


def get_current_list_tradings():
    result = session.query(Trading).all()
    mas = []
    for x in result:
        q = x.__dict__
        lst = list()
        lst.append(q['id'])
        lst.append(q['name_st'])
        lst.append(q['all_period_st'])
        lst.append(q['date'].isoformat())
        lst.append(q['open'])
        lst.append(q['high'])
        lst.append(q['low'])
        lst.append(q['close'])
        if lst not in mas:
            mas.append(lst)
    return mas


def add_to_db(name: str, all_period: bool, from_date: datetime.date, to_date: datetime.date):
    session.add(Database(name=name, all_period=all_period, from_date=from_date, till_date=to_date))
    session.commit()
    add_to_tradings(name, all_period, from_date, to_date)


def add_to_tradings(name: str, all_period: bool, from_date: datetime.date, to_date: datetime.date):
    mas = loader.download_stock(name, from_date, to_date)
    for i in range(1, len(mas)):
        session.add(Trading(name_st=name,
                            all_period_st=all_period,
                            date=mas[i][0],
                            open=mas[i][1],
                            high=mas[i][2],
                            low=mas[i][3],
                            close=mas[i][4]))
        session.commit()


def actualize():
    mas = get_current_list_database()
    for x in mas:
        if x[2] == 1:
            begin_end = get_begin_end_date(x[1])
            if x[4] != str(begin_end[1]):
                new_begin = datetime.datetime.strptime(x[4], "%Y-%m-%d") + datetime.timedelta(days=1)
                add_to_tradings(x[1], x[2], new_begin, begin_end[1])
                row = session.query(Database).filter_by(name=x[1],
                                                        all_period=x[2],
                                                        from_date=x[3],
                                                        till_date=x[4]).first()
                row.till_date = begin_end[1]
                session.add(row)
                session.commit()














