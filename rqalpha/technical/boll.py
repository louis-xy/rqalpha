import jqdatasdk as jq
import talib as tl
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.ticker as mticker
import matplotlib.dates as dates
import matplotlib.dates as mdates
import datetime

class BOLL:
    # 查寻一个时间段内某标的的macd信息
    def __init__(self, stock_data, timeperiod, nbdevup, nbdevdn, matype):
        close = stock_data['close']
        date = stock_data['date']
        self.upper, self.middle, self.lower = tl.BBANDS(close, timeperiod=timeperiod, nbdevup=nbdevup, nbdevdn=nbdevdn, matype=matype)
        self.upper = self.upper.sort_index(ascending=False).dropna().reset_index(drop=True)
        self.middle = self.middle.sort_index(ascending=False).dropna().reset_index(drop=True)
        self.lower = self.lower.sort_index(ascending=False).dropna().reset_index(drop=True)
        self.sz = len(self.upper)
        self.date = date.sort_index(ascending=False).reset_index(drop=True).head(self.sz)
        self.close = close.sort_index(ascending=False).reset_index(drop=True).head(self.sz)

    def get_date_by_index(self, N=0):
        return self.date[N]

    # 判断往前第N个时段是否为金叉，N取值范围为(0, self.sz)，缺省N=0
    def is_gold_cross(self, N=0):
        return (self.close[N+1] < self.upper[N+1] and self.close[N] > self.upper[N])

    # 判断往前第N个时段是否为死叉，N取值范围为(0, self.sz)，缺省N=0
    def is_death_cross(self, N=0):
        return (self.close[N+1] > self.upper[N+1] and self.close[N] < self.upper[N])

    def is_all_increase(self, N=0):
        return (self.upper[N] > self.upper[N+1] and self.middle[N] > self.middle[N+1] and self.lower[N] > self.lower[N+1])

    def is_all_decrease(self, N=0):
        return (self.upper[N] < self.upper[N+1] and self.middle[N] < self.middle[N+1] and self.lower[N] < self.lower[N+1])

    def is_expand(self, N=0):
        return (self.upper[N] > self.upper[N+1] and self.lower[N] < self.lower[N+1])

    def is_shrink(self, N=0):
        return (self.upper[N] < self.upper[N+1] and self.lower[N] > self.lower[N+1])


    def show_boll(self):
        upper = self.upper.sort_index(ascending=False).reset_index(drop=True)
        middle = self.middle.sort_index(ascending=False).reset_index(drop=True)
        lower = self.lower.sort_index(ascending=False).reset_index(drop=True)
        close = self.close.sort_index(ascending=False).reset_index(drop=True)
        date = self.date.sort_index(ascending=False).reset_index(drop=True)
        plt.rcParams['font.sans-serif']=['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus']=False  # 用来正常显示负号
        fig = plt.figure(figsize=(18, 8))
        ax = fig.add_subplot(111)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(ticker.MultipleLocator(50))
        ax.set_xlim([0, len(date)])
        ax.yaxis.grid(color='white', linestyle='--', linewidth=0.5)
        ax.patch.set_facecolor('#303030')
        ax.set_xticklabels(date[i] for i in range(0, len(date), 50))
        plt.xticks(rotation=50)
        plt.title('布林带示例图')
        plt.plot(upper)
        plt.plot(middle)
        plt.plot(lower)
        plt.plot(close, color='w')
        plt.legend(['upper', 'middle', 'lower', 'close'], loc=2)
        plt.show()

# 获取某支股票的详情
def get_stock_data(stock, count, end_date, unit):
    return jq.get_bars(security=stock, fields=['date','open','high','low','close'], count=count, unit=unit, include_now=False, end_dt=end_date, fq_ref_date=None)

if __name__ == "__main__":
    jq.auth('*****','*****')
    print(jq.get_query_count())
    stock_data = get_stock_data('510300.XSHG', 200, datetime.datetime.now().date(), '1d')
    boll = BOLL(stock_data, 20, 2, 2, 0)
    boll.show_boll()