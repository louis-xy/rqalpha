import talib as tl
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.ticker as mticker
import matplotlib.dates as dates
import matplotlib.dates as mdates
import datetime

class MA:
    # 查寻一个时间段内某标的的ma信息
    def __init__(self, stock_data):
        close = stock_data['close']
        date = stock_data['date']
        self.ma = {}
        self.ma['ma01'] = pd.Series(close)
        self.ma['ma05'] = pd.Series(tl.SMA(close, timeperiod=5)).sort_index(ascending=False).dropna()
        self.ma['ma10'] = pd.Series(tl.SMA(close, timeperiod=10)).sort_index(ascending=False).dropna()
        self.ma['ma20'] = pd.Series(tl.SMA(close, timeperiod=20)).sort_index(ascending=False).dropna()
        self.ma['ma30'] = pd.Series(tl.SMA(close, timeperiod=30)).sort_index(ascending=False).dropna()
        self.sz = len(self.ma['ma30'])
        self.ma['ma01'] = self.ma['ma01'].reset_index(drop=True).head(self.sz)
        self.ma['ma05'] = self.ma['ma05'].reset_index(drop=True).head(self.sz)
        self.ma['ma10'] = self.ma['ma10'].reset_index(drop=True).head(self.sz)
        self.ma['ma20'] = self.ma['ma20'].reset_index(drop=True).head(self.sz)
        self.ma['ma30'] = self.ma['ma30'].reset_index(drop=True).head(self.sz)
        self.date = date.sort_index(ascending=False).reset_index(drop=True).head(self.sz)

    def get_date_by_index(self, N=0):
        return self.date[N]

    def is_gold_cross(self, long='ma10', short='ma05', N=0):
        return (self.ma[short][N] > self.ma[long][N] and self.ma[short][N+1] < self.ma[long][N+1])

    def is_death_cross(self, long='ma10', short='ma05', N=0):
        return (self.ma[short][N] < self.ma[long][N] and self.ma[short][N+1] > self.ma[long][N+1])

    # 将macd信息图例化
    def show_ma(self):
        ma05 = self.ma['ma05'].sort_index(ascending=False).reset_index(drop=True)
        ma10 = self.ma['ma10'].sort_index(ascending=False).reset_index(drop=True)
        ma20 = self.ma['ma20'].sort_index(ascending=False).reset_index(drop=True)
        ma30 = self.ma['ma30'].sort_index(ascending=False).reset_index(drop=True)
        date = self.date.sort_index(ascending=False).reset_index(drop=True)

        plt.rcParams['font.sans-serif']=['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus']=False  # 用来正常显示负号
        fig = plt.figure(figsize=(18, 5))
        ax = fig.add_subplot(111)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(ticker.MultipleLocator(3))
        ax.set_xlim([0, len(date)])
        ax.yaxis.grid(color='white', linestyle='--', linewidth=0.5)
        ax.patch.set_facecolor('#303030')
        ax.set_xticklabels(date[i] for i in range(0, len(date), 3))
        plt.xticks(rotation=50)
        plt.title('MA 示例图')
        plt.plot(ma05, color='white')
        plt.plot(ma10, color='red')
        plt.plot(ma20, color='orange')
        plt.plot(ma30, color='blue')
        plt.legend(['MA05', 'MA10', 'MA20', 'MA30'], loc=2)
        plt.show()


# 获取某支股票的详情
def get_stock_data(stock, count, end_date, unit):
    return jq.get_bars(security=stock, fields=['date','open','high','low','close'], count=count, unit=unit, include_now=False, end_dt=end_date, fq_ref_date=None)


if __name__ == "__main__":
    jq.auth('*****','*****')
    stock_data = get_stock_data('510300.XSHG', 200, datetime.datetime.now().date(), '1d')
    ma = MA(stock_data)
    ma.show_ma()