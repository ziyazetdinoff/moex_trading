import yfinance as yf
import pandas as pd


''' class Stock(name="", from_date="", to_date=""):
    def __init__ (self):
        self.data = yf.download(name, from_date, to_date)
'''


data = yf.download('TTLK.ME', '2022-01-01', '2022-02-01')
pd.set_option("display.max.columns", None)
print(data.head(3))
mas = []
print("---------------")
# for i in range(6):
 #   mas.append(data.iloc[0][i])
print(data.iloc[:, 0])
print(data.axes[0])


