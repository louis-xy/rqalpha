import talib as tl
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.ticker as mticker
import matplotlib.dates as dates
import matplotlib.dates as mdates
import datetime

class SAR:
    def __init__(self, stock_data, acceleration=0.02, maximum=0.2):
        high = stock_data['high']
        low = stock_data['low']
        close = stock_data['close']
        date = stock_data['date']
        self.SAR = tl.SAR(high, low, acceleration=acceleration, maximum=maximum)
        self.SAR = pd.Series(self.SAR).sort_index(ascending=False).dropna().reset_index(drop=True)
        self.sz = len(self.SAR)
        self.close = pd.Series(close).sort_index(ascending=False).reset_index(drop=True).head(self.sz)
        self.date = pd.Series(date).sort_index(ascending=False).reset_index(drop=True).head(self.sz)
        #print(low)
        #print(self.SAR)

    def is_red(self, N=0):
        return self.SAR[N] < self.close[N]

    def is_green(self, N=0):
        return self.SAR[N] > self.close[N]

    def is_red_to_green(self, N=0):
        return (self.is_green(N) and self.is_red(N+1))

    def is_green_to_red(self, N=0):
        return (self.is_red(N) and self.is_green(N+1))

    def get_date_by_index(self, N=0):
        return self.date[N]

    def show_sar(self):
        SAR = self.SAR.sort_index(ascending=False).reset_index(drop=True)
        close = self.close.sort_index(ascending=False).reset_index(drop=True)
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
        plt.title('SAR示例图')
        plt.plot(close, color='white')
        plt.scatter(range(len(SAR)), SAR, s=10, color='white')
        #plt.plot(close, color='w')
        plt.legend(['SAR'], loc=2)
        plt.show()


# 获取某支股票的详情
def get_stock_data(stock, count, end_date, unit):
    return jq.get_bars(security=stock, fields=['date','open','high','low','close'], count=count, unit=unit, include_now=False, end_dt=end_date, fq_ref_date=None)

if __name__ == "__main__":
    jq.auth('*****','*****')
    print(jq.get_query_count())
    stock_data = get_stock_data('510300.XSHG', 200, datetime.datetime.now(), '1d')
    sar = SAR(stock_data, 0.02, 0.2)
    sar.show_sar()