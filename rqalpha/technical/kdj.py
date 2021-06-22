import talib as tl
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.ticker as mticker
import matplotlib.dates as dates
import matplotlib.dates as mdates
import datetime

class KDJ:
    # 查寻一个时间段内某标的的macd信息
    def __init__(self, stock_data, fastk_period, slowk_period, slowd_period):
        high = stock_data['high']
        low = stock_data['low']
        close = stock_data['close']
        date = stock_data['date']
        self.K, self.D = tl.STOCH(high, low, close, fastk_period=fastk_period, slowk_period=slowk_period, slowd_period=slowd_period)
        self.J = 3 * self.K - 2 * self.D
        self.K = self.K.sort_index(ascending=False).dropna().reset_index(drop=True)
        self.D = self.D.sort_index(ascending=False).dropna().reset_index(drop=True)
        self.J = self.J.sort_index(ascending=False).dropna().reset_index(drop=True)
        self.sz = len(self.K)
        self.date = date.sort_index(ascending=False).reset_index(drop=True).head(self.sz)
        self.close = close.sort_index(ascending=False).reset_index(drop=True).head(self.sz)

    def get_date_by_index(self, N=0):
        return self.date[N]

    # 判断往前第N个时段是否为金叉，N取值范围为(0, self.sz)，缺省N=0
    def is_gold_cross(self, N=0):
        return (self.J[N+1] < self.K[N+1] and self.J[N] > self.K[N])

    # 判断往前第N个时段是否为死叉，N取值范围为(0, self.sz)，缺省N=0
    def is_death_cross(self, N=0):
        return (self.J[N+1] > self.K[N+1] and self.J[N] < self.K[N])

    # 我用于建模的方法
    def get_feature_list(self, SZ = 0):
        ret = []
        col = ['kdj_is_gold_cross', 'kdj_is_death_cross']
        for i in range(0, SZ):
            lst = []
            lst.append(self.is_gold_cross(N=i))
            lst.append(self.is_death_cross(N=i))
            ret.append(list(map(int, lst)))
        return pd.DataFrame(ret, columns=col)

    def show_kdj(self):
        K = self.K.sort_index(ascending=False).reset_index(drop=True)
        D = self.D.sort_index(ascending=False).reset_index(drop=True)
        J = self.J.sort_index(ascending=False).reset_index(drop=True)
        #close = self.close.sort_index(ascending=False).reset_index(drop=True)
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
        plt.title('KDJ示例图')
        plt.plot(K, color='orange')
        plt.plot(D, color='pink')
        plt.plot(J, color='white')
        #plt.plot(close, color='w')
        plt.legend(['K', 'D', 'J'], loc=2)
        plt.show()

    # 将KDJ的金叉与死叉
    def show_cross(self):
        K = self.K.sort_index(ascending=False).reset_index(drop=True)
        D = self.D.sort_index(ascending=False).reset_index(drop=True)
        J = self.J.sort_index(ascending=False).reset_index(drop=True)
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
        plt.title('KDJ 金叉死叉示例图')
        plt.xticks(rotation=50)
        plt.plot(K, color='orange')
        plt.plot(D, color='pink')
        plt.plot(J, color='white')
        for i in range(1, len(K)):
            if J[i-1] < K[i-1] and J[i] > K[i]:
                # 用红圈标出金叉
                plt.scatter(i, J[i], color='', marker='o', edgecolors='red', s=150, linewidths=1.5)
            elif J[i-1] > K[i-1] and J[i] < K[i]:
                # 用绿圈标出死叉
                plt.scatter(i, J[i], color='', marker='o', edgecolors='green', s=150, linewidths=1.5)
        plt.legend(['K', 'D', 'J'], loc=2)
        plt.show()


# 获取某支股票的详情

if __name__ == "__main__":
    stock_data = get_stock_data('510300.XSHG', 100, datetime.datetime.now(), '1d')
    kdj = KDJ(stock_data, 9, 3, 3)
    kdj.show_kdj()