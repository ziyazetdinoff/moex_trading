import yfinance as yf
import pandas as pd
import requests
import apimoex

import datetime


def form_dict_of_stocks() -> dict:
    request_url_imoex = "https://iss.moex.com/iss/statistics/engines/stock/markets/index/analytics/IMOEX/tickers.json"
    request_url_imoex2 = "https://iss.moex.com/iss/statistics/engines/stock/markets/index/analytics/IMOEX2/tickers.json"
    request_url_rtsi = "https://iss.moex.com/iss/statistics/engines/stock/markets/index/analytics/RTSI/tickers.json"

    dict_stocks = {}
    with requests.Session() as session:
        iss = apimoex.ISSClient(session, request_url_imoex)
        data_imoex = iss.get()
        iss = apimoex.ISSClient(session, request_url_rtsi)
        data_rtsi = iss.get()
        iss = apimoex.ISSClient(session, request_url_imoex2)
        data_imoex2 = iss.get()

    for x in data_imoex['tickers']:
        if x['ticker'] not in dict_stocks:
            mas = [x['from'], x['till']]
            dict_stocks[x['ticker']] = mas
    for x in data_imoex2['tickers']:
        if x['ticker'] not in dict_stocks:
            mas = [x['from'], x['till']]
            dict_stocks[x['ticker']] = mas
    for x in data_rtsi['tickers']:
        if x['ticker'] not in dict_stocks:
            mas = [x['from'], x['till']]
            dict_stocks[x['ticker']] = mas
    return dict_stocks


def download_stock(name: str, from_date: datetime.date, to_date: datetime.date) -> list:
    data = yf.download(name + '.ME', from_date, to_date)
    mas = [data.columns.tolist()] + data.reset_index().values.tolist()
    for i in range(1, len(mas)):
        mas[i][0] = mas[i][0].to_pydatetime().date()
        mas[i][0] = mas[i][0].isoformat()
    return mas








