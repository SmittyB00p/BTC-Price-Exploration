import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import pathlib
import datetime
import yfinance as yf
from utils.metrics import Metrics

yf.AsyncWebSocket().subscribe('BTC-USD')

todays_date = datetime.date.today()

class MomentumBacktest():
    def __init__(self,
                 symbol=str(),
                 start:str = todays_date,
                 end:str = None,
                 interval='1d',
                 trans_cost:float = 0.0,
                 amount=float):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.interval = interval
        self.trans_cost = trans_cost
        self.amount = amount
        self.results = None
        self.get_data()

    def get_data(self):
        data = yf.download(tickers=self.symbol,
                           start=self.start,
                           end=self.end,
                           interval=self.interval,
                           multi_level_index=False,
                           )
        data['returns'] = data['Close'].pct_change() + 1
        data['log_returns'] = np.log(data['returns'])
        
        self.data = data

    def strategy(self, momentum:float = 1):
        self.momentum = momentum

        data = self.data.copy().dropna()
        data['close_sign'] = np.sign(data['log_returns'].rolling(momentum).mean())
        data['strategy'] = data['log_returns'] * data['close_sign'].shift(1)

        # determines trade signal
        data.dropna(inplace=True)
        trades = data['close_sign'].diff().fillna(0) != 0 ## creates boolean mask where the difference between days indicates a trade signal

        self.trans_cost = self.trans_cost/self.amount ## percentage per amount???

        data.loc[trades, 'strategy'] -= self.trans_cost ## using the trades series this selects which days of the strategy to reduce the transaction cost by
        # num_costs = len(data['strategy'][trades]) ## total number of transactions throughout given period...will be subtracted from cumulative returns of strategy

        self.cum_returns = np.exp(data['log_returns'].cumsum())
        self.cum_returns_trend = np.exp(data['strategy'].cumsum())
        # if self.trans_cost == None:
        #     self.cum_returns_trend = np.exp(data['strategy'].cumsum())
        # self.cum_returns_trend = np.exp(data['strategy'].cumsum()) - num_costs*self.trans_cost

        data['creturns'] = self.amount * self.cum_returns
        data['cstrategy'] = self.amount * self.cum_returns_trend
        # data['cstrategy'] = (self.amount * np.exp(data['strategy'].cumsum())) - num_costs*self.trans_cost
        self.results = data

        # performance of strategy
        cperf = self.results['creturns'].iloc[-1]
        sperf = self.results['cstrategy'].iloc[-1]

        return round(cperf, 2), round(sperf, 2)
    
    def plot_strategy(self):
        if self.results is None:
            print(f'No strategy implemented. Please run a {MomentumBacktest.__name__} strategy.')
        else:
            self.results[['creturns', 'cstrategy']].plot(kind='line',
                                                      label=['Cumulative Returns', 'Strategy'],
                                                      title=f"Momentum Strategy using a {self.momentum} day rolling average\nTransaction Cost: ${self.trans_cost}/transaction",
                                                      ylabel='Price ($)',
                                                      xlabel='Date',
                                                      grid=True
                                                      )

    def get_terminal_return(self):
        terminal_return = (self.cum_returns - 1).tolist()[-1]
        terminal_returnl_trend = (self.cum_returns_trend - 1).tolist()[-1]

        return round(terminal_return, 2), round(terminal_returnl_trend, 2)

    def get_annualized_return(self):
        annualized_return = Metrics.annualized_return(self.results['log_returns'])
        annualized_return_trend = Metrics.annualized_return(self.results['strategy'])

        return round(annualized_return, 2), round(annualized_return_trend, 2)
    
    def get_volatility(self):
        volatility = Metrics.volatility(self.cum_returns)
        volatility_trend = Metrics.volatility(self.cum_returns_trend)

        return round(volatility, 2), round(volatility_trend, 2)
    
    def get_sharpe_ratio(self,
                         annualized_return,
                         annualized_volatility,
                         risk_free_rate:float= 0.0):
        return Metrics.sharpe_ratio(annualized_returns=annualized_return,
                                    annualized_volatility=annualized_volatility,
                                    risk_free_rate=risk_free_rate)



class MovingAverageBackTest(MomentumBacktest):

    def strategy(self, sma1, sma2):
        self.sma1 = sma1
        self.sma2 = sma2

        data = self.data.copy().dropna()
        data['SMA-short'] = data['Close'].rolling(self.sma1).mean()
        data['SMA-long'] = data['Close'].rolling(self.sma2).mean()

        ## buy signal
        data['signal'] = np.where(data['SMA-short'] > data['SMA-long'], 1, 0)

        ## sell signal
        data['signal'] = np.where(data['SMA-short'] < data['SMA-long'], -1, data['signal'])

        data.dropna(inplace=True)

        data['strategy'] = data['signal'] * data['log_returns']
        trades = data['signal'].diff().fillna(0) != 0

        self.trans_cost = self.trans_cost/self.amount
        data.loc[trades, 'strategy'] -= self.trans_cost

        self.cum_returns = np.exp(data['log_returns'].cumsum())
        self.cum_returns_trend = np.exp(data['strategy'].cumsum())

        ## multiplies the amount invested with the cumulative returns
        data['creturns'] = self.amount * self.cum_returns
        data['cstrategy'] = self.amount * self.cum_returns_trend
        self.results = data

        # performance of strategy
        cperf = self.results['creturns'].iloc[-1]
        sperf = self.results['cstrategy'].iloc[-1]

        return round(cperf, 2), round(sperf, 2)

    def plot_strategy(self):
        if self.results is None:
            print(f'No strategy implemented. Please run a {MovingAverageBackTest.__name__} strategy.')
        else:
            self.results[['creturns', 'cstrategy']].plot(kind='line',
                                                      label=['Cumulative Returns', 'Strategy'],
                                                      title=f"Moving Average Strategy using a {self.sma1}- and {self.sma2}-day moving average\nTransaction Cost: ${self.trans_cost}/transaction",
                                                      ylabel='Price ($)',
                                                      xlabel='Date',
                                                      grid=True
                                                      )


# if __name__ == '__main__':